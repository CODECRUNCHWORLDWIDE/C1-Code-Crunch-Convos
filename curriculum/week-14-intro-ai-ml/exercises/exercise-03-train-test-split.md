# Exercise 3 — Why `random_state` Matters

> **Topic:** One split is one sample; a pinned seed is what makes a result reproducible
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md)
> **Difficulty:** Medium
> **Target time:** 25 minutes
> **Why this one:** in Exercise 1 you changed `random_state` and the score moved. That was not a bug and it was not noise you can ignore — it is the single most common reason two people running the same model report different numbers. Until you have measured the spread yourself, you will keep believing that a score is a property of a model. It is a property of a model *and a split*.

## The Brief

Take one dataset, one model, and one set of settings. Change nothing except
which rows end up in the test set. Then watch the accuracy move by several
percentage points.

That movement has a name in the wild: **seed shopping**. Someone runs the split
a few times, keeps the seed that produced the best number, reports it, and
quietly does not mention the other runs. It is not usually malicious — it is
usually someone who has never printed the whole distribution and does not know
how wide it is. Think of it like measuring your height once a day and only
telling people the morning you stood tallest. You are going to print the whole
distribution, then prove two things that sound obvious until you see them side
by side: with a pinned seed the split is identical every run, and without one it
is not.

## Starter

Copy this into `exercise-03-train-test-split.py` and fill in the `TODO`s.

```python
"""exercise-03-train-test-split.py — how much does the split move the score?

Holds the model fixed and varies only the train/test split.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

MODEL_SEED = 42
TEST_SIZE = 0.30
SPLIT_SEEDS = range(10)


def score_one_split(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> float:
    """Split with the given seed, fit, and return test accuracy.

    Passing None for split_seed leaves the split unseeded on purpose.
    """
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=split_seed, stratify=y
    )
    model = LogisticRegression(max_iter=1000, random_state=MODEL_SEED)
    model.fit(x_train, y_train)
    return float(model.score(x_test, y_test))


def test_row_labels(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> list[int]:
    """Return the original row numbers that landed in the test set."""
    # TODO: split with this seed and return sorted(x_test.index).
    raise NotImplementedError


def main() -> None:
    """Print the spread across seeds, then prove reproducibility both ways."""
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    scores: list[float] = []
    print("--- one model, ten different splits ---")
    for seed in SPLIT_SEEDS:
        # TODO: score this seed, append to scores, print "seed  N -> 0.xxx".
        raise NotImplementedError

    print(f"lowest : {min(scores):.3f}")
    print(f"highest: {max(scores):.3f}")
    print(f"spread : {max(scores) - min(scores):.3f}")
    print(f"mean   : {sum(scores) / len(scores):.3f}")

    print("--- reproducibility ---")
    pinned_a = test_row_labels(x, y, 42)
    pinned_b = test_row_labels(x, y, 42)
    print(f"seed=42 twice, same test rows?  {pinned_a == pinned_b}")

    # TODO: call test_row_labels twice with None and print the same comparison.


if __name__ == "__main__":
    main()
```

## Requirements

1. The loop prints one line per seed, formatted `seed  N -> 0.xxx`, with the
   accuracy to three decimal places.
2. After the loop, print the lowest, highest, spread, and mean across the ten
   seeds. Spread is `max - min`.
3. `test_row_labels` returns the sorted original index values of the test
   rows, so two runs can be compared with `==`.
4. The seed-42 comparison prints `True`.
5. The unseeded comparison prints `False`.
6. Nothing about the model changes between runs. Same class, same
   `max_iter`, same `random_state=MODEL_SEED`. Only the split moves.

## Constraints

- **Vary exactly one thing.** If you also let the model's seed float, you can
  no longer say which knob moved the score. This is the same discipline as
  changing one line between test runs; machine learning just makes it easier to
  forget, because there are so many knobs and they are all so easy to turn.
- **`random_state=None` is the honest way to write "unseeded".** Do not delete
  the argument — pass `None` explicitly, so the reader can see the choice was
  deliberate. Deleting it makes unseeded code look like a typo, and a reviewer
  cannot tell "meant it" from "forgot".
- **Compare index labels, not accuracies, for the reproducibility check.** Two
  different splits can land on the same accuracy by coincidence — on iris,
  where scores cluster, that happens constantly. Identical row membership is the
  thing that actually proves the split repeated; the score is downstream of it.
- **Do not pick the best seed and move on.** The point of this exercise is
  that the best seed is not information. It is the top of a range, and the
  range is what you should report.

## Expected output

The ten accuracies and the summary statistics are approximate — a different
scikit-learn build shifts them, and on iris a single flower changing hands moves
a score by about 0.022. With every seed in the loop pinned they are identical on
every run of this file. The two `True`/`False` lines are **not** approximate:
they are the whole finding, and if either flips, the exercise has failed.

