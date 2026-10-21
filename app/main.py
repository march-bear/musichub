from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.routes import projects
from app.util.exceptions import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    UserNotFoundException,
)

app = FastAPI()
app.include_router(projects.router)

@app.exception_handler(UserNotFoundException)
def handle_user_not_found_exception(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "User not found"})

@app.exception_handler(ProjectNotFoundException)
def handle_project_not_found_exception(request: Request, exc: ProjectNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "Project not found"})

@app.exception_handler(ProjectAlreadyExistsException)
def handle_project_already_exists_exception(request: Request, exc: ProjectAlreadyExistsException):
    return JSONResponse(status_code=409, content={"detail": "Project already exists"})
