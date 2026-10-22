from pydantic import Field, SecretBytes, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",
    )

    APP_EMAIL_SECRET_KEY: SecretBytes = Field(validation_alias="email_key")
    APP_JWT_SECRET_KEY: SecretStr
    APP_JWT_EXPIRES_IN_TIME: int
    APP_SOUNDFONT: str

    DATABASE_URL: str

    RUSTFS_PORT: str
    RUSTFS_HOST: str
    RUSTFS_ACCESS_KEY: str
    RUSTFS_SECRET_KEY: str
    RUSTFS_PUBLIC_URL: str
    RUSTFS_URL_EXPIRES_IN_TIME: int

    MIGRATIONS_ENABLED: bool = False

    @field_validator("APP_EMAIL_SECRET_KEY", mode="before")
    @classmethod
    def hex_to_bytes(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v.strip())
        if len(v) not in (32,):
            raise ValueError("email_key: ожидается 32 байта")
        return v

settings = Settings()
