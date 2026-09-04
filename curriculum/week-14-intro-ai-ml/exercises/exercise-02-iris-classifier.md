# Exercise 2 — Iris Classifier

> **Topic:** Logistic regression on a three-class problem, and turning class numbers back into names
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md)
> **Difficulty:** Easy
> **Target time:** 20 minutes
> **Why this one:** classification is where the target stops being a quantity and becomes a decision, and beginners lose whole afternoons to the fact that scikit-learn predicts `0`, `1`, `2` while the world wants `setosa`, `versicolor`, `virginica`. You also meet `stratify` and `max_iter` here — two arguments that look like noise until the day they are the reason your model is broken.

## The Brief

Iris is a botany dataset from 1936: 150 flowers, fifty each of three species,
with four measurements per flower — sepal length, sepal width, petal length,
petal width, all in centimetres. It ships inside scikit-learn, so there is
nothing to download.

You are going to train a classifier that takes four measurements and names the
species, then hand it two flowers that are not in the dataset at all —
measurements you type by hand — and see whether it names them the way a
botanist would. Iris is easy on purpose. When a model does well on iris, that
tells you your *code* is right, not that you are good at machine learning.

One idea to hold onto before you start: the model thinks in numbers. Inside, a
species is `0`, `1`, or `2`, never a word. The species names are a lookup table
you keep on the side and reach for only when a human is about to read the
output. Mix the two up early and every line after it has to carry the mess.

## Starter

Copy this into `exercise-02-iris-classifier.py` and fill in the `TODO`s.

```python
"""exercise-02-iris-classifier.py — three-class logistic regression on iris.

Trains on scikit-learn's bundled iris measurements and names two new flowers.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.30
MAX_ITER = 1000

NEW_FLOWERS = [
    [5.0, 3.4, 1.5, 0.2],   # small petals
    [6.7, 3.0, 5.6, 2.2],   # long, wide petals
]


def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Return (X, y, class_names) from the bundled iris dataset."""
    iris = load_iris(as_frame=True)
    # TODO: return iris.data, iris.target, and the species names as a list.
    raise NotImplementedError


def train_classifier(x_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Fit a LogisticRegression and return it."""
    # TODO: pass max_iter=MAX_ITER and random_state=RANDOM_STATE.
    raise NotImplementedError


def main() -> None:
    """Train, score, and name two hand-written flowers."""
    x, y, class_names = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    model = train_classifier(x_train, y_train)
    predictions = model.predict(x_test)

    print("features:", list(x.columns))
    print("classes :", class_names)
    print(f"train rows: {len(x_train)}   test rows: {len(x_test)}")
    print(f"accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"mistakes: {(predictions != y_test).sum()} of {len(y_test)}")

    # TODO: build a DataFrame from NEW_FLOWERS with the same columns as x,
    # predict, and print each flower's measurements next to its species name.


if __name__ == "__main__":
    main()
```

## Requirements

1. `load_data` returns the feature frame, the target Series, and the three
   species names as a plain list of strings.
2. The split uses `test_size=0.30`, `random_state=RANDOM_STATE`, and
   `stratify=y`, producing 105 training rows and 45 test rows.
3. `LogisticRegression` is constructed with `max_iter=1000` and
   `random_state=RANDOM_STATE`.
4. Accuracy is printed to three decimal places, followed by the raw count of
   mistakes out of 45. Two views of the same fact; the count is the one that
   makes it real.
5. Both hand-written flowers are predicted through a DataFrame whose columns
   match `x.columns` exactly, and printed as species **names**, not integers.
   Expected: the first is `setosa`, the second is `virginica`.

## Constraints

- **Pass `stratify=y`.** Without it the split is drawn at random, and a bad
  draw can leave the test set lopsided — twelve setosa in one, twenty-two in
  another. Your score then partly measures the draw. With three balanced
  classes the damage is small; the habit is what you are building, because on
  the imbalanced data in Exercise 5 an unstratified split can hand you a test
  set with almost no positives in it.
