"""challenge-01-titanic-survival.py — predict survival, then audit the model by sex.

A self-contained, offline version of the classic Titanic problem. The famous
dataset needs a download, and this course runs offline and deterministically, so
the passengers here are *generated* from a fixed seed with the real historical
pattern baked in — women and first-class passengers survive more, and age has
missing values you must impute. Every source of randomness is pinned, so the
numbers below are identical on every machine.

What it shows:
  * a ColumnTransformer that imputes + scales numbers and imputes + one-hot
    encodes categories, all inside one Pipeline (no leakage);
  * two classifiers compared on the same split;
  * a fairness audit — precision and recall computed separately for men and
    women — which is the point of the exercise;
  * a joblib round-trip proving the whole pipeline saves and reloads.

Run it with::

    python challenge-01-titanic-survival-solution.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
N_PASSENGERS = 500

NUMERIC_COLS = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_COLS = ["sex", "embarked", "pclass"]


def make_titanic(seed: int = RANDOM_STATE, n: int = N_PASSENGERS) -> pd.DataFrame:
    """Generate a Titanic-shaped passenger table with the real survival pattern.

    Not the historical dataset (which needs a download) but the same columns and
    the same signal: women and first-class passengers are far likelier to
    survive, children get a boost, and `age` carries missing values on purpose.
    """
    rng = np.random.default_rng(seed)

    sex = rng.choice(["male", "female"], size=n, p=[0.64, 0.36])
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
    true_age = rng.normal(29.0, 14.0, n).clip(0.5, 80.0)
    sibsp = rng.integers(0, 4, n)
    parch = rng.integers(0, 3, n)
    base_fare = np.select(
        [pclass == 1, pclass == 2, pclass == 3], [84.0, 21.0, 14.0]
    )
    fare = (base_fare * rng.uniform(0.5, 1.8, n)).round(2)
    embarked = rng.choice(["S", "C", "Q"], size=n, p=[0.72, 0.19, 0.09])

    # Survival probability: the "women and children first" evacuation pattern.
    female = (sex == "female").astype(float)
    first = (pclass == 1).astype(float)
    third = (pclass == 3).astype(float)
    child = (true_age < 12).astype(float)
    logit = (
        -1.0
        + 2.2 * female
        + 0.9 * first
        - 0.6 * third
        + 1.0 * child
        - 0.01 * (true_age - 29.0)
    )
    survived = (rng.random(n) < 1.0 / (1.0 + np.exp(-logit))).astype(int)

    frame = pd.DataFrame(
        {
            "survived": survived,
            "pclass": pclass,
            "sex": sex,
            "age": true_age,
            "sibsp": sibsp,
            "parch": parch,
            "fare": fare,
            "embarked": embarked,
        }
    )

    # Punch holes in the data the way a real manifest has them.
    frame.loc[rng.random(n) < 0.20, "age"] = np.nan
    frame.loc[rng.random(n) < 0.02, "embarked"] = np.nan
    return frame


def build_pipeline(classifier) -> Pipeline:
    """Wrap preprocessing and *classifier* in one leak-free estimator."""
    numeric = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric, NUMERIC_COLS),
            ("cat", categorical, CATEGORICAL_COLS),
        ]
    )
    return Pipeline(steps=[("prep", preprocess), ("clf", classifier)])


def group_metrics(name: str, mask: pd.Series, y_true: pd.Series, y_pred: np.ndarray) -> str:
    """Return one formatted table row of precision/recall/accuracy for a group."""
    truth = y_true[mask]
    guess = y_pred[mask.to_numpy()]
    precision = precision_score(truth, guess, zero_division=0)
    recall = recall_score(truth, guess, zero_division=0)
    accuracy = accuracy_score(truth, guess)
    return f"| {name:<6} | {len(truth):>3} | {precision:>9.2f} | {recall:>6.2f} | {accuracy:>8.2f} |"


def main() -> None:
    """Load, inspect, train two models, audit by sex, and prove persistence."""
    df = make_titanic()

    survived = int(df["survived"].sum())
    print(f"passengers: {len(df)}   survived: {survived}   died: {len(df) - survived}")
    print(f"missing ages: {int(df['age'].isna().sum())}   missing embarked: {int(df['embarked'].isna().sum())}")
    print("survival rate by sex:")
    for sex, rate in df.groupby("sex")["survived"].mean().items():
        print(f"  {sex:<6} {rate:.2f}")
    print("survival rate by class:")
    for pclass, rate in df.groupby("pclass")["survived"].mean().items():
        print(f"  class {pclass} {rate:.2f}")

    x = df.drop(columns=["survived"])
    y = df["survived"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    models = {
        "logreg": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "tree": DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE),
    }
    fitted: dict[str, Pipeline] = {}
    print("--- model comparison (accuracy on the held-out test set) ---")
    for label, classifier in models.items():
        pipe = build_pipeline(classifier)
        pipe.fit(x_train, y_train)
        fitted[label] = pipe
        accuracy = accuracy_score(y_test, pipe.predict(x_test))
        print(f"  {label:<6} accuracy: {accuracy:.3f}")

    best = fitted["logreg"]
    predictions = best.predict(x_test)
    print("--- best model: logreg ---")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_test, predictions))

    print("--- fairness audit: metrics per group (positive class = survived) ---")
    print("| group  |   n | precision | recall | accuracy |")
    print("|--------|-----|-----------|--------|----------|")
    all_mask = pd.Series(True, index=y_test.index)
    print(group_metrics("all", all_mask, y_test, predictions))
    print(group_metrics("male", x_test["sex"] == "male", y_test, predictions))
    print(group_metrics("female", x_test["sex"] == "female", y_test, predictions))

    with tempfile.TemporaryDirectory() as workspace:
        path = Path(workspace) / "titanic.joblib"
        joblib.dump(best, path)
        reloaded = joblib.load(path)
        same = bool(np.array_equal(reloaded.predict(x_test), predictions))
        print(f"saved and reloaded pipeline predicts identically: {same}")


if __name__ == "__main__":
    main()
