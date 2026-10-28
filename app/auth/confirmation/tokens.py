from contextlib import contextmanager

from psycopg.errors import ForeignKeyViolation
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import EmailConfirmation
from app.util.exceptions import NotFoundException


class ConfirmTokenRepository:
    def __init__(self, db: Session):
        self.db = db


    @contextmanager
    def _translate_integrity_error(self):
        try:
            yield
        except IntegrityError as err:
            orig = err.orig
            if isinstance(orig, ForeignKeyViolation) and orig.diag.constraint_name == 'fk_email_confirm_user':
                raise NotFoundException("User") from err
            raise


    def get_user_id_by_token(self, token_cipher: str) -> int | None:
        stmt = (
            select(EmailConfirmation.user_id)
            .where(EmailConfirmation.token_cipher == token_cipher)
        )

        return self.db.scalars(stmt).one_or_none()


    def add(self, user_id: int, token_cipher) -> None:
        confirmation = EmailConfirmation(user_id=user_id, token_cipher=token_cipher)

        with self._translate_integrity_error():
            self.db.add(confirmation)
            self.db.flush()
