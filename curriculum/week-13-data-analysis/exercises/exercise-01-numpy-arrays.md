# Exercise 1 — NumPy Arrays

> **Topic:** Creating arrays, vector math, broadcasting
> **Lecture:** [01 — NumPy & pandas Basics](../lecture-notes/01-numpy-and-pandas-basics.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** pandas is NumPy underneath. Every DataFrame column is an
> array and every filter is a boolean array, so twenty minutes on plain arrays
> now makes the next four exercises feel like one idea wearing four hats.

## The Brief

A neighborhood community center put solar panels on its roof last spring. The
building manager writes down the kilowatt-hours produced each day and the
cloud cover reported at noon. Ten days of that log are in the starter below.

Your job is to answer the questions the manager actually asks — total output,
what it saved, the best day, how many days beat the average — without writing
a single `for` loop. That constraint is the exercise. A mean, a mask, and a
scalar multiply over a whole array is the mental model pandas is built on.

## Starter

Copy this into `exercise-01-numpy-arrays.py` in your practice repo, then fill
in the TODOs.

```python
"""exercise-01-numpy-arrays.py — vector math on ten days of solar output.

Reports totals, averages, the best day, and above-average days using
NumPy array operations only. No Python loops.
"""

import numpy as np

SOLAR_LOG: dict[str, list[int]] = {
    "day":       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "kwh":       [18, 23, 19, 24, 21, 17, 23, 20, 26, 17],
    "cloud_pct": [40, 10, 35, 5, 20, 55, 10, 30, 0, 60],
}

RATE_PER_KWH = 0.18


def main() -> None:
    """Print the nine report lines described in the exercise brief."""
    days = np.array(SOLAR_LOG["day"])
    kwh = np.array(SOLAR_LOG["kwh"])
    cloud = np.array(SOLAR_LOG["cloud_pct"])

    print(f"Readings: {kwh}")
    print(f"dtype={kwh.dtype}  shape={kwh.shape}  ndim={kwh.ndim}")

    # TODO: total and mean production
    # print(f"Total: {...} kWh")
    # print(f"Mean: {...:.2f} kWh")

    # TODO: best day. np.argmax gives the *position* of the largest value.
    #       Use that position to index days, kwh, and cloud.

    # TODO: revenue. Multiply the whole kwh array by RATE_PER_KWH
    #       (broadcasting a scalar), then sum it.

    # TODO: deviation from the mean, rounded to 1 decimal and printed
    #       as a Python list: np.round(deviation, 1).tolist()

    # TODO: a boolean mask of above-average days, then the count
    #       and the mean of just those days.


if __name__ == "__main__":
    main()
```

## Requirements

1. Print `Readings:` followed by the raw `kwh` array. Do not convert it to a
   list first — the array's own display is part of what you are learning to
   read.
2. Print `Total: 208 kWh` and `Mean: 20.80 kWh`, the mean formatted with
   `:.2f`.
3. Print the best day using `np.argmax`, in the form
   `Best day: day 9 (26 kWh, 0% cloud)`.
4. Print total revenue as `Revenue at $0.18/kWh: $37.44`, computed by
   multiplying the whole array by `RATE_PER_KWH` and summing the result.
5. Print each day's distance from the mean, rounded to one decimal, as a
   Python list.
6. Print how many days beat the average and what those days averaged.
7. No `for` loop, no `while` loop, and no list comprehension anywhere in the
   file.

## Constraints

- **No Python loops.** Every one of these answers has a one-line vectorized
  form. A loop would give the same numbers, but the point of the exercise is
  the vectorized habit — when the array is ten million rows instead of ten,
  the loop is thirty seconds and the vectorized version is thirty
  milliseconds.
- **Use `np.argmax`, not `kwh.max()` followed by a search.** `max()` tells you
  *what* the best value was; you also need to know *which day* it belongs to,
  so you can pull the matching entry out of `days` and `cloud`. Position-based
  lookup across parallel arrays is exactly how a DataFrame row works.
- **Round the deviation array with `np.round(..., 1).tolist()` before
  printing.** `20.8` is not representable exactly in binary, so
  `18 - kwh.mean()` is really `-2.8000000000000007`. Rounding to one decimal
  and converting to a list gives output that is stable on every machine.
  Float noise is not a bug in your code; hiding it at the display layer is the
  normal fix.
- **Build the mask as its own named variable** (`above = kwh > kwh.mean()`)
  rather than inlining it. You read that mask twice — once for the count, once
  for the filtered mean — and naming it makes the second use obvious.

## Expected output

```text
$ python exercise-01-numpy-arrays.py
Readings: [18 23 19 24 21 17 23 20 26 17]
dtype=int64  shape=(10,)  ndim=1
Total: 208 kWh
Mean: 20.80 kWh
Best day: day 9 (26 kWh, 0% cloud)
Revenue at $0.18/kWh: $37.44
Deviation from mean: [-2.8, 2.2, -1.8, 3.2, 0.2, -3.8, 2.2, -0.8, 5.2, -3.8]
Above-average days: 5 of 10
Above-average mean: 23.40 kWh
```

Two things there are worth pausing on. The deviations sum to exactly zero —
that is what "mean" means, and it is a free check on your arithmetic. And day
8 produced exactly 20 kWh, below the 20.8 mean, so it is *not* one of the
above-average five. If you get six, your comparison is against 20, not 20.8.

## Steps

1. Activate the week's virtual environment and confirm NumPy is installed:
   `python -c "import numpy; print(numpy.__version__)"`.
2. Create `exercise-01-numpy-arrays.py` and paste the starter.
3. Fill in the total and mean first, then run it. Two correct lines beat six
   guesses.
4. Add the best-day line. Print `np.argmax(kwh)` on its own once, so you see
   that it returns `8` — a position, not a day number.
5. Add revenue, then the deviation list, then the mask. Run after each.
6. Break it on purpose: change the mask to `kwh >= 20` and watch the count go
   from 5 to 6, because day 8's exactly-20 reading now qualifies. Change it
   back. Note what does *not* happen if you try `kwh > 20` instead: the count
   stays at 5. The mean is 20.8, so `> mean` and `> 20` keep out the same days,
   and a strict `>` still shuts day 8 out. Which way the boundary faces is the
   whole difference.

## The Solution

```python
"""exercise-01-numpy-arrays.py — vector math on ten days of solar output.

Reports totals, averages, the best day, and above-average days using
NumPy array operations only. No Python loops.
"""

import numpy as np

SOLAR_LOG: dict[str, list[int]] = {
    "day":       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "kwh":       [18, 23, 19, 24, 21, 17, 23, 20, 26, 17],
    "cloud_pct": [40, 10, 35, 5, 20, 55, 10, 30, 0, 60],
}

RATE_PER_KWH = 0.18


def main() -> None:
    """Print the nine report lines described in the exercise brief."""
    days = np.array(SOLAR_LOG["day"])
    kwh = np.array(SOLAR_LOG["kwh"])
    cloud = np.array(SOLAR_LOG["cloud_pct"])

    print(f"Readings: {kwh}")
    print(f"dtype={kwh.dtype}  shape={kwh.shape}  ndim={kwh.ndim}")

    total = kwh.sum()
    mean = kwh.mean()
    print(f"Total: {total} kWh")
    print(f"Mean: {mean:.2f} kWh")

    best = np.argmax(kwh)
    print(f"Best day: day {days[best]} ({kwh[best]} kWh, {cloud[best]}% cloud)")

    revenue = (kwh * RATE_PER_KWH).sum()
    print(f"Revenue at ${RATE_PER_KWH}/kWh: ${revenue:.2f}")

    deviation = kwh - mean
    print(f"Deviation from mean: {np.round(deviation, 1).tolist()}")

    above = kwh > mean
    print(f"Above-average days: {above.sum()} of {kwh.size}")
    print(f"Above-average mean: {kwh[above].mean():.2f} kWh")


if __name__ == "__main__":
    main()
```

**`mean` is computed once and reused four times.** Look at how many lines
depend on it: the `Mean:` line, the deviation array, the mask, and — through the
mask — both above-average lines. Writing `kwh.mean()` inline in each of those
would recompute the same average four times and, worse, would let the four
copies drift apart the day you decide to exclude a bad reading. One named
variable, one definition of "average". This is the same reasoning that makes
`RATE_PER_KWH` a constant instead of a `0.18` typed into the revenue line.

**`np.argmax` returns a position, and a position is a key into every parallel
array.** `np.argmax(kwh)` is `8`, not `26` and not `9`. That single integer then
indexes `days`, `kwh`, and `cloud` — three separate arrays that happen to be
aligned — and pulls one field from each. That alignment-by-position *is* what a
DataFrame row is, and holding that idea now makes Exercise 2 feel like a
notation change rather than a new concept. It is also why pandas ships two
different accessors, `.iloc` for positions and `.loc` for labels: the two are
genuinely different questions, and NumPy only has the first one.

**The mask is a variable because you use it twice.** `above` is ten booleans:
`[False, True, False, True, True, False, True, False, True, False]`. Summing it
gives 5, because `True` counts as 1 — that is the idiom, not a trick. Indexing
with it, `kwh[above]`, keeps the five days where it is `True`. Naming the mask
means the count and the filtered mean provably describe the same five days. Two
inline copies of `kwh > kwh.mean()` would be two chances to get one of them
wrong.

**Rounding happens at the display layer, not in the arithmetic.** `deviation` is
kept as full-precision floats and only `np.round(deviation, 1)` is printed. That
matters because you never want to round data you are going to compute with
again — you want to round the thing a human reads. Here the difference is
visible: unrounded, day 1's deviation is `-2.8000000000000007`, because 20.8 has
no exact binary representation. The number is not wrong; the display is just
honest about a base-2 machine holding a base-10 value.

**The whole file obeys the no-loops constraint without effort.** Seven of the
nine printed lines are one expression each. That is not code golf — it is the
reason NumPy exists. On ten readings a Python loop costs nothing; on ten million
it is the difference between thirty milliseconds and half a minute, because the
vectorized form runs the arithmetic in compiled C over a contiguous block of
memory instead of unboxing ten million Python integers one at a time.

One free arithmetic check is built into the output: the deviations sum to
exactly zero. They must, because the mean is the value that makes them do so. If
your deviation list does not roughly cancel out, your mean is wrong before
anything else is.

## Run it

Copy the worked answer on this page into `exercise-01-numpy-arrays.py` and run it:

```bash
python exercise-01-numpy-arrays.py
```

It needs only NumPy and prints the nine report lines described in the brief. The `-solution` suffix keeps it from colliding with your own `exercise-01-numpy-arrays.py`.

## Common bugs to catch

- **`ValueError: The truth value of an array with more than one element is
  ambiguous. Use a.any() or a.all()`.** You wrote something like
  `if kwh > kwh.mean():`. An array comparison produces ten booleans, and
  Python cannot decide whether ten booleans are "true". You do not want an
  `if` here at all — you want to index with the mask: `kwh[above]`.
- **`Total: 208.0 kWh` instead of `Total: 208 kWh`.** You summed the Python
  list (`sum(SOLAR_LOG["kwh"])` gives an int) or the array of a float dtype.
  `np.array([18, 23, ...])` is an integer array, and `.sum()` on it returns an
  integer. If you see a `.0`, check that you did not divide somewhere.
- **`dtype=int32` on your machine.** On Windows with NumPy 1.x the default
  integer is 32-bit. Nothing is wrong; your numbers are identical. NumPy 2.0
  changed the Windows default to `int64`, which is what the expected output
  shows.
- **`Deviation from mean: [-2.8000000000000007, ...]`.** You skipped the
  `np.round(..., 1)` step. See the constraint about binary floats — this is
  expected behavior, not a mistake in your subtraction.
- **`Best day: day 8`.** You printed the argmax position instead of using it
  to look up `days[best]`. Position `8` is the ninth element, and the ninth
  element of `days` is `9`. Off-by-one errors between position and label are
  the single most common pandas bug too, which is why `.loc` and `.iloc` exist
  as separate accessors.
- **`AttributeError: 'list' object has no attribute 'mean'`.** You called
  `.mean()` on `SOLAR_LOG["kwh"]` — still a plain Python list — instead of on
  the array you built from it. Check that every calculation uses `kwh`, not
  the dict.

## Under the hood

<details>
<summary>Under the hood — how a scalar multiplies a whole array</summary>

`kwh * RATE_PER_KWH` never loops in Python. NumPy sees an array times a single
number and *broadcasts* the number across every element, running the multiply
in compiled C over one contiguous block of memory. On ten readings that saves
nothing; on ten million it is the difference between thirty milliseconds and
half a minute, because a Python loop would unbox ten million integers one at a
time.

The same rule stretches to whole rows. Stack the two logs into one 2-D array
and ask for a per-row mean:

```python
arr = np.array([SOLAR_LOG["kwh"], SOLAR_LOG["cloud_pct"]])
print(arr.shape)                       # (2, 10)
print(arr.mean(axis=1))                # [20.8 26.5] — one number per row
print(arr - arr.mean(axis=1, keepdims=True))
```

`axis` names the dimension that *disappears*: `axis=1` collapses the ten columns
and leaves one mean per row. `keepdims=True` keeps the result shaped `(2, 1)` so
it lines up against the `(2, 10)` array — drop it and you get a flat `(2,)` pair,
NumPy tries to line `2` up against `10` from the right, and raises `ValueError:
operands could not be broadcast together`. Reading that message once is the
fastest way to learn the rule: line the shapes up right-justified, and every
pair must match or one of them must be 1.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and prints exactly nine lines.
- [ ] All nine lines match the expected output above.
- [ ] There is no `for`, no `while`, and no list comprehension in the file.
- [ ] The above-average count is 5, not 6.
- [ ] `RATE_PER_KWH` is a module-level constant, not a number typed inline.
- [ ] Every function has a type-hinted signature and a docstring.
- [ ] The file is committed to Git with a message like
      `Add Week 13 exercise 1: numpy arrays`.

## Stretch

- Print the mean cloud cover on above-average days versus the rest, using the
  same mask and its inverse (`~above`). If the panels behave sensibly, the
  sunny group should have far lower cloud cover.
- Build a 2-D array with `np.array([SOLAR_LOG["kwh"], SOLAR_LOG["cloud_pct"]])`
  and print its `shape`. Then take `arr.mean(axis=1)` and `arr.mean(axis=0)`
  and say in words what each answer means. Getting `axis` right is worth more
  than any other NumPy detail.
- Center that 2-D array on its per-row means:
  `arr - arr.mean(axis=1, keepdims=True)`. Remove `keepdims=True` and read the
  error — that message teaches the broadcasting rules faster than the docs do.

When your nine lines match, move on to
[Exercise 2 — Load and Inspect](./exercise-02-load-and-inspect.md).
