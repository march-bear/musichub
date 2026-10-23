import datetime
import uuid

import jwt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.models import EmailConfirmation
from app.data.schemas import EmailConfirmTokenOut, TokenOut
from app.services.security_service import SecurityService
from app.services.user_service import UserService
from app.settings import settings
from app.util.exceptions import InvalidConfirmationTokenException, UserNotFoundException


class AuthService:
    BEARER_TOKEN_TYPE = "Bearer" # noqa: S105

    def __init__(
            self,
            user_service: UserService,
            email_confirm_service: EmailConfirmationService | None = None,
    ):
        if email_confirm_service is None and settings.EMAIL_CHECK_ENABLED:
            raise ValueError("При EMAIL_CHECK_ENABLED ожидается не None сервис")

        self.user_service = user_service
        self.email_confirm_service = email_confirm_service


    def extract_token(self, token: str):
        token = jwt.decode(token, settings.APP_JWT_SECRET_KEY.get_secret_value(), algorithms=["HS256"])
        user = self.user_service.get_by_id(int(token["sub"]))

        return user


    @staticmethod
    def generate_token(user_id: int):
        payload = {
            "sub": str(user_id),
            "exp": (
                datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=settings.APP_JWT_EXPIRES_IN_TIME)
            ),
            "iat": datetime.datetime.now(datetime.UTC),
        }
        return jwt.encode(payload, settings.APP_JWT_SECRET_KEY.get_secret_value(), algorithm="HS256")


    def authenticate(self, email: EmailStr, password: str):
        user = self.user_service.get_by_credentials(email, password)

        return TokenOut(access_token=self.generate_token(user.id), token_type=self.BEARER_TOKEN_TYPE)


    def register(self, email: EmailStr, password: str):
        user = self.user_service.create(email, password)

        return user.id, TokenOut(access_token=self.generate_token(user.id), token_type=self.BEARER_TOKEN_TYPE)


if settings.EMAIL_CHECK_ENABLED:
    class EmailConfirmationService:
        @staticmethod
        def generate_uuid():
            return str(uuid.uuid4())

        def __init__(self, db: Session, security_service: SecurityService, user_service: UserService):
            self.db = db
            self.security_service = security_service
            self.user_service = user_service


        def confirm(self, token: str):
            confirmation_stmt = (
                select(EmailConfirmation)
                .where(EmailConfirmation.token_cipher == self.security_service.encrypt_email(token))
            )

            confirmation: EmailConfirmation | None = self.db.scalars(confirmation_stmt).one_or_none()

            if not confirmation:
                raise InvalidConfirmationTokenException()

            self.user_service.confirm_email(confirmation.user_id)


        def create_token(self, user_id: int) -> EmailConfirmTokenOut:
            confirm_token = self.generate_uuid()
            token_cipher = self.security_service.encrypt_email(confirm_token)

            confirmation = EmailConfirmation(user_id=user_id, token_cipher=token_cipher)

            self.db.add(confirmation)
            try:
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                raise UserNotFoundException() from err

            return EmailConfirmTokenOut(confirm_token=confirm_token)
