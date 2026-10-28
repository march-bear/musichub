from pydantic import SecretBytes, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SECURITY__",
        secrets_dir="/run/secrets",
    )

    EMAIL_SECRET_KEY: SecretBytes
    CURRENT_EMAIL_SCHEME: str = "v1"

    @field_validator("EMAIL_SECRET_KEY", mode="after")
    @classmethod
    def hex_to_bytes(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v.strip())
        if len(v) not in (32, 64):
            raise ValueError("email_secret_key: ожидается 32 или 64 байта")
        return v
