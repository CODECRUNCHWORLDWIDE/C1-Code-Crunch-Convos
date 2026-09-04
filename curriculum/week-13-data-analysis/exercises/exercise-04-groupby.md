# Exercise 4 — Groupby

> **Topic:** `groupby` totals and averages, and why the two disagree
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Medium
> **Target time:** 25 minutes
> **Why this one:** split-apply-combine is the single most useful pattern in
> data analysis, and it is also the fastest way to publish a misleading
> number. Total and average rank these four categories in different orders. If
> you cannot explain why, you will eventually hand a manager the wrong chart
> with total confidence.

## The Brief

A neighborhood hardware store closes out its Saturday sales: twelve line
items across four departments. The owner wants a one-page summary — revenue
per department, the average line item, how many units moved, and each
department's share of the day.

There is a trap built into the data, and it is the trap that makes this
exercise worth doing. Fasteners has only two line items on the sheet; Paint
has four. Rank the departments by total revenue and Paint wins comfortably.
Rank them by *average* revenue per line item and Fasteners jumps to the top,
because two big-ticket rows are not diluted by two small ones. Neither number
is wrong. They answer different questions, and your job is to know which
question you were asked.

## Starter

Copy this into `exercise-04-groupby.py` in your practice repo.

```python
"""exercise-04-groupby.py — a Saturday sales summary by department.

Computes revenue per line item, then aggregates by category with
totals, averages, unit counts, and share of the day's revenue.
"""

import pandas as pd

SALES: dict[str, list] = {
    "item": [
        "Interior latex gallon", "Painter's tape", "Roller kit", "Primer quart",
        "Claw hammer", "Cordless drill", "Tape measure",
        "Potting soil", "Pruning shears", "Garden hose 50ft",
        "Deck screws box", "Wall anchors",
    ],
    "category": [
        "Paint", "Paint", "Paint", "Paint",
        "Tools", "Tools", "Tools",
        "Garden", "Garden", "Garden",
        "Fasteners", "Fasteners",
    ],
    "units":      [14, 40, 22, 19, 9, 5, 18, 30, 12, 7, 25, 33],
    "unit_price": [32.50, 4.25, 11.75, 13.25, 18.99, 89.00, 12.50,
                   8.99, 21.50, 34.00, 15.25, 6.40],
}


def main() -> None:
    """Print the line items and four views of the aggregated day."""
    df = pd.DataFrame(SALES)

    # TODO: add a `revenue` column: units * unit_price, rounded to 2 places.
    print("--- rows ---")
    print(df)

    # TODO: print the simplest possible groupby —
    #       df.groupby("category")["revenue"].sum()
    #       under the "--- revenue per category ---" banner.

    # TODO: build `summary` with named aggregations:
    #         total_revenue = sum of revenue
    #         avg_revenue   = mean of revenue
    #         units_sold    = sum of units
    #         line_items    = size of the item column
    #       Round the whole thing to 2 places and print it.

    # TODO: print `ranked` — summary sorted by total_revenue, descending.

    # TODO: print summary sorted by avg_revenue, descending. Compare.

    # TODO: print the grand total with a thousands separator: ${...:,.2f}

    # TODO: print each category's share of the grand total as a percentage,
    #       rounded to 1 decimal, in the ranked-by-total order.

    # TODO: print the single biggest line item in each category using
    #       df.loc[df.groupby("category")["revenue"].idxmax(), [...]]


if __name__ == "__main__":
    main()
```

## Requirements

1. Add a `revenue` column equal to `units * unit_price`, rounded to two
   decimals.
2. Print the twelve rows under `--- rows ---`.
3. Print `df.groupby("category")["revenue"].sum()` under
   `--- revenue per category ---`.
4. Build `summary` with `.agg()` and **named aggregations** producing exactly
   four columns, in this order: `total_revenue`, `avg_revenue`, `units_sold`,
   `line_items`. Round to two decimals and print under
   `--- named aggregations ---`.
