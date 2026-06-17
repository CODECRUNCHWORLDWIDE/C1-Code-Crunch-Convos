# Lecture 1 — NumPy & pandas Basics

Welcome to Week 13. For twelve weeks we have written Python programs that
deal with one value, one record, or one file at a time. This week we change
scale: we will manipulate thousands, millions, or even billions of rows of
data at once, using two libraries that have shaped modern Python more than
any others — **NumPy** and **pandas**. This first lecture introduces both of
them. By the end you will know what an `ndarray` is, why pandas is built on
top of NumPy, how to create `Series` and `DataFrame` objects, and how to
inspect a new dataset in under a minute.

## 1. Why NumPy?

Plain Python lists are wonderfully flexible — a single list can hold an
integer, a string, a dictionary, and another list. That flexibility, however,
comes at a price: every element is a full Python object stored somewhere
random in memory, and iterating over a list invokes the interpreter on every
step. When you have ten million numbers, Python loops are too slow.

NumPy solves this with the **`ndarray`**: a contiguous block of memory
holding values of one fixed type (called the **dtype**) — for example,
`int64`, `float64`, or `bool`. Because the data is packed tightly and
typed, operations run in compiled C code, often **10× to 100× faster** than
the equivalent Python loop.

### Installing and importing

```bash
pip install numpy pandas matplotlib jupyter
```

By long-standing convention, you import them with short aliases:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

You will see these three lines at the top of nearly every data-analysis
notebook on the planet.

### Creating arrays

```python
import numpy as np

a = np.array([1, 2, 3, 4])          # 1-D array
b = np.array([[1, 2], [3, 4]])      # 2-D array (matrix)
zeros = np.zeros(5)                  # array of zeros
ones = np.ones((2, 3))               # 2x3 array of ones
seq = np.arange(0, 10, 2)            # 0, 2, 4, 6, 8
lin = np.linspace(0, 1, 5)           # 5 evenly-spaced values from 0 to 1
rand = np.random.default_rng(0).random(4)  # 4 random floats
```

Every array has three important attributes:

```python
a.shape    # (4,)   tuple of dimensions
a.dtype    # int64  the element type
a.ndim     # 1      number of dimensions
```

### Vectorization

The killer feature of NumPy is **vectorization** — applying an operation to
an entire array without writing a Python loop.

```python
prices = np.array([9.99, 19.95, 4.50, 29.99])
with_tax = prices * 1.08              # multiplies every element
total = prices.sum()                  # one number out
average = prices.mean()
```

The same calculation with a Python list would require a list comprehension
or a `for` loop. Vectorized code is shorter, faster, and — once your eye is
trained — easier to read. Try the following timing experiment in a Jupyter
notebook:

```python
%timeit [x * 2 for x in range(1_000_000)]
%timeit np.arange(1_000_000) * 2
```

The NumPy version will be roughly 30–80× faster on a typical laptop.

### Broadcasting

**Broadcasting** is the rule that lets NumPy combine arrays of different but
compatible shapes without copying data. The simplest case: combining an
array with a single number.

```python
np.array([1, 2, 3]) + 10   # array([11, 12, 13])
```

The scalar `10` is "broadcast" to match the shape of the array. The same
rule lets you center a column on its mean in one line:

```python
data = np.array([[10, 20], [30, 40], [50, 60]])
data - data.mean(axis=0)
```

You will rarely write raw broadcasting code as a beginner, but you must
recognize the term — pandas uses it constantly under the hood. For the
formal rules, skim
<https://numpy.org/doc/stable/user/basics.broadcasting.html> when you feel
ready.

## 2. From NumPy to pandas

NumPy gives us fast numeric arrays. **pandas** gives us labelled tables of
mixed types — exactly the spreadsheets and database rows we actually work
with. Internally a pandas object holds NumPy arrays, plus an **index** that
labels rows (and, for DataFrames, an axis labelling columns).

pandas adds three things on top of NumPy that matter for everyday work:

1. **Labels**: you can refer to a column by name (`df["price"]`) rather than
   by integer position.
