# Problem 1 — Housing Regression: Linear vs Boosted

> **Topic:** Regression metrics, and when a straight line is not enough
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** Exercise 1 fit a line to data that really was a line. Real prices are not. This is where you meet a model that can bend — gradient boosting — and where you learn to report three regression numbers instead of one, because MAE, RMSE and R² each hide something the other two show.

## The Brief

You are pricing homes. Each home has five facts — median income of the area,
house age, average rooms, local population, and latitude — and you want to
predict its value in hundreds of thousands of dollars.

You will train two models on the same data and compare them. The first is
`LinearRegression`, the straight-line model from Exercise 1: it assumes value
goes up by a fixed amount for each extra unit of income, forever, in a dead
straight line. The second is `GradientBoostingRegressor`, which builds a crowd of
tiny decision trees where each new tree fixes the mistakes of the ones before it.
That crowd can bend: it can learn that income matters a lot at first and then
levels off, that location wiggles, that two features together mean something
neither means alone. The whole homework is a race between the straight line and
the bendy crowd on data that is deliberately not straight.

**A note on the data.** The real California housing table needs a download, and
this course runs offline. So the 800 homes here are generated from a fixed seed
with genuine curves baked into the price — income with diminishing returns, a
location term that bends, an income-times-rooms interaction. That curviness is
the point: it is exactly what the line cannot fit and the boosted trees can.

## Starter

Copy this into `problem-01-housing-regression.py`. The generator is given; you
fill in the models and the metrics.

```python
"""problem-01-housing-regression.py — a linear baseline versus gradient boosting."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def make_housing(seed: int = RANDOM_STATE, n: int = 800) -> pd.DataFrame:
    """Synthetic housing with non-linear structure a line cannot capture."""
    rng = np.random.default_rng(seed)
    income = rng.uniform(1.5, 8.0, n)
    house_age = rng.uniform(1.0, 45.0, n)
    avg_rooms = rng.uniform(3.0, 8.0, n)
    population = rng.uniform(200.0, 4000.0, n)
    latitude = rng.uniform(32.0, 42.0, n)
    value = (2.0 * np.log(income) + 0.25 * avg_rooms - 0.012 * house_age
             + 0.9 * np.sin((latitude - 32.0) / 10.0 * np.pi)
             - 0.00004 * population + 0.10 * income * (avg_rooms - 5.0))
    value = value + rng.normal(0.0, 0.20, n)
    return pd.DataFrame({
        "median_income": income.round(2), "house_age": house_age.round(1),
        "avg_rooms": avg_rooms.round(2), "population": population.round(0),
        "latitude": latitude.round(2), "median_value": value.round(3),
    })


def main() -> None:
    df = make_housing()
    x = df.drop(columns=["median_value"])
    y = df["median_value"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE
    )

    # TODO: fit LinearRegression and GradientBoostingRegressor(random_state=42).
    # TODO: for each, print MAE, RMSE (root_mean_squared_error) and R2 on the test set.


if __name__ == "__main__":
    main()
```

## Requirements

1. Train a `LinearRegression` baseline and report MAE, RMSE, and R² on a
   held-out test set.
2. Train a `GradientBoostingRegressor(random_state=42)` and report the same three
   metrics on the same split.
3. Say which is better and by how much, and be ready to explain *why* in one
   sentence.

## Constraints

- **Pin `random_state` on the split and the boosted model.** `LinearRegression`
  has no randomness, but the split and the tree-building do; without a seed your
  numbers move and the comparison is not repeatable.
- **Use `root_mean_squared_error`, not `mean_squared_error(..., squared=False)`.**
  The `squared` argument was removed; scikit-learn 1.6 ships a dedicated function.
- **Compare on the test set only.** Boosting can memorise the training rows
  almost perfectly, so a training-set comparison would make it look far better
  than it is and teach you nothing about which to ship.

## Expected output

Every number is decided by a pinned seed, so the run is identical on every
machine. The three metrics are approximate in the sense that a different library
build could shift a last digit, but the finding — boosting wins comfortably on
curvy data — is the fixed part.

```text
$ python problem-01-housing-regression-solution.py
rows: 800  features: 5  target: median_value ($100k)
train rows: 600   test rows: 200
--- metrics on the held-out test set (lower MAE/RMSE better, higher R2 better) ---
LinearRegression   MAE=0.382  RMSE=0.466  R2=0.895
GradientBoosting   MAE=0.219  RMSE=0.268  R2=0.965
boosting cuts MAE by 42.7% versus the linear baseline
```

Read the three numbers together. MAE is the average miss in $100k units — about
$38k for the line, $22k for the boosted crowd. RMSE is always at least as large
as MAE because it squares the misses before averaging, so it punishes the
occasional big miss harder; the gap between MAE and RMSE tells you how lumpy your
errors are. R² is the share of the variation the model explains, 0 to 1. All
three agree here: the model that can bend fits curvy data better.

## Steps

