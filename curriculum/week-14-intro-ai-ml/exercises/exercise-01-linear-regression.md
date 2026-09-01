# Exercise 1 — Your First Model: Price From Floor Area

> **Topic:** Fitting a linear regression and reading the parameters it learned
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md)
> **Difficulty:** Easy
> **Target time:** 20 minutes
> **Why this one:** this is the smallest complete supervised workflow that exists — data, split, fit, predict, evaluate. Every other exercise this week is this shape with more parts bolted on. If the five-line spine is not automatic for you, Exercise 4's pipeline will look like magic instead of like plumbing, and you will not be able to tell a broken model from a broken script.

## The Brief

You are helping a small housing co-op sanity-check its asking prices. Someone
has typed up sixteen recent condo sales: floor area in square feet, and the
price the unit actually sold for, in thousands of dollars. The question the
co-op wants answered is boring and useful: **for each extra square foot, how
much more does a unit sell for around here?**

That number is the slope of a line, and fitting a line to points is machine
learning in its smallest honest form. Think of it like drawing the straightest
stick you can through a scatter of dots, then reading two facts off the stick:
how steep it is, and where it crosses. You will fit it, read the slope and
intercept off the trained model, check the fit against four sales the model
never saw, and then use it: predict the price of a 2,200 sqft unit that has
not sold yet. That last step is the whole reason anyone trains a model.

## Starter

Copy this into `exercise-01-linear-regression.py` in your practice repo and
fill in the `TODO`s.

```python
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
    # TODO: X must stay a DataFrame. y must be a Series.
    raise NotImplementedError


def fit_model(x_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Train a LinearRegression on the training rows and return it."""
    # TODO: construct, fit, return.
    raise NotImplementedError


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

    # TODO: predict the price of a 2200 sqft unit and print it.
    # Hint: build a one-row DataFrame with the same column name the model saw.


if __name__ == "__main__":
    main()
```

Two words in that starter you need before you begin.

**A feature.** A feature is one fact about a thing you can measure — here, floor
area. It goes into the model. The model calls the bag of features `X`.

**The target.** The target is the thing you want the model to guess — here, the
price. The model calls it `y`. Supervised learning is just showing the model a
big pile of `(X, y)` pairs and letting it work out the rule that turns one into
the other.

## Requirements

1. `split_features_and_target` returns `X` as a **DataFrame** with one column
   (`sqft`) and `y` as a **Series** (`price_k`).
2. The split uses `test_size=0.25` and `random_state=RANDOM_STATE`, giving
   twelve training rows and four test rows.
3. The trained model's slope and intercept are read off `model.coef_[0]` and
   `model.intercept_` — not recomputed by hand.
4. MAE and R² are computed against `y_test`, never against `y_train`.
5. The 2,200 sqft prediction is made with a one-row DataFrame whose column is
   named `sqft`, and printed as a dollar figure rounded to the nearest
   thousand, for example `2200 sqft -> about $438k`.

## Constraints

- **`LISTINGS[["sqft"]]`, not `LISTINGS["sqft"]`.** Single brackets return a
  Series, which is one-dimensional, and scikit-learn refuses it. The feature
  matrix is always `(n_samples, n_features)` — two axes — even when
  `n_features` is 1. Double brackets keep the second axis, and they keep the
  column name, which the model needs later when you predict on a new row.
- **Pass `random_state=RANDOM_STATE` to `train_test_split`.** Without it, the
  split is drawn from fresh randomness on every run, so your MAE and R² change
  each time you press enter. You then cannot tell whether a number moved
  because you improved the code or because the dice rolled differently, and
  nobody else can reproduce your result at all. A pinned seed is what makes
  "I got 0.99" a claim instead of an anecdote.
- **Evaluate on the test rows only.** Scoring on the rows the model trained on
  measures memory, not skill. Twelve points and a straight line will always
  look good in the mirror.

## Expected output

The row counts are fixed; everything the solver decides is printed at full
precision. On this build the numbers below come out identical on every run
because `random_state=42` fixes which four rows are held out — change the seed
or your scikit-learn version and the slope, MAE and R² shift in the last
digits. Read the slope as **about 0.18 thousand dollars per square foot**,
roughly $180 a square foot; that sentence is the deliverable.

