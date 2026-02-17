# src/calendar_smith/cli.py
import argparse
import csv
import sys
from pathlib import Path
from .core import get_fiscal_year, get_iso_weeks_for_year, get_nth_week_of_month
from .utils import to_date, format_ordinal

def process_csv():
    """Entry point for: calendar-smith-csv"""
    parser = argparse.ArgumentParser(description="Add fiscal year column to a CSV.")
    parser.add_argument("input_csv", type=Path, help="Path to input CSV file")
    parser.add_argument("output_csv", type=Path, help="Path to output CSV file")
    parser.add_argument("--date-column", default="date", help="Name of date column (default: 'date')")
    parser.add_argument(
        "--system",
        choices=["us", "jp"],
        default="us",
        help="Fiscal system: 'us' (Oct-30 end) or 'jp' (Mar-31 end)."
    )

    args = parser.parse_args()

    try:
        if not args.input_csv.exists():
            print(f"Error: File {args.input_csv} not found.")
            sys.exit(1)

        with open(args.input_csv, mode='r', encoding='utf-8') as f_in, \
             open(args.output_csv, mode='w', encoding='utf-8', newline='') as f_out:
            
            reader = csv.DictReader(f_in)
            if args.date_column not in reader.fieldnames:
                print(f"Error: Column '{args.date_column}' not found in CSV.")
                sys.exit(1)

            fieldnames = reader.fieldnames + ['fiscal_year']
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in reader:
                # Uses the flexible but safe parser from utils.py
                d = to_date(row[args.date_column])
                # Uses the core fiscal year logic
                row['fiscal_year'] = get_fiscal_year(d, args.system)
                writer.writerow(row)
        
        print(f"Successfully saved to {args.output_csv} (System: {args.system.upper()})")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def solve_weeks():
    """Entry point for: calendar-smith-solve"""
    parser = argparse.ArgumentParser(description="List ISO week date ranges for a given year.")
    parser.add_argument("year", type=int, help="Target year (YYYY)")
    args = parser.parse_args()
    
    print(f"\nISO Weeks in {args.year} (Monday–Sunday):")
    # Fetches the list of WeekSpan namedtuples
    weeks = get_iso_weeks_for_year(args.year)
    for w in weeks:
        print(f"Week {w.number:2}: {w.start} {w.end}")

def determine_nth_week():
    """Entry point for: calendar-smith-nth"""
    print("--- Nth Week of Month Calculator ---")
    date_input = input('Date? [yyyy-mm-dd] (leave blank for today) >> ').strip()
    
    try:
        # Defaults to today if input is empty
        d = to_date(date_input if date_input else None)
        # Calculates ordinal week of month
        nth = get_nth_week_of_month(d)
        
        # Display results with human-readable ordinal formatting
        print(f"\nResult:")
        print(f"  Date:       {d.isoformat()} ({d.strftime('%A')})")
        print(f"  Month Week: The {format_ordinal(nth)} week")
        print(f"  Year Week:  The {format_ordinal(d.isocalendar().week)} week")
    except ValueError as e:
        print(f"Error: {e}")