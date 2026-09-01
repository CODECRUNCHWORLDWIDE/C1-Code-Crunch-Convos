# Exercise 5 — Reading the Confusion Matrix

> **Topic:** Why 95% accuracy can mean the model found nothing, and how the matrix shows it
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** every exercise so far has ended with a single accuracy number, and on balanced data that was fine. It is about to stop being fine. This is the exercise where you learn to distrust your own headline metric, and it is the last thing standing between you and shipping a model that quietly fails the people it was built for.

## The Brief

A clinic wants a first-pass screening tool. Out of every hundred people
screened, about five have the condition; ninety-five do not. The clinic hands
you the data and asks for a model.

You will build two. The first is a `DummyClassifier` that ignores the
measurements entirely and answers "no condition" every single time. It scores
95% accuracy. It has found nothing, learned nothing, and would harm every
patient who has the condition. The second is a real logistic regression, and it
also lands in the mid-nineties. **The two are not close to equivalent**, and the
accuracy number cannot tell them apart. The confusion matrix can, in one glance.

A confusion matrix is just a 2×2 tally: of the people who truly had the
condition, how many did we catch and how many did we miss; and of the healthy
people, how many did we wave through and how many did we needlessly alarm. Four
numbers. Accuracy squashes all four into one and throws away the only two that
matter here.

The data is generated inside the script with
`sklearn.datasets.make_classification`, so there is nothing to download and the
class balance is exactly what we asked for: 950 negatives, 50 positives.

## Starter

Copy this into `exercise-05-confusion-matrix.py` and fill in the `TODO`s.

```python
"""exercise-05-confusion-matrix.py — accuracy hides what the matrix shows.

Screens a synthetic population where only 5% have the condition.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.20
N_SAMPLES = 1000
N_FEATURES = 6
LABELS = ["no condition", "condition"]


def make_population() -> tuple[pd.DataFrame, pd.Series]:
    """Generate a 95/5 imbalanced screening dataset as a frame and a series."""
    features, target = make_classification(
        n_samples=N_SAMPLES, n_features=N_FEATURES,
        n_informative=3, n_redundant=1, n_classes=2,
        weights=[0.95, 0.05], flip_y=0.0, class_sep=0.8,
        random_state=RANDOM_STATE,
    )
    columns = [f"marker_{i}" for i in range(N_FEATURES)]
    return pd.DataFrame(features, columns=columns), pd.Series(target, name="condition")


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy, the confusion matrix, and the per-class report."""
    print(f"--- {name} ---")
    print(f"accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_true, y_pred))
    # TODO: print classification_report with target_names=LABELS and zero_division=0.


def main() -> None:
    """Compare a do-nothing baseline against a real classifier."""
    x, y = make_population()
    print(f"class balance: {y.value_counts().sort_index().to_dict()}")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"test set: {y_test.value_counts().sort_index().to_dict()}")

    dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy.fit(x_train, y_train)
    report("always says 'no condition'", y_test, dummy.predict(x_test))

    # TODO: fit a LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    # and call report() on its test predictions.

    # TODO: pull tn, fp, fn, tp out of the logistic regression's matrix with
    # .ravel() and print how many people with the condition were missed.


if __name__ == "__main__":
    main()
```

One deliberate change from the older starter: the balance is printed with
`y.value_counts().sort_index().to_dict()`, not `dict(y.value_counts())`. Under
numpy 2.x the plain `dict(...)` renders as `{0: np.int64(950), 1: np.int64(50)}`
— the counts are right, the repr is noisy. `.sort_index().to_dict()` converts
the values to built-in `int` and pins the key order at 0 then 1, so the line is
clean on any version.

## Requirements

1. `make_population` returns a DataFrame of six `marker_*` columns and a
   Series named `condition`. The balance is exactly 950 / 50.
2. The split is stratified, so the test set holds exactly 190 negatives and 10
   positives.
3. `report` prints accuracy, the raw 2×2 matrix, and
   `classification_report(..., target_names=LABELS, zero_division=0)`.
4. Both models are reported through the same function, so the two blocks are
   directly comparable line for line.
5. The final lines unpack the logistic regression's matrix with
   `tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()` and print a
   sentence naming the number of missed cases, for example
   `missed 4 of 10 people who had the condition`.

## Constraints

- **`flip_y=0.0` and fixed `weights`.** These pin the class counts to exactly
  950 and 50, so the dummy model's accuracy is exactly 190/200 and you can check
  the arithmetic by hand. Leave `flip_y` at its default and a couple of percent
  of labels get scrambled (943 and 57 on this seed), and the clean example stops
  being clean.
- **Pass `random_state` to the data generator, the split, and both models.**
  This script *creates* its data, so an unpinned seed produces a different
  thousand people — nothing about a rerun is comparable to the run before it, and
  a write-up describing "the four people this model missed" would describe a
  population that no longer exists. Reproducibility here is not a nicety; without
  it there is no experiment.
