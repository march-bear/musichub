from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RUSTFS__",
    )

    PORT: str
    HOST: str
    ACCESS_KEY: str
    SECRET_KEY: str
    PUBLIC_URL: str
    URL_EXPIRES_IN_TIME: int
