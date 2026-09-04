# Problem 3 — Feature Importance: What the Forest Leaned On

> **Topic:** Reading `feature_importances_` honestly, and the difference between "used" and "caused"
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** the first thing anyone asks a trained model is "so which column mattered?", and the number scikit-learn hands back answers a narrower question than the one they asked. This problem sets a trap on purpose: you will delete the model's *most* important feature and watch the accuracy not move at all.

## The Brief

You have four measurements of an iris flower — the length and width of its sepal
(the green leaf-like part underneath) and of its petal — and you want to name the
species. There are three: setosa, versicolor, virginica. A random forest handles
this easily.

Then you ask the model a question it is happy to answer: **which of the four
measurements did you lean on?** scikit-learn gives you `model.feature_importances_`,
four numbers that add up to 1. Big number, important column. Simple.

So test it. Delete the column the model called *least* important and retrain — the
accuracy should barely twitch. Then delete the column it called *most* important
and retrain — the accuracy should fall off a cliff.

It does not. In this run, deleting the least important feature costs you accuracy
and deleting the most important one costs you **nothing**. That is not a bug in
scikit-learn and it is not a bug in your code. It is the honest answer to a
question people ask carelessly, and understanding why is the entire problem.

Here is the analogy to hold on to. Imagine two identical twins who always sit
together in class and always know the same answers. You ask "who told you?" and a
witness names the twin on the left. Now send the left twin home. Did the answers
stop? No — the right twin is still there and knows exactly the same things. The
witness was not lying. "Left twin" was a true report of *who was asked*, and a
useless report of *who was needed*. Two of your four flower measurements are
twins.

## Starter

Copy this into `problem-03-feature-importance.py`. The training helper is given;
you write the ranking and the two drop-one experiments. It runs as pasted and
prints the baseline.

```python
"""problem-03-feature-importance.py — what a forest thinks matters, and what that means."""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def train_and_score(x: pd.DataFrame, y: pd.Series) -> tuple[RandomForestClassifier, float]:
    """Split, fit a forest, and return it with its test accuracy."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model, accuracy_score(y_test, model.predict(x_test))


def main() -> None:
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    model, baseline = train_and_score(x, y)

    # TODO: build `ranking`: (column name, importance) pairs sorted high to low.
    # TODO: print the header line, then each pair, importance to 3 decimal places.
    print(f"baseline accuracy (all 4 features): {baseline:.3f}")

    # TODO: drop the LEAST important column, retrain with train_and_score, print accuracy.
    # TODO: drop the MOST important column, retrain, print accuracy.
    # TODO: print what each drop cost, as baseline minus the new accuracy.


if __name__ == "__main__":
    main()
```

## Requirements

1. Load iris with `load_iris(as_frame=True)` so the columns keep their names.
2. Train a `RandomForestClassifier(n_estimators=200, random_state=42)` on a
   `train_test_split(..., test_size=0.30, random_state=42, stratify=y)` and print
   its test accuracy — that is your baseline.
3. Print `model.feature_importances_` as a **sorted list of (feature, importance)
   pairs**, most important first, to three decimal places.
4. Drop the **least** important feature, retrain with the identical settings, and
   print the new accuracy. Did it change much?
5. Drop the **most** important feature, retrain identically, and print the new
   accuracy. Discuss what happens.
6. Print both costs on one line — baseline minus each new accuracy — so the two
   experiments can be compared at a glance.
7. Hand in your own `problem-03-feature-importance.py` plus a few sentences in
   `report.md` on what "feature importance" actually means here, and what it does
   **not** mean. The word you are circling is *causality*.

## Constraints

- **`random_state=42` on every split and every forest, and `n_estimators=200`
  every time.** All three runs must differ only in which column was removed. If
  the seed moves too, you cannot tell whether the accuracy changed because of the
  missing column or because the split changed, and the experiment says nothing.
- **`stratify=y` on the split.** Iris has exactly 50 of each species and only 45
  test rows. Without stratifying, one species can end up badly under-represented
  in the test set by luck alone.
- **Retrain from scratch after each drop. Do not reuse the fitted model.** A model
  trained on four columns cannot be asked about three; the question is what a
  *new* forest learns when the column was never available.
- **Rank the pairs before you index them.** `ranking[0]` is the most important and
  `ranking[-1]` the least only if you sorted descending. Getting this backwards
  silently swaps the two experiments and produces a story that is exactly wrong.
- **Report the numbers you get, not the numbers you expected.** The surprising
  result is the finding. Do not go looking for a seed that makes it tidy.

## Expected output

Every seed is pinned, so this is what the shipped answer prints on any machine.

