from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

# ---- Public timezone constants ----
UTC_TZ = UTC

JST = ZoneInfo("Asia/Tokyo")
KST = ZoneInfo("Asia/Seoul")
CST_CN = ZoneInfo("Asia/Shanghai")
IST = ZoneInfo("Asia/Kolkata")
SGT = ZoneInfo("Asia/Singapore")

ET = ZoneInfo("America/New_York")
PT = ZoneInfo("America/Los_Angeles")

GMT = ZoneInfo("Europe/London")
CET = ZoneInfo("Europe/Paris")

__all__ = [
    "UTC_TZ",
    "JST",
    "KST",
    "CST_CN",
    "IST",
    "SGT",
    "ET",
    "PT",
    "GMT",
    "CET",
    "now_utc",
    "now_in",
    "now_jst",
    "now_et",
    "to_timezone",
    "to_iso",
    "from_iso",
    "tz",
]


def now_utc() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(UTC_TZ)


def now_in(timezone: ZoneInfo) -> datetime:
    """Return the current datetime in the given timezone."""
    return now_utc().astimezone(timezone)


def now_jst() -> datetime:
    """Return the current datetime in Asia/Tokyo."""
    return now_in(JST)


def now_et() -> datetime:
    """Return the current datetime in America/New_York."""
    return now_in(ET)


def to_timezone(dt: datetime, timezone: ZoneInfo) -> datetime:
    """Convert an aware datetime to another timezone.

    Raises:
        ValueError: If ``dt`` is naive.
    """
    if dt.tzinfo is None:
        raise ValueError("Naive datetime is not allowed")
    return dt.astimezone(timezone)


def to_iso(dt: datetime) -> str:
    """Return an ISO 8601 string for an aware datetime.

    Raises:
        ValueError: If ``dt`` is naive.
    """
    if dt.tzinfo is None:
        raise ValueError("Naive datetime is not allowed")
    return dt.isoformat()


def from_iso(value: str) -> datetime:
    """Parse an ISO 8601 string into an aware datetime.

    Raises:
        ValueError: If the parsed datetime is naive.
    """
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("Naive datetime string is not allowed")
    return dt


def tz(name: str) -> ZoneInfo:
    """Return a timezone from an IANA name.

    Example:
        tz("Australia/Sydney")
    """
    return ZoneInfo(name)