```text
$ python exercise-01-linear-regression-solution.py
rows: 16 | train: 12 | test: 4
slope (price_k per sqft): 0.179
intercept (price_k):      44.4
MAE on test:              3.02
R^2 on test:              0.999
2200 sqft -> about $437k
```

The row counts (`16 | 12 | 4`) are exact. The slope, intercept, MAE and R² are
approximate — a different scikit-learn build can move the last digit, and any
change to the seed moves more than that. R² near 1.0 says the line explains
almost all the variation in these sixteen sales.

## Steps

1. Activate the virtual environment with `scikit-learn` installed:
   `python -c "import sklearn; print(sklearn.__version__)"`.
2. Create `exercise-01-linear-regression.py` and paste the starter.
3. Fill in `split_features_and_target`. Run. It will fail at `fit_model` —
   that is expected, and reading the traceback is practice.
4. Fill in `fit_model`. Run again. You should now see slope, intercept, MAE
   and R².
5. Add the 2,200 sqft prediction. Check it by hand: `0.18 * 2200 + 42`. If
   your number is nowhere near that, the DataFrame you built is wrong.
6. Change `RANDOM_STATE` to `0` and rerun. The MAE moves. Sit with that for a
   moment — it is the entire subject of Exercise 3.

## The Solution

```python
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
```

Three decisions carry this file, and only one of them is about lines and slopes.

**The double brackets are half the exercise.** `listings["sqft"]` and
`listings[["sqft"]]` look one keystroke apart and hand back different shapes: a
`Series` of shape `(16,)` and a `DataFrame` of shape `(16, 1)`. scikit-learn
wants the feature matrix to have two axes always — rows of samples, columns of
features — because the same `fit` has to work whether you have one feature or a
thousand. The target is the opposite: one value per sample, so `y` is correctly
a `Series`. Getting the pair right is the habit the whole week is built on.

**The column name is data, not decoration.** Because `x` is a DataFrame,
`model.fit` writes the column names onto the trained model. That is why the
final prediction is built as `pd.DataFrame({"sqft": [2200]})` rather than as a
bare `[[2200]]`. With one feature the difference is cosmetic. With thirteen — as
in Exercise 4 — it is the only thing standing between you and silently feeding
one column into the slot the model reserved for another. Build the habit now,
while a mistake only earns a warning.

**Evaluating on `x_test` is not a formality.** Twelve points that nearly lie on
a line, fitted with a line, will look superb graded on themselves. The train
MAE here is about 2.2 and the test MAE about 3.0 — the model really is a touch
worse on rows it has not seen, and that gap is the only honest signal in the
whole run. `r2_score(y_test, predictions)` takes the true values first and the
guesses second; `mean_absolute_error` uses the same order. Truth, then guess,
every time.

The intercept, about 44, is what the line says a zero-square-foot condo would
cost, which is nonsense. It is a fitting artefact that holds the line at the
right height over the range 700 to 2,450 square feet, not a claim about
imaginary tiny apartments.

## Download and run

Download
[exercise-01-linear-regression-solution.py](./exercise-01-linear-regression-solution.py)
and run it:

```bash
python exercise-01-linear-regression-solution.py
```

It needs no setup and no download: the sixteen sales are written into the file,
and every seed is pinned, so it prints the same numbers on any machine with
scikit-learn installed. The `-solution` in the name keeps it from colliding with
your own `exercise-01-linear-regression.py`.

## Common bugs to catch

- **`ValueError: Expected a 2-dimensional container but got <class
  'pandas.core.series.Series'> instead.`** You wrote `listings["sqft"]`. Use
  `listings[["sqft"]]`. scikit-learn 1.6 added this pandas-specific wording; on
  an older build, or when you hand over a bare NumPy array, the message is the
  shorter classic `Expected 2D array, got 1D array instead`. Both are the same
  complaint. Ignore the suggestion to `.reshape(-1, 1)` — it works but throws
  the column name away, and you need that name eight lines later.