5. Print the summary sorted by `total_revenue` descending under
   `--- ranked by total ---`, and by `avg_revenue` descending under
   `--- ranked by average ---`.
6. Print `Grand total: $3,334.31` with a comma separator and two decimals.
7. Print each category's percentage share, rounded to one decimal, in
   total-revenue order, under `--- share of total ---`.
8. Print the highest-revenue line item per category under
   `--- best line item per category ---`, using `idxmax`.

## Constraints

- **Round `revenue` at creation, not at print time.** `30 * 8.99` is
  `269.70000000000002` in binary floating point. If you leave it unrounded,
  every downstream sum inherits the noise and your grand total may print
  `$3,334.31` on one machine and something a cent off on another. Money
  columns get rounded once, as early as possible, and then everything
  downstream agrees.
- **Use named aggregations — `total_revenue=("revenue", "sum")` — not
  `.agg(["sum", "mean"])`.** The list form produces a MultiIndex on the
  columns, which you then have to flatten before you can sort or plot. The
  named form gives you flat, self-documenting column names in one step. It is
  the modern recommendation in the pandas docs and in Lecture 3.
- **Use `size` for the line-item count, not `count`.** They agree here because
  nothing is missing, but they mean different things: `size` counts rows,
  `count` counts non-null values. Picking the one that means what you said is
  how you avoid a silent undercount the day a value goes missing.
- **Compute `share` from the ranked frame, so the percentages come out in the
  same order as the ranking.** A share column that reads in a different order
  from the table above it is a chart waiting to be misread.
- **Use `idxmax` for the best line item, not `max`.** `max` gives you the
  largest revenue *number*; you need the *row* — which item, in which
  category. `idxmax` returns the index label of that row, and `df.loc[...]`
  turns labels into rows. This is the same position-versus-label distinction
  you met in Exercise 1 with `argmax`.
- **Do not reach for a loop over categories.** You could write
  `for cat in df["category"].unique():` and filter inside it. That is four
  times the code, it is slower, and it will not survive the day someone adds
  a fifth department. `groupby` discovers the groups for you.

## Expected output

```text
$ python exercise-04-groupby.py
--- rows ---
                     item   category  units  unit_price  revenue
0   Interior latex gallon      Paint     14       32.50   455.00
1          Painter's tape      Paint     40        4.25   170.00
2              Roller kit      Paint     22       11.75   258.50
3            Primer quart      Paint     19       13.25   251.75
4             Claw hammer      Tools      9       18.99   170.91
5          Cordless drill      Tools      5       89.00   445.00
6            Tape measure      Tools     18       12.50   225.00
7            Potting soil     Garden     30        8.99   269.70
8          Pruning shears     Garden     12       21.50   258.00
9        Garden hose 50ft     Garden      7       34.00   238.00
10        Deck screws box  Fasteners     25       15.25   381.25
11           Wall anchors  Fasteners     33        6.40   211.20
--- revenue per category ---
category
Fasteners     592.45
Garden        765.70
Paint        1135.25
Tools         840.91
Name: revenue, dtype: float64
--- named aggregations ---
           total_revenue  avg_revenue  units_sold  line_items
category                                                     
Fasteners         592.45       296.23          58           2
Garden            765.70       255.23          49           3
Paint            1135.25       283.81          95           4
Tools             840.91       280.30          32           3
--- ranked by total ---
           total_revenue  avg_revenue  units_sold  line_items
category                                                     
Paint            1135.25       283.81          95           4
Tools             840.91       280.30          32           3
Garden            765.70       255.23          49           3
Fasteners         592.45       296.23          58           2
--- ranked by average ---
           total_revenue  avg_revenue  units_sold  line_items
category                                                     
Fasteners         592.45       296.23          58           2
Paint            1135.25       283.81          95           4
Tools             840.91       280.30          32           3
Garden            765.70       255.23          49           3
Grand total: $3,334.31
--- share of total ---
category
Paint        34.0
Tools        25.2
Garden       23.0
Fasteners    17.8
Name: total_revenue, dtype: float64
--- best line item per category ---
     category                   item  revenue
10  Fasteners        Deck screws box   381.25
7      Garden           Potting soil   269.70
0       Paint  Interior latex gallon   455.00
5       Tools         Cordless drill   445.00
```

