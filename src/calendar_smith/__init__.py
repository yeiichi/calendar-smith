# src/calendar_smith/__init__.py

"""
Calendar-Smith: Lightweight fiscal and ISO calendar utilities.
"""

from .core import (
    get_fiscal_year,
    get_iso_weeks_for_year,
    get_nth_week_of_month,
    get_dates_windows,
    WeekSpan,
)
from .utils import (
    to_date,
    format_ordinal,
)

__version__ = "0.2.2"

# Defining __all__ ensures that 'from calendar_smith import *' 
# only exports the intended public API.
__all__ = [
    "get_fiscal_year",
    "get_iso_weeks_for_year",
    "get_nth_week_of_month",
    "get_dates_windows",
    "WeekSpan",
    "to_date",
    "format_ordinal",
]