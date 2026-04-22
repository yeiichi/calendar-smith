# src/calendar_smith/__init__.py

"""
Calendar-Smith: Lightweight fiscal and ISO calendar utilities.
"""

from .core import (
    get_fiscal_year,
    get_iso_weeks_for_year,
    get_iso_week_span,
    get_nth_week_of_month,
    get_dates_windows,
    WeekSpan,
    DateRange,
)
from .utils import (
    ensure_date,
    format_ordinal,
)

from .time import (
    UTC_TZ, JST, KST, CST_CN, IST, SGT, ET, PT, GMT, CET,
    now_utc, now_in, now_jst, now_et, to_timezone, to_iso, from_iso, tz
)
from .cli import main, fiscal_year

__version__ = "0.4.2"

# Defining __all__ ensures that 'from calendar_smith import *' 
# only exports the intended public API.
__all__ = [
    "get_fiscal_year",
    "get_iso_weeks_for_year",
    "get_iso_week_span",
    "get_nth_week_of_month",
    "get_dates_windows",
    "WeekSpan",
    "DateRange",
    "ensure_date",
    "format_ordinal",
    "UTC_TZ", "JST", "KST", "CST_CN", "IST", "SGT", "ET", "PT", "GMT", "CET",
    "now_utc", "now_in", "now_jst", "now_et", "to_timezone", "to_iso", "from_iso", "tz",
    "main", "fiscal_year",
]
