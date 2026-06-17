"""Exercise 01 — Linear regression: predict house price from square footage.

Goals:
  * Learn the shape of the scikit-learn API: fit, predict, score.
  * Understand what `model.coef_` and `model.intercept_` mean.
  * Read MAE and R^2 sensibly.

Run:
    python exercise-01-linear-regression.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def build_dataset() -> pd.DataFrame:
    """Return a tiny synthetic house-price dataset.

    Roughly linear: price ~= 0.18 * sqft + 30 (in thousands of dollars),
    with a little noise added so it isn't perfectly linear.
    """
    return pd.DataFrame(
        {
            "sqft": [
                650, 800, 950, 1100, 1250, 1400, 1550, 1700, 1850, 2000,
                2150, 2300, 2450, 2600, 2750, 2900, 3050, 3200, 3350, 3500,
            ],
            "price_k": [
                142, 168, 195, 218, 244, 266, 291, 311, 339, 360,
                382, 410, 431, 460, 484, 512, 533, 561, 588, 613,
            ],
        }
    )


def train_and_evaluate(df: pd.DataFrame) -> LinearRegression:
    """Train a linear regression and print evaluation metrics."""
    X = df[["sqft"]]  # 2D feature matrix
    y = df["price_k"]  # 1D target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("Learned parameters:")
    print(f"  slope     = {float(model.coef_[0]):.4f} (price_k per extra sqft)")
    print(f"  intercept = {float(model.intercept_):.4f} (base price_k at 0 sqft)")

    print("\nEvaluation on the held-out test set:")
    print(f"  MAE = {mean_absolute_error(y_test, preds):.3f} (thousands of dollars)")
    print(f"  R^2 = {r2_score(y_test, preds):.4f}")

    return model


def predict_examples(model: LinearRegression) -> None:
    """Show the model in action on a few hand-picked square-footage values."""
    examples = pd.DataFrame({"sqft": [500, 1500, 2200, 4000]})
    preds = model.predict(examples)
    print("\nPredictions for new houses:")
    for sqft, price in zip(examples["sqft"], preds):
        print(f"  {sqft:5d} sqft -> ${price:.1f}k")


def main() -> None:
    df = build_dataset()
    model = train_and_evaluate(df)
    predict_examples(model)

    print(
        "\nTry this next:\n"
        "  - Re-run with random_state=0. Did the slope/intercept change much?\n"
        "  - Add a noisy row (e.g., 1800 sqft, 900k) to the dataset.\n"
        "    Does it shift the slope? What does that tell you about outliers?\n"
    )


if __name__ == "__main__":
    main()
