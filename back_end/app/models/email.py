from pathlib import Path
from typing import Any, Dict, List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from app.config import settings

TEMPLATE_FOLDER = Path(__file__).resolve().parent.parent.parent / "templates"


class EmailTemplate(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str


config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER,
)


async def sendEmail(email: EmailTemplate) -> None:
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        body=email.body,
        subtype=MessageType.html,
    )
    await FastMail(config).send_message(message)


async def sendTemplateEmail(
    recipients: List[str], subject: str, template_name: str, context: Dict[str, Any]
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html,
    )
    await FastMail(config).send_message(message, template_name=template_name)