```text
$ python exercise-03-train-test-split-solution.py
--- one model, ten different splits ---
seed  0 -> 1.000
seed  1 -> 0.978
seed  2 -> 1.000
seed  3 -> 0.933
seed  4 -> 0.978
seed  5 -> 0.933
seed  6 -> 0.933
seed  7 -> 0.933
seed  8 -> 0.933
seed  9 -> 0.956
lowest : 0.933
highest: 1.000
spread : 0.067
mean   : 0.958
--- reproducibility ---
seed=42 twice, same test rows?  True
unseeded twice, same test rows? False
```

Look at the spread. On a clean, balanced, famously easy dataset — with
stratification on, which *reduces* the variation — changing nothing but the
split moves accuracy by about seven points, which is three flowers out of
forty-five. Now picture someone reporting the 1.000 as "our model's accuracy"
and never mentioning the other nine runs. Nobody has to lie for that to
mislead. The honest form of this result is one sentence with three numbers in
it: **about 0.96 on average, ranging 0.93 to 1.00 across ten stratified
splits.**

## Steps

1. Create the file and paste the starter.
2. Fill in `test_row_labels`. Test it alone first: call it twice with seed 42
   and confirm the lists are equal.
3. Fill in the seed loop. Run. You now have ten numbers.
4. Add the unseeded comparison. Run it three or four times — `False` every
   time. With 45 of 150 rows going to test, the chance of the same 45 coming
   up twice is far too small to worry about.
5. Change `TEST_SIZE` to `0.10` and rerun. The spread does not always widen over
   only ten seeds — read the stretch section for why, and what fifty seeds
   reveal that ten hide.
6. Write the mean and the spread as one sentence — "about 0.96, ranging 0.93
   to 1.00 across ten splits". That is how a result should be reported for the
   rest of your career.

## The Solution

```python
"""exercise-03-train-test-split.py — how much does the split move the score?

Holds the model fixed and varies only the train/test split.
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

MODEL_SEED = 42
TEST_SIZE = 0.30
SPLIT_SEEDS = range(10)


def score_one_split(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> float:
    """Split with the given seed, fit, and return test accuracy.

    Passing None for split_seed leaves the split unseeded on purpose.
    """
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=split_seed, stratify=y
    )
    model = LogisticRegression(max_iter=1000, random_state=MODEL_SEED)
    model.fit(x_train, y_train)
    return float(model.score(x_test, y_test))


def test_row_labels(x: pd.DataFrame, y: pd.Series, split_seed: int | None) -> list[int]:
    """Return the original row numbers that landed in the test set."""
    _, x_test, _, _ = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=split_seed, stratify=y
    )
    return sorted(x_test.index)


def main() -> None:
    """Print the spread across seeds, then prove reproducibility both ways."""
    iris = load_iris(as_frame=True)
    x, y = iris.data, iris.target

    scores: list[float] = []
    print("--- one model, ten different splits ---")
    for seed in SPLIT_SEEDS:
        accuracy = score_one_split(x, y, seed)
        scores.append(accuracy)
        print(f"seed {seed:2d} -> {accuracy:.3f}")

    print(f"lowest : {min(scores):.3f}")
    print(f"highest: {max(scores):.3f}")
    print(f"spread : {max(scores) - min(scores):.3f}")
    print(f"mean   : {sum(scores) / len(scores):.3f}")

    print("--- reproducibility ---")
    pinned_a = test_row_labels(x, y, 42)
    pinned_b = test_row_labels(x, y, 42)
    print(f"seed=42 twice, same test rows?  {pinned_a == pinned_b}")

    loose_a = test_row_labels(x, y, None)
    loose_b = test_row_labels(x, y, None)
    print(f"unseeded twice, same test rows? {loose_a == loose_b}")


if __name__ == "__main__":
    main()
```

**`sorted(x_test.index)` is the whole trick in `test_row_labels`.** After a
split, `x_test` keeps the original row numbers from the full frame — the split
shuffles which rows go where, it does not renumber them. Sorting turns the
membership of the test set into a plain list of integers, and two plain Python
lists compare with `==` to give exactly one boolean. That is what makes
`pinned_a == pinned_b` print `True` instead of an array of booleans.

**Comparing row membership, not accuracy, is the point of requirement 3.** Two
genuinely different splits can hit the same accuracy by coincidence, and on iris
they do so constantly — five of the ten seeds above land on 0.933. Had you
compared scores, you might have "proved" that unseeded splits repeat. Identical
row membership is the thing that actually shows a split repeated.

**Passing `random_state=None` explicitly.** `train_test_split` defaults to
`None`, so deleting the argument does the same thing. It does not *communicate*
the same thing. A reader — including you in three weeks — cannot tell a missing
`random_state` from a forgotten one. Writing `None` is a signature on the
decision.

**Only one knob moves.** `MODEL_SEED` is fixed at 42 for all ten fits, the
class is the same, `max_iter` is the same, `TEST_SIZE` is the same, `stratify=y`
is on throughout. The only difference between iteration 3 and iteration 7 is
which forty-five flowers ended up in the test set. So when the number changes,
there is exactly one thing it can be attributed to.

**What the numbers say.** Across seeds 0 to 9: lowest 0.933, highest 1.000,
spread 0.067, mean 0.958. One flower changing hands is worth 1/45, about 0.022,
so the whole spread is three flowers. That is the honest size of the "which
split did you use?" effect, on the easiest dataset in the book.

