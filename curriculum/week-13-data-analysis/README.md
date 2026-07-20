# Week 13 — Data Analysis with pandas

Welcome to **Week 13** of **Code Crunch Convos**! After twelve weeks of
building Python fluency — from variables and functions to APIs, databases,
testing, and automation — you are now ready to turn raw data into
understanding. This week introduces the two libraries that define modern
Python data work: **NumPy** for fast numerical arrays and **pandas** for
spreadsheet-like tables called DataFrames. You will also meet **matplotlib**
(and, optionally, seaborn) for charts, and the **Jupyter notebook**
environment that practicing analysts and data scientists use every day. By
the end of the week you will have loaded real datasets from CSV, JSON, Excel,
and SQL; cleaned messy values; grouped, joined, and pivoted tables; and
produced at least three publication-ready charts in a Jupyter notebook for
your mini-project.

## Learning Objectives

By the end of this week, you will be able to:

- **Explain** what NumPy arrays are and why they are dramatically faster than
  Python lists for numerical work.
- **Create** and **manipulate** pandas `Series` and `DataFrame` objects from
  Python dictionaries, lists, and external files.
- **Load** datasets with `read_csv`, `read_json`, `read_excel`, and
  `read_sql`, choosing sensible options for each.
- **Inspect** tabular data with `head`, `tail`, `info`, `describe`, `dtypes`,
  and `shape` to form a quick mental model of any new dataset.
- **Select** rows and columns using bracket notation, `.loc`, `.iloc`, and
  boolean masks.
- **Clean** data by handling missing values (`isna`, `fillna`, `dropna`),
  converting types, and applying functions to columns.
- **Aggregate** data with `groupby`, multiple aggregations, and pivot tables.
- **Combine** datasets with `merge`, `concat`, and `join`.
- **Plot** line, bar, scatter, and histogram charts with both matplotlib and
  the pandas `.plot` shortcut, and **save** them as PNG files.
- **Work** inside a Jupyter notebook: cells, markdown, magic commands, and
  exporting results.

## Prerequisites

You should have completed Weeks 1–12 of Code Crunch Convos, or be
comfortable with the topics they cover. In particular, this week leans on:

- **Week 6 — File I/O & Exceptions**: reading and writing files; `with open(...)`.
- **Week 8 — APIs & JSON**: dictionaries, lists, JSON parsing.
- **Week 10 — Databases & SQL**: `SELECT`, `WHERE`, `GROUP BY`, joins.
- **Week 4 — Functions & Modules**: writing reusable functions and importing
  third-party packages.

You also need a working virtual environment (Week 1) and the ability to
install packages with `pip`.

## Topics Covered

- NumPy basics: `ndarray`, vectorization, broadcasting (brief, just enough
  to read pandas internals)
- pandas `Series` and `DataFrame`: indexes, dtypes, axis labels
- Loading data: `read_csv`, `read_json`, `read_excel`, `read_sql`
- Inspecting data: `head`, `tail`, `info`, `describe`, `dtypes`, `shape`,
  `value_counts`
- Selecting data: column access (`df["col"]`), `.loc`, `.iloc`, boolean masks
- Filtering and sorting: `df[df["x"] > 5]`, `sort_values`, `sort_index`
- Missing data: `isna`, `notna`, `fillna`, `dropna`, `interpolate`
- Reshaping and transforming: `apply`, `map`, `assign`, `astype`, `str`
  accessor
- Groupby + aggregation: `groupby`, `agg`, multiple functions, named
  aggregations
- Merging and joining: `merge`, `concat`, `join`
- Pivot tables: `pivot_table`, `crosstab`
- Plotting with matplotlib: figure, axes, line, bar, scatter, histogram
- pandas `.plot` shortcut and customizing: titles, labels, legends
- Saving figures to PNG with `savefig`
- Optional: seaborn for prettier defaults
- Jupyter notebooks: cells, markdown, magic commands (`%timeit`, `%matplotlib
  inline`), exporting

## Weekly Schedule

The schedule below adds up to approximately **36 hours**. Treat it as a
target, not a contract — some sections will click faster, others slower.

