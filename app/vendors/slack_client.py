from __future__ import annotations

import httpx
from fastapi import HTTPException

from ..config import settings


class SlackClient:
    """Posts to a Slack Incoming Webhook — no bot user, no channel invite.

    The webhook URL is already scoped to a single channel when it's created
    in Slack, so callers just send text.
    """

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url or settings.slack_webhook_url
        if not self.webhook_url:
            raise HTTPException(
                status_code=500,
                detail="SLACK_WEBHOOK_URL is not configured.",
            )

    async def post_message(self, text: str) -> None:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(self.webhook_url, json={"text": text})

        if response.is_error:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Slack webhook request failed.",
                    "response": response.text,
                },
            )
