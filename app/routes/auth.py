from typing import Annotated

from fastapi import APIRouter, Depends

from app.data.schemas import LoginForm, RegisterForm, TokenOut
from app.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.util.exceptions import BadCredentialsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(
        form: LoginForm,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_service.authenticate(form.email, form.password)


@router.post("/register", response_model=TokenOut)
def register(
        form: RegisterForm,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    if form.password != form.password_confirm:
        raise BadCredentialsException()

    return auth_service.register(form.email, form.password)
