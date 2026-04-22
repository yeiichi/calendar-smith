Recipes
=======

Common patterns and use cases for **Calendar-Smith**.

---

Working with Japanese fiscal years
----------------------------------

Many organizations in Japan use a fiscal year starting April 1.

.. code-block:: python

   from calendar_smith import get_fiscal_year

   # Date in the current fiscal year (FY2026)
   date_str = "2026-04-22"
   fy = get_fiscal_year(date_str, system="jp")
   # Result: 2026

   # Date in the previous fiscal year (FY2025)
   date_str = "2026-03-31"
   fy = get_fiscal_year(date_str, system="jp")
   # Result: 2025

---

Generating weekly windows for analysis
--------------------------------------

If you need to analyze data in 7-day windows starting from a specific date:

.. code-block:: python

   from calendar_smith import get_dates_windows

   # Start date, window size (7 days), count (4 windows)
   windows = get_dates_windows("2026-03-17", 7, 4)

   for start, end in windows:
       print(f"Window: {start} to {end}")

---

Handling timezones safely
-------------------------

Convert UTC to JST or other timezones without external libraries:

.. code-block:: python

   from calendar_smith import now_utc, to_timezone, JST

   # Current time in UTC
   utc_time = now_utc()

   # Convert to JST
   jst_time = to_timezone(utc_time, JST)

   print(f"UTC: {utc_time.isoformat()}")
   print(f"JST: {jst_time.isoformat()}")

---

Safe date parsing from CSV strings
----------------------------------

When reading from CSV, you often get string dates in various formats. ``ensure_date`` helps normalize them while rejecting ambiguous ones.

.. code-block:: python

   from calendar_smith import ensure_date

   # Standard ISO 8601
   d1 = ensure_date("2026-04-22")

   # Compressed format (YYYYMMDD)
   d2 = ensure_date("20260422")

   # Ambiguous formats like "260422" are strictly REJECTED to prevent errors.
   try:
       ensure_date("260422")
   except ValueError as e:
       print(f"Error: {e}")
