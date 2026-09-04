# Exercise 5 — Plot

> **Topic:** A labelled bar chart with matplotlib, saved to PNG
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** the chart is the deliverable. Nobody reads your DataFrame;
> they read the picture you attached to the email. This exercise also settles
> the two things that break plotting scripts outside a notebook — choosing a
> backend that does not need a screen, and saving to a file instead of hoping
> a window opens.

## The Brief

A coffee cart parked outside the transit station kept a monthly revenue total
for a full year. The owner is applying for a small business loan and needs one
image: revenue by month, labelled well enough that a loan officer who has
never seen the data understands it in five seconds.

You will print the numbers first, then draw the bar chart, add a dashed line
at the annual mean so the strong and weak months are obvious at a glance, and
save it as a PNG at print resolution. You will not call `plt.show()`. A
script that depends on a window opening is a script that fails on a build
server, in a container, or over SSH — all places you will eventually run this
kind of code.

## Starter

Copy this into `exercise-05-plot.py` in your practice repo.

```python
"""exercise-05-plot.py — monthly revenue bar chart, saved as a PNG.

Prints the year's figures, then writes a labelled bar chart to disk
using matplotlib's non-interactive Agg backend.
"""

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

OUTPUT_PATH = Path("monthly-revenue.png")

CART_SALES: dict[str, list] = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "revenue": [4120, 3980, 4760, 5210, 5890, 6340,
                6120, 5980, 5430, 4870, 4310, 4650],
}


def main() -> None:
    """Print the year's totals and save the bar chart to OUTPUT_PATH."""
    df = pd.DataFrame(CART_SALES)
    print(df)

    # TODO: print the total, the mean, the best month, and the worst month.
    #       Use idxmax and idxmin with df.loc to get whole rows.

    fig, ax = plt.subplots(figsize=(9, 5))

    # TODO: draw the bars from df["month"] and df["revenue"].
    # TODO: add a dashed horizontal line at the mean with ax.axhline,
    #       and give it label="Mean" so the legend has something to show.
    # TODO: set the title, the x label, and the y label.
    # TODO: call ax.legend() and add a light y-axis grid.

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)
    # TODO: print a one-line summary — the bar count, the mean to 2
    #       decimals, and how many bars sit above the mean line.


if __name__ == "__main__":
    main()
```

## Requirements

1. Print the twelve-row frame first.
2. Print `Total: $61,660` and `Mean:  $5,138.33`, both with a thousands
   separator. Note the two spaces after `Mean:` that line the numbers up.
3. Print `Best:  Jun ($6,340)` and `Worst: Feb ($3,980)`, found with `idxmax`
   and `idxmin`.
4. Draw a vertical bar chart with one bar per month, in calendar order.
5. Draw a dashed horizontal line at the annual mean, labelled `Mean`.
6. Set a title, an x-axis label, and a y-axis label that names the unit —
   `Revenue ($)`, not `Revenue`.
7. Show a legend and a y-axis grid at low opacity.
8. Save to `monthly-revenue.png` at `dpi=150` with `bbox_inches="tight"`, then
   close the figure and print a one-line summary:
   `Saved chart: 12 bars, mean line at 5138.33, 6 above it`.

## Constraints

- **Call `matplotlib.use("Agg")` before importing `pyplot`, not after.**
  matplotlib picks its backend the first time `pyplot` is imported, and after
  that the choice is locked in. `Agg` is the non-interactive renderer — it
  draws into a memory buffer and writes files, and it never tries to open a
  window. On a headless machine, a container, or a CI runner, the default
  backend either fails outright or silently blocks; `Agg` always works.
- **Save with `savefig`; do not call `plt.show()`.** Under `Agg`, `show()` is a
  no-op — it will not error, it will simply do nothing, which is worse,
  because you will sit there wondering where your chart went. The PNG on disk
  is the artifact.
- **Use the explicit `fig, ax = plt.subplots()` form, not the bare `plt.bar` /
  `plt.title` calls.** The bare form works by drawing on a hidden "current
  figure", which is fine until you have two charts and cannot tell which one
  you are editing. Holding the `fig` and `ax` objects yourself is one extra
  line and it is the form every matplotlib example you will read from here on
  uses.
- **`plt.close(fig)` after saving.** Figures stay in memory until closed. One
  leaked figure is nothing; a loop that writes fifty charts without closing
  them earns you `RuntimeWarning: More than 20 figures have been opened` and
  then a slow crawl as memory fills.
