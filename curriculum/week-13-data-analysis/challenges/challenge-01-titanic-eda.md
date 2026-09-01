# Challenge 1 — Titanic Exploratory Data Analysis

> **Topic:** exploratory data analysis — audit the holes, group, pivot, chart
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** every job that starts with "here is some data, tell me what
> is going on" is this exercise wearing different clothes. You audit what is
> missing, split by the groups that might matter, and end with one sentence a
> non-analyst can act on. Do it once on a small clean table and the full
> 891-row manifest is the same moves at a bigger scale.

## The Brief

In April 1912 the RMS *Titanic* sank on its maiden voyage. Its passenger
manifest is the canonical "first dataset" for a new analyst because survival was
so obviously *not* a coin flip — women, children, and first-class passengers
lived at very different rates from third-class men. Your job is to find that
pattern and state it in one sentence, backed by numbers.

The full manifest ships with the `seaborn` library as an 891-row table, and if
you are online that is exactly what you should explore. But the shipped answer
below cannot depend on a download — an answer key that fails on a train with no
signal is not an answer key. So it works a **16-passenger sample built inline**,
with the real column names and real holes in `age`, `embarked`, and `deck`.
Every technique is identical to what you run on the full 891; only the row count
changes, and with it the exact percentages.

Ask the data four things, in order: *what is missing, who survived, did class
matter on top of sex, and did age matter?* Then compute one finding and say it
plainly.

## Starter

Copy this into `challenge-01-titanic-eda.py` (or a notebook of the same name).
The data and the imports are done; the analysis is yours to fill in.

```python
"""challenge-01-titanic-eda.py — a small exploratory analysis of a manifest."""

import numpy as np
import pandas as pd

NA = np.nan

MANIFEST: dict[str, list] = {
    "survived": [1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    "pclass":   [1, 1, 2, 2, 3, 3, 3, 1, 1, 2, 2, 3, 3, 3, 3, 3],
    "sex": [
        "female", "female", "female", "female", "female", "female", "female",
        "male", "male", "male", "male", "male", "male", "male", "male", "male",
    ],
    "age":      [38.0, 35.0, 28.0, NA, 6.0, 24.0, 45.0,
                 40.0, 52.0, 31.0, NA, 22.0, 9.0, 27.0, NA, 61.0],
    "sibsp":    [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 3, 1, 0, 0, 0],
    "parch":    [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    "fare":     [71.28, 53.10, 26.00, 30.07, 16.70, 7.92, 7.75,
                 52.00, 35.50, 13.00, 10.50, 21.07, 15.25, 7.90, 8.05, 6.24],
    "embarked": ["C", "S", "S", "S", "Q", "S", "S",
                 "S", "S", "S", "C", "S", "S", "Q", NA, "S"],
    "deck":     ["C", "C", NA, NA, NA, NA, NA,
                 "E", "B", NA, NA, NA, NA, NA, NA, NA],
}

df = pd.DataFrame(MANIFEST)

# TODO: a missing-data audit — count nulls per column, as a count and a percent.
# TODO: the overall survival rate, then the rate grouped by sex, then by pclass.
# TODO: a pivot_table of survival rate with sex on the rows and pclass on the
#       columns, and pd.crosstab of the counts beneath it so no cell is over-read.
# TODO: survival rate by age band with pd.cut(bins=[0,10,20,40,60,80], right=False).
# TODO: a family_size column (sibsp + parch + 1) and survival by family size.
# TODO: one bar chart of survival rate by sex, saved to a PNG.
# TODO: one sentence naming the best group, the worst group, and the gap.
```

## Requirements

1. **Audit first.** Print how many values are missing per column, as a count
   and a percentage, showing only the columns that have holes.
2. Print the **overall** survival rate, the rate **by sex**, and the rate **by
   class**.
3. Print a **sex-by-class pivot** of survival rate, and the **counts** for the
   same six groups directly beneath it.
4. Print survival rate **by age band**, using only the passengers whose age is
   known.
