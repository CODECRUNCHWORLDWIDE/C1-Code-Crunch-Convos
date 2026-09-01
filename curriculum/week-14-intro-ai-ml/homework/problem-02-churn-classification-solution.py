"""problem-02-churn-classification.py — imbalanced churn: two models, the right metric.

A synthetic-but-realistic churn dataset (about 15% churn) built with
make_classification, so it runs offline and reproducibly. The lesson is Exercise
5's, applied: on imbalanced data accuracy flatters both models, and the number
that matters is recall on the churn class, because a missed churner is the
expensive mistake. Every seed is pinned.

Run it with::

    python problem-02-churn-classification-solution.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def make_churn(seed: int = RANDOM_STATE, n: int = 5000) -> pd.DataFrame:
    """A ~15% churn dataset of eight anonymous behavioural signals."""
    features, target = make_classification(
        n_samples=n,
        n_features=8,
        n_informative=4,
        n_redundant=2,
        weights=[0.85, 0.15],
        flip_y=0.0,
        class_sep=0.9,
        random_state=seed,
    )
    columns = [f"signal_{i}" for i in range(features.shape[1])]
    frame = pd.DataFrame(features, columns=columns)
    frame["churned"] = target
    return frame


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy plus precision/recall/F1 for the churn class (label 1)."""
    print(f"--- {name} ---")
    print(f"accuracy : {accuracy_score(y_true, y_pred):.3f}")
    print(f"churn precision: {precision_score(y_true, y_pred, zero_division=0):.3f}")
    print(f"churn recall   : {recall_score(y_true, y_pred, zero_division=0):.3f}")
    print(f"churn f1       : {f1_score(y_true, y_pred, zero_division=0):.3f}")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_true, y_pred))


def main() -> None:
    """Train two classifiers and compare them on the churn class, not accuracy."""
    df = make_churn()
    balance = df["churned"].value_counts().sort_index().to_dict()
    print(f"rows: {len(df)}   class balance (0=stay, 1=churn): {balance}")

    x = df.drop(columns=["churned"])
    y = df["churned"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    print(f"test set churn balance: {y_test.value_counts().sort_index().to_dict()}")

    logreg = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    logreg.fit(x_train, y_train)
    report("LogisticRegression", y_test, logreg.predict(x_test))

    forest = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    forest.fit(x_train, y_train)
    report("RandomForest", y_test, forest.predict(x_test))

    logreg_recall = recall_score(y_test, logreg.predict(x_test), zero_division=0)
    forest_recall = recall_score(y_test, forest.predict(x_test), zero_division=0)
    better = "RandomForest" if forest_recall > logreg_recall else "LogisticRegression"
    print(
        f"if a missed churner costs most, pick {better}: it catches the higher "
        f"share of churners (recall {max(logreg_recall, forest_recall):.3f})"
    )


if __name__ == "__main__":
    main()
