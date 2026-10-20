from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.database import SessionLocal
from app.services.storage_service import StorageService
from app.services.track_conv_service import TrackConvService
from app.services.track_saver_service import TrackSaverService
from app.services.track_service import TrackService
from app.settings import settings
from app.data.object_storage import s3, s3_public

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_track_service(db: Session = Depends(get_db)):
    return TrackService(db)


def get_track_conv_service(soundfont: str = settings.SOUNDFONT):
    return TrackConvService(soundfont)


def get_storage_service():
    return StorageService(s3, s3_public)


def get_track_saver_service(
        tc_service: TrackConvService = Depends(get_track_conv_service),
        t_service: TrackService = Depends(get_track_service),
        storage_service: StorageService = Depends(get_storage_service)
):
    return TrackSaverService(tc_service, t_service, storage_service)


