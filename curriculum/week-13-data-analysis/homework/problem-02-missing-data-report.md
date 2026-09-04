# Homework 2 — Missing-data report

> **Topic:** `isna`, counting versus averaging booleans, `dtypes`, and sorting a summary frame
> **Lecture:** [02 — Cleaning & Transforming Data](../lecture-notes/02-cleaning-and-transforming.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** the first thing to do with a dataset you have never seen is
> find out what is not in it. A column that is three-quarters empty will happily
> produce an average, and that average will be wrong in a way nothing warns you
> about. This report is the check you run before you trust a single number.

## The Brief

Imagine a class register with a column for every pupil's swimming badge. Most
of the squares are blank, because most pupils never took the test. Now work out
"the average badge level" from that column. Whatever number comes back, it
describes the handful of pupils who *did* take the test, not the class. Nothing
on the page tells you that. The blanks are silent.

pandas has the same problem and the same silence. `df["age"].mean()` skips the
missing values without a word. So before you compute anything, you build a
report that says, column by column: how many values are missing, what
percentage that is, and what type the column holds.

Write it as a **reusable function**, not a script that works on one file:

```python
def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

Hand it any DataFrame, get back a small DataFrame indexed by column name, with
the worst offenders at the top. The classic test case is seaborn's `titanic`
dataset, where the `deck` column is about 77% empty — most passengers' cabin
letters were never recorded.

## Starter

Copy this into `problem-02-missing-data-report.py` in your homework folder.

```python
"""problem-02-missing-data-report.py — a reusable missing-data report.

Hand `missing_report` any DataFrame; get back one row per column, worst first.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

NA = np.nan


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise missingness per column, worst first.

    Returns a DataFrame indexed by column name with:
        n_missing    int    count of missing values
        pct_missing  float  percent missing, 0-100, rounded to 2 dp
        dtype        object the column's dtype, as a string
    """
    # TODO: df.isna() gives a True/False frame the same shape as df.
    # TODO: .sum() down that frame counts the Trues per column -> n_missing.
    # TODO: .mean() down that frame is the *fraction* -> times 100, round(2).
    # TODO: df.dtypes gives the types; .astype(str) makes them printable.
    # TODO: build one DataFrame from those three, name the index "column",
    #       and sort by pct_missing descending before returning it.
    return pd.DataFrame()  # placeholder, so the stub runs


#: A tiny frame with holes you can check by eye. Add rows if you like.
SAMPLE: dict[str, list] = {
    "survived": [1, 0, 1],
    "age":      [38.0, NA, 35.0],
    "deck":     ["C", NA, NA],
}


if __name__ == "__main__":
    print(missing_report(pd.DataFrame(SAMPLE)).to_string())
```

It runs as pasted and prints `Empty DataFrame`, because the stub returns an
empty one. Replace that placeholder line with the real report and the same
`print` starts saying something.

## Requirements

1. Write `missing_report(df: pd.DataFrame) -> pd.DataFrame`. It takes any
   frame and returns a new one; it never modifies the frame it was given.
2. The result is **indexed by column name**, one row per column of the input.
3. It has exactly these three columns, in this order:

   | Column | Meaning |
   |---|---|
   | `n_missing` | how many values are missing in that column |
   | `pct_missing` | percent missing, 0–100, rounded to 2 decimals |
   | `dtype` | the column's dtype, as a string |

4. Rows are sorted by `pct_missing`, **descending** — worst column first.
5. It survives the awkward inputs: an empty frame, and a frame with no
   missing values at all. No exception either way.
6. Check it against seaborn's Titanic frame if you have seaborn installed:
   `missing_report(seaborn.load_dataset("titanic"))` should put `deck` at the
   top at roughly 77%.
7. Top-of-file docstring, typed signature, no hard-coded paths.

## Constraints

- **Return a new frame; never touch the input.** A reporting function that
  quietly adds a column to the frame you handed it is a function nobody can
  call twice. Everything here reads — `isna`, `dtypes` — and nothing assigns
  back into `df`.
- **Use `isna().mean()` for the percentage, not `n_missing / len(df)`.** They
  give the same answer, but the division breaks on an empty frame with a
  `ZeroDivisionError` — or worse, silently produces `NaN` — while `.mean()` of
  an empty column is simply empty. Requirement 5 is the reason.
- **Round the percentage to 2 decimals inside the function.** The caller is
  going to print this. `76.92307692307693` is not more accurate than `76.92`
  for the purpose of "is this column usable"; it is just harder to read.
- **Convert the dtypes with `.astype(str)`.** `df.dtypes` holds real dtype
  objects, not text. Put them in a frame unconverted and pandas has to store
  them as loose Python objects, which prints inconsistently and cannot be
  sorted or compared. One `.astype(str)` and the column is plain text.
- **Sort last, build first.** Assemble all three columns, then sort the
  finished frame once. Sorting a piece at a time gets you three differently
  ordered pieces that pandas will re-align by index anyway — wasted work that
  reads like a bug.
- **Name the index `column`.** An unnamed index prints as a blank corner and
  the reader has to guess what the row labels are. One line,
  `report.index.name = "column"`, and the table says what it is.

## Expected output

The homework asks you to test against seaborn's 891-row Titanic frame.
seaborn downloads that dataset over the network the first time it is used, so
the shipped answer,
[`problem-02-missing-data-report-solution.py`](./problem-02-missing-data-report-solution.py),
points the very same `missing_report` function at a 13-row inline frame
instead. Same column names, same kind of holes, and it runs offline and
identically on every machine. `deck` still lands on top near 77%, which is the
checkpoint the brief describes. Real captured run:

```text
$ python problem-02-missing-data-report.py
          n_missing  pct_missing    dtype
column                                   
deck             10        76.92   object
age               4        30.77  float64
embarked          1         7.69   object
survived          0         0.00    int64
pclass            0         0.00    int64

empty frame ->
Empty DataFrame
Columns: [n_missing, pct_missing, dtype]
Index: []

no missing values ->
        n_missing  pct_missing   dtype
column                                
a               0          0.0   int64
b               0          0.0  object
```

Three things to notice. `deck` is 10 missing out of 13, which is 76.92% — the
77% the brief promised, arrived at from a frame you can count by hand.
`survived` and `pclass` sit at the bottom with 0.00% because they are complete,
and the sort keeps them there. And in the second table the percentages print as
`0.0`, not `0.00`: rounding produced the number zero, and pandas chooses how
many decimals to show a *column* of floats, so with nothing but zeros it shows
one. The rounding worked; the display is a separate thing.

## Steps

1. Paste the starter. Run `pd.DataFrame(SAMPLE).isna()` on its own and look at
   the True/False frame. That grid is the whole idea.
2. Add `.sum()` to it. Confirm you get one number per column, and that they
   match what you can see by eye.
3. Add `.mean()` to the same `isna()` frame instead. Confirm you get fractions
   between 0 and 1 — 0.667 for `deck` in the small sample.
4. Multiply by 100 and round to 2. Now build the three-column DataFrame.
5. Name the index and sort descending. Print with `.to_string()` so nothing is
   abbreviated with `...`.
6. Call it on `pd.DataFrame()` — a completely empty frame — and on a frame with
   no holes. Fix whatever breaks.
7. If you have seaborn installed, run
   `print(missing_report(seaborn.load_dataset("titanic")).to_string())` and
   check that `deck` leads at roughly 77.10%.

## The Solution

```python
"""hw-02-missing-report.py — a reusable missing-data report for any DataFrame.

The homework tests this against seaborn's 891-row Titanic frame. So it runs
offline and identically everywhere, this shipped answer instead points the same
function at a small inline frame with a deliberately ``deck``-like column that is
about three-quarters empty — the report should float it to the top near 77%,
exactly the checkpoint the homework describes.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

NA = np.nan


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise missingness per column, worst first.

    Returns a DataFrame indexed by column name with:
        n_missing    int    count of missing values
        pct_missing  float  percent missing, 0-100, rounded to 2 dp
        dtype        object the column's dtype, as a string
    """
    report = pd.DataFrame(
        {
            "n_missing": df.isna().sum(),
            "pct_missing": (df.isna().mean() * 100).round(2),
            "dtype": df.dtypes.astype(str),
        }
    )
    report.index.name = "column"
    return report.sort_values("pct_missing", ascending=False)


#: 13 passengers, real column names, real holes: deck ~77% missing, age ~31%.
SAMPLE: dict[str, list] = {
    "survived": [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    "pclass":   [1, 3, 1, 2, 3, 3, 1, 3, 2, 3, 1, 3, 2],
    "age":      [38.0, NA, 35.0, 28.0, NA, 24.0, 40.0, NA, 31.0, 22.0, NA, 27.0, 45.0],
    "deck":     ["C", NA, NA, NA, NA, NA, "E", NA, NA, NA, "B", NA, NA],
    "embarked": ["C", "S", "S", "S", "Q", "S", "S", "S", NA, "S", "C", "S", "S"],
}


if __name__ == "__main__":
    frame = pd.DataFrame(SAMPLE)
    print(missing_report(frame).to_string())

    # Edge cases the function has to survive.
    print()
    print("empty frame ->")
    print(missing_report(pd.DataFrame()).to_string())
    print()
    print("no missing values ->")
    print(missing_report(pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})).to_string())
