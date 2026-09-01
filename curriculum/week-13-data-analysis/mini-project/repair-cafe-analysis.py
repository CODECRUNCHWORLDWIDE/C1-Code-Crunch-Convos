"""repair-cafe-analysis.py — the finished answer to the Week 13 mini-project.

The whole six-step pipeline the project asks for — Load, Inspect, Clean,
Analyze, Visualize, Conclude — worked all the way through on the repair-café
log that ``starter.md`` ships. Every TODO in the starter is done here.

Your own deliverable is a notebook, ``analysis.ipynb``, plus ``findings.md``,
``requirements.txt`` and ``figures/main.png``. A notebook cannot be run by a
plain ``python`` command, so the reference answer ships as this script: same
data, same steps, same numbers, one cell after another turned into one section
after another. Read it top to bottom and you are reading the finished notebook.

Two small differences, both so the download proves itself and leaves nothing
behind. It renders with matplotlib's non-interactive ``Agg`` backend, so no
window is ever opened. And it writes its three charts into a ``figures/`` folder
inside a throwaway temporary directory that Python deletes on the way out, then
prints what it saved. Your notebook saves into a real ``figures/`` beside it, so
you can open the pictures.

Run it with::

    python repair-cafe-analysis.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May"]

# The log five volunteers filled in by hand, one row per category per session.
# Replace this with pd.read_csv("your-data.csv", parse_dates=["date"]) when you
# bring your own dataset. One blank cell is left in on purpose: real logs have
# gaps, and the Clean step is where you decide what to do about them.
REPAIR_LOG: dict[str, list] = {
    "date": [
        "2024-01-06", "2024-01-06", "2024-01-06",
        "2024-02-03", "2024-02-03", "2024-02-03",
        "2024-03-02", "2024-03-02", "2024-03-02",
        "2024-04-06", "2024-04-06", "2024-04-06",
        "2024-05-04", "2024-05-04", "2024-05-04",
    ],
    "category": [
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
    ],
    "items_in": [22, 15, 11, 26, 18, 14, 31, 21, 19,
                 28, 24, 23, 35, 27, 26],
    "items_fixed": [14, 12, 9, 15, 15, 12, 20, 18, 16,
                    17, 21, 20, 21, 23, 22],
    "volunteer_hours": [18.0, 9.0, 12.0, 20.0, 10.5, 15.0,
                        24.0, None, 19.5, 22.0, 13.5, 21.0,
                        26.0, 15.0, 24.0],
}


def load() -> pd.DataFrame:
    """Step 1 — get the table into memory and look at the first few rows."""
    return pd.DataFrame(REPAIR_LOG)


def inspect(df: pd.DataFrame) -> None:
    """Step 2 — shape, dtypes, the missing-data audit, and the summary stats."""
    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum())
    print(df.describe().round(2))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3 — fix the dtypes, fill the one gap, add the derived columns.

    The gap is filled with the median rather than the mean because one
    unusually long session would drag a mean and cannot drag a median. It is
    filled rather than dropped because that row still has good ``items_in`` and
    ``items_fixed`` numbers, and throwing five columns away to avoid one blank
    cell costs real data.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%b")
    df["volunteer_hours"] = df["volunteer_hours"].fillna(
        df["volunteer_hours"].median()
    )
    df["fix_rate"] = (df["items_fixed"] / df["items_in"]).round(3)
    return df


def summarise_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4a — one row per repair category, totalled.

    ``fix_rate`` here is total fixed over total in, not the average of the
    per-session rates. A mean of ratios weights an 11-item session the same as
    a 35-item one, which is not the number anybody wants.
    """
    by_category = df.groupby("category").agg(
        sessions=("items_in", "size"),
        items_in=("items_in", "sum"),
        items_fixed=("items_fixed", "sum"),
        hours=("volunteer_hours", "sum"),
    )
    by_category["fix_rate"] = (
        by_category["items_fixed"] / by_category["items_in"]
    ).round(3)
    by_category["per_hour"] = (
        by_category["items_fixed"] / by_category["hours"]
    ).round(2)
    return by_category


