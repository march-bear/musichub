from sqlalchemy import Sequence
from sqlalchemy.orm import Session

import app.db.models as m
import app.db.schemas as s
from app.repositories.project_repository import ProjectRepository
from app.util.exceptions import NotFoundException


class ProjectService:
    def __init__(self, db: Session, project_repository: ProjectRepository):
        self.db = db
        self.project_repository = project_repository


    @staticmethod
    def _model_to_scheme(model: m.Project):
        return s.Project(name=model.name, payload=s.ProjectPayload.model_validate(model.payload))


    def get(self, user_id: int, project_name: str):
        project = self.project_repository.get(user_id, project_name)

        if project is None:
            raise NotFoundException("Project", f"name={project_name}")

        return self._model_to_scheme(project)


    def get_all(self, user_id: int) -> Sequence[s.Project]:
        projects = self.project_repository.list_by_user(user_id)

        return [self._model_to_scheme(project) for project in projects]


    def create(self, user_id: int, project_name: str):
        payload = s.ProjectPayload(tempo=120, parts=[])
        project = self.project_repository.add(user_id, project_name, payload.model_dump())

        result = self._model_to_scheme(project)
        self.db.commit()

        return result


    def put(self, user_id: int, project: s.Project) -> s.Project:
        updated = self.project_repository.update_payload(
            user_id,
            project.name, project.payload.model_dump(mode="json")
        )

        if updated is None:
            raise NotFoundException("Project", f"name={project.name}")

        self.db.commit()

        return project


    def patch(self, user_id: int, old_name: str, new_name: str) -> s.Project:
        updated = self.project_repository.rename(user_id, old_name, new_name)
        if updated is None:
            raise NotFoundException("Project", f"name={new_name}")

        result = self._model_to_scheme(updated)
        self.db.commit()

        return result


    def delete(self, user_id: int, name: str) -> s.Project:
        deleted = self.project_repository.delete(user_id, name)

        if deleted is None:
            raise NotFoundException("Project", f"name={name}")

        result = self._model_to_scheme(deleted)
        self.db.commit()

        return result