```

**`isna()` turns the frame into a grid of yes-or-no.** Every cell becomes
`True` if the value is missing and `False` if it is there — same rows, same
columns, same shape. Everything else on this page is a question asked of that
grid, and that is why the function is five lines long instead of a loop over
columns.

**`.sum()` and `.mean()` on that grid answer two different questions from the
same booleans.** Python treats `True` as 1 and `False` as 0, so summing a
column of booleans counts the `True`s, and averaging them gives the *fraction*
that are `True`. For `deck`: `sum` is 10, `mean` is 0.769230…, and
`mean * 100` rounded is `76.92`. One grid, two answers, no division by hand.

**`df.dtypes` is a Series indexed by column name — the same index the other
two have.** That is the quiet reason the three pieces snap together inside one
`pd.DataFrame({...})` call with no merging or zipping. All three are labelled
by column name, so pandas aligns them by label, and a column that appeared in
one and not the others would show up as a hole rather than silently shifting
everything by a row. `.astype(str)` turns `dtype('float64')` into the text
`"float64"` so the column is ordinary strings.

**Sorting happens once, on the finished frame.**
`report.sort_values("pct_missing", ascending=False)` returns a new frame in
worst-first order, and returning it directly means the caller cannot forget to
sort. Columns that tie — the two 0.00% ones — keep the order they arrived in,
because pandas' default sort is stable.

**The empty frame works by accident of good choices, not by a special case.**
`pd.DataFrame().isna().sum()` is an empty Series; so is `.mean()`; so is
`dtypes`. Build a frame from three empty Series and you get a frame with the
three column names and no rows, which is exactly what an empty input should
report. Had the percentage been computed as `n_missing / len(df)`, that same
call would have been a division by zero. The choice on line one is what makes
the edge case a non-event.

**The sample frame is 13 rows because 13 rows can be checked by hand.**
`deck` has three letters and ten blanks; you can count them in the source and
confirm 76.92% yourself. A report you cannot verify on a small case is a report
you are trusting rather than testing. Point the same function at the real
891-row Titanic frame and nothing changes but the numbers.

## Run it

Copy the worked answer on this page into `problem-02-missing-data-report.py` and run it:

```bash
python -m pip install pandas numpy
python problem-02-missing-data-report.py
```

It needs only pandas and NumPy — no network, no data files. It prints the
report for the sample frame and then the two edge cases. The `-solution` suffix
keeps it from colliding with your own
`problem-02-missing-data-report.py`. Its docstring still carries the older
`hw-02-` filename from the original brief; the code is unchanged.

To try the Titanic check yourself, add seaborn:

```bash
python -m pip install seaborn
```

then in a Python session:

```python
import seaborn
print(missing_report(seaborn.load_dataset("titanic")).to_string())
```

That call downloads the dataset the first time, so it needs a network
connection.

## Common bugs to catch

- **`AttributeError: 'NoneType' object has no attribute 'to_string'`.** Your
  `missing_report` fell off the end without a `return` — you built the report
  into a local variable and never handed it back.
- **`pct_missing` comes back between 0 and 1.** You used `.mean()` and forgot
  the `* 100`. The brief asks for 0–100.
- **Every percentage is 0 or 100 and nothing in between.** You used
  `.sum() / .count()` or similar on integers, and integer division threw away
  the fraction. `.mean()` on the boolean grid avoids this entirely.
- **`ZeroDivisionError: division by zero`.** An empty frame reached your
  `n_missing / len(df)`. Switch to `.mean()`.
- **`TypeError: '<' not supported between instances of 'dtype' and 'dtype'`.**
  You put raw dtype objects in the frame and then sorted on them. `.astype(str)`
  first.
- **The row labels print as `0 1 2 3` instead of column names.** You called
  `.reset_index()` somewhere, or built the frame from lists instead of from the
  three Series. Keep the index pandas gave you.
- **A column of empty strings reports 0 missing.** It is: `""` is a value, and
  `isna` is asking about `NaN` and `None`, not about emptiness. If blanks
  arrived as `""`, convert them first with
  `df.replace("", np.nan)`.
- **A column of `"NA"` or `"-"` strings reports 0 missing.** Same cause. Tell
  `pd.read_csv` about them when you load:
  `pd.read_csv(path, na_values=["NA", "-", "n/a"])`.
- **The output is cut off with `...` in the middle.** `print(df)` abbreviates
  wide or tall frames. `print(df.to_string())` does not.

## Under the hood

<details>
<summary>Under the hood — NaN, None and NaT are three different holes</summary>

pandas has more than one way to be missing, and they are not interchangeable.

`np.nan` is a *float* — "not a number", part of the IEEE 754 floating point
standard the hardware implements. It is why a column with one missing value
turns from `int64` into `float64`: the old NumPy integer types have no spare
bit pattern to mean "absent", so pandas widens the column to floats, where
`nan` already exists. This is the single most surprising thing about missing
data in pandas, and it explains a whole family of "why did my IDs grow decimal
points" questions.

`None` is Python's own empty object. In an `object` column — text, usually —
pandas keeps it as `None`, and `isna()` reports it as missing just the same.

`NaT`, "not a time", is the datetime version, and it lives in `datetime64`
columns.

`isna()` treats all three as missing, which is exactly why the report uses it
rather than comparing to anything. And it has to: `np.nan == np.nan` is
`False`. A missing value is not equal to itself, by design — the standard says
an unknown quantity cannot be shown to equal another unknown quantity. So
`df[df["age"] == np.nan]` returns nothing at all, silently, forever. Use
`df[df["age"].isna()]`.

Newer pandas adds `pd.NA` and the nullable dtypes (`Int64` with a capital I,
`boolean`, `string`), which keep integers as integers and carry a separate
mask of which cells are absent. Load a frame with
`pd.read_csv(path, dtype_backend="numpy_nullable")` and your ID column stays an
integer column with holes in it. Everything on this page works unchanged; the
`dtype` column just reports `Int64` instead of `float64`.

</details>

<details>
<summary>Under the hood — why summing booleans is fast, not a trick</summary>

`True + True == 2` looks like a Python quirk you should not lean on. Under a
DataFrame it is not a quirk at all.

`df.isna()` produces a NumPy array of `bool` dtype: one byte per cell, packed
in a single contiguous block of memory. `.sum()` on that block runs a loop
written in C over raw bytes, adding them as small integers, with no Python
object created per cell. On a million-row column that is one pass over a
megabyte of memory — microseconds. The equivalent
`sum(1 for v in column if pd.isna(v))` builds a million Python objects and
takes hundreds of times longer.

`.mean()` is the same pass followed by one division, which is why asking for
both the count and the percentage costs almost exactly what asking for one
does.

The same fact is what makes boolean *masks* work: `df[df["age"] > 30]` builds
a byte-per-row array of yes-or-no and hands it to pandas, which walks it in C
and keeps the rows marked yes. Counting a condition is just `.sum()` on that
same mask — `(df["age"] > 30).sum()` — and it is the shortest correct way to
answer "how many rows match".

</details>

<details>
<summary>Under the hood — what to do once the report tells you</summary>

The report is a diagnosis, not a treatment. Four honest responses, roughly in
order of how often they are right:

**Leave it.** `mean`, `sum` and friends already skip missing values. If you are
computing an average age and 30% of ages are absent, the average is correct for
the rows that have one — as long as you say so, and as long as the absent rows
are not systematically different from the present ones.

**Drop the column.** `df.drop(columns="deck")`. At 77% missing, `deck` cannot
support a conclusion. Keeping it invites somebody to use it.

**Drop the rows.** `df.dropna(subset=["age"])` removes rows missing a
specific value. `df.dropna()` removes every row with *any* hole, which on a
wide frame can quietly delete most of your data — check `len` before and after,
every time.

**Fill it.** `df["age"].fillna(df["age"].median())` puts the middle value in
every gap. This is the one that needs a warning label: it shrinks the spread of
the column, because you have added a pile of identical values at the centre.
Any standard deviation or confidence interval computed afterwards is narrower
than the truth. If you fill, add a `age_was_missing` boolean column first, so
the fact survives.

The order matters more than the technique. Report, then decide, then fill —
never fill first and report on the filled frame, which will cheerfully tell you
nothing is missing.

</details>

## Acceptance checklist

- [ ] `missing_report` returns a new frame and leaves the input untouched.
- [ ] The result is indexed by column name, with the index named `column`.
- [ ] Columns are exactly `n_missing`, `pct_missing`, `dtype`, in that order.
- [ ] `pct_missing` is 0–100 with two decimals, not a 0–1 fraction.
- [ ] Rows are sorted worst-first.
- [ ] An empty frame and a frame with no holes both return without raising.
- [ ] On the sample frame, `deck` leads at 76.92%.
- [ ] The signature is typed and the file has a docstring.
- [ ] Committed to Git with a message like
      `Add Week 13 homework 2: missing-data report`.

## Stretch

- Add a `n_unique` column with `df.nunique()`. A column that is 0% missing and
  has exactly one unique value is just as useless as an empty one, and this is
  how you spot it.
- Add `first_valid`, showing an example real value per column with
  `df[col].dropna().iloc[0]`. It turns "object, 7% missing" into "object, 7%
  missing, looks like `'Southampton'`", which is what you actually wanted.
- Add a `threshold` parameter that returns only columns above a given
  percentage, so `missing_report(df, threshold=50)` is a shortlist for
  deletion.
- Make the report renderable as Markdown with `.to_markdown()` and paste it
  into your notes. It needs `pip install tabulate`.
- Run it over three different datasets and write two sentences on each about
  which columns you would refuse to use, and why.

When your report survives the empty frame, move on to
[Homework 3 — Merge two DataFrames](./problem-03-merge-dataframes.md).
