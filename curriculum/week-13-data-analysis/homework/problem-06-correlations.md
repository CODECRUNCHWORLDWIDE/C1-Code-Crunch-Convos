# Homework 6 — Find correlations

> **Topic:** the correlation matrix, finding the strongest pair, fitting a trend line — and reading the number honestly
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hr
> **Why this one:** correlation is the most useful number in a first pass over
> unfamiliar data and the most misread number in the whole field. This problem
> makes you compute it, find the strongest pair automatically, draw it, fit a
> line through it — and then prove, from the same data, that the obvious
> conclusion everyone jumps to is wrong.

## The Brief

Correlation answers one small question: **when this number goes up, does that
one usually go up too?**

Height and shoe size. Taller people usually have bigger feet, so those two
numbers move together — they are correlated. Now say the sentence out loud that
everyone says next: *bigger shoes make you taller.* Obviously false. Buying size
14 boots will not add an inch to anyone.

Hold on to that, because it is the whole point of this page.

**A correlation is not a cause.** It is a description of two columns moving
together, and nothing more. It cannot tell you which one moved first, whether
one pushed the other, or whether some third thing pushed both. Ice cream sales
and drowning deaths rise together every summer; the third thing is hot weather,
and no amount of arithmetic on those two columns will ever say so. This is the
single most misread number in data work, and reading it wrong in a real job gets
real money spent on the wrong thing.

Now the task. You have a restaurant frame: the total on each bill, the tip left,
and the number of people at the table.

1. Compute the correlation of every numeric column against every other numeric
   column. That grid is a **correlation matrix**.
2. Find the strongest positive pair automatically — not by squinting at the grid.
3. Draw those two columns as a scatter plot and fit a straight line through it.
4. Answer the question the brief actually asks: *does a higher bill lead to a
   proportionally higher tip?*

Question 4 is a trap, twice over. The word "lead to" is causal, and no
correlation can support it. And the word "proportionally" is a much stronger
claim than "correlated" — it says double the bill, double the tip. You will find
that the two columns are strongly correlated **and** that the tip is not
proportional, and the same script will show you both. Those are not a
contradiction. They are two different questions that people constantly confuse.

The original brief points at seaborn's `tips` dataset. The shipped answer builds
an eighty-row frame with the same shape, using a seeded generator, so it runs
offline with the same numbers on every machine — and it reproduces the real
dataset's finding.

## Starter

Copy this into `problem-06-correlations.py` in your homework folder. It runs as
pasted.

```python
"""problem-06-correlations.py — find the strongest correlation in a tips frame.

Builds a seeded, tips-shaped frame, prints its correlation matrix, finds the
strongest positive pair, fits a straight line through it, saves the scatter,
and then checks whether the tip is actually proportional to the bill.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUTPUT_PATH = Path("corr_scatter.png")


def make_tips(n: int = 80) -> pd.DataFrame:
    """A seeded tips frame: tip = 0.10*bill + a fixed part + noise."""
    rng = np.random.default_rng(20)
    total_bill = np.round(rng.uniform(8.0, 55.0, n), 2)
    # TODO: tip is ten percent of the bill, plus a fixed 1.2, plus
    #       rng.normal(0, 0.55, n) of noise. Round to 2 decimals.
    tip = np.zeros(n)
    # TODO: size is roughly total_bill / 13, jittered, clipped to 1..6, as int.
    size = np.ones(n, dtype=int)
    return pd.DataFrame({"total_bill": total_bill, "tip": tip, "size": size})


def strongest_pair(corr: pd.DataFrame) -> tuple[str, str, float]:
    """Return (col_a, col_b, r) for the largest off-diagonal correlation."""
    # TODO: build a boolean mask of the upper triangle above the diagonal with
    #       np.triu(np.ones(corr.shape, dtype=bool), k=1).
    # TODO: corr.where(mask).stack(future_stack=True) turns the surviving
    #       cells into a Series keyed by (row, column).
    # TODO: idxmax gives the winning pair, max gives the coefficient.
    return ("", "", 0.0)


if __name__ == "__main__":
    tips = make_tips()

    # 1. Correlation matrix of the numeric columns.
    # TODO: corr = tips.corr(numeric_only=True); print it, rounded to 4,
    #       under the heading "Correlation matrix", with .to_string().

    # 2. Strongest positive off-diagonal pair.
    # TODO: unpack strongest_pair(corr) and print
    #       "Strongest positive correlation: {a} vs {b}, r = {r:.4f}".

    # 3. Scatter with a least-squares trend line.
    # TODO: pull the two columns out as numpy arrays.
    # TODO: slope, intercept = np.polyfit(x, y, deg=1)
    # TODO: scatter the points, plot the fitted line over them, label both
    #       axes and the chart, add a legend and a grid, save the PNG,
    #       close the figure.
    # TODO: print the slope, the intercept, and r squared.

    # 4. Proportional? Compare the tip rate across bill quartiles.
    # TODO: add a tip_pct column: tip / total_bill * 100.
    # TODO: cut total_bill into 4 quartiles with pd.qcut and labels
    #       ["Q1 cheapest", "Q2", "Q3", "Q4 priciest"].
    # TODO: print the mean tip_pct per quartile, rounded to 2.
    print("nothing computed yet")
```

