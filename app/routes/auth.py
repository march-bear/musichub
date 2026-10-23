from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.data.schemas import EmailConfirmTokenOut, LoginForm, RegisterForm, TokenOut
from app.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.settings import settings
from app.util.exceptions import BadCredentialsException

if settings.EMAIL_CHECK_ENABLED:
    from app.dependencies import get_email_confirmation_service
    from app.services.auth_service import EmailConfirmationService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(
        form: LoginForm,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_service.authenticate(form.email, form.password)


if settings.EMAIL_CHECK_ENABLED:
    @router.get("/email-confirm/{token}", status_code=status.HTTP_204_NO_CONTENT)
    def confirm_email(
            email_confirmation_service: Annotated[EmailConfirmationService, Depends(get_email_confirmation_service)],
            token: str,
    ):
        email_confirmation_service.confirm(token)


    @router.post("/register", response_model=EmailConfirmTokenOut)
    def register(
            form: RegisterForm,
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
            email_confirm_service: Annotated[EmailConfirmationService, Depends(get_email_confirmation_service)],
    ):
        if form.password != form.password_confirm:
            raise BadCredentialsException()

        user_id, _ = auth_service.register(form.email, form.password)

        return email_confirm_service.create_token(user_id)
else:
    @router.post("/register", response_model=TokenOut)
    def register(
            form: RegisterForm,
            auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ):
        if form.password != form.password_confirm:
            raise BadCredentialsException()

        _, token = auth_service.register(form.email, form.password)
        return token
