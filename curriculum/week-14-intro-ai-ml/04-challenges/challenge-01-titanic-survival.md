# Challenge 01 — Predict Titanic survival

## The problem

Given a passenger's attributes (age, sex, ticket class, fare paid, port of embarkation, family members on board), predict whether they survived the sinking of the Titanic.

Classic binary classification. Easy data to access, surprisingly rich for teaching, and a famous public ML benchmark — meaning you can compare your numbers to thousands of online write-ups.

## Get the data

```python
import seaborn as sns
df = sns.load_dataset("titanic")
print(df.shape)        # (891, 15)
print(df.columns.tolist())
print(df.head())
```

Columns of interest:

| Column | Meaning |
|----------|------------------------------------------------------------|
| survived | 0 = died, 1 = survived. This is your target `y`. |
| pclass | Ticket class (1, 2, 3). Numeric but really ordinal. |
| sex | "male" or "female". |
| age | Age in years. Has missing values. |
| sibsp | Siblings/spouses aboard. |
| parch | Parents/children aboard. |
| fare | Fare paid in pounds. |
| embarked | "S", "C", or "Q". A few missing values. |

Columns you can safely ignore for a baseline: `who`, `adult_male`, `class`, `alive`, `deck` (mostly missing), `embark_town`, `alone`. Several of those are derived from the other columns and would be data leaks.

## Requirements

1. **Inspect the data first.** Print `df.info()`, count missing values per column, look at survival rate by `sex` and `pclass`. Note what you find.
2. **Handle missing values.** `age` has many missing values; pick a strategy and justify it (median imputation is fine).
3. **Encode categoricals.** Use `OneHotEncoder` for `sex` and `embarked`. Use `ColumnTransformer` to apply it.
4. **Build a Pipeline.** Preprocessing + classifier in one estimator.
5. **Train at least two classifiers.** Suggested: `LogisticRegression` and `DecisionTreeClassifier` (or `RandomForestClassifier`).
6. **Evaluate.** Report accuracy, precision, recall, F1, and the confusion matrix on a held-out test set. Use `random_state=42` so your numbers are reproducible.
7. **Fairness audit.** Compute precision and recall **separately for male and female passengers** in the test set. Comment on what you see. (Hint: the model will heavily favour predicting "female ⇒ survived"; understand why, and discuss whether this is the model "discovering signal" or "learning from a biased label generator".)
8. **Save your best model** to `titanic.joblib` using `joblib.dump`. Confirm you can load it back.

## Skeleton

```python
from __future__ import annotations

import joblib
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load() -> pd.DataFrame:
    df = sns.load_dataset("titanic")
    keep = ["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]
    return df[keep].copy()


def build_pipeline() -> Pipeline:
    numeric_cols = ["age", "sibsp", "parch", "fare"]
    categorical_cols = ["sex", "embarked", "pclass"]

    numeric = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric, numeric_cols),
            ("cat", categorical, categorical_cols),
        ]
    )
    return Pipeline(steps=[
        ("prep", preprocess),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def main() -> None:
    df = load()
    X = df.drop(columns=["survived"])
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)

    print(classification_report(y_test, preds, target_names=["died", "survived"]))
    print("Confusion matrix:\n", confusion_matrix(y_test, preds))

    # TODO: fairness audit — split test set by sex, report precision/recall per group.
    # TODO: try at least one other classifier and compare.
    # TODO: save the best model with joblib.dump(pipe, "titanic.joblib").


if __name__ == "__main__":
    main()
```

## Target scores

A reasonable solution lands at around **0.80 accuracy** with logistic regression and **0.81–0.84 accuracy** with a tuned tree-based model. Beat 0.85 and you have likely overfit to one split; check with cross-validation.

## What to think about

- The "sex" feature is by far the strongest predictor. Discuss with a peer: is the model making a *causal* statement about sex and survival, or is it learning that historical evacuation prioritised women and children? What is the difference?
- The Titanic dataset is small (n ≈ 891). Splits will be noisy. Use cross-validation (`cross_val_score` with `cv=5`) for a more stable read.
- Beware of `class` and `alive` columns — they are post-hoc derivations of the target and the categorical class, and using them is data leakage. Always check whether a feature could only be known *after* you would have made the prediction.

## Stretch

- Build an `age * pclass` interaction feature. Does it help?
- Try `GradientBoostingClassifier`. Compare.
- Plot survival rate vs `fare` (after binning fare into deciles). What story does the chart tell?
- Use `permutation_importance` to rank feature importance. Does the ranking match your intuition?

When you are done, write a one-paragraph reflection covering: best model, best score, biggest surprise, and one thing you would do differently with more time.
