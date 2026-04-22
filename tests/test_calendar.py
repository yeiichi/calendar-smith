import io
import pytest
from unittest.mock import patch
from calendar_smith.cli import (
    main, solve_week_span, solve_weeks, 
    determine_nth_week, generate_windows, fiscal_year, process_csv
)


def test_calendar_smith_solve_subcommand():
    """Verify the umbrella CLI can list ISO weeks."""
    test_args = ["calendar-smith", "solve", "2020"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "ISO Weeks in 2020" in output
            assert "Week 53" in output


def test_calendar_smith_week_span_subcommand():
    """Verify the umbrella CLI can show an ISO week span."""
    test_args = ["calendar-smith", "week-span", "2020", "53"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "ISO Week 53 in 2020" in output
            assert "Start: 2020-12-28" in output
            assert "End:   2021-01-03" in output


def test_legacy_calendar_smith_week_span_script_still_works():
    """Verify the old dedicated script entry point still works."""
    test_args = ["calendar-smith-week-span", "2020", "53"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            solve_week_span()
            output = fake_out.getvalue()
            assert "ISO Week 53 in 2020" in output
            assert "Start: 2020-12-28" in output
            assert "End:   2021-01-03" in output


def test_legacy_calendar_smith_solve_script_still_works():
    """Verify the old dedicated solve script entry point still works."""
    test_args = ["calendar-smith-solve", "2020"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            solve_weeks()
            output = fake_out.getvalue()
            assert "ISO Weeks in 2020" in output
            assert "Week 53" in output

def test_determine_nth_week_cli():
    """Verify the nth week CLI."""
    test_args = ["calendar-smith-nth"]
    with patch("sys.argv", test_args):
        with patch("builtins.input", return_value="2024-04-22"):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                determine_nth_week()
                output = fake_out.getvalue()
                assert "Month Week: The 4th week" in output

def test_generate_windows_cli():
    """Verify the windows generation CLI."""
    test_args = ["calendar-smith-windows", "2024-01-01", "7", "2", "--sampling-rate", "14"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            generate_windows()
            output = fake_out.getvalue()
            assert "Window  1: 2024-01-01 to 2024-01-07" in output
            assert "Window  2: 2024-01-15 to 2024-01-21" in output

def test_fiscal_year_cli():
    """Verify the fiscal year CLI."""
    test_args = ["calendar-smith-fiscal-year", "2023-10-01", "--system", "us"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            fiscal_year()
            output = fake_out.getvalue().strip()
            assert output == "2024"

def test_process_csv_cli(tmp_path):
    """Verify the CSV processing CLI."""
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "output.csv"
    input_csv.write_text("date,event\n2023-09-30,last day\n2023-10-01,new year\n")
    
    test_args = ["calendar-smith-csv", str(input_csv), str(output_csv), "--date-column", "date", "--system", "us"]
    with patch("sys.argv", test_args):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            process_csv()
            output = fake_out.getvalue()
            assert "Successfully saved" in output
            
    content = output_csv.read_text()
    assert "fiscal_year" in content
    assert "2023-09-30,last day,2023" in content
    assert "2023-10-01,new year,2024" in content
