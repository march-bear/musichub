from cryptography.hazmat.primitives.ciphers.aead import AESSIV

from app.security.settings import settings


class EmailAesSivScheme:
    version: str

    def __init__(self, ):
        self.siv = AESSIV(settings.APP_EMAIL_SECRET_KEY.get_secret_value())


    def encrypt(self, email: str) -> bytes:
        return self.siv.encrypt(email.lower().encode(), None)


    def decrypt(self, email_cipher: bytes) -> str:
        return self.siv.decrypt(email_cipher, None).decode()
