from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from pydantic import SecretBytes


class StringAesSivScheme:
    def __init__(self, secret_key: SecretBytes):
        self.siv = AESSIV(secret_key.get_secret_value())


    def encrypt(self, data: str) -> bytes:
        return self.siv.encrypt(data.lower().encode(), None)


    def decrypt(self, cipher: bytes) -> str:
        return self.siv.decrypt(cipher, None).decode()
