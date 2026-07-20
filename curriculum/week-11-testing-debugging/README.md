# Week 11 — Testing, Debugging & Code Quality

Welcome to Week 11 of **Code Crunch Convos**. You have spent ten weeks writing code. By now you have a Flask app, a SQLite task tracker, a class-based gradebook, and a folder of scripts that mostly work — until they don't. This week is about turning "mostly works" into "I can change this code six months from now without fear."

That confidence has a name: **automated tests**. Plus the supporting cast of debuggers, linters, type checkers, and continuous integration. By Friday you will ship a small string-utilities library that is tested to 100 % coverage, formatted by `black`, linted by `ruff`, type-checked by `mypy`, and verified by a real GitHub Actions workflow that runs every time you push.

This is the week where you graduate from "person who writes Python" to "engineer who ships Python".

---

## Learning objectives

By the end of this week you will be able to:

- Explain **why** we write tests: regression prevention, design pressure, executable documentation.
- Install and run `pytest`, and understand the discovery rules (`test_*.py`, `Test*` classes, `test_*` functions).
- Write `assert` statements that produce clear, actionable failure messages.
- Use **fixtures** (`@pytest.fixture`) to share setup code, and explain the four scopes (`function`, `class`, `module`, `session`).
- Use `@pytest.mark.parametrize` to test many cases without copy-paste.
- Mock external dependencies with `unittest.mock` and `pytest-mock`, including `requests.get`.
- Measure test coverage with `pytest-cov` and understand the difference between line and branch coverage.
- Debug code with `print`, `breakpoint()`, the `pdb` cheatsheet, and the VS Code debugger.
- Configure `ruff` and `black` in `pyproject.toml` and explain who handles what.
- Add type hints and run `mypy` to catch bugs before runtime.
- Install `pre-commit` and configure hooks to run quality checks on every commit.
- Write a GitHub Actions workflow that runs your test suite on push and pull request.
- Place a unit, integration, and end-to-end test on the testing pyramid.

---

## Prerequisites

You should be comfortable with material from **Weeks 1–10**:

- **Weeks 1–4**: Python syntax, control flow, functions, modules — the things you will be testing.
- **Week 5**: Data structures — many tests will assert on list and dict shapes.
- **Week 6**: Exceptions — `pytest.raises` lets you test that the right exceptions fire.
- **Week 7**: OOP — fixtures often instantiate classes you wrote.
- **Week 8**: APIs and JSON — we will mock `requests.get` calls back to those APIs.
- **Week 9**: Flask — one of the challenges retrofits tests onto the Week 9 blog app.
- **Week 10**: SQL & SQLite — temporary SQLite files make beautiful test databases.

If any of those feel rusty, spend an hour with the previous week's notes before diving in.

---

## Topics covered

1. **Why test?** Regression prevention, design pressure, documentation, confidence to refactor.
2. **`pytest` install and basics** — discovery, naming conventions, `pytest -v`.
3. **`assert` with messages** — the one-line trick that saves an hour of debugging.
4. **Fixtures** — `@pytest.fixture`, scopes, `yield` fixtures for setup/teardown.
5. **Parametrize** — `@pytest.mark.parametrize`, table-driven tests, `ids=`.
6. **Mocking** — `unittest.mock`, `MagicMock`, `monkeypatch`, `pytest-mock`.
7. **Coverage** — `pytest-cov`, line vs branch coverage, what 100 % does and does not guarantee.
8. **Debugging tools** — `print`, `breakpoint()`, `pdb` commands, VS Code debugger.
9. **Logging vs printing** — when to reach for `logging.info` instead of `print`.
10. **`ruff` and `black`** — fast linting and unambiguous formatting.
11. **`mypy`** — gradual typing, `strict` mode, common errors.
12. **`pre-commit`** — running quality tools automatically on every `git commit`.
13. **GitHub Actions CI** — writing `.github/workflows/ci.yml`, matrix builds, caching.
14. **The testing pyramid** — many unit tests, fewer integration tests, even fewer end-to-end tests.

---

## Schedule (~36 hours)

| Day       | Hours | Focus                                                                                |
|-----------|-------|--------------------------------------------------------------------------------------|
| Monday    | 6     | Read `lecture-notes/01-intro-to-pytest.md`. Do `exercise-01` and `exercise-02`.      |
| Tuesday   | 6     | Do `exercise-03-parametrize.py`. Start `challenge-01-tdd-fizzbuzz.md`.               |
| Wednesday | 6     | Read `lecture-notes/02-mocking-coverage-and-debugging.md`. Do `exercise-04` and `05`.|
| Thursday  | 6     | Read `lecture-notes/03-quality-tools-and-ci.md`. Configure `ruff`, `black`, `mypy`.  |
| Friday    | 6     | Build the **stringutils** mini-project, add CI, push to GitHub.                      |
| Saturday  | 4     | Pick one challenge. Take the quiz. Begin homework.                                   |
| Sunday    | 2     | Finish homework, review, peek at Week 12.                                            |

Adjust the pace to your reality — these are guidelines, not laws.

---

## Folder navigation

- `lecture-notes/` — three deep-dive notes covering pytest, mocking/coverage/debugging, and quality tools/CI.
- `exercises/` — five focused drills. Each one teaches a single skill.
- `challenges/` — two bigger problems: TDD FizzBuzz, and adding tests to the Week 9 Flask blog.
- `mini-project/` — the **stringutils** library with starter code, tests, config, and CI.
- `quiz.md` — 10 multiple-choice questions to check your understanding.
- `homework.md` — six longer problems that combine the week's tools.
- `resources.md` — the official docs and books we recommend.

---

## Stretch goals

If the regular work feels too easy, try one (or more) of these:

- **Mutation testing**: install `mutmut` and find tests that pass even when the code is broken. Eye-opening.
- **Property-based testing**: use `hypothesis` to test `slugify` against generated random strings.
- **Doctest**: add `>>>` examples to every public function and run `pytest --doctest-modules`.
- **Coverage badge**: wire `codecov.io` into your CI and add a coverage badge to your README.
- **Tox / Nox**: run your test suite against Python 3.10, 3.11, and 3.12 locally.
- **Parallel tests**: install `pytest-xdist` and run your suite with `pytest -n auto`.
- **Snapshot testing**: try `syrupy` to lock down complex output without writing 50 `assert`s.

---

## How to ask for help

Stuck? Drop into `#week-11` in the bootcamp Discord. When you ask, include:

1. The test you ran (paste the full command).
2. The full failure output, including the traceback.
3. The code under test.
4. What you expected vs. what happened.

Nine out of ten test failures are off-by-one assertions or a fixture not being passed into the test function. The tenth is a mocked path you forgot to undo.

---

## Up next

**Week 12 — Automation & Scripting.** You will use the testing habits you build this week to ship reliable command-line tools. A script that automates your workflow is only useful if you trust it — and you trust what you test.

See `../week-12-automation-scripting/`.
