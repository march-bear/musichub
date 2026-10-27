from pydantic import EmailStr
from sqlalchemy.orm import Session

import app.db.models as m
import app.db.schemas as s
from app.repositories.user_repository import UserRepository
from app.security.cred_codec import UserCredentialsCodec
from app.util.exceptions import NotFoundException


class UserService:
    def __init__(
            self,
            db: Session,
            cred_codec: UserCredentialsCodec,
            user_repository: UserRepository,
    ):
        self.db = db
        self.cred_codec = cred_codec
        self.user_repository = user_repository


    @staticmethod
    def _model_to_scheme(model: m.User, email: str) -> s.User:
        normalized_email = UserService._normalize_email(email)
        return s.User(id=model.id, email=normalized_email, banned=model.banned, email_confirmed=model.email_confirmed)


    @staticmethod
    def _normalize_email(email: EmailStr) -> EmailStr:
        return email.lower()


    def confirm_email(self, user_id: int) -> None:
        user = self.user_repository.confirm_email(user_id)
        if user is None:
            raise NotFoundException("User")
        self.db.commit()


    def get_by_id(self, user_id: int) -> s.User:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise NotFoundException("User")

        return self._model_to_scheme(user, self.cred_codec.decrypt_email(user.email_cipher))


    def create(self, email: EmailStr, password: str) -> s.User:
        email_cipher = self.cred_codec.encrypt_email(email)
        password_hash = self.cred_codec.hash_password(password)

        user = self.user_repository.add(email_cipher, password_hash)
        result = self._model_to_scheme(user, email)
        self.db.commit()

        return result
