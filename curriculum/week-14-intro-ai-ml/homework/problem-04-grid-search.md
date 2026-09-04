# Problem 4 — Hyperparameter Tuning With GridSearchCV

> **Topic:** Searching settings with cross-validation, inside a pipeline, without quietly cheating
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour
> **Why this one:** every model has knobs, and guessing at them by hand while watching the test score is the most respectable-looking way to cheat in machine learning. This is where you learn the honest version: search on the training data, using folds, and keep one set of data that the search never sees.

## The Brief

You are sorting handwritten digits. Each sample is an 8×8 grey-scale image of a
single digit, flattened into 64 numbers — one brightness value per pixel. There
are 1,797 of them. Your job is to name the digit: 0 through 9.

The model is **k-nearest neighbours**, and it is the simplest idea in this entire
week. It does not really "learn" anything. To classify a new image it measures the
distance to every image it was shown during training, finds the `k` closest ones,
and takes a vote. That is it. It is the machine-learning version of "what do the
kids sitting nearest me think the answer is?".

Which raises an obvious question: **how many neighbours should you ask?** Ask 1 and
you copy whichever single image happens to be nearest, noise and all. Ask 21 and
you drag in neighbours from three streets over. There is no formula for the right
`k`. And there are two more knobs beside it: should closer neighbours get a louder
vote, and how should "distance" even be measured?

The wrong way to choose is to try a value, check the test score, try another, check
again. Do that twenty-eight times and the test set is no longer a test — you have
picked the setting that flatters those particular rows, and your reported score is
about as trustworthy as a student who marked their own exam.

The right way is a **grid search with cross-validation**. Lock the test set in a
drawer. Take the training data and cut it into 5 equal folds. For every
combination of settings, train on 4 folds and score on the 5th, five times over,
rotating which fold is held out, and average. Every combination gets judged on
data it was not trained on, and the real test set is still sealed. Only when the
search has crowned a winner do you open the drawer — **once** — and see whether the
cross-validation estimate held up.

You will also wrap the model in a `Pipeline` with a `StandardScaler`, because k-NN
measures distances and distances care about scale. And a scaler outside a
cross-validation loop is a data leak, which Under the hood explains in detail.

## Starter

Copy this into `problem-04-grid-search.py`. The pipeline skeleton is given; you
fill in the grid and the reporting. It runs as pasted and prints the split sizes.

```python
"""problem-04-grid-search.py — tune a k-NN with GridSearchCV, then check the estimate."""

from __future__ import annotations

from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def build_search() -> GridSearchCV:
    """A scaler + k-NN pipeline wrapped in a 5-fold grid search."""
    pipe = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("knn", KNeighborsClassifier()),
        ]
    )
    # TODO: a param_grid over knn__n_neighbors, knn__weights and knn__metric.
    # TODO: return GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=1).
    raise NotImplementedError("build the grid search")


def main() -> None:
    digits = load_digits()
    x, y = digits.data, digits.target
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    print(f"images: {len(x)}   train: {len(x_train)}   test: {len(x_test)}")

    # TODO: build the search and fit it on the TRAINING data only.
    # TODO: print how many combinations were tried.
    # TODO: print the best parameters, sorted by name, one per line.
    # TODO: print the best 5-fold CV accuracy.
    # TODO: score the best estimator on the held-out test set and print the gap.


if __name__ == "__main__":
    main()
```

## Requirements

1. Split first: `train_test_split(..., test_size=0.25, random_state=42,
   stratify=y)`. Print the image count and both split sizes.
2. Wrap `KNeighborsClassifier` inside a `Pipeline` with a `StandardScaler` in
   front of it. The step names must be `"scale"` and `"knn"`, because the grid
   keys depend on them.
3. Grid-search this exact grid with **5-fold** cross-validation and
   `scoring="accuracy"`:

   ```python
   param_grid = {
       "knn__n_neighbors": [1, 3, 5, 7, 9, 15, 21],
       "knn__weights": ["uniform", "distance"],
       "knn__metric": ["euclidean", "manhattan"],
   }
   ```

4. Fit the search on the **training data only**.
5. Print how many combinations were tried, then the best parameters (sorted by
   name, one per line), then the best CV accuracy to three decimals.
