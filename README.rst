==============
calendar-smith
==============

.. image:: https://img.shields.io/pypi/v/calendar-smith.svg
    :target: https://pypi.org/project/calendar-smith/
    :alt: PyPI Version

**Calendar-Smith** is a zero-dependency, high-performance Python utility for fiscal year calculations, ISO week mapping, and safe date parsing.

It was built for data engineers and analysts who need to process CSVs or perform calendar math without the overhead of heavy libraries like Pandas or Arrow.

Key Features
============

* **Safety-First Parsing**: Strictly rejects ambiguous 6-digit (``460614``) and 7-digit (``2026123``) strings to prevent century errors and data corruption.
* **Fiscal Logic**: Built-in support for US (fiscal year ends Sep 30) and Japanese (fiscal year ends Mar 31) fiscal systems.
* **Fast-Path Execution**: Utilizes ``datetime.fromisoformat`` for high-performance processing of standard data.
* **Timezone Utilities**: Lightweight helpers for UTC, JST, ET, and other common timezones with ISO 8601 support.
* **Ordinal Formatting**: Human-friendly outputs (e.g., "1st week", "3rd week").
* **Zero External Dependencies**: Uses only the Python Standard Library (3.10+).

Installation
============

.. code-block:: bash

    pip install calendar-smith

To contribute or run tests:

.. code-block:: bash

    git clone https://github.com/yeiichi/calendar-smith.git
    cd calendar-smith
    pip install -e ".[dev]"
    pytest

CLI Commands
============

1. ``calendar-smith-csv``
-------------------------
Appends a ``fiscal_year`` column to an existing CSV file. Supports:

* ``us``: fiscal year ends Sep 30
* ``jp``: fiscal year ends Mar 31

.. code-block:: bash

    calendar-smith-csv records.csv records_with_fy.csv --system jp --date-column created_at

2. ``calendar-smith-solve``
---------------------------
Lists the Monday-to-Sunday date ranges for every ISO week in a given year.

.. code-block:: bash

    calendar-smith-solve 2026

3. ``calendar-smith-nth``
-------------------------
Interactive tool to find the ordinal week of the month and the ISO week of the year for any date.

.. code-block:: bash

    $ calendar-smith-nth
    Date? [yyyy-mm-dd] (leave blank for today) >> 2026-02-17

    Result:
      Date:       2026-02-17 (Tuesday)
      Month Week: The 3rd week
      Year Week:  The 8th week

4. ``calendar-smith-week-span``
-------------------------------
Show the Monday-to-Sunday span for a specific ISO week.

.. code-block:: bash

    calendar-smith-week-span 2020 53

5. ``calendar-smith-windows``
-----------------------------
Generate consecutive date windows from a starting date using a fixed window size and repeat count.

.. code-block:: bash

    calendar-smith-windows 2026-03-17 7 4

Example output:

.. code-block:: text

    Generated 4 windows starting from 2026-03-17 with size 7:
      Window  1: 2026-03-17 to 2026-03-23
      Window  2: 2026-03-24 to 2026-03-30
      Window  3: 2026-03-31 to 2026-04-06
      Window  4: 2026-04-07 to 2026-04-13

6. ``calendar-smith-tz``
-----------------------
Convert an ISO 8601 datetime string from one timezone to another.

.. code-block:: bash

    calendar-smith-tz 2026-03-20T10:00:00+09:00 America/New_York
    # Output: 2026-03-19T21:00:00-04:00

Date Parsing Rules
==================

To ensure data integrity, **calendar-smith** follows these parsing rules:

* **Accepted**: ``2026-02-17``, ``2026/02/17``, ``2026.02.17``, ``2026-2-17``, ``20260217``.
* **Rejected**: 
    * ``260217`` (6-digit): Rejected to avoid century ambiguity (1926 vs 2026).
    * ``2026123`` (7-digit): Rejected because it could be Jan 23rd or Dec 3rd.

API Example
===========

.. code-block:: python

    from calendar_smith import (
        get_fiscal_year,
        to_date,
        get_nth_week_of_month,
        get_dates_windows,
        get_iso_week_span,
        get_iso_weeks_for_year,
        format_ordinal,
        WeekSpan,
    )

    # Parse a messy but valid string
    d = to_date("2026/4/1")

    # Get Japanese Fiscal Year (2026)
    fy_jp = get_fiscal_year(d, system="jp")

    # Get US Fiscal Year (2026 - fiscal year ends Sep 30, 2026)
    fy_us = get_fiscal_year(d, system="us")

    # Get week of month
    week_num = get_nth_week_of_month(d)

    # Get a specific ISO week span
    span = get_iso_week_span(2026, 1)

    # Get all ISO week spans for a year
    all_weeks = get_iso_weeks_for_year(2026)

    # Generate the next 4 date windows
    future_windows = get_dates_windows(d, window_size=7, repeats=4)

    from calendar_smith import (
        now_utc,
        now_jst,
        to_timezone,
        to_iso,
        from_iso,
        JST,
        ET,
    )

    # Get current time in JST
    dt_jst = now_jst()

    # Convert to New York time (ET)
    dt_et = to_timezone(dt_jst, ET)

    # Get ISO 8601 string
    iso_str = to_iso(dt_et)

    # Parse ISO 8601 string
    dt_parsed = from_iso("2026-03-20T10:00:00+09:00")

License
=======

MIT License. See ``LICENSE`` for details.
