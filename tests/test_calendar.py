import io
from unittest.mock import patch

from calendar_smith.cli import main, solve_week_span, solve_weeks


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
