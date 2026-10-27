from urllib.request import Request

from fastapi import FastAPI
from jwt import ExpiredSignatureError
from starlette.responses import JSONResponse

from app.routes import auth, projects
from app.util.exceptions import (
    BadCredentialsException,
    EmailAlreadyBusyException,
    EmailNotConfirmedException,
    InvalidConfirmationTokenException,
    ProjectAlreadyExistsException,
    UserBannedException,
    NotFoundException,
)

app = FastAPI()
app.include_router(projects.router)
app.include_router(auth.router)

@app.exception_handler(NotFoundException)
def handle_user_not_found_exception(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.entity} not found{f": {exc.details}" if exc.details else ""}"}
    )

@app.exception_handler(ProjectAlreadyExistsException)
def handle_project_already_exists_exception(request: Request, exc: ProjectAlreadyExistsException):
    return JSONResponse(status_code=409, content={"detail": "Project already exists"})

@app.exception_handler(BadCredentialsException)
def handle_bad_credentials_exception(request: Request, exc: BadCredentialsException):
    return JSONResponse(status_code=401, content={"detail": "Bad credentials"})

@app.exception_handler(UserBannedException)
def handle_user_banned_exception(request: Request, exc: UserBannedException):
    return JSONResponse(status_code=401, content={"detail": "User banned"})

@app.exception_handler(EmailAlreadyBusyException)
def handle_email_already_busy(request: Request, exc: EmailAlreadyBusyException):
    return JSONResponse(status_code=401, content={"detail": "Email already busy"})

@app.exception_handler(ExpiredSignatureError)
def handle_expired_signature_exception(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(status_code=401, content={"detail": "Expired token signature"})

@app.exception_handler(InvalidConfirmationTokenException)
def handle_invalid_confirmation_token_exception(request: Request, exc: InvalidConfirmationTokenException):
    return JSONResponse(status_code=401, content={"detail": "Invalid confirmation token"})

@app.exception_handler(EmailNotConfirmedException)
def handle_email_not_confirmed_exception(request: Request, exc: EmailNotConfirmedException):
    return JSONResponse(status_code=401, content={"detail": "Email not confirmed"})