```text
$ python problem-03-feature-importance.py
feature importances (most to least):
  petal length (cm)    0.431
  petal width (cm)     0.427
  sepal length (cm)    0.115
  sepal width (cm)     0.027
baseline accuracy (all 4 features): 0.911
drop least important (sepal width (cm)): accuracy 0.889
drop most important  (petal length (cm)): accuracy 0.911
dropping the least cost +0.022; dropping the most cost +0.000
```

Read the ranking first. The two petal measurements take **0.431 and 0.427** — a
gap of four thousandths, which is a tie in all but name. Together they own 86% of
the model's attention. Sepal width gets 0.027, which is close to nothing.

Now the experiments, and they do the opposite of what the ranking suggests:

- Drop **sepal width**, the least important, and accuracy falls from 0.911 to
  0.889. Cost: **+0.022**.
- Drop **petal length**, the *most* important, and accuracy stays at **0.911**.
  Cost: **+0.000**. The model does not miss it at all.

The reason is the twins. Petal length and petal width are nearly the same
information wearing two hats — long petals are wide petals on an iris. When both
are present the forest splits its attention roughly evenly between them, so each
scores about 0.43. Take one away and the other simply does the whole job. The
0.431 never meant "this column is worth 43% of the accuracy". It meant "in a world
where its twin was also on the table, this is the one the trees happened to reach
for 43% of the time".

**Two honesty notes about these numbers, and both matter more than the numbers.**

The test set is **45 flowers**. 0.911 is 41 of 45 correct and 0.889 is 40 of 45.
The entire difference between those two runs is **one flower**. On a test set that
small, a 2.2-point move is well inside the range that a different seed would
produce by itself, so the correct summary is "dropping sepal width did not clearly
help or hurt", not "sepal width is secretly vital". A score is an estimate. The
smaller the test set, the wider the estimate wobbles, and 45 rows wobble a lot.

And nothing here says a petal *causes* a species. The forest found that petal
measurements are a reliable way to *tell the species apart*. Evolution ran the
other way round: being a virginica is why the petal is long. Importance is a
report about a model and its columns, never a claim about the world.

## Steps

1. Paste the starter and run it. You should see `baseline accuracy (all 4
   features): 0.911`.
2. Zip `x.columns` with `model.feature_importances_`, sort descending on the
   importance, and print the four lines. Check they sum to 1.
3. Take `ranking[-1][0]` — the least important name — `x.drop(columns=[...])`,
   retrain, print.
4. Take `ranking[0][0]` — the most important — drop, retrain, print.
5. Print both costs on one line and read them side by side.
6. Before writing anything up, print `x.corr()` and look at the petal row. The
   explanation is sitting in that table.
7. Write the `report.md` sentences. Answer both halves: what the number *is*, and
   what it is **not**.

## The Solution

```python
"""problem-03-feature-importance.py — what a forest thinks matters, and what that means.

Trains a RandomForest on iris, ranks the features by importance, then retrains
without the least important and without the most important to watch the accuracy
move. The point is to read feature_importances_ honestly: it says which columns
this model leaned on, not which columns *cause* the outcome. Every seed is pinned.

Run it with::

    python problem-03-feature-importance-solution.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


def train_and_score(x: pd.DataFrame, y: pd.Series) -> tuple[RandomForestClassifier, float]:
    """Split, fit a forest, and return it with its test accuracy."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model, accuracy_score(y_test, model.predict(x_test))


def main() -> None:
    """Rank features, then drop the least and most important and compare."""
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    model, baseline = train_and_score(x, y)
    ranking = sorted(
        zip(x.columns, model.feature_importances_), key=lambda pair: pair[1], reverse=True
    )
    print("feature importances (most to least):")
    for feature, importance in ranking:
        print(f"  {feature:<20} {importance:.3f}")
    print(f"baseline accuracy (all 4 features): {baseline:.3f}")

    least_important = ranking[-1][0]
    _, without_least = train_and_score(x.drop(columns=[least_important]), y)
    print(f"drop least important ({least_important}): accuracy {without_least:.3f}")

    most_important = ranking[0][0]
    _, without_most = train_and_score(x.drop(columns=[most_important]), y)
    print(f"drop most important  ({most_important}): accuracy {without_most:.3f}")

    print(
        f"dropping the least cost {baseline - without_least:+.3f}; "
        f"dropping the most cost {baseline - without_most:+.3f}"
    )


if __name__ == "__main__":
    main()
```

**What the number actually measures.** Every time a tree in the forest makes a
split, it picks the column and the threshold that best separate the species — that
best reduce the *impurity*, the mixed-up-ness of the labels in that branch. The
tree records how much cleaner the split made things, weighted by how many rows
passed through it. Add that up across every split in every one of the 200 trees,
divide so the total is 1, and you have `feature_importances_`. So the honest
translation is: **"how much cleaning did this column do, in this forest, on this
training set, with these columns available."** Every clause in that sentence is
load-bearing.

