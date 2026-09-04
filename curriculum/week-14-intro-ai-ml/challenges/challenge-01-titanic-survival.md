# Challenge 1 — Predict Titanic Survival, Then Audit It

> **Topic:** Mixed-type preprocessing in a ColumnTransformer, two models, and a fairness audit by sex
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the exercises fed you clean, all-numeric data. Real data is not like that — it has words in some columns, numbers in others, and holes where nobody wrote anything down. This is the first problem where preprocessing is most of the work, and it is also the first where the interesting question is not "how accurate?" but "accurate *for whom?*".

## The Brief

Given a passenger's details — age, sex, ticket class, fare paid, port they got
on at, family aboard — predict whether they survived the sinking of the Titanic.
It is the most famous beginner classification problem there is, which means once
you have a number you can compare it to thousands of write-ups online.

Two things make it more than a toy. First, the columns are a mix: `sex` and
`embarked` are words, `age` and `fare` are numbers, and `age` is missing for a
fifth of the passengers. You cannot hand words or holes to a model — every value
has to become a number first, and the missing ones have to be filled in. Second,
the strongest signal in the data is `sex`, and that turns the project into an
ethics problem the moment you look closely: a model that predicts "female ⇒
survived" is not discovering a fact about biology, it is learning that the 1912
evacuation put women and children in the lifeboats first. Whether that is a
pattern you want a model repeating depends entirely on what you plan to do with
it.

**A note on the data.** The real Titanic table needs a download, and this course
runs offline and gives the same numbers on every machine. So the shipped answer
*generates* 500 passengers from a fixed seed with the real historical pattern
built in — the same columns, the same missing ages, the same strong sex effect.
Your own version can load the real `seaborn` dataset if you have it; the pipeline
you build is identical either way.

## Starter

Copy this into `challenge-01-titanic-survival.py`. The data generator and the
column lists are given; you fill in the pipeline and the fairness audit.

```python
"""challenge-01-titanic-survival.py — predict survival, then audit by sex."""

from __future__ import annotations

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
NUMERIC_COLS = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_COLS = ["sex", "embarked", "pclass"]


def make_titanic(seed: int = RANDOM_STATE, n: int = 500) -> pd.DataFrame:
    """Generate a Titanic-shaped table: same columns, same survival pattern."""
    rng = np.random.default_rng(seed)
    sex = rng.choice(["male", "female"], size=n, p=[0.64, 0.36])
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
    true_age = rng.normal(29.0, 14.0, n).clip(0.5, 80.0)
    sibsp = rng.integers(0, 4, n)
    parch = rng.integers(0, 3, n)
    base_fare = np.select([pclass == 1, pclass == 2, pclass == 3], [84.0, 21.0, 14.0])
    fare = (base_fare * rng.uniform(0.5, 1.8, n)).round(2)
    embarked = rng.choice(["S", "C", "Q"], size=n, p=[0.72, 0.19, 0.09])
    female, first, third = (sex == "female"), (pclass == 1), (pclass == 3)
    child = true_age < 12
    logit = (-1.0 + 2.2 * female + 0.9 * first - 0.6 * third
             + 1.0 * child - 0.01 * (true_age - 29.0))
    survived = (rng.random(n) < 1.0 / (1.0 + np.exp(-logit))).astype(int)
    frame = pd.DataFrame({"survived": survived, "pclass": pclass, "sex": sex,
                          "age": true_age, "sibsp": sibsp, "parch": parch,
                          "fare": fare, "embarked": embarked})
    frame.loc[rng.random(n) < 0.20, "age"] = np.nan
    frame.loc[rng.random(n) < 0.02, "embarked"] = np.nan
    return frame


def build_pipeline(classifier) -> Pipeline:
    """Wrap preprocessing and *classifier* in one leak-free estimator."""
    # TODO: a numeric branch (impute median -> scale) and a categorical branch
    # (impute most_frequent -> one-hot), joined by a ColumnTransformer, then
    # the classifier as the final step.
    raise NotImplementedError


def main() -> None:
    df = make_titanic()
    x = df.drop(columns=["survived"])
    y = df["survived"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    # TODO: fit a LogisticRegression pipeline and a DecisionTree pipeline,
    # print each one's test accuracy, and print the confusion matrix of the best.

    # TODO: fairness audit — split the test set into male and female, and print
    # precision, recall and accuracy for each group and for everyone.


if __name__ == "__main__":
    main()
```

## Requirements

1. **Inspect first.** Print the survival counts, how many ages and ports are
   missing, and the survival rate broken down by `sex` and by `pclass`. Notice
   what you find before you model anything.
2. **Impute the holes.** `age` is missing for many passengers; fill it with the
   median. Fill missing `embarked` with the most frequent port.
3. **Encode the words.** Use `OneHotEncoder` for `sex`, `embarked`, and `pclass`
   inside a `ColumnTransformer` so it only touches those columns.
4. **One Pipeline.** Preprocessing and classifier in a single estimator, so the
   imputers and scaler never see the test rows.
5. **Two classifiers.** `LogisticRegression` and `DecisionTreeClassifier`,
   trained on the same split, compared on test accuracy.
