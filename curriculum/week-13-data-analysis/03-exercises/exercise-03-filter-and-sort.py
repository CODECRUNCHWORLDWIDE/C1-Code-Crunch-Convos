"""Exercise 03 — Filter and sort a DataFrame of student grades.

Goal
----
You have a small DataFrame of students with their `score` (out of 100) and
`subject`. Practise four core moves:

1. Build the DataFrame from an inline dictionary.
2. Filter to keep only **passing** rows (score >= 60).
3. Sort the passers from highest to lowest score.
4. Show the top three.

How to run
----------
    python exercise-03-filter-and-sort.py

You should see three tables printed: the original frame, the passers, and
the top three. Fill in the `# YOUR CODE HERE` blocks.
"""

from __future__ import annotations

import pandas as pd


PASS_MARK: int = 60


def build_students() -> pd.DataFrame:
    """Return a small DataFrame of made-up student grades."""
    data: dict[str, list] = {
        "name": [
            "Ada", "Linus", "Grace", "Tim", "Margaret",
            "Dennis", "Barbara", "Hedy", "Alan", "Katherine",
        ],
        "subject": [
            "Math", "Math", "Math", "Math", "Math",
            "Science", "Science", "Science", "Science", "Science",
        ],
        "score": [92, 58, 75, 49, 88, 67, 95, 54, 71, 82],
    }
    return pd.DataFrame(data)


def keep_passers(df: pd.DataFrame, pass_mark: int = PASS_MARK) -> pd.DataFrame:
    """Return only rows where score is at least `pass_mark`.

    Uses a boolean mask. The result is a new DataFrame — the input is
    unchanged.
    """
    # YOUR CODE HERE
    return df[df["score"] >= pass_mark]


def sort_by_score_desc(df: pd.DataFrame) -> pd.DataFrame:
    """Sort the DataFrame from highest to lowest score."""
    # YOUR CODE HERE
    return df.sort_values("score", ascending=False)


def top_n(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Return the top `n` rows of an already-sorted DataFrame."""
    # YOUR CODE HERE
    return df.head(n)


def main() -> None:
    students = build_students()

    print("\nAll students:")
    print(students.to_string(index=False))

    passers = keep_passers(students)
    print(f"\nPassers (score >= {PASS_MARK}):  {len(passers)} of {len(students)}")
    print(passers.to_string(index=False))

    ranked = sort_by_score_desc(passers)
    print("\nPassers sorted by score (high → low):")
    print(ranked.to_string(index=False))

    leaders = top_n(ranked, 3)
    print("\nTop 3:")
    print(leaders.to_string(index=False))

    # Sanity checks the script enforces against your code:
    assert (passers["score"] >= PASS_MARK).all(), "keep_passers let a fail through!"
    assert ranked["score"].is_monotonic_decreasing, "sort_by_score_desc not descending!"
    assert len(leaders) == 3, "top_n should return 3 rows"
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
