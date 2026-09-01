"""exercise-01-linear-regression.py — fit a line, then read what it learned.

Predicts condo sale price (thousands of dollars) from floor area (sqft).
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.25

LISTINGS = pd.DataFrame(
    {
        "sqft": [700, 820, 900, 1010, 1120, 1240, 1330, 1450,
                 1580, 1690, 1800, 1930, 2050, 2180, 2300, 2450],
        "price_k": [171, 187, 206, 221, 246, 263, 284, 301,
                    329, 344, 369, 387, 414, 432, 459, 481],
    }
)


def split_features_and_target(listings: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return (X, y): a 2D feature frame and a 1D target series."""
    x = listings[["sqft"]]
    y = listings["price_k"]
    return x, y


def fit_model(x_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Train a LinearRegression on the training rows and return it."""
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model


def main() -> None:
    """Split, train, evaluate, and price one unseen unit."""
    x, y = split_features_and_target(LISTINGS)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    model = fit_model(x_train, y_train)
    predictions = model.predict(x_test)

    print(f"rows: {len(LISTINGS)} | train: {len(x_train)} | test: {len(x_test)}")
    print(f"slope (price_k per sqft): {float(model.coef_[0]):.3f}")
    print(f"intercept (price_k):      {float(model.intercept_):.1f}")
    print(f"MAE on test:              {mean_absolute_error(y_test, predictions):.2f}")
    print(f"R^2 on test:              {r2_score(y_test, predictions):.3f}")

    unseen = pd.DataFrame({"sqft": [2200]})
    asking_k = float(model.predict(unseen)[0])
    print(f"2200 sqft -> about ${asking_k:.0f}k")


if __name__ == "__main__":
    main()