6. **Evaluate honestly.** Print the confusion matrix on a held-out test set.
   Use `random_state=42` everywhere so the numbers reproduce.
7. **Fairness audit.** Compute precision and recall **separately for male and
   female passengers** in the test set. Comment on what you see.
8. **Save and reload.** `joblib.dump` the best pipeline and confirm the reloaded
   copy predicts identically.

## Constraints

- **The whole preprocessing must live inside the pipeline.** If you impute or
  scale before the split, the median and the column means are computed partly
  from the test rows — the leak from Exercise 4, now with more moving parts.
- **Pin `random_state` on the split, both models, and the data generator.** This
  problem *builds* its data; an unpinned generator gives you 500 different people
  each run and a fairness audit you cannot repeat or defend.
- **Do not feed the model columns it could not know in advance.** The real
  dataset has columns like `alive` and `class` that are just the answer in
  disguise — using them is leakage. Here the generator only hands you honest
  features, but the habit of asking "could I know this *before* the prediction?"
  is the point.
- **Keep the positive class straight.** Survived is `1`. Precision and recall in
  the audit are about the survivors, so pass `survived` as the positive label
  and read every metric that way.

## Expected output

The survival rates and the fairness gap are the finding; the accuracy is
approximate (this synthetic set is noisier than the real one, which is why it
lands near 0.71 rather than the 0.80 you will read about online). With every seed
pinned the whole run is identical on every machine.

```text
$ python challenge-01-titanic-survival.py
passengers: 500   survived: 231   died: 269
missing ages: 96   missing embarked: 11
survival rate by sex:
  female 0.78
  male   0.28
survival rate by class:
  class 1 0.64
  class 2 0.54
  class 3 0.35
--- model comparison (accuracy on the held-out test set) ---
  logreg accuracy: 0.710
  tree   accuracy: 0.710
--- best model: logreg ---
confusion matrix (rows = actual, cols = predicted):
[[46  8]
 [21 25]]
--- fairness audit: metrics per group (positive class = survived) ---
| group  |   n | precision | recall | accuracy |
|--------|-----|-----------|--------|----------|
| all    | 100 |      0.76 |   0.54 |     0.71 |
| male   |  71 |      0.50 |   0.09 |     0.68 |
| female |  29 |      0.79 |   1.00 |     0.79 |
saved and reloaded pipeline predicts identically: True
```

The overall accuracy hides the whole story, which is exactly the lesson from
Exercise 5 wearing new clothes. Read the last two rows instead: the model
catches **every** surviving woman (recall 1.00) and almost **no** surviving man
(recall 0.09). It has not learned "who survives"; it has learned "guess female ⇒
survived, male ⇒ died" and ridden the base rates. That is a fine score and a
model you should think hard about before deploying.

## Steps

1. Paste the starter and run it — `make_titanic` works, and `build_pipeline`
   will raise `NotImplementedError`.
2. Fill in `build_pipeline`: a numeric branch (`SimpleImputer(strategy="median")`
   then `StandardScaler`), a categorical branch
   (`SimpleImputer(strategy="most_frequent")` then `OneHotEncoder`), joined by a
   `ColumnTransformer`, with the classifier as the last step.
3. Add the inspection prints, then the two-model comparison and the confusion
   matrix.
4. Add the fairness audit last. Mask the test rows by `x_test["sex"]` and score
   each group on its own slice.
5. Read the male and female rows against each other. Write one paragraph: is the
   model discovering signal, or repeating a biased history? What is the
   difference, and does it matter for how you would use it?

## The Solution

```python
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
```

**The `ColumnTransformer` is the new idea, and it is a router.** Numbers and
words cannot be treated the same way — you scale a number, you one-hot a word —
so the transformer sends each list of columns down its own little pipeline and
then glues the results back into one wide numeric table for the classifier. The
numeric branch fills missing ages with the median and scales; the categorical
branch fills missing ports with the commonest one and turns each category into
its own 0/1 column. All of it sits *inside* the final `Pipeline`, so when you
call `pipe.fit(x_train, ...)` the median, the mode, and the column means are all
learned from the training rows only. That is the Exercise 4 leak lesson, now with
imputers and an encoder along for the ride.

**Two classifiers, same wrapper.** `build_pipeline` takes the classifier as an
argument, so the exact same preprocessing feeds both models and the comparison is
fair. They tie here at 0.710, which is itself a small lesson: with a dominant
feature like `sex`, the choice of algorithm barely matters — a straight line and
a shallow tree both find the same easy split.

**The audit is the real work.** `group_metrics` slices the test set by sex and
scores each slice on its own. The gap it exposes — women's survival caught
perfectly, men's caught almost never — is not a bug to fix. It is the model
honestly reflecting a training set where 78% of women lived and 72% of men died.
Whether that is acceptable depends entirely on the decision the model is feeding.
For a history lesson, fine. For anything that allocates a real resource to a real
person, a model that is right 79% of the time for one group and effectively
refuses to predict survival for the other is a model you have to justify or not
ship.

