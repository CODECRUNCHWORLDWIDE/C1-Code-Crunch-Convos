# Exercise 2 — Load and Inspect

> **Topic:** Building a DataFrame and forming a mental model of it in under a minute
> **Lecture:** [01 — NumPy & pandas Basics](../lecture-notes/01-numpy-and-pandas-basics.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** every analysis starts with the same four questions — how
> big is this, what are the columns, what type is each one, and is anything
> missing. Analysts who skip the inspection step spend the next hour debugging
> a mean that came back `NaN` for a reason they never checked for.

## The Brief

A city library system has twelve branches. Someone in the director's office
pulled last month's numbers into a spreadsheet: visits, holds filled, and the
hours each branch was open. The spreadsheet has since gone missing, but the
numbers are below, so you will rebuild the table from a dictionary of lists —
the same shape `read_csv` would hand you, minus the file.

Your job is not to answer any question about libraries yet. It is to
*describe the table*: its shape, its column types, its summary statistics, and
how many branches sit in each region. Then add one derived column, visits per
open hour, because a branch open 60 hours a week should not be compared head
to head with one open 32.

**Run it either way.** The starter is laid out as numbered notebook cells.
Paste them into `exercise-02-load-and-inspect.ipynb` and run top to bottom, or
paste the same code into a `.py` file and run it as a script. Every cell uses
`print()`, so the output is identical. In a notebook you can also drop the
`print()` from a cell's last line and pandas renders an HTML table instead —
nicer to look at, same data.

## Starter

```python
# --- Cell 1 — imports ---
"""exercise-02-load-and-inspect.py — first look at a twelve-branch table."""

import pandas as pd


# --- Cell 2 — the data ---
BRANCHES: dict[str, list] = {
    "branch": [
        "Alder", "Birch", "Cedar", "Dogwood", "Elm", "Fir",
        "Ginkgo", "Hawthorn", "Ironwood", "Juniper", "Katsura", "Linden",
    ],
    "region": [
        "North", "South", "North", "East", "South", "North",
        "West", "South", "North", "East", "South", "North",
    ],
    "visits":       [4820, 3110, 5640, 2980, 6150, 3720,
                     4410, 5230, 2760, 6890, 3980, 5010],
    "holds_filled": [612, 488, 903, 377, 1044, 521,
                     688, 815, 342, 1176, 559, 742],
    "open_hours":   [48, 40, 56, 32, 56, 40, 48, 56, 32, 60, 40, 48],
}

df = pd.DataFrame(BRANCHES)


# --- Cell 3 — the first five rows ---
print("--- head ---")
print(df.head())


# --- Cell 4 — size and column types ---
# TODO: print df.shape under the "--- shape ---" banner
# TODO: print df.dtypes under the "--- dtypes ---" banner


# --- Cell 5 — the full structural summary ---
# TODO: call df.info(). Note that info() prints by itself and returns None,
#       so `print(df.info())` would add a stray "None" line. Just call it.


# --- Cell 6 — summary statistics ---
# TODO: print df.describe().round(2)


# --- Cell 7 — how many branches per region ---
# TODO: print the value_counts of the region column


# --- Cell 8 — the last three rows ---
# TODO: print df.tail(3)


# --- Cell 9 — one derived column ---
# TODO: add df["visits_per_hour"], the visits divided by open_hours,
#       rounded to 1 decimal. Then print the branch, region, and
#       visits_per_hour columns for the first five rows.
```

## Requirements

1. Every banner prints exactly as written — `--- head ---`, `--- shape ---`,
   `--- dtypes ---`, `--- info ---`, `--- describe ---`,
   `--- value_counts ---`, `--- tail(3) ---`, `--- derived ---` — so your
   output is diff-able against the block below.
2. `df.shape` prints as the tuple `(12, 5)`. It is an attribute, not a method
   — no parentheses.
3. `df.info()` is called, not printed. `df.describe()` is rounded to two
   decimals before printing.
4. `value_counts()` runs on the `region` column only.
5. The derived column is named `visits_per_hour` and rounded to one decimal.
6. The final print shows only `branch`, `region`, and `visits_per_hour`, for
   the first five rows.

## Constraints

- **Do not call `print()` on `df.info()`.** `info()` writes to standard output
  itself and returns `None`, so wrapping it prints the report and then the
  word `None`. This trips up nearly everyone once; it is worth tripping over
  here rather than in your mini-project.
- **Round `describe()` rather than reformatting it by hand.** Raw `describe()`
  gives six decimal places, which is noise for visit counts. `.round(2)` is one
  call and returns a new DataFrame of the same shape. Never reach for string
  formatting when a DataFrame method already does the job.
- **Select the three final columns with a list inside the brackets** —
  `df[["branch", "region", "visits_per_hour"]]`. The double brackets look odd
  until you see them as two separate things: the outer pair is the indexing
  operation, the inner pair is a Python list. `df["branch", "region"]` without
  the inner list raises `KeyError`.
- **Build the derived column with vectorized division**, not `apply` and not a
  loop. `df["visits"] / df["open_hours"]` divides the two columns row by row
  in compiled code. An `apply(axis=1)` here would be slower and longer for no
  benefit.
- **Leave the index alone.** You may be tempted to `set_index("branch")` so
  the table reads nicer. Do not, for this exercise — the expected output below
  shows the default `RangeIndex`, and one of the things `info()` is telling
  you is that the index is a plain `0..11` range.

## Expected output

```text
$ python exercise-02-load-and-inspect.py
--- head ---
    branch region  visits  holds_filled  open_hours
0    Alder  North    4820           612          48
1    Birch  South    3110           488          40
2    Cedar  North    5640           903          56
3  Dogwood   East    2980           377          32
4      Elm  South    6150          1044          56
--- shape ---
(12, 5)
--- dtypes ---
branch          object
region          object
visits           int64
holds_filled     int64
open_hours       int64
dtype: object
--- info ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 5 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   branch        12 non-null     object
 1   region        12 non-null     object
 2   visits        12 non-null     int64 
 3   holds_filled  12 non-null     int64 
 4   open_hours    12 non-null     int64 
dtypes: int64(3), object(2)
memory usage: 612.0+ bytes
--- describe ---
        visits  holds_filled  open_hours
count    12.00         12.00       12.00
mean   4558.33        688.92       46.33
std    1305.44        258.82        9.57
min    2760.00        342.00       32.00
25%    3567.50        512.75       40.00
50%    4615.00        650.00       48.00
75%    5332.50        837.00       56.00
max    6890.00       1176.00       60.00
--- value_counts ---
region
North    5
South    4
East     2
West     1
Name: count, dtype: int64
--- tail(3) ---
     branch region  visits  holds_filled  open_hours
9   Juniper   East    6890          1176          60
10  Katsura  South    3980           559          40
11   Linden  North    5010           742          48
--- derived ---
    branch region  visits_per_hour
0    Alder  North            100.4
1    Birch  South             77.8
2    Cedar  North            100.7
3  Dogwood   East             93.1
4      Elm  South            109.8
```

Read the `describe()` block the way an analyst would. The median (`50%`) is
4615 against a mean of 4558 — close together, so no single branch is dragging
the average. A standard deviation of 1305 says the branches are genuinely
different sizes. And `count` is 12 on every column, which is `info()`'s
"12 non-null" said a second way: nothing you compute later will silently come
back as `NaN`. Note too that `describe()` shows three columns, not five —
`branch` and `region` are `object` dtype, and `describe()` skips non-numeric
columns unless you pass `include="all"`.

## Steps

1. Create the notebook with `jupyter notebook` (or a new `.ipynb` in VS Code),
   or the `.py` file if you prefer a script.
2. Paste cells 1 through 3 and run them. You should see the five-row head.
3. Fill in cells 4 and 5. Read `info()` left to right: 12 entries, 5 columns,
   non-null count per column, dtype per column, memory.
4. Fill in cell 6 and compare your `describe()` numbers to the block above.
5. Fill in cell 7. Guess which region has the most branches before you run it.
6. Fill in cells 8 and 9 and run the whole thing top to bottom.
7. In a notebook, restart the kernel and run all cells in order once more. A
   notebook that only works because you ran cells out of order will not work
   tomorrow.

## The Solution

```python
# --- Cell 1 — imports ---
"""exercise-02-load-and-inspect.py — first look at a twelve-branch table."""

import pandas as pd


# --- Cell 2 — the data ---
BRANCHES: dict[str, list] = {
    "branch": [
        "Alder", "Birch", "Cedar", "Dogwood", "Elm", "Fir",
        "Ginkgo", "Hawthorn", "Ironwood", "Juniper", "Katsura", "Linden",
    ],
    "region": [
        "North", "South", "North", "East", "South", "North",
        "West", "South", "North", "East", "South", "North",
    ],
    "visits":       [4820, 3110, 5640, 2980, 6150, 3720,
                     4410, 5230, 2760, 6890, 3980, 5010],
    "holds_filled": [612, 488, 903, 377, 1044, 521,
                     688, 815, 342, 1176, 559, 742],
    "open_hours":   [48, 40, 56, 32, 56, 40, 48, 56, 32, 60, 40, 48],
}

df = pd.DataFrame(BRANCHES)


# --- Cell 3 — the first five rows ---
print("--- head ---")
print(df.head())


# --- Cell 4 — size and column types ---
print("--- shape ---")
print(df.shape)
print("--- dtypes ---")
print(df.dtypes)


# --- Cell 5 — the full structural summary ---
print("--- info ---")
df.info()


# --- Cell 6 — summary statistics ---
print("--- describe ---")
print(df.describe().round(2))


# --- Cell 7 — how many branches per region ---
print("--- value_counts ---")
print(df["region"].value_counts())


# --- Cell 8 — the last three rows ---
print("--- tail(3) ---")
print(df.tail(3))


# --- Cell 9 — one derived column ---
print("--- derived ---")
df["visits_per_hour"] = (df["visits"] / df["open_hours"]).round(1)
print(df[["branch", "region", "visits_per_hour"]].head())
```

**The five calls answer five different questions, and the order is not
arbitrary.** `head()` asks "what does a row look like" — it is the one that
catches a header row read in as data, or a column that is one position to the
left of where you expected. `shape` asks "did I get everything" — twelve rows
because there are twelve branches, and if it said eleven you would go looking
for the branch that vanished. `dtypes` and `info()` ask "can I do arithmetic on
this" — an `object` where you expected `int64` means a number arrived as a
string. `describe()` asks "are the values plausible" — a minimum of `-1` in a
visits column is a data-entry error, not an analysis to be run. And
`value_counts()` asks "how is the categorical variable distributed" — four
regions, wildly unequal, which is exactly the sort of thing that makes a later
group mean rest on a single branch.

**`shape` is an attribute; `head()` and `describe()` are methods.** The rule is
not arbitrary either. An attribute is something the frame simply *is* — its
shape, its dtypes, its columns, its index. A method is something it *does* —
compute a summary, take five rows. pandas keeps the distinction consistently, so
once you have the rule you can guess correctly for anything you have not met
yet.

**`info()` prints and returns `None`, so it is called, not printed.** That is
unusual for pandas, where almost everything returns a value you can chain onto.
`info()` is one of a small handful of methods written for a human at a terminal
rather than for a program, and the sign of that is the `None`. The report it
writes is also the densest thing on the page: class, index type and range,
column count, then one line per column giving position, name, non-null count,
and dtype, then the dtype tally and the memory figure. Read it left to right and
you have the whole structure of the table.

**`describe()` shows three columns, not five, and that is information.** It
skips `object` columns unless you pass `include="all"`. If `visits` had gone
missing from this block you would know instantly that pandas was treating it as
text. Rounding with `.round(2)` rather than reformatting by hand matters for the
same reason as everywhere else this week: `.round(2)` returns a DataFrame of the
same shape that you could keep working with, whereas a string format returns
text you can only look at.

**The derived column is one vectorized division.** `df["visits"] /
df["open_hours"]` aligns the two Series on their index and divides row by row in
compiled code. The tempting alternative, `df.apply(lambda r: r["visits"] /
r["open_hours"], axis=1)`, calls a Python function once per row, is roughly two
orders of magnitude slower on a real table, and is longer to read. Reach for
`apply` only when there is genuinely no vectorized equivalent.

And the column earns its place. Elm at 109.8 visits per open hour is the busiest
branch by this measure but only the second busiest by raw visits; Juniper wins
on raw visits (6,890) partly by being open 60 hours. Normalising by exposure
before you compare is most of what separates an analysis from a leaderboard.

**Leaving the index alone is a deliberate choice, not laziness.** `RangeIndex:
12 entries, 0 to 11` in the `info()` block tells you that row labels here carry
no meaning — they are positions with a label's clothes on. That is worth
noticing now, because in Exercise 3 you will filter this kind of frame and watch
the labels stop being `0..n` while the positions carry on as before.

## Run it

Copy the worked answer on this page into `exercise-02-load-and-inspect.py` and run it:

```bash
python exercise-02-load-and-inspect.py
```

It needs only pandas and prints the eight inspection blocks in order. The `-solution` suffix keeps it from colliding with your own `exercise-02-load-and-inspect.py`.

## Common bugs to catch

- **A stray `None` after the info report.** You wrote `print(df.info())`.
  `info()` prints and returns `None`; the `print` around it renders that
  `None`. Drop the wrapper.
- **`TypeError: 'tuple' object is not callable` on the shape line.** You wrote
  `df.shape()`. `shape` is an attribute — no parentheses. Same for `dtypes`,
  `columns`, `index`, and `values`.
- **`ValueError: All arrays must be of the same length`.** One of your lists in
  `BRANCHES` has eleven or thirteen entries. Count them, or let Python count:
  `print({k: len(v) for k, v in BRANCHES.items()})`. Every value must be 12.
- **`KeyError: ('branch', 'region', 'visits_per_hour')`.** You wrote
  `df["branch", "region", "visits_per_hour"]` with one pair of brackets.
  pandas read that as a single tuple-shaped column name. Add the inner list.
- **`describe()` shows only `count`, `unique`, `top`, `freq`.** You called it
  on a string column, or the numeric columns came in as `object` because a
  value was quoted in the source dict. Check `df.dtypes` — if `visits` says
  `object`, one of your numbers is a string like `"4820"`.
- **`AttributeError: 'DataFrame' object has no attribute 'value_counts'` in
  older pandas.** `value_counts` on a whole DataFrame arrived in pandas 1.1.
  This exercise calls it on a Series — `df["region"].value_counts()` — which
  has always worked. If you hit the error, you dropped the column selection.
- **`visits_per_hour` comes out with fifteen decimal places.** You skipped
  `.round(1)`. Division produces `float64`, and floats print in full unless
  you round them.

## Under the hood

<details>
<summary>Under the hood — attribute or method, and why info() returns None</summary>

pandas draws a hard line between what a frame *is* and what it *does*. `shape`,
`dtypes`, `columns`, and `index` are **attributes** — facts the frame already
holds, so you read them with no parentheses. `head()`, `describe()`, and
`value_counts()` are **methods** — work the frame performs on request, so they
take parentheses. Add `()` to an attribute and you try to *call* the value it
already handed back: `df.shape()` raises `TypeError: 'tuple' object is not
callable`, because `df.shape` was already the tuple `(12, 5)`.

`info()` is the exception that proves the rule. It is one of a small handful of
methods written for a human at a terminal rather than for a program: it *prints*
its report as a side effect and hands back `None`. That is why the answer calls
`df.info()` bare instead of `print(df.info())` — wrapping it in `print` tacks a
stray `None` line onto the end of the report.

The `612.0+ bytes` it prints has a story too. The `+` means pandas did not
measure the strings: it counted the three integer columns honestly (12 rows ×
8 bytes) and the two string columns at a pointer each, then stopped. Pass
`df.memory_usage(deep=True)` and it follows those pointers to the real
branch-name bytes — on a million rows of repeated text, that gap is the whole
argument for the `category` dtype.

</details>

## Acceptance checklist

- [ ] Every cell runs top to bottom from a fresh kernel or a fresh
      `python` invocation, with no traceback.
- [ ] All eight banners appear, in order, with the output shown above under
      each.
- [ ] There is no stray `None` line anywhere.
- [ ] `describe()` is rounded to two decimals.
- [ ] The region counts read North 5, South 4, East 2, West 1.
- [ ] You can say out loud, without looking, how many rows and columns the
      table has and which two columns are strings.
- [ ] The file is committed to Git with a message like
      `Add Week 13 exercise 2: load and inspect`.

## Stretch

- Call `df.describe(include="all")` and read the four extra rows it adds for
  the string columns: `unique`, `top`, `freq`, and a `count`. Work out why
  most of the numeric cells in those rows are `NaN`.
- Add a second derived column, `holds_per_visit`, and round it to three
  decimals. Which branch converts visits into filled holds most effectively?
  Is it the same branch as the busiest one?
- Write the frame out with `df.to_csv("branches.csv", index=False)`, then read
  it back with `pd.read_csv("branches.csv")` and compare `dtypes` before and
  after. This is the round trip your mini-project will depend on.
- Use `df.memory_usage(deep=True)` and compare it to the `612.0+ bytes` that
  `info()` reported. The `+` in that number is pandas admitting it did not
  measure the strings; `deep=True` makes it actually look.

When your inspection output matches, move on to
[Exercise 3 — Filter and Sort](./exercise-03-filter-and-sort.md).
