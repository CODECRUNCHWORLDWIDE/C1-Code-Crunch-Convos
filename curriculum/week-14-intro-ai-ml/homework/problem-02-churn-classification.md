# Problem 2 — Churn Classification: When Accuracy Lies

> **Topic:** Imbalanced classes, and why recall on the rare class is the number that matters
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** Exercise 5 showed you a confusion matrix on a rigged example. This is the same trap wearing a business suit. One of the two models you are about to train scores 84% and finds almost nobody, and the only way to see that is to stop reading accuracy and start reading recall.

## The Brief

"Churn" is a word businesses use for customers who leave. A streaming service has
5,000 subscribers. Every month a few cancel. If you could spot the ones who are
about to cancel *before* they do, you could send them a discount and keep them.
So you want a model that looks at a customer and says one of two things: **stays**
or **leaves**.

Here is the catch, and it is the whole homework. Only about **15 out of every 100**
customers churn. Imagine a lazy program that never thinks at all and just answers
"stays" for everybody. It would be right 85 times out of 100. Eighty-five percent!
That sounds like a good model. It is not a model at all — it is a rock with the
word "stays" painted on it, and it will never save a single customer, because it
never points at anyone.

So accuracy — the share of answers you got right — is a liar on data like this. It
is dominated by the boring majority. The number you actually need is **recall on
the churn class**: out of all the customers who really did leave, what fraction did
the model catch? A rock scores zero there, and that is exactly right.

You will train two models on the same customers. `LogisticRegression` draws one
straight boundary through the data and calls everything on one side a churner.
`RandomForestClassifier` grows two hundred decision trees, each one asking a
different chain of yes/no questions, and lets them vote. Then you will compare
them four ways — accuracy, precision, recall, F1 — and print a confusion matrix
for each, and decide which one you would actually ship.

**A note on the data.** Real churn tables belong to real companies and cannot be
downloaded here, so the 5,000 customers are generated in the file by
`make_classification`. Each has eight anonymous behavioural signals — think
"minutes watched last week", "days since last login" — named `signal_0` through
`signal_7`. Four of them genuinely carry information, two are copies mixed from
those four, and two are pure noise. The seed is pinned, so your numbers and the
numbers on this page are the same numbers.

## Starter

Copy this into `problem-02-churn-classification.py`. The data generator is given
to you; you fill in the models and the metrics. It runs as pasted — it just
prints the class balance and stops.

```python
"""problem-02-churn-classification.py — imbalanced churn: two models, the right metric."""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def make_churn(seed: int = RANDOM_STATE, n: int = 5000) -> pd.DataFrame:
    """A ~15% churn dataset of eight anonymous behavioural signals."""
    features, target = make_classification(
        n_samples=n, n_features=8, n_informative=4, n_redundant=2,
        weights=[0.85, 0.15], flip_y=0.0, class_sep=0.9, random_state=seed,
    )
    columns = [f"signal_{i}" for i in range(features.shape[1])]
    frame = pd.DataFrame(features, columns=columns)
    frame["churned"] = target
    return frame


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy plus precision/recall/F1 for the churn class (label 1)."""
    print(f"--- {name} ---")
    # TODO: print accuracy, then churn precision, recall and f1 (all to 3 places).
    # TODO: print the confusion matrix underneath, labelled rows=actual cols=predicted.


def main() -> None:
    df = make_churn()
    balance = df["churned"].value_counts().sort_index().to_dict()
    print(f"rows: {len(df)}   class balance (0=stay, 1=churn): {balance}")

    x = df.drop(columns=["churned"])
    y = df["churned"]
    # TODO: train_test_split with test_size=0.25, random_state=42, stratify=y.
    # TODO: fit LogisticRegression(max_iter=1000, random_state=42) and report() it.
    # TODO: fit RandomForestClassifier(n_estimators=200, random_state=42) and report() it.
    # TODO: print which model you would pick if a missed churner is the costly mistake.


if __name__ == "__main__":
    main()
```

## Requirements

1. Build the churn table with the `make_churn` above, unchanged. Print the row
   count and the class balance.
2. Split with `train_test_split(..., test_size=0.25, random_state=42, stratify=y)`
   and print the test set's churn balance.