5. Add a **`family_size`** column and print survival rate by family size.
6. Draw **one labelled bar chart** of survival rate by sex, with the y-axis
   fixed to the 0–1 range, and save it (a temporary file is fine).
7. End with **one sentence** naming the best-off group, the worst-off group,
   the gap between them in percentage points, and the overall rate — every
   number computed, not typed.

## Constraints

- **Do not fill `age` with its mean before charting or banding it.** It is the
  reflex the lecture's `fillna(mean)` line teaches, and here it is wrong: the
  missing ages are not missing at random, so the mean of the known ages is not a
  defensible guess for the unknown ones. Drop the missing rows for anything
  age-based and state the count you kept.
- **Drop `deck`, and say why.** Three-quarters of it is missing here, and in the
  real manifest the missingness *is* a proxy for wealth — cabins were recorded
  mostly for first class. Imputing it would smuggle the answer into the feature.
- **Combine masks with `&`, `|`, `~`, never `and`/`or`, and parenthesise each
  side.** A boolean Series has no single truth value, so `and` raises; and `&`
  binds tighter than `==`, so `(a == 1) & (b == 2)` needs its parentheses.
- **Put a rate on a 0–1 axis.** `ax.set_ylim(0, 1)` — otherwise matplotlib
  auto-scales the axis to the data and a 40-point gap and a 4-point gap look
  equally dramatic.
- **Compute the finding; do not type it.** The closing sentence must read its
  numbers out of the pivot, so it can never disagree with the table above it.

## Expected output

```text
$ python challenge-01-titanic-eda-solution.py
shape: (16, 9)
--- missing-data audit ---
          n_missing  pct_missing
deck             12         75.0
age               3         18.8
embarked          1          6.2

Overall survival rate: 0.500  (8 of 16)

--- survival rate by sex ---
sex
female    0.714
male      0.333

--- survival rate by class ---
pclass
1    0.75
2    0.75
3    0.25

--- survival rate by sex and class ---
pclass    1    2      3
sex                    
female  1.0  1.0  0.333
male    0.5  0.5  0.200

--- passenger counts by sex and class ---
pclass  1  2  3
sex            
female  2  2  3
male    2  2  5

--- survival rate by age band (known ages only) ---
          n  survivors   rate
age                          
[0, 10)   2          1  0.500
[20, 40)  7          5  0.714
[40, 60)  3          1  0.333
[60, 80)  1          0  0.000

--- survival rate by family size ---
             n   rate
family_size          
1            9  0.444
2            3  0.667
3            2  0.500
4            1  1.000
5            1  0.000

Finding: female in class 1 survived at 100.0%; male in class 3 at 20.0% — a gap of 80 percentage points, against an overall rate of 50.0%.

Saved 1 chart (survival by sex) to a temp dir; cleaned up.
```

Sixteen passengers is far too few to trust any single percentage — the point of
the sample is the *shape* of the analysis, not the numbers. On the full 891-row
manifest the same code returns firmer figures (female first-class near 97%, male
third-class near 14%), and the story holds: sex was the stronger factor, class
the second, and the two compound rather than cancel.

## Steps

1. Paste the starter and run it — it should build the frame and print nothing
   yet. Confirming the data loads before you analyse it is the habit the audit
   is about.
2. Write the missing-data audit. Read it before you compute a single rate: it
   tells you which columns you can trust and which you must caveat.
3. Add the three survival rates — overall, by sex, by class. Each is a
   `groupby(...)["survived"].mean()`, because the mean of a 0/1 column is a
   proportion.
4. Build the pivot and the crosstab. Read across a row and down a column; the
   crosstab underneath stops you over-reading a two-passenger cell.
5. Band the ages with `pd.cut(..., right=False)` and group by family size.
6. Draw the bar chart, fix the y-axis to `(0, 1)`, and save it.
7. Write the finding as one sentence with `f"{value:.1%}"` fields, so the
   numbers come from the computation, not your memory of it.

