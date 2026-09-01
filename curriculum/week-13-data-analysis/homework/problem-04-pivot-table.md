# Homework 4 — Pivot table from raw

> **Topic:** `pivot_table` — folding a long list of rows into a small grid you can actually read
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Intermediate
> **Target time:** 45 min
> **Why this one:** almost every reporting job you will ever be handed ends in a
> grid. Rows down one side, columns across the top, one number in each square.
> This problem builds two grids from the same raw rows, and makes you handle the
> square that has nothing in it — the case that quietly breaks most first
> attempts.

## The Brief

Imagine a shoebox with a restaurant's receipts in it. Every receipt says three
things: which day it was, whether it was lunch or dinner, and the total on the
bill. Fifteen receipts, or fifteen thousand — either way, reading them one at a
time tells you nothing.

So you draw a grid on a napkin. Days down the left. Lunch and Dinner across the
top. Then you go through the shoebox and write one number into each square.

That grid is a **pivot table**. `pivot_table` is the pandas call that builds it
for you. You tell it what goes down the side, what goes across the top, which
number to use, and how to squash many receipts into the one number that belongs
in a square.

You will build two grids from the same receipts.

1. The first holds the **average bill** in each square.
2. The second holds **how many orders** landed in each square.

Same rows, same columns, different question.

Two squares are going to be empty. This restaurant does not serve lunch at the
weekend, so Saturday-Lunch and Sunday-Lunch have no receipts at all. An empty
square is not a bug, and it is not a zero-dollar meal — it is a service that did
not happen. You will fill it with `0` on purpose, and you will be able to say
why.

The original brief points at seaborn's `tips` dataset. The shipped answer
fabricates a fifteen-row frame with the same shape instead — a `day`, a `time`,
a `total_bill`, and the same missing weekend lunches — so it runs offline, on
any machine, with the same numbers every time. If you have seaborn installed,
`sns.load_dataset("tips")` gives you the real dataset and every line below works
on it unchanged.

## Starter

Copy this into `problem-04-pivot-table.py` in your homework folder. It runs as
pasted — it just does not do much yet.

```python
"""problem-04-pivot-table.py — two pivot tables over a restaurant-tips frame.

Rows are days, columns are Lunch and Dinner. The first grid holds the mean
total bill in each square; the second holds how many orders landed there.
"""

from __future__ import annotations

import pandas as pd

DAYS = ["Thur", "Fri", "Sat", "Sun"]
TIMES = ["Lunch", "Dinner"]

TIPS: dict[str, list] = {
    "day": [
        "Thur", "Thur", "Thur", "Fri", "Fri", "Sat", "Sat", "Sat",
        "Sun", "Sun", "Sun", "Thur", "Fri", "Sat", "Sun",
    ],
    "time": [
        "Lunch", "Lunch", "Dinner", "Lunch", "Dinner", "Dinner", "Dinner",
        "Dinner", "Dinner", "Dinner", "Dinner", "Lunch", "Lunch", "Dinner",
        "Dinner",
    ],
    "total_bill": [
        12.50, 15.00, 20.00, 11.00, 22.00, 25.00, 30.00, 18.00,
        28.00, 24.00, 26.00, 14.00, 13.50, 21.00, 27.00,
    ],
}


def mean_bill_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean total_bill for every (day, time) cell; empty cells become 0."""
    # TODO: return df.pivot_table(...) with day down the side, time across the
    #       top, total_bill as the value, and "mean" as the squasher.
    #       Ask for fill_value=0 and observed=False, then round to 2 decimals.
    return pd.DataFrame()


def order_count_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Number of orders in every (day, time) cell, as whole numbers."""
    # TODO: the same call, but squash with "size" instead of "mean",
    #       then convert the whole grid to int64.
    return pd.DataFrame()


if __name__ == "__main__":
    tips = pd.DataFrame(TIPS)

    # TODO: turn "day" and "time" into ordered categories, using DAYS and
    #       TIMES as the order. Without this the grid comes out alphabetical.

    # TODO: print the row count and both category orders on one line.
    print(f"{len(tips)} rows")

    # TODO: print the heading "Mean total_bill by day and time", then the
    #       first grid with .to_string().

    # TODO: print the heading "Order count by day and time", then the second
    #       grid the same way.

    # TODO: print the count grid's dtypes and its grand total, as a self-check.
```

## Requirements

1. Build the frame from `TIPS`, then make `day` and `time` **ordered
   categories** using `DAYS` and `TIMES` as the order.
2. Print one header line first:
   `15 rows, day=['Thur', 'Fri', 'Sat', 'Sun'], time=['Lunch', 'Dinner']`,
   followed by a blank line.