**Which is why deleting the top feature was free.** Petal length and petal width
carry nearly the same signal. The credit for that shared signal gets split between
them roughly at random, tree by tree. Remove one and the other absorbs the whole
share — the forest was never relying on *that column*, it was relying on *petal
size*, which it can still see. Correlated features always do this, and it is the
number-one reason importance rankings mislead people. If two columns tie in the
middle of a ranking, suspect twins before you suspect a real dead heat.

**And why deleting the bottom feature was not free.** Sepal width scored 0.027 and
still cost a flower when it went. Low importance does not mean zero contribution —
it means the column did little of the *bulk* separating. Iris's hard cases are the
versicolor/virginica pairs that overlap on petal size, and a sliver of sepal
information can be exactly what tips one of those borderline flowers the right
way. Small aggregate credit, occasionally decisive. (One flower is also well
inside the noise on 45 test rows — hold both thoughts at once.)

**The rule to leave with.** A feature importance answers "what did this model
use?". It does not answer "what matters in the world?", it does not answer "what
would happen if I removed this?", and it never answers "what causes what". If the
question you actually have is the second one, the experiment in this problem — drop
it and refit — is the answer, and it is the reason the problem is built as an
experiment rather than a printout.

## Run it

Copy the worked answer on this page into `problem-03-feature-importance.py` and run it:

```bash
python -m pip install scikit-learn pandas
python problem-03-feature-importance.py
```

Iris ships inside scikit-learn, so nothing downloads and there is no network
dependency. The `-solution` suffix keeps this file clear of your own
`problem-03-feature-importance.py`.

## Common bugs to catch

- **`AttributeError: 'numpy.ndarray' object has no attribute 'columns'`.** You
  called `load_iris()` without `as_frame=True`, so you have a bare array with no
  column names. Add the argument.
- **Your ranking is upside down.** `sorted()` is ascending by default. You need
  `reverse=True`, and you must sort on the importance — `key=lambda pair: pair[1]` —
  not on the name, or you get an alphabetical list that looks plausible and is
  meaningless.
- **`KeyError: 0`.** You passed the whole `(name, importance)` tuple to
  `drop(columns=...)` instead of just the name. Take `ranking[-1][0]`.
- **The importances change every run.** No `random_state` on the forest. The
  ranking is stable here but the third decimal place is not, and on data with more
  twins the whole order can shuffle.
- **All three accuracies are 1.000.** You scored on the training rows. A forest of
  200 trees memorises 105 flowers perfectly. Score `x_test`.
- **`ValueError: Found input variables with inconsistent numbers of samples`.**
  You dropped a column from `x` but kept an older `y`, or dropped a *row* by
  mistake. `drop(columns=[...])` never touches rows.

## Under the hood

<details>
<summary>Under the hood — Gini impurity, and the arithmetic of a split</summary>

"Impurity" is a measure of how mixed the labels are in a group. The default in
scikit-learn is **Gini impurity**: for a group where the classes appear in
proportions p₁, p₂, p₃, it is

```text
gini = 1 − (p₁² + p₂² + p₃²)
```

A group of 30 flowers that are all setosa gives 1 − 1² = **0**: perfectly pure.
A group that is 10/10/10 gives 1 − (⅓² + ⅓² + ⅓²) = **0.667**, the worst it can be
with three classes. Intuitively, it is the chance you would be wrong if you
guessed a random flower's label by drawing another random label from the same
group.

A split takes one impure group and makes two. Its *gain* is the parent's impurity
minus the size-weighted average of the children's:

```text
gain = gini(parent) − (n_left/n · gini(left) + n_right/n · gini(right))
```

The tree tries every column and every threshold it is allowed to consider and
keeps the split with the biggest gain. Then `feature_importances_` is, for each
column, the sum of `n_at_that_node × gain` over every node that split on it,
across all 200 trees, normalised to sum to 1. The `n ×` weighting is why a split
near the root counts for far more than one deep in a branch: it decided the fate
of more flowers.

This is often called **mean decrease in impurity**, or MDI. When you see that name
in a paper, it is this number.

</details>

<details>
<summary>Under the hood — MDI's two known biases, and how to see them</summary>

MDI is fast — it falls out of training for free — and it has two well-documented
biases you should be able to name.

**1. It favours columns with many distinct values.** A continuous column like
"petal length in cm" offers a tree hundreds of possible thresholds to try. A yes/no
column offers exactly one. More chances to find a good-looking split means more
chances to find one that is good by luck, so continuous and high-cardinality
columns collect importance they have not earned. The classic demonstration: bolt a
column of pure random numbers onto iris, refit, and watch the noise column score
above sepal width.

