# Reference Solution — Real-World Dataset Analysis (Week 13)

This is the worked reference implementation for the Week 13 mini-project,
[Real-World Dataset Analysis](../../../curriculum/week-13-data-analysis/mini-project/README.md).

Read the mini-project page alongside it — the answer sits there beside the brief
that asked for it, and it explains *why* the analysis is shaped this way, where
people get stuck, and how the result scores against the rubric. This file is the
operating manual: what is here, how to run it, and how it maps onto the spec.

Only open this after you have built your own version. The mini-project is the
portfolio piece Week 13 exists to produce; reading a finished answer first
spends the learning for nothing.

---

## What's here

```text
week-13-data-analysis/
├── 00-overview.md      # this file
├── fetch_data.py       # pinned, checksummed download of the dataset
├── analysis.ipynb      # the deliverable notebook, executed with outputs saved
├── findings.md         # the one-page written summary
├── requirements.txt    # exact pinned versions
├── .gitignore          # data/ is not committed — it is reproducible
├── data/               # created on first run; 14 MB CSV cache
└── figures/
    ├── main.png                        # required deliverable
    ├── top15-total-vs-per-capita.png
    ├── income-vs-carbon.png
    └── decoupling-1990-2022.png
```

`analysis.ipynb` is committed **with its outputs**, so you can read it on GitHub
without running anything. That is a deliberate choice for a teaching artifact
and the opposite of what you would do on a production team, where notebook
outputs are stripped before commit because they make every diff unreadable.

---

## The dataset

**Our World in Data — CO2 and Greenhouse Gas Emissions**, 50,411 rows × 79
columns, 1750–2024, CC BY. <https://github.com/owid/co2-data>

`fetch_data.py` pins it to commit `382ee6c` and verifies SHA-256
`7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6`. OWID
rebuilds this file every few months; a `master` URL would silently change every
number in the analysis. This is the single most important thing to copy from
this solution into your own work.

---

## Running it

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .\.venv\Scripts\Activate.ps1     # Windows PowerShell

pip install -r requirements.txt

# Warm the cache (optional — the notebook does it too).
python fetch_data.py

jupyter lab analysis.ipynb         # then Run > Restart Kernel and Run All Cells
```

To prove it runs end to end without opening a browser — this is exactly the
check the rubric's first five points are for:

```bash
jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=300 analysis.ipynb
```

Expected tail:

```text
[NbConvertApp] Converting notebook analysis.ipynb to notebook
[NbConvertApp] Writing 800788 bytes to analysis.ipynb
```

No `[NbConvertApp] ERROR` line, no traceback. On this machine (Python 3.13.2,
pandas 2.2.3) the full run takes about 25 seconds, most of it `read_csv` on the
14 MB file.

### Verifying the headline numbers

```bash
python fetch_data.py
```

```text
OK  .../data/owid-co2-data.csv
    14,377,942 bytes
    sha256 7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6
```

If that checksum matches, the numbers in `findings.md` are the numbers you will
get: 8 absolute decouplers, 1,999 Mt of cuts, 9,228 Mt from China, world carbon
intensity −45.4%.

---

## How it maps onto the spec

| Spec requirement | Where |
|---|---|
| `analysis.ipynb` in the project folder | [`analysis.ipynb`](./analysis.ipynb) |
| One-page `findings.md` | [`findings.md`](./findings.md) |
| `requirements.txt` with exact versions | [`requirements.txt`](./requirements.txt) |
| At least one chart saved at `figures/main.png` | [`figures/main.png`](./figures/main.png) |
| Section 1 — Load | notebook cells 1–2 |
| Section 2 — Inspect | cells 3–8, including a missing-data audit and a coverage-by-year check |
| Section 3 — Clean | cells 9–12, six numbered decisions, one of them verified rather than asserted |
| Section 4 — Analyze | cells 13–23: a `melt` → `pivot_table` fuel mix, a named-aggregation `groupby` over 2023, and a two-value `pivot_table` for the decoupling comparison |
| Section 5 — Visualize | cells 24–28, four charts, all titled and labelled |
| Section 6 — Conclude | final markdown cell |
| Dataset over 1,000 rows and 5 columns | 50,411 × 79 raw; 15,270 × 15 after cleaning |

### Against the 25-point rubric

| Criterion | Points | How this solution earns them |
|---|---:|---|
| Notebook runs top-to-bottom with no errors | 5 | verified with `nbconvert --execute`, transcript above |
| Six sections present and well-labelled | 3 | the six required headers, in order |
| Cleaning is sensible and documented | 3 | six numbered decisions with reasons; the fuel-fill decision is checked in code |
| At least three charts, each labelled | 6 | four charts, each with title, axis labels with units, and a legend where there is more than one series |
| At least two non-trivial aggregations | 3 | three: `melt`+`pivot_table`, named-aggregation `groupby` with a `cumsum`, and a two-metric `pivot_table` with a derived classification |
| Findings sentence is specific and quantitative | 3 | the one-sentence finding in `findings.md` carries five numbers |
| `requirements.txt` accurate | 2 | pinned to the exact versions the run used |

---

## Reading order

1. `fetch_data.py` — 90 lines, and the reason every number reproduces.
2. `analysis.ipynb` sections 1–3 — the load and the cleaning. This is 60% of
   the work in any real analysis and it is where the judgement lives.
3. `analysis.ipynb` section 4 — the three aggregations.
4. `analysis.ipynb` section 5 — the charts.
5. `findings.md` — what it all meant.

If you only read one part, read the Clean section. Charts are easy; deciding
which rows are not countries is the job.
