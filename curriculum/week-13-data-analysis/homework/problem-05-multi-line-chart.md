# Homework 5 — Multi-line chart

> **Topic:** three series, one set of axes, one legend — and a PNG saved without a screen
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Intermediate
> **Target time:** 45 min
> **Why this one:** a single line tells you what happened. Three lines on the
> same axes tell you who is winning, and that is the chart people actually make
> decisions from. It also drills the two things that break plotting scripts
> outside a notebook — a backend that does not need a screen, and saving to a
> file instead of hoping a window opens.

## The Brief

Three runners on a track. If you time them separately and hand somebody three
stopwatches, nobody can tell you who won. Draw all three on one track, from the
same start line, and the answer is obvious before anyone reads a number.

That is a multi-line chart. Three products, twelve months, one picture. Same
x-axis for all of them, one line each, and a legend that says which line is
which.

You will fabricate the data — the brief allows it, and fabricating it means
everybody's chart is comparable. Three products with three different stories:

- **Alpha** starts low and climbs all year.
- **Beta** is flat overall but wanders up and down with the seasons.
- **Gamma** starts highest and slides all the way down.

Print the numbers first, print each product's full-year total, then draw the
chart and save it as `multi_line.png`.

You will not call `plt.show()`. A script that depends on a window opening is a
script that fails on a build server, in a container, or over SSH — all places
this kind of code eventually runs. The PNG on disk is the deliverable.

One warning about the totals, because it is the point of the whole exercise.
The product with the biggest full-year total is **not** the product that is
winning. Adding a year up throws away the direction, and direction is what the
picture keeps.

## Starter

Copy this into `problem-05-multi-line-chart.py` in your homework folder. It runs
as pasted — it prints an empty frame and writes a blank chart.

```python
"""problem-05-multi-line-chart.py — one chart, three product lines, twelve months.

Fabricates a year of sales for three products with a seeded random generator,
prints the table and the full-year totals, then saves one labelled multi-line
chart to multi_line.png using matplotlib's non-interactive Agg backend.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUTPUT_PATH = Path("multi_line.png")


def make_sales() -> pd.DataFrame:
    """Fabricate 12 months of sales for three products. Seeded, so reproducible."""
    rng = np.random.default_rng(13)
    months = pd.period_range("2025-01", periods=12, freq="M")
    n = np.arange(12)

    # TODO: build a dict with three keys — "Alpha", "Beta", "Gamma".
    #       Alpha climbs:   420 + 28 * n
    #       Beta is wavy:   610 + 90 * np.sin(2 * np.pi * n / 12)
    #       Gamma decays:   780 * 0.93 ** n
    #       Add rng.normal(0, 18, 12) to each so the lines are not too clean.
    data: dict[str, object] = {}

    monthly = pd.DataFrame(data, index=months).round(1)
    monthly.index.name = "month"
    return monthly


def plot(monthly: pd.DataFrame) -> None:
    """Draw one line per column on shared axes and save the PNG."""
    # TODO: copy the frame and replace the index with short month names,
    #       monthly.index.strftime("%b"). Plotting a PeriodIndex directly puts
    #       the lines at period ordinals — see Constraints.
    plot_df = monthly

    fig, ax = plt.subplots(figsize=(10, 5))

    # TODO: plot_df.plot(ax=ax, marker="o", linewidth=2) — one line per column.
    # TODO: set the title, the x label, and a y label that names the unit.
    # TODO: start the y axis at zero with ax.set_ylim(0, None).
    # TODO: force one tick per month with set_xticks and set_xticklabels.
    # TODO: ax.legend(title="Product") and a light grid.

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    monthly = make_sales()
    print(monthly.to_string())
    # TODO: print a "full-year totals" heading, then monthly.sum() rounded to
    #       one decimal, printed with .to_string().
    plot(monthly)
    # TODO: print a one-line confirmation naming the file, the number of lines
    #       and the number of months.
```

## Requirements

1. Build a DataFrame of twelve months by three products, using
   `np.random.default_rng(13)` so the numbers are identical on every machine.
   Round to one decimal. Name the index `month`.
