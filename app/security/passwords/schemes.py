import bcrypt


class BCryptPasswordHasherScheme:
    def __init__(self):
        self._dummy_hash = bcrypt.hashpw(b"dummy", bcrypt.gensalt()).decode()

    def dummy_hash(self) -> str:
        return self._dummy_hash


    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())
