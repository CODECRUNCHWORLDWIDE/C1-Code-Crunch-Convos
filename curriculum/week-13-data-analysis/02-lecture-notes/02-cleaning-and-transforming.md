# Lecture 2 — Cleaning & Transforming Data

In Lecture 1 you learned how to *load* and *look at* a dataset. In real
work, that is usually the easy part. The next 80% of your time goes to
**cleaning**: fixing missing values, picking the rows that matter,
converting types, and building new columns that answer the question you
actually care about. This lecture covers the pandas tools that handle those
jobs. Every snippet below assumes you have run the canonical imports:

```python
import numpy as np
import pandas as pd
```

We will use the small `tips` dataset (a record of restaurant tips, included
with seaborn) for examples. If you don't have seaborn installed, the same
data is in `exercises/exercise-02-load-and-inspect.ipynb`.

```python
import seaborn as sns
df = sns.load_dataset("tips")
df.head()
```

## 1. Selecting Columns

The most common operation in pandas is "give me one or more columns".

```python
df["total_bill"]           # one column → a Series
df[["total_bill", "tip"]]  # two columns → a DataFrame
```

The second form uses a *list* of column names. The double brackets confuse
beginners: the outer brackets are the indexing operation, the inner brackets
are a Python list literal. `df["total_bill", "tip"]` (without inner brackets)
is a syntax error.

You can also access columns as attributes — `df.total_bill` — but only when
the column name is a valid Python identifier (no spaces, no leading
numbers). Stick to bracket notation in scripts; it always works.

## 2. Selecting Rows: `.loc` vs `.iloc`

pandas has two row-selection accessors that you will use constantly.

- **`.loc`** selects by **label** (the index value or a column name).
- **`.iloc`** selects by **integer position** (0-indexed, like a list).

```python
df.iloc[0]              # first row (Series)
df.iloc[0:5]            # first 5 rows (DataFrame)
df.iloc[0, 2]           # first row, third column (single value)
df.iloc[:, 1:3]         # all rows, columns at positions 1 and 2

df.loc[10]              # row whose index label is 10
df.loc[10:15]           # rows with labels 10 through 15 (inclusive!)
df.loc[10, "tip"]       # value at row label 10, column "tip"
df.loc[:, "tip":"sex"]  # all rows, columns "tip" through "sex"
```

Two surprises worth memorizing:

1. **`.loc` slices are inclusive** on both ends — `df.loc[10:15]` returns
   six rows. `.iloc[10:15]` returns five, like normal Python slicing.
2. Plain `df[0:5]` works and selects *rows* by position. It is the only
   case where `df[...]` selects rows rather than columns. Stick to
   `.iloc` or `.loc` to avoid the ambiguity.

## 3. Boolean Masks (Filtering)

To keep only rows that satisfy a condition you build a **boolean mask** — a
Series of `True`/`False` values — and pass it to the DataFrame.

```python
mask = df["total_bill"] > 30
big = df[mask]
```

You can inline it:

```python
df[df["total_bill"] > 30]
```

Combine conditions with `&` (and), `|` (or), and `~` (not). **You must
parenthesize each clause**, because `&` has lower precedence than `>`.

```python
df[(df["total_bill"] > 30) & (df["smoker"] == "Yes")]
df[(df["day"] == "Sat") | (df["day"] == "Sun")]
df[~(df["sex"] == "Male")]
```

For membership tests, `isin` is shorter than chained `|`:

```python
df[df["day"].isin(["Sat", "Sun"])]
```

For "between two values", `between` is built in:

```python
df[df["total_bill"].between(20, 30)]
```

If you find yourself writing long boolean chains, `df.query` reads almost
like English:

```python
df.query("total_bill > 30 and smoker == 'Yes'")
```

## 4. Sorting

```python
df.sort_values("total_bill")                       # ascending
df.sort_values("total_bill", ascending=False)      # descending
df.sort_values(["day", "total_bill"])              # by day then bill
df.sort_index()                                    # by row index
```

`sort_values` returns a new DataFrame. To sort in place, pass
`inplace=True`, but most pandas style guides discourage it — chaining is
clearer.

## 5. Missing Data

Missing values in pandas appear as `NaN` (a special floating-point value),
`NaT` (for missing timestamps), or `pd.NA` (newer, type-agnostic). They are
*not* the Python `None`, although pandas treats `None` as missing in object
columns.

### Detecting missing values

```python
df.isna()              # boolean DataFrame, True where missing
df.isna().sum()        # missing per column
df.isna().sum().sum()  # missing total
df["tip"].notna()      # the inverse
```

A common one-liner to see *only columns that have missing values*:

```python
missing = df.isna().sum()
missing[missing > 0]
```

### Dropping missing values

`dropna` removes rows with any missing values:

```python
df.dropna()                           # drop rows with any NaN
df.dropna(subset=["tip"])             # only consider the tip column
df.dropna(axis=1)                     # drop columns instead of rows
df.dropna(thresh=5)                   # keep rows with at least 5 non-NaN
```

