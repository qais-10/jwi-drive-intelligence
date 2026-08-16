import pytest

from app.vendors.agent import review_submission
from app.vendors.constants import DEFAULT_REQUIRED_FIELDS


@pytest.mark.asyncio
async def test_review_submission_complete():
    fields = {
        "company_name": "Acme Co",
        "contact_name": "Jane Doe",
        "contact_email": "jane@acme.com",
        "phone": "555-123-4567",
        "company_address": "123 Main St",
        "service_category": "Printing",
        "tax_id": "12-3456789",
    }
    decision = await review_submission(fields, required_fields=DEFAULT_REQUIRED_FIELDS)
    assert decision.complete is True
    assert decision.missing_fields == []


@pytest.mark.asyncio
async def test_review_submission_flags_blank_fields():
    fields = {
        "company_name": "Acme Co",
        "contact_name": "",
        "contact_email": "jane@acme.com",
        "phone": None,
        "company_address": "123 Main St",
        "service_category": "Printing",
        "tax_id": "12-3456789",
    }
    decision = await review_submission(fields, required_fields=DEFAULT_REQUIRED_FIELDS)
    assert decision.complete is False
    assert decision.missing_fields == ["contact_name", "phone"]


@pytest.mark.asyncio
async def test_review_submission_flags_junk_placeholders():
    fields = {
        "company_name": "Acme Co",
        "contact_name": "Jane Doe",
        "contact_email": "jane@acme.com",
        "phone": "N/A",
        "company_address": "123 Main St",
        "service_category": "tbd",
        "tax_id": "12-3456789",
    }
    decision = await review_submission(fields, required_fields=DEFAULT_REQUIRED_FIELDS)
    assert decision.complete is False
    assert decision.missing_fields == ["phone", "service_category"]