3. Build the mean grid: rows `day`, columns `time`, values `total_bill`,
   squashed with `mean`, empty squares filled with `0`, rounded to 2 decimals.
4. Build the count grid: same rows, same columns, but the number in each square
   is how many orders landed there, as whole numbers (`int64`).
5. Print each grid under its own heading — `Mean total_bill by day and time` and
   `Order count by day and time` — using `.to_string()`.
6. Finish with a self-check line naming the count grid's dtypes and its grand
   total: `count pivot dtypes: [dtype('int64')], grand total = 15`.
7. Both grids are built by **typed functions** that take a DataFrame and return
   a DataFrame. The file has a docstring at the top saying what it does.
8. The whole thing runs end to end with `python problem-04-pivot-table.py` and
   reads no files, so it works on any machine with pandas installed.

## Constraints

- **Make `day` and `time` ordered `Categorical` columns before pivoting.**
  Otherwise pandas sorts the row labels the only way it can — alphabetically —
  and you get Fri, Sat, Sun, Thur. That is not a week. It is not wrong in any
  way pandas could detect, either, which is exactly why it will slip past you in
  a report. An ordered category tells pandas the order you meant.
- **Use `fill_value=0`, not a `.fillna(0)` bolted on afterwards.** `fill_value`
  only touches squares that had no rows behind them at all. A later `.fillna(0)`
  would also overwrite genuine missing values *inside* the data — a receipt with
  a blank total would silently become a zero-dollar meal, and your average would
  be wrong with no warning. Fill the holes you made, not the holes you were
  given.
- **Pass `observed=False` explicitly.** With category columns, pandas is in the
  middle of changing what it does by default: today it keeps every category,
  tomorrow it will keep only the ones it actually saw. Saying which one you want
  means the script prints the same grid after a pandas upgrade, and it silences
  the deprecation warning you would otherwise get.
- **Count with `aggfunc="size"`, not `aggfunc="count"`.** `size` counts *rows*.
  `count` counts non-missing values in the `total_bill` column. They agree right
  up until one receipt has a blank total, and then they disagree by one and you
  have no idea which number is on the report. "How many orders" means rows.
- **`.astype("int64")` on the count grid.** Any grid that had an empty square in
  it comes back as floating point, so you get `3.0` orders. Three orders is a
  whole thing. `3.0` reads as a measurement, which it is not.
- **`.round(2)` on the money grid.** A mean of `13.833333333` is false
  precision — it claims the restaurant can charge a third of a cent. Dollars
  have two decimals; say so.
- **Print with `.to_string()`, not bare `print(df)`.** A bare print lets pandas
  decide the grid is too wide or too tall and replace the middle with `...`.
  That is fine while you are poking around and quietly disastrous in output
  somebody else reads. `.to_string()` prints all of it, always.
- **No file reading and no paths outside your homework folder.** The data is
  inline. A homework script that needs a CSV you happen to have on your desktop
  cannot be run by the person reviewing it.

## Expected output

Real captured run of the shipped answer,
[`problem-04-pivot-table-solution.py`](./problem-04-pivot-table-solution.py):

```text
$ python problem-04-pivot-table-solution.py
15 rows, day=['Thur', 'Fri', 'Sat', 'Sun'], time=['Lunch', 'Dinner']

Mean total_bill by day and time
time  Lunch  Dinner
day                
Thur  13.83   20.00
Fri   12.25   22.00
Sat    0.00   23.50
Sun    0.00   26.25

Order count by day and time
time  Lunch  Dinner
day                
Thur      3       1
Fri       2       1
Sat       0       4
Sun       0       4

count pivot dtypes: [dtype('int64')], grand total = 15
```

Read the two grids against each other. Thursday and Friday serve both meals, so
all four of their squares carry a number. Saturday and Sunday show `0.00` under
Lunch in the first grid and `0` under Lunch in the second — and the second grid
is the one that tells you which kind of zero it is. Zero orders means no service,
not a free meal. That pairing is the reason you print both.

The dinner averages climb across the week — 20.00 on Thursday, 26.25 on Sunday —
while lunch stays near 13. Weekend dinner is the money. Fifteen receipts total,
which the grand total confirms: if that number is not 15, a square went missing.

## Steps

1. Create `problem-04-pivot-table.py` and paste the starter. Run it. You should
   see `15 rows` and nothing else. Confirming the plumbing before you build
   anything saves you from debugging two problems at once.
2. In `mean_bill_pivot`, return the pivot with just `index`, `columns`, `values`
   and `aggfunc="mean"` — no fill, no rounding, no categories yet. Print it.
   Look at the row order and the `NaN` cells. That is the "before" picture.
