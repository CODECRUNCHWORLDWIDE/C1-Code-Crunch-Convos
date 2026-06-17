# Lecture 2 — Building and Shipping

A capstone repo is judged in roughly this order: first impression of the
README, ten seconds skimming the file tree, a glance at the CI badge,
running the install instructions, looking at a representative test, and
only then reading actual code. If any of those steps trip up the
reviewer, the rest of your project does not get its fair chance. This
lecture walks through how to make each of them go right: the project
structure, the README anatomy, the CI workflow, the demo, the video, and
deployment.

## Project structure conventions

There is no single correct Python project layout. There are, however,
*expected* layouts that experienced Python developers recognise at a
glance. Pick one of the two below and stick to it.

### Layout A — the "src" layout (recommended)

```text
your-project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_cli.py
├── docs/
│   ├── PROPOSAL.md
│   └── RETRO.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

The `src/` layout prevents a class of import bugs where your tests
accidentally import the in-tree copy of the package instead of the
installed one. It is what `pip`, `pytest`, `setuptools`, and most modern
templates default to.

### Layout B — the "flat" layout

```text
your-project/
├── your_package/
│   ├── __init__.py
│   ├── cli.py
│   └── core.py
├── tests/
│   └── test_core.py
├── ...
```

Flat works fine for small projects and matches a lot of older tutorials.
Either is acceptable for the capstone. Do not invent a third layout.

### Naming rules to follow

- **Package** — `your_package` — lowercase, underscores, importable.
- **Repo name** — `your-project` — lowercase, hyphens, readable on a URL.
- **Modules** — lowercase, short, descriptive: `database.py`, `cli.py`,
  `models.py`. Not `MyDatabase.py` or `Helpers_v2.py`.
- **Tests** — every file in `tests/` starts with `test_`. Every function
  inside starts with `test_`.

### A minimal `pyproject.toml`

```toml
[project]
name = "habit-tracker"
version = "0.1.0"
description = "A tiny habit tracker built for the Code Crunch Convos capstone."
readme = "README.md"
requires-python = ">=3.10"
authors = [{ name = "Your Name", email = "you@example.com" }]
license = { text = "MIT" }
dependencies = [
    "flask>=3.0",
    "sqlalchemy>=2.0",
    "click>=8.1",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5", "ruff>=0.5", "black>=24"]

[project.scripts]
habit = "habit_tracker.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pytest.ini_options]
addopts = "-q --cov=habit_tracker --cov-report=term-missing"
testpaths = ["tests"]
```

That file alone gives you packaging, a CLI entry point, dependency
management, linting config, and test config.

## README anatomy

A good README answers, in order, the questions a stranger asks. Here is
the spine — you can rearrange but do not omit any of these:

1. **Title** — the project name, in one line.
2. **One-sentence pitch** — what the project does and for whom.
3. **Badges** — build status, coverage, license. Use shields.io.
4. **Screenshot or GIF** — one image worth 200 words of description.
5. **Features** — three to five bullets, not twenty.
6. **Install** — exact commands, copy-pasteable, in a fenced code block.
7. **Usage** — the most common command/route/cell and its output.
8. **Demo link** — if deployed, link to the live demo.
9. **Video link** — your 3–5 minute walkthrough.
10. **Project structure** — a `tree`-style snippet of the repo.
11. **Development setup** — how to run tests, lints, and the dev server.
12. **Contributing** — a paragraph; if you have a CONTRIBUTING.md, link
    it.
13. **License** — the license name with a link to the file.
14. **Acknowledgements** — datasets, libraries, mentors.

A working install section looks like this — note that *every command must
actually work on a fresh clone*:

````markdown
## Install

```bash
git clone https://github.com/yourname/habit-tracker.git
cd habit-tracker
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run the app

```bash
flask --app habit_tracker.web run --debug
```

Open <http://127.0.0.1:5000> and sign up.

## Run the tests

```bash
pytest
```
````

If you can copy those commands into a fresh terminal on a fresh machine
and reach a running app, the README passes the "stranger" test. If they
silently fail, half your grade is gone before the reviewer even reads
your code.

### Screenshots and GIFs

Put screenshots in a top-level `docs/` or `assets/` folder and reference
them with relative paths:

```markdown
![Dashboard](docs/screenshots/dashboard.png)
```

For a short animation of the app working, **kap** (macOS) and **ScreenToGif**
(Windows) both export small GIFs. Compress them — a 5 MB GIF in the README
loads slowly. Aim for under 1 MB.

## CI setup (recap of Week 11)

Here is a minimal `.github/workflows/ci.yml` that runs lints, type checks,
and tests on every push and PR. You almost certainly only need to change
the `python-version` and the package name.

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: ruff check .

      - name: Format check with black
        run: black --check .

      - name: Test with pytest
        run: pytest --cov --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          fail_ci_if_error: false
```

Once this is green, add the badge to the top of your README:

```markdown
![CI](https://github.com/yourname/your-project/actions/workflows/ci.yml/badge.svg)
```

A green badge is small but does outsized work in the first-impression
phase. Aim to get one *before* you write any feature code on Day 2 — even
on a single passing dummy test. Then keep it green every commit after.

### Pre-commit hooks (optional but lovely)

A `.pre-commit-config.yaml` file plus `pre-commit install` runs your
formatter and linter automatically on every commit. It stops a whole class
of "oh no, my CI is red over a trailing newline" PRs. Suggested config:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

This is optional. If you have never seen `pre-commit` before, skip it
this week — the formatter you call from your CI is enough.

## Writing a good demo

A "demo" is the part of your project that a stranger can run *without
having to think*. Three common forms:

- **A web app** — one URL, a clear landing page, a working signup, a
  sample account with seed data so the reviewer is not staring at an
  empty dashboard.
- **A CLI** — a single command shown in the README, with example input
  and example output as a fenced code block.
- **A notebook** — a `.ipynb` file with the outputs already rendered (so
  GitHub shows them), and an explicit "Run Locally" section in the README.

The cardinal rule is **the demo must be reproducible without secrets**.
If your demo needs an API key, either:

1. Provide a free/no-key fallback path that works out of the box; or
2. Use a sample dataset checked into the repo that does not require the
   key; or
3. Cache an example API response under `tests/fixtures/` and have the
   demo run against the cached response by default.

A demo that requires the reviewer to "just create a free account at
example.com and add the key to a `.env` file" *will* be skipped, and your
project will be graded on whatever is left.

### Seed data

For database-backed projects, ship a tiny seed script:

```python
# scripts/seed.py
"""Populate the database with sample data so the demo is interesting."""

from habit_tracker.database import session_scope
from habit_tracker.models import User, Habit


def seed() -> None:
    with session_scope() as session:
        alice = User(email="demo@example.com", password_hash="...")
        session.add_all([
            alice,
            Habit(user=alice, name="Drink water"),
            Habit(user=alice, name="Read 20 pages"),
        ])


if __name__ == "__main__":
    seed()
```

Mention it in the README: "Run `python scripts/seed.py` to populate the
demo data, then log in as `demo@example.com` / `demo`."

## Recording a walkthrough video

The video is 3–5 minutes. Shorter is better than longer. It is *not* a
tutorial — it is a project tour. Aim for this rough structure:

1. **0:00–0:20** — Who you are, what the project is, the problem it
   solves. One sentence each.
2. **0:20–0:50** — Show the live demo solving the problem end-to-end.
3. **0:50–2:30** — Open the repo. Show the file tree, the README, a
   representative module, a representative test, and the green CI badge.
4. **2:30–3:30** — Talk about a real decision you made: a trade-off, a
   library you considered and rejected, a refactor you did. This is the
   moment a reviewer (or future employer) sees that you *think*, not just
   type.
5. **3:30–4:00** — What you would do with another week.

### Tools

- **OBS Studio** (free, all OSes) — most flexible, slight learning curve.
- **Loom free tier** (browser) — easiest, has a 5-minute hard cap which
  is actually a useful constraint.
- **Kap** (macOS) — minimalist, fine for screen-only with no webcam.
- **ShareX** (Windows) — feature-rich and free.

Recording tips, learned the hard way:

- Increase your terminal/editor font size before you start. What is
  readable to you at 1× is illegible on a phone.
- Close every distracting window. Quit Slack. Hide bookmarks bars.
- Write a one-page script of *talking points* (not a literal script).
  Talking from bullets sounds more natural than reading.
- Record in two or three takes and pick the best one. Do not edit each
  sentence — viewers tolerate a "um" far better than visible cuts.
- Upload to YouTube as **Unlisted**. Put the URL in the README.

## Deployment basics

If you are on the web app or API track, deploy your project. If you are
on the data or ML track without a hosted UI, you do not have to — your
notebook on GitHub is the demo.

Free-tier deployment options:

- **Fly.io** — `fly launch` reads your Dockerfile (or generates one for
  Python apps) and deploys to a tiny VM. Bring a credit card to confirm
  you are human; the hobby tier is generous.
- **Render** — connect your GitHub repo, point at the start command,
  done. Free web services sleep when idle.
- **Railway** — similar to Render with a one-click Postgres add-on.
- **PythonAnywhere** — Python-first, very beginner-friendly, free tier.

The pattern is the same on all of them:

1. Make sure your app runs with a single command locally
   (`flask run`, `gunicorn`, `uvicorn`).
2. Bind to `0.0.0.0` and read the port from `$PORT`.
3. Move all secrets to environment variables.
4. Add a `Procfile` (Render/Railway) or `fly.toml` (Fly).
5. Deploy.
6. Click the live URL. If it loads, add it to the README under "Live
   demo".

A common mistake: forgetting that the production database is not the
SQLite file on your laptop. For the capstone, an *empty* SQLite on the
server plus your seed script is acceptable. If you need persistence
across restarts on Fly, mount a Volume.

## The "done" definition

A capstone is done when *all* of the following are true:

- The MVP sentence from your proposal is satisfied on the live (or
  locally-runnable) demo.
- The README's install steps work on a fresh clone.
- `pytest --cov` reports at least 70% coverage and zero failing tests.
- `ruff check .` and `black --check .` both exit clean.
- The CI badge on `main` is green.
- The walkthrough video URL is in the README.
- The repo is pinned on your GitHub profile.
- You have written a short retrospective in `docs/RETRO.md`.

If any of those are missing, you are not done. If all of them are
present, *you are done* — and resist the urge to start one more feature.

Tomorrow's lecture (`03-presentation-and-portfolio.md`) covers what to do
with the finished thing.
