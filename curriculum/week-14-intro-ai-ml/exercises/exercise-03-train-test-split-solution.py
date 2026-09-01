"""exercise-03-train-test-split.py — how much does the split move the score?

Holds the model fixed and varies only the train/test split.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

MODEL_SEED = 42
TEST_SIZE = 0.30
SPLIT_SEEDS = range(10)


def score_one_split(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> float:
    """Split with the given seed, fit, and return test accuracy.

    Passing None for split_seed leaves the split unseeded on purpose.
    """
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=split_seed, stratify=y
    )
    model = LogisticRegression(max_iter=1000, random_state=MODEL_SEED)
    model.fit(x_train, y_train)
    return float(model.score(x_test, y_test))


def test_row_labels(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> list[int]:
    """Return the original row numbers that landed in the test set."""
    _, x_test, _, _ = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=split_seed, stratify=y
    )
    return sorted(x_test.index)


def main() -> None:
    """Print the spread across seeds, then prove reproducibility both ways."""
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    scores: list[float] = []
    print("--- one model, ten different splits ---")
    for seed in SPLIT_SEEDS:
        accuracy = score_one_split(x, y, seed)
        scores.append(accuracy)
        print(f"seed {seed:2d} -> {accuracy:.3f}")

    print(f"lowest : {min(scores):.3f}")
    print(f"highest: {max(scores):.3f}")
    print(f"spread : {max(scores) - min(scores):.3f}")
    print(f"mean   : {sum(scores) / len(scores):.3f}")

    print("--- reproducibility ---")
    pinned_a = test_row_labels(x, y, 42)
    pinned_b = test_row_labels(x, y, 42)
    print(f"seed=42 twice, same test rows?  {pinned_a == pinned_b}")

    loose_a = test_row_labels(x, y, None)
    loose_b = test_row_labels(x, y, None)
    print(f"unseeded twice, same test rows? {loose_a == loose_b}")


if __name__ == "__main__":
    main()
