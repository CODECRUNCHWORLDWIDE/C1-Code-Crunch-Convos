# Exercise 4 — Scaler and Model in One Pipeline

> **Topic:** `StandardScaler` + `LogisticRegression` inside a `Pipeline`, and the leak it prevents
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 25 minutes
> **Why this one:** a pipeline is not a tidiness feature. It is the thing that stops your scaler from seeing the test set, and preprocessing leakage is the most common way a beginner's model reports a score it cannot reproduce in production. Skip this and every later model you build is one forgotten `.transform()` away from being wrong in a way that looks fine.

## The Brief

The wine dataset ships with scikit-learn: 178 Italian wines, thirteen chemical
measurements each, three cultivars to tell apart. It is a good teaching set for
one specific reason — **its features are on wildly different scales**. Alcohol
is around 13. Colour intensity is around 5. Proline, an amino acid
concentration, runs into the hundreds and past a thousand.

Here is the picture to hold in your head. Logistic regression learns by rolling
downhill on a landscape built out of those numbers, looking for the lowest
point. When one feature's numbers are a thousand times bigger than another's,
the landscape is a long narrow canyon instead of a round bowl, and the ball
rolls back and forth across the canyon forever without getting to the bottom.
You will watch it give up, then fix it with `StandardScaler` inside a
`Pipeline` — which reshapes the canyon into a bowl by learning its mean and
spread from the training rows only. You will also prove that the naive
alternative — scale everything first, then split — quietly uses information from
the test set.

## Starter

Copy this into `exercise-04-pipeline.py` and fill in the `TODO`s.

```python
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
    # TODO: steps=[("scale", ...), ("clf", ...)]
    # The classifier needs max_iter=MAX_ITER and random_state=RANDOM_STATE.
    raise NotImplementedError


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
    # TODO: print the classifier's iteration count and the pipeline's accuracy.
    # Reach the classifier with pipe.named_steps["clf"].

    print("--- where the scaler learned its numbers ---")
    honest = pipe.named_steps["scale"].mean_[0]
    leaky = StandardScaler().fit(x).mean_[0]
    print(f"fitted on train only : alcohol mean = {honest:.4f}")
    print(f"fitted on everything : alcohol mean = {leaky:.4f}")
    print(f"identical? {honest == leaky}")


if __name__ == "__main__":
    main()
```

## Requirements

1. `build_pipeline` returns a `Pipeline` with exactly two steps, named
   `"scale"` and `"clf"`, in that order.
2. The classifier inside the pipeline gets `max_iter=1000` and
   `random_state=RANDOM_STATE`.
3. Both models are trained on the same `x_train` / `y_train` and scored on the
   same `x_test` / `y_test`. 133 training rows, 45 test rows.
4. Iteration counts print for both models, read from `n_iter_[0]`.
5. The final block prints two alcohol means and the boolean comparison, which
   must be `False`.

## Constraints

- **The scaler goes inside the pipeline, not before the split.** A
  `StandardScaler` learns a mean and a standard deviation. If it learns them
  from all 178 rows, those two numbers carry information about the 45 rows you
  are about to grade yourself on, and your test score is no longer a forecast
  of unseen data. The pipeline makes the correct thing the default thing —
  `pipe.fit` fits the scaler on the training rows alone, and `pipe.predict`
  applies those same frozen numbers to whatever arrives later.
- **Name the steps.** `Pipeline(steps=[("scale", ...), ("clf", ...)])` lets you
  reach inside with `pipe.named_steps["clf"]`. `make_pipeline` works too, but it
  auto-names the steps from the class names — `standardscaler`,
  `logisticregression` — so your inspection code breaks the moment you swap a
  class. Name them yourself.
- **Pass `random_state` to the classifier and to the split.** The lbfgs solver
  is deterministic, so the model seed changes little here — but the split seed
  decides which 45 wines you are graded on, and an unpinned seed means the
  accuracy you paste into a message is a number nobody else can obtain.
- **Leave the first model at its default `max_iter`.** You want to see the
  `ConvergenceWarning`. Raising the cap hides the symptom; scaling removes the
  cause. Knowing the difference is the exercise.

## Expected output

The `ConvergenceWarning` from the unscaled model is printed to the error stream,
not the output stream, so depending on your terminal it may appear above or
tangled into the lines below rather than where it belongs — it is not part of
the captured output here. The `rows / features / classes` line, the whole
`min`/`max` table, the iteration cap of 100, and `identical? False` are fixed.
Both accuracies and the seventeen iterations are approximate.

