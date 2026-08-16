"""One-time helper that provisions the vendor-approval board on monday.com.

Run with MONDAY_API_TOKEN set (in the environment or .env):

    python -m scripts.setup_monday_board "Vendor Approvals"

It creates the board, the four workflow groups (New Submission, Under
Review, Approved Vendor, Archived), and the tracking columns, then prints
a ready-to-paste .env block with the generated IDs. monday.com also adds a
default "Group Title" group to every new board; delete or rename it by
hand afterwards.
"""

from __future__ import annotations

import asyncio
import sys

from app.vendors import constants
from app.vendors.monday_client import MondayClient

TEXT_COLUMNS = [
    ("Contact Name", "text", "MONDAY_COL_CONTACT_NAME"),
    ("Contact Email", "email", "MONDAY_COL_CONTACT_EMAIL"),
    ("Phone", "phone", "MONDAY_COL_PHONE"),
    ("Company Address", "text", "MONDAY_COL_COMPANY_ADDRESS"),
    ("Service Category", "text", "MONDAY_COL_SERVICE_CATEGORY"),
    ("Tax ID / EIN", "text", "MONDAY_COL_TAX_ID"),
    ("Submission Date", "date", "MONDAY_COL_SUBMISSION_DATE"),
    ("Missing Fields", "long_text", "MONDAY_COL_MISSING_FIELDS"),
    ("AI Review Notes", "long_text", "MONDAY_COL_AI_NOTES"),
    ("Approval Deadline", "date", "MONDAY_COL_APPROVAL_DEADLINE"),
    ("Last Reminder Sent", "date", "MONDAY_COL_LAST_REMINDER_SENT"),
]

STATUS_COLUMN = (
    "Approval Status",
    "status",
    "MONDAY_COL_APPROVAL_STATUS",
    {
        "labels": {
            "0": constants.STATUS_PENDING_REVIEW,
            "1": constants.STATUS_APPROVED,
            "2": constants.STATUS_REJECTED,
        }
    },
)

GROUPS = [
    (constants.GROUP_NEW_SUBMISSION, "MONDAY_GROUP_NEW_SUBMISSION"),
    (constants.GROUP_UNDER_REVIEW, "MONDAY_GROUP_UNDER_REVIEW"),
    (constants.GROUP_APPROVED_VENDOR, "MONDAY_GROUP_APPROVED_VENDOR"),
    (constants.GROUP_ARCHIVED, "MONDAY_GROUP_ARCHIVED"),
]


async def main(board_name: str) -> None:
    monday = MondayClient()

    board_id = await monday.create_board(board_name)
    print(f"Created board {board_name!r} -> {board_id}\n")

    env_lines = [f"MONDAY_BOARD_ID={board_id}"]

    for display_name, env_key in GROUPS:
        group_id = await monday.create_group(board_id, display_name)
        env_lines.append(f"{env_key}={group_id}")
        print(f"Group {display_name!r} -> {group_id}")

    for title, column_type, env_key in TEXT_COLUMNS:
        column_id = await monday.create_column(board_id, title, column_type)
        env_lines.append(f"{env_key}={column_id}")
        print(f"Column {title!r} ({column_type}) -> {column_id}")

    status_title, status_type, status_env_key, status_defaults = STATUS_COLUMN
    status_column_id = await monday.create_column(
        board_id, status_title, status_type, defaults=status_defaults
    )
    env_lines.append(f"{status_env_key}={status_column_id}")
    print(f"Column {status_title!r} ({status_type}) -> {status_column_id}")

    print("\nPaste this into your .env:\n")
    print("\n".join(env_lines))


if __name__ == "__main__":
    board_name = sys.argv[1] if len(sys.argv) > 1 else "Vendor Approvals"
    asyncio.run(main(board_name))
