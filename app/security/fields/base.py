from base64 import b64decode, b64encode
from typing import Protocol


class DataEncryptorScheme(Protocol):
    version: str
    def encrypt(self, data: str) -> bytes: ...
    def decrypt(self, cipher: bytes) -> str: ...


class DataEncryptor:
    def __init__(self, schemes: dict[str, DataEncryptorScheme], current: str):
        self._schemes = schemes
        self._current = current


    def encrypt(self, password: str) -> str:
        scheme = self._schemes[self._current]
        return f"{scheme.version}:{b64encode(self._schemes[self._current].encrypt(password)).decode()}"


    def decrypt(self, cipher: str) -> str:
        version, _, encoded = cipher.partition(":")
        scheme = self._schemes[version]
        return scheme.decrypt(b64decode(encoded.encode()))