3. Add the two `pd.Categorical` lines in the main block. Rerun. The rows jump
   into weekday order. Nothing else changed.
4. Add `fill_value=0` and `observed=False`. The `NaN`s become `0.0`.
5. Add `.round(2)`. Compare against the expected output above, square by square.
6. Fill in `order_count_pivot` with `aggfunc="size"`, the same `fill_value` and
   `observed`, and `.astype("int64")`. Print it under its heading.
7. Add the header line and the final dtypes-and-grand-total line. The grand
   total must be 15.
8. Change one `"Dinner"` to `"Lunch"` in `TIPS` and rerun. Watch both grids move
   together. Change it back. A report you cannot perturb on purpose is a report
   you do not understand.

## The Solution

```python
"""hw-04-pivot.py — two pivot tables over a small restaurant-tips frame.

The homework uses seaborn's ``tips`` dataset. So it runs offline and identically
everywhere, this shipped answer builds an inline frame with the same shape — a
``day`` category, a ``time`` category, and a ``total_bill`` — and, like the real
data, no weekend *lunch* service, so the empty-cell handling is exercised.
"""

from __future__ import annotations

import pandas as pd

DAYS = ["Thur", "Fri", "Sat", "Sun"]
TIMES = ["Lunch", "Dinner"]

TIPS: dict[str, list] = {
    "day": [
        "Thur", "Thur", "Thur", "Fri", "Fri", "Sat", "Sat", "Sat",
        "Sun", "Sun", "Sun", "Thur", "Fri", "Sat", "Sun",
    ],
    "time": [
        "Lunch", "Lunch", "Dinner", "Lunch", "Dinner", "Dinner", "Dinner",
        "Dinner", "Dinner", "Dinner", "Dinner", "Lunch", "Lunch", "Dinner",
        "Dinner",
    ],
    "total_bill": [
        12.50, 15.00, 20.00, 11.00, 22.00, 25.00, 30.00, 18.00,
        28.00, 24.00, 26.00, 14.00, 13.50, 21.00, 27.00,
    ],
}


def mean_bill_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean total_bill for every (day, time) cell; empty cells become 0."""
    return df.pivot_table(
        index="day",
        columns="time",
        values="total_bill",
        aggfunc="mean",
        fill_value=0,
        observed=False,
    ).round(2)


def order_count_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Number of orders in every (day, time) cell, as integers."""
    return df.pivot_table(
        index="day",
        columns="time",
        values="total_bill",
        aggfunc="size",
        fill_value=0,
        observed=False,
    ).astype("int64")


if __name__ == "__main__":
    tips = pd.DataFrame(TIPS)
    tips["day"] = pd.Categorical(tips["day"], categories=DAYS, ordered=True)
    tips["time"] = pd.Categorical(tips["time"], categories=TIMES, ordered=True)

    print(f"{len(tips)} rows, day={list(tips['day'].cat.categories)}, "
          f"time={list(tips['time'].cat.categories)}\n")

    print("Mean total_bill by day and time")
    print(mean_bill_pivot(tips).to_string())

    print("\nOrder count by day and time")
    print(order_count_pivot(tips).to_string())

    counts = order_count_pivot(tips)
    print(f"\ncount pivot dtypes: {counts.dtypes.unique().tolist()}, "
          f"grand total = {counts.to_numpy().sum()}")
```

**`pivot_table` is a `groupby` wearing a grid costume.** Underneath, pandas
groups the rows by every `(day, time)` pair it can see, runs `mean` over the
`total_bill` in each group, and then lays those group answers out as a
rectangle — group keys down the side, group keys across the top. That is the
whole trick. If you can write the `groupby`, you can write the pivot; the pivot
just shows it to you in a shape a human reads faster.

**Ordered categories are why the rows say Thur, Fri, Sat, Sun.** Left alone,
pandas sorts labels the only way it can — alphabetically — and hands you Fri,
Sat, Sun, Thur. Nothing about that is detectably wrong, which is precisely how
it survives all the way onto a slide. `pd.Categorical(values, categories=DAYS,
ordered=True)` says: these are the only four allowed values, and this is the
order I mean. From that point on every sort, every pivot, every group respects
it. `observed=False` is the companion promise — keep every category, even one
nothing landed in — and passing it explicitly means the grid does not change
shape the day pandas ships its new default.

