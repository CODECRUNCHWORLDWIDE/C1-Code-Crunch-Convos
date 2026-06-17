"""Expenses module for the Personal Finance Calculator.

This module owns the concept of "expense". An expense is a dict shaped
like:

    {"label": "rent", "amount": 900.0}

Public functions:
    add_expense(items, label, amount) -> list[dict]
    total_expenses(items) -> float

This file is part of the Week 4 mini-project. See ../README.md.
"""


def add_expense(items: list[dict], label: str, amount: float) -> list[dict]:
    """Append a new expense to `items` and return the updated list.

    Args:
        items: The current list of expense dicts.
        label: A short description, e.g. "rent".
        amount: The monthly amount. Must be >= 0.

    Returns:
        The updated list of expenses.

    Raises:
        ValueError: If `label` is empty or `amount` is negative.
    """
    # TODO:
    #   1. Validate `label` (not empty, not just whitespace).
    #   2. Validate `amount` (>= 0).
    #   3. Append a new dict {"label": ..., "amount": ...} to `items`.
    #   4. Return `items`.
    raise NotImplementedError("add_expense is not yet implemented")


def total_expenses(items: list[dict]) -> float:
    """Return the sum of `amount` values across all expenses.

    Args:
        items: List of expense dicts.

    Returns:
        The total monthly expenses as a float. Returns 0.0 for empty input.
    """
    # TODO:
    #   1. Loop over `items` and sum each "amount".
    #   2. Return the total. Start from 0.0 to keep the result a float.
    raise NotImplementedError("total_expenses is not yet implemented")


def _demo() -> None:
    """Print a small self-demo when this file is run directly."""
    items: list[dict] = []
    items = add_expense(items, "rent", 900.0)
    items = add_expense(items, "food", 350.0)
    items = add_expense(items, "transport", 120.0)
    print(f"Items: {items}")
    print(f"Total monthly expenses: {total_expenses(items):.2f}")


if __name__ == "__main__":
    _demo()
