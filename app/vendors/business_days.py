from __future__ import annotations

from datetime import date, timedelta


def add_business_days(start: date, business_days: int) -> date:
    """Return the date `business_days` weekdays after `start` (Sat/Sun skipped)."""
    if business_days < 0:
        raise ValueError("business_days must be non-negative")

    current = start
    remaining = business_days
    while remaining > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday=0 ... Sunday=6
            remaining -= 1
    return current


def is_past_deadline(deadline: date, *, today: date) -> bool:
    return today > deadline
