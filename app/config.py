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
    #
    # Wired to the JWI "Vendor" board (workspace: CRM). The Approved/Rejected
    # -> group move is handled by two native monday.com board automations
    # (workflow IDs 1718627611 and 1718627615), not by this service — nothing
    # here needs to move items between groups. Run
    # scripts/setup_monday_board.py only if provisioning a *new* board.

    monday_api_token: str = ""
    monday_board_id: str = "5100825568"

    monday_group_new_submission: str = "group_mm69drm1"
    monday_group_under_review: str = "group_mm69t22b"
    monday_group_approved_vendor: str = "topics"
    monday_group_archived: str = "group_mm695ejb"

    # Column IDs on the vendor-approval board.
    monday_col_company_name: str = "text_mm5gy3dh"
    monday_col_contact_email: str = "text_mm5gcy7t"
    monday_col_phone: str = "phone_mm5g2yz8"
    monday_col_company_address: str = "text_mm69hrvh"
    monday_col_service_category: str = "text_mm69p6nq"
    monday_col_tax_id: str = "text_mm69vs33"
    monday_col_submission_date: str = "date_mm69ca9q"
    monday_col_missing_fields: str = "long_text_mm69bjxw"
    monday_col_ai_notes: str = "long_text_mm69712x"
    monday_col_approval_status: str = "color_mm694nww"
    monday_col_approval_deadline: str = "date_mm69ma38"
    monday_col_last_reminder_sent: str = "date_mm69cpa6"

    # Shared secret expected in the X-Cron-Secret header on the deadline
    # check endpoint, e.g. from a Cloud Scheduler job.
    cron_secret: str = ""

    # Slack Incoming Webhook URL for the ops channel (Slack app -> Incoming
    # Webhooks -> Add New Webhook to Workspace, scoped to one channel).
    slack_webhook_url: str = ""

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
