from pydantic import EmailStr

from app.services.user_service import UserService
from app.auth.confirmation.policy import ConfirmationPolicy


class RegisterService:
    def __init__(self, user_service: UserService, confirm_policy: ConfirmationPolicy):
        self._user_service = user_service
        self._confirm_policy = confirm_policy


    def register(self, email: EmailStr, password: str):
        user = self._user_service.create(email, password)
        return user


    async def send_confirmation(self, user_id: int, email: EmailStr) -> None:
        await self._confirm_policy.on_registered(user_id, email)