Now look at the two rankings side by side. By total, Fasteners is last with
$592.45. By average, Fasteners is *first* at $296.23 per line item. Both
numbers come from the same two rows; the only difference is whether you
divided by the number of line items. Paint's four rows include a $170 tape
line that pulls its average down while adding to its total.

Notice too that the first, unsorted `groupby` output is in alphabetical order
— Fasteners, Garden, Paint, Tools. `groupby` sorts its keys by default. That is
convenient for lookups and useless for ranking, which is why you sort
explicitly afterwards. Pass `sort=False` if you ever need the original order
of first appearance instead.

## Steps

1. Create the file, paste the starter, and add only the `revenue` column.
   Run it and check that row 7 shows `269.70`, not `269.700000`.
2. Add the one-line groupby. Confirm the four totals.
3. Add the named aggregation block. Read the printed frame carefully: the
   category names are now the *index*, not a column, which is why they sit
   below a blank header row.
4. Add both sorted views and put them next to each other on screen.
5. Add the grand total and the share column. The shares should add to roughly
   100 — 34.0 + 25.2 + 23.0 + 17.8 = 100.0 here.
6. Add the `idxmax` block last; it is the trickiest line on the page. Print
   `df.groupby("category")["revenue"].idxmax()` on its own first, and see that
   it gives you four index labels: 10, 7, 0, 5.
7. Add a fifth category with one row of your own invention and rerun. Nothing
   in your code should need to change.

## The Solution

```python
"""exercise-04-groupby.py — a Saturday sales summary by department.

Computes revenue per line item, then aggregates by category with
totals, averages, unit counts, and share of the day's revenue.
"""

import pandas as pd

SALES: dict[str, list] = {
    "item": [
        "Interior latex gallon", "Painter's tape", "Roller kit", "Primer quart",
        "Claw hammer", "Cordless drill", "Tape measure",
        "Potting soil", "Pruning shears", "Garden hose 50ft",
        "Deck screws box", "Wall anchors",
    ],
    "category": [
        "Paint", "Paint", "Paint", "Paint",
        "Tools", "Tools", "Tools",
        "Garden", "Garden", "Garden",
        "Fasteners", "Fasteners",
    ],
    "units":      [14, 40, 22, 19, 9, 5, 18, 30, 12, 7, 25, 33],
    "unit_price": [32.50, 4.25, 11.75, 13.25, 18.99, 89.00, 12.50,
                   8.99, 21.50, 34.00, 15.25, 6.40],
}


def main() -> None:
    """Print the line items and four views of the aggregated day."""
    df = pd.DataFrame(SALES)

    df["revenue"] = (df["units"] * df["unit_price"]).round(2)
    print("--- rows ---")
    print(df)

    print("--- revenue per category ---")
    print(df.groupby("category")["revenue"].sum())

    summary = df.groupby("category").agg(
        total_revenue=("revenue", "sum"),
        avg_revenue=("revenue", "mean"),
        units_sold=("units", "sum"),
        line_items=("item", "size"),
    ).round(2)
    print("--- named aggregations ---")
    print(summary)

    ranked = summary.sort_values("total_revenue", ascending=False)
    print("--- ranked by total ---")
    print(ranked)

    print("--- ranked by average ---")
    print(summary.sort_values("avg_revenue", ascending=False))

    grand_total = summary["total_revenue"].sum()
    print(f"Grand total: ${grand_total:,.2f}")

    share = (ranked["total_revenue"] / grand_total * 100).round(1)
    print("--- share of total ---")
    print(share)

    best = df.loc[
        df.groupby("category")["revenue"].idxmax(),
        ["category", "item", "revenue"],
    ]
    print("--- best line item per category ---")
    print(best)


if __name__ == "__main__":
    main()
```