**The joblib round-trip** dumps the whole fitted pipeline — imputers, encoder,
scaler, classifier, and the order they run in — to one file and reloads it, then
checks the reloaded copy predicts the same. That single file is what
"deploying a model" actually means: not the classifier alone, but every
preprocessing decision travelling with it.

## Run it

Copy the worked answer on this page into `challenge-01-titanic-survival.py` and run it:

```bash
python challenge-01-titanic-survival.py
```

It needs `scikit-learn`, `pandas`, `numpy`, and `joblib`, all of which you
already have. There is nothing to download: the 500 passengers are generated from
a fixed seed inside the file, and the joblib file is written to a temporary
folder that is deleted on the way out. The `-solution` suffix keeps it clear of
your own `challenge-01-titanic-survival.py`.

## Common bugs to catch

- **`ValueError: could not convert string to float: 'male'`.** You handed the raw
  frame straight to `LogisticRegression` without the `ColumnTransformer`, so the
  word columns reached the model unencoded. Everything categorical has to become
  a number first.
- **`ValueError: Input X contains NaN.`** Your imputers are not running before
  the model — usually because you scaled or encoded *outside* the pipeline and
  left the holes in. Put every preprocessing step inside the `Pipeline` so `fit`
  fills them in first.
- **The fairness rows all look identical to the `all` row.** You masked
  `predictions` with a boolean `Series` that carried the test set's original
  index, not a positional array, so pandas aligned it oddly. Convert the mask
  with `.to_numpy()` before indexing the NumPy prediction array, as
  `group_metrics` does.
- **`UndefinedMetricWarning` / a group precision of 0.00.** A group the model
  never predicted as a survivor makes precision `0/0`. Pass `zero_division=0` and
  read the 0.00 as "the model flagged nobody here", not "the model was wrong
  about everyone".
- **Different accuracy every run.** A seed is missing somewhere — the split, a
  model, or the generator. Pin all three; this problem manufactures its own data,
  so the generator seed matters as much as the split seed.

## Under the hood

<details>
<summary>Under the hood — "discovering signal" versus "learning a biased label generator"</summary>

The requirement asks you to comment on whether the model is discovering signal or
learning from a biased label generator, and the two are worth pulling apart
because the whole ethics of deployment turns on the difference.

A model only ever learns the relationship between the features it is given and
the labels it is shown. It has no access to *why* the labels came out the way
they did. On the Titanic, the label "survived" was produced by a specific
historical process: an evacuation that, by custom and by order, loaded women and
children into the lifeboats first. So the strong `sex → survived` relationship in
the data is completely real — and it is a fact about *that evacuation*, not a
fact about who deserves to live or who is more valuable.

The model cannot tell those two readings apart, and neither can accuracy. If you
took this model and used it to decide who gets a lifeboat seat *next time*, you
would be taking a description of a past injustice-or-custom and turning it into a
rule that enforces it forward. That is the mechanism behind most real-world
algorithmic harm: a model trained on decisions made by biased humans reproduces
the bias with a clean technical veneer, and the veneer makes it harder to
challenge, because "the model said so" sounds neutral in a way "the 1912 White
Star Line said so" does not.

The engineering discipline this teaches: before you deploy, ask what process
generated your labels, and whether you would be comfortable automating that
process. A fairness audit — precision and recall per group, like the table above
— is how you *measure* the disparity. Deciding what to do about it is not a
scikit-learn question; it is a question about the people the model will touch.

</details>

## Acceptance checklist

- [ ] Missing ages and ports are imputed inside the pipeline, never before the
      split.
- [ ] `sex`, `embarked`, and `pclass` are one-hot encoded via a
      `ColumnTransformer`.
- [ ] Two classifiers are trained on the same split and compared on test
      accuracy.
- [ ] A confusion matrix prints for the chosen model.
- [ ] Precision and recall print separately for male and female passengers.
- [ ] The best pipeline saves with `joblib` and the reloaded copy predicts
      identically.
- [ ] Every `random_state` is pinned; two runs print the same numbers.
- [ ] You wrote one paragraph on the "signal vs biased history" question.

## Stretch

- **A fairer objective.** Retrain with `class_weight="balanced"` or by tuning the
  decision threshold, and watch the male recall climb while overall accuracy
  falls. Which trade would you defend, and to whom?
- **Feature importance.** Run `permutation_importance` on the fitted pipeline and
  confirm `sex` dominates. Compare its ranking to the logistic regression's
  coefficients — they do not always agree, and the disagreement is worth a
  paragraph.
- **A real interaction.** Build an `age × pclass` feature and refit. Does a
  young third-class passenger fare differently from what the two features predict
  separately?
- **The real data.** If you have `seaborn`, swap `make_titanic()` for
  `seaborn.load_dataset("titanic")`, keep the same columns, and see how much the
  accuracy and the fairness gap move. Write one line on why the synthetic set was
  noisier.

When you are done, write a one-paragraph reflection: best model, best score,
biggest surprise, and one thing you would do differently with more time. Then on
to [Challenge 2 — Customer segmentation with k-means](./challenge-02-kmeans-clustering.md).