### Filling missing values

`fillna` fills missing values with something useful:

```python
df["tip"].fillna(0)                          # constant
df["tip"].fillna(df["tip"].mean())           # column mean
df["tip"].fillna(method="ffill")             # forward fill (previous value)
df["tip"].fillna(method="bfill")             # backward fill (next value)
df.fillna({"tip": 0, "size": 1})             # different fill per column
```

For time series, `interpolate` is often better than `fillna` because it
interpolates linearly (or with another method) between known values:

```python
df["price"].interpolate(method="linear")
```

### Choosing between drop and fill

There is no universal rule. Some guidance:

- If the missing rate is small (< 1%) and rows are independent: **drop**.
- If a column is mostly missing (> 50%): **drop the column**.
- For continuous numeric columns with a few gaps: **fill** with mean or
  median.
- For categorical columns: **fill** with `"unknown"` or the mode.
- For time series: **interpolate**, then drop any remaining edges.

## 6. Type Conversions

pandas guesses dtypes when it reads a file. The guesses are usually right,
but you will sometimes need to fix them.

```python
df["size"] = df["size"].astype("int64")
df["total_bill"] = df["total_bill"].astype("float64")
df["smoker"] = df["smoker"].astype("category")    # saves memory
df["day"] = df["day"].astype("string")
df["joined_at"] = pd.to_datetime(df["joined_at"])
df["price"] = pd.to_numeric(df["price"], errors="coerce")   # bad values → NaN
```

`pd.to_datetime` and `pd.to_numeric` are forgiving converters. The
`errors="coerce"` argument turns anything that cannot be parsed into `NaN`
or `NaT`, which is usually what you want when reading messy data.

The **`category`** dtype is a small but important optimisation: it stores
strings once and replaces them with integer codes. For a column with a few
distinct values across millions of rows (`"M"`/`"F"`, country codes, etc.),
converting to category can cut memory use by 90% and speed up groupbys.

## 7. Creating New Columns

You create a new column by assigning to it:

```python
df["tip_pct"] = df["tip"] / df["total_bill"] * 100
df["big_tipper"] = df["tip_pct"] > 20
```

The right-hand side is vectorized — pandas broadcasts the operation across
every row. You almost never need a `for` loop.

`assign` does the same thing but returns a new DataFrame, which is handy
for method chains:

```python
result = (
    df
    .assign(tip_pct=lambda d: d["tip"] / d["total_bill"] * 100)
    .assign(big_tipper=lambda d: d["tip_pct"] > 20)
    .query("big_tipper")
    .sort_values("tip_pct", ascending=False)
)
```

The `lambda d: ...` is so that `assign` sees the DataFrame *after* the
previous step's columns have been added.

## 8. Applying Functions

When vectorization is not enough — say, you want to call a custom Python
function on every value — use `apply` or `map`.

```python
def grade(score: float) -> str:
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    return "F"

df["letter"] = df["score"].apply(grade)
```

For multi-column logic, `apply(axis=1)` passes the whole row as a Series:

```python
df["bill_plus_tip"] = df.apply(
    lambda row: row["total_bill"] + row["tip"], axis=1
)
```

`apply` with `axis=1` is slow on large DataFrames — it falls back to a
Python loop. Always reach for vectorized arithmetic first, and only use
`apply(axis=1)` when there is no clean vectorized form.

For dictionary-style replacement on a single column, `map` is faster than
`apply`:

```python
day_codes = {"Thur": 4, "Fri": 5, "Sat": 6, "Sun": 7}
df["day_num"] = df["day"].map(day_codes)
```

`replace` is also useful for value substitutions:

```python
df["smoker"] = df["smoker"].replace({"Yes": True, "No": False})
```

## 9. String Operations

When a column's dtype is `object` (strings), the `.str` accessor exposes the
familiar Python string methods *vectorized* across the whole column.

```python
df["name"].str.lower()
df["name"].str.strip()
df["name"].str.startswith("M")
df["email"].str.contains("@gmail.com")
df["email"].str.split("@").str[1]      # everything after the @
df["name"].str.len()
df["name"].str.replace("Mr.", "", regex=False)
```

`str.contains` returns a boolean Series, which slots directly into a filter:

```python
df[df["email"].str.contains("@gmail", na=False)]
```

The `na=False` argument tells pandas to treat missing emails as "no match"
rather than `NaN`, which would break the boolean mask.

For pattern extraction, `extract` with a regex is the cleanest tool:

```python
df["area"] = df["phone"].str.extract(r"^\((\d{3})\)")
```

## 10. Renaming, Dropping, and Reordering

```python
df = df.rename(columns={"total_bill": "bill"})
df = df.drop(columns=["smoker"])
df = df.drop(index=[0, 1, 2])
df = df[["bill", "tip", "day"]]      # reorder by listing
```