```text
$ python exercise-04-pipeline-solution.py
rows: 178  features: 13  classes: 3
feature ranges (a few):
     alcohol  color_intensity  proline
min    11.03             1.28    278.0
max    14.83            13.00   1680.0
--- unscaled ---
iterations used: 100 (cap is 100)
accuracy: 0.978
--- pipeline: scale then classify ---
iterations used: 17 (cap is 1000)
accuracy: 1.000
--- where the scaler learned its numbers ---
fitted on train only : alcohol mean = 12.9683
fitted on everything : alcohol mean = 13.0006
identical? False
```

Three things to take from that block. The unscaled model **used every iteration
it had and still was not finished** — that is what the warning means. The scaled
model finished in seventeen and scored higher. And the two alcohol means look
the same rounded to one decimal (both 13.0) but are not equal, which is exactly
why leakage is hard to notice: it does not look like anything.

## Steps

1. Create the file and paste the starter. Run it before filling anything in —
   the unscaled section works already, and the `ConvergenceWarning` should
   appear on your terminal's error stream.
2. Read the `min`/`max` table. Proline's range is roughly a thousand times
   alcohol's. That ratio is the whole problem.
3. Fill in `build_pipeline`, then the pipeline print block, using
   `pipe.named_steps["clf"].n_iter_[0]` and `pipe.score(x_test, y_test)`.
4. Run again. Compare the two iteration counts before you compare the two
   accuracies — the iteration count is the mechanism, the accuracy is only the
   symptom.
5. Confirm the transformed training data is centred:
   `pipe.named_steps["scale"].transform(x_train).mean(axis=0)` should be a row
   of numbers extremely close to zero.
6. Worth ninety seconds: `import joblib; joblib.dump(pipe, "wine.joblib")`.
   One file now holds the scaler, the model, and the order they run in. That
   is the deployment payoff Lecture 3 promised.

## The Solution

```python
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
```

**Why wine and not iris.** Iris is four columns of centimetres, all between
roughly 0 and 8; scaling it changes almost nothing and the lesson would not
land. Wine's thirteen features span orders of magnitude, and the `min`/`max`
table proves it: alcohol varies over a range of about 4, proline over about
1,400. That ratio is the entire problem. `StandardScaler` subtracts each
column's mean and divides by its standard deviation, and the long narrow canyon
becomes a round bowl the solver can reach the bottom of.

**Read the iteration counts before the accuracies.** The unscaled model reports
`iterations used: 100 (cap is 100)` — it did not converge, it ran out of budget,
which is precisely what the `ConvergenceWarning` means. The pipelined model
reports 17 out of a cap of 1,000. Same data, same solver, same seed: seventeen
steps instead of a hundred-and-not-finished. The iteration count is the
mechanism; the accuracy is only the symptom, and on this dataset both models
score well enough that if you had looked at accuracy alone you might have
concluded scaling barely mattered.

**Why the scaler must live inside the pipeline.** `StandardScaler` is not a
formula, it is an estimator: `fit` *learns* thirteen means and thirteen standard
deviations from whatever you show it. Fit it on all 178 rows and those numbers
contain information about the 45 rows you are about to grade yourself on. Your
test score is then no longer a forecast of unseen data, because the data was not
entirely unseen. `Pipeline` makes the correct thing the default thing:
`pipe.fit(x_train, y_train)` fits the scaler on the training rows alone, and
`pipe.predict` applies those same frozen numbers to whatever arrives later —
test rows today, real wine next year.

**The final block is the proof, and its shape is the lesson.** Two alcohol
means, 12.9683 from the training rows and 13.0006 from everything, and
`identical? False`. Rounded to one decimal both are 13.0. The leak does not
announce itself — no warning, no traceback, no number that looks odd. It
produces a slightly different number and a test score that is slightly too
optimistic in a direction you will not notice. That invisibility is why the
structural fix — put the scaler in the pipeline — beats the procedural one —
remember to scale in the right order.

**Named steps.** `pipe.named_steps["clf"]` reaches the fitted classifier so you
can read `n_iter_` off it. Note `pipe.coef_` does not exist — the pipeline is
not the classifier; go through the step with `pipe.named_steps["clf"].coef_`.

## Download and run

Download
[exercise-04-pipeline-solution.py](./exercise-04-pipeline-solution.py)
and run it:

```bash
python exercise-04-pipeline-solution.py
```

The wine data ships with scikit-learn. The split and the classifier are both
seeded, so the accuracies and the alcohol means print identically each run. You
will see one `ConvergenceWarning` on the error stream from the deliberately
unscaled first model — that is the symptom the exercise is about, not a bug in
the download.

## Common bugs to catch

- **`TypeError: All intermediate steps should be transformers and implement fit
  and transform or be the string 'passthrough' ...`** You put the classifier
  first and the scaler second. `Pipeline` runs the steps top to bottom and only
  the last one may be an estimator; everything before it has to be a transformer.