3. Train a `LogisticRegression(max_iter=1000, random_state=42)`.
4. Train a `RandomForestClassifier(n_estimators=200, random_state=42)`.
5. For **each** model print four numbers to three decimal places: accuracy, and
   then precision, recall and F1 **for the churn class** (label `1`).
6. For **each** model print the confusion matrix, with a line saying which axis
   is which.
7. Print which model you would pick **if a missed churner costs the business more
   than a wasted discount**, and the recall that justifies the choice.
8. Hand in your own `problem-02-churn-classification.py` plus a short section in
   `report.md` justifying the pick in your own words. Say plainly what the losing
   model's accuracy hides.

## Constraints

- **Use `random_state=42` on the split, the logistic regression and the forest,
  and use exactly the `make_churn` given above.** Every number on this page came
  from those settings. Change one and your output will not match, and you will
  waste an hour hunting a difference you created yourself.
- **`stratify=y` on the split.** Without it, the split is free to hand the test
  set a different churn rate than the training set by luck, and then you are
  comparing your models on a slightly different problem than you trained them on.
  With 15% positives that wobble is big enough to matter.
- **`max_iter=1000` on the logistic regression.** The default is 100, and the
  solver has not settled by then on this data. You get a `ConvergenceWarning` and
  a model that stopped mid-thought.
- **Score the churn class, not the average.** `precision_score` and friends
  default to the positive label `1`, which is churn here. If you pass
  `average="macro"` you get a blend of both classes and the failure hides again.
- **Report accuracy anyway.** You are not banning it. You are showing it next to
  recall so a reader can see the gap for themselves — that contrast *is* the
  finding.

## Expected output

Every seed is pinned, so this run is the same on every machine. Treat the last
digit as soft — a different library build can move it — but the shape of the
result is fixed and is the whole point.

```text
$ python problem-02-churn-classification-solution.py
rows: 5000   class balance (0=stay, 1=churn): {0: 4250, 1: 750}
test set churn balance: {0: 1063, 1: 187}
--- LogisticRegression ---
accuracy : 0.840
churn precision: 0.118
churn recall   : 0.011
churn f1       : 0.020
confusion matrix (rows = actual, cols = predicted):
[[1048   15]
 [ 185    2]]
--- RandomForest ---
accuracy : 0.952
churn precision: 0.944
churn recall   : 0.722
churn f1       : 0.818
confusion matrix (rows = actual, cols = predicted):
[[1055    8]
 [  52  135]]
if a missed churner costs most, pick RandomForest: it catches the higher share of churners (recall 0.722)
```

Now stare at the logistic regression for a moment, because it is the most useful
failure in this week. Its accuracy is **0.840**. The rock that answers "stays" for
everybody would score 1063/1250 = **0.850**. The model is *worse than the rock*
and still looks respectable. Read its bottom row: 187 real churners, of whom it
caught **2**. Recall 0.011. If you shipped it, you would email a discount to
seventeen people, twelve of whom were never leaving, and lose 185 customers
without noticing.

The forest's bottom row reads `52 135`: it caught 135 of the 187, and missed 52.
Recall 0.722. Its top row reads `1055 8`: it only bothered 8 people who were
staying. Precision 0.944. That is a model you could actually hand to a retention
team.

**And a warning that applies to both numbers.** 0.952 and 0.722 are estimates
measured on 1,250 particular customers. Change the split and they move. They also
say nothing about *which* 52 churners were missed — if all 52 happened to be new
subscribers, the forest has a blind spot the accuracy score will never mention.
A score tells you how often, never who. Problem 6 is where you go looking.

## Steps

1. Paste the starter and run it. You should see the 4250/750 balance line.
2. Split the data with `stratify=y` and print the test balance. Confirm it is
   still about 15% churn.
3. Fill in `report()`: four metrics, then the matrix. Test it on one model first.
4. Fit the logistic regression and call `report()`. Look at the recall and resist
   the urge to assume you broke something. You did not — that is the lesson.
5. Fit the forest and call `report()`.
6. Compare the two recalls and print the recommendation line.
7. Write the `report.md` paragraph. Answer this exactly: *what does the logistic
   regression's 84% accuracy hide, and what would it cost the business?*

## The Solution

