# Lecture 3 — Aggregation & Plotting

Loading and cleaning data gets you to the starting line. **Aggregation** —
summarizing a million rows into a few meaningful numbers — and
**visualization** — turning those numbers into pictures — are what turns
data into insight. This lecture covers groupby, pivot tables, merges, and
the two plotting interfaces you will see most often: raw matplotlib and the
pandas `.plot` shortcut.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

## 1. `groupby`: Split-Apply-Combine

The single most useful pattern in data analysis is **split-apply-combine**:

1. **Split** the DataFrame into groups based on a key.
2. **Apply** a function to each group (sum, mean, count, custom).
3. **Combine** the per-group results into a new DataFrame.

In pandas this is one call:

```python
df.groupby("day")["total_bill"].mean()
```

That line splits the tips dataset by `day`, takes the `total_bill` column
of each group, and returns the mean. The result is a Series indexed by day:

```text
day
Thur    17.682742
Fri     17.151579
Sat     20.441379
Sun     21.410000
Name: total_bill, dtype: float64
```

### Multiple aggregations at once

`agg` accepts a list (same metric on every selected column), a dict
(different metric per column), or named tuples (modern, recommended):

```python
df.groupby("day").agg(
    avg_bill=("total_bill", "mean"),
    total_tip=("tip", "sum"),
    count=("tip", "size"),
)
```

`size` counts rows including NaN; `count` counts non-null values only.

### Multi-key groupby

You can group by more than one column. The result has a **MultiIndex**:

```python
df.groupby(["day", "time"])["total_bill"].mean()
```

`reset_index()` flattens a MultiIndex back into regular columns when you
need to write the result to CSV or pass it to a plotting function.

### `transform`: per-row group result

`agg` collapses each group into one row. `transform` returns a result the
same shape as the input, with the group's value broadcast to every row.

```python
df["avg_bill_for_day"] = df.groupby("day")["total_bill"].transform("mean")
df["bill_vs_day_avg"]  = df["total_bill"] - df["avg_bill_for_day"]
```

That is how you center a value on its group's mean — a step that comes up
constantly in feature engineering and statistical tests.

### Filtering groups

`filter` keeps or drops whole groups based on a condition:

```python
# keep only days with average bill above 20
df.groupby("day").filter(lambda g: g["total_bill"].mean() > 20)
```

## 2. Pivot Tables

A **pivot table** rearranges a long, narrow table into a wider one where
one variable becomes columns and another becomes rows. Spreadsheet users
will recognise it immediately.

```python
df.pivot_table(
    index="day",
    columns="sex",
    values="total_bill",
    aggfunc="mean",
)
```

```text
sex      Male    Female
day
Thur    18.71    16.72
Fri     19.86    14.15
Sat     20.80    19.68
Sun     21.89    19.87
```

Each cell is the mean `total_bill` for that day-sex combination.
`pivot_table` defaults to `mean` but accepts any aggregation:

```python
df.pivot_table(index="day", columns="smoker", values="tip",
               aggfunc=["sum", "mean", "count"])
```

`fill_value=0` is helpful when some combinations have no rows.

For a simpler tabulation of how many rows fall into each combination, use
`pd.crosstab`:

```python
pd.crosstab(df["day"], df["sex"])
```

## 3. Merging and Joining DataFrames

Most real analyses pull data from more than one source. pandas has three
combining functions: `merge`, `concat`, and `join`.

### `merge` (the SQL-style join)

Suppose you have an `orders` table and a `customers` table:

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer_id": [10, 11, 10, 12],
    "amount": [50, 75, 30, 120],
})
customers = pd.DataFrame({
    "customer_id": [10, 11, 12, 13],
    "name": ["Ada", "Linus", "Grace", "Tim"],
})

