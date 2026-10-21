from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    RUSTFS_PORT: str
    RUSTFS_HOST: str
    RUSTFS_ACCESS_KEY: str
    RUSTFS_SECRET_KEY: str
    RUSTFS_PUBLIC_URL: str
    RUSTFS_URL_EXPIRES_IN_TIME: int

    SOUNDFONT: str


settings = Settings()
