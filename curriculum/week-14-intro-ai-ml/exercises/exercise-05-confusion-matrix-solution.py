"""exercise-05-confusion-matrix.py — accuracy hides what the matrix shows.

Screens a synthetic population where only 5% have the condition.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.20
N_SAMPLES = 1000
N_FEATURES = 6
LABELS = ["no condition", "condition"]


def make_population() -> tuple[pd.DataFrame, pd.Series]:
    """Generate a 95/5 imbalanced screening dataset as a frame and a series."""
    features, target = make_classification(
        n_samples=N_SAMPLES, n_features=N_FEATURES,
        n_informative=3, n_redundant=1, n_classes=2,
        weights=[0.95, 0.05], flip_y=0.0, class_sep=0.8,
        random_state=RANDOM_STATE,
    )
    columns = [f"marker_{i}" for i in range(N_FEATURES)]
    return pd.DataFrame(features, columns=columns), pd.Series(target, name="condition")


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy, the confusion matrix, and the per-class report."""
    print(f"--- {name} ---")
    print(f"accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred, target_names=LABELS, zero_division=0))


def main() -> None:
    """Compare a do-nothing baseline against a real classifier."""
    x, y = make_population()
    print(f"class balance: {y.value_counts().sort_index().to_dict()}")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"test set: {y_test.value_counts().sort_index().to_dict()}")

    dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy.fit(x_train, y_train)
    report("always says 'no condition'", y_test, dummy.predict(x_test))

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report("logistic regression", y_test, predictions)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
    print(f"caught {tp} of {tp + fn} people who had the condition")
    print(f"missed {fn} of {tp + fn} people who had the condition")
    print(f"sent {fp} healthy people for a second test")


if __name__ == "__main__":
    main()
