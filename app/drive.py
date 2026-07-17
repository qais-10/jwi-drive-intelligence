from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from fastapi import HTTPException

from .config import settings

DRIVE_BASE_URL = "https://www.googleapis.com/drive/v3"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
FOLDER_MIME = "application/vnd.google-apps.folder"


async def get_google_access_token() -> str:
    if not settings.google_client_id:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_CLIENT_ID is not configured.",
        )

    if not settings.google_client_secret:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_CLIENT_SECRET is not configured.",
        )

    if not settings.google_refresh_token:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_REFRESH_TOKEN is not configured.",
        )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "refresh_token": settings.google_refresh_token,
                "grant_type": "refresh_token",
            },
        )

    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail=(
                f"Google token refresh failed: "
                f"{response.status_code} {response.text}"
            ),
        )

    payload = response.json()
    access_token = payload.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=502,
            detail="Google did not return an access token.",
        )

    return access_token


class GoogleDriveClient:
    def __init__(self, access_token: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    async def _get(
        self,
        path: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{DRIVE_BASE_URL}{path}",
                headers=self.headers,
                params=params,
            )

        if response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Google authentication failed or expired.",
            )

        if response.status_code == 403:
    raise HTTPException(
        status_code=403,
        detail={
            "message": "Google Drive access was denied.",
            "google_response": response.text,
            "request_url": str(response.request.url),
        },
    )

        if response.is_error:
            raise HTTPException(
                status_code=502,
                detail=(
                    f"Google Drive API error: "
                    f"{response.status_code} {response.text}"
                ),
            )

        return response.json()

    async def list_children(
        self,
        parent_id: str,
        *,
        folders_only: bool = False,
        modified_after: Optional[datetime] = None,
        page_size: int = 1000,
    ) -> list[dict[str, Any]]:
        clauses = [
            f"'{parent_id}' in parents",
            "trashed = false",
        ]

        if folders_only:
            clauses.append(
                f"mimeType = '{FOLDER_MIME}'"
            )

        if modified_after:
            utc_value = (
                modified_after.astimezone(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
            clauses.append(
                f"modifiedTime > '{utc_value}'"
            )

        params: dict[str, Any] = {
            "q": " and ".join(clauses),
            "pageSize": min(page_size, 1000),
            "orderBy": "modifiedTime desc",
            "corpora": "drive",
            "driveId": settings.shared_drive_id,
            "fields": (
                "nextPageToken,"
                "files("
                "id,"
                "name,"
                "mimeType,"
                "modifiedTime,"
                "createdTime,"
                "parents,"
                "driveId,"
                "webViewLink"
                ")"
    ),
    "includeItemsFromAllDrives": "true",
    "supportsAllDrives": "true",
}

        files: list[dict[str, Any]] = []

        while True:
            payload = await self._get(
                "/files",
                params,
            )

            files.extend(
                payload.get("files", [])
            )

            token = payload.get("nextPageToken")

            if not token:
                break

            params["pageToken"] = token

        return files
