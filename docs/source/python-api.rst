Python API
==========

**Calendar-Smith** provides a clean and simple Python API for integrating calendar-related math into your own scripts, applications, and data-processing pipelines.

Use the Python API when you want to:

- Call calendar logic directly from Python code
- Reuse date-parsing or fiscal-year-calculation logic programmatically
- Build repeatable pipelines without shell commands
- Integrate timezone conversion or window generation in application code

---

Typical import style
--------------------

Import directly from the top-level package whenever possible:

.. code-block:: python

   from calendar_smith import get_fiscal_year, now_jst

   # Calculate Japanese fiscal year
   fy = get_fiscal_year("2026-04-22", system="jp")

   # Get current time in JST
   current_time = now_jst()

---

Overview
--------

The Python API complements the command-line interface (CLI).

- Use the CLI for one-off tasks and shell workflows.
- Use the Python API when you need direct integration in Python code.

For detailed module reference, see :doc:`api`.

---

Key modules
-----------

- ``calendar_smith.core``: Core logic for fiscal years, ISO weeks, and date windows.
- ``calendar_smith.time``: Timezone utilities and ISO 8601 helpers.
- ``calendar_smith.utils``: General helpers for date parsing and ordinal formatting.

---

Example: Processing a list of dates
-----------------------------------

.. code-block:: python

   from calendar_smith import get_fiscal_year, ensure_date

   raw_dates = ["2026-03-31", "2026-04-01", "2026-04-22"]
   
   # Safely parse and calculate fiscal year for each date
   results = []
   for d in raw_dates:
       date_obj = ensure_date(d)
       fy = get_fiscal_year(date_obj, system="jp")
       results.append((date_obj, fy))

   print(results)

---

Next steps
----------

- For the full module reference, see :doc:`api`.
- For common patterns, see :doc:`recipes`.
- For command-oriented usage, see :doc:`cli`.
