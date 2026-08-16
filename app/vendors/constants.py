from __future__ import annotations

from ..config import settings

# Display names used by scripts/setup_monday_board.py when creating groups
# and the approval-status column. The actual group/column IDs monday.com
# assigns live in Settings (monday_group_*, monday_col_approval_status).
GROUP_NEW_SUBMISSION = "New Submission"
GROUP_UNDER_REVIEW = "Under Review"
GROUP_APPROVED_VENDOR = "Approved Vendor"
GROUP_ARCHIVED = "Archived"

STATUS_PENDING_REVIEW = "Pending Review"
STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"

DEFAULT_REQUIRED_FIELDS = [
    "company_name",
    "contact_name",
    "contact_email",
    "phone",
    "company_address",
    "service_category",
    "tax_id",
]

# Common placeholder junk vendors type into required fields instead of
# leaving them blank.
JUNK_VALUES = {
    "n/a",
    "na",
    "n.a",
    "none",
    "test",
    "asdf",
    "-",
    "tbd",
    "pending",
    "xxx",
    ".",
}


def resolve_required_fields() -> list[str]:
    if not settings.vendor_required_fields:
        return DEFAULT_REQUIRED_FIELDS
    return [
        field.strip()
        for field in settings.vendor_required_fields.split(",")
        if field.strip()
    ]
