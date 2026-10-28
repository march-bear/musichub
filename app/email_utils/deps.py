from typing import Annotated

from fastapi import Depends

from app.deps import get_app_settings
from app.email_utils.renderer_service import RendererService
from app.email_utils.sender_service import SenderService
from app.settings import AppSettings


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
