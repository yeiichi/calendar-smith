# src/calendar_smith/core.py
from datetime import date, timedelta
from typing import NamedTuple, List


class WeekSpan(NamedTuple):
    """Represents a date range for a specific ISO week."""
    number: int
    start: date
    end: date


class DateRange(NamedTuple):
    """Represents a date range."""
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


def get_iso_week_span(iso_year: int, iso_week: int) -> WeekSpan:
    """Return the Monday-to-Sunday date span for an ISO week."""
    iso_week_monday = 1
    iso_week_sunday = 7

    week_start = date.fromisocalendar(iso_year, iso_week, iso_week_monday)
    week_end = date.fromisocalendar(iso_year, iso_week, iso_week_sunday)
    return WeekSpan(number=iso_week, start=week_start, end=week_end)


def get_iso_weeks_for_year(year: int) -> List[WeekSpan]:
    """
    Gets the ISO week spans for a specified year.

    This function calculates all ISO weeks that fall within the specified year
    and generates their corresponding WeekSpan representations.

    Parameters:
    year: int
        The year for which ISO weeks are to be calculated. Must be a valid integer
        within the range of acceptable years for the datetime module.

    Returns:
    List[WeekSpan]
        A list containing WeekSpan objects for each ISO week of the specified year.
    """
    max_week = date(year, 12, 28).isocalendar().week
    return [get_iso_week_span(year, w) for w in range(1, max_week + 1)]


def get_nth_week_of_month(date_obj: date) -> int:
    """
    Calculates the nth week of the month (1-indexed).
    Formula: (day_of_month + first_day_of_month_weekday - 1) // 7 + 1
    """
    first_day = date_obj.replace(day=1)
    dom = date_obj.day
    adjusted_dom = dom + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1


def get_dates_windows(date_obj: date, window_size: int, repeats: int) -> list[DateRange]:
    """
    Generate a list of date ranges (windows) based on a starting date, window size, and number of repeats.

    This function creates consecutive date ranges, known as windows, starting from the provided date
    with each window having the specified size. The function allows the creation of multiple non-overlapping
    windows by repeating the process the specified number of times. Each window range is represented
    as an instance of the DateRange object.

    Arguments:
        date_obj (date): The starting date of the first window.
        window_size (int): The number of days each window spans.
        repeats (int): The number of windows to generate.

    Returns:
        list[DateRange]: A list containing the generated DateRange objects.

    Raises:
        None
    """
    windows: List[DateRange] = []
    current_start = date_obj
    for _ in range(repeats):
        current_end = current_start + timedelta(days=window_size - 1)
        windows.append(DateRange(current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return windows
