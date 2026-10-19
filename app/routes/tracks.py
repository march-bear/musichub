from fastapi import APIRouter
from app import schemas

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", response_model=list[schemas.TrackPayload])
def get_tracks(user_id: int):
    pass


@router.get("/{name}", response_model=schemas.TrackPayload | None)
def get_track(track_name: str, user_id: int):
    pass


@router.get("/{name}/preview")
def get_track_preview(track_name: str, user_id: int):
    pass


@router.get("/current", response_model=schemas.TrackPayload | None)
def get_current_track(user_id: int):
    pass


@router.get("/{name}/download/{fmt}")
def download_track(name: str, user_id: int, fmt: str):
    pass


@router.post("/", response_model=schemas.TrackPayload)
def create_track(user_id: int):
    pass


@router.patch("/{name}", response_model=schemas.TrackPayload | None)
def complete_track(name: str, user_id: int):
    pass


@router.put("/{name}", response_model=schemas.TrackPayload | None)
def update_track(name: str, user_id: int):
    pass


@router.delete("/{name}", response_model=None)
def delete_track(name: str, user_id: int):
    pass


@router.post("/{name}/generate-audio", response_model=None)
def generate_audio_track(name: str, user_id: int):
    pass