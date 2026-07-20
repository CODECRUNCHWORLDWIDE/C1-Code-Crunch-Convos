# Week 11 — Homework

Six problems. Aim to complete at least four. The first three rebuild quality habits on previous projects; the last three stretch into new tools.

Submit by linking to one or more GitHub repos in `#week-11`. For each problem, paste your `pytest -v` output (or the equivalent for the tool in question) in a comment.

---

## Problem 1 — Refactor a previous mini-project to be testable

Pick **any** mini-project from Weeks 5–10 (file I/O, OOP gradebook, API client, Flask blog, SQLite task tracker — your choice).

**Goal:** make the code testable without changing observable behavior.

What to do:

1. Split the code into modules where one module = one responsibility (`parsing.py`, `storage.py`, `api.py`, etc.).
2. Replace global state and hard-coded constants with function arguments.
3. Add type hints to every public function.
4. Document each public function with a one-line docstring.

Deliverable: the refactored project on a `week-11-refactor` branch with a `BEFORE_AFTER.md` describing the three biggest changes and *why* each made testing easier.

---

## Problem 2 — Write tests for the refactored project

Now write tests for the project you refactored in Problem 1. Targets:

- At least **15** test functions.
- At least **3** fixtures, including one `scope="module"` fixture.
- At least **1** parametrized test with **4+** rows.
- At least **1** test that uses `pytest.raises` for a documented error path.
- Coverage report (`pytest --cov`) at **80 %+** on the project's main module.

Deliverable: a `tests/` directory and a coverage report screenshot in the project README.

---

## Problem 3 — Add CI to the same project

Add a `.github/workflows/ci.yml` that does **all** of the following on every push and pull request:

1. Sets up Python 3.11 and 3.12 with `actions/setup-python` and pip caching.
2. Installs the project with `pip install -e ".[dev]"`.
3. Runs `ruff check .`.
4. Runs `black --check .`.
5. Runs `mypy src`.
6. Runs `pytest --cov=src --cov-fail-under=80`.

Push it. Watch it run. Add the workflow badge to your README.

Deliverable: a green badge in the README plus a link to a passing CI run.

---

## Problem 4 — Add `pre-commit` to the same project

Install `pre-commit` and add `.pre-commit-config.yaml` with at least:

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `ruff` (with `--fix`)
- `black`
- `mypy` (with `additional_dependencies` matching your runtime deps)

Run `pre-commit install` and verify with `pre-commit run --all-files`.

Deliverable: the `.pre-commit-config.yaml` plus a paragraph in the README explaining what each hook does in your own words.

---

## Problem 5 — Add a serious `ruff` config

Replace the default `[tool.ruff]` section with one that:

1. Selects at least these rule families: `E`, `W`, `F`, `I`, `B`, `UP`, `SIM`, `C4`, `RET`.
2. Sets `line-length = 100`.
3. Sets `target-version = "py312"`.
4. Has a `per-file-ignores` block that relaxes `S101` (asserts) inside `tests/`.

Then run `ruff check . --fix` and commit the autofixes as a separate commit.

Deliverable: the updated `pyproject.toml`, plus a commit titled "Apply ruff autofixes" that contains *only* the autofix changes.

---

## Problem 6 — Write a `mypy`-clean version of the project

Turn on `strict = true` in `[tool.mypy]`. Run `mypy src`. It will probably scream. Fix every error until `mypy` is silent.

Common fixes:

- Add `-> None` to every helper that returns nothing.
- Replace `dict` with `dict[str, Any]` or a `TypedDict` / dataclass.
- Add `| None` where parameters default to `None`.
- Install `types-requests` (or similar) for libraries without bundled stubs.

Deliverable: a `mypy.txt` log showing zero errors, plus a paragraph in the README on the most surprising thing you had to change.

---

## Submission checklist

- [ ] Problem 1 — refactored project on a branch
- [ ] Problem 2 — 15+ tests, 3+ fixtures, 1+ parametrize, 1+ raises
- [ ] Problem 3 — green GitHub Actions badge
- [ ] Problem 4 — `pre-commit` configured and passing
- [ ] Problem 5 — serious `ruff` config + autofix commit
- [ ] Problem 6 — `mypy --strict` clean

Stretch:

- Add a `codecov.io` coverage badge to the README.
- Run your tests on Python 3.11 *and* 3.12 in CI.
- Add `hypothesis` property-based tests for one function.
