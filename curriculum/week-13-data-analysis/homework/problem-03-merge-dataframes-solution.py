"""hw-03-merge.py — left-join orders to customers, report and fill the misses.

The merged table is written to a throwaway temporary directory that Python
deletes on the way out, then printed, so the script leaves nothing behind.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd


def build_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """The two frames exactly as the homework specifies them."""
    orders = pd.DataFrame({
        "order_id":    [101, 102, 103, 104, 105],
        "customer_id": [1, 2, 1, 3, 99],
        "amount":      [50.0, 75.0, 20.0, 120.0, 9.0],
    })
    customers = pd.DataFrame({
        "customer_id": [1, 2, 3, 4],
        "name":        ["Ada", "Linus", "Grace", "Tim"],
        "country":     ["UK", "FI", "US", "GB"],
    })
    return orders, customers


def main() -> None:
    orders, customers = build_frames()

    # 1. Left join: every order survives, matched or not.
    merged = orders.merge(customers, on="customer_id", how="left", indicator=True)
    print("After the left join:")
    print(merged.to_string(index=False))

    # 2. How many orders failed to match a customer?
    unmatched = merged["_merge"].eq("left_only")
    print(f"\nOrders with no matching customer: {unmatched.sum()}")
    print(merged.loc[unmatched, ["order_id", "customer_id", "amount"]]
                .to_string(index=False))

    # 3. Fill the gaps left by the join.
    merged = merged.drop(columns="_merge")
    merged[["name", "country"]] = merged[["name", "country"]].fillna("UNKNOWN")
    print("\nAfter filling:")
    print(merged.to_string(index=False))
    print("\nRemaining missing values:", int(merged.isna().sum().sum()))

    # 4. Save to a temp dir, print it back, and let it be cleaned up.
    with tempfile.TemporaryDirectory() as workspace:
        out = Path(workspace) / "merged.csv"
        merged.to_csv(out, index=False)
        print(f"\nwrote {out.name}")
        print(out.read_text().rstrip())


if __name__ == "__main__":
    main()