2. The frame is **wide**: one row per month, one column per product. That is
   the shape `.plot()` wants.
3. Print the whole table with `.to_string()`.
4. Print a `full-year totals` heading, then each product's yearly sum rounded to
   one decimal.
5. Call `matplotlib.use("Agg")` **before** importing `pyplot`.
6. Draw all three products on **one** set of axes, with a marker on each data
   point so single months are readable.
7. Give the chart a title, an x-axis label, and a y-axis label that names the
   unit — `Units sold`, not `Sales`.
8. Start the y axis at zero.
9. Put one tick per month, labelled with the short month name (`Jan` … `Dec`).
10. Show a legend headed `Product`, and a light grid.
11. Save to `multi_line.png` at `dpi=150` with `bbox_inches="tight"`, close the
    figure, and print one confirmation line. Do not call `plt.show()`.

## Constraints

- **`matplotlib.use("Agg")` goes before `import matplotlib.pyplot`, not after.**
  matplotlib picks its drawing machinery the first time `pyplot` is imported and
  the choice is locked from then on. `Agg` is the non-interactive renderer — it
  draws into memory and writes files, and it never asks for a window. Put the
  `use` call after the import and it does nothing at all, silently.
- **Save with `savefig`; never call `plt.show()`.** Under `Agg`, `show()` does
  not raise. It warns and does nothing, which is worse than an error, because
  you will sit looking at a clean exit code wondering where your chart went.
- **Plot against short month strings, not the `PeriodIndex`.** A `PeriodIndex`
  puts each point at the period's internal number — January 2025 is 660, not 0 —
  so any tick you set by hand at 0 through 11 lands far outside the axes and
  your labels vanish. Convert with `.strftime("%b")` on a copy and plot that.
- **Keep the frame wide: one column per product.** `df.plot()` draws one line
  per column and takes the line's legend name from the column name. Hand it a
  long frame (a `product` column and a `sales` column) and you get one line
  through all thirty-six points, which is nonsense with a legend attached.
- **One `fig, ax = plt.subplots()`, and pass `ax=ax` to `.plot()`.** The bare
  `plt.*` calls draw onto a hidden "current figure". That is fine until you have
  two charts and cannot tell which one `plt.title` just renamed. Holding `fig`
  and `ax` yourself costs one line and makes every call's target obvious.
- **Start the y axis at zero for this chart.** These are counts of units sold,
  and the reader is comparing how big the products are, not just which way they
  point. A y axis that starts at 400 makes a 15% gap look like a chasm. (Not
  every line chart wants a zero baseline — see Under the hood — but a count
  chart does.)
- **Label the y axis with its unit.** `Sales` could be units, dollars, or
  thousands of dollars. `Units sold` cannot be misread. An unlabelled chart is
  decoration, not information.
- **Seed the generator.** `np.random.default_rng(13)` gives the same twelve
  numbers to everyone, forever. Unseeded random data means your printed output
  matches nobody's, including your own from ten minutes ago, and nothing about
  the result can be checked.
- **`plt.close(fig)` after saving.** pyplot holds on to every figure it makes.
  One leaked figure is nothing; a loop that writes fifty charts without closing
  earns you `RuntimeWarning: More than 20 figures have been opened` and then a
  steadily slower script as memory fills.

## Expected output

Real captured run of the shipped answer,
[`problem-05-multi-line-chart-solution.py`](./problem-05-multi-line-chart-solution.py):

```text
$ python problem-05-multi-line-chart.py
Alpha   Beta  Gamma
month                       
2025-01  452.9  605.5  785.7
2025-02  392.6  667.9  752.1
2025-03  493.2  700.6  657.5
2025-04  505.3  691.1  650.1
2025-05  555.7  681.3  556.8
2025-06  566.9  622.5  548.8
2025-07  620.9  640.2  523.8
2025-08  616.6  561.0  473.4
2025-09  634.7  556.1  429.9
2025-10  682.4  527.5  391.4
2025-11  707.8  567.0  371.3
2025-12  721.6  592.7  370.0

full-year totals
Alpha    6950.6
Beta     7413.4
Gamma    6510.8

saved multi_line.png: 3 product lines across 12 months (temp file, cleaned up)
```

