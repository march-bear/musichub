from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.deps import get_app_settings
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.security.cred_codec import UserCredentialsCodec
from app.security.deps import get_credentials_codec
from app.services.project_conv_service import ProjectConvService
from app.services.project_saver_service import ProjectSaverService
from app.services.project_service import ProjectService
from app.services.user_service import UserService
from app.settings import AppSettings
from app.storage.deps import get_projects_storage
from app.storage.s3_storage import S3Storage


def get_project_repository(db: Annotated[Session, Depends(get_db)]) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_service(
        db: Annotated[Session, Depends(get_db)],
        project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
):
    return ProjectService(db, project_repository)


def get_project_conv_service(
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
):
    return ProjectConvService(cfg.shared.SOUNDFONT)


def get_project_saver_service(
        pc_service: Annotated[ProjectConvService, Depends(get_project_conv_service)],
        p_service: Annotated[ProjectService, Depends(get_project_service)],
        p_storage: Annotated[S3Storage, Depends(get_projects_storage)],
):
    return ProjectSaverService(pc_service, p_service, p_storage)


def get_user_repository(
        db: Annotated[Session, Depends(get_db)],
):
    return UserRepository(db)


def get_user_service(
        db: Annotated[Session, Depends(get_db)],
        cred_codec: Annotated[UserCredentialsCodec, Depends(get_credentials_codec)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(db, cred_codec, user_repository)