- **`UserWarning: X does not have valid feature names, but LinearRegression was
  fitted with feature names`.** You predicted with a bare list like
  `model.predict([[2200]])` instead of a DataFrame. The prediction still comes
  out — correct, even — which is exactly what makes the warning dangerous. It is
  telling you that you just switched from a name-based contract to a
  position-based one. Build `pd.DataFrame({"sqft": [2200]})` and it goes away.
- **`AttributeError: 'LinearRegression' object has no attribute 'coef_'`.** You
  never called `.fit()`. Attributes ending in an underscore only exist after
  fitting — that trailing underscore is scikit-learn's mark for "learned from
  data" (`n_iter_` is found, `max_iter` is chosen). A missing one means you
  skipped a fit.
- **The slope prints as an array like `[0.179]`.** `model.coef_` has one entry
  per feature. Index it: `model.coef_[0]`.
- **R² is negative.** You passed the arguments backwards. It is
  `r2_score(y_true, y_pred)`, so `r2_score(y_test, predictions)`. Flipping them
  gives a wrong number rather than an error.
- **MAE looks impossibly good.** You evaluated on `x_train`. Swapping to the
  training rows here only drops the MAE from `3.02` to `2.23`, which is the real
  lesson: on a small, nearly straight dataset a leaked score does **not** look
  obviously wrong, so you cannot rely on catching leakage by eye. Check which
  variable went into `.predict()` every time.

## Under the hood

<details>
<summary>Under the hood — what LinearRegression is actually solving</summary>

`LinearRegression` does not guess and check. It solves for the two numbers —
slope and intercept — that make the total squared error as small as it can
possibly be, and it does it in one shot with linear algebra, not by walking
downhill the way the logistic-regression solver does in later exercises.

"Squared error" is the reason it picks the line it does. For each training
point it measures the vertical gap between the real price and the line's guess,
squares that gap, and adds all the squares up. Squaring does two things: it
makes every miss positive so they cannot cancel out, and it punishes one big
miss far more than several small ones. The line that minimises that sum is the
"least squares" line, and for a single feature there is a closed-form formula
for it — the same one a statistics course derives by hand.

This is why the fit is instant and identical every run once the split is fixed:
there is no randomness inside `fit` at all. All the run-to-run movement you see
in this exercise comes from `train_test_split` choosing different rows, never
from the model. That is not true of the classifiers you meet next, and knowing
which part of your pipeline is deterministic is half of debugging one.

</details>

## Acceptance checklist

- [ ] The script runs top to bottom with no traceback and no warnings.
- [ ] `x.shape` is `(16, 1)` and `y.shape` is `(16,)`.
- [ ] Slope and intercept are read off the trained model, not hard-coded.
- [ ] MAE and R² are computed on the held-out rows.
- [ ] The 2,200 sqft prediction is within a few thousand of `0.18 * 2200 + 42`
      (the hand check gives 438; the model says 437).
- [ ] Running the script twice in a row prints identical numbers.
- [ ] Committed with a message like `Add Week 14 exercise 1: linear regression baseline`.

## Stretch

- **Predict far outside the training range.** A 400 sqft unit prints about
  $116k and a 9,000 sqft unit about $1,652k. Neither is a forecast. A fitted
  line is two numbers chosen to be good between 700 and 2,450 square feet;
  outside that window it is not reasoning from evidence, it is just continuing
  to be a line. It has no way to say "I have never seen anything like this".
  Write one sentence on why that is.
- **Add a second feature, `bedrooms`, that you make up plausibly, and refit.**
  `model.coef_` now has two entries. Comparing them directly means nothing —
  one is "thousands of dollars per square foot", the other "thousands of dollars
  per bedroom", and rates in different units are not comparable magnitudes.
  Standardise the features first (Exercise 4's `StandardScaler`) and then each
  coefficient is "per one standard deviation" and you may compare them.
- **Print the residuals**, `y_test - predictions`. Two land above the line and
  two below, all within about four thousand dollars. Four points can detect
  almost nothing about the shape of the error — say that, rather than reading a
  trend into it.

Next up: [Exercise 2 — Iris Classifier](./exercise-02-iris-classifier.md),
where the target stops being a number and becomes a label.
