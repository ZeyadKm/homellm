"""Lightweight SMTP helper."""
from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .agent import EmailSettings


def send_email(settings: EmailSettings, subject: str, body: str) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.sender
    message["To"] = ", ".join(settings.recipients)
    message.set_content(body)

    with smtplib.SMTP(settings.host, settings.port, timeout=30) as client:
        if settings.use_tls:
            client.starttls()
        if settings.username and settings.password:
            client.login(settings.username, settings.password)
        client.send_message(message)