## Requirements

1. Build the frame with `np.random.default_rng(20)` and `n = 80`, so everybody
   gets the same numbers.
2. Compute the full correlation matrix with `tips.corr(numeric_only=True)`,
   round it to 4 decimals, and print it with `.to_string()` under the heading
   `Correlation matrix`.
3. Find the strongest positive pair **in code**, ignoring the diagonal and
   counting each pair once. Print
   `Strongest positive correlation: total_bill vs tip, r = 0.9053`.
4. Fit a straight line through those two columns with `np.polyfit(x, y, deg=1)`.
5. Draw a scatter of the two columns with the fitted line over it. Title, both
   axis labels with units, a legend, a grid. Save it to `corr_scatter.png` with
   the `Agg` backend. Do not call `plt.show()`.
6. Print the slope, the intercept, and r squared, each to 4 decimals.
7. Answer the brief's question with evidence, not opinion: add a `tip_pct`
   column, cut `total_bill` into four quartiles with `pd.qcut`, and print the
   mean tip percentage in each.
8. State the verdict in a comment or in the write-up you hand in, and state it
   in the language the data supports — "moves with", not "causes".

## Constraints

- **`numeric_only=True` on `corr`.** A real tips frame has text columns —
  `day`, `sex`, `smoker`. Correlation is arithmetic; it has nothing to say about
  the word "Saturday". Without that flag pandas tries anyway and you get
  `ValueError: could not convert string to float: 'Sat'`.
- **Mask the diagonal and one triangle before hunting for the maximum.** Every
  column correlates with itself at exactly 1.0, so the diagonal always wins and
  your answer is always a column against itself. And the grid is a mirror —
  `total_bill vs tip` appears twice. `np.triu(..., k=1)` keeps only the cells
  above the diagonal, which is each pair, once.
- **Pass `future_stack=True` to `stack`.** pandas is changing what `stack` does
  with the empty cells the mask left behind. Saying which behaviour you want
  means the script gives the same answer after a pandas upgrade rather than
  quietly changing its mind.
- **`np.polyfit(x, y, deg=1)`, in that order.** The first array is the
  horizontal one. Swap them and you fit bill-against-tip instead of
  tip-against-bill, and your slope comes back as about 9 rather than about 0.1 —
  a hundredfold error that raises nothing at all.
- **Never write "causes", "drives", "leads to" or "because of" about a
  correlation.** Not in a comment, not in a commit message, not in the sentence
  you say out loud in the meeting. The honest verbs are "moves with", "is
  associated with", "predicts". If somebody wants a causal claim, they need an
  experiment — change one thing on purpose and see what happens — not a
  coefficient.
- **Look at the scatter before you trust the coefficient.** The `r` you are
  computing is Pearson's, and it measures one thing only: how close the points
  sit to a *straight* line. A perfect upside-down U — a real, strong, obvious
  relationship — scores an `r` near zero. Reporting "no correlation" from that
  number without opening the picture is how a genuine finding gets thrown away.
- **Seed the generator.** Unseeded random data makes every number on this page,
  including the answer, unreproducible.
- **`Agg` backend, `savefig`, no `plt.show()`.** Same rule as the last problem:
  a script that needs a window is a script that dies on a server.

## Expected output

Real captured run of the shipped answer,
[`problem-06-correlations-solution.py`](./problem-06-correlations-solution.py):

