Quickstart
==========

Get started with **Calendar-Smith** in minutes.

The project provides both a command-line interface (CLI) and a Python API.

---

Command-line usage
------------------

Find the fiscal year for a specific date (Japanese system):

.. code-block:: bash

   calendar-smith fiscal-year 2026-04-22 --system jp

Generate 4 consecutive 7-day windows starting from a date:

.. code-block:: bash

   calendar-smith windows 2026-03-17 7 4

Convert a timestamp to another timezone:

.. code-block:: bash

   calendar-smith tz 2026-03-20T10:00:00+09:00 America/New_York

---

Python API usage
----------------

Import common utilities from the top-level package:

.. code-block:: python

   from calendar_smith import get_fiscal_year, now_jst

   # Calculate Japanese fiscal year (starts April 1)
   fy = get_fiscal_year("2026-04-22", system="jp")
   print(f"Fiscal Year: {fy}")

   # Get current time in JST
   current_time = now_jst()
   print(f"JST Time: {current_time.isoformat()}")

---

Next steps
----------

- For more CLI commands, see :doc:`cli`.
- For common patterns, see :doc:`recipes`.
- For detailed module documentation, see :doc:`api`.
