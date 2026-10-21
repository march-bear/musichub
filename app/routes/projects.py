from fastapi import APIRouter, Depends
from pathlib import Path
from starlette import status
from starlette.responses import JSONResponse

from app.data import schemas
from app.data.models import AudioFormat
from app.dependencies import get_storage_service, get_project_saver_service, get_project_service
from app.services.project_saver_service import ProjectSaverService
from app.services.project_service import ProjectService
from app.services.storage_service import StorageService


router = APIRouter(prefix="/projects", tags=["projects"])

@router.get(
    "/",
    response_model=list[schemas.Project],
    status_code=status.HTTP_200_OK)
def get_projects(
        user_id: int,
        project_service: ProjectService = Depends(get_project_service)
):
    projects = project_service.get_all(user_id)
    if len(projects) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])

    return projects


@router.get("/{name}", response_model=schemas.Project)
def get_project(
        name: str,
        user_id: int,
        project_service: ProjectService = Depends(get_project_service)
):
    return project_service.get(user_id, name)


@router.get("/{name}/preview", response_model=schemas.ProjectURL)
def get_project_preview(
        name: str,
        user_id: int,
        storage_service: StorageService = Depends(get_storage_service)
):
    return schemas.ProjectURL(
        name=name,
        url=storage_service.get_file_url(str(Path(str(user_id)) / f"{name}.preview.mp3"))
    )


@router.get("/{name}/download/{fmt}")
def download_project(
        name: str,
        user_id: int,
        fmt: AudioFormat,
        storage_service: StorageService = Depends(get_storage_service)
):
    return schemas.ProjectURL(
        name=name,
        url=storage_service.get_file_url(str(Path(str(user_id)) / f"{name}.{fmt.value}"))
    )


@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
        name: str,
        user_id: int,
        project_service: ProjectService = Depends(get_project_service)
):
    return project_service.create(user_id, name)


@router.patch("/{name}", response_model=schemas.Project)
def complete_project(
        name: str,
        user_id: int,
        project_payload: schemas.ProjectPayload,
        project_service: ProjectService = Depends(get_project_service),
):
    return project_service.patch(user_id, schemas.Project(name=name, payload=project_payload))


@router.put("/{name}", response_model=schemas.Project)
def update_project(
        name: str,
        user_id: int,
        project_payload: schemas.ProjectPayload,
        project_service: ProjectService = Depends(get_project_service),
):
    return project_service.put(user_id, schemas.Project(name=name, payload=project_payload))


@router.delete("/{name}", response_model=schemas.Project)
def delete_project(
        name: str,
        user_id: int,
        project_service: ProjectService = Depends(get_project_service),
):
    return project_service.delete(user_id, name)


@router.post(
    "/{name}/generate-audio",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def generate_audio_by_project(
        name: str,
        user_id: int,
        project_saver_service: ProjectSaverService = Depends(get_project_saver_service)
):
    project_saver_service.save_project(user_id, name)