import secrets

from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.util.exceptions import InvalidConfirmationTokenException
from auth.confirm_tokens import ConfirmTokenRepository
from email_utils.sender_service import SenderService
from security.fields.base import DataEncryptor


class EmailConfirmService:
    def __init__(
            self,
            db: Session,
            encryptor: DataEncryptor,
            user_service: UserService,
            confirms: ConfirmTokenRepository,
            sender: SenderService
    ):
        self.db = db
        self.encryptor = encryptor
        self.user_service = user_service
        self.confirms = confirms
        self.sender = sender


    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)


    async def send_confirmation_email(self, user_id: int, email: str) -> None:
        token = self.generate_confirmation(user_id)
        await self.sender.send_confirm_link(email, token)


    def confirm(self, token: str) -> None:
        token_cipher = self.encryptor.encrypt(token)
        user_id = self.confirms.get_user_id_by_token(token_cipher)

        if user_id is None:
            raise InvalidConfirmationTokenException()

        self.user_service.confirm_email(user_id)


    def generate_confirmation(self, user_id: int) -> str:
        token = self.generate_token()
        token_cipher = self.encryptor.encrypt(token)
        self.confirms.add(user_id, token_cipher)
        self.db.commit()

        return token