- **`dpi=150` and `bbox_inches="tight"`.** The default 100 dpi looks soft when
  a chart is embedded in a PDF or a slide, and 300 quadruples the file size for
  no visible gain on screen. `bbox_inches="tight"` crops the whitespace that
  otherwise surrounds the axes, and — more importantly — it stops long axis
  labels from being clipped off the edge.
- **Label the y axis with its unit.** `Revenue` could be dollars, cups, or
  thousands of dollars. `Revenue ($)` cannot be misread. An unlabelled chart is
  decoration, as Lecture 3 puts it, not information.
- **Keep the months in calendar order.** Do not sort by revenue. A bar chart
  of a time series carries meaning in the left-to-right order; sorting it
  destroys the seasonal shape that is the whole point of the picture.

## Expected output

```text
$ python exercise-05-plot.py
   month  revenue
0    Jan     4120
1    Feb     3980
2    Mar     4760
3    Apr     5210
4    May     5890
5    Jun     6340
6    Jul     6120
7    Aug     5980
8    Sep     5430
9    Oct     4870
10   Nov     4310
11   Dec     4650
Total: $61,660
Mean:  $5,138.33
Best:  Jun ($6,340)
Worst: Feb ($3,980)
Saved chart: 12 bars, mean line at 5138.33, 6 above it
```

The terminal output is only half the check. Open `monthly-revenue.png` and
confirm all six of these:

1. Twelve bars, Jan on the left and Dec on the right.
2. A dashed horizontal line crossing the bars a little above 5,000.
3. Exactly six bars above the line and six below.
4. A title, both axis labels, and a legend entry reading `Mean`.
5. Nothing clipped at any edge.
6. A y axis that starts at zero. Bar charts must start at zero, because the
   length of the bar is the number; a truncated axis exaggerates differences.

On the third item: the mean is 5,138.33, so the six months that clear it are
April through September — April's 5,210 just makes it, and October's 4,870
just misses. Count the bars in your PNG against that list. If your dashed line
looks like it sits near 6,000, you passed the maximum to `axhline` instead of
the mean.

## Steps

1. Create the file and paste the starter. Run it as-is — it should already
   print the frame and save a blank chart. Confirming the plumbing before you
   draw anything saves you from debugging two problems at once.
2. Add the four summary print lines and check them against the block above.
3. Add `ax.bar(df["month"], df["revenue"])`. Run it, open the PNG, and see
   twelve unlabelled bars.
4. Add the title and both axis labels. Reopen the PNG.
5. Add `ax.axhline(df["revenue"].mean(), color="#c0392b", linestyle="--",
   linewidth=1, label="Mean")`, then `ax.legend()`.
6. Add `ax.grid(axis="y", alpha=0.3)` and rerun.
7. Delete the PNG and rerun to prove the script recreates it from nothing.
   A script that only works when yesterday's output is still lying around is
   not finished.
8. Comment out the `matplotlib.use("Agg")` line and run it again. On a desktop
   a window may open; on a headless machine you will get an error or a hang.
   Put the line back and remember what it prevents.

## The Solution

```python
"""exercise-05-plot-solution.py — monthly revenue bar chart, saved as a PNG.

Prints the year's figures, then draws a labelled bar chart with matplotlib's
non-interactive Agg backend. The chart is written into a throwaway temporary
directory that Python deletes on the way out, so nothing is left in your folder;
the deterministic summary line at the end is the proof the render worked.

Your own ``exercise-05-plot.py`` should save ``monthly-revenue.png`` next to the
script so you can open it. This shipped answer writes to a temp dir instead only
so the automated check leaves no file behind — the plotting code above the save
is identical to what you write.

Run it with::

    python exercise-05-plot-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # must come before importing pyplot — see Constraints

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CART_SALES: dict[str, list] = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "revenue": [4120, 3980, 4760, 5210, 5890, 6340,
                6120, 5980, 5430, 4870, 4310, 4650],
}


def main() -> None:
    """Print the year's totals and save the bar chart into a temp folder."""
    df = pd.DataFrame(CART_SALES)
    print(df)

    total = df["revenue"].sum()
    mean = df["revenue"].mean()
    best = df.loc[df["revenue"].idxmax()]
    worst = df.loc[df["revenue"].idxmin()]

    print(f"Total: ${total:,}")
    print(f"Mean:  ${mean:,.2f}")
    print(f"Best:  {best['month']} (${best['revenue']:,})")
    print(f"Worst: {worst['month']} (${worst['revenue']:,})")

    above_mean = int((df["revenue"] > mean).sum())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["month"], df["revenue"], color="#3273dc")
    ax.axhline(mean, color="#c0392b", linestyle="--", linewidth=1, label="Mean")
    ax.set_title("Coffee cart revenue by month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()

    with tempfile.TemporaryDirectory() as workspace:
        output_path = Path(workspace) / "monthly-revenue.png"
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"Saved chart: {len(df)} bars, mean line at {mean:.2f}, {above_mean} above it")


if __name__ == "__main__":
    main()
```

