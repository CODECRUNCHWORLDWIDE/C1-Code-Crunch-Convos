"""challenge-02-time-series-solution.py — resample and rolling mean on a year of sales.

Generates a full year of synthetic daily sales with a *known* structure — a
weekly cycle, a gentle upward trend, and Gaussian noise — then uses resample and
rolling to recover the trend and the weekly rhythm that the raw daily line
hides. Because the random generator is seeded, every number below is exactly
reproducible on any machine, with nothing downloaded.

The two charts are drawn with matplotlib's non-interactive Agg backend and
written into a throwaway temporary directory that Python deletes on the way out,
so the script leaves nothing behind.

Run it with::

    python challenge-02-time-series-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # choose a headless backend before importing pyplot

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_sales() -> pd.Series:
    """Return 366 days of 2024 sales: weekly cycle + upward trend + noise."""
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    baseline = 1000 + 300 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    trend = np.linspace(0, 400, len(dates))
    noise = rng.normal(0, 80, len(dates))
    return pd.Series((baseline + trend + noise).round(2), index=dates, name="sales")


def main() -> None:
    """Inspect, resample, roll, and measure the recovered structure."""
    sales = build_sales()

    print("--- head ---")
    print(sales.head())
    print(f"\n{len(sales)} days, {sales.index.min().date()} to {sales.index.max().date()}")

    print("\n--- describe ---")
    print(sales.describe().round(2).to_string())

    monthly = sales.resample("ME").sum()
    print("\n--- monthly totals ---")
    print(monthly.round(2).to_string())
    print(f"\nHighest month: {monthly.idxmax():%B %Y} at {monthly.max():,.2f}")

    rolling7 = sales.rolling(window=7, min_periods=1).mean()
    print("\n--- rolling-mean checks ---")
    print(f"first: {rolling7.iloc[0]:.2f} == day 1 value {sales.iloc[0]:.2f}")
    print(f"day 7: {rolling7.iloc[6]:.2f} == mean of days 1-7 {sales.iloc[:7].mean():.2f}")
    print(f"rolling mean day 1  : {rolling7.iloc[0]:.2f}")
    print(f"rolling mean day 366: {rolling7.iloc[-1]:.2f}")
    print(f"lift across the year: {rolling7.iloc[-1] - rolling7.iloc[0]:+.2f}")

    detrended = sales - rolling7
    by_dow = detrended.groupby(detrended.index.day_name()).mean()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_dow = by_dow.reindex(order)
    print("\n--- weekly seasonality (detrended, by weekday) ---")
    print(by_dow.round(2).to_string())
    print(f"\npeak {by_dow.idxmax()} {by_dow.max():+.2f}, trough {by_dow.idxmin()} {by_dow.min():+.2f}")
    print(f"peak-to-trough swing: {by_dow.max() - by_dow.min():,.2f}")

    with tempfile.TemporaryDirectory() as workspace:
        out = Path(workspace)

        fig, ax = plt.subplots(figsize=(12, 5))
        sales.plot(ax=ax, label="Daily", alpha=0.4, color="#3273dc")
        rolling7.plot(ax=ax, label="7-day rolling mean", linewidth=2, color="#d9534f")
        ax.set_title("Daily sales with 7-day rolling mean, 2024")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales (units)")
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "fig-daily-rolling.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(monthly.index.strftime("%b"), monthly.values, color="#3273dc")
        ax.set_title("Monthly sales totals, 2024")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total sales (units)")
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "fig-monthly-totals.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print("\nSaved 2 charts (daily+rolling, monthly totals) to a temp dir; cleaned up.")


if __name__ == "__main__":
    main()
