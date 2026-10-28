from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Security
from starlette import status

from app.auth.deps import get_current_user
from app.db import schemas
from app.db.models import AudioFormat
from app.services.deps import get_project_saver_service, get_project_service
from app.services.project_saver_service import ProjectSaverService
from app.services.project_service import ProjectService
from app.storage.deps import get_projects_storage
from app.storage.s3_storage import S3Storage

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get(
    "/",
    response_model=list[schemas.Project],
    status_code=status.HTTP_200_OK)
def get_projects(
        user: Annotated[schemas.User, Security(get_current_user)],
        project_service: Annotated[ProjectService, Depends(get_project_service)]
):
    projects = project_service.get_all(user.id)

    return projects


@router.get("/{name}", response_model=schemas.Project)
def get_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        project_service: Annotated[ProjectService, Depends(get_project_service)]
):
    return project_service.get(user.id, name)


@router.get("/{name}/preview", response_model=schemas.ProjectURL)
def get_project_preview(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        storage_service: Annotated[S3Storage, Depends(get_projects_storage)],
):
    return schemas.ProjectURL(
        name=name,
        url=storage_service.get_url(str(Path(str(user.id)) / f"{name}.preview.mp3"))
    )


@router.get("/{name}/download/{fmt}")
def download_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        fmt: AudioFormat,
        storage_service: Annotated[S3Storage, Depends(get_projects_storage)]
):
    return schemas.ProjectURL(
        name=name,
        url=storage_service.get_url(str(Path(str(user.id)) / f"{name}.{fmt.value}"))
    )


@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        project_service: Annotated[ProjectService, Depends(get_project_service)]
):
    return project_service.create(user.id, name)


@router.patch("/{name}", response_model=schemas.Project)
def complete_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        new_name: str,
        project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return project_service.patch(user.id, name, new_name)


@router.put("/{name}", response_model=schemas.Project)
def update_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        project_payload: schemas.ProjectPayload,
        project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return project_service.put(user.id, schemas.Project(name=name, payload=project_payload))


@router.delete("/{name}", response_model=schemas.Project)
def delete_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return project_service.delete(user.id, name)


@router.post(
    "/{name}/generate-audio",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def generate_audio_by_project(
        user: Annotated[schemas.User, Security(get_current_user)],
        name: str,
        project_saver_service: Annotated[ProjectSaverService, Depends(get_project_saver_service)]
):
    project_saver_service.save_project(user.id, name)
