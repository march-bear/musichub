from pydantic import EmailStr
from sqlalchemy.orm import Session

import app.data.models as m
import app.data.schemas as s
from app.repositories.user_repository import UserRepository
from app.security.fields.email import EmailEncryptor
from app.security.passwords.hasher import PasswordHasher
from app.util.exceptions import (
    BadCredentialsException,
    NotFoundException,
)


class UserService:
    def __init__(
            self,
            db: Session,
            password_hasher: PasswordHasher,
            email_encryptor: EmailEncryptor,
            user_repository: UserRepository,
    ):
        self.db = db
        self.password_hasher = password_hasher
        self.email_encryptor = email_encryptor
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


    def get_by_credentials(self, email: EmailStr, password: str) -> s.User:
        email_cipher = self.email_encryptor.encrypt(email)

        user = self.user_repository.get_by_email_cipher(email_cipher)
        password_hash = user.password_hash if user is not None else self.password_hasher.dummy_hash()
        password_ok = self.password_hasher.verify(password, password_hash)
        if user is None or not password_ok:
            raise BadCredentialsException()

        return self._model_to_scheme(user, email)


    def get_by_id(self, user_id: int) -> s.User:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise NotFoundException("User")

        return self._model_to_scheme(user, self.email_encryptor.decrypt(user.email_cipher))


    def create(self, email: EmailStr, password: str) -> s.User:
        email_cipher = self.email_encryptor.encrypt(email)
        password_hash = self.password_hasher.hash(password)

        user = self.user_repository.add(email_cipher, password_hash)
        result = self._model_to_scheme(user, email)
        self.db.commit()

        return result
