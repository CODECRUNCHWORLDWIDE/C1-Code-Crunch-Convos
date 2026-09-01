# Mini-Project — Real-World Dataset Analysis

> **Topic:** the whole week in one notebook — load, inspect, clean, aggregate, plot, and write down what you found
> **Lecture:** [01 — NumPy and pandas Basics](../lecture-notes/01-numpy-and-pandas-basics.md) · [02 — Cleaning and Transforming](../lecture-notes/02-cleaning-and-transforming.md) · [03 — Aggregation and Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Medium
> **Target time:** 8 hours
> **Why this one:** it is the first thing in this course you can hand to a stranger. Every data job description asks for someone "comfortable with messy real-world data in Python", and a notebook that loads a real file, cleans it, charts it and says what it means is the proof.

## The Brief

Pick a free public dataset that genuinely interests you. Build one Jupyter
notebook that loads it, cleans it, summarises it with at least three charts,
and ends with a short written answer to a question you asked *before* you
started.

Think of the dataset as a shoebox of receipts somebody just handed you. Nobody
wants the shoebox. They want one sentence: *where did the money go, and how do
you know?* Every step below — the loading, the hunt for missing values, the
`groupby`, the three pictures — exists to earn that one sentence at the end.

The notebook has six sections, always in this order, always with these names:

1. **Load** — `pd.read_csv(...)` or equivalent.
2. **Inspect** — `head()`, `info()`, `describe()`, and a missing-data audit.
3. **Clean** — fix dtypes, fill or drop the gaps, build derived columns.
4. **Analyze** — at least two `groupby` + `agg` or `pivot_table` summaries.
5. **Visualize** — at least three charts, each with a title and labelled axes.
6. **Conclude** — two or three sentences answering the question you set out
   with, every one of them carrying a number from the tables above it.

Do not renumber them. A grader, a reviewer, or a future employer reading your
notebook wants to find the cleaning step without hunting for it.

### Suggested datasets

Use any dataset you like. These five are a curated start — each has at least
1,000 rows and at least 5 columns.

| Topic | Source | Direct link |
|-------|--------|-------------|
| **NYC Taxi trips** | NYC Open Data | <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page> |
| **Olympic medals (1896–2022)** | Kaggle | <https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results> |
| **COVID-19 time series** | Our World in Data | <https://github.com/owid/covid-19-data/tree/master/public/data> |
| **World Bank indicators** | World Bank | <https://data.worldbank.org/> |
| **Spotify charts data** | Kaggle | <https://www.kaggle.com/datasets/dhruvildave/spotify-charts> |

Other places to browse: [Kaggle Datasets](https://www.kaggle.com/datasets),
[data.gov](https://data.gov/), and
[Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets).

Avoid anything larger than about 500 MB on your first try. How fast the
notebook re-runs matters more than how much data is in it, and a run you have
to wait ninety seconds for is a run you stop doing.

## Starter

This section is the whole scaffold. It also lives beside this page as
[`starter.md`](./starter.md) if you would rather scroll one file while you
type — the two say the same thing.

The scaffold ships with a small table written inline, so the notebook runs top
to bottom before you have downloaded anything. When your own dataset arrives
you replace one cell and keep the rest.

### Set the project up

1. Make the project folder, move into it, and create a virtual environment:

   ```bash
   mkdir -p week-13/mini-project
   cd week-13/mini-project
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell the activate line is `.venv\Scripts\Activate.ps1`.

2. Save this as `requirements.txt` in that folder. These are the versions the
   numbers on this page were produced with:

   ```text
   pandas==2.2.3
   numpy==2.2.3
   matplotlib==3.10.1
   jupyterlab==4.4.5
   ipykernel==6.30.0
   ```

   Install it:

   ```bash
   python -m pip install -r requirements.txt
   ```

   If you add anything later — `seaborn`, `pyarrow`, `openpyxl` for Excel
   files — pin it too, then regenerate with
   `python -m pip freeze > requirements.txt`. A `requirements.txt` with no
   version numbers is a promise that your notebook will still run next year,
   and it is a promise nobody can keep.

3. Start the notebook server and make a new Python 3 notebook called
   `analysis.ipynb`:

   ```bash
   jupyter lab
   ```

4. Paste the cells below in order, one block per cell. Blocks marked *markdown
   cell* need the cell type changed from Code to Markdown — press `Esc` then
   `M`, or use the toolbar dropdown.

5. Run the whole thing before you edit anything: **Run > Run All Cells**. Every
   cell should execute. The tables will be incomplete and the three charts will
   come out blank, which is exactly right — the plumbing works, so from here on
   any error you see comes from a line you wrote.

6. Work the eleven `TODO`s top to bottom, running each cell as you go.

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
#         weights an 11-item session the same as a 35-item one, which is
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

## Requirements

1. **A Jupyter notebook** named `analysis.ipynb` in your project folder, with
   the six sections above, in order, as markdown headers.
2. **It runs top to bottom from a restarted kernel** with no traceback.
3. **At least two non-trivial aggregations** — the `groupby` in Cell 10 and the
   `pivot_table` in Cell 11 both count.
4. **At least three charts**, each with a title, both axis labels including the
   unit, and a legend wherever there is more than one series.
5. **At least one saved chart** as a PNG at `figures/main.png`.
6. **A one-page summary** named `findings.md`, answering three questions: what
   dataset you picked and why; the single most interesting thing you found; and
   what you would investigate next with another week.
7. **A `requirements.txt`** naming every package you actually imported, each
   with a pinned version.
8. **No `TODO` comments left anywhere** in the finished notebook.

## Constraints

- **Look for missing values before you compute anything.** `df.isna().sum()`
  comes first, always. A `NaN` you have not seen becomes a mean you cannot
  explain, and pandas will not warn you — most of its arithmetic skips missing
  values silently, so a column with a hole in it quietly averages over fewer
  rows than you think.
- **Fill or drop, but say which and say why.** Both are defensible; neither is
  defensible unsaid. Here the gap is filled with the **median**, because one
  unusually long session would drag a mean and cannot drag a median, and it is
  filled rather than dropped because that row still carries good `items_in` and
  `items_fixed` numbers.
- **Aggregate rates from the totals, never by averaging the rates.** The
  overall fix rate is total fixed over total in. The mean of fifteen
  per-session rates is a different number, because the sessions are not the
  same size — it lets an 11-item Saturday vote as loudly as a 35-item one.
- **`parse_dates` in the `read_csv` call, not a conversion afterwards.** A date
  left as text will not sort, will not resample, and will plot as a smear of
  category labels. Convert it at the door.
- **Every chart gets a title, both axis labels, and units in the y label.**
  `Revenue` could be dollars, cups, or thousands of dollars. `Revenue ($)`
  cannot be misread. An unlabelled chart is decoration, not information.
- **A correlation is not a cause.** Two lines that rise together are a pattern
  you found, not a mechanism you proved. Write the finding as what the data
  shows, then name at least one other thing that could have produced the same
  picture. This is the single easiest place to lose a reader's trust, and the
  cheapest to get right.
- **Keep the first run small.** `nrows=10_000` while you build the pipeline,
  removed for the final pass. A run you wait ninety seconds for is a run you
  stop doing, and a pipeline you stop re-running is a pipeline that quietly
  breaks.

## Expected output

This is the finished pipeline, run end to end on the starter's repair log. Your
own dataset will produce different numbers; the shape of each block is what you
are matching.

```text
$ python repair-cafe-analysis.py
Repair Cafe Analysis — the Week 13 mini-project, end to end.

1. Load
         date     category  items_in  items_fixed  volunteer_hours
0  2024-01-06  Electronics        22           14             18.0
1  2024-01-06     Textiles        15           12              9.0
2  2024-01-06     Bicycles        11            9             12.0
3  2024-02-03  Electronics        26           15             20.0
4  2024-02-03     Textiles        18           15             10.5

2. Inspect
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

3. Clean
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

4. Analyze
             sessions  items_in  items_fixed   hours  fix_rate  per_hour
category                                                                
Bicycles            5        93           79   91.50     0.849      0.86
Electronics         5       142           87  110.00     0.613      0.79
Textiles            5       105           89   66.75     0.848      1.33
category  Bicycles  Electronics  Textiles
month                                    
Jan              9           14        12
Feb             12           15        15
Mar             16           20        18
Apr             20           17        21
May             22           21        23
Sessions logged:      15
Items brought in:     340
Items repaired:       255
Overall fix rate:     75.0%
Volunteer hours:      268.25
Repairs per hour:     0.95

5. Visualize
Saved figures/main.png
       items_in  items_fixed
month                       
Jan          48           35
Feb          58           42
Mar          71           54
Apr          75           58
May          88           66
Saved figures/monthly-trend.png
Saved figures/fix-rate.png

6. Conclude
Textiles give the community the most back per volunteer hour: 1.33 repaired items an hour, against 0.86 for bicycles and 0.79 for electronics.
Electronics is also the hardest category to fix at all, sending home 61.3% of what arrives against 84.8% for textiles.
Intake climbed from 48 items in Jan to 88 in May while repairs climbed from 35 to 66, so the cafe is getting busier rather than better.
Both numbers rising together is a pattern, not a cause: five sessions cannot tell us whether word of mouth, the weather or the new tool wall brought people in.
```

Three things in there are worth a second look, because they are what the
conclusion is for.

The overall fix rate is exactly 75.0 percent — 255 items out of 340. Electronics
sits at 0.613 while textiles and bicycles both sit near 0.85, which answers the
first half of the question: broken electronics really are harder to fix than a
torn hem or a slipped chain. And the 268.25 volunteer hours *include* the median
value filled into the one blank cell, so if your total reads 249.50 instead,
TODO 4 is not done.

The monthly table answers the second half. Intake rose from 48 items to 88
across five sessions and repairs rose from 35 to 66 — both growing, at close to
the same rate. So the café is getting busier rather than better. That is a less
flattering finding than "we improved", and it is the one the numbers support.

Then open the three PNGs and check each one has a title, both axis labels with
units, a legend where there is more than one series, nothing clipped at the
edges, and a y axis that starts at zero.

## Steps

Eleven TODOs, worked top to bottom. Run each cell as you finish it.

1. **TODO 1 — swap in your dataset.** The inline dictionary exists so the
   notebook runs on the train. Once you have your CSV, `pd.read_csv` replaces
   it. Pass `parse_dates=["date"]` in the call rather than converting
   afterwards.
2. **TODO 2 — the missing-data audit.** `df.isna()` gives a table of booleans
   the same shape as your data; `.sum()` counts the `True`s down each column,
   because `True` counts as 1.
3. **TODO 3 — `describe`.** Round it, or you get six decimal places of noise on
   a column of item counts. Read the `count` row first: it says 15 for every
   column except the one with the gap — the same fact `isna()` gave you, said
   from the other direction.
4. **TODO 4 — fill the gap.** `Series.fillna(value)` returns a *new* Series, so
   assign it back to the column or nothing changes. That single line is the
   difference between 268.25 volunteer hours and 249.50.
5. **TODO 5 — the derived column.** `df["items_fixed"] / df["items_in"]`
   divides row by row in compiled code. Do not reach for `apply` and do not
   write a loop. Round to three decimals here, so the column reads cleanly
   everywhere it appears later.
6. **TODO 6 — the named aggregations.** The keyword form
   `name=("column", "function")` names the output columns as it builds them,
   which is why the result prints with headers you chose rather than a
   two-level index you then have to flatten. `"size"` counts rows in the group;
   `"sum"` adds a column up.
7. **TODO 7 — the aggregate fix rate.** Divide the summed column by the summed
   column. This is the one place in the notebook where the obvious shortcut is
   wrong. Work it out both ways once and see how far apart they land.
8. **TODO 8 — put the months back in order.** `.reindex([...])` with the months
   you want, in the order you want them. Any month you leave out of that list
   disappears from the table, and any month you spell wrong comes back as a row
   of `NaN` — both are useful, and both are easy to miss.
9. **TODO 9 — the headline lines.** Four f-strings. `:.1%` multiplies by 100 and
   appends the percent sign for you, so you never write `* 100` by hand and
   never forget it. Pad the labels so the numbers line up in one column.
10. **TODO 10a, 10b, 10c — the three charts.** Same discipline on all three, and
    it is the discipline the checklist grades: a title that states what the
    chart shows, an x label, and a y label that names the unit. Where there is
    more than one series, a legend. The `fig, ax = plt.subplots()` form is
    already given because holding the figure and the axes yourself is what lets
    you save a *specific* chart rather than whatever matplotlib last drew on.
11. **TODO 11 — the conclusion.** Written last, from your own charts. Three
    sentences with numbers in them beat a page without.

Then, before you call it done: restart the kernel and Run All Cells from a
clean slate. A notebook that only works because you ran cells out of order does
not work.

## The Solution

```python
"""repair-cafe-analysis.py — the finished answer to the Week 13 mini-project.

The whole six-step pipeline the project asks for — Load, Inspect, Clean,
Analyze, Visualize, Conclude — worked all the way through on the repair-café
log that ``starter.md`` ships. Every TODO in the starter is done here.

Your own deliverable is a notebook, ``analysis.ipynb``, plus ``findings.md``,
``requirements.txt`` and ``figures/main.png``. A notebook cannot be run by a
plain ``python`` command, so the reference answer ships as this script: same
data, same steps, same numbers, one cell after another turned into one section
after another. Read it top to bottom and you are reading the finished notebook.

Two small differences, both so the download proves itself and leaves nothing
behind. It renders with matplotlib's non-interactive ``Agg`` backend, so no
window is ever opened. And it writes its three charts into a ``figures/`` folder
inside a throwaway temporary directory that Python deletes on the way out, then
prints what it saved. Your notebook saves into a real ``figures/`` beside it, so
you can open the pictures.

Run it with::

    python repair-cafe-analysis.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May"]

# The log five volunteers filled in by hand, one row per category per session.
# Replace this with pd.read_csv("your-data.csv", parse_dates=["date"]) when you
# bring your own dataset. One blank cell is left in on purpose: real logs have
# gaps, and the Clean step is where you decide what to do about them.
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


def load() -> pd.DataFrame:
    """Step 1 — get the table into memory and look at the first few rows."""
    return pd.DataFrame(REPAIR_LOG)


def inspect(df: pd.DataFrame) -> None:
    """Step 2 — shape, dtypes, the missing-data audit, and the summary stats."""
    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum())
    print(df.describe().round(2))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3 — fix the dtypes, fill the one gap, add the derived columns.

    The gap is filled with the median rather than the mean because one
    unusually long session would drag a mean and cannot drag a median. It is
    filled rather than dropped because that row still has good ``items_in`` and
    ``items_fixed`` numbers, and throwing five columns away to avoid one blank
    cell costs real data.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%b")
    df["volunteer_hours"] = df["volunteer_hours"].fillna(
        df["volunteer_hours"].median()
    )
    df["fix_rate"] = (df["items_fixed"] / df["items_in"]).round(3)
    return df


def summarise_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4a — one row per repair category, totalled.

    ``fix_rate`` here is total fixed over total in, not the average of the
    per-session rates. A mean of ratios weights an 11-item session the same as
    a 35-item one, which is not the number anybody wants.
    """
    by_category = df.groupby("category").agg(
        sessions=("items_in", "size"),
        items_in=("items_in", "sum"),
        items_fixed=("items_fixed", "sum"),
        hours=("volunteer_hours", "sum"),
    )
    by_category["fix_rate"] = (
        by_category["items_fixed"] / by_category["items_in"]
    ).round(3)
    by_category["per_hour"] = (
        by_category["items_fixed"] / by_category["hours"]
    ).round(2)
    return by_category


def summarise_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4b — repairs per month per category, months in calendar order.

    ``pivot_table`` sorts its index, and "Apr" sorts before "Jan", so the
    ``reindex`` is what puts the year back in the order a reader expects.
    """
    return df.pivot_table(
        index="month",
        columns="category",
        values="items_fixed",
        aggfunc="sum",
    ).reindex(MONTH_ORDER)


def headline(df: pd.DataFrame) -> None:
    """Step 4c — the five numbers the conclusion is allowed to lean on."""
    items_in = df["items_in"].sum()
    items_fixed = df["items_fixed"].sum()
    hours = df["volunteer_hours"].sum()

    print(f"Sessions logged:      {len(df)}")
    print(f"Items brought in:     {items_in}")
    print(f"Items repaired:       {items_fixed}")
    print(f"Overall fix rate:     {items_fixed / items_in:.1%}")
    print(f"Volunteer hours:      {hours:.2f}")
    print(f"Repairs per hour:     {items_fixed / hours:.2f}")


def draw_charts(df: pd.DataFrame, by_category: pd.DataFrame,
                figure_dir: Path) -> pd.DataFrame:
    """Step 5 — three labelled charts, each saved and each announced.

    Returns the month-by-month totals, because the second chart has to compute
    them and the conclusion wants to quote them.
    """
    figure_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(by_category.index, by_category["items_fixed"], color="#3273dc")
    ax.set_title("Items repaired by category, Jan–May 2024")
    ax.set_xlabel("Category")
    ax.set_ylabel("Items repaired (count)")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "main.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/main.png")

    monthly = df.groupby("month", sort=False)[["items_in", "items_fixed"]].sum()
    print(monthly)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly.index, monthly["items_in"], marker="o", label="Brought in")
    ax.plot(monthly.index, monthly["items_fixed"], marker="o", label="Repaired")
    ax.set_title("Intake and repairs by month, Jan–May 2024")
    ax.set_xlabel("Month")
    ax.set_ylabel("Items (count)")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "monthly-trend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/monthly-trend.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(by_category.index, by_category["fix_rate"], color="#27ae60")
    ax.set_title("Share of items sent home working, by category")
    ax.set_xlabel("Fix rate (share of items brought in)")
    ax.set_ylabel("Category")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(figure_dir / "fix-rate.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/fix-rate.png")

    return monthly


def conclude(by_category: pd.DataFrame, monthly: pd.DataFrame) -> None:
    """Step 6 — three sentences, every one of them carrying a number."""
    best = by_category["per_hour"].idxmax()
    print(
        f"{best} give the community the most back per volunteer hour: "
        f"{by_category.loc[best, 'per_hour']:.2f} repaired items an hour, "
        f"against {by_category.loc['Bicycles', 'per_hour']:.2f} for bicycles "
        f"and {by_category.loc['Electronics', 'per_hour']:.2f} for electronics."
    )
    print(
        "Electronics is also the hardest category to fix at all, sending home "
        f"{by_category.loc['Electronics', 'fix_rate']:.1%} of what arrives "
        f"against {by_category.loc['Textiles', 'fix_rate']:.1%} for textiles."
    )
    first, last = monthly.index[0], monthly.index[-1]
    print(
        f"Intake climbed from {monthly.loc[first, 'items_in']} items in {first} "
        f"to {monthly.loc[last, 'items_in']} in {last} while repairs climbed "
        f"from {monthly.loc[first, 'items_fixed']} to "
        f"{monthly.loc[last, 'items_fixed']}, so the cafe is getting busier "
        "rather than better."
    )
    print(
        "Both numbers rising together is a pattern, not a cause: five sessions "
        "cannot tell us whether word of mouth, the weather or the new tool "
        "wall brought people in."
    )


def main() -> None:
    """Run the whole pipeline and narrate each step."""
    print("Repair Cafe Analysis — the Week 13 mini-project, end to end.")

    print()
    print("1. Load")
    df = load()
    print(df.head())

    print()
    print("2. Inspect")
    inspect(df)

    print()
    print("3. Clean")
    df = clean(df)
    print(df.dtypes)
    print(df[["date", "category", "month", "volunteer_hours", "fix_rate"]].head())

    print()
    print("4. Analyze")
    by_category = summarise_by_category(df)
    print(by_category)
    print(summarise_by_month(df))
    headline(df)

    print()
    print("5. Visualize")
    with tempfile.TemporaryDirectory() as workspace:
        monthly = draw_charts(df, by_category, Path(workspace) / "figures")

    print()
    print("6. Conclude")
    conclude(by_category, monthly)


if __name__ == "__main__":
    main()
```

**Why it works.** The script is the notebook with the cell walls taken out.
Each of the six steps is one function, in the same order, with the same names,
and `main()` calls them one after another — so `load`, `inspect`, `clean`,
`summarise_by_category`, `draw_charts` and `conclude` are Cells 4, 6, 8, 10, 14
and 17. Reading it top to bottom is reading the finished notebook.

**`clean()` takes a copy first.** `df = df.copy()` on the first line means the
function cannot reach back and change the table its caller handed it. That is
also the fix for pandas' most confusing message,
`SettingWithCopyWarning` — it fires when you assign a column onto something
that *might* be a view of another frame, and pandas genuinely cannot tell
whether you meant to change the original. Take an explicit copy and the
question never comes up.

**`fillna` is assigned back.** `df["volunteer_hours"].fillna(...)` builds a new
column and hands it to you; it does not edit the old one. The line reads
`df["volunteer_hours"] = df["volunteer_hours"].fillna(...)` for exactly that
reason. Drop the assignment and the whole notebook still runs, prints no
warning, and is quietly wrong by 18.75 hours.

**The two summaries are two different questions.** `groupby("category")` folds
the table down to one row per category and answers "which kind of repair"; the
`pivot_table` spreads month down the side and category across the top and
answers "and did it change". Both come from the same fifteen rows. A `groupby`
makes the table shorter; a `pivot_table` makes it wider.

**The rates are computed from totals.** `by_category["items_fixed"] /
by_category["hours"]` divides one summed column by another summed column. It
would have been one character shorter to average the per-session `fix_rate`,
and it would have been the wrong number, because the sessions are different
sizes.

**The charts never open a window.** `matplotlib.use("Agg")` runs *before*
`import matplotlib.pyplot`, which is the only moment that choice can be made.
`Agg` draws into a memory buffer and writes PNG files and never asks the
operating system for a window, so the same code runs on your laptop, on a build
server, and over SSH. Each chart is built with the explicit
`fig, ax = plt.subplots()` form, saved with `dpi=150` and
`bbox_inches="tight"`, then closed with `plt.close(fig)` — figures do not free
themselves, and a loop that leaks fifty of them earns you
`RuntimeWarning: More than 20 figures have been opened`.

**`conclude()` reads its numbers out of the tables.** Nothing in those four
sentences is typed by hand; every figure is pulled from `by_category` or
`monthly` with an f-string. Change the data and the conclusion changes with
it, which is the only way a written finding stays true. And the last sentence
is the important one: intake and repairs rose together, and that is a pattern,
not a cause. Five sessions cannot tell you whether word of mouth, the weather,
or a new tool wall brought people through the door.

## Download and run

<!-- no-runnable-file: the deliverable here is a Jupyter notebook plus findings.md, requirements.txt and a figures/ folder, and a .ipynb cannot be started by a plain python command. The runnable answer ships as repair-cafe-analysis.py, the same six steps with the cell walls taken out, linked from Download and run. -->

Download [repair-cafe-analysis.py](./repair-cafe-analysis.py) and run it:

```bash
python -m pip install pandas matplotlib
python repair-cafe-analysis.py
```

It prints the run above. The three charts are written into a `figures/` folder
inside a throwaway temporary directory that Python deletes on the way out, so
the download leaves nothing behind — the `Saved figures/…` lines are the proof
each render worked. Your own `analysis.ipynb` saves into a real `figures/`
beside the notebook, so you can open the pictures. The answer file is named
after the café, not after your notebook, so it can never be mistaken for the
thing you are supposed to write.

## Common bugs to catch

- **`ValueError: All arrays must be of the same length`** when Cell 4 runs. One
  of the five lists in `REPAIR_LOG` has fourteen or sixteen entries. Let Python
  count them for you: `print({k: len(v) for k, v in REPAIR_LOG.items()})`.
  Every value must be 15.
- **`KeyError: 'month'`** in Cell 11 or Cell 15. You ran the analysis cells
  without running Cell 8 first, or you restarted the kernel and jumped back into
  the middle. Run All Cells from the top; out-of-order execution is the single
  most common way a notebook lies to you.
- **`AttributeError: Can only use .dt accessor with datetimelike values`.**
  Cell 8's `to_datetime` line did not run, so `date` is still text. The `.dt`
  accessor only exists on a datetime column, which is why the conversion has to
  come first.
- **The volunteer-hours total reads 249.50 instead of 268.25.** You called
  `fillna` but did not assign the result back to the column. The method returns
  a new Series and leaves the old one alone.
- **The pivot table reads Apr, Feb, Jan, Mar, May.** TODO 8 is not done.
  `pivot_table` sorts its index and your months are strings, so it sorts them
  alphabetically. `.reindex()` with an explicit list is the fix.
- **`SettingWithCopyWarning: A value is trying to be set on a copy of a slice
  from a DataFrame`.** You assigned a new column onto a filtered subset —
  `subset["fix_rate"] = ...` where `subset = df[df["items_in"] > 20]`. pandas
  cannot tell whether you meant to change the original. Take an explicit
  `.copy()` when you slice, or assign onto `df` itself.
- **The charts are blank but no error appears.** The `fig.savefig(...)` line
  runs whether or not you drew anything, which is by design — it proves the
  plumbing before you touch the drawing. If the PNG is empty, your `ax.bar` or
  `ax.plot` call is missing, or you drew on a different axes object.
- **`FileNotFoundError: [Errno 2] No such file or directory:
  'figures/main.png'`.** The `FIGURE_DIR.mkdir(...)` line in Cell 2 did not run.
  matplotlib will create a file but never a folder.
- **`RuntimeWarning: More than 20 figures have been opened`.** You dropped
  `plt.close(fig)`. pyplot keeps a reference to every figure it made, so they
  pile up until you close them.
- **The chart from the last run keeps reappearing.** Your image viewer is
  showing a cached copy. Close it and reopen, or check the file's modification
  time.

## Under the hood

<details>
<summary>Under the hood — why the average of the averages is the wrong number</summary>

Averaging fifteen per-session fix rates and dividing the two totals are not two
ways of getting the same answer. They are two different questions.

The mean of the rates gives every **session** one vote. The ratio of the totals
gives every **item** one vote. On this data the gap is small, but the mechanism
that produces it has a name — the second is a *weighted* mean, where each
session's rate is weighted by how many items it handled — and the gap grows
with how uneven the group sizes are.

Pushed far enough, the two can point in opposite directions. That is **Simpson's
paradox**: a treatment can look better than another in every single subgroup and
worse overall, purely because the subgroups are different sizes. It is not a
trick or a rare curiosity; it has shown up in university admissions data and in
clinical trials, and the arithmetic behind it is exactly the arithmetic in
TODO 7. Whenever you are about to average something that is already a ratio,
stop and ask what you want each vote to represent.

</details>

<details>
<summary>Under the hood — what NaN actually is, and why one gap changes a column's type</summary>

The missing volunteer-hours cell is not empty. It holds `NaN`, "not a number",
a specific bit pattern the IEEE-754 floating-point standard reserves to mean
"no answer here". It has a strange and useful property: it is not equal to
anything, including itself. `float("nan") == float("nan")` is `False`, which is
precisely why you write `df.isna()` and never `df == None`.

That is also why `items_in` is `int64` while `volunteer_hours` is `float64`
even though both columns look like plain numbers. NumPy's integer types have no
spare bit pattern to spend on "missing" — every one of the 2⁶⁴ patterns is
already a valid integer. Floats have `NaN` for free. So the moment one value
goes missing from a would-be integer column, pandas quietly promotes the whole
column to float, and that is where the trailing `.0` on your counts comes from.

Modern pandas offers nullable dtypes — `Int64` with a capital I, backed by a
separate mask of which values are present — that keep integers as integers with
gaps allowed. They are worth knowing about and are not the default, which is
why the column in front of you is a float.

</details>

<details>
<summary>Under the hood — why a notebook can pass for you and fail for everyone else</summary>

A notebook is not a program. It is a live Python process — the **kernel** — with
a document sitting next to it, and the numbers in the square brackets to the
left of each cell are the order you actually ran things in, which need not
match the order they appear on screen. Every cell you ran and then edited, every
variable you defined in a cell you later deleted, is still in that kernel's
memory.

This is why "restart the kernel and Run All Cells" is not a ritual. It is the
only run that proves the document is the program. Plenty of published notebooks
execute `[1]`, `[2]`, `[7]`, `[3]` and cannot be reproduced by anyone,
including the person who wrote them, a week later.

The same fact explains the plotting rule. In a notebook, matplotlib's default
setup draws under each cell automatically, so `plt.show()` looks unnecessary and
`savefig` looks optional. Outside one — in a script, on a build server, in a
container — there is no place to draw and no window to open, and the file on
disk is the only artifact that survives. Writing the notebook as if it were a
script, saving every figure explicitly, is what makes it portable.

</details>

## Acceptance checklist

The project is worth twenty-five points. These are the same criteria, phrased
as things you can check.

- [ ] Restart the kernel and Run All Cells: every cell executes, top to bottom,
      with no traceback. **(5)**
- [ ] All six required sections are present, in order, as markdown headers.
      **(3)**
- [ ] The cleaning step is documented — a reader can see which dtype changed,
      which gap you filled, and why you filled rather than dropped it. **(3)**
- [ ] Three charts, each with a title, both axis labels including units, and a
      legend where there is more than one series. **(6)**
- [ ] At least two non-trivial aggregations. **(3)**
- [ ] The findings sentence is specific and quantitative, and does not claim a
      cause it cannot show. **(3)**
- [ ] `requirements.txt` names every package you imported, each with a pinned
      version. **(2)**
- [ ] `figures/main.png` exists, and is recreated after you delete it and rerun.
- [ ] `findings.md` answers the three questions, and every claim in it carries a
      number from the notebook.
- [ ] No `TODO` comments are left anywhere in the notebook.
- [ ] Committed and pushed:

      ```bash
      git add analysis.ipynb requirements.txt findings.md figures/main.png
      git commit -m "feat(week-13): dataset analysis mini-project"
      git push
      ```

## Stretch

- **Streamlit** — wrap the notebook in a [Streamlit](https://streamlit.io/) app
  with one dropdown that re-filters a chart, and deploy it free at
  <https://streamlit.io/cloud>. **This unlocks Week 14 bonus credit.**
- **A second dataset** — merge one in, joined on a shared key. World Bank GDP
  against COVID case counts is a good first join.
- **A predictive column** — split the data on a date, train a simple
  scikit-learn model on the past, evaluate it on the future. You do not need
  this for Week 13; it is a preview of Week 14.
- **Parquet** — convert your CSV to Parquet and benchmark the read speed both
  ways. Then look at the file sizes.
- **Read it cold** — this is the first thing in the course you can hand to a
  stranger. Before you call it finished, open it as that stranger would, top to
  bottom, and see whether the question in Cell 1 gets an answer by Cell 17.

That is Week 13. Next week takes the cleaned DataFrame straight into
scikit-learn:
[Week 14 — Intro to AI & Machine Learning](../../week-14-intro-ai-ml/README.md).
