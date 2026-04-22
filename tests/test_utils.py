import datetime
import pytest
from calendar_smith.utils import format_ordinal, parse_date_lenient, ensure_date

def test_format_ordinal():
    assert format_ordinal(1) == "1st"
    assert format_ordinal(2) == "2nd"
    assert format_ordinal(3) == "3rd"
    assert format_ordinal(4) == "4th"
    assert format_ordinal(10) == "10th"
    assert format_ordinal(11) == "11th"
    assert format_ordinal(12) == "12th"
    assert format_ordinal(13) == "13th"
    assert format_ordinal(21) == "21st"
    assert format_ordinal(22) == "22nd"
    assert format_ordinal(23) == "23rd"
    assert format_ordinal(101) == "101st"
    assert format_ordinal(111) == "111th"

def test_parse_date_lenient_valid():
    assert parse_date_lenient("20240422") == datetime.date(2024, 4, 22)
    assert parse_date_lenient("2024-04-22") == datetime.date(2024, 4, 22)
    assert parse_date_lenient("2024/04/22") == datetime.date(2024, 4, 22)
    assert parse_date_lenient("2024.04.22") == datetime.date(2024, 4, 22)
    assert parse_date_lenient("2024-04-22T12:00:00") == datetime.date(2024, 4, 22)
    assert parse_date_lenient("2024-04-22 12:00:00") == datetime.date(2024, 4, 22)

def test_parse_date_lenient_invalid():
    with pytest.raises(ValueError, match="Ambiguous date '240422' rejected"):
        parse_date_lenient("240422")
    with pytest.raises(ValueError, match="Could not parse 'invalid'. Expected YYYY-MM-DD or YYYYMMDD."):
        parse_date_lenient("invalid")
    with pytest.raises(ValueError, match="Could not parse '2024-13-01'. Expected YYYY-MM-DD or YYYYMMDD."):
        parse_date_lenient("2024-13-01")

def test_ensure_date():
    # None returns today
    assert ensure_date(None) == datetime.date.today()
    
    # date object returns same
    d = datetime.date(2024, 4, 22)
    assert ensure_date(d) is d
    
    # string ISO format
    assert ensure_date("2024-04-22") == d
    
    # string lenient format
    assert ensure_date("20240422") == d
    
    # string with whitespace
    assert ensure_date("  2024-04-22  ") == d

def test_ensure_date_invalid():
    with pytest.raises(ValueError):
        ensure_date("not-a-date")
