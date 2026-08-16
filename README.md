# JWI Drive Intelligence API

V1 scans the JWI `Clients` folder, enters each client's `01. Working` folder, identifies project folders, and reports projects that contain files modified within a selected period.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

The `/projects/recent` endpoint expects a Google OAuth access token:

```bash
curl -H "Authorization: Bearer GOOGLE_ACCESS_TOKEN" \
  "http://127.0.0.1:8000/projects/recent?days=45&client=Epson"
```

## Deploy to Google Cloud Run

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
gcloud run deploy jwi-drive-intelligence \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

`--allow-unauthenticated` allows ChatGPT to reach the service. The API still requires the Google OAuth Bearer token on project endpoints.

## Current limitations

- V1 detects project activity from recently modified files.
- It does not yet extract document text or determine meaningful strategic changes.
- The next phase adds `/projects/{project_id}/updates` and document extraction.

## Vendor approval automation (monday.com)

Automates the vendor intake -> approval -> onboarding pipeline on the JWI
**Vendor** board (workspace: CRM, board id `5100825568`), which has four
groups: **New Submission**, **Under Review**, **Approved Vendor** (formerly
"Active Vendors"), **Archived**.

**Flow**

1. The website form `POST`s to `/vendors/submit`. The vendor is created as
   an item in **New Submission** (item name = contact name; company name,
   email, phone, address, service category, and tax ID go into columns).
2. An AI completeness check runs against the submission (a deterministic
   required-field check, optionally augmented by a Claude call if
   `ANTHROPIC_API_KEY`/`ANTHROPIC_MODEL` are set — it also catches
   placeholder junk like "N/A" or "TBD" in required fields).
   - **Complete:** the item moves to **Under Review**, gets an approval
     deadline (`APPROVAL_DEADLINE_BUSINESS_DAYS`, default 5 business
     days), and ops/management are notified in Slack.
   - **Incomplete:** the vendor gets an email listing exactly what's
     missing, and the item stays in **New Submission**.
3. Ops/management approve or reject by setting the item's **Approval
   Status** column (Pending Review / Approved / Rejected). Two native
   monday.com board automations — not this service — then move the item:
   - *When Approval Status changes to Approved* -> move to **Approved Vendor**
   - *When Approval Status changes to Rejected* -> move to **Archived**
4. A daily job hits `POST /cron/vendor-deadlines`, which scans **Under
   Review** for anything past its deadline and Slack-reminds ops/management
   (tracked via a "Last Reminder Sent" column so it won't repeat same-day).

There's also a pre-existing automation on the board that creates a Vendor
item straight into **Approved Vendor** whenever a contact's Type is set to
"Vendor" on the Contacts board — a separate, older intake path from the
CRM's Contacts sync that this automation doesn't touch.

**One-time setup**

The board, groups, columns, and the two approve/reject automations are
already provisioned (IDs default in `app/config.py`). What's still needed
to actually run the service:

1. Create a monday.com API token (Admin > API) and set `MONDAY_API_TOKEN`.
2. Create a Slack bot with `chat:write` scope, invite it to the ops
   channel, and set `SLACK_BOT_TOKEN` / `SLACK_CHANNEL_OPS`.
3. Set SMTP creds (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`,
   `SMTP_PASSWORD`, `EMAIL_FROM`) for the vendor follow-up email.
4. Schedule `POST /cron/vendor-deadlines` daily (e.g. Cloud Scheduler)
   with header `X-Cron-Secret: <CRON_SECRET>`.

`scripts/setup_monday_board.py` is only needed if you're standing up a
*different* board from scratch — see the script's docstring.

**Tests**

```bash
pip install -r requirements-dev.txt
pytest
```
