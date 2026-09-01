"""exercise-01-function-basics-solution.py — the tool library's late-fee desk.

Three small functions. One works out the fee, one says it in plain English,
one writes it into the day's ledger.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

DAILY_RATE = 0.25
FEE_CAP = 5.00


def late_fee(
    days_late: int,
    daily_rate: float = DAILY_RATE,
    cap: float = FEE_CAP,
) -> float:
    """Return the fee owed for bringing a tool back `days_late` days late.

    Args:
        days_late: Whole days past the due date. Zero or negative is on time.
        daily_rate: Dollars charged per late day.
        cap: The most the library will ever charge for one tool.

    Returns:
        The fee in dollars, rounded to two decimals. Never above `cap`.
    """
    if days_late <= 0:
        return 0.0
    return round(min(days_late * daily_rate, cap), 2)


def borrower_summary(name: str, tool: str, days_late: int) -> str:
    """Return one line of plain English describing what `name` owes."""
    fee = late_fee(days_late)
    if fee == 0.0:
        return f"{name} returned the {tool} on time."
    day_word = "day" if days_late == 1 else "days"
    return f"{name} owes ${fee:.2f} for the {tool} ({days_late} {day_word} late)."


def record_fee(entry: str, ledger: list[str] | None = None) -> list[str]:
    """Append `entry` to `ledger` and return it, starting a new one if needed."""
    if ledger is None:
        ledger = []
    ledger.append(entry)
    return ledger


if __name__ == "__main__":
    assert late_fee(0) == 0.0, late_fee(0)
    assert late_fee(-2) == 0.0, late_fee(-2)
    assert late_fee(3) == 0.75, late_fee(3)
    assert late_fee(5) == 1.25, late_fee(5)
    assert late_fee(40) == 5.00, late_fee(40)
    assert late_fee(4, daily_rate=0.50) == 2.00, late_fee(4, daily_rate=0.50)
    assert late_fee(3, cap=0.50) == 0.50, late_fee(3, cap=0.50)

    print(borrower_summary("Rosa", "hedge trimmer", 5))
    print(borrower_summary("Ken", "socket set", 1))
    print(borrower_summary("Amina", "cordless drill", 0))
    print(borrower_summary("Marcus", "wheelbarrow", 40))

    assert borrower_summary("Ken", "socket set", 1) == (
        "Ken owes $0.25 for the socket set (1 day late)."
    )
    assert borrower_summary("Amina", "cordless drill", 0) == (
        "Amina returned the cordless drill on time."
    )

    first = record_fee("Rosa $1.25")
    second = record_fee("Ken $0.25")
    assert first == ["Rosa $1.25"], first
    assert second == ["Ken $0.25"], second

    running = record_fee("Marcus $5.00")
    record_fee("Priya $0.50", running)
    assert running == ["Marcus $5.00", "Priya $0.50"], running

    print("All checks passed.")
