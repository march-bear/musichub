import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import (
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


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[IntPk]
    user_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[CreatedAt]

    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_project_name"),)