## The Solution

```python
"""challenge-01-titanic-eda-solution.py — a worked EDA on a small passenger manifest.

The challenge asks you to explore the full 891-row Titanic dataset that seaborn
downloads. So this shipped answer runs anywhere, offline, and gives identical
numbers on every machine, it works a self-contained 16-passenger *sample* built
inline as a dict of lists — the exact columns of the real manifest, with real
holes punched in ``age``, ``embarked`` and ``deck``. Every move here (a survival
rate as the mean of a 0/1 column, a sex-by-class pivot, an age-band cut, a
missing-data audit) is line-for-line what you run on the full dataset; only the
row count changes.

The one chart is drawn with matplotlib's non-interactive Agg backend and written
into a throwaway temporary directory that Python deletes on the way out.

Run it with::

    python challenge-01-titanic-eda-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # choose a headless backend before importing pyplot

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

NA = np.nan

# A 16-passenger sample of the manifest. Real column names; real holes.
MANIFEST: dict[str, list] = {
    "survived": [1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    "pclass":   [1, 1, 2, 2, 3, 3, 3, 1, 1, 2, 2, 3, 3, 3, 3, 3],
    "sex": [
        "female", "female", "female", "female", "female", "female", "female",
        "male", "male", "male", "male", "male", "male", "male", "male", "male",
    ],
    "age":      [38.0, 35.0, 28.0, NA, 6.0, 24.0, 45.0,
                 40.0, 52.0, 31.0, NA, 22.0, 9.0, 27.0, NA, 61.0],
    "sibsp":    [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 3, 1, 0, 0, 0],
    "parch":    [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    "fare":     [71.28, 53.10, 26.00, 30.07, 16.70, 7.92, 7.75,
                 52.00, 35.50, 13.00, 10.50, 21.07, 15.25, 7.90, 8.05, 6.24],
    "embarked": ["C", "S", "S", "S", "Q", "S", "S",
                 "S", "S", "S", "C", "S", "S", "Q", NA, "S"],
    "deck":     ["C", "C", NA, NA, NA, NA, NA,
                 "E", "B", NA, NA, NA, NA, NA, NA, NA],
}


def main() -> None:
    """Audit the holes, then compute survival rates every way that matters."""
    df = pd.DataFrame(MANIFEST)
    print(f"shape: {df.shape}")

    # 1. Missing-data audit — decide the holes before touching the numbers.
    audit = pd.DataFrame({
        "n_missing": df.isna().sum(),
        "pct_missing": (df.isna().mean() * 100).round(1),
    })
    print("--- missing-data audit ---")
    print(
        audit[audit["n_missing"] > 0]
        .sort_values("pct_missing", ascending=False)
        .to_string()
    )

    # 2. Survival rates: the mean of a 0/1 column IS a proportion.
    overall = df["survived"].mean()
    print(f"\nOverall survival rate: {overall:.3f}  ({df['survived'].sum()} of {len(df)})")

    print("\n--- survival rate by sex ---")
    print(df.groupby("sex")["survived"].mean().round(3).to_string())

    print("\n--- survival rate by class ---")
    print(df.groupby("pclass")["survived"].mean().round(3).to_string())

    # 3. Two factors at once: a sex-by-class pivot, with the counts beneath it.
    pivot = df.pivot_table(index="sex", columns="pclass", values="survived", aggfunc="mean")
    print("\n--- survival rate by sex and class ---")
    print(pivot.round(3).to_string())
    print("\n--- passenger counts by sex and class ---")
    print(pd.crosstab(df["sex"], df["pclass"]).to_string())

    # 4. Age bands on the known ages only, half-open so a 10-year-old is a teen.
    bands = pd.cut(df["age"], bins=[0, 10, 20, 40, 60, 80], right=False)
    by_band = df.groupby(bands, observed=True).agg(
        n=("survived", "size"),
        survivors=("survived", "sum"),
        rate=("survived", "mean"),
    )
    print("\n--- survival rate by age band (known ages only) ---")
    print(by_band.round(3).to_string())

    # 5. Family size, derived from sibsp + parch + the passenger themselves.
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    print("\n--- survival rate by family size ---")
    print(df.groupby("family_size")["survived"].agg(n="size", rate="mean").round(3).to_string())

    # 6. The finding — computed from the pivot, never typed in by hand.
    rates = pivot.stack(future_stack=True)
    best, worst = rates.idxmax(), rates.idxmin()
    print(
        f"\nFinding: {best[0]} in class {best[1]} survived at {rates.max():.1%}; "
        f"{worst[0]} in class {worst[1]} at {rates.min():.1%} — a gap of "
        f"{(rates.max() - rates.min()) * 100:.0f} percentage points, against an "
        f"overall rate of {overall:.1%}."
    )

    # 7. One labelled chart, into a temp dir that is deleted on the way out.
    by_sex = df.groupby("sex")["survived"].mean()
    with tempfile.TemporaryDirectory() as workspace:
        fig, ax = plt.subplots(figsize=(6, 4))
        by_sex.plot.bar(ax=ax, color=["#ee6666", "#3273dc"], rot=0)
        ax.set_title("Survival rate by sex (16-passenger sample)")
        ax.set_xlabel("Sex")
        ax.set_ylabel("Survival rate")
        ax.set_ylim(0, 1)
        fig.tight_layout()
        fig.savefig(Path(workspace) / "fig-survival-by-sex.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print("\nSaved 1 chart (survival by sex) to a temp dir; cleaned up.")


if __name__ == "__main__":
    main()
```

