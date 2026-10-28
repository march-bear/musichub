from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.field_types import Port


class SenderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="EMAIL__",
    )

    SENDER_NAME: str = "noreply"
    SENDER_HOST: str

    SMTP_HOST: str = "localhost"
    SMTP_PORT: Port = 567
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_START_TLS: bool = False
    SMTP_USE_TLS: bool = False

    @model_validator(mode="after")
    def smtp_validate(self):
        if (
            (self.SMTP_USER and not self.SMTP_PASSWORD)
            or (not self.SMTP_USER and self.SMTP_PASSWORD)
        ):
            raise ValueError(
                "SMTP_USER и SMTP_PASSWORD должны быть установлены одновременно, либо не установлены вовсе"
            )
        return self