1. Paste the starter and run it — `make_housing` works, `main` does nothing yet.
2. Fit `LinearRegression`, predict on the test set, print MAE, RMSE, R².
3. Fit `GradientBoostingRegressor(random_state=42)` and print the same three.
4. Compute the percentage by which boosting cuts the MAE and print it.
5. Write one sentence: which won, and why the loser lost. (Hint: look at the
   `np.log` and `np.sin` terms in `make_housing`.)

## The Solution

```python
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
```

**Why boosting wins here is written into the data.** The price has a `np.log` of
income (which flattens as income rises), a `np.sin` of latitude (which goes up
then down), and an `income × rooms` term (where two features multiply). A linear
model can only add a fixed amount per feature; it has no way to express "flattens
off" or "goes up then down" or "these two together". Gradient boosting builds
shallow trees, and a tree splits on thresholds — "income below 4 does this, above
4 does that" — so a crowd of them can approximate any curve you like. Hand both
the same curvy target and the flexible one wins, which is most of the time in the
real world.

**Three metrics, because one lies by omission.** MAE treats every dollar of error
equally. RMSE squares errors first, so a single big miss counts far more than
several small ones — RMSE noticeably above MAE is your warning that a few
predictions are badly off even if most are fine. R² rescales everything into "how
much of the variation did we capture", which is comparable across datasets in a
way raw dollars are not. Report all three and a reader can see not just how big
the errors are but what shape they are.

**When the line would win.** If the data really were linear, `LinearRegression`
would match or beat boosting and run in a fraction of the time, and boosting's
extra flexibility would just fit noise. "More powerful model" is not a free win;
it is the right call only when the data has structure a line cannot reach.

## Download and run

Download
[problem-01-housing-regression-solution.py](./problem-01-housing-regression-solution.py)
and run it:

```bash
python problem-01-housing-regression-solution.py
```

The homes are generated from a fixed seed inside the file, so there is nothing to
download and the metrics are identical on every machine. The `-solution` suffix
keeps it clear of your own `problem-01-housing-regression.py`.

## Common bugs to catch

- **`TypeError: mean_squared_error() got an unexpected keyword argument 'squared'`.**
  That argument was removed. Import and call `root_mean_squared_error` instead.
- **Boosting looks perfect (R² ≈ 1.0).** You evaluated on the training rows.
  Boosting nearly memorises them; score on `x_test`.
- **The two models tie, or the line wins.** You may have flattened the data — if
  you simplified `make_housing` to a purely linear target while experimenting,
  the line has nothing left to lose to. The curviness is the whole exercise.
- **`ValueError: Input contains NaN`.** The generator does not create NaNs; if
  you swapped in your own data with holes, impute them first (see Challenge 1).

## Under the hood

<details>
<summary>Under the hood — what "boosting" actually does, tree by tree</summary>

Gradient boosting is a surprisingly simple idea repeated a hundred times. Start
with a dumb prediction — the average price. Look at how wrong it is on every home
(the *residuals*, the leftover errors). Now train one small decision tree whose
only job is to predict those errors. Add its predictions to the running total,
which nudges every prediction a little closer. The total is still wrong, but less
wrong, so you compute the new residuals and train another small tree on those.
Repeat.

Each tree is deliberately weak — shallow, allowed to explain only a sliver — and
each is scaled down by a *learning rate* before being added, so no single tree
can dominate. After a hundred rounds the sum of all those small corrections is a
model that bends and wiggles to match the data, built entirely out of "fix the
current mistakes a little". That is the "gradient" in the name: each round steps
in the direction that most reduces the error, the same downhill idea as the
logistic-regression solver, but taking a whole tree as each step.

This is why boosting overfits if you let it run too long or grow trees too deep:
given enough rounds it will start fixing the *noise* in the training set, which
is memorisation, not learning. The knobs that matter — `n_estimators`,
`learning_rate`, `max_depth` — are all really one question: how much flexibility
do you hand it before it starts learning the noise? That is a job for
cross-validation (Problem 4), not for guessing.

</details>

## Acceptance checklist

- [ ] Both models train on the same split and are scored on the held-out test
      set.
- [ ] MAE, RMSE, and R² print for each model.
- [ ] `random_state=42` is on the split and the boosted model.
- [ ] Boosting's MAE is clearly lower than the linear model's.
- [ ] Two runs print identical numbers.
- [ ] You wrote one sentence on why the linear model lost.

## Stretch

- **Tune the boosting.** Try `learning_rate=0.05` with `n_estimators=400`. Does
  a slower, longer fit beat the default? Check on the test set, not the training
  set.
- **Which feature carried it?** Print `boosted.feature_importances_` sorted, and
  see whether `median_income` dominates the way it does in real housing data.
- **A middle option.** Add a `RandomForestRegressor(random_state=42)` to the
  comparison. Forests also bend but build their trees independently rather than
  in sequence — does it land between the line and the boosting, or beat both?
