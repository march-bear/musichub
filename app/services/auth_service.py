import datetime

import jwt
from pydantic import EmailStr

from app.data.schemas import TokenOut
from app.services.user_service import UserService
from app.settings import settings
from app.util.exceptions import UserBannedException


class AuthService:
    BEARER_TOKEN_TYPE = "Bearer" # noqa: S105

    def __init__(self, user_service: UserService):
        self.user_service = user_service


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
        if user.banned:
            raise UserBannedException()

        return TokenOut(access_token=self.generate_token(user.id), token_type=self.BEARER_TOKEN_TYPE)


    def register(self, email: EmailStr, password: str):
        user = self.user_service.create(email, password)

        return TokenOut(access_token=self.generate_token(user.id), token_type=self.BEARER_TOKEN_TYPE)
