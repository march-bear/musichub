from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    OBJECT_STORAGE_PORT: str
    OBJECT_STORAGE_HOST: str
    OBJECT_STORAGE_ACCESS_KEY: str
    OBJECT_STORAGE_SECRET_KEY: str
    OBJECT_STORAGE_PUBLIC_URL: str
    EXPIRES_IN_TIME: int

    SOUNDFONT: str


settings = Settings()