| Day       | Focus                                          | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----------|------------------------------------------------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday    | NumPy & pandas basics                          |    2h    |    2h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Tuesday   | Loading, inspecting, selecting                 |    2h    |    2h     |     0h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Wednesday | Cleaning, filtering, missing data              |    2h    |    1h     |     1h     |    0.5h   |   1h     |     0h       |    0.5h    |     6h      |
| Thursday  | Groupby, merge, pivot                          |    2h    |    1h     |     1h     |    0.5h   |   1h     |     1h       |    0h      |     6.5h    |
| Friday    | Matplotlib & pandas plotting                   |    1h    |    1h     |     0h     |    0.5h   |   1h     |     2h       |    0h      |     5.5h    |
| Saturday  | Mini-project deep work                         |    0h    |    0h     |     0h     |    0h     |   0h     |     5h       |    0h      |     5h      |
| Sunday    | Quiz, write findings, polish                   |    0h    |    0h     |     0h     |    1h     |   0h     |     0h       |    0h      |     1h      |
| **Total** |                                                | **9h**   | **7h**    | **2h**     | **3.5h**  | **5h**   |   **8h**     |   **1h**   |  **36h**    |

## How to Navigate This Week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview (you are here) |
| [resources.md](./resources.md) | Official docs, free books, dataset catalogues |
| [lecture-notes/01-numpy-and-pandas-basics.md](./lecture-notes/01-numpy-and-pandas-basics.md) | NumPy arrays, vectorization, broadcasting; pandas Series and DataFrame |
| [lecture-notes/02-cleaning-and-transforming.md](./lecture-notes/02-cleaning-and-transforming.md) | Selecting, filtering, sorting, missing data, type conversions, string ops |
| [lecture-notes/03-aggregation-and-plotting.md](./lecture-notes/03-aggregation-and-plotting.md) | Groupby, pivot tables, merging, matplotlib & pandas `.plot` |
| [exercises/README.md](./exercises/README.md) | Index of short coding exercises |
| [exercises/exercise-01-numpy-arrays.py](./exercises/exercise-01-numpy-arrays.py) | Create arrays, vector math, broadcasting |
| [exercises/exercise-02-load-and-inspect.ipynb](./exercises/exercise-02-load-and-inspect.ipynb) | Jupyter notebook: load a small dataset, inspect it |
| [exercises/exercise-03-filter-and-sort.py](./exercises/exercise-03-filter-and-sort.py) | Filter passing grades and sort by score |
| [exercises/exercise-04-groupby.py](./exercises/exercise-04-groupby.py) | Sales by category — total + average |
| [exercises/exercise-05-plot.py](./exercises/exercise-05-plot.py) | Monthly totals bar chart, saved as PNG |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-titanic-eda.md](./challenges/challenge-01-titanic-eda.md) | Exploratory data analysis on the Titanic dataset |
| [challenges/challenge-02-time-series.md](./challenges/challenge-02-time-series.md) | Resample a time series and plot a rolling mean |
| [quiz.md](./quiz.md) | 10 multiple-choice questions |
| [homework.md](./homework.md) | Six practice problems for the week |
| [mini-project/README.md](./mini-project/README.md) | Full spec for the dataset analysis notebook |
| [mini-project/starter.ipynb](./mini-project/starter.ipynb) | Scaffolded Jupyter notebook to work from |
| [mini-project/requirements.txt](./mini-project/requirements.txt) | Python dependencies for the mini-project |

## Stretch Goals

If you finish early and want to push further, try any of the following:

- **Build a Streamlit dashboard** that wraps your mini-project notebook into
  an interactive web app — see <https://streamlit.io/>. You can deploy it
  free at <https://streamlit.io/cloud>.
- Learn **seaborn** for higher-level statistical plots
  (<https://seaborn.pydata.org/>). Try `sns.pairplot` and `sns.heatmap` on
  your dataset.
- Read about **method chaining** and rewrite a messy pandas pipeline using
  `.pipe()` and `.assign()` for clarity.
- Explore **`pandas.DataFrame.query`**: a SQL-like filter syntax that some
  analysts prefer over boolean masks for readability.
- Profile a large pandas operation with `%timeit` and compare against
  **Polars** (<https://pola.rs/>) or **DuckDB** (<https://duckdb.org/>).
- Convert your mini-project to a **parquet** file and compare its size and
  read speed against the CSV.

## Up Next

Continue to [Week 14 — Intro to AI & Machine Learning](../week-14-intro-ai-ml/README.md)
once you have submitted your mini-project notebook and your one-page summary.
You will start applying the same pandas DataFrames you mastered this week to
training your first machine-learning models with scikit-learn.
