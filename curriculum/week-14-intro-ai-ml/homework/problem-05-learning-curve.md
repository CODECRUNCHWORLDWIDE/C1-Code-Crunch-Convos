# Problem 5 — Learning Curve: More Data, or a Bigger Brain?

> **Topic:** Learning curves, and telling "get more data" apart from "get a better model"
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** every other problem this week asks *how good is this model?* This one asks the question that decides what you do next: is the model held back by the amount of data, or by the model itself? Those two problems look identical from a single accuracy score and need completely opposite fixes.

## The Brief

Picture a student practising for a spelling test. You give her ten words to
study, then a hundred, then a thousand. Each time you check two things: how well
she spells the words she practised, and how well she spells brand-new words she
has never seen. Write both down at every step and the pattern tells you what she
needs — more practice words, or a different way of studying.

That is a **learning curve**: a table (or a plot) of two scores against the size
of the training set. The first score is on the rows the model trained on. The
second is on rows it was not shown, the *validation* score. You retrain the model
from scratch at each size and record both.

Three shapes, three different pieces of advice:

- **The two lines are far apart and the validation line is still climbing.** The
  model can clearly learn more than it has; it just has not seen enough examples.
  Go and get more data.
- **The two lines have met, and they met somewhere low.** More rows change
  nothing — the model has already learned everything it is capable of learning
  from this kind of data. That is **underfitting**, and the fix is a more
  flexible model or better features, not a bigger download.
- **The validation line flattens out below a near-perfect training line.** More
  rows of the same kind buy you very little. Whatever is left is either noise, or
  something this model cannot express.

Your data is `load_digits`: 1,797 tiny 8×8 greyscale pictures of handwritten
digits, 64 pixels each, shipped inside scikit-learn so there is nothing to
download. Your model is `LogisticRegression`. Your job is to train it at six
growing training sizes and read the shape.

**One thing this page deliberately does not do: open a window.** The classic
hand-in for this problem is a picture, `learning_curve.png`. The shipped answer
prints a table of the same numbers instead, for two reasons. A table is text, so
it can be checked; a picture cannot. And `plt.show()` waits for a human to close
a window, so on a grading machine, a server, or any computer with no screen, a
script that calls it simply hangs forever. When you *do* draw the picture — and
you should, it is Requirement 5 — you save it to a file and never show it. The
Stretch has the code.

## Starter

Copy this into `problem-05-learning-curve.py`. The imports, the seed and the six
sizes are given; you fill in the model, the call, and the table.

```python
"""problem-05-learning-curve.py — does this model want more data, or a bigger brain?"""

from __future__ import annotations

from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve

RANDOM_STATE = 42
# 5-fold CV trains on 4/5 of the 1,797 images = 1,437, so the sizes stay under that.
TRAIN_SIZES = [50, 100, 250, 500, 900, 1400]


def main() -> None:
    digits = load_digits()
    x, y = digits.data, digits.target

    # TODO: build LogisticRegression(max_iter=5000, random_state=RANDOM_STATE).
    # TODO: call learning_curve(model, x, y, train_sizes=TRAIN_SIZES, cv=5,
    #       scoring="accuracy", shuffle=True, random_state=RANDOM_STATE).
    # TODO: average train_scores and val_scores across the 5 folds with .mean(axis=1).
    # TODO: print one row per size: train_size, train_acc, val_acc, and the gap.
    # TODO: print whether the validation line is still rising or has flattened.


if __name__ == "__main__":
    main()
```

## Requirements

1. Load `load_digits()` and build a
   `LogisticRegression(max_iter=5000, random_state=42)`.
2. Call `learning_curve` at training sizes `[50, 100, 250, 500, 900, 1400]`, with
   `cv=5`, `scoring="accuracy"`, `shuffle=True` and `random_state=42`. Those
   exact settings are what produce the numbers under Expected output.
3. Average the five folds at each size and print one row per size: the training
   size, the training accuracy, the validation accuracy, and the gap between
   them, all to three decimals.
4. Print how validation accuracy moved from the smallest size to the largest,
   then a one-line verdict: **still rising** if the last step gained more than
   0.005, otherwise **flattening**.
5. In your own file, also save the picture as `learning_curve.png` — two lines,
   train and validation, against training size — drawn with matplotlib's `Agg`
   backend and `plt.savefig`, never `plt.show()`. The shipped answer stops at the
   table because the course checks printed text and a PNG has none; the plotting
   code is in Stretch.
6. Write one paragraph of interpretation in your `report.md`: is this model
   bottlenecked by data or by capacity, and which numbers made you say so?

## Constraints

- **Pin `random_state=42` on the model *and* on `learning_curve`.** Both of them
  shuffle: the solver has a random component, and `shuffle=True` mixes the rows
  before the folds are cut. Without a seed on both, your table is slightly
  different every run and nobody can check your work.
