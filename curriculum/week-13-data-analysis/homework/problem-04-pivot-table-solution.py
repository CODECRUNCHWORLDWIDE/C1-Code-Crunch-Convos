"""hw-04-pivot.py — two pivot tables over a small restaurant-tips frame.

The homework uses seaborn's ``tips`` dataset. So it runs offline and identically
everywhere, this shipped answer builds an inline frame with the same shape — a
``day`` category, a ``time`` category, and a ``total_bill`` — and, like the real
data, no weekend *lunch* service, so the empty-cell handling is exercised.
"""

from __future__ import annotations

import pandas as pd

DAYS = ["Thur", "Fri", "Sat", "Sun"]
TIMES = ["Lunch", "Dinner"]

TIPS: dict[str, list] = {
    "day": [
        "Thur", "Thur", "Thur", "Fri", "Fri", "Sat", "Sat", "Sat",
        "Sun", "Sun", "Sun", "Thur", "Fri", "Sat", "Sun",
    ],
    "time": [
        "Lunch", "Lunch", "Dinner", "Lunch", "Dinner", "Dinner", "Dinner",
        "Dinner", "Dinner", "Dinner", "Dinner", "Lunch", "Lunch", "Dinner",
        "Dinner",
    ],
    "total_bill": [
        12.50, 15.00, 20.00, 11.00, 22.00, 25.00, 30.00, 18.00,
        28.00, 24.00, 26.00, 14.00, 13.50, 21.00, 27.00,
    ],
}


def mean_bill_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean total_bill for every (day, time) cell; empty cells become 0."""
    return df.pivot_table(
        index="day",
        columns="time",
        values="total_bill",
        aggfunc="mean",
        fill_value=0,
        observed=False,
    ).round(2)


def order_count_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Number of orders in every (day, time) cell, as integers."""
    return df.pivot_table(
        index="day",
        columns="time",
        values="total_bill",
        aggfunc="size",
        fill_value=0,
        observed=False,
    ).astype("int64")


if __name__ == "__main__":
    tips = pd.DataFrame(TIPS)
    tips["day"] = pd.Categorical(tips["day"], categories=DAYS, ordered=True)
    tips["time"] = pd.Categorical(tips["time"], categories=TIMES, ordered=True)

    print(f"{len(tips)} rows, day={list(tips['day'].cat.categories)}, "
          f"time={list(tips['time'].cat.categories)}\n")

    print("Mean total_bill by day and time")
    print(mean_bill_pivot(tips).to_string())

    print("\nOrder count by day and time")
    print(order_count_pivot(tips).to_string())

    counts = order_count_pivot(tips)
    print(f"\ncount pivot dtypes: {counts.dtypes.unique().tolist()}, "
          f"grand total = {counts.to_numpy().sum()}")
