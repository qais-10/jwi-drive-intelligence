from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException

from ..config import settings
from . import service
from .models import DeadlineCheckResult, VendorSubmission, VendorSubmissionResult

router = APIRouter(tags=["vendors"])


@router.post(
    "/vendors/submit",
    response_model=VendorSubmissionResult,
    operation_id="submitVendorInformation",
    summary="Receive a new vendor submission from the website intake form",
    description=(
        "Creates the vendor as a New Submission item on the monday.com "
        "vendor-approval board, then runs the AI completeness check. "
        "Complete submissions move to Under Review and ops/management "
        "are notified in Slack. Incomplete submissions trigger an email "
        "to the vendor listing what's missing."
    ),
)
async def submit_vendor(submission: VendorSubmission) -> VendorSubmissionResult:
    return await service.handle_new_submission(submission)


@router.post(
    "/cron/vendor-deadlines",
    response_model=DeadlineCheckResult,
    operation_id="checkVendorApprovalDeadlines",
    summary="Slack-remind ops/management about overdue vendor approvals",
    description=(
        "Intended to be called on a daily schedule (e.g. Cloud Scheduler). "
        "Scans the Under Review group for items past their "
        f"{settings.approval_deadline_business_days}-business-day approval "
        "deadline and posts a Slack reminder for each one."
    ),
)
async def vendor_deadlines(
    x_cron_secret: str | None = Header(default=None),
) -> DeadlineCheckResult:
    if settings.cron_secret and x_cron_secret != settings.cron_secret:
        raise HTTPException(status_code=401, detail="Invalid cron secret.")
    return await service.check_overdue_reviews()
