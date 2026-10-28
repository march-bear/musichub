from pydantic import SecretBytes, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH__",
        secrets_dir="/run/secret/",
    )

    JWT_SECRET_KEY: SecretBytes
    JWT_EXPIRATION_DELTA: int

    CONFIRM_EMAIL_ENABLED: bool = False
    CONFIRM_TOKEN_SECRET_KEY: SecretBytes
    CONFIRM_EMAIL_EXPIRATION_DELTA: int

    @field_validator("JWT_SECRET_KEY", mode="before")
    @classmethod
    def jwt_secret_validator(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v)
        if len(v) not in (32,):
            raise ValueError(f"JWT_SECRET_KEY: ожидается 32 байта, получено: {len(v)}")
        return v

    @field_validator("CONFIRM_TOKEN_SECRET_KEY", mode="before")
    @classmethod
    def confirm_token_secret_validator(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v)
        if len(v) not in (32,):
            raise ValueError(f"CONFIRM_TOKEN_SECRET_KEY: ожидается 32 байта, получено: {len(v)}")
        return v