2. **Mixed types**: one column can be strings, the next floats, the next
   timestamps.
3. **Missing data**: a first-class concept (`NaN`, `NaT`, `pd.NA`) with rich
   helpers to handle it.

## 3. The pandas `Series`

A `Series` is a one-dimensional labelled array — think "a single column
with its row labels".

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"], name="score")
print(s)
# a    10
# b    20
# c    30
# d    40
# Name: score, dtype: int64
```

You can access values by label or by position:

```python
s["b"]      # 20    by label
s.iloc[1]   # 20    by integer position
s.mean()    # 25.0  vectorized math, just like NumPy
s + 5       # adds 5 to every element
```

A `Series` is the building block of a DataFrame: each column is a `Series`,
and rows themselves are `Series` too.

## 4. The pandas `DataFrame`

A `DataFrame` is a two-dimensional labelled table — rows and columns, like
an Excel sheet or a SQL table.

### Creating from a dictionary

The fastest way to build a DataFrame by hand is from a dictionary of equal-
length lists, where each key becomes a column.

```python
data = {
    "name":   ["Ada",   "Linus", "Grace", "Tim"],
    "lang":   ["Python","C",     "COBOL", "Web"],
    "year":   [1843,    1969,    1959,    1989],
    "rating": [9.9,     9.8,     9.5,     9.7],
}
df = pd.DataFrame(data)
print(df)
```

```text
    name    lang   year  rating
0    Ada  Python   1843     9.9
1  Linus       C   1969     9.8
2  Grace   COBOL   1959     9.5
3    Tim     Web   1989     9.7
```

The leftmost column with `0, 1, 2, 3` is the **index** — it is *not* a
column, it is a row label. You can choose your own index:

```python
df = df.set_index("name")
```

### Creating from a list of dicts

When you scrape an API or parse JSON line-by-line you often have a list of
records, each a dict. pandas handles this directly:

```python
records = [
    {"name": "Ada",   "year": 1843, "rating": 9.9},
    {"name": "Linus", "year": 1969, "rating": 9.8},
]
df = pd.DataFrame(records)
```

### Creating from a CSV

In practice you almost never type data into a DataFrame — you load it from
a file or database. The most common loader is `read_csv`:

```python
df = pd.read_csv("data/tips.csv")
```

`read_csv` is the workhorse of pandas. It has more than 50 keyword
arguments. The few you will actually use are:

- `sep=","` — the column separator. Use `"\t"` for TSV files.
- `header=0` — which row is the header. `None` means there is no header row.
- `names=[...]` — supply your own column names.
- `index_col="id"` — use a column as the row index.
- `parse_dates=["date"]` — convert these columns to datetimes.
- `na_values=["NA", "?", "-"]` — treat these strings as missing.
- `dtype={"zip": str}` — force a column to a specific type. Very handy for
  zip codes that start with `0`.
- `nrows=1000` — only read the first 1000 rows (perfect for previewing big
  files).

Other loaders work the same way:

```python
pd.read_json("data/players.json")
pd.read_excel("data/sales.xlsx", sheet_name="Q1")
pd.read_sql("SELECT * FROM orders", con=connection)
```

`read_sql` accepts a database connection — for SQLite, that is a regular
`sqlite3.Connection`. You learned how to create one in Week 10.

### Writing data back out

Every reader has a matching writer. Common ones:

```python
df.to_csv("out.csv", index=False)
df.to_json("out.json", orient="records", indent=2)
df.to_excel("out.xlsx", sheet_name="Result", index=False)
```

`index=False` is the option you will forget most often — without it pandas
writes the row labels as a column, which is rarely what you want.

## 5. Inspecting a New Dataset

The first thing you do with a new DataFrame is *look at it*. There are six
methods you will call hundreds of times this week.

```python
df.head()       # first 5 rows
df.head(20)     # first 20 rows
df.tail()       # last 5 rows
df.shape        # (rows, columns) — an attribute, no parens
df.dtypes       # type of each column
df.info()       # rows, columns, non-null counts, dtypes, memory
df.describe()   # summary statistics for numeric columns
```

A typical first-look workflow:

```python
df = pd.read_csv("data/sales.csv")
print(df.shape)
print(df.dtypes)
df.head()
df.describe()
```

Within 30 seconds you should know: how big is the file, what columns it has,
what type each column is, whether there is missing data, and roughly what the
numeric values look like.

### `info()` in detail

`df.info()` prints something like:

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 244 entries, 0 to 243
Data columns (total 7 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   total_bill  244 non-null    float64
 1   tip         244 non-null    float64
 2   sex         244 non-null    object
 3   smoker      244 non-null    object
 4   day         244 non-null    object
 5   time        244 non-null    object
 6   size        244 non-null    int64
dtypes: float64(2), int64(1), object(4)
memory usage: 13.5+ KB
```