**`fill_value=0` fills the holes the pivot made, and nothing else.** There were
never any Saturday-Lunch receipts, so that square has no rows behind it and
pandas has nothing to put there. `fill_value` writes the `0`. Doing it as a
later `.fillna(0)` would look identical here and be a slow-acting bug: it would
also overwrite a genuinely missing `total_bill` inside a real receipt, turning
"we do not know what this bill was" into "this bill was zero dollars", and
dragging your average down with no message on screen. Fill what you emptied.

**`size` versus `count` is the difference between rows and values.** `size` asks
how many rows fell in this square. `count` asks how many non-missing
`total_bill` values fell in this square. On clean data they are the same number,
so nobody notices which one they typed — until one bill is blank, the two
disagree, and the report is off by one with no way to tell which figure was
printed. "How many orders" is a question about rows. Use `size`.

**`.astype("int64")` and `.round(2)` are both about not lying with digits.** A
grid that contained an empty square comes back as floating point, so the counts
print as `3.0` — which reads like a measurement that happened to land on three,
not a tally of three whole orders. And a raw mean of `13.833333333` claims the
kitchen can charge a third of a cent. Round money to money; cast counts to
counts.

**`.to_string()` prints the whole grid, every time.** A bare `print(df)` lets
pandas decide the frame is too wide or too tall and quietly swap the middle for
`...`. That is convenient at the REPL and indefensible in output somebody else
is going to read and act on. Four rows will never trip the limit; the habit is
what you are building, and the habit is what saves you at four hundred.

**The last line is a self-check, not decoration.** `counts.to_numpy().sum()`
must equal the number of receipts you started with — 15. Every row has to land
in exactly one square, so the squares have to add back up to the shoebox. If
that number comes out low, a row fell through: a typo in a day name, a category
list that does not cover the data, or a filter you forgot you wrote. One cheap
line that catches a whole family of silent mistakes.

**About the shipped file.** Its docstring still carries the name
`hw-04-pivot.py` from an earlier draft of this assignment. Your own file is
`problem-04-pivot-table.py`; the `-solution` suffix on the download exists so it
cannot collide with it.

## Download and run

Download
[problem-04-pivot-table-solution.py](./problem-04-pivot-table-solution.py)
and run it:

```bash
pip install pandas
python problem-04-pivot-table-solution.py
```

It needs pandas and nothing else. The data is inline, so it reads no files,
writes no files, and prints the same numbers on every machine.

## Common bugs to catch

- **The rows come out `Fri, Sat, Sun, Thur`.** You skipped the `pd.Categorical`
  lines, so pandas fell back on alphabetical order. Add them before you pivot.
- **`KeyError: 'dayy'`.** A column name in `index=`, `columns=` or `values=`
  does not exist. pandas quotes the name it could not find — check it against
  `df.columns`.
- **`FutureWarning: The default value of observed=False is deprecated and will
  change to observed=True in a future version of pandas.`** You pivoted category
  columns without saying which behaviour you want. Pass `observed=False`.
- **`pandas.errors.IntCastingNaNError: Cannot convert non-finite values (NA or
  inf) to integer`.** You called `.astype("int64")` on a grid that still has
  empty squares in it. `fill_value=0` has to come first — you cannot cast
  "nothing" to a whole number.
- **Whole rows or columns vanish from the mean grid.** `pivot_table` drops rows
  and columns that came out entirely empty. If a day genuinely had no service at
  all, it disappears rather than showing zeros. Set `fill_value=0` and keep the
  categories, or pass `dropna=False`.
- **The counts print as `3.0` and `4.0`.** You forgot `.astype("int64")`. The
  empty square forced the whole grid to floating point.
- **The averages print as `13.833333333333334`.** No `.round(2)`. Round money
  once, at the end, for display — not in the middle of a calculation.
- **The middle of the grid is replaced with `...`.** You used a bare
  `print(df)` on something wide. Switch to `.to_string()`.
- **The grand total is not 15.** Rows are being lost. Most often a value in
  `day` or `time` is not in your `categories=` list — a stray `"Thurs"` for
  `"Thur"` becomes `NaN` the moment you build the `Categorical`, and a `NaN` key
  lands in no square at all. Check with
  `tips["day"].isna().sum()` right after the conversion.
- **Every square in the count grid reads `1`.** You passed `aggfunc="size"` a
  column that is unique per row, or you pivoted a frame you had already
  aggregated once. Pivot the raw rows.

## Under the hood

<details>
<summary>Under the hood — what pivot_table actually does, and when to reach for crosstab or unstack instead</summary>

`pivot_table` is a thin, friendly wrapper. Underneath it does
`df.groupby([index_keys, column_keys]).agg(aggfunc)` and then calls `.unstack()`
to swing the second grouping key from the row index out into the columns. That
is the entire operation. Knowing this pays off two ways: anything you can do in
a `groupby` you can do in a pivot (including `aggfunc=["mean", "median"]`, which
gives you a second level of column headings), and when a pivot behaves oddly,
you can reproduce it as a `groupby` and see the long form pandas was working
with.

