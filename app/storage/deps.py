from typing import Annotated

from fastapi import Depends

from app.deps import get_app_settings
from app.settings import AppSettings
from app.storage.s3_storage import S3Storage, create_s3_client


def get_projects_storage(
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
):
    return S3Storage(
        create_s3_client(
            f"{cfg.storage.HOST}:{cfg.storage.PORT}",
            cfg.storage.ACCESS_KEY,
            cfg.storage.SECRET_KEY,
        ),
        create_s3_client(
            cfg.storage.PUBLIC_URL,
            cfg.storage.ACCESS_KEY,
            cfg.storage.SECRET_KEY,
        ),
        "projects",
        cfg.storage.URL_EXPIRES_IN_TIME,
    )
