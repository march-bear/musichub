import asyncio
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

import aiosmtplib
from pydantic import EmailStr

from app.settings import settings


class EmailService:
    def __init__(self):
        pass


    def send_token_to_email(self, email: EmailStr, token: str):
        match settings.APP_API_PUBLIC_PORT:
            case 80:
                url = f"http://{settings.APP_API_PUBLIC_HOST}/auth/email-confirm/{token}"
            case 443:
                url = f"https://{settings.APP_API_PUBLIC_HOST}/auth/email-confirm/{token}"
            case _:
                url = f"http://{settings.APP_API_PUBLIC_HOST}:{settings.APP_API_PUBLIC_PORT}/auth/email-confirm/{token}"

        msg = EmailMessage()
        msg["From"] = f"noreply@{settings.SMTP_HOST_DOMAIN}"
        msg["To"] = email
        msg["Subject"] = "Подтверждение адреса электронной почты"
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=settings.SMTP_HOST_DOMAIN)

        msg.set_content(url)

        msg.add_alternative(
            f"<h2>Ваша почта была указана для регистрации на сайте {settings.SMTP_HOST_DOMAIN}</h2>"
            f"<p>Для потверждения адреса перейдите по ссылке ниже."
            f"Если вы не проходили регистрацию, проигнорируйте сообщение</p>"
            f"<a href={url}>{url}</a>",
            subtype="html",
        )

        async def _send():
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                start_tls=False,
            )

        asyncio.run(_send())
