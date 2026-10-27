from pydantic import EmailStr

from app.auth.confirm_policy import ConfirmationPolicy
from app.auth.sessions import SessionService
from app.db.schemas import TokenOut
from app.repositories.user_repository import UserRepository
from app.security.cred_codec import UserCredentialsCodec
from app.util.exceptions import BadCredentialsException, EmailNotConfirmedException, UserBannedException


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository,
            cred_codec: UserCredentialsCodec,
            confirm_policy: ConfirmationPolicy,
            tokens: SessionService,
    ):
        self.user_repository = user_repository
        self.cred_codec = cred_codec
        self.confirm_policy = confirm_policy
        self.tokens = tokens


    def authenticate(self, email: EmailStr, password: str) -> int:
        email_cipher = self.cred_codec.encrypt_email(email)
        user = self.user_repository.get_by_email_cipher(email_cipher)
        password_ok = self.cred_codec.verify_password(password, user.password_hash if user else None)

        if user is None or not password_ok:
            raise BadCredentialsException()
        if user.banned:
            raise UserBannedException()
        if self.confirm_policy.required and not user.email_confirmed:
            raise EmailNotConfirmedException()

        return user.id


    def login(self, email: EmailStr, password: str) -> TokenOut:
        user_id = self.authenticate(email, password)
        return TokenOut(access_token=self.tokens.generate_access_token(user_id), token_type="Bearer") # noqa: S106
