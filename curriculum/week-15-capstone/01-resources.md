# Week 15 — Capstone Resources

This page is a working list of resources you can lean on while planning,
building, and shipping your capstone. It is intentionally short — bookmark
it and return when you hit a wall, rather than reading it cover-to-cover.

## Project planning

- **First Contributions** — a friendly walkthrough of the GitHub flow, with
  practice tasks. Great for cementing the open-source loop before you
  scaffold your own repo: <https://github.com/firstcontributions/first-contributions>
- **awesome-readme** — a curated gallery of excellent README files. Use it
  to find a structure you like, then steal it (open-source norms encourage
  it): <https://github.com/matiassingers/awesome-readme>
- **Open Source Guides** by GitHub — short articles on starting, growing,
  and maintaining an open-source project: <https://opensource.guide/>
- **Make a README** — a tiny but excellent checklist for what every README
  should contain: <https://www.makeareadme.com/>
- **Shields.io** — generate the small badges (build status, coverage,
  license) you see on professional READMEs: <https://shields.io/>

### Lightweight planning templates

If you are not sure what a 1-page proposal looks like, try one of these
formats — copy-paste into `docs/PROPOSAL.md` and fill in:

- **Lean Canvas** (one page, business-y but useful for any project):
  <https://leanstack.com/lean-canvas>
- **Shape Up pitch** (Basecamp) — pitch-style template that forces you to
  state the problem, appetite, and "no-gos":
  <https://basecamp.com/shapeup/1.5-chapter-06>
- **PRFAQ** ("press release / FAQ") — write your project's launch press
  release before you build it: <https://productschool.com/blog/product-strategy/product-template-amazons-pr-faq>

## Open data sources

Almost every track benefits from real data. These are free, well-known,
and *not* covered by aggressive terms of use:

- **Kaggle Datasets** — thousands of curated, tagged, downloadable
  datasets: <https://www.kaggle.com/datasets>
- **data.gov** — the U.S. federal open data portal (transit, climate,
  education, health): <https://www.data.gov/>
- **UK data.gov.uk** — the equivalent for the United Kingdom:
  <https://www.data.gov.uk/>
- **EU Open Data Portal**: <https://data.europa.eu/>
- **GitHub Trending** — for "what are people building right now?" research
  on automation, ML, and tooling: <https://github.com/trending>
- **awesome-public-datasets** — a giant categorised list:
  <https://github.com/awesomedata/awesome-public-datasets>
- **OpenStreetMap** — geographic data, great for maps and transit:
  <https://www.openstreetmap.org/>
- **MovieLens** — classic recommender system dataset:
  <https://grouplens.org/datasets/movielens/>
- **Hugging Face Datasets** — both classic and modern ML datasets, ready to
  stream: <https://huggingface.co/datasets>

When you pick a dataset, *read its license*. "Open" is not "free for any
use" — some are non-commercial, some require attribution.

## Free hosting

You do not need a credit card to deploy a small project, though some
providers ask for one to confirm you are human. Pick one and stop
shopping:

- **Fly.io** — runs Docker containers in mini-VMs in many regions; very
  generous hobby tier. Good for Flask, FastAPI, and small databases:
  <https://fly.io/>
- **Render** — Heroku-style "git push to deploy" for web services and
  static sites: <https://render.com/>
- **Railway** — similar to Render, with a Postgres add-on:
  <https://railway.app/>
- **PythonAnywhere** — a Python-first host with a free tier; great for
  beginners but a little dated: <https://www.pythonanywhere.com/>
- **GitHub Pages** — free static hosting from a repo; perfect for a
  Jupyter-rendered HTML notebook or a project landing page:
  <https://pages.github.com/>
- **Hugging Face Spaces** — free hosting for ML demos using Gradio,
  Streamlit, or Docker: <https://huggingface.co/spaces>
- **Streamlit Community Cloud** — one-click deploy for Streamlit apps:
  <https://streamlit.io/cloud>

If you are deploying a database-backed app, **Supabase** and **Neon** both
offer free Postgres tiers if your host does not bundle one.

## Walkthrough video tools

You need a 3–5 minute screen recording. Any of these are free and good
enough:

- **OBS Studio** — open-source, runs on macOS / Windows / Linux:
  <https://obsproject.com/>
- **Loom (free tier)** — browser-based, 5-minute limit on the free plan
  which forces useful brevity: <https://www.loom.com/>
- **Kap** — macOS-only, minimalist screen recorder:
  <https://getkap.co/>
- **ShareX** — Windows-only, very feature-rich:
  <https://getsharex.com/>

If you can, upload to YouTube as **Unlisted** so it lives at a stable URL
you can put in your README.

## Portfolio inspiration

When you are stuck on what "polished" looks like, browse:

- **GitHub Explore** — projects trending now, by language:
  <https://github.com/explore>
- **awesome-python** — categorised list of well-loved Python projects;
  click through a few of the smaller ones to see how their READMEs read:
  <https://github.com/vinta/awesome-python>
- **Read the Docs gallery** — examples of project documentation done well:
  <https://docs.readthedocs.io/en/stable/examples.html>
- **Personal portfolios on the GitHub blog** — search "GitHub readme
  profile" for inspiration on your *profile* README, which is separate
  from your project README.

## How to write a great GitHub README

The single best resource is the **awesome-readme** repo:
<https://github.com/matiassingers/awesome-readme>. It is a curated list of
README examples grouped by what they do well — minimalist, badges,
animations, contribution guides, etc. Browse five examples, pick one whose
*structure* you like (not necessarily its visual flair), and use it as a
template.

For checklists rather than examples:

- **Make a README** — the minimum: <https://www.makeareadme.com/>
- **standard-readme** — a stricter spec used by many JavaScript and Go
  projects but useful for Python too: <https://github.com/RichardLitt/standard-readme>

## Licenses

Pick one when you create the repo. The most common open-source choices:

- **MIT** — short, permissive, the default for most small projects.
- **Apache 2.0** — permissive plus an explicit patent grant; preferred for
  projects you expect to be used by larger companies.
- **GPLv3** — copyleft; derivative works must also be GPLv3.

**choosealicense.com** is the easiest way to pick:
<https://choosealicense.com/>. GitHub will offer to add the file for you
when you create the repo.

## Reference docs you will need this week

- **PEP 8** — Python style guide: <https://peps.python.org/pep-0008/>
- **PEP 257** — docstring conventions: <https://peps.python.org/pep-0257/>
- **black** — uncompromising formatter: <https://black.readthedocs.io/>
- **ruff** — fast linter & formatter, modern flake8 replacement:
  <https://docs.astral.sh/ruff/>
- **pytest** — testing framework: <https://docs.pytest.org/>
- **coverage.py** — line/branch coverage measurement:
  <https://coverage.readthedocs.io/>
- **GitHub Actions** — the CI we use this week:
  <https://docs.github.com/actions>
- **Conventional Commits** — optional but tidy commit message style:
  <https://www.conventionalcommits.org/>

## Stuck? Ask.

The Code Crunch Convos community runs office hours every Tuesday and
Thursday. Show up with a *specific* question — "my CI is red, here is the
log" gets a much faster answer than "I don't know what to build". The
community channels are listed in the main repo's
[../../community/](../../community/) folder.
