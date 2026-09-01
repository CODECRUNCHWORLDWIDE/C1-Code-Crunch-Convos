"""Stretch additions to `report`: compounding and per-category totals.

Kept in its own file so the four files the brief asks for stay exactly as
specified. Like `report`, everything here is pure: numbers in, numbers or
strings out.
"""

import report

CATEGORY_WIDTH = 17
CATEGORY_VALUE_WIDTH = 9
DEFAULT_CATEGORY = "other"


def compounded_projection(monthly: float, months: int, monthly_rate: float) -> float:
    """Return the value of `months` monthly deposits compounded at `monthly_rate`.

    `monthly_rate` is a fraction per month, so 0.004 is 0.4% a month. A rate of
    0 gives exactly the same answer as `report.project_savings`.
    """
    if months < 0:
        raise ValueError("months must be zero or positive")
    if monthly_rate == 0:
        return report.project_savings(monthly, months)
    return monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)


def totals_by_category(items: list[dict]) -> dict[str, float]:
    """Return {category: total} for `items`, defaulting a missing category."""
    totals: dict[str, float] = {}
    for item in items:
        category = item.get("category", DEFAULT_CATEGORY)
        totals[category] = totals.get(category, 0.0) + item["amount"]
    return totals


def format_categories(items: list[dict]) -> str:
    """Return a category breakdown block, sorted by descending total."""
    totals = totals_by_category(items)
    ordered = sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
    lines = [report.RULE, "Expenses by category", report.RULE]
    for category, amount in ordered:
        lines.append(
            f"{category + ':':<{CATEGORY_WIDTH}} {f'${amount:.2f}':>{CATEGORY_VALUE_WIDTH}}"
        )
    lines.append(report.RULE)
    return "\n".join(lines)


def _demo() -> str:
    """Return both stretch features running on the brief's sample numbers."""
    items = [
        {"label": "rent", "amount": 900.0, "category": "housing"},
        {"label": "food", "amount": 350.0, "category": "living"},
        {"label": "transport", "amount": 120.0, "category": "living"},
    ]
    flat = report.project_savings(1530.0, 12)
    grown = compounded_projection(1530.0, 12, 0.004)
    return "\n".join(
        [
            format_categories(items),
            f"straight-line 12 mo: ${flat:.2f}",
            f"compounded at 0.4%/mo: ${grown:.2f}",
        ]
    )


if __name__ == "__main__":
    print(_demo())