Four closely related calls are worth telling apart:

| Call | What it is for |
|------|----------------|
| `df.pivot_table(...)` | many rows per square, so it needs an `aggfunc` |
| `df.pivot(...)` | exactly one row per square already; raises if there are two |
| `pd.crosstab(a, b)` | counting pairs; a pivot table with `aggfunc="size"` and a nicer signature |
| `series.unstack()` | you already have a grouped Series and just want it wide |

`df.pivot` is the strict one: it does not aggregate at all, and it raises
`ValueError: Index contains duplicate entries, cannot reshape` if two rows want
the same square. That strictness is useful. If you believe your data has one row
per `(day, time)` and you are wrong, `pivot` tells you and `pivot_table` quietly
averages the duplicates away.

`margins=True` adds a totals row and a totals column, labelled `All`. Be careful
reading them: the `All` cell for a mean is the mean of *all the underlying
rows*, not the mean of the row of means. Those differ whenever the squares hold
different numbers of receipts, which is almost always. That is not a bug; a
weighted average is the right answer. It is just not the number people expect
when they add up a row and divide by four.

</details>

<details>
<summary>Under the hood — what an ordered Categorical costs and buys</summary>

A `Categorical` column does not store the string `"Thur"` fifteen times. It
stores the four distinct strings once, in a small array called the categories,
and then stores fifteen tiny integers pointing into it. On a column of a million
day names with four distinct values, that is roughly a 4-byte integer per row
instead of a full Python string object per row — often a ten-to-twentyfold drop
in memory, and faster grouping, because comparing two small integers beats
comparing two strings.

`ordered=True` adds one more thing: a defined `<`. Once pandas knows
`Thur < Fri < Sat < Sun`, sorting, `min`, `max`, `groupby` ordering and pivot row
order all fall into place for free, and `df[df["day"] > "Fri"]` means "the
weekend" instead of raising or comparing letters.

The sharp edge is what happens to a value that is not in the category list.
`pd.Categorical(["Thurs"], categories=["Thur", "Fri"])` does not raise. It
produces `NaN`, silently. That is the single most common way rows go missing
from a pivot, and it is why the last line of this answer adds the squares back
up and checks the total against the number of receipts. After any conversion to
`Categorical`, `df["day"].isna().sum()` is worth one look.

`observed` controls whether pandas keeps categories nothing landed in. Today's
default is `False` — keep them all, which is what makes an empty
Saturday-Lunch square exist at all so that `fill_value` has somewhere to write a
zero. The default is being changed to `True` in a future release, which would
make that square silently not exist. Passing it explicitly is how the script
survives the upgrade.

</details>

## Acceptance checklist

- [ ] `python problem-04-pivot-table.py` runs with no traceback and no warnings.
- [ ] The printed output matches the expected block, line for line.
- [ ] Rows read Thur, Fri, Sat, Sun. Columns read Lunch, Dinner.
- [ ] The mean grid shows two decimals everywhere and `0.00` at weekend lunch.
- [ ] The count grid shows whole numbers, and the grand total is 15.
- [ ] Both grids are returned by typed functions, and the file has a
      top-of-file docstring.
- [ ] The script reads no files and hard-codes no path outside your homework
      folder.
- [ ] The file is committed to Git with a message like
      `Add Week 13 homework 4: pivot tables`.

## Stretch

- Add `margins=True` to both pivots for a totals row and column. Then work out
  by hand why the `All` cell of the mean grid is not the average of the four
  numbers above it, and write the reason in a comment.
- Rebuild the count grid with `pd.crosstab(tips["day"], tips["time"])` and
  compare the code to the `pivot_table` version. Same grid, shorter call, less
  control.
- Pass a list to `aggfunc` — `aggfunc=["mean", "median", "max"]` — and look at
  what happens to the column headings. That is a MultiIndex; `.columns.levels`
  will show you its two layers.
- Add a third dimension: `index=["day", "time"]`, `columns="size"`. The result
  is a grid with two levels of row labels. Print it and decide whether it is
  easier or harder to read than two separate grids.
- Install seaborn, swap the inline frame for `sns.load_dataset("tips")`, and run
  the same two functions unchanged. The row order is already categorical in the
  real dataset — check whether it matches yours, and if not, why not.
- Write both grids to one Excel workbook on separate sheets with
  `pd.ExcelWriter`. That is the format the person who asked you for this report
  actually wanted.
