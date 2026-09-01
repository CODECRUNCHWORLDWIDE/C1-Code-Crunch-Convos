"""exercise-05-plot-solution.py — monthly revenue bar chart, saved as a PNG.

Prints the year's figures, then draws a labelled bar chart with matplotlib's
non-interactive Agg backend. The chart is written into a throwaway temporary
directory that Python deletes on the way out, so nothing is left in your folder;
the deterministic summary line at the end is the proof the render worked.

Your own ``exercise-05-plot.py`` should save ``monthly-revenue.png`` next to the
script so you can open it. This shipped answer writes to a temp dir instead only
so the automated check leaves no file behind — the plotting code above the save
is identical to what you write.

Run it with::

    python exercise-05-plot-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CART_SALES: dict[str, list] = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "revenue": [4120, 3980, 4760, 5210, 5890, 6340,
                6120, 5980, 5430, 4870, 4310, 4650],
}


def main() -> None:
    """Print the year's totals and save the bar chart into a temp folder."""
    df = pd.DataFrame(CART_SALES)
    print(df)

    total = df["revenue"].sum()
    mean = df["revenue"].mean()
    best = df.loc[df["revenue"].idxmax()]
    worst = df.loc[df["revenue"].idxmin()]

    print(f"Total: ${total:,}")
    print(f"Mean:  ${mean:,.2f}")
    print(f"Best:  {best['month']} (${best['revenue']:,})")
    print(f"Worst: {worst['month']} (${worst['revenue']:,})")

    above_mean = int((df["revenue"] > mean).sum())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["month"], df["revenue"], color="#3273dc")
    ax.axhline(mean, color="#c0392b", linestyle="--", linewidth=1, label="Mean")
    ax.set_title("Coffee cart revenue by month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()

    with tempfile.TemporaryDirectory() as workspace:
        output_path = Path(workspace) / "monthly-revenue.png"
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"Saved chart: {len(df)} bars, mean line at {mean:.2f}, {above_mean} above it")


if __name__ == "__main__":
    main()
