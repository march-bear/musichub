from collections.abc import Iterator
from contextlib import contextmanager

from psycopg.errors import UniqueViolation
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.data.models as m
from app.util.exceptions import EmailAlreadyBusyException


class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    @contextmanager
    def _translate_integrity_error(self) -> Iterator[None]:
        try:
            yield
        except IntegrityError as err:
            orig = err.orig
            if isinstance(orig, UniqueViolation) and orig.diag.constraint_name == "uq_user_email_cipher":
                raise EmailAlreadyBusyException() from err
            raise


    def update_banned(self, user_id: int, banned: bool) -> m.User | None:
        user_upd_stmt = (
            update(m.User)
            .where(m.User.id == user_id)
            .values(banned=banned)
            .returning(m.User)
        )

        return self.db.scalars(user_upd_stmt).one_or_none()


    def confirm_email(self, user_id: int) -> m.User | None:
        user_upd_stmt = (
            update(m.User)
            .where(m.User.id == user_id)
            .values(email_confirmed=True)
            .returning(m.User)
        )

        return self.db.scalars(user_upd_stmt).one_or_none()


    def get_by_email_cipher(self, email_cipher: str) -> m.User | None:
        stmt = (
            select(m.User)
            .where(m.User.email_cipher == email_cipher)
        )

        return self.db.scalars(stmt).one_or_none()


    def get_by_id(self, user_id: int) -> m.User | None:
        stmt = (
            select(m.User)
            .where(m.User.id == user_id)
        )

        return self.db.scalars(stmt).one_or_none()


    def add(self, email_cipher: str, password_hash: str, role: m.UserRole | None = None) -> m.User:
        user = m.User(
            email_cipher=email_cipher,
            role=(role if role is not None else m.UserRole.USER),
            password_hash=password_hash,
        )

        with self._translate_integrity_error():
            self.db.add(user)
            self.db.flush()

        return user
