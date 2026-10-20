from fastapi import APIRouter, Depends
from pathlib import Path
from starlette import status
from starlette.responses import JSONResponse

from app.data import schemas
from app.data.models import AudioFormat
from app.dependencies import get_storage_service, get_track_saver_service, get_track_service
from app.services.track_saver_service import TrackSaverService
from app.services.track_service import TrackService
from app.services.storage_service import StorageService


router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get(
    "/",
    response_model=list[schemas.Track],
    status_code=status.HTTP_200_OK)
def get_tracks(
        user_id: int,
        track_service: TrackService = Depends(get_track_service)
):
    tracks = track_service.get_all(user_id)
    if len(tracks) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])

    return tracks


@router.get("/{name}", response_model=schemas.Track)
def get_track(
        name: str,
        user_id: int,
        track_service: TrackService = Depends(get_track_service)
):
    return track_service.get(user_id, name)


@router.get("/{name}/preview", response_model=schemas.TrackURL)
def get_track_preview(
        name: str,
        user_id: int,
        storage_service: StorageService = Depends(get_storage_service)
):
    return schemas.TrackURL(
        name=name,
        url=storage_service.get_file_url(str(Path(str(user_id)) / f"{name}.preview.mp3"))
    )


@router.get("/{name}/download/{fmt}")
def download_track(
        name: str,
        user_id: int,
        fmt: AudioFormat,
        storage_service: StorageService = Depends(get_storage_service)
):
    return schemas.TrackURL(
        name=name,
        url=storage_service.get_file_url(str(Path(str(user_id)) / f"{name}.{fmt.value}"))
    )


@router.post("/", response_model=schemas.Track, status_code=status.HTTP_201_CREATED)
def create_track(
        name: str,
        user_id: int,
        track_service: TrackService = Depends(get_track_service)
):
    return track_service.create(user_id, name)


@router.patch("/{name}", response_model=schemas.Track)
def complete_track(
        name: str,
        user_id: int,
        track_payload: schemas.TrackPayload,
        track_service: TrackService = Depends(get_track_service),
):
    return track_service.patch(user_id, schemas.Track(name=name, payload=track_payload))


@router.put("/{name}", response_model=schemas.Track)
def update_track(
        name: str,
        user_id: int,
        track_payload: schemas.TrackPayload,
        track_service: TrackService = Depends(get_track_service),
):
    return track_service.put(user_id, schemas.Track(name=name, payload=track_payload))


@router.delete("/{name}", response_model=schemas.Track)
def delete_track(
        name: str,
        user_id: int,
        track_service: TrackService = Depends(get_track_service),
):
    return track_service.delete(user_id, name)


@router.post(
    "/{name}/generate-audio",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def generate_audio_track(
        name: str,
        user_id: int,
        track_saver_service: TrackSaverService = Depends(get_track_saver_service)
):
    track_saver_service.save_track(user_id, name)