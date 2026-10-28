from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.auth_service import AuthService
from app.auth.confirmation.policy import ConfirmationPolicy, NoConfirmation, RequiredConfirmation
from app.auth.confirmation.service import EmailConfirmService
from app.auth.confirmation.tokens import ConfirmTokenRepository
from app.auth.sessions.service import SessionService
from app.db import schemas
from app.db.deps import get_db
from app.deps import get_app_settings
from app.email_utils.deps import get_sender_service
from app.email_utils.sender_service import SenderService
from app.repositories.user_repository import UserRepository
from app.security.cred_codec import UserCredentialsCodec
from app.security.deps import get_credentials_codec
from app.security.fields.base import DataEncryptor
from app.security.fields.string_field_schemes import StringAesSivScheme
from app.services.deps import get_user_repository, get_user_service
from app.services.user_service import UserService
from app.settings import AppSettings
from app.util.exceptions import EmailNotConfirmedException, UserBannedException


def get_confirm_token_repository(
        db: Annotated[Session, Depends(get_db)],
):
    return ConfirmTokenRepository(db)


def get_email_confirm_service(
        db: Annotated[Session, Depends(get_db)],
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
        users: Annotated[UserService, Depends(get_user_service)],
        confirm_token_repository: Annotated[ConfirmTokenRepository, Depends(get_confirm_token_repository)],
        sender_service: Annotated[SenderService, Depends(get_sender_service)]
) -> EmailConfirmService | None:
    if cfg.auth.CONFIRM_EMAIL_ENABLED:
        encryptor_schemes = {"v1": StringAesSivScheme(cfg.auth.CONFIRM_TOKEN_SECRET_KEY)}
        return EmailConfirmService(
            db,
            DataEncryptor(encryptor_schemes, "v1"),
            users,
            confirm_token_repository,
            sender_service,
        )
    return None


def get_confirm_policy(
        email_confirm_service: Annotated[EmailConfirmService | None, Depends(get_email_confirm_service)],
):
    return RequiredConfirmation(email_confirm_service) \
        if email_confirm_service is not None \
        else NoConfirmation()


def get_session_service(
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return SessionService(cfg.auth, user_repository)


def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        cred_codec: Annotated[UserCredentialsCodec, Depends(get_credentials_codec)],
        policy: Annotated[ConfirmationPolicy, Depends(get_confirm_policy)],
        tokens: Annotated[SessionService, Depends(get_session_service)],
):
    return AuthService(user_repository, cred_codec, policy, tokens)


bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Security(bearer_scheme)],
        tokens: Annotated[SessionService, Depends(get_session_service)],
        confirm_policy: Annotated[ConfirmationPolicy, Depends(get_confirm_policy)],
) -> schemas.User:
    token = credentials.credentials
    user = tokens.extract_access_token(token)
    if user.banned:
        raise UserBannedException()
    if confirm_policy.required and not user.confirmed:
        raise EmailNotConfirmedException()

    return user