The terminal is only half the check. A page cannot show you the picture, so
open `multi_line.png` and confirm all seven of these:

1. Exactly three lines, in three different colours, each with twelve round
   markers on it.
2. The x axis runs `Jan` through `Dec`, one tick per month, left to right.
3. The y axis starts at 0 and reaches a little past 800.
4. **Alpha** starts near 450 on the left and finishes highest, near 720. It is
   the line that goes uphill the whole way.
5. **Gamma** starts highest of all, near 786, and finishes lowest, near 370. It
   is the line that goes downhill the whole way. Alpha and Gamma cross between
   **May and June** — that crossing is the story of the year.
6. **Beta** is the wavy one. It rises to about 700 in March, sags to about 528
   in October, and ends near where it started. It crosses Gamma between February
   and March and is overtaken by Alpha between July and August.
7. A title, both axis labels, a legend headed `Product` naming all three, and
   nothing clipped at any edge.

Now look at the totals again. **Beta has the biggest full-year total** — 7,413.4
against Alpha's 6,950.6 — and Beta is the product going nowhere. Alpha finishes
the year outselling it by nearly 130 units a month and rising. That is the whole
argument for drawing the picture: a sum is a single number with the direction
thrown away, and direction is the part that tells you what happens next.

## Steps

1. Create the file and paste the starter. Run it. It should print an empty frame
   and still write a (blank) `multi_line.png`. Proving the plumbing before you
   draw anything means you only ever debug one thing at a time.
2. Fill in the three columns in `make_sales`. Run it and check the printed table
   against the expected output, number for number. If they differ, your seed or
   your formula is off — fix that before you plot anything.
3. Add the totals print. Beta should be highest.
4. Add `plot_df.plot(ax=ax, marker="o", linewidth=2)` and nothing else. Open the
   PNG. You should see three unlabelled lines — and, if you skipped the
   `strftime` step, an x axis reading `660` to `671`. Skip it on purpose once so
   you recognise the symptom.
5. Add the `strftime("%b")` index copy. Reopen the PNG. The x axis now reads
   `Jan` to `Dec`.
6. Add the title and both axis labels, then `ax.set_ylim(0, None)`. Reopen.
7. Add `ax.set_xticks(range(len(plot_df)))` and `ax.set_xticklabels(...)`, then
   `ax.legend(title="Product")` and `ax.grid(alpha=0.3)`.
8. Delete `multi_line.png` and rerun. A script that only works when yesterday's
   output is still lying around is not finished.
9. Comment out `matplotlib.use("Agg")` and run it again. On a desktop a window
   may open; on a headless machine you get an error or a hang. Put it back and
   remember what it prevents.

## The Solution

