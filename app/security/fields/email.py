from pydantic import EmailStr

from app.security.fields.base import DataEncryptor


class EmailEncryptor:
    def __init__(self, encryptor: DataEncryptor):
        self.encryptor = encryptor


    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.lower().strip()


    def encrypt(self, email: EmailStr) -> str:
        normalized_email = self._normalize_email(email)
        return self.encryptor.encrypt(normalized_email)


    def decrypt(self, data: str) -> EmailStr:
        return self._normalize_email(self.encryptor.decrypt(data))
