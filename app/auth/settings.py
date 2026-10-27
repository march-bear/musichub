from pydantic import SecretStr
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_EXPIRATION_DELTA: int

    CONFIRM_EMAIL_ENABLED: bool
    CONFIRM_TOKEN_SECRET_KEY: SecretStr
    CONFIRM_EMAIL_EXPIRATION_DELTA: int