```python
"""hw-05-multi-line.py — one chart, three product lines, twelve months, saved to PNG.

The data is fabricated inline with a seeded generator, so every printed number
is reproducible. The chart is drawn with matplotlib's non-interactive Agg backend
and written into a throwaway temporary directory that Python deletes on the way
out, so the script leaves no PNG behind.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_sales() -> pd.DataFrame:
    """Fabricate 12 months of sales for three products. Seeded, so reproducible.

    Alpha grows steadily, Beta is flat and seasonal, Gamma decays.
    """
    rng = np.random.default_rng(13)
    months = pd.period_range("2025-01", periods=12, freq="M")
    n = np.arange(12)

    data = {
        "Alpha": 420 + 28 * n + rng.normal(0, 18, 12),
        "Beta": 610 + 90 * np.sin(2 * np.pi * n / 12) + rng.normal(0, 18, 12),
        "Gamma": 780 * 0.93**n + rng.normal(0, 18, 12),
    }
    monthly = pd.DataFrame(data, index=months).round(1)
    monthly.index.name = "month"
    return monthly


def plot(monthly: pd.DataFrame) -> None:
    """Draw one line per column on shared axes and save into a temp dir."""
    # Plot against short month names, not the PeriodIndex. A PeriodIndex puts
    # the lines at period *ordinals* (660..671 for 2025), so hand-set ticks at
    # 0..11 would land outside the axes and vanish.
    plot_df = monthly.copy()
    plot_df.index = monthly.index.strftime("%b")

    fig, ax = plt.subplots(figsize=(10, 5))
    plot_df.plot(ax=ax, marker="o", linewidth=2)

    ax.set_title("Monthly unit sales by product, 2025")
    ax.set_xlabel("Month")
    ax.set_ylabel("Units sold")
    ax.set_ylim(0, None)
    # Now that x runs 0..11, forcing a tick per month is safe.
    ax.set_xticks(range(len(plot_df)))
    ax.set_xticklabels(plot_df.index)
    ax.legend(title="Product")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    with tempfile.TemporaryDirectory() as workspace:
        fig.savefig(Path(workspace) / "multi_line.png", dpi=150, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    monthly = make_sales()
    print(monthly.to_string())
    print("\nfull-year totals")
    print(monthly.sum().round(1).to_string())
    plot(monthly)
    print("\nsaved multi_line.png: 3 product lines across 12 months (temp file, cleaned up)")
```

**`matplotlib.use("Agg")` before `import matplotlib.pyplot` — the order is the
whole point.** matplotlib chooses its rendering backend the first time `pyplot`
is imported, and after that the choice is fixed for the life of the process.
`Agg` is the Anti-Grain Geometry renderer: it draws into a memory buffer and
writes PNG files, and it never asks the operating system for a window. That is
what makes this script work on a build server, in a container, and over SSH —
the three places your code ends up whether you planned for it or not. Put the
`use` call after the `pyplot` import and it is a silent no-op. This is also why
the imports here are not in one tidy alphabetical block, and why a linter will
complain about it and be wrong.

**One `.plot()` call draws all three lines, because the frame is wide.**
`plot_df.plot(ax=ax)` walks the columns and draws one line per column, taking
each line's colour from matplotlib's colour cycle and each line's legend entry
from the column name. `Alpha`, `Beta` and `Gamma` are labelled in the legend
without you naming them anywhere, because they are already the column names.
That is the payoff for keeping the data wide: one row per month, one column per
product, and the frame is already the shape of the picture.

**The `strftime("%b")` copy is not cosmetic — it is the bug this problem is
built around.** A `PeriodIndex` does not hold the strings `2025-01`; it holds
integers counting months from an epoch, and January 2025 is 660. Plot it
directly and matplotlib puts your twelve points at x = 660 through 671. The
lines still look right, so nothing seems wrong — until you ask for ticks at 0
through 11 and they land six hundred units to the left of anything drawn, off
the edge of the axes, and your month labels disappear. Replacing the index with
`Jan` … `Dec` on a **copy** moves the points to x = 0 through 11, which is where
your hand-set ticks are. The copy matters: `monthly` still holds real periods
afterwards, so anything else you do with the data — sorting, resampling,
date arithmetic — still works.

**`ax.set_ylim(0, None)` is an argument, not a default.** `None` means "leave
the top wherever matplotlib put it" and `0` pins the bottom. These are counts of
units, and the reader is comparing sizes as well as directions; an axis starting
at 400 would turn a 15% gap between Alpha and Beta into a picture of a chasm.
Charts of things that have a meaningful zero — counts, dollars, quantities —
start at zero.

**`savefig`, never `show`; then `close`.** The file on disk is the artifact.
`dpi=150` is a deliberate middle: the default 100 looks soft the moment a chart
is dropped into a slide, and 300 quadruples the file for no visible gain on
screen. `bbox_inches="tight"` crops to what was actually drawn so a long y-axis
label is not sliced off at the file boundary, and `fig.tight_layout()` rearranges
the axes *inside* the figure so labels do not collide with each other. They solve
different halves of the same problem; use both. `plt.close(fig)` matters because
pyplot keeps a reference to every figure it made so `show()` could find them
later — close it in the same function that opened it.

