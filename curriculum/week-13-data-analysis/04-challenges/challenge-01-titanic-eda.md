# Challenge 01 — Titanic Exploratory Data Analysis

## Background

In April 1912 the RMS *Titanic* sank on its maiden voyage; of the 2,224
passengers and crew aboard, more than 1,500 perished. The passenger manifest
has been studied for over a century and is the canonical "first dataset"
for new data analysts because the survival rates differ sharply by gender,
class, and age — making it easy to find non-trivial patterns.

A cleaned-up version of the manifest ships with seaborn and contains 891
rows. You will use it.

## Your task

Open a new Jupyter notebook in this folder named
`challenge-01-titanic-eda.ipynb`. Load the dataset and produce a short
exploratory analysis. You should have:

1. **At least four code cells** demonstrating different pandas methods.
2. **At least three charts**, each with title and axis labels.
3. **At least three markdown cells** with prose interpreting the data.
4. **One numeric finding** stated as a clear sentence at the end.

## Loading the data

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = sns.load_dataset("titanic")
df.head()
```

The columns are:

| Column      | Meaning |
|-------------|---------|
| `survived`  | 0 = died, 1 = survived |
| `pclass`    | Passenger class (1, 2, 3) |
| `sex`       | "male" / "female" |
| `age`       | Age in years (some missing) |
| `sibsp`     | # of siblings / spouses aboard |
| `parch`     | # of parents / children aboard |
| `fare`      | Ticket fare in pounds |
| `embarked`  | Port of embarkation (C, Q, S) |
| `class`     | Same as pclass but as a string |
| `who`       | "man", "woman", "child" |
| `alive`     | "yes" / "no" (matches `survived`) |
| `deck`      | Letter A–G (lots of missing values) |
| `embark_town` | Full town name |
| `alone`     | Boolean |

## Suggested questions

Answer at least **three** of these. Treat them as starting points.

1. What was the overall survival rate?
2. How did survival rate differ by `sex`?
3. How did survival rate differ by `pclass`?
4. What was the average `age` by class? By gender?
5. How does survival rate change with `age` band (e.g. 0–10, 10–20, etc.)?
   Hint: `pd.cut`.
6. What fraction of children (`who == "child"`) survived versus adults?
7. Is there a correlation between `fare` and survival? Use a scatter plot
   or a box plot.
8. How much data is missing per column? What would you do about `deck`?

## Required charts (at least three)

- A **bar chart** of survival rate broken down by one categorical variable
  (`sex`, `pclass`, or `embarked`).
- A **histogram** of `age` (drop NaN first).
- A **third chart of your choice** — scatter, box, stacked bar, heatmap,
  etc.

Each chart should be a complete picture: title, axis labels, sensible scale.

## A starting recipe

```python
df = sns.load_dataset("titanic")

# Look around
print(df.shape)
df.info()
df.head()

# Missing-data audit
df.isna().sum().sort_values(ascending=False)

# Survival rate by sex
df.groupby("sex")["survived"].mean()

# Survival rate by class
df.groupby("pclass")["survived"].mean()

# Plot the survival rate by sex
ax = df.groupby("sex")["survived"].mean().plot.bar(color=["#ee6666", "#3273dc"])
ax.set_title("Titanic survival rate by sex")
ax.set_ylabel("Survival rate")
ax.set_ylim(0, 1)
```

## Stretch ideas

- Build a `family_size` feature as `sibsp + parch + 1` and explore survival
  by family size.
- Bin `age` into "child / adult / senior" and chart survival by bin.
- Try seaborn's `sns.heatmap(df.corr(numeric_only=True), annot=True)` for a
  correlation matrix.
- Save your favourite chart as a 300-DPI PNG and embed it in your one-page
  summary.

## Deliverable

A notebook saved as
`challenges/solutions/challenge-01-titanic-eda.ipynb` that runs top-to-
bottom without error and contains:

- Imports and data load.
- A missing-data audit cell.
- Three or more charts, each labelled.
- A final markdown cell with **one** numeric finding stated as a sentence
  (e.g. *"Female first-class passengers survived at a rate of 97% versus
  16% for male third-class passengers — a gap of 81 percentage points."*).
