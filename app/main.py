from fastapi import Depends, FastAPI, Header, HTTPException, Query

from .config import settings
from .drive import GoogleDriveClient
from .models import RecentProjectsResponse
from .projects import get_recent_projects

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "JWI project intelligence API. It scans each client's 01. Working folder "
        "and returns active project folders with recent file activity."
    ),
)


def extract_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Google OAuth bearer token.")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty Google OAuth bearer token.")
    return token


@app.get("/health", operation_id="healthCheck")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get(
    "/projects/recent",
    response_model=RecentProjectsResponse,
    operation_id="getRecentClientProjects",
    summary="Find active JWI client projects with recent document activity",
    description=(
        "Use this whenever the user asks about current, recent, active, ongoing or updated "
        "JWI client projects. It scans only each client's 01. Working folder and does not "
        "treat general Drive recency as a project update."
    ),
)
async def recent_projects(
    days: int = Query(default=settings.default_days, ge=1, le=365),
    client: str | None = Query(
        default=None,
        description="Optional client-name filter, for example Epson.",
    ),
    access_token: str = Depends(extract_bearer_token),
) -> RecentProjectsResponse:
    drive = GoogleDriveClient(access_token)
    projects = await get_recent_projects(drive, days=days, client_filter=client)
    return RecentProjectsResponse(scanned_days=days, projects=projects)