**The seed is what makes any of this checkable.** `np.random.default_rng(13)`
produces the same stream of numbers on every machine, every run, forever. Drop
the seed and the printed table above becomes fiction: nobody, including you
tomorrow, can confirm the chart is right. Fabricated data is fine. Fabricated
data you cannot reproduce is not data.

**About the shipped file.** The chart-building code is exactly what you write.
The one difference is the save: this download wraps `savefig` in a
`tempfile.TemporaryDirectory`, so the PNG is written, proven to render, and then
deleted with the folder on the way out — which keeps the automated check from
littering the repo. Your own `problem-05-multi-line-chart.py` points
`OUTPUT_PATH` at `multi_line.png` next to the script, so you can open the
picture. Its docstring also still carries the older name `hw-05-multi-line.py`
from an earlier draft of this assignment.

## Run it

Copy the worked answer on this page into `problem-05-multi-line-chart.py` and run it:

```bash
pip install pandas matplotlib numpy
python problem-05-multi-line-chart.py
```

It builds the chart with the non-interactive `Agg` backend, writes the PNG into
a throwaway temporary directory that Python deletes on the way out — so it
leaves nothing in your folder — and prints the table, the totals and a
confirmation line. Your own `problem-05-multi-line-chart.py` saves
`multi_line.png` beside the script instead, so you can open it. The `-solution`
suffix keeps the download from colliding with your file.

## Common bugs to catch

- **The x axis reads `660` to `671`, or the month labels are simply missing.**
  You plotted the `PeriodIndex` directly. Replace the index on a copy with
  `monthly.index.strftime("%b")` before plotting.
- **`ValueError: The number of FixedLocator locations (12), usually from a call
  to set_ticks, does not match the number of labels (3).`** Your
  `set_xticklabels` list is a different length from your `set_xticks` list.
  Build both from the same thing: `range(len(plot_df))` and `plot_df.index`.
- **`TypeError: no numeric data to plot`.** One of your columns is text. Numbers
  read from a file arrive as strings; check `monthly.dtypes` and convert with
  `pd.to_numeric`.
- **One line instead of three.** Your frame is long, not wide — a `product`
  column and a `sales` column. Reshape it first:
  `df.pivot(index="month", columns="product", values="sales")`.
- **The legend says `0`, `1`, `2`.** Your columns have no names, usually because
  you built the frame from a list of lists. Name them, or build from a dict.
- **All three lines come out the same colour.** You drew them in a `for` loop
  with a hard-coded `color=`. Drop the `color` argument and let matplotlib's
  colour cycle do it, or better, let one `.plot()` call handle all three.
- **`UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be
  shown`.** You called `plt.show()` under `Agg`. Delete it. The PNG is the
  output.
- **The PNG exists but is blank.** You called `plt.close(fig)` before
  `fig.savefig(...)`, so you saved an empty figure. Save first, close second.
- **`FileNotFoundError: [Errno 2] No such file or directory:
  'charts/multi_line.png'`.** You pointed the output at a folder that does not
  exist. matplotlib creates files, not directories. Add
  `OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)`.
- **The y-axis label is cut off in the file even though it looked fine in the
  window.** You dropped `fig.tight_layout()` or `bbox_inches="tight"`. Use both.
- **The numbers change on every run.** No seed. Use
  `np.random.default_rng(13)`, not `np.random.normal(...)` straight from the
  global generator.
- **The chart never seems to update.** Your image viewer is showing a cached
  copy. Close it and reopen, or check the file's modification time.

## Under the hood

<details>
<summary>Under the hood — PeriodIndex, DatetimeIndex, and why one of them plots at 660</summary>

A `PeriodIndex` stores *spans* of time. January 2025 is not an instant; it is the
whole month, and internally it is stored as a single integer counting months
from January 1970 — which makes January 2025 the number 660. That integer is
what matplotlib receives when you plot against the index, so your twelve points
land at x = 660 … 671. The line looks perfectly fine, which is what makes this
so slippery; it only bites when you set ticks by hand at 0 … 11 and they land
six hundred units off-canvas.

