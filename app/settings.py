
from pydantic import Field, SecretBytes, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",
    )

    APP_API_PUBLIC_HOST: str
    APP_API_PUBLIC_PORT: int

    APP_EMAIL_SECRET_KEY: SecretBytes = Field(validation_alias="email_key")
    APP_JWT_SECRET_KEY: SecretStr
    APP_JWT_EXPIRES_IN_TIME: int
    APP_SOUNDFONT: str
    APP_EMAIL_CONFIRM_TIME: int | None = None

    DATABASE_URL: str

    RUSTFS_PORT: str
    RUSTFS_HOST: str
    RUSTFS_ACCESS_KEY: str
    RUSTFS_SECRET_KEY: str
    RUSTFS_PUBLIC_URL: str
    RUSTFS_URL_EXPIRES_IN_TIME: int

    MIGRATIONS_ENABLED: bool = False
    EMAIL_CHECK_ENABLED: bool = False

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_HOST_DOMAIN: str | None = None

    @field_validator("APP_EMAIL_SECRET_KEY", mode="before")
    @classmethod
    def hex_to_bytes(cls, v):
        if isinstance(v, str):
            v = bytes.fromhex(v.strip())
        if len(v) not in (32,):
            raise ValueError("email_key: ожидается 32 байта")
        return v

    @model_validator(mode="after")
    def validate_email_check_params(self):
        if self.EMAIL_CHECK_ENABLED and (
                not self.SMTP_HOST
                or not self.SMTP_PORT
                or not self.SMTP_HOST_DOMAIN
                or not self.EMAIL_CHECK_ENABLED
        ):
            raise ValueError("SMTP_ параметры должны быть установлены при включенной проверке почты")

        return self


settings = SharedSettings()
