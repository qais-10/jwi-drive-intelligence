from __future__ import annotations

from typing import Any, Optional

import httpx
from fastapi import HTTPException

from ..config import settings

SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


class SlackClient:
    def __init__(self, bot_token: Optional[str] = None) -> None:
        token = bot_token or settings.slack_bot_token
        if not token:
            raise HTTPException(
                status_code=500,
                detail="SLACK_BOT_TOKEN is not configured.",
            )
        self.headers = {"Authorization": f"Bearer {token}"}

    async def post_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        payload: dict[str, Any] = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                SLACK_POST_MESSAGE_URL,
                headers=self.headers,
                json=payload,
            )

        if response.is_error:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Slack API request failed.",
                    "response": response.text,
                },
            )

        data = response.json()
        if not data.get("ok"):
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Slack API returned an error.",
                    "slack_response": data,
                },
            )
