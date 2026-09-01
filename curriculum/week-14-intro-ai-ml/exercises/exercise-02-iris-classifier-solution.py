"""exercise-02-iris-classifier.py — three-class logistic regression on iris.

Trains on scikit-learn's bundled iris measurements and names two new flowers.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.30
MAX_ITER = 1000

NEW_FLOWERS = [
    [5.0, 3.4, 1.5, 0.2],   # small petals
    [6.7, 3.0, 5.6, 2.2],   # long, wide petals
]


def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Return (X, y, class_names) from the bundled iris dataset."""
    iris = load_iris(as_frame=True)
    return iris.data, iris.target, iris.target_names.tolist()


def train_classifier(x_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Fit a LogisticRegression and return it."""
    model = LogisticRegression(max_iter=MAX_ITER, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model


def main() -> None:
    """Train, score, and name two hand-written flowers."""
    x, y, class_names = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    model = train_classifier(x_train, y_train)
    predictions = model.predict(x_test)

    print("features:", list(x.columns))
    print("classes :", class_names)
    print(f"train rows: {len(x_train)}   test rows: {len(x_test)}")
    print(f"accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"mistakes: {(predictions != y_test).sum()} of {len(y_test)}")

    new_frame = pd.DataFrame(NEW_FLOWERS, columns=x.columns)
    for measurements, code in zip(NEW_FLOWERS, model.predict(new_frame)):
        print(f"{measurements} -> {class_names[code]}")


if __name__ == "__main__":
    main()
