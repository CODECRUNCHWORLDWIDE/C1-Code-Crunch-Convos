# Milestone 04 — Test & Polish (Day 5)

## Goal

By end of Day 5 your repo passes **all linters**, hits at least **70%
test coverage**, every public function has a **docstring**, and the
README has been **polished with screenshots**. The draft PR is now a
real PR, reviewed by you (and ideally by a peer), and **merged** to
`main`. CI is green on `main`.

This day is unglamorous and load-bearing. Most of the rubric points
sitting on the table after Milestone 03 are won here.

## Tasks

### Morning — tests

1. **Run coverage first.**

   ```bash
   pytest --cov=<your_package> --cov-report=term-missing
   ```

   Note the percentage and the list of uncovered lines.

2. **Aim coverage at logic, not getters.** Spend your time covering the
   functions where bugs *could* live: data validation, business rules,
   edge cases. Skip trivial `__repr__` and `@property` getters.

3. **Add 4–8 more tests until coverage is ≥ 70%.** For most capstones,
   this is the day's biggest task. Each test should be small enough that
   its name explains exactly what it asserts:

   ```python
   def test_streak_resets_when_day_is_skipped() -> None:
       """A missed day breaks the streak; only days after the gap count."""
       ...
   ```

4. **Write at least one *integration* test.** For a web app, this is a
   test that hits the real route with the Flask test client. For a CLI,
   it invokes `main()` with `click.testing.CliRunner`. For an API, it
   uses `requests` or `httpx` against a test server.

5. **Add a `pytest` fixture for a clean DB.** Conftest:

   ```python
   # tests/conftest.py
   import pytest
   from your_package.database import init_db, drop_db


   @pytest.fixture()
   def clean_db():
       """Yield a freshly initialised in-memory database."""
       init_db(":memory:")
       try:
           yield
       finally:
           drop_db()
   ```

6. **Re-run coverage and confirm the number.** Drop a screenshot of the
   coverage report into `docs/screenshots/coverage.png` for the README.

### Midday — lint, format, type-check

1. **Format everything.**

   ```bash
   black src tests
   ruff format src tests        # or skip if you use black alone
   ```

2. **Lint and fix.**

   ```bash
   ruff check --fix src tests
   ```

3. **Read the remaining warnings.** Some you should fix; some you should
   silence with a `# noqa: <code>` and a comment explaining why. Do not
   blanket-disable rules.

4. **Run `mypy` (optional but encouraged).** Even without `--strict`,
   `mypy src` catches a lot of real bugs.

5. **Add docstrings** to every public function, class, and module. The
   format that pleases both humans and tools is:

   ```python
   def add_check_in(habit_id: int, on_date: date) -> CheckIn:
       """Record a check-in for ``habit_id`` on ``on_date``.

       Args:
           habit_id: Primary key of the habit being checked in to.
           on_date: The calendar date of the check-in. Usually today.

       Returns:
           The newly persisted ``CheckIn`` row.

       Raises:
           ValueError: If a check-in for this habit/date already exists.
       """
   ```

   You do not need a docstring on every private helper, but every public
   one is rubric-grade documentation.

6. **Commit.** Message: `style: format, lint, and add docstrings`.

### Afternoon — README polish and screenshots

1. **Take three screenshots** of the app working. For each, choose a
   moment that *teaches* something: the dashboard, a typed form, the
   streak going up. Put them under `docs/screenshots/`.

2. **Compress the screenshots.** 200–500 KB each. Tools: `pngquant`
   (CLI), [TinyPNG](https://tinypng.com/), or macOS Preview's "Reduce
   File Size".

3. **Rewrite the README.** Use the anatomy from
   [../lecture-notes/02-building-and-shipping.md](../lecture-notes/02-building-and-shipping.md):

   - Title and one-sentence pitch.
   - Badges: CI, coverage (optional, via Codecov), license.
   - One headline screenshot near the top.
   - Features (3–5 bullets).
   - Install (copy-pasteable).
   - Usage (most common command + output).
   - Demo link if deployed (you'll fill this in tomorrow).
   - Video link (also tomorrow).
   - Project structure.
   - Development (tests, lints).
   - Contributing (link to `CONTRIBUTING.md` if you wrote one).
   - License.
   - Acknowledgements.

4. **Re-read it as a stranger.** Open it in incognito. Open the install
   block in a fresh terminal. Does it work?

5. **Merge the build-core PR.** Self-review it: every commit message,
   every changed file. Add a final commit if you need to. Squash if it
   makes sense (it usually doesn't — preserve the small commits).

6. **Make sure CI is green on `main`** after the merge. If it isn't, fix
   forward in a follow-up PR.

## Outputs

By end of Day 5:

- [ ] `pytest --cov` shows ≥ 70% coverage.
- [ ] `ruff check .` exits with no errors.
- [ ] `black --check .` exits with no errors.
- [ ] At least one integration test exists.
- [ ] Every public function/class/module has a docstring.
- [ ] Three or more screenshots are in `docs/screenshots/`.
- [ ] README has been rewritten and is genuinely good.
- [ ] The build-core PR is merged. CI on `main` is green.

## Pitfalls

- **Coverage theatre.** Writing tests that exercise lines without
  asserting anything meaningful. A test without an `assert` is not a
  test.
- **One giant "fix lint" commit.** Split formatting commits from
  feature commits — it makes the history far easier to read.
- **Forgetting the integration test.** Unit tests alone do not prove
  the app *runs*. Integration tests do.
- **A README written in five minutes.** This is the artefact reviewers
  read first. Spend two hours on it. The polish here repays itself many
  times over in the *Documentation* and *Presentation* rubric scores.

## Done check

- [ ] Coverage ≥ 70%.
- [ ] Lint, format, and tests all green locally.
- [ ] CI green on `main`.
- [ ] README pleases you when you re-read it.
- [ ] Screenshots committed.
- [ ] Build-core PR merged.

Tomorrow: ship and present. See
[05-ship-and-present.md](05-ship-and-present.md).
