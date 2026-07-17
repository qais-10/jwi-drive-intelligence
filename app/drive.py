from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from fastapi import HTTPException

DRIVE_BASE_URL = "https://www.googleapis.com/drive/v3"
FOLDER_MIME = "application/vnd.google-apps.folder"


class GoogleDriveClient:
    def __init__(self, access_token: str) -> None:
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{DRIVE_BASE_URL}{path}",
                headers=self.headers,
                params=params,
            )

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Google authentication failed or expired.")
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="Google Drive access was denied.")
        if response.is_error:
            raise HTTPException(
                status_code=502,
                detail=f"Google Drive API error: {response.status_code} {response.text}",
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
        clauses = [f"'{parent_id}' in parents", "trashed = false"]
        if folders_only:
            clauses.append(f"mimeType = '{FOLDER_MIME}'")
        if modified_after:
            utc_value = modified_after.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
            clauses.append(f"modifiedTime > '{utc_value}'")

        params: dict[str, Any] = {
            "q": " and ".join(clauses),
            "pageSize": min(page_size, 1000),
            "orderBy": "modifiedTime desc",
            "fields": "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,parents,driveId,webViewLink)",
            "includeItemsFromAllDrives": "true",
            "supportsAllDrives": "true",
        }

        files: list[dict[str, Any]] = []
        while True:
            payload = await self._get("/files", params)
            files.extend(payload.get("files", []))
            token = payload.get("nextPageToken")
            if not token:
                break
            params["pageToken"] = token
        return files
