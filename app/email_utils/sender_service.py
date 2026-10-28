from email.message import EmailMessage
from email.utils import formatdate, make_msgid

import aiosmtplib
from pydantic import EmailStr

from app.common import SharedSettings
from app.email_utils.email_templates import EmailTemplate
from app.email_utils.renderer_service import RendererService
from app.email_utils.settings import SenderSettings
from app.util.exceptions import EmailSendError


class SenderService:
    def __init__(
            self,
            renderer: RendererService,
            sender_settings: SenderSettings,
            shared_settings: SharedSettings,
    ):
        self._renderer = renderer
        self._sender_cfg = sender_settings
        self._shared_cfg = shared_settings


    async def send(self, email: EmailStr, subject: str, content: str, html: str):
        msg = EmailMessage()
        msg["From"] = f"${self._sender_cfg.SENDER_NAME}@{self._sender_cfg.SENDER_HOST}"
        msg["To"] = email
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=self._sender_cfg.SENDER_HOST)

        msg.set_content(content)
        msg.add_alternative(html, subtype="html")

        try:
            await aiosmtplib.send(
                msg,
                hostname=self._sender_cfg.SMTP_HOST,
                port=self._sender_cfg.SMTP_PORT,
                username=self._sender_cfg.SMTP_USER,
                password=self._sender_cfg.SMTP_PASSWORD,
                start_tls=self._sender_cfg.SMTP_START_TLS,
                use_tls=self._sender_cfg.SMTP_USE_TLS,
            )
        except aiosmtplib.SMTPException as err:
            raise EmailSendError() from err


    async def send_confirm_link(self, email: EmailStr, token: str):
        match self._shared_cfg.API_PUBLIC_PORT:
            case 80:
                url = f"http://{self._shared_cfg.API_PUBLIC_HOST}/auth/email-confirm/{token}"
            case 443:
                url = f"https://{self._shared_cfg.API_PUBLIC_HOST}/auth/email-confirm/{token}"
            case _:
                url = f"http://{self._shared_cfg.API_PUBLIC_HOST}:{self._shared_cfg.API_PUBLIC_PORT}/auth/email-confirm/{token}"

        subject, content, html = self._renderer.render(
            EmailTemplate.EMAIL_CONFIRMATION,
            {"url": url, "domain": self._shared_cfg.SMTP_HOST_DOMAIN}
        )

        await self.send(email, subject, content, html)

