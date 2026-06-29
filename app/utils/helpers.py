import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


async def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = to_email

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(
            settings.MAIL_USERNAME,
            settings.MAIL_PASSWORD,
        )
        server.send_message(msg)