**The two rankings are both correct and they answer different questions.**
Fasteners is last by total revenue at $592.45 and first by average at $296.23
per line item. Nothing is inconsistent: `avg_revenue` is `total_revenue`
divided by `line_items`, and Fasteners has only two rows to divide by. Paint has
four rows, and one of them is $170 of painter's tape that adds to the total
while pulling the average down. Ask "which department made the store the most
money on Saturday" and the answer is Paint. Ask "which department's typical sale
is biggest" and the answer is Fasteners. Ask "which department is best" and you
have not asked a question yet.

The `line_items` column is in the summary precisely so that this is visible on
the page rather than being something a reader has to know. An average without
its denominator is a number you cannot audit.

**Named aggregations give you flat column names in one step.**
`total_revenue=("revenue", "sum")` reads as "make a column called
`total_revenue` by taking `sum` of `revenue`", and it produces exactly that. The
older `.agg(["sum", "mean"])` form returns a two-level column index —
`revenue/sum`, `revenue/mean` — which you must flatten before you can
`sort_values("total_revenue")` or hand the frame to a plotting call. The named
form also lets each output column draw on a different input column, which is how
`units_sold` (from `units`) and `line_items` (from `item`) sit in the same call
as the two revenue columns.

**`size` and `count` agree here and mean different things.** `size` counts rows
in the group; `count` counts non-null values in the named column. With nothing
missing they both give 2, 3, 4, 3. The day a line item arrives with a blank
description, `size` still says how many sales there were and `count` starts
quietly undercounting. Pick the one that means what your column name claims —
`line_items` is a count of rows, so it is `size`.

**`idxmax` returns a label, and `.loc` turns labels into rows.**
`df.groupby("category")["revenue"].idxmax()` gives you four index labels:

```text
category
Fasteners    10
Garden        7
Paint         0
Tools         5
Name: revenue, dtype: int64
```

`max` would have given you the four revenue *numbers*, which cannot tell you
which item they came from. This is the same distinction as `np.argmax` in
Exercise 1 — position or label versus value — and it is the reason the final
block still shows the original row labels 10, 7, 0, 5 rather than a fresh 0–3.
Those labels are the receipt: row 10 of the source data is where $381.25 came
from.

**Rounding `revenue` at creation keeps the money column honest.** Two of the
twelve products land on a binary float that is not exactly the decimal you
typed: `33 * 6.40` is `211.20000000000002` and `9 * 18.99` is fine but
`30 * 8.99` is exactly `269.7`, so the noise is real but sparser than you might
expect. (The exercise page names `30 * 8.99` as the offender; on this build it is
`33 * 6.40`.) Rounding once at creation means every downstream figure inherits
clean cents. It also shows up in the grand total: `df["revenue"].sum()` over the
twelve rows in source order is `3334.3099999999995`, while
`summary["total_revenue"].sum()` over the four already-summed categories is
exactly `3334.31`. Both print `$3,334.31` under `:,.2f`, which is the point —
round the money once, format at the edge, and stop worrying about which addition
order you got.

**`groupby` sorts its keys, so you sort again for ranking.** The first, plain
groupby prints Fasteners, Garden, Paint, Tools — alphabetical, not by size.
That default is convenient for looking a category up and useless for ranking,
which is why `ranked` exists. `sort=False` gives you order of first appearance
instead, and on a large frame it is measurably faster because it skips the sort
entirely.

**The share column is computed from `ranked`, not from `summary`.** Dividing
`ranked["total_revenue"]` by the grand total means the percentages come out in
the same order as the table above them: 34.0, 25.2, 23.0, 17.8. They sum to
100.0 here; with four shares rounded to one decimal, 99.9 or 100.1 would also be
correct and nothing needs fixing.

## Run it

Copy the worked answer on this page into `exercise-04-groupby.py` and run it:

```bash
python exercise-04-groupby.py
```

It needs only pandas and prints the line items and the four aggregated views. The `-solution` suffix keeps it from colliding with your own `exercise-04-groupby.py`.

## Common bugs to catch

