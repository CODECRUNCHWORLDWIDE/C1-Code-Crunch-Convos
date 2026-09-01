# Mini-Project Starter — Real-World Dataset Analysis

> **Project:** [Week 13 — Mini-Project: Real-World Dataset Analysis](./README.md)
> **Week:** 13
> **What this is:** the scaffold for the Week 13 notebook. Create
> `analysis.ipynb` next to this page and paste the cells below into it, one
> cell per block, in order. It ships with a small table written inline so the
> whole notebook runs top to bottom before you have downloaded anything; when
> your own dataset arrives you replace one cell and keep the rest.

The six section headers the project requires — Load, Inspect, Clean, Analyze,
Visualize, Conclude — are already here as markdown cells. Do not renumber
them. A grader, a reviewer, or a future employer reading your notebook wants
to find the cleaning step without hunting for it.

## How to use this page

1. Make the project folder, move into it, and create a virtual environment:

   ```bash
   mkdir -p week-13/mini-project
   cd week-13/mini-project
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell the activate line is `.venv\Scripts\Activate.ps1`.

2. Save the dependency block from the Requirements section below as
   `requirements.txt` in that folder, then install it:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the notebook server and create a new Python 3 notebook named
   `analysis.ipynb`:

   ```bash
   jupyter lab
   ```

4. Paste the cells below in order, one block per notebook cell. Blocks marked
   *markdown cell* need the cell type changed from Code to Markdown — press
   `Esc` then `M`, or use the dropdown in the toolbar.

5. Run the whole notebook before you edit anything: **Run > Run All Cells**.
   Every cell should execute. The tables will be incomplete and the three
   charts will come out blank, which is exactly right — the plumbing works, so
   from here on any error you see comes from a line you wrote.

6. Work the eleven `TODO`s top to bottom, running each cell as you go.

7. When the notebook is finished, restart the kernel and run all cells once
   more from a clean slate. A notebook that only works because you ran cells
   out of order does not work.

## Requirements

Save this as `requirements.txt` beside your notebook. These are the versions
the outputs on this page were produced with.

```text
pandas==2.2.3
numpy==2.2.3
matplotlib==3.10.1
jupyterlab==4.4.5
ipykernel==6.30.0
```

Install them into the active virtual environment with:

```bash
python -m pip install -r requirements.txt
```

If you add anything later — `seaborn`, `pyarrow`, `openpyxl` for Excel files —
pin it too, then regenerate the file with `python -m pip freeze >
requirements.txt`. A `requirements.txt` that does not name versions is a
promise that your notebook will still run next year, and it is a promise
nobody can keep.

## The starter

### Cell 1 — title (markdown cell)

```markdown
# Repair Café Analysis

A neighborhood repair café meets on the first Saturday of the month.
Volunteers take in broken electronics, clothing and bicycles, and log how
many items came in, how many left working, and how many volunteer hours
it took. Five sessions are recorded here, January to May 2024.

**Question:** which category of repair gives the community the most
working items back per volunteer hour, and is the café getting better at
it over time?

