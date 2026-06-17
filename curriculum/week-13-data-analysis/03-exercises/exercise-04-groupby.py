"""Exercise 04 — Groupby: sales by category.

Goal
----
You are given 12 rows of fake sales data. For each `category`, compute:

- the **total** revenue (`revenue.sum()`),
- the **average** revenue per sale (`revenue.mean()`),
- the **number** of sales (`size`).

Then sort the result by total revenue descending.

This is the single most common pandas pattern in business analytics.

How to run
----------
    python exercise-04-groupby.py
"""

from __future__ import annotations

import pandas as pd


def build_sales() -> pd.DataFrame:
    """Return a fake sales DataFrame: 12 transactions across 4 categories."""
    data: dict[str, list] = {
        "sale_id":  list(range(1, 13)),
        "category": [
            "Books",   "Books",   "Books",
            "Toys",    "Toys",
            "Games",   "Games",   "Games",   "Games",
            "Music",   "Music",   "Music",
        ],
        "revenue":  [12.99, 8.50, 19.99, 24.00, 14.50, 39.99, 49.99, 29.99, 19.99, 9.99, 14.99, 7.50],
    }
    return pd.DataFrame(data)


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Group by category and return total, mean, and count of revenue.

    The output columns must be named exactly: `total`, `average`, `count`.
    Sort the result by `total` descending.

    Use the named-aggregation form of `agg`:

        df.groupby("category").agg(
            total=("revenue", "sum"),
            average=("revenue", "mean"),
            count=("revenue", "size"),
        )
    """
    # YOUR CODE HERE
    summary = (
        df.groupby("category")
        .agg(
            total=("revenue", "sum"),
            average=("revenue", "mean"),
            count=("revenue", "size"),
        )
        .sort_values("total", ascending=False)
        .round(2)
    )
    return summary


def main() -> None:
    sales = build_sales()

    print("\nRaw sales:")
    print(sales.to_string(index=False))

    summary = summarize_by_category(sales)
    print("\nSummary by category (sorted by total revenue, descending):")
    print(summary)

    # Sanity checks:
    expected_cols = {"total", "average", "count"}
    assert set(summary.columns) == expected_cols, (
        f"Expected columns {expected_cols}, got {set(summary.columns)}"
    )
    assert summary["total"].is_monotonic_decreasing, "totals should be descending"
    assert summary["count"].sum() == len(sales), "counts should sum to total rows"
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
