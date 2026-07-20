# Week 13 — Homework

Six problems. Each one mirrors a real task you will hit in industry: file
conversion, missing-data audits, joins, pivots, multi-line plots, and
correlation analysis. Plan on 4–6 hours total.

## Setup

Work in the same virtual environment you used for the exercises.

```bash
pip install numpy pandas matplotlib jupyter openpyxl
```

`openpyxl` is needed for Excel files (Problem 1 mentions it).

## Submission

Create a folder called `homework/` next to this file (it should already
exist). Put one `.py` or `.ipynb` per problem inside, named e.g.
`hw-01-csv-to-json.py`. Push to your fork; share links in the community
channel.

---

## Problem 1 — CSV → JSON converter

Write a short program that:

1. Takes a path to a CSV file as a command-line argument.
2. Reads it with `pd.read_csv`.
3. Writes it to a JSON file at the same location with the extension changed
   to `.json`, using `to_json(orient="records", indent=2)`.

Example use:

```bash
python hw-01-csv-to-json.py data/sales.csv
# writes data/sales.json
```

Bonus: accept either `.csv` or `.tsv` as input, and round numeric columns to
two decimals before writing.

---

## Problem 2 — Missing-data report

Given any DataFrame, write a function

```python
def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

that returns a DataFrame indexed by column name with these columns:

| Column         | Meaning |
|----------------|---------|
| `n_missing`    | how many missing values |
| `pct_missing`  | percent missing (0–100, rounded to 2 dp) |
| `dtype`        | the column's dtype |

Sort by `pct_missing` descending. Test it against
`seaborn.load_dataset("titanic")` — your function should report
`deck` at the top with about 77% missing.

---

## Problem 3 — Merge two DataFrames

You are given two DataFrames built inline:

```python
orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105],
    "customer_id": [1, 2, 1, 3, 99],
    "amount":      [50.0, 75.0, 20.0, 120.0, 9.0],
})

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name":        ["Ada", "Linus", "Grace", "Tim"],
    "country":     ["UK", "FI", "US", "GB"],
})
```

Write code that:

1. Performs a **left join** of `orders` onto `customers` on `customer_id`.
2. Prints how many orders failed to match a customer.
3. Fills the missing `name` and `country` with the literal string
   `"UNKNOWN"`.
4. Saves the merged DataFrame as `merged.csv`.

---

## Problem 4 — Pivot table from raw

Use the seaborn `tips` dataset (or any other DataFrame with at least two
categorical columns and one numeric column). Produce a pivot table with:

- Rows: `day`
- Columns: `time` (Lunch / Dinner)
- Values: **mean** `total_bill`
- Fill missing cells with `0`.

Then a second pivot:

- Rows: `day`
- Columns: `time`
- Values: **count** of orders.

Print both. Bonus: round mean values to 2 decimals; format the count pivot
as integers.

---

## Problem 5 — Multi-line chart

Take a small DataFrame of three product sales across 12 months (you may
fabricate the data). Produce a single chart that shows:

- A separate line for each product.
- One shared x-axis (months).
- A legend identifying each product.
- A clear title and y-axis label.
- Saved to `multi_line.png`.

Hint: if `monthly` is a DataFrame indexed by month with one column per
product, then `monthly.plot(ax=ax)` makes exactly the chart you want.

---

## Problem 6 — Find correlations

Load the seaborn `tips` dataset.

1. Compute the correlation matrix of the numeric columns: `df.corr(numeric_only=True)`.
2. Identify the **two columns with the strongest positive correlation**
   (excluding the diagonal). Print the column names and the coefficient.
3. Make a scatter plot of those two columns and overlay a linear trend line.
   (You can fit one with `np.polyfit(x, y, deg=1)`.)
4. In a comment or markdown cell, answer: does a higher `total_bill` lead
   to a proportionally higher `tip`?

Bonus: render the correlation matrix as a heatmap with
`sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)`.

---

## Quality checklist for all six problems

- [ ] Filenames follow `hw-NN-short-name.{py,ipynb}`.
- [ ] Every script has a top-of-file docstring stating the problem.
- [ ] Functions are typed (`def fn(x: int) -> str:`).
- [ ] No hard-coded paths outside your homework folder.
- [ ] Each plot has a title and axis labels.
- [ ] Code runs end-to-end with `python hw-NN-...py` (or notebook
      restarts-and-runs-all).
