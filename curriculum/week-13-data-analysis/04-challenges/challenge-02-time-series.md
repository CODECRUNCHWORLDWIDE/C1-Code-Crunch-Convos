# Challenge 02 — Time Series: Resample & Rolling Mean

## Background

A lot of real-world data is recorded against time: stock prices, sensor
readings, web traffic, hospital admissions. pandas was built for time-series
work, and it has two features that other tools envy:

- **`resample`** — group rows by a time bucket (daily, weekly, monthly).
- **`rolling`** — apply a windowed function (e.g. 7-day moving average).

Together they turn noisy minute-by-minute data into trends a human can
read.

## Your task

Build a notebook called `challenge-02-time-series.ipynb` that:

1. Loads a daily time series (the script below generates one if you don't
   have a real dataset).
2. **Resamples** to monthly totals.
3. Computes a **7-day rolling mean** on the daily values.
4. Plots both: the daily series with the rolling mean overlaid, and a
   second chart of the monthly totals.

## Generating the data

If you do not have your own time series, paste this cell to fake one:

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
# Simulated daily sales with weekly seasonality + noise
baseline = 1000 + 300 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
trend = np.linspace(0, 400, len(dates))
noise = rng.normal(0, 80, len(dates))
sales = pd.Series((baseline + trend + noise).round(2), index=dates, name="sales")
sales.head()
```

You now have a `pd.Series` of 366 daily sales with a clear weekly pattern
and a slight upward trend.

## Required steps

### 1. Inspect

```python
sales.describe()
sales.index.min(), sales.index.max()
sales.head(10).plot(title="First 10 days of sales")
```

### 2. Resample to monthly totals

```python
monthly = sales.resample("M").sum()
monthly.plot.bar(figsize=(10, 4), title="Monthly sales total")
```

`"M"` means month-end. Other useful aliases: `"W"` weekly, `"Q"` quarterly,
`"Y"` yearly. See
<https://pandas.pydata.org/docs/user_guide/timeseries.html#offset-aliases>.

### 3. Rolling mean

```python
rolling7 = sales.rolling(window=7, min_periods=1).mean()
```

A 7-day rolling mean smooths the weekly bumps so the underlying trend is
obvious.

### 4. Overlay daily + rolling on one chart

```python
fig, ax = plt.subplots(figsize=(12, 5))
sales.plot(ax=ax, label="Daily", alpha=0.4)
rolling7.plot(ax=ax, label="7-day rolling mean", linewidth=2)
ax.set_title("Daily sales with 7-day rolling mean")
ax.set_ylabel("Sales")
ax.legend()
```

### 5. Write 2–3 sentences

In a final markdown cell, describe in plain English:

- Did sales trend up, down, or sideways across the year?
- How big is the weekly seasonality (peak day vs. trough day)?
- Which month had the highest total?

## Stretch ideas

- Plot the 7-day, 14-day, and 30-day rolling means together to compare
  smoothing levels.
- Add `rolling(7).std()` to draw a "noise band" around the mean.
- Use `.resample("W-MON").sum()` to bucket weeks starting on Monday.
- Replace the synthetic data with a real time series — try **air-quality
  data** from <https://aqs.epa.gov/aqsweb/airdata/download_files.html> or
  **COVID time series** from
  <https://github.com/owid/covid-19-data/tree/master/public/data>.

## Deliverable

A notebook saved as
`challenges/solutions/challenge-02-time-series.ipynb` containing:

- The daily series and an overlaid rolling mean chart.
- A monthly bar chart.
- A markdown cell with a written interpretation.
