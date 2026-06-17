"""Exercise 05 — Bar chart of monthly totals, saved as a PNG.

Goal
----
Given a year of fake monthly revenue, produce one bar chart with:

- A clear title.
- Labelled X and Y axes (with units).
- Sensible figure size.
- Saved to `monthly_revenue.png` at 150 DPI.

How to run
----------
    python exercise-05-plot.py

After the script runs, open `monthly_revenue.png` from the same directory
to view your chart.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_FILE: Path = Path(__file__).parent / "monthly_revenue.png"


def build_monthly_revenue() -> pd.DataFrame:
    """Return one year of fake monthly revenue (in USD)."""
    data: dict[str, list] = {
        "month": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ],
        "revenue": [
            12_500, 11_300, 14_200, 13_800, 15_100, 18_400,
            21_300, 22_900, 17_600, 16_800, 19_200, 24_500,
        ],
    }
    return pd.DataFrame(data)


def plot_monthly_revenue(df: pd.DataFrame, output: Path) -> None:
    """Create a bar chart of monthly revenue and save it to disk.

    Steps:
      1. Make a figure and axes with `plt.subplots(figsize=...)`.
      2. Use `ax.bar(...)` (or `df.plot.bar(ax=ax)`) to draw the bars.
      3. Set title, xlabel, ylabel.
      4. Save the figure to `output` with `fig.savefig(...)`.
    """
    # YOUR CODE HERE
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["month"], df["revenue"], color="#3273dc")
    ax.set_title("Monthly Revenue — FY 2025")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (USD)")
    ax.grid(True, axis="y", alpha=0.3)

    # Label each bar with its value (a nice touch — optional).
    for rect, value in zip(ax.patches, df["revenue"]):
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height(),
            f"${value/1000:.1f}k",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = build_monthly_revenue()

    print("\nMonthly revenue data:")
    print(df.to_string(index=False))
    print(f"\nTotal for the year: ${df['revenue'].sum():,}")
    print(f"Best month: {df.loc[df['revenue'].idxmax(), 'month']}")

    plot_monthly_revenue(df, OUTPUT_FILE)

    assert OUTPUT_FILE.exists(), f"Expected {OUTPUT_FILE} to be created"
    print(f"\nChart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