6. Evaluate the best estimator on the held-out test set. Print that accuracy and
   the **gap** between it and the CV estimate, signed. Did it match?
7. Hand in your own `problem-04-grid-search.py` plus a paragraph in `report.md`
   describing what changed and what did not — and say which of the three knobs
   actually mattered.

## Constraints

- **`random_state=42` on the split, and this exact grid.** Every number on this
  page comes from those settings. The grid search itself has no randomness — 5-fold
  cross-validation without shuffling is deterministic — so with the split pinned,
  the winner and both scores are fixed. Change the seed and the winning `k` can
  change too.
- **`stratify=y` on the split.** Ten classes and 450 test images; without it, a
  digit can end up short-changed by luck.
- **The scaler goes *inside* the pipeline, never before the split.** If you scale
  the whole dataset up front, the mean and standard deviation are computed using
  the test rows, and information from the test set has leaked into training. Your
  score goes up and it is not real. Inside a pipeline, each fold refits the scaler
  on its own 4 folds — which is correct, and it is the entire reason `Pipeline`
  exists.
- **Fit the search on `x_train` only.** The moment `x_test` enters the search, the
  final number stops being an independent check.
- **`n_jobs=1`.** Parallel workers make the run non-deterministic in its output
  ordering and can crash inside some sandboxes. 28 combinations × 5 folds finishes
  in a few seconds single-threaded.
- **Report the gap even when it is negative.** A held-out score slightly *below* the
  CV estimate is the expected outcome, not a failure. Hiding it would hide the
  lesson.

## Expected output

```text
$ python problem-04-grid-search.py
images: 1797   train: 1347   test: 450
combinations tried: 28  (x 5 folds)
best parameters:
  knn__metric = euclidean
  knn__n_neighbors = 5
  knn__weights = distance
best 5-fold CV accuracy: 0.978
held-out test accuracy : 0.964
test - CV gap: -0.013
```

Count the work first: 7 neighbour values × 2 weightings × 2 metrics = **28**
combinations, each trained and scored 5 times, so 140 model fits, plus one final
refit of the winner on the whole training set. That final refit is automatic —
`GridSearchCV` does it for you, which is why `search.score(...)` works straight
away.

The winner is `k=5`, distance-weighted, euclidean. Middle of the road, which is
usually where the answer lives: 1 neighbour is too jumpy, 21 is too blurry.

Now the two scores, because the gap between them is the real content of this
problem. Cross-validation said **0.978**. The sealed test set said **0.964**. The
gap is **−0.013**: the estimate was about one and a third points optimistic.

That is not a bug, and it was predictable. You chose the winner *because* it had
the highest cross-validation score, and with 28 contestants, some of the winner's
lead is genuine skill and some is luck on those particular folds. Pick the maximum
of 28 noisy numbers and you will, on average, pick a number that is a bit too high.
It has a name — the **winner's curse** — and it is why the CV score of the best
model is not an honest estimate of how it will do on new data, and why you kept
450 images in a drawer.

**Hold both scores loosely.** 0.964 is 434 of 450 images. Move the split and it
moves; on 450 rows, one image is 0.2 points. And neither number says *which* 16
digits it got wrong. If most of them are 1s mistaken for 7s, this model has a
specific weakness that a single accuracy figure will never mention, no matter how
high it is.

## Steps

1. Paste the starter and run it — it should print
   `images: 1797   train: 1347   test: 450` and then raise the
   `NotImplementedError`, which is the stub telling you where to start.
2. Write the `param_grid`. Every key is `step_name__parameter_name`, so it is
   `knn__n_neighbors`, with **two** underscores.
3. Return the `GridSearchCV` and fit it on `x_train, y_train`.
4. Print `len(search.cv_results_["params"])` and check it is 28. If it is not,
   your grid has a typo.
5. Print `search.best_params_` sorted, and `search.best_score_`.
6. Call `search.score(x_test, y_test)` — that scores the refitted winner — and
   print the signed gap.
7. Before writing the report, print the top few rows of `search.cv_results_` (see
   Stretch) and find out how much of the grid was wasted effort. Then answer: what
   changed, what did not, and which knob actually mattered?

## The Solution

