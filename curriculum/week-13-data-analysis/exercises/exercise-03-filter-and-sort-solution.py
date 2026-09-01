"""exercise-03-filter-and-sort.py — who passed, and in what order.

Filters a cohort DataFrame by score and produces a ranked pass list.
"""

import pandas as pd

PASSING_SCORE = 70

COHORT: dict[str, list] = {
    "learner": [
        "Amara", "Bo", "Chen", "Dalia", "Emeka", "Farrah",
        "Gustavo", "Hana", "Idris", "Jo", "Kiran", "Lena",
    ],
    "session": [
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
        "Tuesday", "Thursday", "Tuesday", "Thursday", "Tuesday", "Thursday",
    ],
    "score":   [88, 64, 70, 95, 52, 79, 70, 91, 45, 83, 68, 76],
    "minutes": [240, 90, 150, 310, 60, 200, 175, 285, 45, 220, 130, 190],
}


def main() -> None:
    """Print the cohort, the passers, the ranking, and two means."""
    df = pd.DataFrame(COHORT)
    print("--- all rows ---")
    print(df)

    passing = df[df["score"] >= PASSING_SCORE].copy()
    print("--- passing ---")
    print(passing)
    print(f"Passed: {len(passing)} of {len(df)}")

    ranked = passing.sort_values(
        ["score", "minutes"], ascending=False
    ).reset_index(drop=True)
    print("--- ranked ---")
    print(ranked)

    top = ranked.iloc[0]
    print(f"Top scorer: {top['learner']} with {top['score']}")

    tuesday_pass = df[
        (df["score"] >= PASSING_SCORE) & (df["session"] == "Tuesday")
    ].copy()
    print("--- Tuesday passers ---")
    print(tuesday_pass)

    print(f"Mean score, all: {df['score'].mean():.2f}")
    print(f"Mean score, passing: {passing['score'].mean():.2f}")


if __name__ == "__main__":
    main()