- **Keep the largest training size at or below 1,437.** With `cv=5`, one fifth of
  the 1,797 images is held out every time, so at most 1,437 rows are ever
  available to train on. Ask for 1,500 and scikit-learn raises a `ValueError`
  before it fits anything. That is why the sizes here end at 1,400.
- **`max_iter=5000`, not the default 100.** These are 64 raw pixel values on very
  different scales, and the solver needs a lot of steps to settle. At the default
  it stops early and warns, and then your curve is measuring an unfinished fit
  rather than the model you meant to test.
- **`shuffle=True`.** Rows that sit next to each other in this file often come
  from the same handwriting sample, so a contiguous slice of 50 rows is less
  varied than 50 random ones. Left off, the small sizes score noticeably lower —
  and for a reason that has nothing to do with the model.
- **Never call `plt.show()` in a script you hand in.** It blocks, waiting for a
  window that a headless machine will never draw. Save the figure to a file
  instead; the file is also easier to attach to a report.
- **Read the validation column, not the training one.** Training accuracy here is
  a flat 1.000 at every size. A number that never moves cannot tell you anything
  about whether more data would help.

## Expected output

Every seed is pinned, so this run is the same on every machine. A different
scikit-learn build could move a last digit; the shape of the two columns is the
fixed part.

```text
$ python problem-05-learning-curve-solution.py
learning curve (mean accuracy across 5 folds):
  train_size  train_acc  val_acc     gap
          50      1.000    0.818   0.182
         100      1.000    0.873   0.127
         250      1.000    0.910   0.090
         500      1.000    0.910   0.090
         900      1.000    0.919   0.081
        1400      1.000    0.915   0.085
validation accuracy went from 0.818 at 50 rows to 0.915 at 1400 rows
the validation line is flattening — the curve has mostly levelled off
```

Read it column by column. **Training accuracy is 1.000 everywhere** — with 64
features and only 50 rows, the model can fit those 50 rows perfectly, and it
still can at 1,400. **Validation accuracy climbs steeply and then stops**: 0.818
at 50 rows, 0.910 by 250, and 0.915 at 1,400. Going from 50 rows to 250 bought
almost ten points. Going from 900 to 1,400 — five hundred more images — bought
nothing; it even ticks down from 0.919 to 0.915, which is noise between folds,
not damage. **The gap narrows and then parks** around 0.08.

So the verdict line is right: this curve has flattened. Collecting another
thousand handwritten digits would be a poor use of a week. If you want to get
past roughly 0.92, you need a different model — one that can express something a
straight-line-per-pixel rule cannot.

## Steps

1. Paste the starter and run it. Nothing prints yet; that is fine.
2. Build the model and call `learning_curve` with the settings from Requirement
   2. Print the raw `sizes`, `train_scores`, `val_scores` once and look at them:
   the two score arrays are 6 rows (one per size) by 5 columns (one per fold).
3. Average each row with `.mean(axis=1)`, then print the table.
4. Add the summary line — first validation score, last validation score — and the
   rising-or-flattening verdict.
5. Draw the PNG in your own file with the code from Stretch, and open it. The
   picture and the table say the same thing; seeing both is the point.
6. Write the paragraph. Name the shape you see, and say what you would do next.

## The Solution

```python
"""problem-05-learning-curve.py — does this model want more data, or a bigger brain?

A learning curve plots training and validation accuracy as the training set grows.
The real deliverable is a PNG; this course runs headless and compares text, so the
curve is printed as a table instead. Reading it: if the two lines meet low, more
data will not help (the model is too simple — underfitting); if they meet high with
a gap, more data closes the gap. Every seed is pinned.

Run it with::

    python problem-05-learning-curve-solution.py
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve

RANDOM_STATE = 42
# 5-fold CV trains on 4/5 of the 1,797 images = 1,437, so the sizes stay under that.
TRAIN_SIZES = [50, 100, 250, 500, 900, 1400]


def main() -> None:
    """Compute train and validation accuracy at growing training sizes."""
    digits = load_digits()
    x, y = digits.data, digits.target

    model = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    sizes, train_scores, val_scores = learning_curve(
        model,
        x,
        y,
        train_sizes=TRAIN_SIZES,
        cv=5,
        scoring="accuracy",
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    print("learning curve (mean accuracy across 5 folds):")
    print(f"  {'train_size':>10}  {'train_acc':>9}  {'val_acc':>7}  {'gap':>6}")
    train_mean = train_scores.mean(axis=1)
    val_mean = val_scores.mean(axis=1)
    for size, train_acc, val_acc in zip(sizes, train_mean, val_mean):
        print(f"  {size:>10}  {train_acc:>9.3f}  {val_acc:>7.3f}  {train_acc - val_acc:>6.3f}")

    print(f"validation accuracy went from {val_mean[0]:.3f} at {sizes[0]} rows "
          f"to {val_mean[-1]:.3f} at {sizes[-1]} rows")
    verdict = (
        "still rising — more data would likely help"
        if val_mean[-1] - val_mean[-2] > 0.005
        else "flattening — the curve has mostly levelled off"
    )
    print(f"the validation line is {verdict}")


if __name__ == "__main__":
    main()
```

