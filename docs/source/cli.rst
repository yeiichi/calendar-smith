CLI Reference
=============

**Calendar-Smith** provides a powerful command-line interface (CLI) for everyday calendar-related tasks.

The main command is ``calendar-smith``, which includes multiple subcommands.
Additionally, several standalone scripts are provided for convenience.

Available commands
------------------

Top-level command
^^^^^^^^^^^^^^^^^

- ``calendar-smith``: The main entry point with subcommands (``solve``, ``week-span``, ``nth``, ``windows``, ``tz``, ``fiscal-year``, ``csv``).

Standalone scripts
^^^^^^^^^^^^^^^^^^

- ``calendar-smith-csv``: Appends a ``fiscal_year`` column to an existing CSV.
- ``calendar-smith-solve``: Lists Monday-to-Sunday date ranges for every ISO week in a given year.
- ``calendar-smith-nth``: Interactive tool to find the ordinal week of the month/year for any date.
- ``calendar-smith-week-span``: Shows the Monday-to-Sunday span for a specific ISO week.
- ``calendar-smith-windows``: Generates date windows (consecutive, overlapping, or gapped).
- ``calendar-smith-tz``: Converts a timestamp to a target timezone.
- ``calendar-smith-fiscal-year``: Displays the fiscal year for a given date.

---

Quick examples
--------------

Get fiscal year:

.. code-block:: bash

   calendar-smith fiscal-year 2026-04-22 --system jp

Generate 4 consecutive 7-day windows:

.. code-block:: bash

   calendar-smith windows 2026-03-17 7 4

Convert timezone:

.. code-block:: bash

   calendar-smith tz 2026-03-20T10:00:00+09:00 America/New_York

---

Command details
---------------

calendar-smith-csv
^^^^^^^^^^^^^^^^^^

Appends a ``fiscal_year`` column to an existing CSV file.

.. code-block:: bash

   calendar-smith-csv records.csv output.csv --system jp --date-column created_at

Options:

- ``--system``: One of ``us`` (fiscal year ends Sep 30) or ``jp`` (fiscal year ends Mar 31).
- ``--date-column``: The name of the column containing the date strings.

calendar-smith-nth
^^^^^^^^^^^^^^^^^^

An interactive tool (or non-interactive with ``--date``) to determine the ordinal week of the month and the ISO week of the year.

.. code-block:: bash

   calendar-smith-nth --date 2026-02-17

calendar-smith-windows
^^^^^^^^^^^^^^^^^^^^^^

Generates a sequence of date windows starting from a given date.

.. code-block:: bash

   calendar-smith-windows START_DATE SIZE COUNT [options]

Example:

.. code-block:: bash

   # Generate 4 overlapping 7-day windows starting every 1 day
   calendar-smith-windows 2026-03-17 7 4 --sampling-rate 1

---

Getting help
------------

To see the help message for the top-level command:

.. code-block:: bash

   calendar-smith --help

To see the help message for a specific subcommand:

.. code-block:: bash

   calendar-smith fiscal-year --help

---

Notes
-----

- All CLI commands strictly reject ambiguous date formats (e.g., 6-digit or 7-digit numbers) to prevent data corruption.
- Output is generally formatted for human readability or as CSV where applicable.
