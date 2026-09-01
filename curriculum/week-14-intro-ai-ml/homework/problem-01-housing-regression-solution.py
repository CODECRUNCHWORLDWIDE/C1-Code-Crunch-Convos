"""problem-01-housing-regression.py — a linear baseline versus gradient boosting.

The real California housing table needs a download; this course runs offline, so
the houses here are generated from a fixed seed with genuine non-linear structure
built in — income has diminishing returns, location bends, and rooms interact
with income. That non-linearity is the whole point: it is what a straight-line
model cannot fit and a boosted tree can. Every seed is pinned, so the numbers are
identical on every machine.

Run it with::

    python problem-01-housing-regression-solution.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def make_housing(seed: int = RANDOM_STATE, n: int = 800) -> pd.DataFrame:
    """Synthetic housing with non-linear structure a line cannot capture.

    Target `median_value` is in $100,000s, like the real dataset.
    """
    rng = np.random.default_rng(seed)
    income = rng.uniform(1.5, 8.0, n)
    house_age = rng.uniform(1.0, 45.0, n)
    avg_rooms = rng.uniform(3.0, 8.0, n)
    population = rng.uniform(200.0, 4000.0, n)
    latitude = rng.uniform(32.0, 42.0, n)

    value = (
        2.0 * np.log(income)                       # diminishing returns of income
        + 0.25 * avg_rooms
        - 0.012 * house_age
        + 0.9 * np.sin((latitude - 32.0) / 10.0 * np.pi)  # location bends
        - 0.00004 * population
        + 0.10 * income * (avg_rooms - 5.0)        # income x rooms interaction
    )
    value = value + rng.normal(0.0, 0.20, n)

    return pd.DataFrame(
        {
            "median_income": income.round(2),
            "house_age": house_age.round(1),
            "avg_rooms": avg_rooms.round(2),
            "population": population.round(0),
            "latitude": latitude.round(2),
            "median_value": value.round(3),
        }
    )


def evaluate(name: str, model, x_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Print MAE, RMSE and R^2 for a fitted *model* on the test set."""
    predictions = model.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = root_mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"{name:<18} MAE={mae:.3f}  RMSE={rmse:.3f}  R2={r2:.3f}")


def main() -> None:
    """Train two regressors on the same split and compare their errors."""
    df = make_housing()
    print(f"rows: {len(df)}  features: {df.shape[1] - 1}  target: median_value ($100k)")

    x = df.drop(columns=["median_value"])
    y = df["median_value"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE
    )
    print(f"train rows: {len(x_train)}   test rows: {len(x_test)}")

    linear = LinearRegression()
    linear.fit(x_train, y_train)

    boosted = GradientBoostingRegressor(random_state=RANDOM_STATE)
    boosted.fit(x_train, y_train)

    print("--- metrics on the held-out test set (lower MAE/RMSE better, higher R2 better) ---")
    evaluate("LinearRegression", linear, x_test, y_test)
    evaluate("GradientBoosting", boosted, x_test, y_test)

    linear_mae = mean_absolute_error(y_test, linear.predict(x_test))
    boosted_mae = mean_absolute_error(y_test, boosted.predict(x_test))
    improvement = (linear_mae - boosted_mae) / linear_mae * 100
    print(f"boosting cuts MAE by {improvement:.1f}% versus the linear baseline")


if __name__ == "__main__":
    main()