## Download and run

Download
[exercise-03-train-test-split-solution.py](./exercise-03-train-test-split-solution.py)
and run it:

```bash
python exercise-03-train-test-split-solution.py
```

Iris ships with scikit-learn, so there is nothing to fetch. Every seed inside
the loop is pinned, so the ten accuracies and the summary print identically each
run; the unseeded lines at the bottom are the one place randomness is left on,
on purpose, and they print `False` every time.

## Common bugs to catch

- **The seeded comparison prints `False`.** You returned `x_test.index` and
  compared two `Index` objects with `==`, which does an element-wise comparison
  and hands back forty-five booleans, not one. Put that inside an f-string or an
  `if` and you get `ValueError: The truth value of an array with more than one
  element is ambiguous. Use a.any() or a.all()`. Convert to a plain list with
  `sorted(...)`, as the answer does, or use `index_a.equals(index_b)`.
- **The spread comes out `0.000`.** Every seed printed the same score, so the
  loop variable never reached `train_test_split`. The two classic causes:
  building the split above the loop and only putting the `print` inside it, and
  writing `random_state=MODEL_SEED` (or `random_state=SPLIT_SEEDS`) where you
  meant `random_state=seed`. The second is nastier because the code still reads
  plausibly — you did pass *a* seed.
- **The unseeded comparison prints `True`.** Almost always because
  `test_row_labels` was called once and its result compared to itself. You must
  call it twice; each call runs its own unseeded shuffle. With 45 rows drawn
  from 150, two identical draws are so unlikely you can treat `False` as certain.
- **Picking the winning seed and moving on.** No error message, and it is the
  mistake this exercise exists to prevent. Seeds 0 and 2 both give 1.000 here.
  Reporting either is **seed shopping** — not usually malicious, usually just
  someone who never printed the distribution. The best seed is not information;
  it is the top of a range, and the range is the finding.
- **`ValueError: Expected 2D array, got 1D array instead.`** You passed
  `iris.data["petal width (cm)"]` while experimenting with one feature. Double
  brackets, as in Exercise 1.

## Under the hood

<details>
<summary>Under the hood — what a seed actually is, and why the same one repeats</summary>

A computer cannot flip a real coin, so `train_test_split` does not shuffle at
random in the true sense. It uses a **pseudo-random number generator**: a
formula that, starting from one number, produces a long stream of numbers that
*look* random but are completely determined by where the stream started. That
starting number is the seed — the `random_state`.

Give it `42` and it produces the exact same stream every time, so it shuffles
the rows into the exact same order and cuts the test set at the exact same
place. That is why `seed=42 twice` gives identical test rows: same seed, same
stream, same shuffle. Give it `None` and scikit-learn quietly draws a fresh
starting number from the operating system's entropy — the clock, hardware noise
— so the stream is different each call and the test set is different too. That
is why the unseeded comparison is `False`.

This is the deep reason a pinned seed makes a result *reproducible* rather than
merely *lucky*: reproducible does not mean "a good number", it means "anyone who
runs this exact code gets this exact number". A seeded experiment is a claim a
stranger can check. An unseeded one is a story about a number that no longer
exists. None of this makes the seeded score more *correct* than an unseeded one
— seed 0 and seed 3 are equally valid single samples — it just makes the whole
distribution something you can put on the table instead of one draw from it.

</details>

## Acceptance checklist

- [ ] Ten seed lines print, each with a three-decimal accuracy.
- [ ] Lowest, highest, spread and mean all print, and the spread is clearly
      greater than zero.
- [ ] `seed=42 twice` prints `True`.
- [ ] `unseeded twice` prints `False`, repeatedly, across several runs.
- [ ] You can state in one sentence why reporting only the best seed is
      dishonest even when no one lied.
- [ ] Committed with a message like `Add Week 14 exercise 3: split variance and seeding`.

## Stretch

- **Fifty seeds instead of ten.** Widen the loop to `range(50)` and the mean
  barely moves (0.958 to about 0.961) while the observed range widens — more
  draws pin down the centre and reveal more of the tails. That settling of the
  mean is the intuition behind cross-validation.
- **`cross_val_score` instead of the loop.** `cross_val_score(model, x, y, cv=5)`
  gives five numbers for one call, and unlike ten random splits its five test
  folds do not overlap — every row is tested exactly once. Fewer numbers, better
  designed.
- **Smaller test sets are noisier — but ten seeds may hide it.** Setting
  `TEST_SIZE = 0.10` does *not* obviously widen the spread over only ten seeds
  (both come out near 0.067), because with fifteen test flowers one mistake is
  worth 0.067 and the score can only take a few values. Run fifty seeds at each
  size and the effect is unmistakable: the standard deviation nearly doubles
  from `test_size=0.30` to `test_size=0.10`. Small test sets give noisy scores;
  ten samples was just too few to see it.

Next: [Exercise 4 — Scaler and Model in One Pipeline](./exercise-04-pipeline.md),
where you stop applying preprocessing by hand.