```text
$ python problem-06-correlations.py
Correlation matrix
            total_bill     tip    size
total_bill      1.0000  0.9053  0.8816
tip             0.9053  1.0000  0.7785
size            0.8816  0.7785  1.0000

Strongest positive correlation: total_bill vs tip, r = 0.9053
slope     = 0.0999 dollars of tip per dollar of bill
intercept = 1.0987 dollars
r squared = 0.8196

Mean tip percentage by total_bill quartile
total_bill
Q1 cheapest    18.45
Q2             15.17
Q3             13.36
Q4 priciest    12.46
```

Read it in four passes.

**The matrix.** The diagonal is all `1.0000` — every column is a perfect match
for itself, which is true and useless, and is exactly why the code masks it.
The grid is symmetric: `total_bill vs tip` reads 0.9053 whichever way round you
look it up. The strongest real pair is `total_bill` and `tip` at 0.9053. Party
`size` is close behind against the bill, at 0.8816, which makes sense — more
people, more food.

**The line.** The fit is `tip = 0.0999 x bill + 1.0987`. About ten cents of tip
for every dollar of bill, *plus* a fixed dollar and ten. That fixed part is the
whole answer to the homework's question and it is easy to skim past.

**r squared = 0.8196.** Square the correlation and you get the share of the
up-and-down in the tips that moves in step with the bill: about 82%. The other
18% is everything else — mood, service, whether the table liked the waiter. A
number that high says the bill is a genuinely good predictor of the tip.

**The quartiles, which settle it.** Split the bills into four equal-sized groups
from cheapest to priciest and look at the tip *percentage*:

| Quartile | Mean tip % |
|---|---|
| Q1 cheapest | 18.45 |
| Q2 | 15.17 |
| Q3 | 13.36 |
| Q4 priciest | 12.46 |

The percentage falls, steadily, from 18.45% to 12.46%. So the answer to *"does a
higher bill lead to a proportionally higher tip?"* is **no**, in two separate
ways.

First, on the arithmetic: proportional means a straight line through the origin —
double the bill, double the tip. This line does not pass through the origin. It
starts $1.10 up. On a $10 bill that fixed dollar-ten is 11% of the bill; on a
$50 bill it is 2%. That is precisely why the percentage drops as bills grow,
and it is why 0.9053 and "not proportional" sit together with no contradiction:
they are answers to different questions.

Second, on the word "lead to": nothing here can tell you the bill *caused* the
tip. The two rise together. A tipping habit, a party size, a menu price and a
level of service all sit behind both columns, and this data set cannot separate
them. The finding is that bills and tips move together, tightly, with a fixed
floor. That is a real, useful, sellable finding. It is not a cause, and calling
it one would be the mistake this whole problem exists to prevent.

The chart is the fifth pass and a page cannot show it to you. Open
`corr_scatter.png` and confirm: eighty semi-transparent dots forming a broad
upward band from about $8 to about $55 on the x axis; one straight red line
rising gently through the middle of them, meeting the left edge somewhere above
$2 rather than at zero; a title carrying `r = 0.91` and `n = 80`; both axes
labelled with `($)`; and a legend whose second entry spells out the fitted
equation. The gap between where that line meets the axis and the origin *is* the
non-proportionality, drawn.

## Steps

1. Create the file, paste the starter, run it. It prints one line and does
   nothing else. That is the baseline.
2. Fill in `make_tips`. Print `tips.head()` and `tips.describe()` and look at
   the ranges before you compute anything. Bills from about $8 to about $55,
   tips of a few dollars, parties of one to six.
3. Add the correlation matrix and print it. Check the diagonal is 1.0 and that
   the grid is symmetric — if it is not, you have printed something else.
4. Write `strongest_pair`. Test it deliberately: first without the mask, and
   watch it return a column against itself at 1.0. Then add the mask. Seeing the
   wrong answer once is worth more than reading about it.
5. Add `np.polyfit`. Print the slope and intercept. Then swap `x` and `y` on
   purpose, see the slope jump to about 9, and swap them back.
6. Build the scatter and the line, label everything, save the PNG, open it.
   Sanity-check the picture against the numbers: a slope of 0.1 should look
   gentle, not steep.
7. Add `r squared` and say out loud what it means: about 82% of the movement in
   tips travels with the bill.
8. Add the `tip_pct` column and the `qcut` quartiles. This is the step that
   answers the actual question.
9. Write two or three sentences of verdict at the bottom of the file, in a
   comment or a docstring. Use "moves with", not "causes". If you catch yourself
   typing "because", stop and rewrite the sentence.