Replace this cell with your own dataset and your own question before you
submit.
```

### Cell 2 — imports and setup

```python
"""analysis.ipynb — Week 13 mini-project.

Loads a small repair log, cleans it, summarises it, and saves three
charts. Replace the LOAD cell with your own dataset when you have one.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
```

### Cell 3 — section header (markdown cell)

```markdown
## 1. Load
```

### Cell 4 — build the DataFrame

```python
REPAIR_LOG: dict[str, list] = {
    "date": [
        "2024-01-06", "2024-01-06", "2024-01-06",
        "2024-02-03", "2024-02-03", "2024-02-03",
        "2024-03-02", "2024-03-02", "2024-03-02",
        "2024-04-06", "2024-04-06", "2024-04-06",
        "2024-05-04", "2024-05-04", "2024-05-04",
    ],
    "category": [
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
        "Electronics", "Textiles", "Bicycles",
    ],
    "items_in": [22, 15, 11, 26, 18, 14, 31, 21, 19,
                 28, 24, 23, 35, 27, 26],
    "items_fixed": [14, 12, 9, 15, 15, 12, 20, 18, 16,
                    17, 21, 20, 21, 23, 22],
    "volunteer_hours": [18.0, 9.0, 12.0, 20.0, 10.5, 15.0,
                        24.0, None, 19.5, 22.0, 13.5, 21.0,
                        26.0, 15.0, 24.0],
}

df = pd.DataFrame(REPAIR_LOG)

# TODO 1: once you have picked your own dataset, replace the two lines
#         above with a read_csv call and delete REPAIR_LOG entirely:
#             df = pd.read_csv("your-data.csv", parse_dates=["date"])
#         While you are building the pipeline, add nrows=10_000 to keep
#         each run fast, then take it out for the final pass.

print(df.head())
```

### Cell 5 — section header (markdown cell)

```markdown
## 2. Inspect
```

### Cell 6 — four questions about the table

```python
print(df.shape)
print(df.dtypes)

# TODO 2: print the missing-data audit with df.isna().sum(). One column
#         here has a gap in it; find out which, and how many.
# TODO 3: print df.describe().round(2). Compare the `count` row against
#         the 15 rows df.shape reported and note where they disagree.
```

### Cell 7 — section header (markdown cell)

```markdown
## 3. Clean
```

### Cell 8 — dtypes, gaps, derived columns

```python
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%b")

# TODO 4: volunteer_hours has one missing value. Fill it with the column
#         median and assign the result back to df["volunteer_hours"].
#         Median, not mean: one unusually long session would drag a mean
#         and cannot drag a median.
# TODO 5: add df["fix_rate"], items_fixed divided by items_in, rounded to
#         3 decimals. Then print
#         df[["date", "category", "month", "volunteer_hours",
#             "fix_rate"]].head()
#         to check both new columns at once.

print(df.dtypes)
```

### Cell 9 — section header (markdown cell)

```markdown
## 4. Analyze
```

### Cell 10 — first aggregation: by category

```python
by_category = df.groupby("category").agg(
    sessions=("items_in", "size"),
    # TODO 6: add three more named aggregations, all "sum":
    #         items_in, items_fixed, and hours (from volunteer_hours).
)

# TODO 7: add a fix_rate column to by_category — total items_fixed over
#         total items_in, rounded to 3. Compute it from the summed
#         columns, not by averaging df["fix_rate"]. A mean of ratios
#         weights a 5-item session the same as a 35-item one, which is
#         not the number anybody wants.

print(by_category)
```

### Cell 11 — second aggregation: by month and category

```python
by_month = df.pivot_table(
    index="month",
    columns="category",
    values="items_fixed",
    aggfunc="sum",
)

# TODO 8: pivot_table sorts its index, and "Apr" sorts before "Jan".
#         Chain .reindex(["Jan", "Feb", "Mar", "Apr", "May"]) onto the
#         call above so the months read in calendar order.

print(by_month)
```

### Cell 12 — the headline numbers

```python
items_in = df["items_in"].sum()
items_fixed = df["items_fixed"].sum()
hours = df["volunteer_hours"].sum()

print(f"Sessions logged:      {len(df)}")
print(f"Items brought in:     {items_in}")

# TODO 9: print three more lines, lined up in the same column:
#         "Items repaired:" as a plain count,
#         "Overall fix rate:" as items_fixed / items_in with :.1%,
#         "Volunteer hours:" with :.2f,
#         and "Repairs per hour:" as items_fixed / hours with :.2f.
```

### Cell 13 — section header (markdown cell)

```markdown
## 5. Visualize
```

### Cell 14 — chart one: repairs by category

```python
fig, ax = plt.subplots(figsize=(8, 5))

# TODO 10a: draw bars from by_category.index and
#           by_category["items_fixed"], then set the title, the x label,
#           and a y label that names the unit — "Items repaired (count)",
#           not "Items". Add ax.grid(axis="y", alpha=0.3).

fig.tight_layout()
fig.savefig(FIGURE_DIR / "main.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved figures/main.png")
```

### Cell 15 — chart two: intake against repairs over time

```python
monthly = df.groupby("month", sort=False)[["items_in", "items_fixed"]].sum()
print(monthly)

fig, ax = plt.subplots(figsize=(8, 5))

# TODO 10b: plot two lines against monthly.index, one for each column,
#           with marker="o" and a label= on each so the legend has
#           something to show. Title, both axis labels, ax.legend(), and
#           ax.grid(alpha=0.3).

fig.tight_layout()
fig.savefig(FIGURE_DIR / "monthly-trend.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved figures/monthly-trend.png")
```

### Cell 16 — chart three: fix rate by category

```python
fig, ax = plt.subplots(figsize=(8, 5))

# TODO 10c: draw a horizontal bar chart with ax.barh from
#           by_category.index and by_category["fix_rate"]. Title, both
#           axis labels, ax.set_xlim(0, 1) so the bars are read against
#           the whole scale, and ax.grid(axis="x", alpha=0.3).

fig.tight_layout()
fig.savefig(FIGURE_DIR / "fix-rate.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved figures/fix-rate.png")
```

### Cell 17 — section header and conclusion (markdown cell)

```markdown
## 6. Conclude

TODO 11: replace this cell with two or three sentences of your own,
written after you have read your own charts. Every sentence must carry a
number from the notebook above it. A conclusion a reader cannot check
against a table is an opinion.

Answer three things:

1. What the data says. Name the figure.
2. Why it might be so, and what would have to be true for that to hold.
3. What you would look at next with another week.
```

## What each TODO is asking for

- **TODO 1 — swap in your dataset.** The inline dictionary exists so the
  notebook runs on the train. Once you have your CSV, `pd.read_csv` replaces
  it. Pass `parse_dates=["date"]` in the call rather than converting
  afterwards — pandas reads the column as datetimes directly, and a date left
  as a string will not sort, resample or plot correctly.
- **TODO 2 — the missing-data audit.** `df.isna()` gives a table of booleans
  the same shape as your data; `.sum()` counts the `True`s down each column,
  because `True` counts as 1. Do this before anything else. A `NaN` you have
  not seen becomes a mean you cannot explain.
- **TODO 3 — `describe`.** Round it, or you get six decimal places of noise on
  a column of item counts. Read the `count` row first: it will say 15 for
  every column except the one with the gap, which is the same fact `isna()`
  gave you, said from the other direction.
- **TODO 4 — fill the gap.** `Series.fillna(value)` returns a new Series, so
  assign it back to the column or nothing changes. The alternative is
  `dropna()`, and here it would be the wrong call: that row has good
  `items_in` and `items_fixed` numbers, and throwing all five columns away to
  avoid one blank cell costs you real data.
- **TODO 5 — the derived column.** `df["items_fixed"] / df["items_in"]`
  divides row by row in compiled code. Do not reach for `apply` and do not
  write a loop. Round to three decimals here, so the column reads cleanly
  everywhere it appears later.
- **TODO 6 — the named aggregations.** The keyword form
  `name=("column", "function")` names the output columns as it builds them,
  which is why the result prints with headers you chose rather than a
  two-level index you then have to flatten. `"size"` counts rows in the group;
  `"sum"` adds a column up.
- **TODO 7 — the aggregate fix rate.** Divide the summed column by the summed
  column. This is the one place in the notebook where the obvious shortcut is
  wrong: the mean of the fifteen per-session rates is not the overall rate,
  because the sessions are not the same size. Work it out both ways once and
  see how far apart they land.
- **TODO 8 — put the months back in order.** `pivot_table` sorts its index,
  and alphabetically April comes first. `.reindex([...])` with the months you
  want, in the order you want them, fixes it. Any month you leave out of that
  list disappears from the table, and any month you spell wrong comes back as
  a row of `NaN` — both are useful, and both are easy to miss.
- **TODO 9 — the headline lines.** Four f-strings. `:.1%` multiplies by 100
  and appends the percent sign for you, so you never write `* 100` by hand and
  never forget it. Pad the labels so the numbers line up in one column; a
  ragged block of figures is harder to scan than a straight one.
- **TODO 10a, 10b, 10c — the three charts.** Same discipline on all three,
  and it is the discipline the rubric grades: a title that states what the
  chart shows, an x label, and a y label that names the unit. Where there is
  more than one series, a legend. The `fig, ax = plt.subplots()` form is
  already given because holding the figure and the axes yourself is what lets
  you save a specific chart rather than whatever matplotlib last drew on.
- **TODO 11 — the conclusion.** Written last, from your own charts. Three
  sentences with numbers in them beat a page without.

## Expected output when you are done

Running **Run All Cells** on the finished notebook, with the starter data
still in place, produces this. Your own dataset will produce different
numbers; the shape of each block is what you are matching.

```text
$ jupyter lab

[Cell 4]
         date     category  items_in  items_fixed  volunteer_hours
0  2024-01-06  Electronics        22           14             18.0
1  2024-01-06     Textiles        15           12              9.0
2  2024-01-06     Bicycles        11            9             12.0
3  2024-02-03  Electronics        26           15             20.0
4  2024-02-03     Textiles        18           15             10.5

[Cell 6]
(15, 5)
date                object
category            object
items_in             int64
items_fixed          int64
volunteer_hours    float64
dtype: object
date               0
category           0
items_in           0
items_fixed        0
volunteer_hours    1
dtype: int64
       items_in  items_fixed  volunteer_hours
count     15.00        15.00            14.00
mean      22.67        17.00            17.82
std        6.55         4.17             5.39
min       11.00         9.00             9.00
25%       18.50        14.50            13.88
50%       23.00        17.00            18.75
75%       26.50        20.50            21.75
max       35.00        23.00            26.00

[Cell 8]
date               datetime64[ns]
category                   object
items_in                    int64
items_fixed                 int64
volunteer_hours           float64
month                      object
fix_rate                  float64
dtype: object
        date     category month  volunteer_hours  fix_rate
0 2024-01-06  Electronics   Jan             18.0     0.636
1 2024-01-06     Textiles   Jan              9.0     0.800
2 2024-01-06     Bicycles   Jan             12.0     0.818
3 2024-02-03  Electronics   Feb             20.0     0.577
4 2024-02-03     Textiles   Feb             10.5     0.833

[Cell 10]
             sessions  items_in  items_fixed   hours  fix_rate
category
Bicycles            5        93           79   91.50     0.849
Electronics         5       142           87  110.00     0.613
Textiles            5       105           89   66.75     0.848

[Cell 11]
category  Bicycles  Electronics  Textiles
month
Jan              9           14        12
Feb             12           15        15
Mar             16           20        18
Apr             20           17        21
May             22           21        23

[Cell 12]
Sessions logged:      15
Items brought in:     340
Items repaired:       255
Overall fix rate:     75.0%
Volunteer hours:      268.25
Repairs per hour:     0.95

[Cell 14]
Saved figures/main.png

[Cell 15]
       items_in  items_fixed
month
Jan          48           35
Feb          58           42
Mar          71           54
Apr          75           58
May          88           66
Saved figures/monthly-trend.png

[Cell 16]
Saved figures/fix-rate.png
```

Three numbers in there are worth a second look, because they are what the
conclusion cell is for.

The overall fix rate is exactly 75.0 percent — 255 items out of 340. Electronics
is the outlier at 0.613 while textiles and bicycles both sit near 0.85, which
is the answer to the first half of the question: broken electronics are
genuinely harder to fix than a torn hem or a slipped chain. And the 268.25
volunteer hours include the median value you filled into the one blank cell,
so if your total reads 249.50 instead, TODO 4 is not done.

The monthly table answers the second half. Intake rose from 48 items to 88
across five sessions and repairs rose from 35 to 66 — both growing, at close
to the same rate, so the café is getting busier rather than better. That is a
less flattering finding than "we improved", and it is the one the numbers
support.

Then open the three PNGs and check each one has a title, both axis labels
with units, a legend where there is more than one series, nothing clipped at
the edges, and a y axis that starts at zero.

## Common bugs to catch

- **`ValueError: All arrays must be of the same length`** when Cell 4 runs.
  One of the five lists in `REPAIR_LOG` has fourteen or sixteen entries. Let
  Python count them for you:
  `print({k: len(v) for k, v in REPAIR_LOG.items()})`. Every value must be 15.
- **`KeyError: 'month'`** in Cell 11 or Cell 15. You ran the analysis cells
  without running Cell 8 first, or you restarted the kernel and jumped back
  into the middle. Run All Cells from the top; out-of-order execution is the
  single most common way a notebook lies to you.
- **`AttributeError: Can only use .dt accessor with datetimelike values`.**
  Cell 8's `to_datetime` line did not run, so `date` is still text. The `.dt`
  accessor only exists on a datetime column, which is why the conversion has
  to come first.
- **The pivot table reads Apr, Feb, Jan, Mar, May.** TODO 8 is not done.
  `pivot_table` sorts its index and your months are strings, so it sorts them
  alphabetically. `.reindex()` with an explicit list is the fix.
- **`SettingWithCopyWarning: A value is trying to be set on a copy of a slice
  from a DataFrame`.** You assigned a new column onto a filtered subset —
  `subset["fix_rate"] = ...` where `subset = df[df["items_in"] > 20]`. pandas
  cannot tell whether you meant to change the original. Take an explicit
  `.copy()` when you slice, or assign onto `df` itself as the starter does.
- **The charts are blank but no error appears.** The `fig.savefig(...)` line
  runs whether or not you drew anything, which is by design — it proves the
  plumbing before you touch the drawing. If the PNG is empty, your `ax.bar`
  or `ax.plot` call is missing, or you drew on a different axes object.
- **`FileNotFoundError: [Errno 2] No such file or directory:
  'figures/main.png'`.** The `FIGURE_DIR.mkdir(...)` line in Cell 2 did not
  run. matplotlib will create a file but never a folder.
- **The chart from the last run keeps reappearing.** Your image viewer is
  showing a cached copy. Close it and reopen, or check the file's modification
  time. Adding `plt.close(fig)` — already in the starter — stops the other
  version of this problem, where figures pile up in memory until you get
  `RuntimeWarning: More than 20 figures have been opened`.

## When you are done

The project rubric is worth twenty-five points. These are the same criteria,
phrased as things you can check.

- [ ] Restart the kernel and Run All Cells: every cell executes, top to
      bottom, with no traceback.
- [ ] All six required sections are present, in order, as markdown headers.
- [ ] The cleaning step is documented — a reader can see which dtype changed,
      which gap you filled, and why you filled rather than dropped it.
- [ ] Three charts, each with a title, both axis labels including units, and a
      legend where there is more than one series.
- [ ] At least two non-trivial aggregations: the `groupby` in Cell 10 and the
      `pivot_table` in Cell 11 both count.
- [ ] `figures/main.png` exists, and is recreated after you delete it and
      rerun.
- [ ] `requirements.txt` names every package you actually imported, with a
      pinned version for each.
- [ ] `findings.md` answers the three questions from the project README, and
      every claim in it carries a number from the notebook.
- [ ] No `TODO` comments are left anywhere in the notebook.
- [ ] Committed and pushed:

      ```bash
      git add analysis.ipynb requirements.txt findings.md figures/main.png
      git commit -m "Week 13 mini-project: dataset analysis notebook"
      git push
      ```

This is the first thing in the bootcamp you can hand to a stranger. Before you
call it finished, read it once as that stranger: open it cold, top to bottom,
and see whether the question in Cell 1 gets an answer by Cell 17.
