import io
import sys
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from unittest.mock import patch
import pytest

from calendar_smith.time import (
    JST, ET, UTC_TZ, 
    now_utc, now_jst, 
    to_timezone, to_iso, from_iso, tz
)
from calendar_smith.cli import convert_timezone

# --- Logic Tests ---

def test_timezone_constants():
    """Verify that predefined timezone constants are correct."""
    assert JST == ZoneInfo("Asia/Tokyo")
    assert ET == ZoneInfo("America/New_York")
    assert UTC_TZ == UTC

def test_now_functions():
    """Verify that current time helpers return aware datetimes in the right zones."""
    dt_utc = now_utc()
    assert dt_utc.tzinfo == UTC
    
    dt_jst = now_jst()
    assert dt_jst.tzinfo == JST

def test_to_timezone_conversion():
    """Verify aware-to-aware conversion logic."""
    dt_jst = datetime(2026, 3, 20, 10, 0, tzinfo=JST)
    dt_et = to_timezone(dt_jst, ET)
    
    # JST (UTC+9) 10:00 -> ET (UTC-4 in March) is 21:00 previous day
    assert dt_et.hour == 21
    assert dt_et.day == 19
    assert dt_et.tzinfo == ET

def test_to_timezone_naive_fails():
    """Verify that naive datetimes are rejected by to_timezone."""
    naive_dt = datetime(2026, 3, 20, 10, 0)
    with pytest.raises(ValueError, match="Naive datetime is not allowed"):
        to_timezone(naive_dt, JST)

def test_iso_formatting_and_parsing():
    """Verify round-trip ISO 8601 formatting and parsing."""
    iso_str = "2026-03-20T10:00:00+09:00"
    dt = from_iso(iso_str)
    
    assert dt.tzinfo is not None
    assert to_iso(dt) == iso_str

def test_from_iso_naive_fails():
    """Verify that naive ISO strings are rejected."""
    with pytest.raises(ValueError, match="Naive datetime string is not allowed"):
        from_iso("2026-03-20T10:00:00")

def test_tz_helper():
    """Verify the tz helper returns the correct ZoneInfo."""
    assert tz("Europe/London") == ZoneInfo("Europe/London")

# --- CLI Tests ---

def test_convert_timezone_cli():
    """Verify the CLI output for timezone conversion."""
    test_args = ["calendar-smith-tz", "2026-03-20T10:00:00+09:00", "America/New_York"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            convert_timezone()
            output = fake_out.getvalue().strip()
            # JST 10:00 -> ET 21:00 (March 19)
            assert output == "2026-03-19T21:00:00-04:00"

def test_convert_timezone_cli_error():
    """Verify CLI error handling for invalid input."""
    test_args = ["calendar-smith-tz", "invalid-date", "America/New_York"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with pytest.raises(SystemExit) as excinfo:
                convert_timezone()
            assert excinfo.value.code == 1
            assert "Error:" in fake_out.getvalue()