## The Solution

```python
"""hw-06-correlations.py — find the strongest correlation in a tips-like frame.

The homework uses seaborn's ``tips`` dataset. So it runs offline and identically
everywhere, this shipped answer builds an inline, seeded frame where tip depends
on the bill with a *fixed* component (a positive intercept) plus noise — the same
shape as the real data, and enough to reproduce the finding that a bigger bill
does not tip proportionally more.

The scatter is drawn with matplotlib's non-interactive Agg backend and written
into a throwaway temporary directory that Python deletes on the way out.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_tips(n: int = 80) -> pd.DataFrame:
    """A seeded tips frame: tip = 0.10*bill + fixed part + noise; size tracks bill."""
    rng = np.random.default_rng(20)
    total_bill = np.round(rng.uniform(8.0, 55.0, n), 2)
    tip = np.round(0.10 * total_bill + 1.2 + rng.normal(0, 0.55, n), 2)
    size = np.clip(np.round(total_bill / 13 + rng.normal(0, 0.5, n)), 1, 6).astype(int)
    return pd.DataFrame({"total_bill": total_bill, "tip": tip, "size": size})


def strongest_pair(corr: pd.DataFrame) -> tuple[str, str, float]:
    """Return (col_a, col_b, r) for the largest off-diagonal correlation.

    The diagonal and lower triangle are masked with NaN so a column cannot win
    against itself and each pair is considered once.
    """
    mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    pairs = corr.where(mask).stack(future_stack=True)
    a, b = pairs.idxmax()
    return a, b, float(pairs.max())


if __name__ == "__main__":
    tips = make_tips()

    # 1. Correlation matrix of the numeric columns.
    corr = tips.corr(numeric_only=True)
    print("Correlation matrix")
    print(corr.round(4).to_string())

    # 2. Strongest positive off-diagonal pair.
    a, b, r = strongest_pair(corr)
    print(f"\nStrongest positive correlation: {a} vs {b}, r = {r:.4f}")

    # 3. Scatter with a least-squares trend line.
    x = tips[a].to_numpy()
    y = tips[b].to_numpy()
    slope, intercept = np.polyfit(x, y, deg=1)
    xs = np.linspace(x.min(), x.max(), 100)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.6, color="#3273dc", label="Orders")
    ax.plot(xs, slope * xs + intercept, color="#d9534f", linewidth=2,
            label=f"Fit: tip = {slope:.4f} x bill + {intercept:.4f}")
    ax.set_title(f"Tip vs total bill (r = {r:.2f}, n = {len(tips)})")
    ax.set_xlabel("Total bill ($)")
    ax.set_ylabel("Tip ($)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    with tempfile.TemporaryDirectory() as workspace:
        fig.savefig(Path(workspace) / "corr_scatter.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"slope     = {slope:.4f} dollars of tip per dollar of bill")
    print(f"intercept = {intercept:.4f} dollars")
    print(f"r squared = {r ** 2:.4f}")

    # 4. Proportional? Compare the tip rate across bill quartiles.
    tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100
    quartiles = pd.qcut(tips["total_bill"], 4,
                        labels=["Q1 cheapest", "Q2", "Q3", "Q4 priciest"])
    print("\nMean tip percentage by total_bill quartile")
    print(tips.groupby(quartiles, observed=True)["tip_pct"].mean().round(2).to_string())
```

**A correlation matrix is every column asked about every other column.**
`tips.corr(numeric_only=True)` takes the three numeric columns and fills a 3×3
grid: row `tip`, column `total_bill` holds how tightly those two move together.
The number in each cell runs from -1 to +1. `+1` means they move in perfect
lockstep upward, `-1` means perfectly opposite, `0` means no straight-line
relationship at all. The diagonal is all `1.0` because a column matches itself
perfectly, and the grid is a mirror across that diagonal, because "how does tip
move with bill" and "how does bill move with tip" are the same question.
`numeric_only=True` keeps the text columns out; without it pandas tries to turn
`"Sat"` into a number and stops with `ValueError`.

