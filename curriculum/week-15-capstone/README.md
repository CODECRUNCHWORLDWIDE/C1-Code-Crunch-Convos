# Week 15 — Capstone Project

Welcome to **Week 15** of **Code Crunch Convos** — the final week. For the
last fourteen weeks you have been *learning*. This week, you are *shipping*.
The capstone is not a tutorial, a worksheet, or a quiz. It is a real,
public, open-source project that you design, build, test, document,
deploy, and present. When this week is over, the artefact you submit should
be something you would happily put on your resume and link to in a job
application, a graduate school application, or your next freelance pitch.
That is the bar. This README is the hub for your capstone week.

Unlike previous weeks, there are no new Python topics to learn. Everything
you need has already been covered:

- **Week 1–7** — Python language and OOP
- **Week 8** — APIs and JSON
- **Week 9** — Flask web development
- **Week 10** — Databases and SQL
- **Week 11** — Testing and debugging
- **Week 12** — Automation and scripting
- **Week 13** — Data analysis with pandas
- **Week 14** — Intro to AI/ML

Your job this week is to combine those skills into a substantial,
portfolio-quality project of *your choice*.

## Learning Objectives

By the end of this week, you will be able to:

- **Scope** a small-but-substantial software project from a vague idea down
  to a concrete MVP with explicit anti-goals.
- **Structure** a Python repository the way professional teams do: modules,
  tests, configuration, CI, and docs.
- **Apply** the testing, linting, and formatting practices from Week 11 to
  your own code, achieving at least 70% coverage.
- **Wire up** a GitHub Actions CI workflow that runs your tests and linters
  on every push and pull request.
- **Write** a comprehensive README that lets a stranger install, run, and
  contribute to your project.
- **Ship** a working demo — a web app, a CLI, a notebook with reproducible
  outputs, an API, or a trained model.
- **Record** a short walkthrough video that explains what you built and
  why.
- **Talk** about your project clearly in writing (for resumes) and
  out loud (for interviews) using the STAR method.

## Standards this week meets

| Bar | What this week is measured against |
| --- | --- |
| University | `COP 2210` — Complete a substantial program of the learner's own design, and defend it. |
| Industry | Take a project from a one-page proposal to something a stranger can clone, install from the README and run, with tests, green CI on every push, and a written retrospective. |
| Beyond the bar | The week keeps going after the code is finished, into pinning the repo, writing the resume line, answering the deep-dive questions out loud, and getting the project reviewed by a peer and by a stranger — `lecture-notes/03-presentation-and-portfolio.md` |

## Prerequisites

This week assumes you have completed (or are comfortable with) Weeks 1–14.
You should already be able to:

- Create a virtual environment and install packages with `pip`.
- Write functions, classes, and modules; import them across files.
- Read and write files; handle exceptions; make HTTP requests.
- Build at least a tiny Flask app or CLI.
- Write `pytest` tests and read coverage reports.
- Commit, branch, push, and open a pull request on GitHub.

If any of these are still shaky, spend the first half-day this week
refreshing rather than diving straight into the project — you will move
faster overall.

## How this week works

The capstone is intentionally less structured than previous weeks. Instead
of daily lessons, you have **five milestones spread across seven days**:

| Day(s)   | Milestone                          | Deliverable                          |
|----------|------------------------------------|--------------------------------------|
| Day 1    | **01 — Idea & Scope**              | 1-page proposal in `docs/PROPOSAL.md` |
| Day 2    | **02 — Design & Skeleton**         | Public repo + CI stub + open issues   |
| Day 3–4  | **03 — Build Core**                | MVP code on a branch + draft PR       |
| Day 5    | **04 — Test & Polish**             | 70% coverage, lint-clean, screenshots |
| Day 6–7  | **05 — Ship & Present**            | Deploy (if web), record video, retro  |

Each milestone has its own file in [milestones/](milestones/). Read them
*in order* and check off the steps as you go.

## Suggested tracks

Pick **one** of the following. You are not locked in — but committing to a
track on Day 1 prevents the most common capstone failure, which is
re-starting on Day 4.

- **Web App track** — A Flask application with a database, user accounts,
  and a few real features (see [examples/web-app-track.md](examples/web-app-track.md)).
- **Data track** — A Jupyter notebook plus a Python package analyzing a
  real dataset, with a polished writeup (see [examples/data-track.md](examples/data-track.md)).
