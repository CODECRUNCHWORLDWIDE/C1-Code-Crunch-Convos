"""Income module for the Personal Finance Calculator.

This module owns the concept of "income source". An income source is a
dict shaped like:

    {"label": "salary", "amount": 2500.0}

Public functions:
    add_income(sources, label, amount) -> list[dict]
    total_income(sources) -> float

This file is part of the Week 4 mini-project. See ../README.md.
"""


def add_income(sources: list[dict], label: str, amount: float) -> list[dict]:
    """Append a new income source to `sources` and return the updated list.

    Args:
        sources: The current list of income source dicts.
        label: A short description, e.g. "salary".
        amount: The monthly amount in your local currency. Must be >= 0.

    Returns:
        The updated list of sources.

    Raises:
        ValueError: If `label` is empty or `amount` is negative.
    """
    # TODO:
    #   1. Validate `label` (not empty, not just whitespace).
    #   2. Validate `amount` (>= 0).
    #   3. Append a new dict {"label": ..., "amount": ...} to `sources`.
    #   4. Return `sources`.
    raise NotImplementedError("add_income is not yet implemented")


def total_income(sources: list[dict]) -> float:
    """Return the sum of `amount` values across all sources.

    Args:
        sources: List of income source dicts.

    Returns:
        The total monthly income as a float. Returns 0.0 for an empty list.
    """
    # TODO:
    #   1. Loop over `sources` and add up the "amount" of each.
    #   2. Return the total. Use 0.0 as the starting value to keep it a float.
    raise NotImplementedError("total_income is not yet implemented")


def _demo() -> None:
    """Print a small self-demo when this file is run directly."""
    sources: list[dict] = []
    sources = add_income(sources, "salary", 2500.0)
    sources = add_income(sources, "freelance", 400.0)
    print(f"Sources: {sources}")
    print(f"Total monthly income: {total_income(sources):.2f}")


if __name__ == "__main__":
    _demo()
