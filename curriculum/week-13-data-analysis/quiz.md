# Week 13 — Quiz

Ten multiple-choice questions covering the lecture notes for the week. Pick
**one** answer per question. The answer key is at the bottom — try the whole
quiz before scrolling.

---

### 1. What is the conventional alias for the pandas library?

- A. `pd`
- B. `pa`
- C. `panda`
- D. `pdr`

---

### 2. Given `df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})`, which
expression returns the **first column as a Series**?

- A. `df.loc["a"]`
- B. `df["a"]`
- C. `df[["a"]]`
- D. `df.iloc[0]`

---

### 3. What does `df.shape` return for a DataFrame with 100 rows and 7
columns?

- A. `100`
- B. `(7, 100)`
- C. `(100, 7)`
- D. `[100, 7]`

---

### 4. Which method shows the dtype of each column **plus** the count of
non-null values in every column?

- A. `df.head()`
- B. `df.describe()`
- C. `df.info()`
- D. `df.dtypes`

---

### 5. You want every row where `score > 80` **and** `subject == "Math"`.
Which expression is correct?

- A. `df[df["score"] > 80 and df["subject"] == "Math"]`
- B. `df[(df["score"] > 80) & (df["subject"] == "Math")]`
- C. `df[df["score"] > 80 && df["subject"] == "Math"]`
- D. `df.where("score > 80 and subject == 'Math'")`

---

### 6. What is the difference between `.loc` and `.iloc`?

- A. `.loc` selects by label, `.iloc` selects by integer position.
- B. `.loc` selects rows only, `.iloc` selects columns only.
- C. `.loc` returns a copy, `.iloc` returns a view.
- D. They are aliases of each other.

---

### 7. To replace missing values in column `price` with the column's mean,
which line is correct?

- A. `df["price"].dropna(df["price"].mean())`
- B. `df["price"].fillna(df["price"].mean())`
- C. `df["price"].replace(np.nan, "mean")`
- D. `df["price"] = df["price"].mean()`

---

### 8. Which call produces a Series of the **mean** `tip` per `day`?

- A. `df.groupby("day").mean("tip")`
- B. `df.groupby("day")["tip"].mean()`
- C. `df.mean().groupby("day")`
- D. `df["tip"].groupby("day").mean()`

---

### 9. To combine two DataFrames `orders` and `customers` on the column
`customer_id`, keeping every order even when the customer is missing, you
would write:

- A. `orders.merge(customers, on="customer_id", how="inner")`
- B. `orders.merge(customers, on="customer_id", how="left")`
- C. `pd.concat([orders, customers], axis=1)`
- D. `orders.join(customers)`

---

### 10. Which line saves a matplotlib figure to a PNG with crisp resolution
and trimmed whitespace?

- A. `plt.print("chart.png")`
- B. `fig.savefig("chart.png")`
- C. `fig.savefig("chart.png", dpi=150, bbox_inches="tight")`
- D. `fig.export("chart.png", quality=high)`

---

## Answer key

<details>
<summary>Click to reveal answers</summary>

1. **A** — `import pandas as pd`.
2. **B** — Single brackets with a string return a `Series`; double brackets
   `[["a"]]` would return a one-column DataFrame.
3. **C** — `shape` is `(rows, columns)`.
4. **C** — `info()` is the all-in-one summary.
5. **B** — `&` and `|` with parentheses around each clause. The Python
   keywords `and` / `or` do not work element-wise.
6. **A** — Label vs. integer position.
7. **B** — `fillna` is the right tool; the mean is a fine fill value.
8. **B** — Group, then select the column, then aggregate.
9. **B** — `how="left"` keeps every row from `orders`.
10. **C** — Both `dpi` and `bbox_inches="tight"` matter for a publishable
    figure.

</details>

## Score yourself

- 9–10 correct: you're ready for the mini-project. Go!
- 7–8 correct: skim the lecture sections you missed, then proceed.
- ≤ 6 correct: re-read [lecture-notes/01-numpy-and-pandas-basics.md](./lecture-notes/01-numpy-and-pandas-basics.md)
  through [lecture-notes/03-aggregation-and-plotting.md](./lecture-notes/03-aggregation-and-plotting.md)
  and retake the quiz tomorrow.