**2. It is computed on the training set.** MDI measures how much a column helped
carve up the rows the trees were fitted on — including the rows they memorised.
A column can score well for helping the forest overfit.

The fix for both is **permutation importance**, which asks a different and often
better question: take the fitted model, take the *test* set, shuffle one column so
it keeps its distribution but loses its link to the answer, and measure how much
the score drops.

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, x_test, y_test, n_repeats=20, random_state=42)
for name, drop in sorted(zip(x.columns, result.importances_mean), key=lambda p: -p[1]):
    print(f"{name:<20} {drop:+.3f}")
```

That is measured on held-out data and in the units of the score itself, so it is
directly comparable to "how much accuracy would I lose". Note that it does *not*
escape the twin problem: shuffle petal length while petal width is still there and
the model shrugs, so both twins look unimportant. Correlated features are hard for
every importance method; that is a property of the data, not a flaw in the tool.

</details>

<details>
<summary>Under the hood — why "important" and "causal" are different questions</summary>

Three different questions get flattened into the word "important", and mixing them
up is how models end up justifying bad decisions.

1. **Which columns did this model use?** — MDI. Free, and it is a fact about the
   model.
2. **Which columns does this model need?** — permutation importance, or the
   drop-and-refit experiment in this problem. A fact about the model *and* the
   data.
3. **Which columns change the outcome if I intervene?** — causality. Not answerable
   from this table, at any sample size, by any algorithm.

The gap between 2 and 3 is where the damage happens. A model predicting hospital
readmission may lean heavily on "number of previous admissions" — an excellent
predictor. Nobody thinks admitting a patient again causes them to need admitting
again; it is a marker for how sick they are. But phrase the finding as "previous
admissions are the most important driver of readmission" and someone will propose
a policy about admissions.

The famous worked example is a 1990s pneumonia study where a model learned that
asthma patients had *lower* risk of dying. True in the data, and lethal as a rule:
asthmatics with pneumonia were rushed straight to intensive care, and the care is
what lowered the risk. A model that saw only the columns concluded asthma was
protective. Answering question 3 needs an experiment, or a causal model with
assumptions written down and defended — never a sorted list of importances.

</details>

<details>
<summary>Under the hood — why iris is easy, and what that hides</summary>

Iris is 150 flowers, four columns, three species, measured by Edgar Anderson and
published in 1936. Setosa is *linearly separable* from the other two — you can
draw a single straight line on a petal-length axis that gets every setosa right.
Versicolor and virginica overlap slightly, and essentially every mistake any model
makes on iris is one of those two being confused for the other. Your four misses
are almost certainly all in that pair; print `confusion_matrix(y_test, preds)` and
check.

That easiness is why iris is a good teaching set and a bad benchmark. Any
reasonable model lands in the 90s, so the dataset cannot tell good models from
great ones, and 45 test rows means a whole percentage point is worth less than
half a flower. Never conclude "model A beats model B" from a dataset this size —
including in this problem, where the honest reading of a one-flower difference is
"too close to call".

</details>

## Acceptance checklist

- [ ] The four importances print sorted, most important first, and sum to 1.
- [ ] Baseline, drop-least and drop-most all use `random_state=42`,
      `test_size=0.30`, `stratify=y` and `n_estimators=200`.
- [ ] Each drop retrains a fresh forest rather than reusing the fitted one.
- [ ] Both costs print on one line.
- [ ] You can say out loud why dropping the top feature cost nothing.
- [ ] You noted that 45 test rows makes a 0.022 gap one single flower.
- [ ] Two runs print identical numbers.
- [ ] `report.md` says what importance means **and** what it does not — including
      the word causality.
- [ ] Your file is `problem-03-feature-importance.py` and runs end to end from a
      clean shell with no manual edits. Due before Week 15 begins.

## Stretch

- **Plant a fake.** Add a column of random numbers with
  `x["noise"] = np.random.default_rng(0).normal(size=len(x))`, refit, and print the
  ranking. Where does pure noise place? Anything it outranks should worry you.
- **Look at the twins directly.** Print `x.corr().round(2)`. Find the correlation
  between petal length and petal width, and predict from that number alone which
  drop would be free.
- **Drop both twins.** Remove petal length *and* petal width and retrain. Now the
  model has only sepals. This is the experiment that shows what petal size was
  really worth.
- **Try the other method.** Run `permutation_importance` on the test set (see Under
  the hood) and put the two rankings side by side. Where they disagree, work out
  which question each one answered.
- **Ask a different model.** Fit a `LogisticRegression` and look at `.coef_`.
  Those are not importances — they are per-class weights, they can be negative,
  and they depend on the scale of each column. Explain to yourself why you cannot
  compare them to the forest's numbers without standardising first.