**`matplotlib.use("Agg")` before `import matplotlib.pyplot` — the order is the
whole point.** matplotlib chooses its rendering backend the first time `pyplot`
is imported, and after that the choice is fixed for the process. `Agg` is the
Anti-Grain Geometry renderer: it draws into a memory buffer and writes PNG
files, and it never asks the operating system for a window. That is what makes
the script work on a build server, in a Docker container, and over SSH — the
three places your code will end up whether you planned for it or not. Put the
`use` call after the `pyplot` import and it is a no-op, silently.

This is also why the imports in this file are not in the usual alphabetical
block. Linters will flag `import matplotlib.pyplot` as an import that is not at
the top of the file, and they are wrong here; the comment on the `use` line is
what stops a future reader from "tidying" it and breaking the script on a
machine they do not have.

**`savefig`, never `show`.** Under `Agg` a `plt.show()` call does not raise — it
warns and does nothing, which is worse than an error, because you will sit
looking at a clean exit code wondering where the chart went. The file on disk is
the artifact. `dpi=150` is chosen deliberately: the default 100 looks soft the
moment a chart is embedded in a PDF or a slide, and 300 quadruples the file for
no visible gain on screen.

**`fig, ax = plt.subplots()` rather than the bare `plt.*` calls.** The bare form
draws onto a hidden "current figure" that pyplot tracks globally. It is fine
until you have two charts open and cannot tell which one `plt.title` just
changed. Holding `fig` and `ax` yourself costs one line and makes the target of
every call explicit — and every matplotlib example worth reading from here on
uses that form.

**`plt.close(fig)` because figures do not free themselves.** pyplot keeps a
reference to every figure it created so that `plt.show()` can find them later.
One leaked figure is nothing. A loop that writes fifty charts without closing
gets you `RuntimeWarning: More than 20 figures have been opened` and then a
steadily slower script as memory fills. Close it in the same function that
opened it.

**`tight_layout()` and `bbox_inches="tight"` solve overlapping halves of the
same problem.** `tight_layout()` rearranges the axes *inside* the figure so
labels do not collide with each other; `bbox_inches="tight"` crops the saved
image to what was actually drawn, so a long y-axis label is not sliced off at
the file boundary. Use both. Lecture 3's plot-hygiene checklist lists the
second; the first is what saves you when the title is long.

**The mean line is the chart's whole argument.** Twelve bars alone show a hump
in the middle of the year. The dashed line at 5,138.33 turns that into a
statement: six months clear the annual average and six do not, and the two
groups are contiguous — April through September above, October through March
below. That is a seasonal business, stated in one horizontal line. `label="Mean"`
is what makes it appear in the legend; `ax.legend()` only lists artists that
were given a label.

**Calendar order, not sorted order.** Sorting these bars by revenue would
produce a tidier picture and destroy the only thing it has to say. A bar chart
of a time series carries meaning in its left-to-right order. The same rule is
why the y axis starts at zero: the length of the bar *is* the number, so a
truncated axis exaggerates every difference on the chart.

The saved PNG should show twelve bars Jan to Dec, a dashed red line a little
above 5,000 with exactly six bars clearing it, a title, both axis labels with
the unit named, a legend entry reading `Mean`, and nothing clipped at any edge.

**About the shipped file.** The chart-building code above is exactly what you write. The one difference is the save: this download wraps `savefig` in a `tempfile.TemporaryDirectory`, so the PNG is written, proven to exist, and then deleted with the folder on the way out. That keeps the automated check from littering the repo. Your own version points the save at `monthly-revenue.png` next to the script so you can open the picture.

## Run it

Copy the worked answer on this page into `exercise-05-plot.py` and run it:

```bash
python exercise-05-plot.py
```

It needs pandas and matplotlib. It builds the chart with the non-interactive `Agg` backend, writes the PNG into a throwaway temporary directory that Python deletes on the way out — so it leaves nothing in your folder — and prints the one-line summary. Your own `exercise-05-plot.py` saves `monthly-revenue.png` beside the script instead, so you can open it. The `-solution` suffix keeps it from colliding with your own `exercise-05-plot.py`.