- **Pass `random_state` to both the split and the model.** An unpinned seed
  means the run you show someone is not the run they get, and neither of you can
  prove which one is right.
- **`max_iter=1000`, not the default 100.** At the default the solver hits its
  cap on this data and prints a `ConvergenceWarning` — it stopped because it ran
  out of budget, not because it finished. A warning is not a crash, so it is
  easy to scroll past, and a model that stopped optimising early is a model
  whose score means less than you think.
- **Convert class numbers to names for display only.** Keep `y` as integers
  everywhere the model touches it. Mapping to strings at the print statement is
  presentation; mapping earlier means every metric call needs the strings too,
  and eventually one of them will not get them.
- **Do not scale the features here.** All four are centimetres in a similar
  range. Exercise 4 is where scaling earns its keep, and doing it now would
  hide the contrast.

## Expected output

The features list, the class names, the row counts, and the two species answers
are fixed. The accuracy and the mistake count depend on the split and the
scikit-learn build, so read them as approximate — but with every seed pinned
they come out identical on every run of this file.

```text
$ python exercise-02-iris-classifier.py
features: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
classes : ['setosa', 'versicolor', 'virginica']
train rows: 105   test rows: 45
accuracy: 0.933
mistakes: 3 of 45
[5.0, 3.4, 1.5, 0.2] -> setosa
[6.7, 3.0, 5.6, 2.2] -> virginica
```

