from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.track_service import TrackService
from app.data.database import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_track_service(db: Session = Depends(get_db)):
    return TrackService(db)