**Masking is the difference between an answer and a tautology.** The mask
`np.triu(np.ones(corr.shape, dtype=bool), k=1)` is a grid of `True` and `False`
where only the cells *above* the diagonal are `True` — `k=1` is what pushes it
one step off the diagonal. `corr.where(mask)` blanks everything else.
`.stack(future_stack=True)` then folds that grid into a flat list keyed by pairs,
so `idxmax` returns the two column names and `max` returns the coefficient. Skip
the mask and the diagonal wins every time, at 1.0, and your program confidently
reports that `total_bill` is strongly correlated with `total_bill`. Skip only the
`k=1` and you get the same. The `future_stack=True` flag pins down what pandas
does with the blanked cells so this answer does not change under you at the next
upgrade.

**`np.polyfit(x, y, deg=1)` draws the one straight line that misses by the
least.** `deg=1` means a straight line — degree 1, so `y = slope*x + intercept`.
It finds the pair of numbers that make the total of the squared vertical gaps
between the line and the dots as small as possible. It returns them highest
power first, which is why the unpacking is `slope, intercept` in that order. The
argument order matters enormously and nothing warns you: the first array is the
horizontal axis. Swap them here and the slope comes back as roughly 9 instead of
roughly 0.1, because you have asked how many dollars of *bill* accompany a dollar
of *tip*.

**The intercept is the answer to the homework, and it is one number in the
middle of the output.** The fit says `tip = 0.0999 x bill + 1.0987`. Ten cents
per dollar, plus a fixed $1.10 that appears whatever the bill is. Proportional
would mean a line through the origin — spend nothing, tip nothing; spend double,
tip double. This line starts a dollar and ten above zero, so the small bills
carry a bigger percentage. The quartile table proves it from the other
direction, with no model at all: 18.45% on the cheapest quarter of bills, 12.46%
on the priciest. Two independent routes, same conclusion.

**r squared is r times itself, and it has a plain meaning.** 0.9053 squared is
0.8196: about 82% of the variation in tips moves in step with the bill. The
remaining 18% is everything the bill does not know about — service, mood, the
size of the party, whether it was somebody's birthday. Squaring is useful
because it converts a coefficient people argue about into a share people can
picture. An `r` of 0.5 sounds like "half"; its r squared is 0.25, which is a
quarter, and that is the honest impression.

**`pd.qcut` cuts by rank, not by value.** `qcut(bills, 4)` sorts the bills and
slices them into four groups of twenty rows each, so every quartile carries the
same weight. Its cousin `pd.cut` slices the *range* into four equal-width bands
instead, which on skewed data can leave one band with sixty rows and another
with two. For "how do cheap tables behave versus expensive tables", equal group
sizes is the right cut. `observed=True` on the `groupby` says: only report the
labels that actually contain rows.

**And the sentence this whole page exists for.** The strongest pair in this
matrix is `total_bill` and `tip` at r = 0.9053. That is a genuine, strong,
useful association — you could predict a tip from a bill and be right most of
the time. It is **not** a statement that the bill causes the tip. Correlation
never carries that. A third thing standing behind both columns produces exactly
this picture and leaves no trace in the arithmetic: party size, in this very
frame, correlates with the bill at 0.8816 and with the tip at 0.7785, so bigger
parties inflate both. Ice cream sales and drownings rise together every summer,
and the cause of both is the weather. The only way to earn the word "cause" is
to change one thing on purpose and watch what the other one does. Write "moves
with". Write "predicts". Do not write "causes".

**About the shipped file.** The chart code is exactly what you write, with one
difference: this download wraps `savefig` in a `tempfile.TemporaryDirectory`, so
the PNG renders, is proven to exist, and is deleted with the folder on the way
out, leaving nothing behind for the automated check to trip over. Your own
`problem-06-correlations.py` saves `corr_scatter.png` beside the script so you
can look at it. Its docstring also still carries the older name
`hw-06-correlations.py` from an earlier draft of this assignment.

## Run it

Copy the worked answer on this page into `problem-06-correlations.py` and run it:

```bash
pip install pandas numpy matplotlib
python problem-06-correlations.py
```

The data is generated inline from a fixed seed, so it reads no files and prints
the same numbers on every machine. The scatter is drawn with the non-interactive
`Agg` backend into a throwaway temporary directory, so nothing is left in your
folder. Your own `problem-06-correlations.py` saves `corr_scatter.png` beside
the script instead. The `-solution` suffix keeps the download from colliding
with your file.

## Common bugs to catch

- **`ValueError: could not convert string to float: 'Sat'`.** You called
  `.corr()` on a frame with text columns and no `numeric_only=True`. Add it.
