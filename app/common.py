from pydantic_settings import BaseSettings, SettingsConfigDict

from app.util.field_types import Port


class SharedSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP__",
        secrets_dir="/run/secrets",
    )

    API_HOST: str
    API_PORT: Port
    API_PUBLIC_HOST: str
    API_PUBLIC_PORT: Port

    SOUNDFONT: str
    DATABASE_URL: str
    MIGRATIONS_ENABLED: bool = False
