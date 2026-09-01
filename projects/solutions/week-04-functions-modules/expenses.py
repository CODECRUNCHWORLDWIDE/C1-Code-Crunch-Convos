"""Monthly expenses.

An "item" is a dict with exactly two keys: "label" (str) and "amount" (float).
Deliberately the same shape as an income source -- see 00-overview.md for why
the two modules stay separate anyway.
"""


def add_expense(items: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `items` plus one more expense."""
    return [*items, {"label": label, "amount": float(amount)}]


def total_expenses(items: list[dict]) -> float:
    """Return the sum of every item's amount, or 0.0 for no items."""
    return sum((item["amount"] for item in items), 0.0)


def _demo() -> str:
    """Return a short demonstration of this module's two public functions."""
    items = add_expense([], "rent", 900)
    items = add_expense(items, "food", 350)
    items = add_expense(items, "transport", 120)
    return "\n".join(
        [
            f"items: {items}",
            f"total_expenses: {total_expenses(items):.2f}",
            f"total_expenses([]): {total_expenses([]):.2f}",
        ]
    )


if __name__ == "__main__":
    print(_demo())