- **`KeyError: 'clf'`.** You used `make_pipeline`, which auto-names the steps
  `standardscaler` and `logisticregression`, then reached for your own names.
  Print `pipe.named_steps.keys()` when unsure. Related:
  `AttributeError: 'Pipeline' object has no attribute 'coef_'` — the pipeline is
  not the classifier; go through `pipe.named_steps["clf"].coef_`.
- **`identical?` prints `True`.** You fitted the comparison scaler on `x_train`
  (`StandardScaler().fit(x_train)`), the same rows as the pipeline. The leaky one
  must be fit on the full `x`, before any split — that is the whole contrast.
- **Raising `max_iter` on the bare model to silence the warning.** It works, and
  it removes your only visible evidence of the problem while leaving the cause in
  place. The solver still has to crawl across a badly conditioned surface; you
  just gave it more time to. Scaling removes the cause: seventeen iterations.
  Knowing which of the two you did is the exercise.
- **`sklearn.exceptions.NotFittedError: Pipeline is not fitted yet.`** You called
  `pipe.score` before `pipe.fit`, usually because the pipeline was rebuilt
  between the fit and the score. Older scikit-learn phrased this as
  `This Pipeline instance is not fitted yet.`; 1.6.1 shortened it.
- **`ValueError: Expected 2D array, got 1D array instead.`** You passed
  `x["alcohol"]` while experimenting with a single feature. `x[["alcohol"]]`
  gives the DataFrame the pipeline needs — and note the traceback points at
  `StandardScaler`, so you go looking in the wrong place.

## Under the hood

<details>
<summary>Under the hood — what "leakage" costs, and why a pipeline is the real fix</summary>

Leakage is any time information from the test set sneaks into training. Fitting
a scaler on all the data before splitting is the gentlest possible example, and
that is what makes it a good teacher: the harm is real but almost invisible.

The concrete mechanism: `StandardScaler.fit(x)` computes each column's mean and
standard deviation over all 178 wines. Those numbers then get baked into how
*every* row is transformed, including the 45 you set aside to grade yourself on.
So each test wine is being scaled using a mean that was computed partly from
itself and its neighbours. The test set was supposed to stand in for wine you
have never seen; now it has whispered its own average into the training process.
Your reported accuracy drifts a little above what the model will actually
achieve on truly new wine, and nothing warns you.

Why not just "remember to scale after splitting"? Because you will forget, and
worse, the day you switch to cross-validation you have to re-scale correctly
inside every one of five folds, by hand, five chances to slip. The pipeline
turns a rule you must remember into a structure that cannot be gotten wrong:
`cross_val_score(pipe, x, y, cv=5)` refits the scaler from each fold's own
training rows automatically. This is the whole reason `Pipeline` exists — not to
save typing, but to make the correct order the only order. In a production
system the same object, saved with `joblib`, guarantees that live data is
scaled by the exact numbers the model was trained against, in the exact order,
forever.

</details>

## Acceptance checklist

- [ ] The unscaled run shows a `ConvergenceWarning` and an iteration count
      equal to its cap (100 of 100).
- [ ] The pipeline run shows no warning and a much lower iteration count.
- [ ] The pipeline's accuracy is at least as good as the unscaled model's.
- [ ] `identical?` prints `False`.
- [ ] You can explain, in one sentence, what information leaks when a scaler
      is fit before the split.
- [ ] Two consecutive runs print the same accuracies.
- [ ] 133 training rows and 45 test rows (add `print(len(x_train), len(x_test))`
      to see them).
- [ ] Committed with a message like `Add Week 14 exercise 4: scaling inside a pipeline`.

## Stretch

- **Cross-validate the pipeline.** `cross_val_score(pipe, x_train, y_train,
  cv=5)` gives roughly `[1.0, 1.0, 0.963, 1.0, 0.962]`, mean about 0.985. Each
  fold refits the scaler from that fold's own training rows. Hand
  `cross_val_score` a pre-scaled `x` and every one of the five folds leaks —
  quietly, five times over. This is the case where the pipeline is not
  convenience but correctness.
- **Add an imputer.** `SimpleImputer(strategy="median")` as a third step in
  front of the scaler runs end to end even after you poke `NaN` values into a
  copy of the data. Each new step is one more thing you no longer have to
  remember to apply to production input in the right order.
- **A tree does not care.** `DecisionTreeClassifier(max_depth=3,
  random_state=42)` scores the same scaled and unscaled. Trees split on
  thresholds, and a threshold on proline works the same whether proline runs to
  1,680 or to 2.4 standard deviations. Scaling never hurts a tree; it just does
  nothing.

Last one: [Exercise 5 — Reading the Confusion Matrix](./exercise-05-confusion-matrix.md),
where a 95% accurate model turns out to be useless.