- **The strongest pair is a column against itself, at r = 1.0000.** You did not
  mask the diagonal, or you used `np.triu(..., k=0)` instead of `k=1`. `k=1`
  starts the triangle one cell above the diagonal.
- **`TypeError: cannot unpack non-iterable numpy.str_ object`** from
  `a, b = pairs.idxmax()`. Your masked grid collapsed to a plain index instead
  of a pair index, usually because you stacked before masking. Mask first, then
  stack.
- **The slope is about 9 instead of about 0.1.** `x` and `y` are the wrong way
  round in `np.polyfit`. The first array is the horizontal one. Nothing warns
  you about this — the fit is perfectly valid, it just answers a question you
  did not ask.
- **`RankWarning: Polyfit may be poorly conditioned`.** Your `x` has almost no
  spread — every value nearly the same — so there is no unique line through the
  points. Check `x.min()` and `x.max()`.
- **`ValueError: Bin edges must be unique`** from `pd.qcut`. Too many identical
  values, so two quartile boundaries land on the same number. Either use fewer
  bins or pass `duplicates="drop"`, and say in a comment that you did.
- **`r` is near zero but the scatter clearly shows a shape.** Pearson's `r` only
  sees straight lines. A curve, a U, or a step scores near zero. Try
  `df.corr(method="spearman")`, which ranks the values first and catches any
  relationship that only ever goes one direction, and keep looking at the
  picture.
- **The trend line is drawn as a jagged mess instead of a straight line.** You
  plotted the fit against the raw, unsorted `x` values. Build a clean sorted
  range with `np.linspace(x.min(), x.max(), 100)` and plot the line against
  that.
- **The scatter is a solid unreadable blob.** Too many overlapping points. Lower
  `alpha`, shrink the marker with `s=`, or switch to a 2-D histogram.
- **Somebody reads your r = 0.90 aloud as "bills cause tips".** This is the
  actual bug. It has no traceback and it ships. The fix is in your wording:
  write the finding as "tips move with bills" and put the intercept and the
  quartile table right next to it.

## Under the hood

<details>
<summary>Under the hood — what Pearson's r actually computes, and what it cannot see</summary>

Pearson's `r` is a ratio. Take how much the two columns vary *together* — their
covariance — and divide it by how much each one varies on its own. In symbols,
`r = cov(x, y) / (std(x) * std(y))`. The division is what pins the answer between
-1 and +1 and makes it unitless, so dollars against dollars and centimetres
against kilograms both land on the same scale and can be compared.

The mechanical way to picture it: subtract each column's mean from itself, so
both are centred on zero. Multiply the two centred columns row by row. A row
where both values sit above their means gives a positive product; so does a row
where both sit below. A row where one is above and the other below gives a
negative one. Average those products and scale, and you have `r`. It is a vote,
row by row, on whether the two columns lean the same way.

Two consequences follow directly and both matter.

It only sees straight lines. Anscombe's quartet is four small data sets with
identical means, identical variances, an identical `r` of 0.816 and an identical
best-fit line — and four completely different pictures. One is a clean linear
relationship, one is a perfect curve, one is a straight line with a single
outlier dragging it, and one is a vertical stack plus one distant point that
invents the entire correlation on its own. `r` cannot tell them apart. A
scatter plot can, instantly. That is why "always plot it" is a rule and not a
suggestion.

And it is not robust. One extreme point can create or destroy a correlation on
its own, because the products in that average scale with distance from the mean.
`df.corr(method="spearman")` guards against this: it replaces every value with
its rank — 1st, 2nd, 3rd — before doing the same arithmetic, so an outlier is
just "the biggest one" rather than "a thousand times the mean". Spearman also
catches any relationship that only ever moves one direction, even a curved one.
When Pearson and Spearman disagree sharply, that disagreement is itself the
finding: look for outliers or a curve.

</details>

<details>
<summary>Under the hood — why "correlation is not causation" has a specific shape, and what would settle it</summary>

The slogan is easy to repeat and easy to under-use. It helps to know the three
specific ways a correlation between A and B can appear with no arrow from A to
B.

**The arrow points the other way.** B causes A. Hospitals correlate with
sickness; the sickness came first.

**A third thing causes both.** This is the confounder, and it is the common
case. Ice cream sales correlate with drowning deaths, and hot weather drives
both. In this very frame, party `size` correlates 0.8816 with the bill and
0.7785 with the tip — a bigger table raises both numbers, so part of the
bill-to-tip correlation is really party size showing up twice.

