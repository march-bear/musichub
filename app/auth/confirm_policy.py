from typing import Protocol

from app.auth.email_confirm import EmailConfirmService


class ConfirmationPolicy(Protocol):
    @property
    def required(self) -> bool: ...
    async def on_registered(self, user_id: int, email: str) -> None: ...


class RequiredConfirmation:
    required = True

    def __init__(self, confirm_service: EmailConfirmService):
        self.confirm_service = confirm_service


    async def on_registered(self, user_id: int, email: str) -> None:
        await self.confirm_service.send_confirmation_email(user_id, email)


class NoConfirmation:
    required = False

    async def on_registered(self, user_id: int, email: str) -> None:
        pass
