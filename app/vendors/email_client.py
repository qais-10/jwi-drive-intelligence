from __future__ import annotations

import asyncio
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException

from ..config import settings


class EmailClient:
    def __init__(self) -> None:
        if not settings.smtp_host:
            raise HTTPException(
                status_code=500,
                detail="SMTP_HOST is not configured.",
            )
        if not settings.email_from:
            raise HTTPException(
                status_code=500,
                detail="EMAIL_FROM is not configured.",
            )

    async def send(self, to_email: str, subject: str, body_text: str) -> None:
        await asyncio.to_thread(self._send_sync, to_email, subject, body_text)

    def _send_sync(self, to_email: str, subject: str, body_text: str) -> None:
        message = EmailMessage()
        message["From"] = settings.email_from
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body_text)

        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
                if settings.smtp_use_tls:
                    server.starttls()
                if settings.smtp_username:
                    server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(message)
        except smtplib.SMTPException as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to send email: {exc}",
            ) from exc
