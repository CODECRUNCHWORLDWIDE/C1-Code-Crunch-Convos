# Lecture 3 — Code Quality Tools and Continuous Integration

> "Make it work. Make it right. Make it fast." — Kent Beck

Lectures 1 and 2 made you a tester and a debugger. This lecture turns those habits into a **system**: tools that run automatically, every time you save, commit, and push, so your tests never go stale and your code never drifts.

We will cover four pieces: `ruff`, `black`, `mypy`, and CI with GitHub Actions — plus the glue that ties them together (`pre-commit` and `pyproject.toml`).

---

## 1. Why automate quality?

You already know how to run `pytest`. You can also run `ruff check .` by hand, and `black .`, and `mypy src`. So why automate?

- **Humans forget.** You will skip the formatter when you are tired. CI will not.
- **Disagreements get expensive.** A team of five with five style opinions wastes time in code review. Tools decide.
- **Bugs caught early are cheap.** A type error caught by `mypy` on your laptop costs one minute. The same error in production costs an hour and an apology.
- **Pull requests should be about ideas, not commas.** Automating the comma debates frees humans to discuss the actual design.

---

## 2. `ruff` and `black` — different jobs

Beginners often think these are competitors. They are not. They do different things.

| Tool   | Job                                                                                  |
|--------|--------------------------------------------------------------------------------------|
| `black`| **Formats** your code — line length, quotes, trailing commas, blank lines.           |
| `ruff` | **Lints** your code — unused imports, dead variables, common bugs, missing docstrings.|

Newer versions of `ruff` also include a *formatter* (`ruff format`) that aims for `black`-compatible output. Whichever you pick, run **one formatter** and **one linter**.

### 2.1 `black`

Install and run:

```bash
pip install black
black .
```

`black` reformats your code in place. It does not ask for your opinion. That is the whole point — by removing the option to bikeshed, it removes the bikeshedding.

Configure it in `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ["py311", "py312"]
```

The default line length is 88. Many teams use 100 or 120. Pick one and forget it.

Cite: <https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html>

### 2.2 `ruff`

`ruff` is a linter written in Rust. It is roughly 100× faster than the older `flake8` + `isort` + `pyupgrade` combo, and it replaces all of them.

```bash
pip install ruff
ruff check .
ruff check . --fix          # apply safe autofixes
ruff format .               # format (instead of black)
```

A starter config:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort import order
    "B",    # bugbear (likely bugs)
    "UP",   # pyupgrade (use modern syntax)
    "SIM",  # simplifications
]
ignore = ["E501"]   # let black handle line length

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]   # asserts are fine in tests
```

`select = ["E", "F"]` is a sensible minimum; adding `B`, `UP`, and `SIM` catches a lot of real bugs and style nudges new Python programmers in the right direction.

Cite: <https://docs.astral.sh/ruff/configuration/>

### 2.3 Order of operations

Run `ruff check --fix` first (it can rewrite imports), then `black` (it has the final word on layout). Or use `ruff format` and skip `black` entirely. The point is to **decide once and write it down**.

---

## 3. `mypy` — static type checking

You have been writing type hints since Week 4. `mypy` reads them and proves your code is internally consistent.

Install:

```bash
pip install mypy
mypy src
```

Catch this kind of bug without ever running the code:

```python
def greet(name: str) -> str:
    return "Hello, " + name


greet(42)   # mypy: Argument 1 to "greet" has incompatible type "int"; expected "str"
```

### 3.1 Configuring `mypy`

Add to `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests"]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

`strict = true` enables a stack of flags including:

- `--disallow-untyped-defs` (every function must be typed)
- `--no-implicit-optional` (a default of `None` does *not* make a parameter `Optional`)
- `--warn-unused-ignores`
- `--check-untyped-defs`

It is the gold standard for new projects. For legacy projects, turn flags on one at a time.

Cite: <https://mypy.readthedocs.io/en/stable/config_file.html>

### 3.2 Common errors and how to read them

`mypy` errors look like:

```
src/myapp/core.py:42: error: Incompatible return value type (got "int", expected "str")
```

Three patterns dominate the beginner experience:

1. **Forgot to type a function.** Add `-> None`, `-> int`, etc.
2. **`None` slipped in.** A function returns `str | None`, you forgot the `None`. Use `assert result is not None` or handle it explicitly.
3. **Dict shape unknown.** `mypy` cannot guess that a dict has a key called `"name"`. Either use a `TypedDict` or a dataclass.

When a third-party library has no types, you will see:

```
error: Library stubs not installed for "requests"
```

Fix:

```bash
pip install types-requests
```

Or, as a last resort, silence it:

```toml
[[tool.mypy.overrides]]
module = "some_untyped_lib.*"
ignore_missing_imports = true
```

---

## 4. `pyproject.toml` — the one config to rule them all

The modern Python world has converged on `pyproject.toml` (PEP 518/PEP 621) as the single configuration file. Here is a complete example for a small package:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "stringutils"
version = "0.1.0"
description = "Small string utilities for the Code Crunch Convos bootcamp."
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Your Name", email = "you@example.com" }]
license = { text = "MIT" }
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-mock>=3.12",
    "ruff>=0.5",
    "black>=24.0",
    "mypy>=1.10",
    "pre-commit>=3.7",
]

