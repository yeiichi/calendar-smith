# src/calendar_smith/cli.py
import argparse
import csv
import sys
from pathlib import Path

from .core import (
    get_fiscal_year,
    get_iso_weeks_for_year,
    get_iso_week_span,
    get_nth_week_of_month,
    get_dates_windows,
)
from .utils import ensure_date, format_ordinal
from .time import from_iso, to_timezone, tz, to_iso


def process_csv_args(args):
    """Add a fiscal year column to a CSV."""
    try:
        if not args.input_csv.exists():
            print(f"Error: File {args.input_csv} not found.")
            sys.exit(1)

        with open(args.input_csv, mode="r", encoding="utf-8") as f_in, \
                open(args.output_csv, mode="w", encoding="utf-8", newline="") as f_out:

            reader = csv.DictReader(f_in)
            if args.date_column not in reader.fieldnames:
                print(f"Error: Column '{args.date_column}' not found in CSV.")
                sys.exit(1)

            fieldnames = reader.fieldnames + ["fiscal_year"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)

            writer.writeheader()
            for row in reader:
                d = ensure_date(row[args.date_column])
                row["fiscal_year"] = get_fiscal_year(d, args.system)
                writer.writerow(row)

        print(f"Successfully saved to {args.output_csv} (System: {args.system.upper()})")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def solve_weeks_args(args):
    """List ISO week ranges for a year."""
    print(f"\nISO Weeks in {args.year} (Monday–Sunday):")
    weeks = get_iso_weeks_for_year(args.year)
    for w in weeks:
        print(f"Week {w.number:2}: {w.start} {w.end}")


def solve_week_span_args(args):
    """Show the span for a specific ISO week."""
    try:
        span = get_iso_week_span(args.iso_year, args.iso_week)
        print(f"\nISO Week {span.number} in {args.iso_year}:")
        print(f"  Start: {span.start}")
        print(f"  End:   {span.end}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def determine_nth_week_args(_args):
    """Show the week number within a month."""
    print("--- Nth Week of Month Calculator ---")
    date_input = input("Date? [yyyy-mm-dd] (leave blank for today) >> ").strip()

    try:
        d = ensure_date(date_input if date_input else None)
        nth = get_nth_week_of_month(d)

        print("\nResult:")
        print(f"  Date:       {d.isoformat()} ({d.strftime('%A')})")
        print(f"  Month Week: The {format_ordinal(nth)} week")
        print(f"  Year Week:  The {format_ordinal(d.isocalendar().week)} week")
    except ValueError as e:
        print(f"Error: {e}")


def generate_windows_args(args):
    """Generate date windows with optional sampling rate."""
    try:
        start = ensure_date(args.start_date)
        dates = get_dates_windows(start, args.window_size, args.repeats, args.sampling_rate)

        print(f"\nGenerated {args.repeats} windows starting from {start} with size {args.window_size}:")
        if args.sampling_rate:
            print(f"  (Sampling rate: {args.sampling_rate} days)")
        for i, window in enumerate(dates, 1):
            print(f"  Window {i:2}: {window.start} to {window.end}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def convert_timezone_args(args):
    """Convert an ISO 8601 datetime to another timezone."""
    try:
        dt = from_iso(args.dt_iso)
        target = tz(args.target_tz)
        converted = to_timezone(dt, target)
        print(to_iso(converted))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="calendar-smith",
        description="Calendar-Smith command line tools.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_csv = subparsers.add_parser("csv", help="Add fiscal year column to a CSV.")
    p_csv.add_argument("input_csv", type=Path)
    p_csv.add_argument("output_csv", type=Path)
    p_csv.add_argument("--date-column", default="date")
    p_csv.add_argument("--system", choices=["us", "jp"], default="us")
    p_csv.set_defaults(func=process_csv_args)

    p_solve = subparsers.add_parser("solve", help="List ISO week date ranges for a year.")
    p_solve.add_argument("year", type=int)
    p_solve.set_defaults(func=solve_weeks_args)

    p_nth = subparsers.add_parser("nth", help="Interactive week-of-month calculator.")
    p_nth.set_defaults(func=determine_nth_week_args)

    p_span = subparsers.add_parser("week-span", help="Show the span for a specific ISO week.")
    p_span.add_argument("iso_year", type=int)
    p_span.add_argument("iso_week", type=int)
    p_span.set_defaults(func=solve_week_span_args)

    p_windows = subparsers.add_parser("windows", help="Generate date windows.")
    p_windows.add_argument("start_date")
    p_windows.add_argument("window_size", type=int)
    p_windows.add_argument("repeats", type=int)
    p_windows.add_argument("--sampling-rate", "-s", type=int)
    p_windows.set_defaults(func=generate_windows_args)

    p_tz = subparsers.add_parser("tz", help="Convert an ISO 8601 datetime to another timezone.")
    p_tz.add_argument("dt_iso")
    p_tz.add_argument("target_tz")
    p_tz.set_defaults(func=convert_timezone_args)

    return parser


def main(argv=None):
    """Top-level CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def process_csv():
    return main(["csv", *sys.argv[1:]])


def solve_weeks():
    return main(["solve", *sys.argv[1:]])


def solve_week_span():
    return main(["week-span", *sys.argv[1:]])


def determine_nth_week():
    return main(["nth"])


def generate_windows():
    return main(["windows", *sys.argv[1:]])


def convert_timezone():
    return main(["tz", *sys.argv[1:]])
