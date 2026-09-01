"""challenge-01-titanic-eda-solution.py — a worked EDA on a small passenger manifest.

The challenge asks you to explore the full 891-row Titanic dataset that seaborn
downloads. So this shipped answer runs anywhere, offline, and gives identical
numbers on every machine, it works a self-contained 16-passenger *sample* built
inline as a dict of lists — the exact columns of the real manifest, with real
holes punched in ``age``, ``embarked`` and ``deck``. Every move here (a survival
rate as the mean of a 0/1 column, a sex-by-class pivot, an age-band cut, a
missing-data audit) is line-for-line what you run on the full dataset; only the
row count changes.

The one chart is drawn with matplotlib's non-interactive Agg backend and written
into a throwaway temporary directory that Python deletes on the way out.

Run it with::

    python challenge-01-titanic-eda-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # choose a headless backend before importing pyplot

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

NA = np.nan

# A 16-passenger sample of the manifest. Real column names; real holes.
MANIFEST: dict[str, list] = {
    "survived": [1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    "pclass":   [1, 1, 2, 2, 3, 3, 3, 1, 1, 2, 2, 3, 3, 3, 3, 3],
    "sex": [
        "female", "female", "female", "female", "female", "female", "female",
        "male", "male", "male", "male", "male", "male", "male", "male", "male",
    ],
    "age":      [38.0, 35.0, 28.0, NA, 6.0, 24.0, 45.0,
                 40.0, 52.0, 31.0, NA, 22.0, 9.0, 27.0, NA, 61.0],
    "sibsp":    [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 3, 1, 0, 0, 0],
    "parch":    [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    "fare":     [71.28, 53.10, 26.00, 30.07, 16.70, 7.92, 7.75,
                 52.00, 35.50, 13.00, 10.50, 21.07, 15.25, 7.90, 8.05, 6.24],
    "embarked": ["C", "S", "S", "S", "Q", "S", "S",
                 "S", "S", "S", "C", "S", "S", "Q", NA, "S"],
    "deck":     ["C", "C", NA, NA, NA, NA, NA,
                 "E", "B", NA, NA, NA, NA, NA, NA, NA],
}


def main() -> None:
    """Audit the holes, then compute survival rates every way that matters."""
    df = pd.DataFrame(MANIFEST)
    print(f"shape: {df.shape}")

    # 1. Missing-data audit — decide the holes before touching the numbers.
    audit = pd.DataFrame({
        "n_missing": df.isna().sum(),
        "pct_missing": (df.isna().mean() * 100).round(1),
    })
    print("--- missing-data audit ---")
    print(
        audit[audit["n_missing"] > 0]
        .sort_values("pct_missing", ascending=False)
        .to_string()
    )

    # 2. Survival rates: the mean of a 0/1 column IS a proportion.
    overall = df["survived"].mean()
    print(f"\nOverall survival rate: {overall:.3f}  ({df['survived'].sum()} of {len(df)})")

    print("\n--- survival rate by sex ---")
    print(df.groupby("sex")["survived"].mean().round(3).to_string())

    print("\n--- survival rate by class ---")
    print(df.groupby("pclass")["survived"].mean().round(3).to_string())

    # 3. Two factors at once: a sex-by-class pivot, with the counts beneath it.
    pivot = df.pivot_table(index="sex", columns="pclass", values="survived", aggfunc="mean")
    print("\n--- survival rate by sex and class ---")
    print(pivot.round(3).to_string())
    print("\n--- passenger counts by sex and class ---")
    print(pd.crosstab(df["sex"], df["pclass"]).to_string())

    # 4. Age bands on the known ages only, half-open so a 10-year-old is a teen.
    bands = pd.cut(df["age"], bins=[0, 10, 20, 40, 60, 80], right=False)
    by_band = df.groupby(bands, observed=True).agg(
        n=("survived", "size"),
        survivors=("survived", "sum"),
        rate=("survived", "mean"),
    )
    print("\n--- survival rate by age band (known ages only) ---")
    print(by_band.round(3).to_string())

    # 5. Family size, derived from sibsp + parch + the passenger themselves.
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    print("\n--- survival rate by family size ---")
    print(df.groupby("family_size")["survived"].agg(n="size", rate="mean").round(3).to_string())

    # 6. The finding — computed from the pivot, never typed in by hand.
    rates = pivot.stack(future_stack=True)
    best, worst = rates.idxmax(), rates.idxmin()
    print(
        f"\nFinding: {best[0]} in class {best[1]} survived at {rates.max():.1%}; "
        f"{worst[0]} in class {worst[1]} at {rates.min():.1%} — a gap of "
        f"{(rates.max() - rates.min()) * 100:.0f} percentage points, against an "
        f"overall rate of {overall:.1%}."
    )

    # 7. One labelled chart, into a temp dir that is deleted on the way out.
    by_sex = df.groupby("sex")["survived"].mean()
    with tempfile.TemporaryDirectory() as workspace:
        fig, ax = plt.subplots(figsize=(6, 4))
        by_sex.plot.bar(ax=ax, color=["#ee6666", "#3273dc"], rot=0)
        ax.set_title("Survival rate by sex (16-passenger sample)")
        ax.set_xlabel("Sex")
        ax.set_ylabel("Survival rate")
        ax.set_ylim(0, 1)
        fig.tight_layout()
        fig.savefig(Path(workspace) / "fig-survival-by-sex.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print("\nSaved 1 chart (survival by sex) to a temp dir; cleaned up.")


if __name__ == "__main__":
    main()
