from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any

from .config import settings
from .drive import GoogleDriveClient
from .models import ProjectSummary

PROJECT_PATTERN = re.compile(
    r"^(?P<job_code>J[A-Za-z0-9]+)_(?P<client>[^_]+)_(?P<project_name>.+)$",
    re.IGNORECASE,
)


def parse_project_folder(folder_name: str, fallback_client: str) -> tuple[str | None, str, str]:
    match = PROJECT_PATTERN.match(folder_name.strip())
    if not match:
        return None, fallback_client, folder_name.strip()

    return (
        match.group("job_code"),
        fallback_client,
        match.group("project_name").strip(),
    )


async def find_named_folder(
    drive: GoogleDriveClient,
    parent_id: str,
    folder_name: str,
) -> dict[str, Any] | None:
    folders = await drive.list_children(parent_id, folders_only=True)
    target = folder_name.casefold().strip()
    for folder in folders:
        if folder.get("name", "").casefold().strip() == target:
            return folder
    return None


async def get_recent_projects(
    drive: GoogleDriveClient,
    *,
    days: int,
    client_filter: str | None = None,
) -> list[ProjectSummary]:
    modified_after = datetime.now(timezone.utc) - timedelta(days=days)
    client_folders = await drive.list_children(
        settings.clients_root_folder_id,
        folders_only=True,
    )

    results: list[ProjectSummary] = []
    for client_folder in client_folders[: settings.max_clients]:
        client_name = client_folder["name"].strip()
        if client_filter and client_filter.casefold() not in client_name.casefold():
            continue

        working_folder = await find_named_folder(
            drive,
            client_folder["id"],
            settings.active_work_folder_name,
        )
        if not working_folder:
            continue

        project_folders = await drive.list_children(
            working_folder["id"],
            folders_only=True,
        )

        for project_folder in project_folders[: settings.max_projects_per_client]:
            recent_files = await drive.list_children(
                project_folder["id"],
                modified_after=modified_after,
            )
            if not recent_files:
                continue

            job_code, parsed_client, project_name = parse_project_folder(
                project_folder["name"],
                client_name,
            )
            latest = recent_files[0].get("modifiedTime")
            results.append(
                ProjectSummary(
                    project_id=project_folder["id"],
                    job_code=job_code,
                    client=parsed_client,
                    project_name=project_name,
                    folder_url=project_folder.get(
                        "webViewLink",
                        f"https://drive.google.com/drive/folders/{project_folder['id']}",
                    ),
                    last_activity=latest,
                    recent_file_count=len(recent_files),
                )
            )

    results.sort(
        key=lambda item: item.last_activity or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return results
