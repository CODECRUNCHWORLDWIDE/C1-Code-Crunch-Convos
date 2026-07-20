# Data Track Example — Public Transit Reliability Study

A reproducible data analysis of one city's public transit reliability,
using the **GTFS** (General Transit Feed Specification) data that most
transit agencies publish openly. The deliverable is a Jupyter notebook
plus a Python package, packaged into a public repo with a polished
writeup and at least four publication-quality figures.

## MVP sentence

> *A reader can clone the repo, run `make figures`, and reproduce a
> short report that ranks bus and rail routes in <CITY> by on-time
> performance over the past 30 days, with at least four charts.*

If that sentence is true on a fresh clone, the MVP is done.

## Goals

1. **Load** real GTFS data for a chosen city (e.g. Boston MBTA, NYC
   MTA, BART, London TfL, or your own city if it publishes GTFS).
2. **Clean** the schedule and (optionally) the GTFS-Realtime feed into
   tidy pandas DataFrames.
3. **Compute** an on-time-performance metric per route per day.
4. **Visualise** rankings and trends across the period.
5. **Write** a short report (Markdown + the notebook) that any reader
   can follow.

## Anti-goals

- A live web dashboard. The artefact is a notebook + report, not a
  hosted UI.
- Multi-city comparison. One city, done well, beats five cities done
  shallowly.
- Predicting future delays with ML — that is the ML track.
- Building your own GTFS parser; use an existing library
  (`gtfs-kit` or similar).

## Suggested tech stack

- Python 3.11+
- `pandas`, `numpy`
- `matplotlib`, optionally `seaborn`
- `gtfs-kit` for parsing GTFS schedule data
- `requests` for downloading data
- `jupyter` and `nbconvert` for the notebook
- `pytest` + `pytest-cov` for the package's tests
- `ruff` + `black`
- GitHub Actions for CI

## Folder layout

```text
transit-reliability/
├── src/transit_reliability/
│   ├── __init__.py
│   ├── load.py           # download + parse GTFS
│   ├── clean.py          # tidy DataFrames
│   ├── metrics.py        # on_time_rate(...), pure functions
│   └── plots.py          # matplotlib helpers, return Figure objects
├── tests/
│   ├── fixtures/
│   │   └── tiny_gtfs.zip   # a 5-stop, 1-route fake feed for tests
│   ├── test_clean.py
│   ├── test_metrics.py
│   └── test_plots.py
├── notebooks/
│   └── report.ipynb        # the headline notebook
├── figures/
│   ├── route_ranking.png
│   ├── weekday_vs_weekend.png
│   └── delay_distribution.png
├── docs/
│   ├── PROPOSAL.md
│   ├── REPORT.md           # the prose version of the notebook
│   └── RETRO.md
├── data/
│   └── .gitkeep            # raw data is downloaded, not committed
├── Makefile
├── pyproject.toml
├── .github/workflows/ci.yml
├── README.md
└── LICENSE
```

## Why the package and the notebook?

The package is where logic *lives*: parsing, cleaning, computing
metrics, building plots. The notebook is where the *story* lives: load
data, call the package, narrate, show figures, conclude. Splitting them
this way means your notebook reads top-to-bottom like a short paper,
and your code is unit-testable in a way that notebook cells never are.

A reviewer scoring the *Architecture & Modularity* rubric will look
exactly for this split.

## Suggested data sources

- **MBTA (Boston)** — <https://www.mbta.com/developers/gtfs>
- **MTA (New York)** — <https://www.mta.info/developers>
- **BART (San Francisco Bay)** — <https://www.bart.gov/schedules/developers>
- **TfL (London)** — <https://tfl.gov.uk/info-for/open-data-users/>
- **Transitfeeds aggregator** — <https://transitfeeds.com/>

Whichever you pick, **read the licence**. Most GTFS feeds allow free
use with attribution.

## A representative `metrics.py`

```python
"""Pure metric functions over tidied GTFS DataFrames."""

from __future__ import annotations

import pandas as pd


def on_time_rate(
    stop_times: pd.DataFrame,
    threshold_seconds: int = 300,
) -> pd.DataFrame:
    """Compute the on-time percentage per route.

    A trip is "on time" if its actual arrival is within
    ``threshold_seconds`` of its scheduled arrival.

    Args:
        stop_times: A DataFrame with at minimum the columns
            ``route_id``, ``scheduled_arrival``, ``actual_arrival``.
            All times are pandas Timestamps in the same timezone.
        threshold_seconds: How many seconds late counts as on-time.
            Defaults to 5 minutes, which is a common transit standard.

    Returns:
        A DataFrame indexed by ``route_id`` with one column
        ``on_time_rate`` between 0.0 and 1.0.
    """
    delays = (
        stop_times["actual_arrival"] - stop_times["scheduled_arrival"]
    ).dt.total_seconds()
    on_time = delays.between(-60, threshold_seconds, inclusive="both")
    return (
        on_time.groupby(stop_times["route_id"])
        .mean()
        .rename("on_time_rate")
        .to_frame()
    )
```

That function is short, typed, has a docstring, and is testable with a
hand-crafted DataFrame fixture — exactly the shape of code a reviewer
wants to see.

## Day-by-day plan

**Day 1.** Proposal. Pick a city. Skim its GTFS feed once.

**Day 2.** Repo skeleton, smoke test, CI green. Open issues.

**Day 3 AM.** `load.py` — download the GTFS zip, cache it under
`data/`, return tidy DataFrames. Write a test using a tiny fixture
feed shipped under `tests/fixtures/`.

**Day 3 PM.** `clean.py` — handle missing/malformed rows, harmonise
times to a single timezone. Tests for each cleaning step.

**Day 4 AM.** `metrics.py` — on-time rate, average delay, share of
trips cancelled. Pure functions, hand-crafted DataFrame fixtures.

**Day 4 PM.** `plots.py` — return matplotlib `Figure` objects. Build
four figures: route ranking bar chart, weekday vs weekend, delay
distribution, time-of-day heatmap.

**Day 5.** Wire all of the above into `notebooks/report.ipynb`. Write
the prose. Add screenshots of the figures to the README. Push coverage
to ≥ 70% on the package.

**Day 6 AM.** `Makefile` so `make figures` regenerates all PNGs from
scratch. `make notebook` runs and saves the notebook with outputs.

**Day 6 PM.** Record the walkthrough video. Show the notebook, then
show the package and its tests.

**Day 7.** `docs/REPORT.md` — a 500–800 word prose version of the
notebook's narrative. Retro. Pin. Submit.

## Where this project demonstrates each week

- **Week 6** — file I/O with the GTFS zip files.
- **Week 8** — HTTP downloads (and possibly GTFS-Realtime JSON).
- **Week 11** — pytest, fixtures, CI.
- **Week 12** — `Makefile` as automation glue.
- **Week 13** — pandas, matplotlib, the Jupyter notebook.

## "Done" check

- [ ] The notebook runs top-to-bottom from a fresh kernel without
      changes.
- [ ] `make figures` regenerates the PNGs.
- [ ] The four figures are committed under `figures/`.
- [ ] `docs/REPORT.md` exists, is short, and reads as a coherent piece.
- [ ] The package tests pass and coverage is ≥ 70%.
- [ ] The README links to the rendered notebook on GitHub.

## Stretch goals

- Use GTFS-Realtime (live vehicle positions) instead of static schedule
  delays. This makes the project punchier but is a real time sink — do
  not start it until Day 5 if at all.
- Publish the rendered notebook on GitHub Pages.
- Compare two adjacent route patterns side-by-side.
