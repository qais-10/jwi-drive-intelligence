from datetime import date

from app.vendors.business_days import add_business_days, is_past_deadline


def test_add_business_days_skips_weekend():
    # Friday 2026-08-14 + 5 business days -> Friday 2026-08-21
    start = date(2026, 8, 14)
    assert add_business_days(start, 5) == date(2026, 8, 21)


def test_add_business_days_from_weekend_start():
    # Saturday + 1 business day -> Monday
    start = date(2026, 8, 15)
    assert add_business_days(start, 1) == date(2026, 8, 17)


def test_add_business_days_zero_returns_start():
    start = date(2026, 8, 17)
    assert add_business_days(start, 0) == start


def test_add_business_days_rejects_negative():
    try:
        add_business_days(date(2026, 8, 17), -1)
    except ValueError:
        return
    raise AssertionError("expected ValueError for negative business_days")


def test_is_past_deadline():
    deadline = date(2026, 8, 14)
    assert is_past_deadline(deadline, today=date(2026, 8, 15)) is True
    assert is_past_deadline(deadline, today=date(2026, 8, 14)) is False
    assert is_past_deadline(deadline, today=date(2026, 8, 13)) is False
