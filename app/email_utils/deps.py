from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.email_utils.renderer_service import RendererService
from app.email_utils.sender_service import SenderService
from app.settings import AppSettings
from deps import get_app_settings


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


def get_renderer_service():
    return RendererService()


def get_sender_service(
        renderer_service: Annotated[RendererService, Depends(get_renderer_service)],
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
):
    return SenderService(
        renderer_service,
        cfg.sender,
        cfg.shared,
    )
