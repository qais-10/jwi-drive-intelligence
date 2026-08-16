from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import httpx

from ..config import settings
from .constants import JUNK_VALUES, resolve_required_fields

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


@dataclass
class AgentDecision:
    complete: bool
    missing_fields: list[str] = field(default_factory=list)
    notes: str = ""


def _is_blank_or_junk(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    if not text:
        return True
    return text.casefold() in JUNK_VALUES


def _rule_based_check(fields: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [name for name in required_fields if _is_blank_or_junk(fields.get(name))]


async def _ai_review(
    fields: dict[str, Any],
    required_fields: list[str],
) -> tuple[list[str], str]:
    prompt = (
        "You are reviewing a new vendor intake submission for completeness.\n"
        f"Required fields: {', '.join(required_fields)}.\n"
        f"Submission (JSON): {json.dumps(fields)}\n\n"
        "Flag any required field that is technically filled in but is "
        "meaningless, a placeholder, or clearly invalid (gibberish, an "
        "email without a real domain, a phone number with the wrong "
        "number of digits, contradictory information, etc.).\n"
        "Respond with ONLY a JSON object of this exact shape, no other text:\n"
        '{"missing_or_invalid": ["field_name", ...], "notes": "one short sentence"}'
    )

    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": settings.anthropic_model,
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(ANTHROPIC_API_URL, headers=headers, json=body)

    response.raise_for_status()
    payload = response.json()
    text = payload["content"][0]["text"]
    parsed = json.loads(text)
    return parsed.get("missing_or_invalid", []), parsed.get("notes", "")


async def review_submission(
    fields: dict[str, Any],
    required_fields: list[str] | None = None,
) -> AgentDecision:
    required = required_fields or resolve_required_fields()
    missing = set(_rule_based_check(fields, required))
    notes = ""

    if settings.anthropic_api_key and settings.anthropic_model:
        try:
            ai_missing, ai_notes = await _ai_review(fields, required)
            missing.update(name for name in ai_missing if name in required)
            notes = ai_notes
        except Exception:
            # AI review is a best-effort enhancement on top of the
            # deterministic check above; never let an API hiccup block a
            # vendor's submission from being processed.
            notes = "AI review unavailable; used the rule-based completeness check only."

    ordered_missing = [name for name in required if name in missing]
    return AgentDecision(
        complete=not ordered_missing,
        missing_fields=ordered_missing,
        notes=notes,
    )