joined = orders.merge(customers, on="customer_id", how="left")
```

The `how` argument matches SQL exactly:

- `"inner"` — keep only matching rows in both (default).
- `"left"` — keep all rows from the left frame.
- `"right"` — keep all rows from the right frame.
- `"outer"` — keep all rows from either side.

When the join column has different names on each side:

```python
orders.merge(customers, left_on="cust_id", right_on="customer_id")
```

When the join key is the index, use `left_index=True` or `right_index=True`.

### `concat` (stack rows or columns)

`concat` glues DataFrames together along an axis without matching keys.

```python
all_sales = pd.concat([jan, feb, mar], ignore_index=True)
side_by_side = pd.concat([df1, df2], axis=1)
```

`ignore_index=True` rebuilds a fresh `0..n` index — usually what you want
after stacking files of monthly sales.

## 4. Plotting: Why Two Interfaces?

There are two ways to make a plot in this ecosystem:

1. **matplotlib directly** — verbose, but gives complete control.
2. **pandas `.plot`** — a thin wrapper around matplotlib; great for quick
   exploratory charts.

Almost every pandas plot is matplotlib under the hood, so anything you
learn about one transfers to the other. You will use `.plot` for fast
iteration and drop down to matplotlib when you need to polish a figure.

A pattern that suits beginners: start with `.plot`; if you need to label,
resize, or annotate, capture the returned `ax` and call matplotlib methods
on it.

```python
ax = df["total_bill"].plot.hist(bins=20)
ax.set_title("Distribution of total bills")
ax.set_xlabel("Total bill ($)")
plt.tight_layout()
plt.savefig("bills.png", dpi=150)
```

## 5. The matplotlib Mental Model

A matplotlib chart is built from two layers:

- **Figure** — the entire image (one window, one PNG).
- **Axes** — one set of x/y axes inside the figure. You can have multiple
  axes per figure to make grids of plots.

The explicit, recommended way:

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("My first plot")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()
```

If you just call `plt.plot`, `plt.title`, etc., matplotlib silently creates
a figure and axes for you — convenient, but the explicit `fig, ax` form
makes it obvious how to add a second subplot later.

### The plot types you will use this week

```python
ax.plot(x, y)         # line
ax.bar(x, y)          # vertical bar
ax.barh(x, y)         # horizontal bar
ax.scatter(x, y)      # dots
ax.hist(values)       # histogram
ax.boxplot(values)    # box-and-whisker
```

### Customising

```python
ax.set_title("Sales by month")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.legend(["Product A", "Product B"])
ax.grid(True, alpha=0.3)
ax.tick_params(axis="x", rotation=45)
```

### Saving figures

```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
```

`dpi=150` is a good balance between file size and crispness. `bbox_inches=
"tight"` trims the surrounding whitespace.

`plt.show()` displays the figure interactively; in a notebook it is
optional because the result is shown automatically.

## 6. pandas `.plot`: The Shortcut

Every DataFrame and Series has a `.plot` method that wraps matplotlib for
you. The signature is `.plot(kind="line", ...)` but most chart types have
their own shortcut:

```python
df["total_bill"].plot()                 # line plot of one column
df["total_bill"].plot.hist(bins=20)     # histogram
df["total_bill"].plot.box()             # box plot
df.plot.scatter(x="total_bill", y="tip")
df.groupby("day")["total_bill"].mean().plot.bar()
```

When the DataFrame has multiple numeric columns, `.plot()` makes one line
per column on the same axes — handy for time series with several
measurements.

```python
monthly = df.groupby("month")[["A", "B", "C"]].sum()
monthly.plot(figsize=(10, 5), title="Monthly sales by product")
```

The `.plot` method returns the underlying `Axes` object so you can keep
customizing:

```python
ax = monthly.plot()
ax.set_ylabel("Revenue ($)")
ax.legend(loc="upper left")
```

## 7. A Worked Example

Here is the kind of mini-report you will produce in this week's mini-
project.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("tips")

# Aggregate
summary = (
    df
    .groupby(["day", "time"], observed=True)
    .agg(avg_bill=("total_bill", "mean"),
         avg_tip=("tip", "mean"),
         n=("tip", "size"))
    .reset_index()
)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

(df.groupby("day", observed=True)["total_bill"]
   .mean()
   .plot.bar(ax=axes[0], color="#3273dc"))
axes[0].set_title("Average bill by day")
axes[0].set_ylabel("Average bill ($)")

axes[1].scatter(df["total_bill"], df["tip"], alpha=0.6)
axes[1].set_title("Tip vs. bill")
axes[1].set_xlabel("Total bill ($)")
axes[1].set_ylabel("Tip ($)")

fig.tight_layout()
fig.savefig("tips_report.png", dpi=150, bbox_inches="tight")
```

Two panels side by side, both labelled, saved at print quality, all in under
20 lines of code.

## 8. seaborn (Optional but Recommended)

seaborn is a higher-level plotting library that sits on top of matplotlib.
Its defaults are prettier, and it understands DataFrames natively, so you
can pass column *names* rather than arrays.

```python
import seaborn as sns
sns.set_theme()