`rename` with a dict only changes the columns you mention — others are left
alone. To uppercase every column name:

```python
df.columns = [c.upper() for c in df.columns]
```

## 11. Duplicates

Duplicate rows creep into real datasets all the time — a user double-clicks
"submit", an ETL job runs twice, two source systems agree on a record. The
tools to find and remove them are simple:

```python
df.duplicated()            # boolean Series
df.duplicated().sum()
df.drop_duplicates()       # remove exact duplicate rows
df.drop_duplicates(subset=["email"], keep="first")
```

By default, `duplicated()` marks every row after the first occurrence as a
duplicate. Pass `keep="last"` to flip that, or `keep=False` to mark *every*
row that has a copy. The `subset` argument lets you decide which columns
define "the same" — for a customer table, `subset=["email"]` is usually
what you want.

A common mistake: calling `drop_duplicates()` on a frame and being
surprised that nothing changed. That usually means the duplicates are not
**exactly** identical — leading/trailing whitespace, a different case, or
one extra space inside a string is enough to make pandas see them as
different. Run `df["email"].str.lower().str.strip()` first if you suspect
this.

## 12. Sampling, Heads, and Tails

When you have ten million rows, you cannot eyeball the whole frame. Three
tools help:

```python
df.sample(10)              # random 10 rows
df.sample(frac=0.01)       # random 1% of rows
df.nlargest(5, "amount")   # top 5 by amount
df.nsmallest(5, "amount")  # bottom 5 by amount
```

`nlargest` and `nsmallest` are much faster than `sort_values(...).head(5)`
on big frames because they only need to maintain a small heap, not sort
everything.

## 13. A Realistic Cleaning Pipeline

Here is the kind of code you will write for almost every dataset you touch
this week. Read it slowly — every line is a tool from this lecture.

```python
def load_and_clean(path: str) -> pd.DataFrame:
    """Load a sales CSV and return a tidy DataFrame."""
    df = pd.read_csv(path, parse_dates=["order_date"])

    # standardise column names
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    # drop obvious junk rows
    df = df.dropna(subset=["order_id"])
    df = df.drop_duplicates(subset=["order_id"])

    # fix types
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"]    = pd.to_numeric(df["price"], errors="coerce")
    df["category"] = df["category"].astype("category")

    # fill missing prices with the category median
    df["price"] = df.groupby("category")["price"].transform(
        lambda s: s.fillna(s.median())
    )

    # derived columns
    df["revenue"]    = df["quantity"] * df["price"]
    df["year_month"] = df["order_date"].dt.to_period("M")

    # final filter — drop rows that still have missing critical data
    df = df.dropna(subset=["quantity", "price"])

    return df
```

Notice how the function is just a sequence of small, named transformations.
That is the pandas style: each step does one thing, the data flows top to
bottom, and a reader can stop at any line and ask `df.head()`.

## 14. The Copy-vs-View Trap (and `SettingWithCopyWarning`)

Sooner or later — usually within your first ten hours of pandas — you will
hit this warning:

```text
SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
```

It looks scary; it usually is harmless; and you should still fix it. The
root cause is *chained indexing*:

```python
df[df["score"] > 60]["letter"] = "P"   # bad: assignment to a copy
```

The expression `df[df["score"] > 60]` returns a *new* DataFrame, and
assigning to a column of that new frame does not mutate `df`. Use `.loc`
with both axes specified instead:

```python
df.loc[df["score"] > 60, "letter"] = "P"   # good
```

This idiom — "boolean mask in `.loc` row position, target column on the
right" — is the single most useful pattern for conditional assignment.
Memorize it.

If you want to work with a slice safely and *not* mutate the original,
make the copy explicit:

```python
sub = df[df["score"] > 60].copy()
sub["letter"] = "P"
```

`copy()` ends the ambiguity — pandas knows you mean a new frame.

## 15. Recap

You can now:

- Select rows by label (`.loc`), by position (`.iloc`), and by condition
  (boolean masks).
- Combine conditions with `&`, `|`, `~` and use `isin`, `between`, and
  `query` for cleaner code.
- Sort with `sort_values` and `sort_index`.
- Detect missing data with `isna`, and either `dropna` or `fillna` as
  appropriate.
- Convert columns with `astype`, `pd.to_datetime`, and `pd.to_numeric`.
- Build new columns by assignment or `assign`, and use `apply`/`map` for
  custom logic.
- Use the `.str` accessor for vectorized string work.

Next lecture: **aggregation and plotting**. You will turn cleaned data into
summaries and charts — the deliverables your future colleagues will
actually read.

## Further Reading

- pandas User Guide — "Indexing and selecting data":
  <https://pandas.pydata.org/docs/user_guide/indexing.html>
- pandas User Guide — "Working with missing data":
  <https://pandas.pydata.org/docs/user_guide/missing_data.html>
- pandas User Guide — "Working with text data":
  <https://pandas.pydata.org/docs/user_guide/text.html>
