from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from app.auth.auth_service import AuthService
from app.auth.confirmation.service import EmailConfirmService
from app.auth.deps import get_auth_service, get_email_confirm_service, get_register_service
from app.auth.register_service import RegisterService
from app.db.schemas import LoginForm, RegisterForm, TokenOut
from app.util.exceptions import BadCredentialsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(
        form: LoginForm,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_service.login(form.email, form.password)



@router.get("/email-confirm/{token}", status_code=status.HTTP_204_NO_CONTENT)
def confirm_email(
        email_confirmation_service: Annotated[EmailConfirmService | None, Depends(get_email_confirm_service)],
        token: str,
):
    if email_confirmation_service is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    email_confirmation_service.confirm(token)


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register(
        form: RegisterForm,
        register_service: Annotated[RegisterService, Depends(get_register_service)],
        background: BackgroundTasks,
):
    if form.password != form.password_confirm:
        raise BadCredentialsException()

    user = register_service.register(form.email, form.password)
    background.add_task(register_service.send_confirmation, user.id, user.email)