Read this output left to right: how many rows, how many non-null values per
column (`244 non-null` means no missing values), and the dtype. **`object`**
in pandas usually means "Python strings". If a column you expect to be
numeric shows up as `object`, that is your hint that there is text or
garbage in it.

### `describe()` in detail

`df.describe()` returns count, mean, std, min, 25%, 50%, 75%, max for every
numeric column. Pass `include="all"` to also see counts and most-frequent
values for string columns. This single command answers half the questions
that come up in a first review of a dataset.

### `value_counts`

For categorical columns, `value_counts` is the equivalent of
`SELECT col, COUNT(*) FROM t GROUP BY col ORDER BY 2 DESC`:

```python
df["day"].value_counts()
# Sat    87
# Sun    76
# Thur   62
# Fri    19
```

## 6. A Mental Model You Can Trust

Every time you work with pandas, picture the table:

- **Columns** have names. You select them with `df["col"]`, which returns a
  `Series`.
- **Rows** have an index. You select them by label with `df.loc["row"]` or
  by position with `df.iloc[0]`.
- Operations are **column-wise by default**: `df.mean()` returns one mean
  per column.
- Most pandas methods **return a new DataFrame** rather than modifying in
  place — assign the result back if you want to keep it.

## 7. The Jupyter Notebook

Almost all data analysis is done in **Jupyter notebooks** — files with the
extension `.ipynb` that mix executable code cells with markdown cells. Each
cell can be run independently and its output (text, table, plot) is saved in
the file. Notebooks are excellent for exploration; for production code you
will still write `.py` files.

Start a notebook from your virtual environment:

```bash
pip install jupyter
jupyter notebook    # or: jupyter lab
```

Useful magic commands you will see in this week's materials:

- `%matplotlib inline` — render plots inside the notebook (default in modern
  Jupyter, but harmless to include).
- `%timeit expression` — time a single expression.
- `%%time` — time a whole cell.
- `!ls` — run a shell command without leaving the notebook.

VS Code supports `.ipynb` natively — open one and you will get the same
cell-by-cell experience without launching Jupyter from the terminal.

## 8. Recap

You now know:

- What NumPy arrays are and why they are fast.
- How vectorization and broadcasting eliminate most explicit loops.
- The two pandas core objects: `Series` (one labelled column) and
  `DataFrame` (a labelled table).
- How to create DataFrames from dicts, lists, and files
  (`read_csv`/`read_json`/`read_excel`/`read_sql`).
- The six methods that give you a 30-second mental model of any new dataset:
  `head`, `tail`, `shape`, `dtypes`, `info`, `describe`.
- What Jupyter notebooks are for and how to start one.

Next lecture: cleaning and transforming. You will learn how to select
specific rows, fix bad values, handle missing data, and create derived
columns — the core of real analysis work.

## Further Reading

- pandas — "10 minutes to pandas":
  <https://pandas.pydata.org/docs/user_guide/10min.html>
- NumPy — "The absolute basics for beginners":
  <https://numpy.org/doc/stable/user/absolute_beginners.html>
- Jake VanderPlas, *Python Data Science Handbook*, Chapter 2 (NumPy) and
  Chapter 3.1–3.3 (pandas):
  <https://jakevdp.github.io/PythonDataScienceHandbook/>
