from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectSummary(BaseModel):
    project_id: str
    job_code: Optional[str] = None
    client: str
    project_name: str
    folder_url: str
    last_activity: Optional[datetime] = None
    status: str = "active"
    recent_file_count: int = 0
    public_shareability: str = "approval_required"


class RecentProjectsResponse(BaseModel):
    scanned_days: int = Field(ge=1, le=365)
    projects: list[ProjectSummary]
