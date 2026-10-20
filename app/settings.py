from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    EXPIRES_IN_TIME: int
    SOUNDFONT: str


settings = Settings()