[tool.black]
line-length = 100
target-version = ["py312"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests"]

[tool.pytest.ini_options]
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
pythonpath = ["src"]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 90
```

Every contributor opens this one file to understand how the project is configured. That single source of truth is worth a great deal.

---

## 5. `pre-commit` — quality gates on every commit

`pre-commit` is a Git hook manager. You declare which tools should run before every `git commit`, and `pre-commit` installs a hook that runs them. If anything fails, the commit is rejected — until you fix it.

Install:

```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--strict]
```

Activate:

```bash
pre-commit install
```

Now every `git commit` runs `ruff`, `black`, and `mypy` on the changed files. To run on every file (e.g. once, after onboarding):

```bash
pre-commit run --all-files
```

Cite: <https://pre-commit.com/>

If a hook auto-fixes something, the commit is aborted and the fix is left in your working tree. Re-stage and re-commit — that is the loop.

### 5.1 Why `pre-commit` matters

Without `pre-commit`, you push code that fails CI, the build breaks, you context-switch back to fix it. With `pre-commit`, the failure happens before the commit ever leaves your machine. Same fix, ten seconds instead of ten minutes.

---

## 6. GitHub Actions — running everything in the cloud

The local `pre-commit` hook protects you. CI protects the whole team. If your laptop is broken, or you forgot to install the hook, CI is the safety net.

GitHub Actions is GitHub's built-in CI/CD system. A workflow is a YAML file in `.github/workflows/`. Create `.github/workflows/ci.yml`:

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
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: ruff check .

      - name: Check formatting with black
        run: black --check .

      - name: Type-check with mypy
        run: mypy src

      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Let's walk through it.

- **`on:`** — when this workflow runs. Here, every push to `main` and every pull request targeting `main`.
- **`jobs:`** — one or more named jobs. Each job runs on its own VM.
- **`runs-on: ubuntu-latest`** — a fresh Ubuntu virtual machine.
- **`strategy.matrix`** — run the job N times in parallel with different variables. We test on Python 3.11 and 3.12.
- **`steps:`** — ordered commands. Each step either runs a shell command (`run:`) or uses a pre-built action (`uses:`).
- **`actions/checkout@v4`** — clones your repo onto the runner.
- **`actions/setup-python@v5`** — installs Python and caches `pip` downloads between runs.
- **`pip install -e ".[dev]"`** — install the project in editable mode plus the `dev` extras (pytest, ruff, etc.).
- **Lint, format, type-check, test** — fail the job if any of them fail.

Push the file. Open the repo's **Actions** tab. Watch your workflow run, in real time. Green means the world is right.

Cite: <https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions> and <https://github.com/actions/setup-python>.

---

## 7. CI tricks worth knowing

### 7.1 Caching

The `cache: pip` argument to `setup-python` caches pip downloads automatically. For more control:

```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
```

### 7.2 Concurrency — cancel old runs

If a PR has been pushed three times in a row, you do not need to finish the first two. Cancel them:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 7.3 Secrets

Never commit API keys. Define them in **Settings → Secrets and variables → Actions**, then use:

```yaml
- name: Deploy
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
  run: ./deploy.sh
```

### 7.4 Artifacts

Upload the coverage HTML report so you can download and inspect it:

```yaml
- name: Upload coverage HTML
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: coverage-html
    path: htmlcov/
```

---

## 8. Badges

A badge in your README is a small image that says "tests passing", "coverage 96 %", or "pypi version 1.2.3". They are vanity, and they also reassure new users. The pattern:

```markdown
![CI](https://github.com/<org>/<repo>/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/<org>/<repo>/branch/main/graph/badge.svg)](https://codecov.io/gh/<org>/<repo>)
```

GitHub gives you the workflow badge URL from **Actions → workflow → … menu → Create status badge**. Coverage badges typically come from <https://codecov.io>, which is free for open-source projects.

---

## 9. Releases (a glimpse)

Once your code is tested and CI is green, releases are mostly a tagging exercise:

```bash
git tag -a v0.1.0 -m "First release"
git push origin v0.1.0
```

GitHub Actions can react to a tag push and publish to PyPI:

```yaml
on:
  push:
    tags: ["v*"]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

We will not go deep on packaging this week. Just know that the pipeline from `pytest` → CI → published package is short, and well-trodden.

---

## 10. Putting it all together

This week's mini-project, `stringutils`, will give you the full stack:

1. `pyproject.toml` configures `pytest`, `coverage`, `ruff`, `black`, and `mypy`.
2. `pre-commit` runs the linters and formatters before every commit.
3. GitHub Actions runs `ruff`, `black --check`, `mypy`, and `pytest --cov` on every push.
4. Coverage is gated at 90 % minimum.
5. A status badge in the README turns green when everything passes.

That setup, once you have it, is essentially copy-paste for every new Python project for the rest of your career. Invest the hour now.

---

## 11. Recap

- `ruff` lints, `black` formats — different jobs, no overlap if you configure them right.
- `mypy` enforces type hints. `strict = true` is the gold standard for new code.
- `pyproject.toml` is the single config file for all of the above.
- `pre-commit` runs quality tools on your machine before code leaves it.
- GitHub Actions runs the same tools (plus tests) on every push, on a clean VM, on multiple Python versions.
- Badges, caching, secrets, and matrix builds are nice extras but not the point.

The point is that **failing fast is a kindness** — to your teammates, your future self, and your users.

---

## Self-check

1. What is the difference between a linter and a formatter? Which is `ruff`, which is `black`?
2. Why does `mypy` not require running the code under test to find bugs?
3. Sketch the contents of `.pre-commit-config.yaml` for a project that uses `ruff` and `black`.
4. What does `strategy.matrix.python-version: ["3.11", "3.12"]` do in a GitHub Actions workflow?
5. Why might you set `--cov-fail-under=90` in CI?