```python
"""problem-04-grid-search.py — tune a k-NN with GridSearchCV, then check the estimate.

Grid-searches a StandardScaler -> KNeighborsClassifier pipeline over neighbours,
weighting and distance metric on the bundled digits dataset, with 5-fold
cross-validation. Then it scores the best estimator on a held-out test set the
search never touched, to see whether the CV estimate held up. Every seed is
pinned; the search itself is deterministic.

Run it with::

    python problem-04-grid-search-solution.py
"""

from __future__ import annotations

from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def build_search() -> GridSearchCV:
    """A scaler + k-NN pipeline wrapped in a 5-fold grid search."""
    pipe = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("knn", KNeighborsClassifier()),
        ]
    )
    param_grid = {
        "knn__n_neighbors": [1, 3, 5, 7, 9, 15, 21],
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan"],
    }
    return GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=1)


def main() -> None:
    """Split, grid-search on the training half, then test the winner."""
    digits = load_digits()
    x, y = digits.data, digits.target
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    print(f"images: {len(x)}   train: {len(x_train)}   test: {len(x_test)}")

    search = build_search()
    search.fit(x_train, y_train)

    print(f"combinations tried: {len(search.cv_results_['params'])}  (x 5 folds)")
    print("best parameters:")
    for name, value in sorted(search.best_params_.items()):
        print(f"  {name} = {value}")
    print(f"best 5-fold CV accuracy: {search.best_score_:.3f}")

    test_accuracy = search.score(x_test, y_test)
    print(f"held-out test accuracy : {test_accuracy:.3f}")
    print(f"test - CV gap: {test_accuracy - search.best_score_:+.3f}")


if __name__ == "__main__":
    main()
```

**Why k-NN needs the scaler.** k-NN's whole decision is "who is nearest", so
whichever column has the biggest numbers shouts loudest in the distance sum. Here
every column is a pixel on the same 0–16 brightness scale, so the scaler earns
less than it would elsewhere — but some pixels (the corners) are almost always
blank, and standardising stops a near-constant pixel and a busy central one from
being weighted as if they were equally informative. Put the scaler in the pipeline
anyway, every time, as a reflex. The one occasion you leave it out to save a
second will be the occasion your features are "age in years" and "income in
dollars", and income will win every comparison by a factor of a thousand.

**What the pipeline really buys you.** A `Pipeline` is not tidying. It is a
promise: whatever happens to the training rows happens to the test rows *and*
happens **separately in every fold**. When the grid search trains on folds 1–4, the
scaler learns its mean and standard deviation from folds 1–4 only, then applies
them to fold 5. Scale the whole array once before the search and every fold's
scaler has already peeked at its own validation rows. The leak is small, it is
invisible, it inflates your score, and it never reproduces in production. This is
the single most common silent error in beginner machine-learning code.

**Why five folds and not one split.** A single validation split judges each
setting on one arbitrary slice of data. With 1,347 training images a slice is
small, and small slices are noisy, so you would sometimes crown a setting that
merely got a friendly slice. Five folds average five judgements and every training
row gets used for validation exactly once. It costs five times the compute, and on
a search this size that is a few seconds.

**And why the sealed test set is still necessary.** Cross-validation removed the
cheating from *choosing*. It did not remove the winner's curse from *reporting*.
The number you publish must come from data that took no part in any decision —
none of the 140 fits, none of the comparisons. That is what the 450 images were
for, and it is why they were split off in the very first lines, before anything
else happened.

## Run it

Copy the worked answer on this page into `problem-04-grid-search.py` and run it:
it:

```bash
python -m pip install scikit-learn
python problem-04-grid-search.py
```

The digits dataset ships inside scikit-learn, so nothing downloads. The run takes
a handful of seconds — 140 fits of a model that barely trains. The `-solution`
suffix keeps this file clear of your own `problem-04-grid-search.py`.

## Common bugs to catch

- **`ValueError: Invalid parameter 'n_neighbors' for estimator Pipeline(...)`.**
  Inside a pipeline the keys need the step prefix: `knn__n_neighbors`, not
  `n_neighbors`. Two underscores.
- **`ValueError: Invalid parameter 'knn' for estimator Pipeline(...)`.** Your step
  is named something else. The name in `steps=[("knn", ...)]` and the prefix in the
  grid must match exactly.
