from typing import Annotated

from fastapi import Depends

from app.deps import get_app_settings
from app.security.cred_codec import UserCredentialsCodec
from app.security.fields.base import DataEncryptor
from app.security.fields.email import EmailEncryptor
from app.security.fields.string_field_schemes import StringAesSivScheme
from app.security.passwords.hasher import PasswordHasher
from app.security.passwords.schemes import BCryptPasswordHasherScheme
from app.settings import AppSettings


def get_credentials_codec(
        cfg: Annotated[AppSettings, Depends(get_app_settings)],
):
    password_schemes = {"v1": BCryptPasswordHasherScheme()}
    password_hasher = PasswordHasher(password_schemes, "v1")

    current_scheme = cfg.security.CURRENT_EMAIL_SCHEME
    email_schemes = {current_scheme: StringAesSivScheme(cfg.security.EMAIL_SECRET_KEY)}
    email_encryptor = EmailEncryptor(DataEncryptor(email_schemes, current_scheme))

    return UserCredentialsCodec(password_hasher, email_encryptor)
