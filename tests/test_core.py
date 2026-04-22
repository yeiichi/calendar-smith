from datetime import date
import pytest
from calendar_smith.core import (
    get_fiscal_year,
    get_iso_week_span,
    get_iso_weeks_for_year,
    get_nth_week_of_month,
    get_dates_windows,
    WeekSpan,
    DateRange
)

def test_get_fiscal_year_us():
    assert get_fiscal_year(date(2023, 9, 30), system="us") == 2023
    assert get_fiscal_year(date(2023, 10, 1), system="us") == 2024
    assert get_fiscal_year(date(2024, 1, 1), system="us") == 2024

def test_get_fiscal_year_jp():
    assert get_fiscal_year(date(2023, 3, 31), system="jp") == 2022
    assert get_fiscal_year(date(2023, 4, 1), system="jp") == 2023
    assert get_fiscal_year(date(2024, 1, 1), system="jp") == 2023

def test_get_fiscal_year_invalid():
    with pytest.raises(ValueError, match="Unsupported fiscal system: uk"):
        get_fiscal_year(date(2023, 1, 1), system="uk")

def test_get_iso_week_span():
    span = get_iso_week_span(2020, 53)
    assert span.number == 53
    assert span.start == date(2020, 12, 28)
    assert span.end == date(2021, 1, 3)

def test_get_iso_weeks_for_year():
    weeks_2020 = get_iso_weeks_for_year(2020)
    assert len(weeks_2020) == 53
    assert weeks_2020[0].number == 1
    assert weeks_2020[-1].number == 53

    weeks_2021 = get_iso_weeks_for_year(2021)
    assert len(weeks_2021) == 52

def test_get_nth_week_of_month():
    # 2024-04-01 is Monday
    assert get_nth_week_of_month(date(2024, 4, 1)) == 1
    # 2024-04-07 is Sunday
    assert get_nth_week_of_month(date(2024, 4, 7)) == 1
    # 2024-04-08 is Monday
    assert get_nth_week_of_month(date(2024, 4, 8)) == 2
    
    # 2024-05-01 is Wednesday. 
    # Mon=0, Tue=1, Wed=2. 
    # first_day.weekday() = 2.
    # adjusted_dom = 1 + 2 = 3.
    # (3 - 1) // 7 + 1 = 1.
    assert get_nth_week_of_month(date(2024, 5, 1)) == 1
    # 2024-05-05 is Sunday.
    # adjusted_dom = 5 + 2 = 7.
    # (7 - 1) // 7 + 1 = 1.
    assert get_nth_week_of_month(date(2024, 5, 5)) == 1
    # 2024-05-06 is Monday.
    # adjusted_dom = 6 + 2 = 8.
    # (8 - 1) // 7 + 1 = 2.
    assert get_nth_week_of_month(date(2024, 5, 6)) == 2

def test_get_dates_windows_basic():
    windows = get_dates_windows(date(2024, 1, 1), 7, 2)
    assert len(windows) == 2
    assert windows[0] == DateRange(date(2024, 1, 1), date(2024, 1, 7))
    assert windows[1] == DateRange(date(2024, 1, 8), date(2024, 1, 14))

def test_get_dates_windows_sampling():
    windows = get_dates_windows(date(2024, 1, 1), 7, 2, sampling_rate=14)
    assert len(windows) == 2
    assert windows[0] == DateRange(date(2024, 1, 1), date(2024, 1, 7))
    assert windows[1] == DateRange(date(2024, 1, 15), date(2024, 1, 21))

def test_get_dates_windows_overlapping():
    windows = get_dates_windows(date(2024, 1, 1), 7, 2, sampling_rate=3)
    assert len(windows) == 2
    assert windows[0] == DateRange(date(2024, 1, 1), date(2024, 1, 7))
    assert windows[1] == DateRange(date(2024, 1, 4), date(2024, 1, 10))

def test_get_dates_windows_errors():
    with pytest.raises(ValueError, match="window_size must be at least 1 day."):
        get_dates_windows(date(2024, 1, 1), 0, 1)
    with pytest.raises(ValueError, match="repeats cannot be negative."):
        get_dates_windows(date(2024, 1, 1), 7, -1)
    with pytest.raises(ValueError, match="sampling_rate must be at least 1 day to progress forward."):
        get_dates_windows(date(2024, 1, 1), 7, 2, sampling_rate=0)
