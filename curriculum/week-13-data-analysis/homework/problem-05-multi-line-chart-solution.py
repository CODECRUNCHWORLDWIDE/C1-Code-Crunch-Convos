"""hw-05-multi-line.py — one chart, three product lines, twelve months, saved to PNG.

The data is fabricated inline with a seeded generator, so every printed number
is reproducible. The chart is drawn with matplotlib's non-interactive Agg backend
and written into a throwaway temporary directory that Python deletes on the way
out, so the script leaves no PNG behind.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_sales() -> pd.DataFrame:
    """Fabricate 12 months of sales for three products. Seeded, so reproducible.

    Alpha grows steadily, Beta is flat and seasonal, Gamma decays.
    """
    rng = np.random.default_rng(13)
    months = pd.period_range("2025-01", periods=12, freq="M")
    n = np.arange(12)

    data = {
        "Alpha": 420 + 28 * n + rng.normal(0, 18, 12),
        "Beta": 610 + 90 * np.sin(2 * np.pi * n / 12) + rng.normal(0, 18, 12),
        "Gamma": 780 * 0.93**n + rng.normal(0, 18, 12),
    }
    monthly = pd.DataFrame(data, index=months).round(1)
    monthly.index.name = "month"
    return monthly


def plot(monthly: pd.DataFrame) -> None:
    """Draw one line per column on shared axes and save into a temp dir."""
    # Plot against short month names, not the PeriodIndex. A PeriodIndex puts
    # the lines at period *ordinals* (660..671 for 2025), so hand-set ticks at
    # 0..11 would land outside the axes and vanish.
    plot_df = monthly.copy()
    plot_df.index = monthly.index.strftime("%b")

    fig, ax = plt.subplots(figsize=(10, 5))
    plot_df.plot(ax=ax, marker="o", linewidth=2)

    ax.set_title("Monthly unit sales by product, 2025")
    ax.set_xlabel("Month")
    ax.set_ylabel("Units sold")
    ax.set_ylim(0, None)
    # Now that x runs 0..11, forcing a tick per month is safe.
    ax.set_xticks(range(len(plot_df)))
    ax.set_xticklabels(plot_df.index)
    ax.legend(title="Product")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    with tempfile.TemporaryDirectory() as workspace:
        fig.savefig(Path(workspace) / "multi_line.png", dpi=150, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    monthly = make_sales()
    print(monthly.to_string())
    print("\nfull-year totals")
    print(monthly.sum().round(1).to_string())
    plot(monthly)
    print("\nsaved multi_line.png: 3 product lines across 12 months (temp file, cleaned up)")
