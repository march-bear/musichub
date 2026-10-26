
from pydantic import Field, SecretBytes, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",
    )

    APP_EMAIL_SECRET_KEY: SecretBytes = Field(validation_alias="email_key")
    APP_CURRENT_EMAIL_SCHEME: str = "v1"

    @field_validator("APP_EMAIL_SECRET_KEY", mode="before")
    @classmethod
    def hex_to_bytes(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v.strip())
        if len(v) not in (32,):
            raise ValueError("email_key: ожидается 32 байта")
        return v


settings = SecuritySettings()