- **`stratify=y` is mandatory, not optional, on imbalanced data.** With only
  fifty positives in a thousand rows, an unstratified 20% test split could hand
  you three positives, or seventeen. Recall computed on three people is not a
  measurement.
- **`zero_division=0` on the report, and read the warning it silences first.**
  The dummy model never predicts the positive class, so its precision there is
  `0/0`. Setting it to zero keeps the table readable — but 0.00 now means
  "undefined" in that cell and "genuinely zero" in the recall cell beside it, and
  only having read the warning do you know which is which.

## Expected output

The whole dummy block is fixed by construction — 190 and 10 come from the
stratified split, and a model that always answers `0` can produce no other
matrix. The logistic regression's accuracy, 0.980, is approximate; its four
cells have fixed row sums (190 and 10) but the individual numbers can move a case
across the diagonal on a different build. Do not quote the 0.980 without the
recall beside it — that is the entire exercise.

```text
$ python exercise-05-confusion-matrix-solution.py
class balance: {0: 950, 1: 50}
test set: {0: 190, 1: 10}
--- always says 'no condition' ---
accuracy: 0.950
confusion matrix (rows = actual, cols = predicted):
[[190   0]
 [ 10   0]]
              precision    recall  f1-score   support

no condition       0.95      1.00      0.97       190
   condition       0.00      0.00      0.00        10

    accuracy                           0.95       200
   macro avg       0.47      0.50      0.49       200
weighted avg       0.90      0.95      0.93       200

--- logistic regression ---
accuracy: 0.980
confusion matrix (rows = actual, cols = predicted):
[[190   0]
 [  4   6]]
              precision    recall  f1-score   support

no condition       0.98      1.00      0.99       190
   condition       1.00      0.60      0.75        10

    accuracy                           0.98       200
   macro avg       0.99      0.80      0.87       200
weighted avg       0.98      0.98      0.98       200

caught 6 of 10 people who had the condition
missed 4 of 10 people who had the condition
sent 0 healthy people for a second test
```

Look at the dummy model's two rows. Ninety-five percent accurate. Recall on the
condition: **zero**. It found none of the ten. If that number had been the only
one on the slide, the clinic would have bought it. The logistic regression does
better — recall 0.60, six of the ten found — but three points of accuracy is all
that separates "useless" from "moderately useful", and three points is the only
thing accuracy has to say about a difference that, in the clinic, is the
difference between everyone going home undiagnosed and most of them being caught.

## Why accuracy misleads here, and what a miss costs

Accuracy is `correct / total`. When 95% of the population is negative, 95% of
the answer is decided before the model does anything at all. A model that is
completely blind to the condition still lands in the mid-nineties, because it is
being graded almost entirely on people it was never really being asked about.
The metric is dominated by the majority class: it reports confidently on the
easy part of the problem and stays silent about the hard part. The question the
clinic actually asked — of the ten people who had it, how many did we find? — is
recall on the minority class, and it is the number accuracy averages away.

The two kinds of mistake are not equal either, and no metric knows that unless
you tell it. A **false positive** sends a healthy person for a second, more
expensive test: an anxious week, a bill, an afternoon off work. Those costs are
real and mostly recoverable. A **false negative** sends someone home with a
clean result they should never have been given. They stop looking. They
attribute the next symptom to something else. They come back later, if they come
back, with a condition that has advanced and is harder to treat — and nothing in
your evaluation ever registered that harm, because in your accuracy number that
person was one of two hundred, a rounding error in the third decimal place. On
this run the model missed four such people and inconvenienced nobody: zero false
positives. For a screening tool that is not the safe trade, it is the wrong way
round.

