"""Entry point for the Personal Finance Calculator.

This is the ONLY file in the mini-project that talks to the user (calls
`print` and `input`). It imports the three sibling modules and ties
them together.

Run it from inside the project folder:

    $ python main.py

See ../README.md for the full spec.
"""

from income import add_income, total_income
from expenses import add_expense, total_expenses
from report import format_report


def _read_amount(prompt: str) -> float:
    """Prompt the user for a numeric amount, re-asking on bad input.

    Args:
        prompt: The prompt string to display.

    Returns:
        A float >= 0.
    """
    # TODO:
    #   1. Loop forever.
    #   2. Call input(prompt) and try to convert to float.
    #   3. If conversion fails, print a hint and continue.
    #   4. If the number is negative, print a hint and continue.
    #   5. Otherwise return it.
    raise NotImplementedError("_read_amount is not yet implemented")


def _read_int(prompt: str) -> int:
    """Prompt for a non-negative integer, re-asking on bad input."""
    # TODO: similar pattern to _read_amount, but with int() and a >= 0 check.
    raise NotImplementedError("_read_int is not yet implemented")


def _collect_incomes() -> list[dict]:
    """Loop and collect income sources until the user enters a blank label."""
    sources: list[dict] = []
    print("\nEnter income sources. Blank label to stop.")
    # TODO:
    #   1. Loop.
    #   2. Ask for "  Label: ".
    #   3. If blank, break.
    #   4. Ask for "  Amount: " using _read_amount.
    #   5. Call add_income(sources, label, amount).
    return sources


def _collect_expenses() -> list[dict]:
    """Loop and collect expenses until the user enters a blank label."""
    items: list[dict] = []
    print("\nEnter expenses. Blank label to stop.")
    # TODO: same pattern as _collect_incomes but with add_expense.
    return items


def main() -> None:
    """Run the full personal finance calculator flow."""
    print("== Personal Finance Calculator ==")

    sources = _collect_incomes()
    items = _collect_expenses()

    months = _read_int("\nProject savings over how many months? ")

    income = total_income(sources)
    expenses = total_expenses(items)

    print()
    print(format_report(income=income, expenses=expenses, months=months))


if __name__ == "__main__":
    main()
