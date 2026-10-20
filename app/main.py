from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.routes import tracks
from app.util.exceptions import (
    TrackAlreadyExistsException,
    TrackNotFoundException,
    UserNotFoundException,
)

app = FastAPI()
app.include_router(tracks.router)

@app.exception_handler(UserNotFoundException)
def handle_user_not_found_exception(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "User not found"})

@app.exception_handler(TrackNotFoundException)
def handle_track_not_found_exception(request: Request, exc: TrackNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "Track not found"})

@app.exception_handler(TrackAlreadyExistsException)
def handle_track_already_exists_exception(request: Request, exc: TrackAlreadyExistsException):
    return JSONResponse(status_code=409, content={"detail": "Track already exists"})