- **`AttributeError: 'GridSearchCV' object has no attribute 'best_params_'`.** You
  read it before calling `.fit()`. Everything with a trailing underscore only
  exists after fitting.
- **`combinations tried` is not 28.** A typo in a list, or a stray key. 7 × 2 × 2
  is the arithmetic to check against.
- **Your test score is *higher* than the CV score by a lot.** Suspicious. Check you
  did not scale before splitting, and that the search never saw `x_test`.
- **Your test score is 1.000.** You scored on the training data, or on the data the
  search already used.
- **The run takes minutes, or the process dies.** You left `n_jobs=-1` on and the
  worker pool is struggling. Set `n_jobs=1`.
- **`UserWarning: Could not find the number of physical cores`.** Harmless joblib
  chatter on some Windows machines; it goes to stderr and does not affect the
  result.

## Under the hood

<details>
<summary>Under the hood — what 5-fold cross-validation actually does, fold by fold</summary>

Deal the 1,347 training images into 5 piles of about 269. Then run five rounds:

```text
round 1:  train on piles 2 3 4 5   score on pile 1
round 2:  train on piles 1 3 4 5   score on pile 2
round 3:  train on piles 1 2 4 5   score on pile 3
round 4:  train on piles 1 2 3 5   score on pile 4
round 5:  train on piles 1 2 3 4   score on pile 5
```

Average the five scores and that is one combination's CV score. Every image is
scored exactly once, by a model that never saw it, and every image is trained on
four times. That is the trick: you get the reliability of a large validation set
without permanently giving up any rows to it.

For a classifier, scikit-learn quietly upgrades `cv=5` to **StratifiedKFold**, so
each pile keeps roughly the same 10% of each digit. And unless you ask for
shuffling it does not shuffle, which is why this whole search is deterministic —
the piles are the same on every run and on every machine.

`cv=5` is the usual default. More folds means each model trains on more data (so
less pessimistic bias) but costs more and makes the folds smaller and noisier. The
extreme, `cv=n`, is leave-one-out: maximally data-efficient, expensive, and its
average is famously high-variance.

</details>

<details>
<summary>Under the hood — how k-NN classifies, and why it has no training time</summary>

k-NN is the outlier of this course: **it does not build a model.** `.fit()` stores
the training array and, for the default `algorithm="auto"`, builds a spatial index
to make lookups faster. That is all. There are no learned weights, no trees, no
coefficients. It is sometimes called a *lazy learner* for exactly this reason, and
all its cost is at prediction time, not training time — the opposite of everything
else you have fitted this week.

To predict, it computes the distance from the new image to stored images, takes
the `k` smallest, and votes. Your grid tuned three things about that sentence:

- **`n_neighbors`** — how many votes. Small `k` follows every wiggle in the
  training data including the noise (high variance); large `k` smooths across the
  boundary between classes and starts ignoring genuine local detail (high bias).
  The best `k` is the middle of that trade, and there is no way to know it but to
  try. Here it is 5.
- **`weights`** — `"uniform"` gives all `k` neighbours an equal vote;
  `"distance"` weights each vote by 1/distance, so a neighbour twice as far away
  counts half as much. It won here, and it usually helps when `k` is larger than
  the tightest clusters.
- **`metric`** — `"euclidean"` is straight-line distance, √Σ(a−b)²; `"manhattan"`
  is Σ|a−b|, the distance a taxi drives on a grid of streets. Manhattan is often
  steadier in high dimensions because it does not square differences and so is less
  dominated by one badly mismatched pixel. On 64 tidy pixels, euclidean took it.

The reason 64 dimensions is still fine for k-NN, when "the curse of dimensionality"
says distances become meaningless in high dimensions, is that digit images do not
fill those 64 dimensions. They lie on a much lower-dimensional surface inside it —
most pixel patterns are not any digit at all. The *effective* dimension is far
below 64.

</details>

<details>
<summary>Under the hood — the winner's curse, and how to measure honestly</summary>

Every measured score is the truth plus some noise:

```text
observed CV score  =  true skill of this setting  +  luck of these folds
```

Take the maximum over 28 such numbers and you are selecting on the sum, so you
preferentially pick settings that had *both* good skill and good luck. The
expected luck of the winner is positive. Therefore `best_score_` is biased upward
as an estimate of the winner's true skill — even though every individual fold was
scored honestly on unseen data.

