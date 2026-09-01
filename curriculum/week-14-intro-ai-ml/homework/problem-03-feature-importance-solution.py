"""problem-03-feature-importance.py — what a forest thinks matters, and what that means.

Trains a RandomForest on iris, ranks the features by importance, then retrains
without the least important and without the most important to watch the accuracy
move. The point is to read feature_importances_ honestly: it says which columns
this model leaned on, not which columns *cause* the outcome. Every seed is pinned.

Run it with::

    python problem-03-feature-importance-solution.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def train_and_score(x: pd.DataFrame, y: pd.Series) -> tuple[RandomForestClassifier, float]:
    """Split, fit a forest, and return it with its test accuracy."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model, accuracy_score(y_test, model.predict(x_test))


def main() -> None:
    """Rank features, then drop the least and most important and compare."""
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    model, baseline = train_and_score(x, y)
    ranking = sorted(
        zip(x.columns, model.feature_importances_), key=lambda pair: pair[1], reverse=True
    )
    print("feature importances (most to least):")
    for feature, importance in ranking:
        print(f"  {feature:<20} {importance:.3f}")
    print(f"baseline accuracy (all 4 features): {baseline:.3f}")

    least_important = ranking[-1][0]
    _, without_least = train_and_score(x.drop(columns=[least_important]), y)
    print(f"drop least important ({least_important}): accuracy {without_least:.3f}")

    most_important = ranking[0][0]
    _, without_most = train_and_score(x.drop(columns=[most_important]), y)
    print(f"drop most important  ({most_important}): accuracy {without_most:.3f}")

    print(
        f"dropping the least cost {baseline - without_least:+.3f}; "
        f"dropping the most cost {baseline - without_most:+.3f}"
    )


if __name__ == "__main__":
    main()
