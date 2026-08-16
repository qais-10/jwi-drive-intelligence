from __future__ import annotations

from datetime import date
from typing import Any

from ..config import settings
from . import constants
from .agent import review_submission
from .business_days import add_business_days, is_past_deadline
from .email_client import EmailClient
from .models import DeadlineCheckResult, VendorSubmission, VendorSubmissionResult
from .monday_client import MondayClient, column_text
from .slack_client import SlackClient


def _vendor_fields(submission: VendorSubmission) -> dict[str, Any]:
    data = submission.model_dump(exclude={"extra_fields"})
    data.update(submission.extra_fields)
    return data


def _item_url(item_id: str) -> str:
    return f"https://monday.com/boards/{settings.monday_board_id}/pulses/{item_id}"


async def handle_new_submission(submission: VendorSubmission) -> VendorSubmissionResult:
    monday = MondayClient()

    # The board's item name column is the contact person's name (it mirrors
    # the JWI Contacts board); Company Name is a separate text column.
    item_id = await monday.create_item(
        settings.monday_board_id,
        settings.monday_group_new_submission,
        submission.contact_name,
        {
            settings.monday_col_company_name: submission.company_name,
            settings.monday_col_contact_email: submission.contact_email,
            settings.monday_col_phone: (
                {"phone": submission.phone, "countryShortName": "US"}
                if submission.phone
                else ""
            ),
            settings.monday_col_company_address: submission.company_address or "",
            settings.monday_col_service_category: submission.service_category or "",
            settings.monday_col_tax_id: submission.tax_id or "",
            settings.monday_col_submission_date: {"date": date.today().isoformat()},
        },
    )

    decision = await review_submission(_vendor_fields(submission))

    if decision.complete:
        deadline = add_business_days(date.today(), settings.approval_deadline_business_days)
        await monday.change_column_values(
            settings.monday_board_id,
            item_id,
            {
                settings.monday_col_approval_status: {"label": constants.STATUS_PENDING_REVIEW},
                settings.monday_col_approval_deadline: {"date": deadline.isoformat()},
                settings.monday_col_missing_fields: "",
                settings.monday_col_ai_notes: decision.notes,
            },
        )
        # Moving Approved/Rejected items out of Under Review is handled by
        # native monday.com board automations, not here — but the initial
        # New Submission -> Under Review move has no status-change trigger
        # to hang off of, so it still happens explicitly.
        await monday.move_item_to_group(item_id, settings.monday_group_under_review)
        await _notify_slack_new_submission(submission, item_id)
        status = "under_review"
    else:
        await monday.change_column_values(
            settings.monday_board_id,
            item_id,
            {
                settings.monday_col_missing_fields: ", ".join(decision.missing_fields),
                settings.monday_col_ai_notes: decision.notes,
            },
        )
        await _email_missing_info(submission, decision.missing_fields)
        status = "awaiting_vendor_info"

    return VendorSubmissionResult(
        monday_item_id=item_id,
        status=status,
        missing_fields=decision.missing_fields,
        notes=decision.notes or None,
    )


async def _notify_slack_new_submission(submission: VendorSubmission, item_id: str) -> None:
    if not settings.slack_bot_token or not settings.slack_channel_ops:
        return

    slack = SlackClient()
    await slack.post_message(
        settings.slack_channel_ops,
        (
            f":inbox_tray: New vendor submission ready for review: "
            f"*{submission.company_name}* ({submission.contact_email})\n"
            f"<{_item_url(item_id)}|Open in monday.com> — approval is due within "
            f"{settings.approval_deadline_business_days} business days."
        ),
    )


async def _email_missing_info(submission: VendorSubmission, missing_fields: list[str]) -> None:
    if not settings.smtp_host:
        return

    email = EmailClient()
    field_list = "\n".join(
        f"- {name.replace('_', ' ').title()}" for name in missing_fields
    )
    form_line = (
        f"Please complete the form again here: {settings.vendor_form_url}\n\n"
        if settings.vendor_form_url
        else "Please reply to this email with the missing details.\n\n"
    )
    body = (
        f"Hi {submission.contact_name},\n\n"
        "Thanks for submitting your vendor information. Before we can move "
        "your application forward, we need a bit more detail:\n\n"
        f"{field_list}\n\n"
        f"{form_line}"
        "Thanks,\nVendor Onboarding Team"
    )
    await email.send(
        submission.contact_email,
        "Action needed: complete your vendor application",
        body,
    )


async def check_overdue_reviews() -> DeadlineCheckResult:
    """Scan the Under Review group and Slack-remind on anything past its deadline."""
    monday = MondayClient()
    items = await monday.get_items_in_group(
        settings.monday_board_id,
        settings.monday_group_under_review,
    )

    today = date.today()
    overdue_ids: list[str] = []
    reminders_sent = 0

    for item in items:
        status = column_text(item, settings.monday_col_approval_status)
        if status and status != constants.STATUS_PENDING_REVIEW:
            continue

        deadline_text = column_text(item, settings.monday_col_approval_deadline)
        if not deadline_text:
            continue

        deadline = date.fromisoformat(deadline_text)
        if not is_past_deadline(deadline, today=today):
            continue

        overdue_ids.append(item["id"])

        last_reminder_text = column_text(item, settings.monday_col_last_reminder_sent)
        if last_reminder_text == today.isoformat():
            continue  # already reminded today

        if settings.slack_bot_token and settings.slack_channel_ops:
            slack = SlackClient()
            await slack.post_message(
                settings.slack_channel_ops,
                (
                    f":rotating_light: Vendor approval overdue: *{item['name']}* has been "
                    f"awaiting a decision past its {settings.approval_deadline_business_days}-"
                    f"business-day deadline (due {deadline.isoformat()}).\n"
                    f"<{_item_url(item['id'])}|Review now>"
                ),
            )
            reminders_sent += 1

        await monday.change_column_values(
            settings.monday_board_id,
            item["id"],
            {settings.monday_col_last_reminder_sent: {"date": today.isoformat()}},
        )

    return DeadlineCheckResult(
        checked_items=len(items),
        reminders_sent=reminders_sent,
        overdue_item_ids=overdue_ids,
    )
