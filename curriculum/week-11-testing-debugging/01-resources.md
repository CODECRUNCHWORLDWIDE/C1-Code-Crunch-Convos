# Week 11 — Resources

Bookmark the official docs. Everything else is commentary.

---

## Official documentation

### Testing

- **pytest** — the test framework we use all week.
  <https://docs.pytest.org/>
  - Getting started: <https://docs.pytest.org/en/stable/getting-started.html>
  - Fixtures: <https://docs.pytest.org/en/stable/explanation/fixtures.html>
  - Parametrize: <https://docs.pytest.org/en/stable/how-to/parametrize.html>
  - Monkeypatch: <https://docs.pytest.org/en/stable/how-to/monkeypatch.html>

- **`unittest.mock`** — Python's standard library for mocks, patches, and `MagicMock`.
  <https://docs.python.org/3/library/unittest.mock.html>

- **`pytest-mock`** — the thin wrapper that turns `unittest.mock` into a pytest fixture.
  <https://pytest-mock.readthedocs.io/>

- **`pytest-cov`** — coverage plugin for pytest, built on top of `coverage.py`.
  <https://pytest-cov.readthedocs.io/>

- **`coverage.py`** — the underlying coverage tool. Read its docs to understand branch coverage.
  <https://coverage.readthedocs.io/>

### Debugging

- **`pdb`** — the standard library debugger and its full command reference.
  <https://docs.python.org/3/library/pdb.html>

- **`breakpoint()`** — the built-in that drops you into a debugger.
  <https://docs.python.org/3/library/functions.html#breakpoint>

- **VS Code Python debugger** — official Microsoft tutorial.
  <https://code.visualstudio.com/docs/python/debugging>

- **`logging`** — the standard library logging system, in case you decide to graduate from `print`.
  <https://docs.python.org/3/library/logging.html>

### Code quality

- **Ruff** — a very fast linter (and formatter) written in Rust.
  <https://docs.astral.sh/ruff/>
  - Rules index: <https://docs.astral.sh/ruff/rules/>
  - Configuration: <https://docs.astral.sh/ruff/configuration/>

- **Black** — the "uncompromising" code formatter.
  <https://black.readthedocs.io/>

- **mypy** — static type checker for Python.
  <https://mypy.readthedocs.io/>
  - Cheatsheet: <https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>

- **`typing` module** — the standard library types that power `mypy`.
  <https://docs.python.org/3/library/typing.html>

- **pre-commit** — Git hook manager for running quality tools on every commit.
  <https://pre-commit.com/>

### Continuous integration

- **GitHub Actions** — CI/CD on GitHub.
  <https://docs.github.com/en/actions>
  - Workflow syntax: <https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions>
  - `actions/setup-python`: <https://github.com/actions/setup-python>

---

## Books

- **Test-Driven Development: By Example**, Kent Beck — the original TDD book. Short, opinionated, classic. Examples are in Java but the ideas translate directly to Python.

- **Testing Python with pytest**, Brian Okken — the definitive pytest book. If you read one Python testing book, read this one.

- **The Pragmatic Programmer**, Hunt & Thomas — chapter on "Pragmatic Paranoia" makes the case for testing as a programming habit.

- **Working Effectively with Legacy Code**, Michael Feathers — what to do when you inherit a codebase with zero tests. Eventually you will need this.

---

## Free online tutorials

- **Real Python — Getting Started with Testing in Python**: <https://realpython.com/python-testing/>
- **Real Python — Effective Python Testing with pytest**: <https://realpython.com/pytest-python-testing/>
- **Hypothesis quickstart** (for stretch goal property-based testing): <https://hypothesis.readthedocs.io/en/latest/quickstart.html>

---

## Cheatsheets we recommend printing

- pytest assertion idioms — keep next to your keyboard.
- `pdb` command list — `n`, `s`, `c`, `b`, `l`, `p`, `pp`, `w`, `q`.
- `ruff` and `black` configuration snippets — copy/paste into every new project.

---

## Talks worth watching

- *"Stop Writing Classes"* — Jack Diederich (testable code tends to be simple code).
- *"Beyond Unit Tests: Taking Your Testing to the Next Level"* — Augie Fackler & Nathaniel Manista.
- *"Type-checked Python in the real world"* — talks by the mypy and pyright teams on PyCon.
