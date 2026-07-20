# Week 13 — Mini-Project: Real-World Dataset Analysis

## Goal

Pick a free public dataset that genuinely interests you, then produce a
clean Jupyter notebook that loads it, cleans it, summarises it with at
least three charts, and ends with a short written analysis. By the end you
will have a portfolio-quality artifact: a notebook you can show in
interviews, hand to a friend, or extend into the Streamlit dashboard
stretch goal.

## Why it matters

Every chapter of every data-science job description includes some version
of "comfortable working with messy real-world data in Python". This
project is your first portfolio piece that proves you can.

## Suggested datasets

You may use any dataset you like, but here are five we recommend if you
want a curated start. Each has at least 1,000 rows and at least 5 columns.

| Topic | Source | Direct link |
|-------|--------|-------------|
| **NYC Taxi trips** | NYC Open Data | <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page> |
| **Olympic medals (1896–2022)** | Kaggle | <https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results> |
| **COVID-19 time series** | Our World in Data | <https://github.com/owid/covid-19-data/tree/master/public/data> |
| **World Bank indicators** | World Bank | <https://data.worldbank.org/> |
| **Spotify charts data** | Kaggle | <https://www.kaggle.com/datasets/dhruvildave/spotify-charts> |

Other places to browse:

- Kaggle Datasets: <https://www.kaggle.com/datasets>
- data.gov: <https://data.gov/>
- Awesome Public Datasets:
  <https://github.com/awesomedata/awesome-public-datasets>

Avoid datasets larger than ~500 MB on first try — work-in-Jupyter speed
matters more than data volume at this stage.

## Required deliverables

1. **A Jupyter notebook** named `analysis.ipynb` placed in this folder.
   Start from [`starter.ipynb`](./starter.ipynb).
2. **A one-page summary** (markdown or PDF) named `findings.md`
   answering:
   - What dataset did you pick and why?
   - What is the single most interesting thing you found?
   - What would you investigate next if you had another week?
3. **A `requirements.txt`** listing exact package versions you used. We
   already provide [`requirements.txt`](./requirements.txt); pin versions if
   you used anything else.
4. **At least one saved chart** as a PNG at `figures/main.png`.

## Notebook structure (required sections)

Use these six section headers, in this order. The starter notebook has them
already.

1. **Load** — `pd.read_csv(...)` or equivalent.
2. **Inspect** — `head()`, `info()`, `describe()`, missing-data audit.
3. **Clean** — fix dtypes, drop or fill missing, build derived columns.
4. **Analyze** — at least two `groupby` + `agg` or `pivot_table` summaries.
5. **Visualize** — at least three charts, each with title, axis labels,
   legend if applicable.
6. **Conclude** — a markdown cell with 2–3 sentences answering the question
   you set out with.

## Grading rubric

| Criterion                                              | Points |
|--------------------------------------------------------|-------:|
| Notebook runs top-to-bottom with no errors             | 5 |
| Six sections present and well-labelled                 | 3 |
| Cleaning is sensible and documented                    | 3 |
| At least three charts, each labelled                   | 6 |
| At least two non-trivial aggregations                  | 3 |
| Findings sentence is specific and quantitative         | 3 |
| `requirements.txt` accurate                            | 2 |
| **Total**                                              | **25** |

## Stretch goals

- Wrap your notebook in a **Streamlit** app (<https://streamlit.io/>) with
  one dropdown that re-filters a chart. Deploy free at
  <https://streamlit.io/cloud>. **This unlocks Week 14 bonus credit.**
- Add a **second** dataset and merge it with your first (e.g. World Bank
  GDP joined to COVID case counts).
- Add a **predictive** column: split the data on a date, train a simple
  scikit-learn model on the past, evaluate on the future. (You don't need
  this for Week 13 — it's a preview of Week 14.)
- Convert your CSV input to **Parquet** and benchmark read speed.

## Common pitfalls

- **Loading too big a file.** Use `nrows=10_000` while you build the
  pipeline; remove it for the final run.
- **Forgetting `parse_dates`.** Dates as strings won't sort or resample
  correctly.
- **Plots without titles.** Worth 0% even if the analysis is correct.
- **Showing raw numbers without interpretation.** Always pair a chart with
  one sentence of plain English in a markdown cell.

## Time budget

| Phase           | Hours |
|-----------------|------:|
| Pick a dataset  | 0.5 |
| Load + inspect  | 1.0 |
| Clean           | 1.5 |
| Analyze + chart | 3.0 |
| Write findings  | 1.0 |
| Polish          | 1.0 |
| **Total**       | **8h** |

## Up next

Once you submit, move on to
[Week 14 — Intro to AI & Machine Learning](../../week-14-intro-ai-ml/README.md).
You'll bring the cleaned DataFrame from this project straight into
scikit-learn.
