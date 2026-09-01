"""exercise-04-groupby.py — a Saturday sales summary by department.

Computes revenue per line item, then aggregates by category with
totals, averages, unit counts, and share of the day's revenue.
"""

import pandas as pd

SALES: dict[str, list] = {
    "item": [
        "Interior latex gallon", "Painter's tape", "Roller kit", "Primer quart",
        "Claw hammer", "Cordless drill", "Tape measure",
        "Potting soil", "Pruning shears", "Garden hose 50ft",
        "Deck screws box", "Wall anchors",
    ],
    "category": [
        "Paint", "Paint", "Paint", "Paint",
        "Tools", "Tools", "Tools",
        "Garden", "Garden", "Garden",
        "Fasteners", "Fasteners",
    ],
    "units":      [14, 40, 22, 19, 9, 5, 18, 30, 12, 7, 25, 33],
    "unit_price": [32.50, 4.25, 11.75, 13.25, 18.99, 89.00, 12.50,
                   8.99, 21.50, 34.00, 15.25, 6.40],
}


def main() -> None:
    """Print the line items and four views of the aggregated day."""
    df = pd.DataFrame(SALES)

    df["revenue"] = (df["units"] * df["unit_price"]).round(2)
    print("--- rows ---")
    print(df)

    print("--- revenue per category ---")
    print(df.groupby("category")["revenue"].sum())

    summary = df.groupby("category").agg(
        total_revenue=("revenue", "sum"),
        avg_revenue=("revenue", "mean"),
        units_sold=("units", "sum"),
        line_items=("item", "size"),
    ).round(2)
    print("--- named aggregations ---")
    print(summary)

    ranked = summary.sort_values("total_revenue", ascending=False)
    print("--- ranked by total ---")
    print(ranked)

    print("--- ranked by average ---")
    print(summary.sort_values("avg_revenue", ascending=False))

    grand_total = summary["total_revenue"].sum()
    print(f"Grand total: ${grand_total:,.2f}")

    share = (ranked["total_revenue"] / grand_total * 100).round(1)
    print("--- share of total ---")
    print(share)

    best = df.loc[
        df.groupby("category")["revenue"].idxmax(),
        ["category", "item", "revenue"],
    ]
    print("--- best line item per category ---")
    print(best)


if __name__ == "__main__":
    main()
