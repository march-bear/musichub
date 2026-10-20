from sqlalchemy import select, delete, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.data.schemas as s
import app.data.models as m
from app.util.exceptions import TrackNotFoundException, TrackAlreadyExistsException


class TrackService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int, track_name: str):
        stmt = select(m.Track).where(
            m.Track.user_id == user_id,
            m.Track.name == track_name,
        )

        track: m.Track | None = self.db.scalars(stmt).one_or_none()

        if track is None:
            raise TrackNotFoundException()

        return s.Track(name=track.name, payload=s.TrackPayload.model_validate(track.payload))

    def get_all(self, user_id: int):
        stmt = select(m.Track).where(
            m.Track.user_id == user_id,
        )

        tracks: Sequence[m.Track] = self.db.scalars(stmt).all()

        return [
            s.Track(
                name=track.name,
                payload=s.TrackPayload.model_validate(track.payload)
            ) for track in tracks
        ]

    def create(self, user_id: int, track_name: str):
        payload = s.TrackPayload(tempo=120, parts=[])
        db_track = m.Track(user_id=user_id, name=track_name, payload=payload.model_dump())
        self.db.add(db_track)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise TrackAlreadyExistsException()

        return s.Track(name=db_track.name, payload=payload)


    def put(self, user_id: int, track: s.Track) -> s.Track:
        stmt = (
            select(m.Track)
            .where(
                m.Track.user_id == user_id,
                m.Track.name == track.name,
            ).with_for_update()
        )

        db_track: m.Track | None = self.db.scalars(stmt).one_or_none()

        if db_track is None:
            raise TrackNotFoundException()

        db_track.payload = track.payload.model_dump(mode="json")
        self.db.commit()

        return track


    def patch(self, user_id: int, track: s.Track) -> s.Track:
        return self.put(user_id, track)


    def delete(self, user_id: int, track_name: str) -> s.Track:
        stmt = (
            delete(m.Track)
            .where(
                m.Track.user_id == user_id,
                m.Track.name == track_name,
            )
            .returning(m.Track.name, m.Track.payload)
        )
        row = self.db.execute(stmt).one_or_none()
        self.db.commit()

        if row is None:
            raise TrackNotFoundException()

        return s.Track(name=row.name, payload=s.TrackPayload(tempo=120, parts=list()))