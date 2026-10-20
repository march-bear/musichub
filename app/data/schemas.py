from pydantic import BaseModel

class Track(BaseModel):
    name: str
    payload: TrackPayload | None


class TrackPayload(BaseModel):
    tempo: int
    parts: list[TrackPart]


class TrackPart(BaseModel):
    instrument: str
    part: list[Note]


class Note(BaseModel):
    number: int
    duration: int
    time: int
    velocity: int