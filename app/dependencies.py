from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.database import SessionLocal
from app.services.storage_service import StorageService
from app.services.project_conv_service import ProjectConvService
from app.services.project_saver_service import ProjectSaverService
from app.services.project_service import ProjectService
from app.settings import settings
from app.data.object_storage import s3, s3_public

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)):
    return ProjectService(db)


def get_project_conv_service(soundfont: str = settings.SOUNDFONT):
    return ProjectConvService(soundfont)


def get_storage_service():
    return StorageService(s3, s3_public)


def get_project_saver_service(
        pc_service: ProjectConvService = Depends(get_project_conv_service),
        p_service: ProjectService = Depends(get_project_service),
        storage_service: StorageService = Depends(get_storage_service)
):
    return ProjectSaverService(pc_service, p_service, storage_service)