```python
"""problem-02-churn-classification.py — imbalanced churn: two models, the right metric.

A synthetic-but-realistic churn dataset (about 15% churn) built with
make_classification, so it runs offline and reproducibly. The lesson is Exercise
5's, applied: on imbalanced data accuracy flatters both models, and the number
that matters is recall on the churn class, because a missed churner is the
expensive mistake. Every seed is pinned.

Run it with::

    python problem-02-churn-classification-solution.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def make_churn(seed: int = RANDOM_STATE, n: int = 5000) -> pd.DataFrame:
    """A ~15% churn dataset of eight anonymous behavioural signals."""
    features, target = make_classification(
        n_samples=n,
        n_features=8,
        n_informative=4,
        n_redundant=2,
        weights=[0.85, 0.15],
        flip_y=0.0,
        class_sep=0.9,
        random_state=seed,
    )
    columns = [f"signal_{i}" for i in range(features.shape[1])]
    frame = pd.DataFrame(features, columns=columns)
    frame["churned"] = target
    return frame


def report(name: str, y_true: pd.Series, y_pred) -> None:
    """Print accuracy plus precision/recall/F1 for the churn class (label 1)."""
    print(f"--- {name} ---")
    print(f"accuracy : {accuracy_score(y_true, y_pred):.3f}")
    print(f"churn precision: {precision_score(y_true, y_pred, zero_division=0):.3f}")
    print(f"churn recall   : {recall_score(y_true, y_pred, zero_division=0):.3f}")
    print(f"churn f1       : {f1_score(y_true, y_pred, zero_division=0):.3f}")
    print("confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_true, y_pred))


def main() -> None:
    """Train two classifiers and compare them on the churn class, not accuracy."""
    df = make_churn()
    balance = df["churned"].value_counts().sort_index().to_dict()
    print(f"rows: {len(df)}   class balance (0=stay, 1=churn): {balance}")

    x = df.drop(columns=["churned"])
    y = df["churned"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    print(f"test set churn balance: {y_test.value_counts().sort_index().to_dict()}")

    logreg = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    logreg.fit(x_train, y_train)
    report("LogisticRegression", y_test, logreg.predict(x_test))

    forest = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    forest.fit(x_train, y_train)
    report("RandomForest", y_test, forest.predict(x_test))

    logreg_recall = recall_score(y_test, logreg.predict(x_test), zero_division=0)
    forest_recall = recall_score(y_test, forest.predict(x_test), zero_division=0)
    better = "RandomForest" if forest_recall > logreg_recall else "LogisticRegression"
    print(
        f"if a missed churner costs most, pick {better}: it catches the higher "
        f"share of churners (recall {max(logreg_recall, forest_recall):.3f})"
    )


if __name__ == "__main__":
    main()
```

**Why the straight line loses so badly.** Logistic regression draws one boundary
and puts everything on one side into the churn bin. It is trained to make the
*total* number of mistakes small — and with 85% of customers staying, the cheapest
way to make few mistakes is to say "stays" almost always. It is not broken. It is
doing exactly what it was asked to do, and what it was asked to do was the wrong
thing. This is the single most common way a beginner's classifier fails: the model
optimised the metric, and the metric was not the goal.

**Why the forest wins.** A decision tree carves the space into rectangles with
questions like "is `signal_3` above 0.7 and `signal_5` below −0.2?". A rectangle
can be small. It can wrap tightly around a pocket of churners that a single
straight line would have to swallow half the staying customers to reach. Two
hundred such trees, each grown on a different random resample of the rows and
allowed to look at a different random handful of columns at each split, then vote.
The bits they each get wrong tend to be different bits, so the vote cancels a lot
of the individual error out.

**Precision and recall are a trade, and you pick the side.** Recall asks: of the
people who really left, how many did we flag? Precision asks: of the people we
flagged, how many really left? Chase recall and you flag half the customer base to
be safe — expensive in discounts, annoying to people who were happy. Chase
precision and you only flag the dead certainties — cheap, and you lose everyone
borderline. F1 is the two of them squeezed into one number (their harmonic mean,
which sags toward whichever is worse), useful for ranking models but useless for
deciding *policy*. The brief tells you the policy here: a missed churner costs
more than a wasted discount, so recall is the one to protect, and the forest's
0.722 beats 0.011 by a distance that no amount of accuracy can argue with.

**What "pick the forest" does not mean.** It does not mean forests beat logistic
regression. It means *this* forest beat *this* logistic regression on *this* split
of *this* generated data, on the metric this business cares about. A logistic
regression with `class_weight="balanced"` would be a far closer fight — see Under
the hood. Every claim in machine learning has that many conditions attached, and
the honest ones say so.

