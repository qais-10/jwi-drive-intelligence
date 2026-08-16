from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JWI Drive Intelligence API"

    clients_root_folder_id: str = "1-3FfMbvGrddiOHboFeNxUOAy6ds8uIFM"
    active_work_folder_name: str = "01. Working"
    shared_drive_id: str = "0AM6Po6F6qN0UUk9PVA"

    google_client_id: str = ""
    google_client_secret: str = ""
    google_refresh_token: str = ""

    default_days: int = 45
    max_clients: int = 100
    max_projects_per_client: int = 100

    # --- Vendor approval automation (monday.com) ---

    monday_api_token: str = ""
    monday_board_id: str = ""

    # Group IDs on the vendor-approval board. Populate these after running
    # scripts/setup_monday_board.py, which creates the board and prints the
    # generated IDs.
    monday_group_new_submission: str = ""
    monday_group_under_review: str = ""
    monday_group_approved_vendor: str = ""
    monday_group_archived: str = ""

    # Column IDs on the vendor-approval board. Also populated by
    # scripts/setup_monday_board.py.
    monday_col_contact_name: str = ""
    monday_col_contact_email: str = ""
    monday_col_phone: str = ""
    monday_col_company_address: str = ""
    monday_col_service_category: str = ""
    monday_col_tax_id: str = ""
    monday_col_submission_date: str = ""
    monday_col_missing_fields: str = ""
    monday_col_ai_notes: str = ""
    monday_col_approval_status: str = ""
    monday_col_approval_deadline: str = ""
    monday_col_last_reminder_sent: str = ""

    # Shared secret appended as ?token=... to the monday.com webhook URL.
    # monday.com does not sign webhook payloads, so this is how we confirm
    # inbound requests actually came from the webhook we registered.
    monday_webhook_secret: str = ""

    # Shared secret expected in the X-Cron-Secret header on the deadline
    # check endpoint, e.g. from a Cloud Scheduler job.
    cron_secret: str = ""

    slack_bot_token: str = ""
    slack_channel_ops: str = ""

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    email_from: str = ""

    # Public URL of the vendor intake form, linked in "missing info" emails.
    vendor_form_url: str = ""

    # Optional AI-augmented completeness review. Leave anthropic_api_key
    # empty to fall back to the deterministic required-field check only.
    anthropic_api_key: str = ""
    anthropic_model: str = ""

    # Comma-separated list of required submission fields, e.g.
    # "company_name,contact_name,contact_email,tax_id". Falls back to
    # app.vendors.constants.DEFAULT_REQUIRED_FIELDS when empty.
    vendor_required_fields: str = ""

    approval_deadline_business_days: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
