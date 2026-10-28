from app.auth.settings import AuthSettings
from app.common import SharedSettings
from app.email_utils.settings import SenderSettings
from app.security.settings import SecuritySettings
from app.storage.settings import StorageSettings


class AppSettings:
    def __init__(self):
        self.shared = SharedSettings()
        self.security = SecuritySettings()
        self.storage = StorageSettings()
        self.auth = AuthSettings()
        self.sender = SenderSettings()
