from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH__",
        secrets_dir="/run/secret/",
    )

    JWT_SECRET_KEY: SecretStr
    JWT_EXPIRATION_DELTA: int

    CONFIRM_EMAIL_ENABLED: bool = False
    CONFIRM_TOKEN_SECRET_KEY: SecretStr
    CONFIRM_EMAIL_EXPIRATION_DELTA: int

    @field_validator("JWT_SECRET_KEY", mode="after")
    def secrets_validator(cls, v):
        if len(v) not in (32,):
            raise ValueError("JWT_SECRET_KEY: ожидается 32 байта")
        return v



