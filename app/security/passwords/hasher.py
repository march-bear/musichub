from typing import Protocol


class PasswordHasherScheme(Protocol):
    def dummy_hash(self) -> str: ...
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...


class PasswordHasher:
    def __init__(self, schemes: dict[str, PasswordHasherScheme], current: str):
        self._schemes = schemes
        self._current = current


    def dummy_hash(self) -> str:
        return self._schemes[self._current].dummy_hash()


    def hash(self, password: str) -> str:
        return self._schemes[self._current].hash(password)


    def _detect_scheme(self, hashed: str):
        if hashed.startswith(("$2a$", "$2y$", "$2b$")):
            return self._schemes["bcrypt"]

        raise ValueError("Unknown hash format")


    def verify(self, password: str, hashed: str) -> tuple[bool, bool]:
        scheme = self._detect_scheme(hashed)
        try:
            return scheme.verify(password, hashed), True
        except ValueError, KeyError:
            return False, False
