from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


class VendorSubmission(BaseModel):
    company_name: str
    contact_name: str
    contact_email: EmailStr
    phone: Optional[str] = None
    company_address: Optional[str] = None
    service_category: Optional[str] = None
    tax_id: Optional[str] = None
    # Anything else the website form collects that isn't one of the
    # first-class fields above, but should still be considered by the
    # completeness check (e.g. custom required fields per vendor_required_fields).
    extra_fields: dict[str, Any] = Field(default_factory=dict)


class VendorSubmissionResult(BaseModel):
    monday_item_id: str
    status: str  # "under_review" | "awaiting_vendor_info"
    missing_fields: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class DeadlineCheckResult(BaseModel):
    checked_items: int
    reminders_sent: int
    overdue_item_ids: list[str] = Field(default_factory=list)