def summarise_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4b — repairs per month per category, months in calendar order.

    ``pivot_table`` sorts its index, and "Apr" sorts before "Jan", so the
    ``reindex`` is what puts the year back in the order a reader expects.
    """
    return df.pivot_table(
        index="month",
        columns="category",
        values="items_fixed",
        aggfunc="sum",
    ).reindex(MONTH_ORDER)


def headline(df: pd.DataFrame) -> None:
    """Step 4c — the five numbers the conclusion is allowed to lean on."""
    items_in = df["items_in"].sum()
    items_fixed = df["items_fixed"].sum()
    hours = df["volunteer_hours"].sum()

    print(f"Sessions logged:      {len(df)}")
    print(f"Items brought in:     {items_in}")
    print(f"Items repaired:       {items_fixed}")
    print(f"Overall fix rate:     {items_fixed / items_in:.1%}")
    print(f"Volunteer hours:      {hours:.2f}")
    print(f"Repairs per hour:     {items_fixed / hours:.2f}")


def draw_charts(df: pd.DataFrame, by_category: pd.DataFrame,
                figure_dir: Path) -> pd.DataFrame:
    """Step 5 — three labelled charts, each saved and each announced.

    Returns the month-by-month totals, because the second chart has to compute
    them and the conclusion wants to quote them.
    """
    figure_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(by_category.index, by_category["items_fixed"], color="#3273dc")
    ax.set_title("Items repaired by category, Jan–May 2024")
    ax.set_xlabel("Category")
    ax.set_ylabel("Items repaired (count)")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "main.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/main.png")

    monthly = df.groupby("month", sort=False)[["items_in", "items_fixed"]].sum()
    print(monthly)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly.index, monthly["items_in"], marker="o", label="Brought in")
    ax.plot(monthly.index, monthly["items_fixed"], marker="o", label="Repaired")
    ax.set_title("Intake and repairs by month, Jan–May 2024")
    ax.set_xlabel("Month")
    ax.set_ylabel("Items (count)")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "monthly-trend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/monthly-trend.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(by_category.index, by_category["fix_rate"], color="#27ae60")
    ax.set_title("Share of items sent home working, by category")
    ax.set_xlabel("Fix rate (share of items brought in)")
    ax.set_ylabel("Category")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "fix-rate.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/fix-rate.png")

    return monthly


def conclude(by_category: pd.DataFrame, monthly: pd.DataFrame) -> None:
    """Step 6 — three sentences, every one of them carrying a number."""
    best = by_category["per_hour"].idxmax()
    print(
        f"{best} give the community the most back per volunteer hour: "
        f"{by_category.loc[best, 'per_hour']:.2f} repaired items an hour, "
        f"against {by_category.loc['Bicycles', 'per_hour']:.2f} for bicycles "
        f"and {by_category.loc['Electronics', 'per_hour']:.2f} for electronics."
    )
    print(
        "Electronics is also the hardest category to fix at all, sending home "
        f"{by_category.loc['Electronics', 'fix_rate']:.1%} of what arrives "
        f"against {by_category.loc['Textiles', 'fix_rate']:.1%} for textiles."
    )
    first, last = monthly.index[0], monthly.index[-1]
    print(
        f"Intake climbed from {monthly.loc[first, 'items_in']} items in {first} "
        f"to {monthly.loc[last, 'items_in']} in {last} while repairs climbed "
        f"from {monthly.loc[first, 'items_fixed']} to "
        f"{monthly.loc[last, 'items_fixed']}, so the cafe is getting busier "
        "rather than better."
    )
    print(
        "Both numbers rising together is a pattern, not a cause: five sessions "
        "cannot tell us whether word of mouth, the weather or the new tool "
        "wall brought people in."
    )


def main() -> None:
    """Run the whole pipeline and narrate each step."""
    print("Repair Cafe Analysis — the Week 13 mini-project, end to end.")

    print()
    print("1. Load")
    df = load()
    print(df.head())

    print()
    print("2. Inspect")
    inspect(df)

    print()
    print("3. Clean")
    df = clean(df)
    print(df.dtypes)
    print(df[["date", "category", "month", "volunteer_hours", "fix_rate"]].head())

    print()
    print("4. Analyze")
    by_category = summarise_by_category(df)
    print(by_category)
    print(summarise_by_month(df))
    headline(df)

    print()
    print("5. Visualize")
    with tempfile.TemporaryDirectory() as workspace:
        monthly = draw_charts(df, by_category, Path(workspace) / "figures")

    print()
    print("6. Conclude")
    conclude(by_category, monthly)


if __name__ == "__main__":
    main()