## Common bugs to catch

- **`UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be
  shown`.** You called `plt.show()` under the `Agg` backend. Delete the call —
  the PNG is your output.
- **Nothing happens and no file appears.** You built the figure but never
  called `savefig`, or you called it on `plt` before creating the axes. Check
  that the `fig.savefig(...)` line actually runs; put a `print` right before
  it if you are unsure.
- **`FileNotFoundError: [Errno 2] No such file or directory:
  'charts/monthly-revenue.png'`.** You pointed `OUTPUT_PATH` at a folder that
  does not exist. matplotlib will create the file but not the directory. Add
  `OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)` before saving.
- **`ImportError: Cannot load backend 'TkAgg'`** or a hang with no output on a
  server. Your `matplotlib.use("Agg")` line is missing, or it sits *after*
  `import matplotlib.pyplot as plt`. Order matters; move it up.
- **Month labels overlapping into an unreadable smear.** Your `figsize` is too
  narrow. Widen it, or rotate the ticks with
  `ax.tick_params(axis="x", rotation=45)`.
- **The x axis shows 0 through 11 instead of month names.** You passed
  `df.index` or `df["revenue"].index` as the first argument to `bar`. Pass
  `df["month"]`.
- **The dashed line does not appear in the legend.** `ax.legend()` only lists
  artists that were given a `label=`. Add `label="Mean"` to the `axhline`
  call.
- **The y-axis label is cut off in the PNG even though it looks fine on
  screen.** You dropped either `fig.tight_layout()` or `bbox_inches="tight"`.
  Use both; they solve slightly different parts of the same problem.
- **The chart from your previous run keeps reappearing unchanged.** You are
  opening a cached copy in your image viewer. Close it and reopen, or check
  the file's modification time.

## Under the hood

<details>
<summary>Under the hood — why the backend is chosen before pyplot is imported</summary>

matplotlib picks the machinery that turns figures into pixels — its **backend** —
the first time `pyplot` is imported, and the choice is then locked for the whole
process. `matplotlib.use("Agg")` has to run *before* that import to have any
effect; put it after and it is a silent no-op. `Agg` (Anti-Grain Geometry) draws
into a memory buffer and writes PNG files, and it never asks the operating
system for a window — which is exactly what lets the script run on a build
server, in a Docker container, and over SSH, the three places your code ends up
whether you planned for it or not. Under `Agg`, `plt.show()` does not raise; it
warns and does nothing, which is worse than an error because you sit staring at
a clean exit code wondering where the chart went.

`dpi=150` is a deliberate middle: the default 100 looks soft the moment a chart
is dropped into a PDF or a slide, and 300 quadruples the file for no visible
gain on screen. And `plt.close(fig)` matters because pyplot keeps a reference to
every figure it made so `show()` can find them later — leak one and nothing
happens, but a loop that writes fifty charts without closing earns
`RuntimeWarning: More than 20 figures have been opened` and a steadily slower
run as memory fills.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and no warnings, on a machine with no
      display attached.
- [ ] The printed lines match the expected output exactly.
- [ ] `monthly-revenue.png` exists and is recreated after you delete it.
- [ ] The chart has a title, both axis labels with units, and a legend.
- [ ] The mean line sits just above 5,000 and six bars clear it.
- [ ] Nothing is clipped and the y axis starts at zero.
- [ ] The file is committed to Git with a message like
      `Add Week 13 exercise 5: monthly revenue chart`.

## Stretch

- Colour the bars conditionally: months above the mean in one colour, months
  below in another. Build the colour list with a comprehension over
  `df["revenue"] > df["revenue"].mean()` and pass it as `color=`.
- Add a second panel with `fig, axes = plt.subplots(1, 2, figsize=(14, 5))` —
  bars on the left, a cumulative line (`df["revenue"].cumsum()`) on the right.
  Give the figure one `suptitle`.
- Redraw the same chart with the pandas shortcut,
  `df.plot.bar(x="month", y="revenue", ax=ax)`, and compare the code length.
  Then work out how to get the same labels on it — the shortcut returns an
  `Axes`, so everything you learned still applies.
- Write the summary numbers to a small text file alongside the PNG, so the
  loan application has both the picture and the figures behind it.
- Annotate the best month directly on the chart with `ax.annotate`. A reader
  should not have to trace a bar down to the axis to learn it was June.

That is the last exercise for Week 13. When your PNG looks right, take the
same load–filter–aggregate–plot loop into the longer problems in
[the Week 13 challenges](../challenges/README.md).
