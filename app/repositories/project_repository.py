from collections.abc import Iterator
from contextlib import contextmanager

from psycopg.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import Sequence, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.data.models as m
from app.util.exceptions import NotFoundException, ProjectAlreadyExistsException


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db


    @contextmanager
    def _translate_integrity_error(self) -> Iterator[None]:
        try:
            yield
        except IntegrityError as err:
            orig = err.orig
            if isinstance(orig, UniqueViolation) and orig.diag.constraint_name == "uq_project_name":
                raise ProjectAlreadyExistsException() from err
            if isinstance(orig, ForeignKeyViolation) and orig.diag.constraint_name == "fk_project_user":
                raise NotFoundException("User") from err
            raise


    def get(self, user_id: int, project_name: str, *, for_update: bool = False) -> m.Project | None:
        stmt = (
            select(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == project_name,
            )
        )

        if for_update:
            stmt = stmt.with_for_update()

        return self.db.scalars(stmt).one_or_none()


    def list_by_user(self, user_id: int) -> Sequence[m.Project]:
        stmt = (
            select(m.Project).where(
                m.Project.user_id == user_id,
            )
        )

        return self.db.scalars(stmt).all()


    def add(self, user_id: int, name: str, payload: dict) -> m.Project:
        project = m.Project(user_id=user_id, name=name, payload=payload)

        with self._translate_integrity_error():
            self.db.add(project)
            self.db.flush()

        return project

    def update_payload(self, user_id: int, name: str, payload: dict) -> m.Project | None:
        stmt = (
            update(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == name,
            )
            .values(payload=payload)
            .returning(m.Project)
        )

        return self.db.scalars(stmt).one_or_none()


    def rename(self, user_id: int, old_name: str, new_name: str) -> m.Project | None:
        stmt = (
            update(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == old_name,
            )
            .values(name=new_name)
            .returning(m.Project)
        )

        with self._translate_integrity_error():
            return self.db.scalars(stmt).one_or_none()


    def delete(self, user_id: int, project_name: str) -> m.Project | None:
        stmt = (
            delete(m.Project)
            .where(
                m.Project.user_id == user_id,
                m.Project.name == project_name,
            )
        )

        return self.db.scalars(stmt).one_or_none()
