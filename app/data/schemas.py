import enum

from pydantic import BaseModel


class Project(BaseModel):
    name: str
    payload: ProjectPayload


class ProjectPayload(BaseModel):
    tempo: int
    parts: list[ProjectPart]


class ProjectPart(BaseModel):
    instrument: int
    part: list[Note]


class Note(BaseModel):
    note: MIDINote
    duration: float
    time: float
    velocity: int

# MIDINote >

_NAMES = ["C", "C_sharp", "D", "D_sharp", "E", "F",
          "F_sharp", "G", "G_sharp", "A", "A_sharp", "B"]

def _note_name(n: int) -> str:
    octave = n // 12 - 1
    return f"{_NAMES[n % 12]}_minus_{-octave}" if octave < 0 else f"{_NAMES[n % 12]}{octave}"

MIDINote = enum.IntEnum("MIDINote", {_note_name(n): n for n in range(128)})

# < MIDINote

class ProjectURL(BaseModel):
    name: str
    url: str