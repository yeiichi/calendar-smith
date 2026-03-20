# src/calendar_smith/core.py
from datetime import date, timedelta
from typing import NamedTuple, List


class WeekSpan(NamedTuple):
    """ISO week span with week number, start date, and end date."""
    number: int
    start: date
    end: date


class DateRange(NamedTuple):
    """Simple date range with start and end dates."""
    start: date
    end: date


def get_fiscal_year(date_obj: date, system: str = "us") -> int:
    """Return the fiscal year for a date.

    Supported systems:
        - ``us``: fiscal year starts Oct 1
        - ``jp``: fiscal year starts Apr 1
    """
    if system == "us":
        return date_obj.year + 1 if date_obj.month >= 10 else date_obj.year
    elif system == "jp":
        return date_obj.year if date_obj.month >= 4 else date_obj.year - 1
    raise ValueError(f"Unsupported fiscal system: {system}")


def get_iso_week_span(iso_year: int, iso_week: int) -> WeekSpan:
    """Return the Monday-to-Sunday span for an ISO week."""
    iso_week_monday = 1
    iso_week_sunday = 7

    week_start = date.fromisocalendar(iso_year, iso_week, iso_week_monday)
    week_end = date.fromisocalendar(iso_year, iso_week, iso_week_sunday)
    return WeekSpan(number=iso_week, start=week_start, end=week_end)


def get_iso_weeks_for_year(year: int) -> List[WeekSpan]:
    """Return all ISO week spans for a given year."""
    max_week = date(year, 12, 28).isocalendar().week
    return [get_iso_week_span(year, w) for w in range(1, max_week + 1)]


def get_nth_week_of_month(date_obj: date) -> int:
    """Return the 1-based week number within the month."""
    first_day = date_obj.replace(day=1)
    dom = date_obj.day
    adjusted_dom = dom + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1


def get_dates_windows(date_obj: date, window_size: int, repeats: int) -> list[DateRange]:
    """Return consecutive non-overlapping date windows."""
    windows: List[DateRange] = []
    current_start = date_obj
    for _ in range(repeats):
        current_end = current_start + timedelta(days=window_size - 1)
        windows.append(DateRange(current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return windows
