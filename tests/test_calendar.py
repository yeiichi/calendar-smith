import io
from datetime import date
from unittest.mock import patch

import pytest

from calendar_smith.cli import generate_windows, solve_week_span
from calendar_smith.core import (
    get_fiscal_year,
    get_iso_weeks_for_year,
    get_iso_week_span,
    get_nth_week_of_month,
    get_dates_windows,
    DateRange
)
from calendar_smith.utils import to_date, format_ordinal


# --- Core Logic Tests ---

@pytest.mark.parametrize("input_date, system, expected", [
    (date(2023, 10, 1), "us", 2024),  # US FY starts Oct 1
    (date(2023, 9, 30), "us", 2023),
    (date(2024, 4, 1), "jp", 2024),  # JP FY starts Apr 1
    (date(2024, 3, 31), "jp", 2023),
])
def test_fiscal_year_logic(input_date, system, expected):
    """Verify US and Japanese fiscal year boundary logic."""
    assert get_fiscal_year(input_date, system) == expected


def test_iso_weeks_generation():
    """Verify that we generate the correct number of ISO weeks for a year."""
    weeks = get_iso_weeks_for_year(2024)  # 2024 has 52 weeks
    assert len(weeks) == 52
    assert weeks[0].number == 1
    assert weeks[0].start == date(2024, 1, 1)
    assert weeks[-1].end == date(2024, 12, 29)


def test_get_iso_week_span():
    """Verify ISO week spans map to Monday-to-Sunday date ranges."""
    span = get_iso_week_span(2024, 1)
    assert span.number == 1
    assert span.start == date(2024, 1, 1)
    assert span.end == date(2024, 1, 7)


def test_get_iso_week_span_year_boundary():
    """Verify ISO weeks that cross a year boundary are handled correctly."""
    span = get_iso_week_span(2020, 53)
    assert span.number == 53
    assert span.start == date(2020, 12, 28)
    assert span.end == date(2021, 1, 3)


@pytest.mark.parametrize("test_date, expected_nth", [
    (date(2024, 1, 1), 1),  # Mon, Jan 1st
    (date(2024, 1, 7), 1),  # Sun, Jan 7th
    (date(2024, 1, 8), 2),  # Mon, Jan 8th
    (date(2024, 2, 29), 5),  # Leap year end of month
])
def test_nth_week_logic(test_date, expected_nth):
    """Verify the mathematical calculation of the week of the month."""
    assert get_nth_week_of_month(test_date) == expected_nth


def test_get_dates_windows():
    """Verify sequence of future window ranges incremented by window size."""
    start_date = date(2024, 1, 1)
    window_size = 7
    repeats = 3
    # Window 1: 1-7, Window 2: 8-14, Window 3: 15-21
    expected = [
        DateRange(date(2024, 1, 1), date(2024, 1, 7)),
        DateRange(date(2024, 1, 8), date(2024, 1, 14)),
        DateRange(date(2024, 1, 15), date(2024, 1, 21))
    ]
    assert get_dates_windows(start_date, window_size, repeats) == expected


def test_get_dates_windows_sampling_rate():
    """Verify window generation when sampling rate is different from window size."""
    start_date = date(2024, 1, 1)
    window_size = 3
    repeats = 3
    sampling_rate = 1
    # Overlapping windows
    # Window 1: 1-3, Window 2: 2-4, Window 3: 3-5
    expected = [
        DateRange(date(2024, 1, 1), date(2024, 1, 3)),
        DateRange(date(2024, 1, 2), date(2024, 1, 4)),
        DateRange(date(2024, 1, 3), date(2024, 1, 5))
    ]
    assert get_dates_windows(start_date, window_size, repeats, sampling_rate) == expected


def test_get_dates_windows_gaps():
    """Verify window generation with gaps (sampling_rate > window_size)."""
    start_date = date(2024, 1, 1)
    window_size = 2
    repeats = 2
    sampling_rate = 5
    # Gapped windows
    # Window 1: 1-2, Window 2: 6-7
    expected = [
        DateRange(date(2024, 1, 1), date(2024, 1, 2)),
        DateRange(date(2024, 1, 6), date(2024, 1, 7))
    ]
    assert get_dates_windows(start_date, window_size, repeats, sampling_rate) == expected


# --- Utility & Parser Tests ---

@pytest.mark.parametrize("valid_input, expected", [
    ("2026-02-17", date(2026, 2, 17)),  # Strict ISO
    ("2026-2-17", date(2026, 2, 17)),  # Unpadded ISO
    ("20260217", date(2026, 2, 17)),  # 8-digit padded
    ("2026/02/17", date(2026, 2, 17)),  # Slashes
    ("2026.02.17", date(2026, 2, 17)),  # Dots
    ("2026-02-17T14:00", date(2026, 2, 17)),  # ISO with Time component
    (None, date.today()),  # Fallback to today
])
def test_valid_date_parsing(valid_input, expected):
    """Test the 'Fast Path' and 'Safe Path' parsing."""
    assert to_date(valid_input) == expected


@pytest.mark.parametrize("invalid_input", [
    "460614",  # 6-digit shorthand rejected to prevent century ambiguity
    "2026123",  # 7-digit ambiguous string rejected
    "2026-13-01",  # Invalid month
    "not-a-date"
])
def test_date_rejections(invalid_input):
    """Ensure ambiguous or incorrect formats raise a ValueError."""
    with pytest.raises(ValueError):
        to_date(invalid_input)


@pytest.mark.parametrize("num, expected", [
    (1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"),
    (11, "11th"), (12, "12th"), (13, "13th"),  # Special cases
    (21, "21st"), (22, "22nd"), (23, "23rd")
])
def test_ordinal_formatting(num, expected):
    """Verify text representation of numbers (1st, 2nd, etc)."""
    assert format_ordinal(num) == expected


# --- CLI Tests ---

def test_generate_windows_cli():
    """Verify the CLI output for generate_windows."""
    test_args = ["calendar-smith-windows", "2026-03-17", "7", "2"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            generate_windows()
            output = fake_out.getvalue()
            assert "Generated 2 windows" in output
            assert "Window  1: 2026-03-17 to 2026-03-23" in output
            assert "Window  2: 2026-03-24 to 2026-03-30" in output


def test_generate_windows_sampling_cli():
    """Verify the CLI output for generate_windows with sampling_rate."""
    test_args = ["calendar-smith-windows", "2026-03-17", "7", "2", "--sampling-rate", "1"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            generate_windows()
            output = fake_out.getvalue()
            assert "Generated 2 windows" in output
            assert "(Sampling rate: 1 days)" in output
            assert "Window  1: 2026-03-17 to 2026-03-23" in output
            assert "Window  2: 2026-03-18 to 2026-03-24" in output


def test_solve_week_span_cli():
    """Verify the CLI output for ISO week span lookup."""
    test_args = ["calendar-smith-week-span", "2020", "53"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            solve_week_span()
            output = fake_out.getvalue()
            assert "ISO Week 53 in 2020" in output
            assert "Start: 2020-12-28" in output
            assert "End:   2021-01-03" in output
