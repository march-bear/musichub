from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.data import schemas
from app.data.database import SessionLocal
from app.data.object_storage import s3, s3_public
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.project_conv_service import ProjectConvService
from app.services.project_saver_service import ProjectSaverService
from app.services.project_service import ProjectService
from app.services.security_service import SecurityService
from app.services.storage_service import StorageService
from app.services.user_service import UserService
from app.settings import settings
from app.util.exceptions import EmailNotConfirmedException, UserBannedException

if settings.EMAIL_CHECK_ENABLED:
    from app.services.auth_service import AuthService, EmailConfirmationService

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Annotated[Session, Depends(get_db)]):
    return ProjectService(db)


def get_project_conv_service(soundfont: str = settings.APP_SOUNDFONT):
    return ProjectConvService(soundfont)


def get_storage_service():
    return StorageService(s3, s3_public)


def get_project_saver_service(
        pc_service: Annotated[ProjectConvService, Depends(get_project_conv_service)],
        p_service: Annotated[ProjectService, Depends(get_project_service)],
        storage_service: Annotated[StorageService, Depends(get_storage_service)]
):
    return ProjectSaverService(pc_service, p_service, storage_service)


def get_security_service():
    return SecurityService()


def get_user_service(
        db: Annotated[Session, Depends(get_db)],
        security_service: Annotated[SecurityService, Depends(get_security_service)]
):
    return UserService(db, security_service)


def get_auth_service(
        user_service: Annotated[UserService, Depends(get_user_service)],
        email_confirmation_service: Annotated[EmailConfirmationService, Depends(get_email_confirmation_service)],
):
    return AuthService(user_service, email_confirmation_service)


bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Security(bearer_scheme)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> schemas.User:
    token = credentials.credentials
    user = auth_service.extract_token(token)
    if user.banned:
        raise UserBannedException()
    if settings.EMAIL_CHECK_ENABLED and not user.confirmed:
        raise EmailNotConfirmedException()

    return user


def get_email_confirmation_service(
        db: Annotated[Session, Depends(get_db)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        security_service: Annotated[SecurityService, Depends(get_security_service)]
):
    if settings.EMAIL_CHECK_ENABLED:
        return EmailConfirmationService(db, security_service, user_service)
    return None


def get_email_service():
    return EmailService()
