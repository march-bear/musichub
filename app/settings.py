
from pydantic_settings import BaseSettings, SettingsConfigDict

from auth.settings import AuthSettings
from email_utils.sender_service import SenderService
from security.settings import SecuritySettings
from storage.settings import StorageSettings


class SharedSettings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",
    )

    SOUNDFONT: str
    DATABASE_URL: str
    MIGRATIONS_ENABLED: bool = False


class AppSettings:
    def __init__(self):
        self.shared = SharedSettings()
        self.security = SecuritySettings()
        self.storage = StorageSettings()
        self.auth = AuthSettings()
        self.sender = SenderService()