- **ML track** — Train a model on a real dataset, then deploy it as a CLI
  or Flask inference service (see [examples/ml-track.md](examples/ml-track.md)).
- **Automation track** — A real automation tool that solves a real problem,
  e.g. a GitHub bot, an inbox tidier, a cron job that does something useful
  (see [examples/automation-track.md](examples/automation-track.md)).
- **API track** — Build a public REST API with proper documentation,
  caching, and deployment (see [examples/api-track.md](examples/api-track.md)).

Browse [examples/](examples/) before picking — concrete examples make the
abstract tracks click.

## Capstone requirements

To pass the capstone you must meet most of the following. The exact
weighting is in [rubric.md](rubric.md).

- [ ] **Clean code** — PEP 8 compliant, formatted with `black`, lint-clean
      under `ruff` (or `flake8`).
- [ ] **Multi-module structure** — not a single `main.py`. At least three
      Python modules with clear separation of concerns.
- [ ] **Type hints** — public functions are annotated; `mypy --strict` is
      bonus but not required.
- [ ] **Tests with pytest** — at least **70% line coverage** measured by
      `coverage.py` (or `pytest --cov`).
- [ ] **CI workflow** — GitHub Actions runs your tests and linters on every
      push to `main` and every PR.
- [ ] **Comprehensive README** — purpose, install, usage, screenshots,
      contributing, license. See [lecture-notes/02-building-and-shipping.md](lecture-notes/02-building-and-shipping.md)
      for the anatomy.
- [ ] **Reproducible install** — `requirements.txt` or `pyproject.toml`,
      and the README's install steps actually work on a clean machine.
- [ ] **Working demo** — a web app, CLI, notebook, or deployed API that
      anyone can run or visit.
- [ ] **Walkthrough video** — 3–5 minutes, unlisted on YouTube or Loom,
      linked from the README.
- [ ] **One of**: persists state (SQLite or JSON), calls an external API,
      performs data analysis, or trains an ML model.

## Rubric

Your capstone is graded out of **100 points** across seven dimensions:

| Dimension                  | Points |
|----------------------------|-------:|
| Code Quality               |     20 |
| Architecture & Modularity  |     15 |
| Testing & CI               |     15 |
| Documentation              |     15 |
| Functionality & Polish     |     15 |
| Git Hygiene                |     10 |
| Presentation               |     10 |
| **Total**                  | **100**|

The full rubric, with what counts for full marks vs. partial credit, is in
[rubric.md](rubric.md). Read it on Day 1 — knowing how you will be graded
shapes how you build.

## Deliverable checklist

When you submit, you submit:

1. The **URL** of your public GitHub repository.
2. The **URL** of your walkthrough video.
3. The **URL** of your deployed demo (if applicable).
4. A pinned position for the repo on your **GitHub profile**.
5. A short **retrospective** (Markdown) inside the repo at `docs/RETRO.md`.

The full pre-submit walk-through is in [submission-checklist.md](submission-checklist.md).

## Resources

A curated list of project planning aids, open data sources, free hosting
providers, README inspiration, and portfolio tips lives in
[resources.md](resources.md). Skim it on Day 1; come back to it when you
get stuck.

## Lecture notes

The three lecture notes for this week are short, dense, and meant to be
re-read whenever a milestone feels hard:

1. [01-planning-your-capstone.md](lecture-notes/01-planning-your-capstone.md)
   — picking and scoping a project, MVP thinking, anti-patterns.
2. [02-building-and-shipping.md](lecture-notes/02-building-and-shipping.md)
   — repo conventions, README anatomy, CI, demos, deployment.
3. [03-presentation-and-portfolio.md](lecture-notes/03-presentation-and-portfolio.md)
   — pinning, resumes, interviews, open-sourcing well, getting feedback.

## Up next

After finishing this week, your capstone repo is the artefact. There is no
"Week 16" — you are graduating. The master capstone guide that sits
*outside* this curriculum and is referenced by your mentors and reviewers
lives at [../../projects/capstone/](../../projects/capstone/). It contains
the long-form submission instructions and the historical archive of past
learner capstones. Bookmark it.

## A final note

You will be tempted, on Day 3, to abandon your idea for a "better" one.
Don't. The capstone is graded on what you ship, not on what you imagined.
A small, finished, polished project beats a sprawling, half-built one every
single time. Trust your Day 1 scope, follow the milestones, and ship.

Good luck — and welcome to the other side of the bootcamp.
