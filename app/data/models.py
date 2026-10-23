import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

IntPk = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[
    datetime, mapped_column(server_default=func.now())
]


class Base(DeclarativeBase):
    pass


class AudioFormat(enum.Enum):
    MIDI = "mid"
    MP3 = "mp3"
    PREVIEW_MP3 = "preview.mp3"
    WAV = "wav"


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[IntPk]
    email_cipher: Mapped[bytes] = mapped_column(unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    banned: Mapped[bool] = mapped_column(default=False)
    password_hash: Mapped[str]
    email_confirmed: Mapped[bool] = mapped_column(default=False)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[IntPk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[CreatedAt]

    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_project_name"),)


class EmailConfirmation(Base):
    __tablename__ = "email_confirmations"

    id: Mapped[IntPk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token_cipher: Mapped[bytes] = mapped_column(unique=True)
    created_at: Mapped[CreatedAt]
