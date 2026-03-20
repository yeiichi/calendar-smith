# src/calendar_smith/utils.py
import datetime
import re

def format_ordinal(n: int) -> str:
    """Return ``n`` as an ordinal string, such as ``1st`` or ``22nd``."""
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

def super_date_parser(date_str: str) -> datetime.date:
    """Parse common date formats and reject ambiguous shorthand values."""
    date_part = date_str.split('T')[0].split(' ')[0]
    digits_only = re.sub(r'[^0-9]', '', date_part)

    if len(digits_only) == 8 and date_part.isdigit():
        return datetime.datetime.strptime(digits_only, "%Y%m%d").date()

    normalized = re.sub(r'[./]', '-', date_part)
    if '-' in normalized:
        try:
            return datetime.datetime.strptime(normalized, "%Y-%m-%d").date()
        except ValueError:
            pass

    if len(digits_only) in (6, 7):
        raise ValueError(
            f"Ambiguous date '{date_str}' rejected. "
            "Please use 8-digit YYYYMMDD or delimiters (YYYY-MM-DD)."
        )

    raise ValueError(f"Could not parse '{date_str}'. Expected YYYY-MM-DD or YYYYMMDD.")

def to_date(date_input: str | datetime.date | None) -> datetime.date:
    """Convert a string, date, or ``None`` into a ``datetime.date``."""
    if not date_input:
        return datetime.date.today()
    if isinstance(date_input, datetime.date):
        return date_input

    clean_input = str(date_input).strip()
    try:
        return datetime.date.fromisoformat(clean_input)
    except ValueError:
        return super_date_parser(clean_input)