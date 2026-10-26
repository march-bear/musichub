from pydantic_settings import BaseSettings


class SenderSettings(BaseSettings):
    SENDER_NAME: str = "noreply"
    SENDER_HOST: str

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 567
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_START_TLS: bool = False
    SMTP_USE_TLS: bool = False

