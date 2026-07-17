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
