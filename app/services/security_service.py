import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESSIV

from app.settings import settings


class SecurityService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())


    def __init__(self):
        self.siv = AESSIV(settings.APP_EMAIL_SECRET_KEY.get_secret_value())


    def encrypt_email(self, email: str) -> bytes:
        return self.siv.encrypt(email.lower().encode(), None)


    def decrypt_email(self, email_cipher: bytes) -> str:
        return self.siv.decrypt(email_cipher, None).decode()
