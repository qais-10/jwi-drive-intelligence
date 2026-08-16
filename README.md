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

Automates the vendor intake -> approval -> onboarding pipeline on a
monday.com board with four groups: **New Submission**, **Under Review**,
**Approved Vendor**, **Archived**.

**Flow**

1. The website form `POST`s to `/vendors/submit`. The vendor is created as
   an item in **New Submission**.
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
   Status** column. monday.com calls our webhook (`/webhooks/monday`) on
   that change, which moves the item to **Approved Vendor** or
   **Archived** and posts a Slack update.
4. A daily job hits `POST /cron/vendor-deadlines`, which scans **Under
   Review** for anything past its deadline and Slack-reminds ops/management.

**One-time setup**

1. Create a monday.com API token (Admin > API) and set `MONDAY_API_TOKEN`.
2. Run the board provisioning script — it creates the board, the four
   groups, and all tracking columns, then prints the IDs to paste into `.env`:

   ```bash
   pip install -r requirements-dev.txt
   cp .env.example .env   # set MONDAY_API_TOKEN first
   python -m scripts.setup_monday_board "Vendor Approvals"
   ```

3. Register a monday.com webhook (Board > Integrations, or the
   `create_webhook` API mutation) pointing at
   `https://<your-deployment>/webhooks/monday?token=<MONDAY_WEBHOOK_SECRET>`
   for the "column value changed" event. monday.com sends a one-time
   `{"challenge": ...}` handshake that the endpoint echoes back automatically.
4. Create a Slack bot with `chat:write` scope, invite it to the ops
   channel, and set `SLACK_BOT_TOKEN` / `SLACK_CHANNEL_OPS`.
5. Set SMTP creds (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`,
   `SMTP_PASSWORD`, `EMAIL_FROM`) for the vendor follow-up email.
6. Schedule `POST /cron/vendor-deadlines` daily (e.g. Cloud Scheduler)
   with header `X-Cron-Secret: <CRON_SECRET>`.

**Tests**

```bash
pip install -r requirements-dev.txt
pytest
```