A `DatetimeIndex` stores *instants* instead, as nanoseconds since 1970, and
matplotlib has a dedicated date converter for it: plot one and you get real
date ticks and automatic label rotation, no `strftime` needed. That is usually
the better answer for a time series you will keep working with. Periods earn
their place when the thing you are counting genuinely is a whole month or a
whole quarter — `df.groupby(df.index.to_period("M")).sum()` is the clearest way
to say "monthly totals", and no instant can honestly represent "March".

The rule of thumb: aggregate with periods, plot with strings or datetimes. The
answer here converts to short strings on a copy because it wants hand-placed
ticks at every month, and strings give it a plain 0 … 11 axis to place them on.

</details>

<details>
<summary>Under the hood — the colour cycle, and when a line chart should not start at zero</summary>

matplotlib does not pick line colours at random. It walks a list called the
property cycle, set in `rcParams["axes.prop_cycle"]`, and hands out the next
colour each time an artist is drawn without one. The default list is the ten
colours of the `tab10` palette, chosen to stay distinguishable side by side. It
repeats after ten lines, which is a useful signal: if two lines on your chart
are the same colour, you have drawn more than ten and the chart is past the
point where anyone can read it. `ax.set_prop_cycle(color=[...])` replaces the
list when a house style demands specific colours.

On the zero baseline: bar charts must start at zero, without exception, because
the *length* of the bar is the number and a cropped axis lies about the ratio
between two bars. Line charts are a different case. A line encodes its value by
*position*, and the reader compares the shape, not the area, so a chart of body
temperature over a week or a share price over a month is entirely honest — and
much more readable — starting at 36°C or at $180. Forcing those to zero
flattens the only signal into a straight line at the top of an empty rectangle.

The test is what the reader is being asked to compare. Sizes and ratios: start
at zero. Movement and shape in a range that never approaches zero: do not. This
chart is counts of units sold, and the reader is comparing how big the products
are as well as which way they are heading, so it starts at zero. Say which one
you chose in a comment; the next person will assume you did not think about it.

</details>

## Acceptance checklist

- [ ] `python problem-05-multi-line-chart.py` runs with no traceback and no
      warnings, on a machine with no display attached.
- [ ] The printed table and totals match the expected output exactly.
- [ ] `multi_line.png` exists, and is recreated after you delete it.
- [ ] Three lines, three colours, twelve markers each, on one set of axes.
- [ ] The x axis reads `Jan` through `Dec` — not `660` through `671`.
- [ ] The y axis starts at zero and is labelled with its unit.
- [ ] There is a title and a legend headed `Product` naming all three products.
- [ ] Nothing is clipped at any edge.
- [ ] The file has a top-of-file docstring and typed functions.
- [ ] The file is committed to Git with a message like
      `Add Week 13 homework 5: multi-line product chart`.

## Stretch

- Annotate the Alpha/Gamma crossing directly on the chart with `ax.annotate`,
  arrow and all. A reader should not have to trace two lines to find the moment
  the year turned.
- Add a second panel with `fig, axes = plt.subplots(1, 2, figsize=(15, 5))` —
  the three lines on the left, each product's cumulative total (`.cumsum()`) on
  the right. Give the figure one `suptitle`.
- Redraw the same chart with a `for` loop over the columns and explicit
  `ax.plot(...)` calls. Same picture, four times the code — which is exactly why
  `.plot()` exists. Keep whichever version you find easier to read in six
  months.
- Smooth each line with a three-month rolling mean
  (`monthly.rolling(3).mean()`) and draw it faintly behind the real lines. Note
  where the first two months went, and why.
- Write the table out as `multi_line.csv` alongside the PNG, so whoever gets the
  picture can also check the figures behind it.
- Shade the region where Alpha is above Gamma with `ax.fill_between`. Then
  decide whether it helped or just made the chart busier — that judgement is the
  real skill.