**What `learning_curve` is doing for you.** You handed it one model, six sizes
and `cv=5`, and it quietly trained thirty models. For each of the five folds it
sets that fold aside as the validation set, then trains on the first 50 rows of
what is left, then the first 100, and so on up to 1,400 — scoring both the rows
it trained on and the held-out fold every time. `train_scores` and `val_scores`
come back as 6×5 grids, one row per size and one column per fold, which is why
the very next thing the code does is `.mean(axis=1)` to collapse each row of five
numbers into one average.

**Why the table instead of the plot.** The answer prints numbers because numbers
can be compared automatically and a picture cannot, and because nothing here may
open a window — a `plt.show()` on a machine with no screen waits forever. Nothing
is lost: a learning curve is a shape, and the shape is just as visible in the
`val_acc` column, which rises fast and then stops.

**Why the verdict is computed, not typed.** The last line compares the final two
validation scores and only claims "still rising" if the gain clears 0.005. That
threshold is a judgement call written down in code, which is better than a
judgement call made by eye — and it means the sentence stays true if you change
the sizes or the model. Small wobbles between neighbouring sizes are normal; five
folds of a few hundred rows are not enough to make the third decimal meaningful.

**The reading of this particular curve.** A near-perfect training score with a
validation score stuck around 0.92 is the classic mild-overfitting shape: the
model has more than enough capacity to memorise what it sees, and the last eight
points of gap are the part it memorised that does not generalise. More rows shrink
that gap slowly at best — the curve already shows it barely moving from 900 to
1,400. This is a "change the model" situation, not a "get more data" one.

## Download and run

Download
[problem-05-learning-curve-solution.py](./problem-05-learning-curve-solution.py)
and run it:

```bash
python problem-05-learning-curve-solution.py
```

If scikit-learn is not installed yet:

```bash
python -m pip install scikit-learn
```

The digits are inside scikit-learn, so there is nothing to download and the table
is identical on every machine. It takes a few seconds — remember it is fitting
thirty models. Add `matplotlib` only if you are doing the plotting stretch:
`python -m pip install matplotlib`. The `-solution` suffix keeps this file clear
of your own `problem-05-learning-curve.py`.

## Common bugs to catch

- **`ValueError: train_sizes has been interpreted as absolute numbers of training
  samples and must be within (0, 1437], but is within [50, 1500].`** You asked to
  train on more rows than a 5-fold split leaves available. Lower the top size, or
  lower `cv`.
- **`ConvergenceWarning: lbfgs failed to converge (status=1): STOP: TOTAL NO. OF
  ITERATIONS REACHED LIMIT.`** The solver ran out of steps. Raise `max_iter` to
  5000. Do not ignore it — the scores printed under that warning came from a model
  that never finished training.
- **The script prints nothing and never exits.** You called `plt.show()`. Replace
  it with `plt.savefig("learning_curve.png")`, and select the `Agg` backend before
  importing `pyplot`.
- **The table prints arrays like `[1. 1. 1. 1. 1.]` instead of one number.** You
  forgot `.mean(axis=1)`. Those five numbers are the five folds at one size.
- **Every run gives different numbers.** `shuffle=True` without
  `random_state=42`. The shuffle is genuinely random until you pin it.
- **Your sizes come back as something like 143 when you asked for 0.1.** Any
  `train_sizes` value below 1.0 is read as a *fraction* of the data, not a row
  count. Pass whole numbers when you mean rows.
- **Validation accuracy looks far too high (near 1.000).** You scored the training
  rows twice. The second array `learning_curve` returns is the validation one;
  unpack it in the right order.

## Under the hood

<details>
<summary>Under the hood — the thirty models behind six rows</summary>

`learning_curve` is a loop around a loop. The outer loop is the cross-validation
split: with `cv=5` the data is cut into five folds, and each fold takes a turn as
the validation set while the other four (1,437 rows) are the training pool. The
inner loop walks your `train_sizes`, and for each one it takes a **prefix of that
pool** — the first 50 rows, the first 100, the first 250 — and fits a fresh copy
of the model on it.

Two consequences worth knowing. First, the subsets are **nested**: the 100-row
training set contains the 50-row one. That is on purpose, so consecutive points
on the curve differ only by the rows that were added, not by a whole new random
draw, which would add wobble that has nothing to do with size. Second, the cost is
`len(train_sizes) × cv` fits — thirty here. Learning curves are one of the more
expensive diagnostics in scikit-learn, which is why you run one to make a decision,
not on every commit. `n_jobs=-1` will spread those fits across your cores.

