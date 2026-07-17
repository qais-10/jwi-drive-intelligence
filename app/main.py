from fastapi import FastAPI, Query

from .config import settings
from .drive import (
    GoogleDriveClient,
    get_google_access_token,
)
from .models import RecentProjectsResponse
from .projects import get_recent_projects

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description=(
        "JWI project intelligence API. "
        "It scans each client's 01. Working folder "
        "and returns active project folders "
        "with recent file activity."
    ),
)


@app.get(
    "/health",
    operation_id="healthCheck",
)
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }


@app.get(
    "/projects/recent",
    response_model=RecentProjectsResponse,
    operation_id="getRecentClientProjects",
    summary=(
        "Find active JWI client projects "
        "with recent document activity"
    ),
    description=(
        "Use this whenever the user asks about "
        "current, recent, active, ongoing, "
        "or updated JWI client projects. "
        "It scans only each client's 01. Working folder."
    ),
)
async def recent_projects(
    days: int = Query(
        default=settings.default_days,
        ge=1,
        le=365,
    ),
    client: str | None = Query(
        default=None,
        description=(
            "Optional client-name filter, "
            "for example Epson."
        ),
    ),
) -> RecentProjectsResponse:
    access_token = await get_google_access_token()

    drive = GoogleDriveClient(access_token)

    projects = await get_recent_projects(
        drive,
        days=days,
        client_filter=client,
    )

    return RecentProjectsResponse(
        scanned_days=days,
        projects=projects,
    )
