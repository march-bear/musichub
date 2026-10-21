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
    relationship,
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


class ConversionStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[IntPk]
    user_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[CreatedAt]

    conversions: Mapped[list[ProjectConversion]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_project_name"),)


class ProjectConversion(Base):
    __tablename__ = "project_conversions"
    __table_args__ = (
        UniqueConstraint("project_id", "format", name="uq_project_format"),
    )

    id: Mapped[IntPk]
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    format: Mapped[AudioFormat] = mapped_column(Enum(AudioFormat))
    status: Mapped[ConversionStatus] = mapped_column(
        Enum(ConversionStatus), default=ConversionStatus.PENDING
    )
    file_key: Mapped[str | None]
    error: Mapped[str | None]
    created_at: Mapped[CreatedAt]
    finished_at: Mapped[datetime | None]

    project: Mapped[Project] = relationship(back_populates="conversions")
