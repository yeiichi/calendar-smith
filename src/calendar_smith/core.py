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


def get_dates_windows(
        start_date: date,
        window_size: int,
        repeats: int,
        sampling_rate: int | None = None,
) -> list[DateRange]:
    """
    Return date windows based on a sampling rate.

    Args:
        start_date: The starting date of the first window.
        window_size: The duration of each window in days.
        repeats: Number of windows to generate.
        sampling_rate: The number of days between the start of each window.
            Defaults to window_size, which produces consecutive non-overlapping windows.
    """
    if window_size < 1:
        raise ValueError("window_size must be at least 1 day.")
    if repeats < 0:
        raise ValueError("repeats cannot be negative.")

    sampling_rate = window_size if sampling_rate is None else sampling_rate
    if sampling_rate < 1:
        raise ValueError("sampling_rate must be at least 1 day to progress forward.")

    window_end_offset = timedelta(days=window_size - 1)

    return [
        DateRange(
            start_date + timedelta(days=index * sampling_rate),
            start_date + timedelta(days=index * sampling_rate) + window_end_offset,
        )
        for index in range(repeats)
    ]