## Download and run

Download
[problem-02-churn-classification-solution.py](./problem-02-churn-classification-solution.py)
and run it:

```bash
python -m pip install scikit-learn pandas
python problem-02-churn-classification-solution.py
```

The customers are generated inside the file from a pinned seed, so nothing
downloads and the numbers are identical everywhere. The `-solution` suffix keeps
this file clear of your own `problem-02-churn-classification.py` — they live in
the same folder and must not collide.

## Common bugs to catch

- **`ConvergenceWarning: lbfgs failed to converge (status=1)`.** The solver ran
  out of steps. Pass `max_iter=1000`. Do not ignore it: the numbers from a model
  that stopped early are not the numbers this page shows.
- **`UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in
  labels with no predicted samples`.** Your model predicted zero churners, so
  "of the ones we flagged, how many were right?" has no denominator. On this data
  it is a real finding, not a crash — pass `zero_division=0` to say "call it 0
  and carry on", and then go and read the recall.
- **Your test balance is not `{0: 1063, 1: 187}`.** You dropped `stratify=y`, or
  changed `test_size`. Both change every number below that line.
- **The confusion matrix looks backwards.** scikit-learn's matrix is rows =
  actual, columns = predicted, labels ascending. So `[[1048, 15], [185, 2]]` reads:
  1048 stayers correctly left alone, 15 stayers wrongly flagged, 185 churners
  missed, 2 churners caught. Bottom-left is always the misses, and on imbalanced
  data bottom-left is where you look first.
- **`ValueError: pos_label=1 is not a valid label`.** Your `churned` column holds
  strings like `"yes"`/`"no"`. Either encode it to 0/1 or pass `pos_label="yes"`.
- **The forest's numbers change every run.** You left `random_state` off it. Both
  the bootstrap resampling and the per-split feature sampling are random.

## Under the hood

<details>
<summary>Under the hood — what make_classification is actually building</summary>

`make_classification` does not sprinkle random numbers and hope. It builds the
data backwards, starting from the answer.

It places the two classes at the corners of a high-dimensional cube, then draws
clusters of points around those corners as Gaussian blobs. Each argument steers a
piece of that:

| Argument | What it does here |
|---|---|
| `n_informative=4` | four columns genuinely carry the class signal |
| `n_redundant=2` | two columns are random linear blends of those four — correlated, no new information |
| `n_features=8` | the remaining two are pure noise |
| `weights=[0.85, 0.15]` | 85% of rows get class 0, 15% class 1 |
| `class_sep=0.9` | how far apart the class blobs sit; higher is an easier problem |
| `flip_y=0.0` | fraction of labels randomly flipped — set to zero here so there is no irreducible noise floor |

`flip_y` defaults to `0.01`, which would randomly mislabel 1% of rows. That is
realistic, but it caps how good any model can be and makes the comparison muddier,
so this problem turns it off. The redundant columns are deliberate: real feature
tables are full of near-duplicate columns, and Problem 3 is about what that does
to a model's sense of which column mattered.

</details>

<details>
<summary>Under the hood — the four metrics, computed from the matrix by hand</summary>

Every metric on this page comes out of the four cells of the confusion matrix.
Name them from the churn class's point of view:

```text
                   predicted stay   predicted churn
actual stay              TN                FP
actual churn             FN                TP
```

- **TP** (true positive) — churner, flagged. A save.
- **FN** (false negative) — churner, missed. The expensive one here.
- **FP** (false positive) — stayer, flagged. A wasted discount.
- **TN** (true negative) — stayer, left alone.

Then:

- accuracy = (TP + TN) / everything — "how often right", blind to which kind of wrong
- precision = TP / (TP + FP) — "when we flagged, were we right?"
- recall = TP / (TP + FN) — "of the real churners, how many did we catch?"
- F1 = 2 · precision · recall / (precision + recall)

Check it against the forest's matrix `[[1055, 8], [52, 135]]`:
precision = 135/(135+8) = 0.944. recall = 135/(135+52) = 0.722.
F1 = 2(0.944)(0.722)/(0.944+0.722) = 0.818. Those are the printed numbers.

Notice what accuracy does with these cells: it adds TP and TN together, and TN is
1055 of them. The big number swamps everything. That is the arithmetic behind
"accuracy is a liar on imbalanced data" — it is not a metaphor, it is a
denominator.

