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

4. ``calendar-smith-windows``
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

    from calendar_smith import get_fiscal_year, to_date, get_nth_week_of_month, get_dates_windows

    # Parse a messy but valid string
    d = to_date("2026/4/1")

    # Get Japanese Fiscal Year (2026)
    fy_jp = get_fiscal_year(d, system="jp")

    # Get US Fiscal Year (2026 - fiscal year ends Sep 30, 2026)
    fy_us = get_fiscal_year(d, system="us")

    # Get week of month
    week_num = get_nth_week_of_month(d)

    # Generate the next 4 date windows
    future_windows = get_dates_windows(d, window_size=7, repeats=4)

License
=======

MIT License. See ``LICENSE`` for details.
