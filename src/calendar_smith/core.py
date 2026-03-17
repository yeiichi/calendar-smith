# src/calendar_smith/core.py
from datetime import date, timedelta
from typing import NamedTuple, List, Tuple


class WeekSpan(NamedTuple):
    """Represents a date range for a specific ISO week."""
    number: int
    start: date
    end: date


def get_fiscal_year(date_obj: date, system: str = "us") -> int:
    """
    Calculates the fiscal year for a given date.
    :param date_obj: The date to evaluate.
    :param system: 'us' (starts Oct 1) or 'jp' (starts Apr 1).
    :return: The integer fiscal year.
    """
    if system == "us":
        return date_obj.year + 1 if date_obj.month >= 10 else date_obj.year
    elif system == "jp":
        return date_obj.year if date_obj.month >= 4 else date_obj.year - 1
    raise ValueError(f"Unsupported fiscal system: {system}")


def get_iso_weeks_for_year(year: int) -> List[WeekSpan]:
    """Generates all ISO weeks for a given year using standard library."""
    max_week = date(year, 12, 28).isocalendar().week
    return [
        WeekSpan(
            number=w,
            start=date.fromisocalendar(year, w, 1),
            end=date.fromisocalendar(year, w, 7)
        ) for w in range(1, max_week + 1)
    ]


def get_nth_week_of_month(date_obj: date) -> int:
    """
    Calculates the nth week of the month (1-indexed).
    Formula: (day_of_month + first_day_of_month_weekday - 1) // 7 + 1
    """
    first_day = date_obj.replace(day=1)
    dom = date_obj.day
    adjusted_dom = dom + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1


def get_dates_windows(date_obj: date, window_size: int, repeats: int) -> List[Tuple[date, date]]:
    """
    Generates a list of (start_date, end_date) tuples representing each window.

    This function calculates a series of future date ranges (windows) based on a given
    starting date, a specified window size, and the number of times the calculation
    should repeat. Each window starts immediately after the previous one ends.

    Parameters:
    date_obj: date
        The starting date of the first window.
    window_size: int
        The time interval, in days, for each window.
    repeats: int
        The number of future windows to generate.

    Returns:
    List[Tuple[date, date]]
        A list of tuples, each containing the (start_date, end_date) for a window.
    """
    windows = []
    current_start = date_obj
    for _ in range(repeats):
        current_end = current_start + timedelta(days=window_size - 1)
        windows.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return windows
