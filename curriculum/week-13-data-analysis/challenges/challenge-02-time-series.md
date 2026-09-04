# Challenge 2 — Time Series: Resample & Rolling Mean

> **Topic:** time series — `resample` to a coarser bucket, `rolling` to smooth
> **Lecture:** [03 — Aggregation & Plotting](../lecture-notes/03-aggregation-and-plotting.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** a daily line of real data is almost always too noisy to read
> the trend off directly. `resample` and `rolling` are the two tools that turn
> jitter into a story, and this problem hands you data with a *known* trend and
> a *known* weekly cycle, so you can check your analysis against the truth.

## The Brief

A lot of real data is stamped with a time: sales, sensor readings, web traffic,
hospital admissions. pandas was built for it, and two moves do most of the work
— **`resample`** rolls rows up into time buckets (daily → monthly), and
**`rolling`** slides a window along to smooth the noise (a 7-day moving average).

You are handed a full year of daily sales built from three ingredients you can
see in the generator: a **weekly cycle**, a gentle **upward trend**, and random
**noise**. Neither the trend nor the cycle is visible in the raw daily line —
the noise is bigger than the year's growth. The whole exercise is making them
visible. Because the random generator is **seeded**, every number is exactly
reproducible, which means you can check your recovered trend and seasonality
against the values that were baked in.

## Starter

Copy this into `challenge-02-time-series.py` (or a notebook of the same name).
The generator is done; the analysis is yours.

```python
"""challenge-02-time-series.py — resample and roll a year of daily sales."""

import numpy as np
import pandas as pd


def build_sales() -> pd.Series:
    """Return 366 days of 2024 sales: weekly cycle + upward trend + noise."""
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    baseline = 1000 + 300 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    trend = np.linspace(0, 400, len(dates))
    noise = rng.normal(0, 80, len(dates))
    return pd.Series((baseline + trend + noise).round(2), index=dates, name="sales")


sales = build_sales()

# TODO: print sales.head() and describe(); confirm 366 days across all of 2024.
# TODO: monthly = sales.resample("ME").sum(); print it and name the biggest month.
# TODO: rolling7 = sales.rolling(7, min_periods=1).mean(); check both ends.
# TODO: detrend (sales - rolling7), group by weekday, measure the peak-to-trough swing.
# TODO: chart 1 — daily with the rolling mean overlaid on ONE axis.
# TODO: chart 2 — a bar chart of the monthly totals.
```

## Requirements

1. Print `sales.head()` and `sales.describe()`, and confirm the series covers
   **366 days** (2024 is a leap year) from 2024-01-01 to 2024-12-31.
2. **Resample to monthly totals** with `resample("ME").sum()` and name the
   highest month.
3. Compute a **7-day rolling mean** with `min_periods=1`, and verify it at both
   ends: day 1 equals the raw day-1 value, day 7 equals the mean of days 1–7.
4. **Detrend** (`sales - rolling7`), group the remainder **by weekday**, and
   report the **peak-to-trough swing** — the size of the weekly cycle.
5. Draw **two charts**: the daily series with the rolling mean overlaid on one
   axis, and a bar chart of the monthly totals. Save them (temporary files are
   fine).

## Constraints

- **Use `"ME"`, not `"M"`.** On pandas 2.2 the bare `"M"` still resamples but
  warns that it is deprecated; `"ME"` means "month end" and `"MS"` means "month
  start". The alias grew a letter because `"M"` clashed with the minute alias.
- **Pass `min_periods=1` deliberately, and know what it buys.** By default
  `rolling(7)` returns `NaN` for the first six days, because there is no full
  window yet. `min_periods=1` says "use whatever you have", so the line has no
  gap at the left but a noisier first week. For an overlay chart that reads
  better; for a number you will quote, prefer the honest gap.
- **Overlay the two lines on one `ax`.** Each bare `.plot()` in a notebook makes
  its own figure — pass `ax=` to both so the rolling mean lands on top of the
  daily line, not in a second chart.
- **Make the rolling window one full period of what you want to remove.** A
  7-day window cancels a 7-day cycle exactly; a 5-day or 10-day window leaves a
  wobble behind. Match the window to the period.
- **Label both axes and name the units.** `Sales (units)`, not `Sales`. An
  unlabelled time axis is the easiest way to mislead with a chart.

## Expected output

```text
$ python challenge-02-time-series.py
--- head ---
2024-01-01    1024.38
2024-01-02    1152.45
2024-01-03    1354.71
2024-01-04    1208.70
2024-01-05     718.14
Freq: D, Name: sales, dtype: float64

366 days, 2024-01-01 to 2024-12-31

--- describe ---
count     366.00
mean     1200.25
std       258.37
min       608.83
25%      1000.14
50%      1191.78
75%      1388.68
max      1793.20

--- monthly totals ---
2024-01-31    32248.31
2024-02-29    30661.96
2024-03-31    32700.17
2024-04-30    32918.52
2024-05-31    35871.88
2024-06-30    34954.17
2024-07-31    38165.93
2024-08-31    37964.11
2024-09-30    38737.69
2024-10-31    41307.37
2024-11-30    40716.95
2024-12-31    43043.68
Freq: ME

Highest month: December 2024 at 43,043.68

--- rolling-mean checks ---
first: 1024.38 == day 1 value 1024.38
day 7: 978.49 == mean of days 1-7 978.49
rolling mean day 1  : 1024.38
rolling mean day 366: 1412.50
lift across the year: +388.12

--- weekly seasonality (detrended, by weekday) ---
Monday         8.40
Tuesday      244.53
Wednesday    295.03
Thursday     141.47
Friday      -157.08
Saturday    -292.28
Sunday      -227.38

peak Wednesday +295.03, trough Saturday -292.28
peak-to-trough swing: 587.31

Saved 2 charts (daily+rolling, monthly totals) to a temp dir; cleaned up.
```

Because the generator is seeded, those are not "about right" — they are the
answer. `1024.38` on 2024-01-01 and `43,043.68` for December will be identical
on every machine. If your first value differs, you changed the seed, the date
range, or the order of the `rng.normal` call.

## Steps

1. Paste the starter and run it. `build_sales()` returns the same 366 numbers
   every time.
2. Print `head()` and `describe()`. Read the standard deviation (258) against
   the year's trend (400): the noise is nearly as big as the signal, which is
   why the raw line hides the trend.
3. Resample to monthly totals and find the biggest month with `idxmax()`.
4. Build the 7-day rolling mean and check it at both ends before you trust it.
5. Detrend, group by weekday, reindex to Monday–Sunday, and measure the swing.
6. Draw the overlay chart and the monthly bar chart, then save both.

## The Solution

```python
"""challenge-02-time-series-solution.py — resample and rolling mean on a year of sales.

Generates a full year of synthetic daily sales with a *known* structure — a
weekly cycle, a gentle upward trend, and Gaussian noise — then uses resample and
rolling to recover the trend and the weekly rhythm that the raw daily line
hides. Because the random generator is seeded, every number below is exactly
reproducible on any machine, with nothing downloaded.

The two charts are drawn with matplotlib's non-interactive Agg backend and
written into a throwaway temporary directory that Python deletes on the way out,
so the script leaves nothing behind.

Run it with::

    python challenge-02-time-series-solution.py
"""

import matplotlib

matplotlib.use("Agg")  # choose a headless backend before importing pyplot

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_sales() -> pd.Series:
    """Return 366 days of 2024 sales: weekly cycle + upward trend + noise."""
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    baseline = 1000 + 300 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    trend = np.linspace(0, 400, len(dates))
    noise = rng.normal(0, 80, len(dates))
    return pd.Series((baseline + trend + noise).round(2), index=dates, name="sales")


def main() -> None:
    """Inspect, resample, roll, and measure the recovered structure."""
    sales = build_sales()

    print("--- head ---")
    print(sales.head())
    print(f"\n{len(sales)} days, {sales.index.min().date()} to {sales.index.max().date()}")

    print("\n--- describe ---")
    print(sales.describe().round(2).to_string())

    monthly = sales.resample("ME").sum()
    print("\n--- monthly totals ---")
    print(monthly.round(2).to_string())
    print(f"\nHighest month: {monthly.idxmax():%B %Y} at {monthly.max():,.2f}")

    rolling7 = sales.rolling(window=7, min_periods=1).mean()
    print("\n--- rolling-mean checks ---")
    print(f"first: {rolling7.iloc[0]:.2f} == day 1 value {sales.iloc[0]:.2f}")
    print(f"day 7: {rolling7.iloc[6]:.2f} == mean of days 1-7 {sales.iloc[:7].mean():.2f}")
    print(f"rolling mean day 1  : {rolling7.iloc[0]:.2f}")
    print(f"rolling mean day 366: {rolling7.iloc[-1]:.2f}")
    print(f"lift across the year: {rolling7.iloc[-1] - rolling7.iloc[0]:+.2f}")

    detrended = sales - rolling7
    by_dow = detrended.groupby(detrended.index.day_name()).mean()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_dow = by_dow.reindex(order)
    print("\n--- weekly seasonality (detrended, by weekday) ---")
    print(by_dow.round(2).to_string())
    print(f"\npeak {by_dow.idxmax()} {by_dow.max():+.2f}, trough {by_dow.idxmin()} {by_dow.min():+.2f}")
    print(f"peak-to-trough swing: {by_dow.max() - by_dow.min():,.2f}")

    with tempfile.TemporaryDirectory() as workspace:
        out = Path(workspace)

        fig, ax = plt.subplots(figsize=(12, 5))
        sales.plot(ax=ax, label="Daily", alpha=0.4, color="#3273dc")
        rolling7.plot(ax=ax, label="7-day rolling mean", linewidth=2, color="#d9534f")
        ax.set_title("Daily sales with 7-day rolling mean, 2024")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales (units)")
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "fig-daily-rolling.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(monthly.index.strftime("%b"), monthly.values, color="#3273dc")
        ax.set_title("Monthly sales totals, 2024")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total sales (units)")
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "fig-monthly-totals.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    print("\nSaved 2 charts (daily+rolling, monthly totals) to a temp dir; cleaned up.")


if __name__ == "__main__":
    main()
```

**`resample` is `groupby` for a `DatetimeIndex`.** `sales.resample("ME")` splits
the 366 rows into month-end buckets and `.sum()` combines them — the same
split-apply-combine from Lecture 3, with the grouping key derived from the index
instead of a column. It only works because `pd.date_range` gave the Series a
real `DatetimeIndex`. On a Series indexed by date *strings*, `resample` raises:

```text
TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'Index'
```

**`"ME"`, not `"M"`.** The assignment was written against an older pandas. On
2.2.3, `sales.resample("M")` still works but warns:

```text
FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.
```

`ME` is "month end", `MS` is "month start". The alias got the extra letter
because `"M"` was ambiguous with the new `"m"`-style minute aliases. `"Y"` →
`"YE"` and `"Q"` → `"QE"` changed the same way. Note the resulting index labels
are 2024-01-31, 2024-02-29 … — the *right edge* of each bucket.

**`min_periods=1` decides what happens at the start.** By default
`rolling(7)` produces `NaN` for the first six days, because there is no full
7-day window yet. `min_periods=1` says "compute with whatever you have", so day
1 is its own value, day 2 the mean of two, and only from day 7 on is it a true
7-day mean. The solution checks both: `rolling7.iloc[0] == sales.iloc[0]` and
`rolling7.iloc[6] == sales.iloc[:7].mean()`. Which you want is a real choice —
`min_periods=1` gives a chart with no gap but a noisier left edge; the default
gives an honest gap. For an overlay chart, no gap usually reads better; for a
number you are going to quote, take the default.

**Why a 7-day window kills a 7-day cycle exactly.** The mean of any seven
consecutive samples of `sin(2πn/7)` is zero, because those seven samples are the
complete set of the seven phase positions and a full period of a sine sums to
zero. So the rolling mean of `baseline` is a flat 1000 from day 7 onward, and
what remains in `rolling7` is the trend plus damped noise. That is not a
coincidence to admire — it is the design rule: **make the window one full period
of the thing you want to remove.**

**Detrending before measuring seasonality is what makes cell 6 valid.**
`sales - rolling7` removes the local level, so each day is expressed as a
deviation from its own week. Grouping *that* by weekday isolates the cycle. If
you had grouped raw `sales` by weekday instead, you would still get roughly the
right shape here — the trend spreads itself evenly across weekdays over 52 weeks
— but only by luck, and any series with a trend that is not a whole number of
weeks long will bias one weekday over another.

And the measurement checks out against the generator. The sine peaks at day
index 2 (Wednesday, since 2024-01-01 was a Monday) at `300·sin(4π/7) = +292.5`
and troughs at index 5 (Saturday) at `-292.5`, for a true peak-to-trough of
**585.0**. The estimate is **587.31**. Likewise the true trend lift is exactly
+400 and the rolling mean recovers **+388.12** — a little short, because the
rolling mean at day 1 is a single noisy observation and at day 366 is a 7-day
average, so the two endpoints are not measured the same way.

## Run it

Copy the worked answer on this page into `challenge-02-time-series.py` and run it:

```bash
python challenge-02-time-series.py
```

It needs only pandas, numpy, and matplotlib — no dataset file, no network. It
generates the seeded series inline, prints every check, draws the two charts
into a temporary directory that Python deletes on the way out, and prints a
confirmation line. The `-solution` suffix keeps it from colliding with your own
`challenge-02-time-series.py`.

## Common bugs to catch

**Charting the daily series and calling the trend.** The single most common
outcome for this challenge is a 366-point spaghetti line, a shrug, and "it goes
up a bit maybe". The daily standard deviation is 258 against a full-year trend
of 400 — the signal is smaller than the wobble. That is the entire reason
`rolling` exists, and it is why the brief asks for the overlay rather than two
separate charts: the value of the smoothed line is only visible next to the
noise it removed. Put the sizes side by side and it is obvious — the weekly
swing alone is ±292 units, and the entire year's growth is +400.

**Comparing months by total when the months are different lengths.** February
2024 has 29 days, January 31. That is a 6.5% handicap before any business
happens, which is a bigger effect than several of the month-to-month
differences in the table. If you want to compare months rather than count them,
use `.resample("ME").mean()`.

**`sales.rolling(7).mean().plot()` without keeping the axes.** Each `.plot()`
call in a notebook creates its own figure unless you pass `ax=`. Two calls, two
charts, no overlay. The solution makes one `ax` and passes it to both.

**Forgetting that `pd.date_range` end dates are inclusive.**
`pd.date_range("2024-01-01", "2024-12-31", freq="D")` yields 366 dates, not 365
(2024 is a leap year) and not 365 by exclusion of the endpoint. Unlike a Python
`range`, the `end` of a `date_range` is included. Check `len()` before you build
an analysis on it.

**Using `.rolling(7).mean()` on data that is not sorted by date.** `rolling`
walks the Series in *row order*, not in date order. If you concatenated monthly
files without sorting, your "7-day mean" is a mean of seven arbitrary days and
nothing will tell you. `sales = sales.sort_index()` costs nothing.

## Under the hood

<details>
<summary>Under the hood — why a 7-day window kills a 7-day cycle exactly</summary>

The mean of any seven consecutive samples of `sin(2πn/7)` is zero. Those seven
samples are the complete set of the seven phase positions of the wave, and a
full period of a sine sums to zero. So a 7-day rolling mean of the seasonal
component flattens it to a constant from day 7 onward, and what is left in the
rolling line is the trend plus damped noise — which is exactly what you wanted
to see. That is not a lucky coincidence; it is the design rule: **make the
window one full period of the thing you want to remove.**

You can see the diminishing returns of a wider window. A 7-day mean has a
day-to-day standard deviation around 120; widening to 14 or 30 days only drops it
to about 116 and 110, because the seasonal component is *already* gone after one
period and all a longer window does is average more noise while blurring the
ends. Match the window to the period; do not just make it bigger.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and no `FutureWarning` (it uses `"ME"`).
- [ ] The series is 366 days long and every printed number is reproducible.
- [ ] Monthly totals are resampled and the biggest month is named.
- [ ] The rolling mean is verified at both ends.
- [ ] The weekly swing is measured from the detrended series.
- [ ] Both charts have titles, labelled axes, and named units.
- [ ] Committed to Git with a message like
      `Add Week 13 challenge 2: time series resample and rolling mean`.

## Stretch

- Overlay the 7-, 14-, and 30-day rolling means on one chart, and add a
  `rolling(7).std()` band around the 7-day line — the cheapest honesty you can
  add to a trend chart.
- Resample with `sales.resample("W-MON").sum()` to bucket weeks on Monday. Check
  `weekly.head(2)` and `weekly.tail(2)` first: the first and last buckets are
  partial and will look like a collapse if you do not.
- Compare months by `resample("ME").mean()` instead of `.sum()`. February is
  the low month partly because it is the shortest — a mean is the fairer
  comparison when the buckets are different lengths.
