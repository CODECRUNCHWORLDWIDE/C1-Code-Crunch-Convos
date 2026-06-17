"""Exercise 03 — Train/test split: why random_state matters.

Goals:
  * Show that a single train/test score is noisier than you'd think.
  * Demonstrate that random_state controls reproducibility.
  * Introduce cross-validation as a more honest estimate.

Run:
    python exercise-03-train-test-split.py
"""

from __future__ import annotations

import statistics

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split


def score_with_seed(X, y, seed: int) -> float:
    """Train logistic regression once with the given random_state, return accuracy."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return float(model.score(X_test, y_test))


def main() -> None:
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target

    print("Same model, same data, different random_state values:")
    seeds = list(range(10))
    scores: list[float] = []
    for seed in seeds:
        acc = score_with_seed(X, y, seed)
        scores.append(acc)
        print(f"  random_state={seed:2d}  accuracy={acc:.4f}")

    print()
    print(f"min   accuracy : {min(scores):.4f}")
    print(f"max   accuracy : {max(scores):.4f}")
    print(f"mean  accuracy : {statistics.mean(scores):.4f}")
    print(f"stdev accuracy : {statistics.stdev(scores):.4f}")

    print(
        "\nObservation: even on iris, the score varies a few percent depending\n"
        "on which examples land in the test set. A single split lies. Always set\n"
        "random_state for reproducibility, and use cross-validation for honest\n"
        "estimates.\n"
    )

    # Cross-validation: same idea automated.
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=1000),
        X,
        y,
        cv=5,
        scoring="accuracy",
    )
    print(f"5-fold cross-validation scores: {cv_scores}")
    print(f"  mean = {cv_scores.mean():.4f}, std = {cv_scores.std():.4f}")

    print(
        "\nTry this next:\n"
        "  - Repeat the seed loop with test_size=0.5 (a 50/50 split).\n"
        "    The spread should grow. Why?\n"
        "  - Try cv=10 instead of cv=5. Does the mean change? The std?\n"
    )


if __name__ == "__main__":
    main()
