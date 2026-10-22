from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.data.models as m
import app.data.schemas as s
from app.services.security_service import SecurityService
from app.util.exceptions import BadCredentialsException, EmailAlreadyBusyException, UserNotFoundException


class UserService:
    def __init__(self, db: Session, security_service: SecurityService):
        self.db = db
        self.security_service = security_service


    def get_by_credentials(self, email: EmailStr, password: str):
        email_cipher = self.security_service.encrypt_email(email)
        password_hash = self.security_service.hash_password(password)

        stmt = (
            select(m.User)
            .where(
                m.User.email_cipher == email_cipher,
                m.User.password_hash == password_hash,
            )
        )

        user: m.User | None = self.db.execute(stmt).scalars().one_or_none()
        if user is None:
            raise BadCredentialsException()

        return s.User(id=user.id, email=email, banned=user.banned)


    def get_by_id(self, user_id: int) -> s.User:
        stmt = (
            select(m.User)
            .where(m.User.id == user_id)
        )
        user: m.User | None = self.db.execute(stmt).scalars().one_or_none()

        if user is None:
            raise UserNotFoundException()

        return s.User(
            id=user.id,
            email=self.security_service.decrypt_email(user.email_cipher),
            banned=user.banned,
        )


    def create(self, email: EmailStr, password: str):
        db_user = m.User(
            email_cipher=self.security_service.encrypt_email(email),
            role=m.UserRole.USER,
            password_hash=self.security_service.hash_password(password)
        )
        self.db.add(db_user)
        try:
            self.db.commit()
        except IntegrityError as err:
            self.db.rollback()
            raise EmailAlreadyBusyException() from err

        self.db.refresh(db_user)

        return s.User(
            id=db_user.id,
            email=email,
            banned=db_user.banned,
        )