**Selection.** The correlation is real inside your data and absent outside it,
because of how the rows were chosen. Look only at restaurant customers who
stayed for dessert, and you have quietly filtered on satisfaction, which touches
both the bill and the tip.

What would actually settle a causal question is an intervention: change one
thing on purpose, hold everything else steady, and see whether the other moves.
That is what a randomised experiment — an A/B test, a clinical trial — buys you.
Randomising who gets the treatment breaks every link between the treatment and
any third thing, because a coin flip cannot be caused by the weather or the
party size. When an experiment is impossible or unethical, whole fields exist to
extract causal claims from observed data anyway, using designs with names like
instrumental variables, difference-in-differences and regression discontinuity.
Every one of them works by finding something in the world that behaves *like* a
coin flip. None of them is `df.corr()`.

The practical version, for the report you will write next week: state the
association, state the size of it, state what you controlled for, and stop.
"Tips move with bills, r = 0.91, and the relationship is not proportional —
smaller bills carry a higher percentage" is a complete, defensible,
decision-ready finding. Adding "so raising prices will raise tips" is an
unearned extra sentence that could cost somebody money.

</details>

<details>
<summary>Under the hood — r squared, and the trap of reading it as a grade</summary>

Squaring `r` gives the **coefficient of determination**: the share of the
variation in one column that travels with the other. Here 0.9053² = 0.8196, so
about 82% of the up-and-down in tips moves in step with the bill and 18% does
not. Squaring is useful mainly because it deflates the impression a raw
coefficient gives. An `r` of 0.5 sounds like "half of it". Its r squared is 0.25
— a quarter — which is the honest picture.

Two traps come with it.

The first is treating it as a score. A high r squared does not mean the model is
correct, only that it tracks this particular data. Fit a wiggly enough curve
through any set of points and the r squared goes to 1.0, having learned the
noise perfectly and the world not at all. That is overfitting, and it is why
models get judged on data they were not fitted to.

The second is expecting it to be big. In physics an r squared of 0.99 is normal
and 0.90 suggests a broken instrument. In anything involving human beings, 0.30
can be a career-making result, because people are noisy and any single
measurement of them is fighting hundreds of unmeasured influences. The number
means nothing without its field.

</details>

## Acceptance checklist

- [ ] `python problem-06-correlations.py` runs with no traceback and no
      warnings, on a machine with no display attached.
- [ ] The printed output matches the expected block exactly.
- [ ] The strongest pair is found in code, not by eye, and is
      `total_bill vs tip` at `r = 0.9053` — never a column against itself.
- [ ] The slope is about `0.0999` and the intercept about `1.0987`. If the slope
      is about 9, your `x` and `y` are swapped.
- [ ] `corr_scatter.png` exists, has a title, both axis labels with units, a
      legend and a visible straight fit line, and is recreated after you delete
      it.
- [ ] The quartile table shows the tip percentage falling from 18.45 to 12.46.
- [ ] Your written verdict answers "no, not proportional", explains the
      intercept, and uses "moves with" rather than "causes".
- [ ] The file has a top-of-file docstring and typed functions.
- [ ] The file is committed to Git with a message like
      `Add Week 13 homework 6: correlation analysis`.

## Stretch

- Draw the correlation matrix as a heatmap:
  `sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)`. `center=0` is the
  part that matters — it puts the neutral colour at zero, so positive and
  negative read as opposite colours instead of just different shades.
- Run `tips.corr(method="spearman")` alongside the Pearson matrix and print them
  side by side. Where they differ, work out whether an outlier or a curve is
  responsible.
- Add a `tip_pct` line to the chart on a second y axis with `ax.twinx()`, and
  watch the falling percentage and the rising tip appear in the same picture.
- Load Anscombe's quartet (`sns.load_dataset("anscombe")`), compute `r` for each
  of its four groups, and plot all four. Same coefficient, four different
  worlds. Keep the image; it is the best argument you will ever have for
  plotting before concluding.
- Fit `deg=2` instead of `deg=1` and compare the r squared. Then decide whether
  the improvement is real or whether you have just given the model more room to
  memorise noise.
- Install seaborn, swap in the genuine `sns.load_dataset("tips")`, and run the
  whole script unchanged. Check whether the real data agrees: strong
  correlation, non-zero intercept, falling tip percentage as bills grow.
