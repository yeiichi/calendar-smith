# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-17

### Added
- Initial release of **calendar-smith**.
- `calendar-smith-csv`: CLI tool to append fiscal year columns to CSV data.
- `calendar-smith-solve`: CLI tool to list ISO week ranges for any given year.
- `calendar-smith-nth`: CLI tool to calculate the ordinal week of the month for a date.
- Support for US (Oct-Sep) and Japanese (Apr-Mar) fiscal year systems.
- "Safety-first" date parser supporting ISO 8601, `YYYYMMDD`, and delimited formats.

### Changed
- Refined `to_date` logic to prioritize high-speed `fromisoformat` parsing with a flexible fallback.

### Fixed
- Resolved `ImportError` regarding script entry points in `pyproject.toml`.
- Eliminated century ambiguity by explicitly rejecting 6-digit (`YYMMDD`) and 7-digit date strings.

### Security
- Implemented strict input validation to prevent silent data corruption from ambiguous date shorthand.