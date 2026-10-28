import datetime

import jwt

from app.auth.settings import AuthSettings
from app.repositories.user_repository import UserRepository


class SessionService:
    def __init__(self, settings: AuthSettings, user_repository: UserRepository):
        self._cfg = settings
        self.users = user_repository


    def extract_access_token(self, token: str):
        token = jwt.decode(token, self._cfg.JWT_SECRET_KEY.get_secret_value(), algorithms=["HS256"])
        user = self.users.get_by_id(int(token["sub"]))

        return user


    def generate_access_token(self, user_id: int):
        payload = {
            "sub": str(user_id),
            "exp": (
                datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=self._cfg.JWT_EXPIRATION_DELTA)
            ),
            "iat": datetime.datetime.now(datetime.UTC),
        }
        return jwt.encode(payload, self._cfg.JWT_SECRET_KEY.get_secret_value(), algorithm="HS256")