**A note on that accuracy, because it matters.** With everything this page
mandates — `test_size=0.30`, `random_state=42`, `stratify=y`, `max_iter=1000` —
this build produces **0.933, three mistakes out of forty-five**, and it does so
on every run. If you have read an older version of this page promising "about
0.98" and one mistake, that number does not reproduce with these settings on
scikit-learn 1.6.1; 0.933 does. Three mistakes is correct here, and you should
not go hunting for a bug. All three are versicolor and virginica confused for
one another — exactly the pair
[Lecture 3](../lecture-notes/03-pipelines-evaluation-and-ethics.md#the-confusion-matrix)
warns you about. Setosa is never confused with anything, on any run. The two
hand-written flowers, `setosa` and `virginica`, are not close calls: if either
comes back as something else, your columns are in the wrong order.

## Steps

1. Create the file and paste the starter.
2. Fill in `load_data`. Print `x.head()` and `y.value_counts()` before going
   further — fifty of each class, four float columns.
3. Fill in `train_classifier`. Run. You should get the accuracy line.
4. Add the new-flower block. Build the frame with
   `pd.DataFrame(NEW_FLOWERS, columns=x.columns)` so the names travel with the
   values.
5. Print `model.predict_proba(new_frame).round(3)` and compare the confidence
   on each row.
6. Now drop both petal columns from `x` and rerun. Accuracy should fall
   noticeably. Petals, not sepals, separate these species — the model just
   told you something about flowers.

## The Solution

```python
"""exercise-02-iris-classifier.py — three-class logistic regression on iris.

Trains on scikit-learn's bundled iris measurements and names two new flowers.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.30
MAX_ITER = 1000

NEW_FLOWERS = [
    [5.0, 3.4, 1.5, 0.2],   # small petals
    [6.7, 3.0, 5.6, 2.2],   # long, wide petals
]


def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Return (X, y, class_names) from the bundled iris dataset."""
    iris = load_iris(as_frame=True)
    return iris.data, iris.target, iris.target_names.tolist()


def train_classifier(x_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Fit a LogisticRegression and return it."""
    model = LogisticRegression(max_iter=MAX_ITER, random_state=RANDOM_STATE)
    model.fit(x_train, y_train)
    return model


def main() -> None:
    """Train, score, and name two hand-written flowers."""
    x, y, class_names = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    model = train_classifier(x_train, y_train)
    predictions = model.predict(x_test)

    print("features:", list(x.columns))
    print("classes :", class_names)
    print(f"train rows: {len(x_train)}   test rows: {len(x_test)}")
    print(f"accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"mistakes: {(predictions != y_test).sum()} of {len(y_test)}")

    new_frame = pd.DataFrame(NEW_FLOWERS, columns=x.columns)
    for measurements, code in zip(NEW_FLOWERS, model.predict(new_frame)):
        print(f"{measurements} -> {class_names[code]}")


if __name__ == "__main__":
    main()
```

**`.tolist()`, not `list()`.** This is the one line where the obvious version is
wrong. `iris.target_names` is a NumPy array. Wrapping it in `list()` gives you a
Python list of *NumPy string scalars*, and under numpy 2.x those print as
`[np.str_('setosa'), np.str_('versicolor'), np.str_('virginica')]`. The values
still compare equal to `"setosa"` and everything downstream works, but the
printed line looks broken. `.tolist()` converts all the way down to built-in
`str`, and the output reads `['setosa', 'versicolor', 'virginica']`.

**Integers everywhere the model touches them; names only at the print.** `y`
stays as the codes 0, 1 and 2 for the split, the fit, the accuracy, and the
mistake count. The one conversion happens inside the `zip` at the bottom, where
`class_names[code]` indexes the list. Map to strings early instead and
`stratify` is stratifying on strings, `accuracy_score` is comparing strings, and
every later metric needs the string version too — one of them eventually will
not get it. Keep the machine-readable form as the single source of truth and
render at the very edge.

**`stratify=y` makes the score worse here, and that is the point.** Stratifying
forces the split to keep the class proportions, so the test set holds exactly
fifteen of each species. On this seed, that makes the reported accuracy *lower*
— unstratified at `random_state=42` this model scores 1.000, stratified it
scores 0.933. The stratified number is the trustworthy one, because the
unstratified split simply handed the model an easier forty-five flowers. That is
a small, concrete preview of Exercise 3.

**`max_iter=1000`.** At the default 100 the solver runs out of budget and warns.
Raising the cap lets it finish — and on this data it finishes with the same
accuracy it had when it gave up early. Worth sitting with: the warning was real,
and fixing it changed nothing about the score. A warning tells you the process
was wrong; it does not promise the answer was.

## Run it

Copy the worked answer on this page into `exercise-02-iris-classifier.py` and run it:

```bash
python exercise-02-iris-classifier.py
```

The iris data ships inside scikit-learn, so there is nothing to download and no
setup. Every seed is pinned, so two runs print byte-identical output. The
`-solution` suffix keeps it clear of your own `exercise-02-iris-classifier.py`.

## Common bugs to catch

- **`classes : [np.str_('setosa'), np.str_('versicolor'), np.str_('virginica')]`.**
  No error, no warning, just a line that looks like a bug. You used
  `list(iris.target_names)` instead of `.tolist()`. Under numpy 1.x this printed
  cleanly, which is why so much older code does it. Use `.tolist()`, or
  `[str(name) for name in iris.target_names]` to be explicit.
- **`ConvergenceWarning: lbfgs failed to converge (status=1): STOP: TOTAL NO. OF
  ITERATIONS REACHED LIMIT.`** You left `max_iter` at its default. Raise it to
  1000. scikit-learn 1.6.1 prints that line in full capitals with a trailing
  period — older pages render it lowercase. `model.n_iter_` reads `[100]`,
  meaning it used every iteration it had.
- **Predictions print as `[0 2]` instead of species.** `model.predict` returns
  the integer codes it was trained on. `class_names[code]` turns one code into a
  name; `iris.target_names[predictions]` does a whole array at once.
- **`ValueError: Expected 2D array, got 1D array instead.`** You handed over one
  flower as a flat list — `model.predict([5.0, 3.4, 1.5, 0.2])`. One sample
  still needs the outer brackets, because the contract is
  `(n_samples, n_features)` and you supplied a shape of `(4,)`. Note the wording
  differs from Exercise 1's: a plain list becomes a NumPy array rather than a
  pandas Series, and the array path still uses the older message.
- **`UserWarning: X does not have valid feature names, but LogisticRegression
  was fitted with feature names`.** You predicted with a bare list of lists.
  Wrap it: `pd.DataFrame(NEW_FLOWERS, columns=x.columns)`. Silently trusting
  column order is how a model ends up reading sepal width as petal length.
- **`AttributeError: 'numpy.ndarray' object has no attribute 'columns'`.** You
  called `load_iris()` without `as_frame=True`, so you got NumPy arrays with no
  column names.

## Under the hood

<details>
<summary>Under the hood — how one logistic regression handles three species at once</summary>

Logistic regression, taken literally, answers a yes/no question: it draws one
boundary and asks "which side is this point on?". Iris has three species, which
is not a yes/no question. So how does one `LogisticRegression` name three
things?

scikit-learn's answer for this solver is **multinomial** logistic regression:
instead of one boundary it learns a score for each of the three classes at once,
and turns the three scores into three probabilities that add up to 1 using a
function called *softmax*. `predict_proba` shows you those three numbers;
`predict` just reports whichever class scored highest and throws the other two
away. That is why an ambiguous flower — say `[6.0, 2.7, 4.8, 1.6]`, which sits
on the versicolor/virginica border — comes back a confident `versicolor` from
`predict` while `predict_proba` quietly reveals a near-tie behind it.

Older code sometimes built three separate yes/no models instead — "setosa vs
the rest", "versicolor vs the rest", "virginica vs the rest" — and picked the
most confident. That is called one-vs-rest, and scikit-learn can still do it,
but the multinomial version fits all three boundaries together so their
probabilities are calibrated against each other. For a beginner the takeaway is
smaller than the machinery: `predict` is hiding a vector of probabilities, and
the moment a decision has a cost (Exercise 5) that hidden vector is the thing you
actually want.

</details>

## Acceptance checklist

- [ ] The script runs clean — no traceback, no `ConvergenceWarning`, no
      feature-name warning.
- [ ] 105 training rows and 45 test rows print.
- [ ] Accuracy prints as `0.933` and the mistake count agrees: three of
      forty-five (42/45 = 0.933).
- [ ] Both hand-written flowers print as species names, and they are `setosa`
      and `virginica`.
- [ ] Two consecutive runs print byte-identical output.
- [ ] Committed with a message like `Add Week 14 exercise 2: iris logistic regression`.

## Stretch

- **Three algorithms, one problem.** Swap `LogisticRegression` for
  `KNeighborsClassifier(n_neighbors=5)` and then
  `DecisionTreeClassifier(max_depth=3, random_state=42)`. On this stratified
  seed-42 split you get roughly `logreg 0.933`, `knn5 0.978`, `tree 0.978` —
  two mistakes separate the best from the worst on forty-five flowers. The
  sentence worth writing down: **which algorithm you pick matters far less than
  beginners expect, and far less than which features you have and how you split.**
- **Probabilities on an ambiguous flower.** `[6.0, 2.7, 4.8, 1.6]` sits on the
  versicolor/virginica border and `predict_proba` returns roughly
  `[[0.002, 0.599, 0.398]]`. `predict` reports `versicolor` and says nothing
  about the 0.398 right behind it. Those three numbers are the model's real
  state of belief, and `predict` discards two of them.
- **Dropping the petal columns.** Train on the two sepal columns alone and
  accuracy falls from 0.933 to about 0.733 — roughly twelve mistakes instead of
  three. Petals separate these species; sepals barely do. You learned that from
  a `.score()` call, not a botany book, and that is a first taste of feature
  importance.

Next: [Exercise 3 — Why `random_state` Matters](./exercise-03-train-test-split.md),
which explains why your score moved when you changed one number.