**A survival rate is just the mean of the `survived` column.** `survived` is
`0` for died and `1` for lived, so `groupby("sex")["survived"].mean()` averages
ones and zeros — and the average of a 0/1 column is exactly the fraction of
ones. That is why the manifest stores survival as an integer: it is
arithmetic-ready. You never need `value_counts(normalize=True)` and a division.

**`pivot_table` is `groupby` on two keys with the second one spread sideways.**
`df.groupby(["sex", "pclass"])["survived"].mean()` computes the same six numbers;
`pivot_table` differs only in laying them out as a 2×3 grid instead of a six-row
stack. The grid is what you want when you intend to read *across* a row and
*down* a column, which is exactly the class-versus-sex comparison. The
`crosstab` of counts goes underneath so nobody mistakes a rate that rests on two
passengers for one that rests on twenty.

**`pd.cut` with `right=False` makes the bins half-open, and that is the correct
choice for ages.** `bins=[0, 10, 20, 40, 60, 80]` with `right=False` gives
`[0, 10)`, `[10, 20)`, … — so a passenger aged exactly 10 lands in the *second*
bin, and, crucially, a newborn aged 0 lands in the first. The default
`right=True` would give `(0, 10]` and silently drop age 0 entirely, which on a
manifest that includes infants is a real bug. `observed=True` on the groupby
keeps pandas from emitting empty bands and from warning about it.

**The finding is computed, never typed.** `pivot.stack(future_stack=True)`
flattens the 2×3 grid back into a six-row Series keyed by `(sex, pclass)`, and
`.idxmax()` / `.idxmin()` hand back the best and worst *labels*, not the values —
so the sentence can name the groups and read their rates straight from the same
object. Type the sentence by hand and it starts lying the first time the data
changes.

**About the shipped file.** The 16-row `MANIFEST` and the single chart written to
a `tempfile.TemporaryDirectory` exist so this download runs offline and leaves
nothing behind. On the real dataset you would swap the dict for
`seaborn.load_dataset("titanic")` and point `savefig` at a real file — every
line between those two edits is unchanged.

## Download and run

Download
[challenge-01-titanic-eda-solution.py](./challenge-01-titanic-eda-solution.py)
and run it:

```bash
python challenge-01-titanic-eda-solution.py
```

