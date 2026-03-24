Changelog
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

0.4.0 - 2026-03-24
------------------

Added
~~~~~
- ``DateRange``: New namedtuple for simple date ranges.
- ``sampling_rate`` parameter in ``get_dates_windows``: Allows generating overlapping or gapped date windows.
- ``--sampling-rate`` (or ``-s``) option to ``calendar-smith-windows`` CLI tool.

Changed
~~~~~~~
- Bumped package version to ``0.4.0``.
- Updated ``src/calendar_smith/__init__.py`` to export ``DateRange``.
- Updated ``README.rst`` with ``sampling_rate`` examples and documentation.

0.3.0 - 2026-03-20
------------------

Added
~~~~~
- ``src/calendar_smith/time.py``: New module for timezone-aware datetime utilities.
- ``calendar-smith-tz``: New CLI tool to convert ISO 8601 datetime strings between timezones.
- New timezone constants: ``UTC_TZ``, ``JST``, ``KST``, ``CST_CN``, ``IST``, ``SGT``, ``ET``, ``PT``, ``GMT``, ``CET``.
- New functions: ``now_utc``, ``now_in``, ``now_jst``, ``now_et``, ``to_timezone``, ``to_iso``, ``from_iso``, ``tz``.

Changed
~~~~~~~
- Bumped package version to ``0.3.0``.
- Updated ``src/calendar_smith/__init__.py`` to export new timezone utilities.
- Updated ``README.rst`` with timezone usage examples and CLI documentation.

0.2.3 - 2026-03-19
------------------

Added
~~~~~
- ``calendar-smith-week-span``: New CLI tool to retrieve the start and end dates for a specific ISO week number.
- ``get_iso_week_span``: New core utility function to get the Monday-to-Sunday span for a given ISO year and week.

Changed
~~~~~~~
- Bumped package version to ``0.2.3``.
- Updated author email in ``pyproject.toml``.

0.2.2 - 2026-03-17
------------------

Changed
~~~~~~~
- Bumped package version to ``0.2.2``.
- Refreshed ``README.rst`` so CLI descriptions and examples match current behavior.
- Clarified fiscal-year wording and windows output documentation.

0.2.1 - 2026-03-17
------------------

Changed
~~~~~~~
- Bumped package version to ``0.2.1``.

0.2.0 - 2026-03-17
------------------

Added
~~~~~
- ``calendar-smith-windows``: New CLI tool to generate a sequence of future dates using a starting date, window size (days), and repeat count.
- ``get_dates_windows``: New core utility function to programmatically generate lists of dates by incrementing a starting date.
- Added comprehensive project metadata to ``pyproject.toml``, including keywords, standard PyPI classifiers, and project URLs (Homepage, Repository, Bug Tracker).

Changed
~~~~~~~
- Bumped package version to ``0.2.0``.
- Formally exposed ``get_dates_windows`` and ``WeekSpan`` in the public API (``calendar_smith`` package root).
- Modified ``get_dates_windows`` and ``calendar-smith-windows`` to return/print window ranges (start to end) to clearly show ending dates.

0.1.0 - 2026-02-17
------------------

Added
~~~~~
- Initial release of **calendar-smith**.
- ``calendar-smith-csv``: CLI tool to append fiscal year columns to CSV data.
- ``calendar-smith-solve``: CLI tool to list ISO week ranges for any given year.
- ``calendar-smith-nth``: CLI tool to calculate the ordinal week of the month for a date.
- Support for US (Oct-Sep) and Japanese (Apr-Mar) fiscal year systems.
- "Safety-first" date parser supporting ISO 8601, ``YYYYMMDD``, and delimited formats.

Changed
~~~~~~~
- Refined ``to_date`` logic to prioritize high-speed ``fromisoformat`` parsing with a flexible fallback.

Fixed
~~~~
- Resolved ``ImportError`` regarding script entry points in ``pyproject.toml``.
- Eliminated century ambiguity by explicitly rejecting 6-digit (``YYMMDD``) and 7-digit date strings.

Security
~~~~~~~~
- Implemented strict input validation to prevent silent data corruption from ambiguous date shorthand.