The estimator you pass in is never modified. Each fit happens on a clone, so the
`model` object you built is still unfitted when the call returns.

</details>

<details>
<summary>Under the hood — why the training score is a flat 1.000</summary>

Each image is 64 pixels, so each one is a point in 64-dimensional space, and
logistic regression draws flat dividing surfaces through that space. There is a
geometric fact hiding here: as long as you have fewer points than dimensions plus
one — and 50 points in 64 dimensions qualifies — you can almost always find a
surface that separates them perfectly, whatever the labels are. The model is not
being clever at 50 rows; it has enough freedom to place a boundary that puts
every training point on the correct side.

That is exactly why the training column is useless on its own and why the gap
between the columns is the interesting quantity. A perfect training score with a
0.18 validation gap at 50 rows says "it has memorised these fifty". The same
perfect training score with a 0.085 gap at 1,400 says something much better: with
1,400 examples, most of what it fits is real structure that transfers, and only a
little is memorised.

Regularisation is what keeps this from being worse. `LogisticRegression` applies
an L2 penalty by default (`C=1.0`), which pushes the coefficients toward zero and
makes the model prefer the *simplest* separating surface rather than a wildly
contorted one. Set `C=1e6` to effectively switch it off and the validation column
slips by a point or two at almost every size while the training column stays
pinned at 1.000 — a small, clean demo of what regularisation is buying you.

</details>

<details>
<summary>Under the hood — learning curves versus validation curves</summary>

Two diagnostics that look alike and answer different questions.

A **learning curve** varies the *amount of data* with the model fixed. It answers
"would more rows help?".

A **validation curve** (`sklearn.model_selection.validation_curve`) varies *one
hyperparameter* with the data fixed — `max_depth` for a tree, `C` for logistic
regression, `n_neighbors` for k-NN. It answers "is this knob set too low or too
high?", and it has the same two-line shape: the training score climbs as the model
gets more flexible while the validation score climbs, peaks, and then falls as
the model starts fitting noise.

Use the learning curve to decide where to spend money — data collection is
expensive — and the validation curve to decide where to set a knob. Problem 4's
`GridSearchCV` is the automated cousin of the validation curve: same idea, many
knobs at once, and it reports only the winner instead of the whole shape.

</details>

## Acceptance checklist

- [ ] `learning_curve` runs with `cv=5`, `scoring="accuracy"`, `shuffle=True` and
      `random_state=42`.
- [ ] The training sizes are `[50, 100, 250, 500, 900, 1400]` and none exceeds
      1,437.
- [ ] The model is `LogisticRegression(max_iter=5000, random_state=42)` and no
      convergence warning appears.
- [ ] The table prints six rows with train accuracy, validation accuracy and the
      gap, to three decimals.
- [ ] A summary line reports the first and last validation scores, followed by a
      rising-or-flattening verdict.
- [ ] `learning_curve.png` is saved by your own file, and nothing calls
      `plt.show()`.
- [ ] Two runs print identical numbers.
- [ ] You wrote the paragraph, and it names data or capacity as the bottleneck.

## Stretch

- **Draw the picture.** This is Requirement 5, and it is eight lines:

  ```python
  import matplotlib
  matplotlib.use("Agg")          # draw to a file, never to a window
  import matplotlib.pyplot as plt

  plt.plot(sizes, train_mean, marker="o", label="train")
  plt.plot(sizes, val_mean, marker="o", label="validation")
  plt.xlabel("training rows")
  plt.ylabel("accuracy")
  plt.legend()
  plt.savefig("learning_curve.png", dpi=120)
  ```

  `matplotlib.use("Agg")` must come *before* `import matplotlib.pyplot`. Agg is
  the backend that renders straight into an image file and needs no screen.
- **Show the spread.** You averaged five folds away. Plot
  `val_mean ± val_scores.std(axis=1)` as a shaded band with
  `plt.fill_between`, and see how much of the wobble at the right-hand end is
  just fold-to-fold variation.
- **Move the ceiling.** Swap in `RandomForestClassifier(random_state=42)` or
  `SVC(random_state=42)` and rerun. If a different model lands well above 0.92 at
  the same 1,400 rows, you have proved the bottleneck was capacity, not data.
- **See the other shape.** Rerun the curve with
  `DecisionTreeClassifier(max_depth=2, random_state=42)`. A tree allowed only two
  questions cannot tell ten digits apart, and both columns collapse into the low
  0.3s and stay there as the data grows. Two low lines that never separate is the
  underfitting shape, and no amount of extra data will move it.
- **Change the question.** Set `scoring="f1_macro"` instead of accuracy. On a
  balanced set like digits the two barely differ; keep that in mind for Problem 6,
  where the choice of metric changes the answer completely.