The bias grows with the size of the grid. Search 28 combinations and it is small
(here, about a point). Search 5,000 in a random search on a small dataset and it
can be large enough to make your headline number fiction.

Three ways people handle it:

1. **Hold out a final test set.** What this problem does. Simple, and one number
   at the end is genuinely independent — as long as you look **once**. Looking,
   adjusting and looking again turns it into a validation set and the whole
   argument collapses.
2. **Nested cross-validation.** An outer CV loop for estimating, an inner loop for
   tuning, so the tuning happens fresh inside each outer fold. Statistically the
   cleanest answer and it costs folds × folds fits.
3. **Report the whole distribution.** `search.cv_results_["std_test_score"]` gives
   the spread across folds for each setting. If the top five settings sit inside
   one standard deviation of each other, there is no real winner, and the correct
   report says "these five are indistinguishable" rather than crowning one.

There is a habit hiding in point 3 that is worth more than the technique: when
differences are inside the noise, say so. A model tuned to a hundredth of a point
on 450 images has been tuned to nothing.

</details>

<details>
<summary>Under the hood — when a grid is the wrong shape of search</summary>

`GridSearchCV` tries every combination. That is exhaustive and reassuring, and it
scales terribly: adding a fourth knob with 5 values takes 28 fits to 140, times 5
folds is 700. Grids grow by multiplying.

The usual alternative is `RandomizedSearchCV`, which samples a fixed number of
random combinations from ranges you give it. It sounds worse and often is not.
Most hyperparameters barely matter; a grid spends the same effort on every axis,
so it evaluates the one knob that matters at only 7 distinct values while
faithfully exploring two knobs that change nothing. A random search of the same
budget tries a different value of *every* knob on *every* draw, so it samples the
important axis far more finely. Bergstra and Bengio made this argument in 2012 and
it is why random search is the default advice for anything past three knobs.

Beyond that sit sequential methods — `HalvingGridSearchCV`, which starts every
candidate on a small slice of data and repeatedly kills the worst half, and
Bayesian optimisation, which fits a model of the score surface and picks where to
look next.

Use a grid when the space is small and you want the guarantee. Everything on this
page — split first, pipeline the preprocessing, cross-validate the choice, keep a
sealed test set — applies identically to all of them. The search strategy is the
part that changes; the honesty is not.

</details>

## Acceptance checklist

- [ ] The split happens **before** anything else and uses `test_size=0.25`,
      `random_state=42`, `stratify=y`.
- [ ] `StandardScaler` sits inside the `Pipeline`, not before the split.
- [ ] The grid is the one in the requirements and `combinations tried` prints 28.
- [ ] The search is fitted on `x_train` only.
- [ ] Best parameters print sorted, one per line, and the best CV accuracy prints
      to three decimals.
- [ ] The held-out test accuracy and the signed gap both print.
- [ ] You can explain why the gap is negative without calling it a bug.
- [ ] Two runs print identical numbers.
- [ ] `report.md` says what changed, what did not, and which knob mattered.
- [ ] Your file is `problem-04-grid-search.py` and runs end to end from a clean
      shell with no manual edits. Due before Week 15 begins.

## Stretch

- **Read the whole scoreboard.** Load `pd.DataFrame(search.cv_results_)`, sort by
  `rank_test_score`, and print `params`, `mean_test_score` and `std_test_score` for
  the top 10. How many settings are within one standard deviation of the winner?
- **Isolate the knobs.** Group the results by `param_knn__metric` and by
  `param_knn__weights` and average. Which of the three knobs moved the score most,
  and which was 70 fits of nothing?
- **Where does it fail?** Print `confusion_matrix(y_test, search.predict(x_test))`.
  Find the two digits it confuses most. Would you ship this on a form where those
  two digits are a postcode?
- **Try a random search.** Swap in `RandomizedSearchCV` with `n_iter=10` over
  `n_neighbors` ranging 1–30. Does a third of the compute find a comparable
  setting?
- **Take the leak for a walk.** Deliberately scale the whole `x` before splitting,
  rerun, and note the score. Seeing how small and how convincing the inflation is
  will teach you more than any warning on this page.
