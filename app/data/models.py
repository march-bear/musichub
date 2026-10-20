import enum
from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import (
    String, ForeignKey, UniqueConstraint, Enum, func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
)

IntPk = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[
    datetime, mapped_column(server_default=func.now())
]


class Base(DeclarativeBase):
    pass


class AudioFormat(enum.Enum):
    MIDI = "midi"
    MP3 = "mp3"
    PREVIEW_MP3 = "preview_mp3"
    WAV = "wav"


class ConversionStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[IntPk]
    user_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(100))
    payload: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[CreatedAt]

    conversions: Mapped[list["TrackConversion"]] = relationship(
        back_populates="track", cascade="all, delete-orphan"
    )


class TrackConversion(Base):
    __tablename__ = "track_conversions"
    __table_args__ = (
        UniqueConstraint("track_id", "format", name="uq_track_format"),
    )

    id: Mapped[IntPk]
    track_id: Mapped[int] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"), index=True
    )
    format: Mapped[AudioFormat] = mapped_column(Enum(AudioFormat))
    status: Mapped[ConversionStatus] = mapped_column(
        Enum(ConversionStatus), default=ConversionStatus.PENDING
    )
    file_key: Mapped[Optional[str]]
    error: Mapped[Optional[str]]
    created_at: Mapped[CreatedAt]
    finished_at: Mapped[Optional[datetime]]

    track: Mapped["Track"] = relationship(back_populates="conversions")