sns.barplot(data=df, x="day", y="total_bill", hue="sex")
sns.scatterplot(data=df, x="total_bill", y="tip", hue="time")
sns.histplot(data=df, x="tip", bins=20)
sns.boxplot(data=df, x="day", y="total_bill")
```

The killer features are `sns.pairplot(df)` (a grid of scatterplots across
every numeric column) and `sns.heatmap(df.corr())` (a correlation matrix
in colour). Both are one-liners that look much better than the matplotlib
equivalents.

You do **not** have to use seaborn — pandas `.plot` and matplotlib alone
cover everything in this week's deliverables. seaborn is for the day you
decide your charts deserve to look nicer.

## 9. Subplots: Multiple Charts on One Figure

A single image with several panels is often the right way to present a
mini-analysis. matplotlib's `plt.subplots(rows, cols)` returns a grid of
axes you can fill independently.

```python
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

df["total_bill"].plot.hist(ax=axes[0, 0], bins=20)
axes[0, 0].set_title("Bill distribution")

df["tip"].plot.hist(ax=axes[0, 1], bins=20, color="seagreen")
axes[0, 1].set_title("Tip distribution")

axes[1, 0].scatter(df["total_bill"], df["tip"], alpha=0.5)
axes[1, 0].set_title("Tip vs. bill")

(df.groupby("day", observed=True)["total_bill"]
   .mean()
   .plot.bar(ax=axes[1, 1]))
axes[1, 1].set_title("Average bill by day")

fig.suptitle("Tips dataset — quick look", fontsize=14)
fig.tight_layout()
```

`axes` is a 2-D NumPy array of `Axes` objects when both `nrows` and `ncols`
are above 1; it is a 1-D array when only one of them is, and a single
`Axes` when both are 1. If you find this annoying, pass `squeeze=False` and
you will always get a 2-D array.

`fig.suptitle` puts a single overall title on the whole figure;
`fig.tight_layout` then adjusts spacing so the titles do not overlap.

## 10. Date-aware Plotting

When your DataFrame index is a `DatetimeIndex`, matplotlib draws time on
the x-axis automatically, with sensible date tick labels.

```python
df["date"] = pd.to_datetime(df["date"])
ts = df.set_index("date")
ts["revenue"].plot(figsize=(10, 4))
```

Two helpers you will use often with time series:

```python
ts["revenue"].resample("M").sum().plot.bar()    # monthly totals
ts["revenue"].rolling(7).mean().plot()          # 7-day rolling mean
```

`resample` is `groupby` for time; `rolling` is `groupby` for sliding
windows. Combined with the date-aware x-axis, they make it trivial to turn
noisy daily data into a clean trend chart in three lines.

## 11. Plot Hygiene

A short checklist that distinguishes a good chart from a bad one:

- **Title** — what is the chart about?
- **Axis labels with units** — what does each axis mean?
- **Legend** — if there is more than one series.
- **Sensible scale** — don't let one outlier flatten the rest.
- **Color choice** — be consistent across charts in the same report. Avoid
  red/green together (colour blindness).
- **`tight_layout()` or `bbox_inches="tight"`** — keeps labels from
  getting clipped.

A chart that is not labelled is not a chart, it is decoration. Spend ten
extra seconds on titles and axis labels every time.

## 12. Working in a Notebook

Jupyter notebooks render matplotlib figures inline by default. You can use
the magic `%matplotlib inline` to be explicit. Each cell ending in a plot
call shows the figure under the cell. To save and display:

```python
fig.savefig("out.png", dpi=150)
fig
```

The bare `fig` on the last line re-renders the figure as the cell's
output. This is the easiest way to keep a screenshot of your finished chart
inside the notebook.

## 13. Recap

You can now:

- Use `groupby` and `agg` to compute per-group summaries.
- Use `transform` to broadcast a group result back to every row.
- Combine DataFrames with `merge` (SQL-style joins) and `concat` (stacking).
- Reshape with `pivot_table` and `crosstab`.
- Build matplotlib charts with the explicit `fig, ax = plt.subplots()`
  pattern.
- Use the pandas `.plot` shortcut for quick exploration.
- Save figures with `savefig`.
- Optionally use seaborn for prettier defaults.

You have everything you need for the mini-project: load, clean, aggregate,
visualize, conclude. Go make something interesting.

## Further Reading

- pandas User Guide — "Group by: split-apply-combine":
  <https://pandas.pydata.org/docs/user_guide/groupby.html>
- pandas User Guide — "Merge, join, concatenate and compare":
  <https://pandas.pydata.org/docs/user_guide/merging.html>
- matplotlib — "Pyplot tutorial":
  <https://matplotlib.org/stable/tutorials/introductory/pyplot.html>
- seaborn — "Tutorial":
  <https://seaborn.pydata.org/tutorial.html>
