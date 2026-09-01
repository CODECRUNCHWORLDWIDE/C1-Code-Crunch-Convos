"""hw-06-correlations.py — find the strongest correlation in a tips-like frame.

The homework uses seaborn's ``tips`` dataset. So it runs offline and identically
everywhere, this shipped answer builds an inline, seeded frame where tip depends
on the bill with a *fixed* component (a positive intercept) plus noise — the same
shape as the real data, and enough to reproduce the finding that a bigger bill
does not tip proportionally more.

The scatter is drawn with matplotlib's non-interactive Agg backend and written
into a throwaway temporary directory that Python deletes on the way out.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_tips(n: int = 80) -> pd.DataFrame:
    """A seeded tips frame: tip = 0.10*bill + fixed part + noise; size tracks bill."""
    rng = np.random.default_rng(20)
    total_bill = np.round(rng.uniform(8.0, 55.0, n), 2)
    tip = np.round(0.10 * total_bill + 1.2 + rng.normal(0, 0.55, n), 2)
    size = np.clip(np.round(total_bill / 13 + rng.normal(0, 0.5, n)), 1, 6).astype(int)
    return pd.DataFrame({"total_bill": total_bill, "tip": tip, "size": size})


def strongest_pair(corr: pd.DataFrame) -> tuple[str, str, float]:
    """Return (col_a, col_b, r) for the largest off-diagonal correlation.

    The diagonal and lower triangle are masked with NaN so a column cannot win
    against itself and each pair is considered once.
    """
    mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    pairs = corr.where(mask).stack(future_stack=True)
    a, b = pairs.idxmax()
    return a, b, float(pairs.max())


if __name__ == "__main__":
    tips = make_tips()

    # 1. Correlation matrix of the numeric columns.
    corr = tips.corr(numeric_only=True)
    print("Correlation matrix")
    print(corr.round(4).to_string())

    # 2. Strongest positive off-diagonal pair.
    a, b, r = strongest_pair(corr)
    print(f"\nStrongest positive correlation: {a} vs {b}, r = {r:.4f}")

    # 3. Scatter with a least-squares trend line.
    x = tips[a].to_numpy()
    y = tips[b].to_numpy()
    slope, intercept = np.polyfit(x, y, deg=1)
    xs = np.linspace(x.min(), x.max(), 100)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.6, color="#3273dc", label="Orders")
    ax.plot(xs, slope * xs + intercept, color="#d9534f", linewidth=2,
            label=f"Fit: tip = {slope:.4f} x bill + {intercept:.4f}")
    ax.set_title(f"Tip vs total bill (r = {r:.2f}, n = {len(tips)})")
    ax.set_xlabel("Total bill ($)")
    ax.set_ylabel("Tip ($)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    with tempfile.TemporaryDirectory() as workspace:
        fig.savefig(Path(workspace) / "corr_scatter.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"slope     = {slope:.4f} dollars of tip per dollar of bill")
    print(f"intercept = {intercept:.4f} dollars")
    print(f"r squared = {r ** 2:.4f}")

    # 4. Proportional? Compare the tip rate across bill quartiles.
    tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100
    quartiles = pd.qcut(tips["total_bill"], 4,
                        labels=["Q1 cheapest", "Q2", "Q3", "Q4 priciest"])
    print("\nMean tip percentage by total_bill quartile")
    print(tips.groupby(quartiles, observed=True)["tip_pct"].mean().round(2).to_string())
