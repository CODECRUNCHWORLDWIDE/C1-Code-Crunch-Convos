"""exercise-04-pipeline.py — why scaling belongs inside the pipeline.

Compares an unscaled classifier with a scaled one on the wine dataset,
then shows that scaling before the split leaks test information.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
TEST_SIZE = 0.25
MAX_ITER = 1000


def build_pipeline() -> Pipeline:
    """Return a StandardScaler -> LogisticRegression pipeline."""
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=MAX_ITER, random_state=RANDOM_STATE)),
        ]
    )


def main() -> None:
    """Score unscaled vs pipelined, then compare fitted scaler means."""
    wine = load_wine(as_frame=True)
    x, y = wine.data, wine.target

    print(f"rows: {len(x)}  features: {x.shape[1]}  classes: {y.nunique()}")
    print("feature ranges (a few):")
    print(x[["alcohol", "color_intensity", "proline"]].describe().loc[["min", "max"]])

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    bare = LogisticRegression(random_state=RANDOM_STATE)  # default max_iter=100
    bare.fit(x_train, y_train)
    print("--- unscaled ---")
    print(f"iterations used: {bare.n_iter_[0]} (cap is {bare.max_iter})")
    print(f"accuracy: {bare.score(x_test, y_test):.3f}")

    pipe = build_pipeline()
    pipe.fit(x_train, y_train)
    print("--- pipeline: scale then classify ---")
    classifier = pipe.named_steps["clf"]
    print(f"iterations used: {classifier.n_iter_[0]} (cap is {classifier.max_iter})")
    print(f"accuracy: {pipe.score(x_test, y_test):.3f}")

    print("--- where the scaler learned its numbers ---")
    honest = pipe.named_steps["scale"].mean_[0]
    leaky = StandardScaler().fit(x).mean_[0]
    print(f"fitted on train only : alcohol mean = {honest:.4f}")
    print(f"fitted on everything : alcohol mean = {leaky:.4f}")
    print(f"identical? {honest == leaky}")


if __name__ == "__main__":
    main()