It needs only pandas, numpy, and matplotlib — no network, no dataset file. It
builds the sample inline, prints the audit and every survival rate, draws one
chart into a temporary directory that Python deletes on the way out, and prints
the computed finding. The `-solution` suffix keeps it from colliding with your
own `challenge-01-titanic-eda.py`.

## Common bugs to catch

- **The histogram grows a spike at 29.** You filled missing ages with the mean
  before charting. Every imputed passenger piles onto one bin and invents a peak
  that is not in the data. Drop the missing ages instead, and print the count
  you kept.
- **`ValueError: The truth value of a Series is ambiguous.`** You wrote a mask
  with `and` — `df[df["sex"] == "female" and df["pclass"] == 1]`. Python's `and`
  calls `bool()` on an entire Series, which has no single truth value. Use `&`
  and parenthesise: `df[(df["sex"] == "female") & (df["pclass"] == 1)]`.
- **`TypeError: agg function failed [how->mean,dtype->object]`.** You averaged a
  text column — grouping on a `"yes"`/`"no"` survival column instead of the 0/1
  one. Average the integer.
- **Every survival rate is `NaN` or wildly off.** A `pivot_table` cell with no
  passengers comes back `NaN`; here all six cells are filled, but on your own
  subset check the `crosstab` before trusting a rate.
- **The bar chart makes a small gap look enormous, or an enormous gap look
  small.** You left the y-axis to auto-scale. A rate belongs on `set_ylim(0, 1)`
  unless you have a stated reason otherwise.
- **You quoted the example sentence as your answer.** The brief's "97% versus
  14%" is the *shape* of a finding, not the finding. Compute yours from the
  pivot — that is what the last line of the solution is for.

## Under the hood

<details>
<summary>Under the hood — why .T decides which variable becomes the x-axis</summary>

`pivot` here is sex-by-class: two rows (`female`, `male`), three columns
(`1`, `2`, `3`). When you hand a DataFrame to pandas' `.plot.bar`, it puts the
**index on the x-axis** and draws **one coloured series per column**. So plotting
`pivot` straight gives two x-groups (the sexes) with three bars each (the
classes); plotting `pivot.T` gives three x-groups (the classes) with two bars
each (the sexes). Neither is wrong — they answer different questions. Decide
which variable you want running along the bottom, and transpose or not to put it
there.

The same rule explains why a plain `groupby(["sex", "pclass"])` Series is
awkward to chart and the pivot is easy: the Series has a two-level MultiIndex on
one axis, so matplotlib cannot tell which level is the x-axis and which is the
series. The pivot has already made that decision by putting one variable on the
rows and the other on the columns — which is the whole reason `pivot_table`
exists next to `groupby`.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and no `FutureWarning`.
- [ ] The audit shows `deck`, `age`, and `embarked` as the columns with holes.
- [ ] Survival rate appears overall, by sex, by class, and as a sex-by-class
      pivot with counts beneath it.
- [ ] Age bands use `right=False` and cover only the known ages.
- [ ] The chart has a title, both axis labels, and a y-axis fixed to `(0, 1)`.
- [ ] The finding is one sentence and every number in it is computed.
- [ ] Committed to Git with a message like
      `Add Week 13 challenge 1: titanic EDA`.

## Stretch

- Add a `who`-style column (`"child"` for age < 13, else `"adult"`) and compare
  child versus adult survival. Children are the one group that tends to cut
  across the sex-and-class pattern.
- Chart the sex-by-class pivot as grouped bars with `pivot.T.plot.bar()`, and
  read the transpose note in *Under the hood* before you decide which way round
  to plot it.
- Swap the inline `MANIFEST` for `seaborn.load_dataset("titanic")` on a
  connected machine and rerun. The code does not change; the numbers firm up to
  the famous ones, and you can feel how much a 16-row sample was hiding.
- Add a correlation view: `df.corr(numeric_only=True).round(2)`. Which numeric
  columns move together, and which of those is just `fare` standing in for
  `pclass`?
