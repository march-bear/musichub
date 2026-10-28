from app.security.fields.email import EmailEncryptor
from app.security.passwords.hasher import PasswordHasher


class UserCredentialsCodec:
    def __init__(self, password_hasher: PasswordHasher, email_encryptor: EmailEncryptor):
        self.password_hasher = password_hasher
        self.email_encryptor = email_encryptor


    @staticmethod
    def normalize_email(email: str) -> str:
        return email.lower().strip()


    def encrypt_email(self, email: str) -> str:
        return self.email_encryptor.encrypt(email)


    def decrypt_email(self, email_cipher: str) -> str:
        return self.email_encryptor.decrypt(email_cipher)


    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)


    def verify_password(self, password: str, hashed: str | None) -> bool:
        password_hash = self.password_hasher.dummy_hash() if hashed is None else hashed
        return self.password_hasher.verify(password, password_hash)[0]