F1 is the *harmonic* mean rather than the plain average on purpose: the harmonic
mean is pulled hard toward the smaller of the two. Precision 1.0 with recall 0.0
averages to 0.5 the ordinary way, which would flatter a useless model; the
harmonic mean gives 0.0.

</details>

<details>
<summary>Under the hood — three ways to rescue the logistic regression</summary>

The straight line is not doomed. It was just asked the wrong question. Three fixes,
in increasing order of how much thought they need:

**1. Reweight the classes.** `LogisticRegression(class_weight="balanced")` tells
the training process that each churner's mistake counts about 5.7× a stayer's
(the ratio of the class sizes). Suddenly saying "stays" to everybody is expensive
and the boundary shifts. Recall jumps; precision falls. Try it — it is the first
Stretch task.

**2. Move the threshold.** The model does not really output a class. It outputs a
probability, and `.predict()` rounds at 0.5. That 0.5 is a *default*, not a law.
Call `.predict_proba(x_test)[:, 1]` and flag everyone above 0.2 instead, and you
trade precision for recall on a dial you control. Sweeping that dial from 0 to 1
and plotting the result is what a precision-recall curve is.

**3. Resample the rows.** Train on a set where churners have been duplicated
(oversampling) or stayers thinned out (undersampling). It works, but it changes
the data rather than the objective, and it can make the model's probabilities
badly calibrated — it now thinks churn is common. Prefer 1 or 2 unless you have a
reason.

The order matters as a habit: change the objective before you change the data.

</details>

<details>
<summary>Under the hood — why 200 trees, and why they disagree usefully</summary>

A random forest is a crowd of decision trees plus two deliberate sources of
disagreement.

First, **bagging**: each tree is trained not on the training set but on a
bootstrap sample of it — draw 3,750 rows *with replacement*, so some rows appear
twice and roughly a third never appear at all. Each tree therefore sees a slightly
different world.

Second, **feature subsampling**: at every single split, a tree may only consider a
random handful of the columns (the default is √8 ≈ 3 of the 8 here). This stops
every tree from seizing on the same one dominant column and becoming clones of one
another.

Then they vote. The maths behind why this helps: if the trees' errors were
perfectly correlated, averaging them would change nothing; because the errors are
*decorrelated* by those two tricks, the individual mistakes partly cancel and the
average is more stable than any single tree. A lone deep decision tree is famously
twitchy — move three rows and its top split can change — and the forest is the
cure for exactly that twitchiness.

`n_estimators=200` is a cost knob, not an accuracy risk. Unlike boosting, more
trees in a forest never overfit; the score just flattens out and the run gets
slower. 200 is comfortably past the flattening point on 3,750 rows.

</details>

## Acceptance checklist

- [ ] `make_churn` is unchanged and prints `{0: 4250, 1: 750}`.
- [ ] The split uses `test_size=0.25`, `random_state=42` and `stratify=y`.
- [ ] Both models print accuracy, churn precision, churn recall and churn F1.
- [ ] Both models print a labelled confusion matrix.
- [ ] The logistic regression's recall is close to zero and you can say why.
- [ ] The recommendation line names `RandomForest` and quotes its recall.
- [ ] Two runs print identical numbers.
- [ ] `report.md` has a section saying what the 84% accuracy hides, in your words.
- [ ] Your file is `problem-02-churn-classification.py` and runs end to end from a
      clean shell with no manual edits. Due before Week 15 begins.

## Stretch

- **Rescue the loser.** Retrain the logistic regression with
  `class_weight="balanced"`. Recall should climb a long way. What happened to
  precision, and would the retention team accept that trade?
- **Turn the dial yourself.** Get `logreg.predict_proba(x_test)[:, 1]`, flag
  everyone above 0.2 instead of 0.5, and recompute the four metrics. You have just
  built one point on a precision-recall curve by hand.
- **Price the mistakes.** Say a missed churner costs $200 in lost subscription and
  a wasted discount costs $15. Compute total cost for both models from their
  confusion matrices. Does the cheaper model match the one recall picked?
- **Cut the noise.** Two of the eight signals carry nothing. Refit the forest on
  only the four most important columns (`forest.feature_importances_` will rank
  them — that is Problem 3). Does anything change?
