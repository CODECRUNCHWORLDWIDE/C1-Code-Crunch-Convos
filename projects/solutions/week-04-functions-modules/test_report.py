"""Stretch goal 4: pytest tests for the pure parts of the project.

Run from this folder with:  python -m pytest -q

`main.py` is not tested here on purpose. It is the only file that talks to the
user, and testing prompts needs tools we have not met yet. That asymmetry is the
whole argument for keeping the computation pure and the I/O thin.
"""

import pytest

import expenses
import income
import report
import report_stretch

BRIEF_REPORT = """\
------------------------------
Personal Finance Report
------------------------------
Income:            $2900.00
Expenses:          $1370.00
Monthly savings:   $1530.00
Savings rate:        52.76%
Projected (12 mo): $18360.00
------------------------------"""


def test_add_income_does_not_mutate_its_argument() -> None:
    original: list[dict] = []
    result = income.add_income(original, "salary", 2500)
    assert original == []
    assert result == [{"label": "salary", "amount": 2500.0}]


def test_totals_start_at_float_zero() -> None:
    assert income.total_income([]) == 0.0
    assert isinstance(income.total_income([]), float)
    assert expenses.total_expenses([]) == 0.0
    assert isinstance(expenses.total_expenses([]), float)


def test_totals_add_up() -> None:
    sources = income.add_income(income.add_income([], "salary", 2500), "freelance", 400)
    assert income.total_income(sources) == 2900.0


def test_savings_rate_matches_the_brief() -> None:
    assert report.savings_rate(2900, 1370) == pytest.approx(52.7586206896, rel=1e-9)


def test_savings_rate_of_zero_income_is_zero_not_a_crash() -> None:
    assert report.savings_rate(0, 0) == 0.0
    assert report.savings_rate(0, 500) == 0.0


def test_savings_rate_can_go_negative() -> None:
    assert report.savings_rate(1000, 1500) == -50.0


def test_project_savings_rejects_negative_months() -> None:
    with pytest.raises(ValueError, match="months must be zero or positive"):
        report.project_savings(100.0, -1)


def test_project_savings_allows_zero_months() -> None:
    assert report.project_savings(100.0, 0) == 0.0


def test_format_report_matches_the_brief_byte_for_byte() -> None:
    assert report.format_report(2900.0, 1370.0, 12) == BRIEF_REPORT


def test_compounding_at_zero_equals_straight_line() -> None:
    assert report_stretch.compounded_projection(1530.0, 12, 0.0) == 18360.0


def test_compounding_beats_straight_line_at_a_positive_rate() -> None:
    grown = report_stretch.compounded_projection(1530.0, 12, 0.004)
    assert grown > report.project_savings(1530.0, 12)
    assert grown == pytest.approx(18769.35, abs=0.01)


def test_totals_by_category_defaults_a_missing_category() -> None:
    items = [
        {"label": "rent", "amount": 900.0, "category": "housing"},
        {"label": "food", "amount": 350.0, "category": "living"},
        {"label": "transport", "amount": 120.0, "category": "living"},
        {"label": "misc", "amount": 30.0},
    ]
    assert report_stretch.totals_by_category(items) == {
        "housing": 900.0,
        "living": 470.0,
        "other": 30.0,
    }