When costs are asymmetric like this, you tune for recall on the minority class,
you accept more false positives, and you say so out loud in the write-up rather
than letting the reader assume a balanced objective. Lower the decision
threshold on this model from 0.50 to 0.15 and recall climbs from 0.60 to 0.90 at
a cost of six false positives out of 190 healthy people — nine of the ten found,
six people sent for a second test that turns out fine. State that trade
explicitly and let the clinic decide; it is their call, not yours. And when you
cannot get recall high enough at any threshold you would defend, the honest
engineering answer is that the model is not ready to screen anyone — not that
98% sounds good in a meeting.
[Lecture 3](../lecture-notes/03-pipelines-evaluation-and-ethics.md#when-not-to-deploy-a-model)
is explicit that declining to ship is a valid engineering decision, and this is
the shape of the situation where you make it.

## Steps

1. Create the file, paste the starter, and run it before filling in anything.
   The dummy block should already print, and it should already look wrong.
2. Check the balance line by hand: 950 + 50 = 1000, and 5% of 200 is 10. The
   library and the arithmetic agree.
3. Add the `classification_report` line to `report`. Run again and read the
   `condition` row for the dummy model. Three zeros.
4. Fit the logistic regression and report it. Compare the two blocks side by
   side — similar accuracy lines, very different `condition` rows.
5. Unpack the matrix with `.ravel()` and print the missed-cases sentence. Say
   it out loud with real nouns in it: "this model sends N people with the
   condition home."
6. Shift the decision threshold: take `model.predict_proba(x_test)[:, 1]` and
   predict positive above `0.15` instead of the default `0.50`. Re-run the
   tally. Recall goes up, precision goes down. Decide which of the three you
   would defend to the clinic.

## The Solution

```python
"""exercise-05-confusion-matrix.py — accuracy hides what the matrix shows.

Screens a synthetic population where only 5% have the condition.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.20
N_SAMPLES = 1000
N_FEATURES = 6
LABELS = ["no condition", "condition"]


def make_population() -> tuple[pd.DataFrame, pd.Series]:
    """Generate a 95/5 imbalanced screening dataset as a frame and a series."""
    features, target = make_classification(
        n_samples=N_SAMPLES, n_features=N_FEATURES,
        n_informative=3, n_redundant=1, n_classes=2,
        weights=[0.95, 0.05], flip_y=0.0, class_sep=0.8,
        random_state=RANDOM_STATE,
    )
    columns = [f"marker_{i}" for i in range(N_FEATURES)]
    return pd.DataFrame(features, columns=columns), pd.Series(target, name="condition")


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy, the confusion matrix, and the per-class report."""
    print(f"--- {name} ---")
    print(f"accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred, target_names=LABELS, zero_division=0))


def main() -> None:
    """Compare a do-nothing baseline against a real classifier."""
    x, y = make_population()
    print(f"class balance: {y.value_counts().sort_index().to_dict()}")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"test set: {y_test.value_counts().sort_index().to_dict()}")

    dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy.fit(x_train, y_train)
    report("always says 'no condition'", y_test, dummy.predict(x_test))

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report("logistic regression", y_test, predictions)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
    print(f"caught {tp} of {tp + fn} people who had the condition")
    print(f"missed {fn} of {tp + fn} people who had the condition")
    print(f"sent {fp} healthy people for a second test")


if __name__ == "__main__":
    main()
```

**Everything about the population is nailed down, and that is what makes the
comparison a comparison.** `weights=[0.95, 0.05]` sets the ratio and
`flip_y=0.0` switches off label noise, so the balance is exactly 950 and 50.
`stratify=y` then forces the test set to exactly 190 and 10. Because those
numbers are fixed, the dummy classifier's accuracy is exactly 190/200 = 0.950
and its matrix is exactly `[[190, 0], [10, 0]]`. You can check the whole
baseline by hand, so when the real model's numbers arrive you already know what
they are being measured against.

**`random_state` on the generator matters more here than anywhere else this
week.** This script does not load data, it makes it. An unpinned seed does not
merely reshuffle the split — it produces a different thousand people, and a
rerun is not comparable to the run before it.

**One `report` function, called twice.** The two blocks are comparable line for
line because they come from the same code. Write the printing twice and you will
eventually format one differently, and the difference you notice will be an
artefact of your formatting rather than of the models.

**`zero_division=0`, but only after you have seen the warning.** The dummy model
never predicts the positive class, so precision for that class is `0/0`. Without
the argument scikit-learn tells you so, three times over. Passing it fills the
cell with 0.00 — which is why you read the warning first, so you know that cell
means "undefined", not "zero".

**The last three lines force the finding into nouns.** `matrix.ravel()` flattens
`[[tn, fp], [fn, tp]]` into four values in reading order, and the sentences it
feeds — *caught 6 of 10*, *missed 4 of 10*, *sent 0 healthy people for a second
test* — are the version of this result you could actually say to the clinic.
"0.980" is not.

## Download and run

Download
[exercise-05-confusion-matrix-solution.py](./exercise-05-confusion-matrix-solution.py)
and run it:

```bash
python exercise-05-confusion-matrix-solution.py
```

The population is generated inside the file from a pinned seed, so there is
nothing to download and the same thousand people appear on every machine. Both
models and the split are seeded too, so the two report blocks print identically
each run.

## Common bugs to catch

- **The matrix comes out transposed.** You called `confusion_matrix(y_pred,
  y_true)`. The order is `(y_true, y_pred)`, always, and getting it backwards
  swaps the two off-diagonal cells — in this scenario, swaps "annoyed four
  healthy people" with "sent four sick people home", and nothing warns you.
  Truth first, prediction second, the same convention as `r2_score` in
  Exercise 1.
- **`ValueError: not enough values to unpack (expected 4, got 1)`** from
  `.ravel()`. The matrix collapsed because only one class appeared in both
  `y_test` and the predictions — usually because you sliced the data down while
  experimenting, or dropped `stratify` and got unlucky. Print
  `confusion_matrix(...).shape` before unpacking. (An older page quotes this as
  `too many values to unpack (expected 4)`; Python raises the "not enough" form
  when the matrix is *smaller* than expected, which is the direction this failure
  actually goes.)
- **`UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in
  labels with no predicted samples.`** Expected on the dummy model — it never
  predicts the positive class. Pass `zero_division=0` *after* you have read it.
- **Dropping `stratify=y`.** The test set no longer holds exactly ten positives
  — across the first six seeds it ranges from nine to fourteen — so the two
  models are graded on different scales and the hand-checkable 190/200 baseline
  is gone. On imbalanced data `stratify` is what makes the measurement a
  measurement.
- **Recall on the condition is exactly 0.0 for the logistic regression too.**
  Possible, and worth pausing on rather than fixing in a hurry — with
  `class_sep=0.8` the classes genuinely overlap. Try `class_weight="balanced"`
  and watch recall jump while precision collapses. Neither version is "the right
  answer"; the trade is the answer.

## Under the hood

<details>
<summary>Under the hood — precision, recall, and the two ways a screen can be wrong</summary>

The confusion matrix's four cells have names, and once you know them the
`classification_report` stops being a wall of numbers.

- **True positive (TP):** had the condition, model said so. A catch.
- **False negative (FN):** had the condition, model said healthy. A miss — the
  dangerous one here.
- **False positive (FP):** healthy, model said condition. A false alarm.
- **True negative (TN):** healthy, model said so. Correct all-clear.

Two ratios are built from these, and they answer different questions:

- **Recall = TP / (TP + FN)** — of everyone who truly had it, what fraction did
  we catch? This is the screening question. The dummy model's recall is
  0/(0+10) = 0.00. The real model's is 6/(6+4) = 0.60.
- **Precision = TP / (TP + FP)** — of everyone we flagged, what fraction really
  had it? This is the "how much do we trust an alarm?" question. The real model's
  precision is 6/(6+0) = 1.00 here, because it raised no false alarms.

There is a tension between them. Flag more people and you catch more of the sick
(recall up) but raise more false alarms (precision down); flag fewer and the
reverse. The **F1 score** is their harmonic mean — `2 · P · R / (P + R)` — a
single number that only stays high when *both* are high, which is why F1 on the
minority class is a far more honest headline than accuracy on an imbalanced
problem. And the whole trade is governed by the decision threshold: `predict`
uses 0.50, but `predict_proba` hands you the raw probability so you can move that
line yourself, wherever the costs of a miss and a false alarm put it.

</details>

## Acceptance checklist

- [ ] The class balance prints as exactly 950 negatives and 50 positives.
- [ ] The test set prints as exactly 190 and 10.
- [ ] The dummy model scores exactly 0.950 with recall 0.00 on the condition.
- [ ] The logistic regression's matrix rows sum to 190 and 10.
- [ ] The missed-cases sentence prints with a real number in it.
- [ ] You can say in one sentence why the clinic should not buy the dummy
      model, without using the word "accuracy".
- [ ] Committed with a message like `Add Week 14 exercise 5: confusion matrix and imbalance`.

## Stretch

- **Sweep the decision threshold.** Take `model.predict_proba(x_test)[:, 1]` and
  call positive anything at or above a threshold, from 0.05 up to 0.50. Recall
  first reaches 0.90 at a threshold of 0.15, costing six false positives. Watch
  accuracy on the way: it *rises* slightly as the threshold drops to 0.20, then
  collapses at 0.05. It is not tracking the thing you care about in either
  direction.
- **More extreme imbalance.** Regenerate with `weights=[0.99, 0.01]` and the
  dummy model scores 99%. The more skewed the population, the better accuracy
  looks and the less it means.
- **`class_weight="balanced"`.** Instead of moving the threshold, tell the
  classifier the classes matter equally during fitting. Recall jumps to about
  0.90, precision collapses to about 0.24, accuracy falls twelve points. Nine of
  ten found, at the cost of twenty-eight healthy people sent for a second test.
  **The trade is the answer**, and choosing a point on it is a decision about
  people, not a hyperparameter search.
- **Write a five-line model card:** what it predicts, on whom it was trained,
  its recall on the positive class, its known failure mode, and who a patient
  contacts to dispute a result. The first four are in the transcript above. The
  last one is not in your code at all — it is a fact about the organisation
  deploying the model, and that is exactly why it is the line that gets left out.

That is the week's exercise set. Harder, less-guided work is waiting in
[the challenges](../challenges/README.md).
