from sqlalchemy import Sequence, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.data.models as m
import app.data.schemas as s
from app.util.exceptions import ProjectAlreadyExistsException, ProjectNotFoundException


class ProjectService:
    def __init__(self, db: Session):
        self.db = db


    def get(self, user_id: int, project_name: str):
        stmt = select(m.Project).where(
            m.Project.user_id == user_id,
            m.Project.name == project_name,
        )

        project: m.Project | None = self.db.scalars(stmt).one_or_none()

        if project is None:
            raise ProjectNotFoundException()

        return s.Project(name=project.name, payload=s.ProjectPayload.model_validate(project.payload))


    def get_all(self, user_id: int):
        stmt = select(m.Project).where(
            m.Project.user_id == user_id,
        )

        projects: Sequence[m.Project] = self.db.scalars(stmt).all()

        return [
            s.Project(
                name=project.name,
                payload=s.ProjectPayload.model_validate(project.payload)
            ) for project in projects
        ]


    def create(self, user_id: int, project_name: str):
        payload = s.ProjectPayload(tempo=120, parts=[])
        db_project = m.Project(user_id=user_id, name=project_name, payload=payload.model_dump())
        self.db.add(db_project)
        try:
            self.db.commit()
        except IntegrityError as err:
            self.db.rollback()
            raise ProjectAlreadyExistsException() from err

        return s.Project(name=db_project.name, payload=payload)


    def put(self, user_id: int, project: s.Project) -> s.Project:
        stmt = (
            select(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == project.name,
            ).with_for_update()
        )

        db_project: m.Project | None = self.db.scalars(stmt).one_or_none()

        if db_project is None:
            raise ProjectNotFoundException()

        db_project.payload = project.payload.model_dump(mode="json")
        self.db.commit()

        return project


    def patch(self, user_id: int, old_name: str, new_name: str) -> s.Project:
        stmt = (
            update(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == old_name,
            )
            .values(name=new_name)
            .returning(m.Project.name, m.Project.payload)
        )

        try:
            row = self.db.execute(stmt).one_or_none()
            self.db.commit()
            if row is None:
                self.db.rollback()
                raise ProjectNotFoundException()
        except IntegrityError as err:
            self.db.rollback()
            raise ProjectAlreadyExistsException() from err

        return s.Project(name=row.name, payload=s.ProjectPayload.model_validate(row.payload))


    def delete(self, user_id: int, project_name: str) -> s.Project:
        stmt = (
            delete(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == project_name,
            )
            .returning(m.Project.name, m.Project.payload)
        )
        row = self.db.execute(stmt).one_or_none()
        self.db.commit()

        if row is None:
            raise ProjectNotFoundException()

        return s.Project(name=row.name, payload=s.ProjectPayload(tempo=120, parts=[]))
