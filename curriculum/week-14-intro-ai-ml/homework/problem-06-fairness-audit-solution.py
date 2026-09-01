"""problem-06-fairness-audit.py — one model, three scorecards: everyone, men, women.

Trains a single survival classifier on the offline Titanic-shaped data from
Challenge 1, then scores it three times: on all test passengers, on men only, and
on women only. A model can be "accurate overall" and still behave completely
differently for two groups, and the only way to see that is to measure each group
on its own. Every seed is pinned.

Run it with::

    python problem-06-fairness-audit-solution.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
NUMERIC_COLS = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_COLS = ["sex", "embarked", "pclass"]


def make_titanic(seed: int = RANDOM_STATE, n: int = 500) -> pd.DataFrame:
    """Titanic-shaped passengers with the historical survival pattern."""
    rng = np.random.default_rng(seed)
    sex = rng.choice(["male", "female"], size=n, p=[0.64, 0.36])
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
    true_age = rng.normal(29.0, 14.0, n).clip(0.5, 80.0)
    sibsp = rng.integers(0, 4, n)
    parch = rng.integers(0, 3, n)
    base_fare = np.select([pclass == 1, pclass == 2, pclass == 3], [84.0, 21.0, 14.0])
    fare = (base_fare * rng.uniform(0.5, 1.8, n)).round(2)
    embarked = rng.choice(["S", "C", "Q"], size=n, p=[0.72, 0.19, 0.09])

    female = (sex == "female").astype(float)
    first = (pclass == 1).astype(float)
    third = (pclass == 3).astype(float)
    child = (true_age < 12).astype(float)
    logit = (-1.0 + 2.2 * female + 0.9 * first - 0.6 * third
             + 1.0 * child - 0.01 * (true_age - 29.0))
    survived = (rng.random(n) < 1.0 / (1.0 + np.exp(-logit))).astype(int)

    frame = pd.DataFrame(
        {
            "survived": survived, "pclass": pclass, "sex": sex, "age": true_age,
            "sibsp": sibsp, "parch": parch, "fare": fare, "embarked": embarked,
        }
    )
    frame.loc[rng.random(n) < 0.20, "age"] = np.nan
    frame.loc[rng.random(n) < 0.02, "embarked"] = np.nan
    return frame


def build_pipeline() -> Pipeline:
    """A leak-free preprocessing + logistic-regression pipeline."""
    numeric = Pipeline(
        steps=[("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    categorical = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocess = ColumnTransformer(
        transformers=[("num", numeric, NUMERIC_COLS), ("cat", categorical, CATEGORICAL_COLS)]
    )
    return Pipeline(
        steps=[
            ("prep", preprocess),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )


def score_group(name: str, mask: np.ndarray, y_true: pd.Series, y_pred: np.ndarray) -> None:
    """Print one row of the fairness table for the passengers in *mask*."""
    truth = y_true.to_numpy()[mask]
    guess = y_pred[mask]
    precision = precision_score(truth, guess, zero_division=0)
    recall = recall_score(truth, guess, zero_division=0)
    accuracy = accuracy_score(truth, guess)
    print(f"| {name:<6} | {mask.sum():>3} | {precision:>9.2f} | {recall:>6.2f} | {accuracy:>8.2f} |")


def main() -> None:
    """Train one classifier and score it for everyone, men, and women."""
    df = make_titanic()
    x = df.drop(columns=["survived"])
    y = df["survived"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(x_train, y_train)
    predictions = pipe.predict(x_test)
    print(f"overall test accuracy: {accuracy_score(y_test, predictions):.3f}")

    sex = x_test["sex"].to_numpy()
    print("fairness audit (positive class = survived):")
    print("| group  |   n | precision | recall | accuracy |")
    print("|--------|-----|-----------|--------|----------|")
    score_group("all", np.ones(len(sex), dtype=bool), y_test, predictions)
    score_group("male", sex == "male", y_test, predictions)
    score_group("female", sex == "female", y_test, predictions)

    male_recall = recall_score(y_test.to_numpy()[sex == "male"], predictions[sex == "male"], zero_division=0)
    female_recall = recall_score(y_test.to_numpy()[sex == "female"], predictions[sex == "female"], zero_division=0)
    print(
        f"same model, but recall is {female_recall:.2f} for women and {male_recall:.2f} "
        f"for men -- the overall accuracy hid that gap"
    )


if __name__ == "__main__":
    main()