- **`KeyError: 'revenue'` inside the `agg` call.** You put the aggregation
  before the line that creates the `revenue` column. `groupby` can only
  aggregate columns that already exist.
- **A two-level column header like `revenue sum | revenue mean`.** You used
  `.agg(["sum", "mean"])`. That is a MultiIndex, and `summary["total_revenue"]`
  will raise on it. Switch to named aggregations.
- **`SpecificationError: nested renamer is not supported`.** You wrote the old
  dict-of-dicts form, `.agg({"revenue": {"total": "sum"}})`. pandas removed
  that years ago. The replacement is the named-aggregation keyword form.
- **`TypeError: agg function failed [how->mean,dtype->object]`.** One of your
  numeric columns is holding strings — usually because a value in the starter
  dict got quoted. Check `df.dtypes`; `units` and `unit_price` must be numeric.
- **The grand total prints as `$3334.31` with no comma.** Your format spec is
  `:.2f` instead of `:,.2f`. The comma goes before the dot.
- **Share percentages that add to 1.0 instead of 100.** You divided but forgot
  to multiply by 100. If they add to something like 99.9 or 100.1, that is
  just rounding each share to one decimal, and it is fine.
- **`FutureWarning: The default of observed=False is deprecated`.** You
  converted `category` to the pandas `category` dtype somewhere. Pass
  `observed=True` to `groupby` to silence it and to stop pandas from emitting
  rows for combinations that never occurred.
- **`ValueError: Cannot index with multidimensional key` on the `idxmax`
  line.** You passed the whole grouped object rather than one column. The
  order matters: `df.groupby("category")["revenue"].idxmax()`, column
  selection before `idxmax`.

## Under the hood

<details>
<summary>Under the hood — idxmax returns a label, and transform keeps every row</summary>

`df.groupby("category")["revenue"].idxmax()` does not give you the four biggest
revenue *numbers* — `max` does that. It gives you the four index *labels* where
those maxima sit: `10, 7, 0, 5`. A label is a key, so feeding it to
`df.loc[...]` pulls the whole winning row for each category, receipt and all.
This is the same position-or-label-versus-value distinction as `np.argmax` back
in Exercise 1; miss the `["revenue"]` selection and `idxmax` runs on every
numeric column, returns a *frame* of labels, and `.loc` shreds it into a wall of
character tuples.

`agg` collapses the twelve rows to four — one per group. Its quiet sibling
`transform` does the opposite: it computes the same group answer but writes it
back into *every* member row, so the frame keeps its twelve rows.

```python
df["category_total"] = df.groupby("category")["revenue"].transform("sum")
df["share_of_category"] = (df["revenue"] / df["category_total"] * 100).round(1)
```

That is how you compute "this row as a fraction of its group" without a merge —
and it is the one groupby move that does not shrink the frame.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and no warnings.
- [ ] The `revenue` column shows exactly two decimals on every row.
- [ ] `summary` has exactly four columns with the names the brief specifies.
- [ ] Paint leads by total and Fasteners leads by average.
- [ ] `Grand total: $3,334.31` prints with the comma.
- [ ] You can explain in one sentence why the two rankings differ.
- [ ] The file is committed to Git with a message like
      `Add Week 13 exercise 4: groupby`.

## Stretch

- Group by two keys at once. Add a `channel` column with values like
  `"in-store"` and `"online"`, then run
  `df.groupby(["category", "channel"])["revenue"].sum()` and look at the
  MultiIndex it returns. Flatten it with `.reset_index()`.
- Use `transform` to add a `category_total` column to the original twelve
  rows, then a `share_of_category` column. `transform` broadcasts the group's
  answer back to every member row — the one groupby behavior that does not
  collapse the frame.
- Reproduce the summary with `df.pivot_table(index="category",
  values="revenue", aggfunc=["sum", "mean"])` and decide which of the two
  spellings you would rather maintain.
- Use `groupby(...).filter()` to keep only the departments whose total
  revenue clears $700. Three should survive.

When both rankings make sense to you, move on to
[Exercise 5 — Plot](./exercise-05-plot.md).
