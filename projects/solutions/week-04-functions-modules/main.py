"""Personal Finance Calculator -- entry point.

The only file in this project that calls `print` or `input`. It collects income
sources and expenses from the user, asks for a projection horizon, and hands the
three numbers to `report.format_report`.

Run it with:  python main.py
"""

from collections.abc import Callable

import expenses
import income
import report

BANNER = "== Personal Finance Calculator =="
INCOME_HEADING = "Enter income sources. Blank label to stop."
EXPENSE_HEADING = "Enter expenses. Blank label to stop."
MONTHS_PROMPT = "Project savings over how many months? "

# add_income and add_expense have the same shape, so `collect` can take either.
Adder = Callable[[list[dict], str, float], list[dict]]


def read_amount() -> float:
    """Prompt for an amount until the user types something `float()` accepts."""
    while True:
        raw = input("  Amount: ").strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  {raw!r} is not a number. Try again.")


def read_months() -> int:
    """Prompt until the user types a whole number of months that is >= 0."""
    while True:
        raw = input(MONTHS_PROMPT).strip()
        try:
            months = int(raw)
        except ValueError:
            print(f"{raw!r} is not a whole number. Try again.")
            continue
        if months < 0:
            print("Months cannot be negative. Try again.")
            continue
        return months


def collect(heading: str, add: Adder) -> list[dict]:
    """Collect label/amount pairs with `add` until the user leaves a label blank."""
    print(heading)
    entries: list[dict] = []
    while True:
        try:
            label = input("  Label: ").strip()
        except EOFError:
            break
        if not label:
            break
        entries = add(entries, label, read_amount())
    print()
    return entries


def main() -> None:
    """Run the interview and print the report."""
    print(BANNER)
    print()
    sources = collect(INCOME_HEADING, income.add_income)
    items = collect(EXPENSE_HEADING, expenses.add_expense)
    months = read_months()
    print()
    print(
        report.format_report(
            income.total_income(sources),
            expenses.total_expenses(items),
            months,
        )
    )


if __name__ == "__main__":
    main()
