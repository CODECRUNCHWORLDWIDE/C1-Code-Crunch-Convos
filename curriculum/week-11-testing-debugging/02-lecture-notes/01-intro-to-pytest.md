# Lecture 1 — Introduction to `pytest`

> "Code without tests is broken by design." — Jacob Kaplan-Moss

This note covers the *why* of testing, then walks through `pytest` from `pip install` to writing parametrized tests. By the end you will know enough to test every Python project you have built so far.

---

## 1. Why bother with tests?

There are three reasons, and they compound.

### 1.1 Regression prevention

You write a function. It works. Two weeks later you "improve" it. Now it works for the new case you cared about — and silently breaks the old one. A test would have screamed at you the moment you broke it. Without tests, you find out from a user, in production, on a Friday.

Every test you write is a contract that says, "this behavior must keep working." When you change code, the test suite tells you what you broke. That is **regression prevention**, and it is the single biggest reason engineers write tests.

### 1.2 Design pressure

The easiest code to test is small, pure functions with clear inputs and outputs. The hardest code to test is a 200-line function that reads global state, calls three APIs, writes to a database, and prints to stdout.

When you commit to writing tests, you naturally start writing the easier kind. **Testability is a forcing function for good design.** This is why test-driven development is more about design than about testing.

### 1.3 Executable documentation

A docstring says, "here is how this function works." A test *proves* it, and stays in sync. New teammates read tests to learn how an API behaves. Tests do not lie. Comments do.

---

## 2. Installing `pytest`

`pytest` is a third-party package. Install it into a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate            # Windows PowerShell
pip install pytest
pytest --version
```

You should see something like `pytest 8.x.x`. If `pytest --version` errors, your virtual environment is not active.

> Throughout this week we assume you are inside an activated virtual environment. If `which python` does not point at your `.venv`, fix that first.

---

## 3. Your first test

Create two files side by side:

```python
# math_utils.py
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b
```

```python
# test_math_utils.py
from math_utils import add


def test_add_positive_numbers() -> None:
    assert add(2, 3) == 5


def test_add_with_zero() -> None:
    assert add(0, 7) == 7


def test_add_negatives() -> None:
    assert add(-1, -1) == -2
```

Run it:

```bash
pytest
```

You should see three green dots and `3 passed`. Now break the implementation — change `return a + b` to `return a - b` — and rerun. Three failures, with the exact line and expected vs. actual values. That is the loop.

---

## 4. Test discovery: how `pytest` finds your tests

`pytest` scans recursively from the current directory and collects anything matching its conventions. The defaults (which you almost never need to change) are:

- Files named `test_*.py` or `*_test.py`.
- Classes named `Test*` that **do not** define `__init__`.
- Functions and methods named `test_*`.

Cite: <https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery>

So this works:

```
project/
├── src/
│   └── widgets.py
└── tests/
    ├── test_widgets.py
    └── helpers/
        └── test_edge_cases.py
```

But this does *not* — `pytest` will skip the file because the name doesn't match:

```
tests/
└── widget_tests.py        # missing the test_ prefix
```

---

## 5. `assert` — and `assert` with messages

In `pytest`, you write tests with the built-in `assert` statement. No `self.assertEqual`. No `expect(...).toBe(...)`. Just Python.

```python
def test_truncate_default_suffix() -> None:
    result = truncate("hello world", 5)
    assert result == "he..."
```

When that assertion fails, `pytest` does some magic called **assertion rewriting** and shows you both sides of the comparison:

```
>       assert result == "he..."
E       AssertionError: assert 'hello' == 'he...'
E         - he...
E         + hello
```

You can also attach a message that is printed on failure. Use this whenever the values are not self-explanatory:

```python
assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
```

Rule of thumb: if the failure message would force you to open a debugger to understand it, add a message.

---

## 6. Testing exceptions with `pytest.raises`

Some functions are *supposed* to raise. Test that, too:

```python
import pytest
from math_utils import divide


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_divide_by_zero_message() -> None:
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(10, 0)
```

The `match=` argument is a **regex**, so escape `.` and `(` if you use them.

---

## 7. Fixtures — sharing setup code

You write five tests. All of them need the same sample list. Copy-pasting that list is fine the first time and disgusting by the third. Enter **fixtures**.

```python
import pytest


@pytest.fixture
def sample_users() -> list[dict]:
    return [
        {"id": 1, "name": "Ada", "active": True},
        {"id": 2, "name": "Linus", "active": False},
        {"id": 3, "name": "Grace", "active": True},
    ]


def test_count_active(sample_users: list[dict]) -> None:
    active = [u for u in sample_users if u["active"]]
    assert len(active) == 2


def test_first_user_name(sample_users: list[dict]) -> None:
    assert sample_users[0]["name"] == "Ada"
```

`pytest` sees the argument name `sample_users`, looks up a fixture with that name, calls it, and passes the return value. This is **dependency injection** for tests.

### 7.1 Fixture scope

By default a fixture is called **once per test**. For expensive setup (a temp file, a database connection) you can widen the scope:

```python
@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    yield conn
    conn.close()
```

The four scopes are:

| Scope     | Lifetime                                       |
|-----------|------------------------------------------------|
| `function`| One per test function (the default).           |
| `class`   | One per test class.                            |
| `module`  | One per test file.                             |
| `session` | One per `pytest` invocation.                   |

Use the narrowest scope you can. Wider scope means faster tests but a higher chance of one test leaking state into another.

Cite: <https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes>

### 7.2 `yield` fixtures for setup *and* teardown

```python
@pytest.fixture
def temp_file(tmp_path):
    path = tmp_path / "data.txt"
    path.write_text("hello\n")
    yield path
    # Teardown runs after the test:
    # tmp_path is auto-cleaned by pytest, so this is illustrative.
    print(f"cleaning up {path}")
```

Everything before `yield` is setup. Everything after is teardown — guaranteed to run even if the test fails.

### 7.3 Built-in fixtures worth knowing

- `tmp_path` — a fresh `pathlib.Path` to a temp directory, auto-cleaned.
- `tmp_path_factory` — a session-scoped version.
- `monkeypatch` — safely patch attributes and env vars; auto-reverted.
- `capsys` — capture stdout/stderr written by your code.
- `caplog` — capture log records.

Try `pytest --fixtures` in any project to see the full list.

---

## 8. Parametrize — table-driven tests

Three tests for `add`, one per case, gets repetitive fast. Parametrize them:

```python
import pytest


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (0, 7, 7),
        (-1, -1, -2),
        (1_000_000, 1, 1_000_001),
    ],
)
def test_add(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected
```

`pytest` runs this as four separate tests. If one fails, you see exactly which row. You can name the cases for nicer output:

```python
@pytest.mark.parametrize(
    "year, expected",
    [
        (2024, True),
        (2023, False),
        (2000, True),
        (1900, False),
    ],
    ids=["divisible-by-4", "ordinary-odd", "divisible-by-400", "century-not-400"],
)
def test_is_leap_year(year: int, expected: bool) -> None:
    assert is_leap_year(year) == expected
```

Cite: <https://docs.pytest.org/en/stable/how-to/parametrize.html>

---

## 9. Organizing tests

A reasonable layout for a small project:

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── conftest.py
│   ├── test_core.py
│   └── test_integration.py
├── pyproject.toml
└── README.md
```

Key ideas:

- Keep production code in `src/` (avoids "shadowing" bugs where Python imports your local folder before the installed package).
- Mirror the source layout in `tests/` — every `foo.py` gets a `test_foo.py`.
- `conftest.py` holds fixtures shared across multiple test files. `pytest` discovers it automatically.

Run only the tests you care about:

```bash
pytest tests/test_core.py                   # one file
pytest tests/test_core.py::test_add_zero    # one function
pytest -k "leap and not century"            # name expression
pytest -m slow                              # marker expression
pytest -v                                   # verbose
pytest -x                                   # stop on first failure
pytest --lf                                 # rerun last failures only
```

---

## 10. The TDD loop: red, green, refactor

Test-driven development is a discipline:

1. **Red** — write a failing test. It must fail because the feature does not exist yet, not because of a typo.
2. **Green** — write the *minimum* code to make it pass. Hard-code values if you must.
3. **Refactor** — clean the code up. The test guards you.
4. **Repeat** — write the next test.

A 90-second example. We are building a `slugify` function.

```python
# test_slugify.py
from stringutils import slugify


def test_slugify_lowercases() -> None:
    assert slugify("Hello") == "hello"
```

```
$ pytest -q
ImportError: cannot import name 'slugify' from 'stringutils'
```

Add the function:

```python
# stringutils.py
def slugify(text: str) -> str:
    return text.lower()
```

```
$ pytest -q
. 1 passed
```

Next test:

```python
def test_slugify_replaces_spaces() -> None:
    assert slugify("Hello World") == "hello-world"
```

```
$ pytest -q
F   assert 'hello world' == 'hello-world'
```

Update the function:

```python
def slugify(text: str) -> str:
    return text.lower().replace(" ", "-")
```

Pass. Add a test for trimming, then for stripping punctuation, then for unicode. Each step is small, each test runs in milliseconds, and you always know exactly which change broke which behavior. That is the loop.

You do not need to *always* TDD. Many engineers TDD when designing a new module from scratch, and write tests after the fact for exploratory code. The point is that **the discipline becomes a habit** — and habit beats willpower.

---

## 11. Configuring `pytest` in `pyproject.toml`

Once your project grows past three files, you will want a config section. Add this to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "slow: marks tests as slow (deselect with -m 'not slow')",
]
```

What each line does:

- `minversion` — fail if someone runs with an older `pytest`.
- `addopts` — flags applied to every run. `-ra` shows a summary of skipped/xfail tests, `-q` is quieter output, `--strict-markers` rejects typos in `@pytest.mark.<name>`.
- `testpaths` — directories to search. Faster than scanning the whole repo.
- `pythonpath` — adds `src/` to `sys.path` so `from myproject import ...` works.
- `markers` — declare every marker you use so `--strict-markers` is happy.

Cite: <https://docs.pytest.org/en/stable/reference/customize.html>

---

## 12. What to test, what not to test

You cannot (and should not) test everything. A rough triage:

- **Test**: business logic, edge cases, error paths, regressions for every bug you fix.
- **Test lightly**: thin wrappers around well-tested libraries.
- **Skip**: framework internals, third-party code, your own `__repr__`s, code that exists only to glue tested pieces together.

A test that just re-states the implementation is worse than no test — it makes refactors harder without catching real bugs. Prefer tests that describe *behavior* ("`slugify('Hello World')` returns `'hello-world'`") over tests that describe *implementation* ("`slugify` calls `.lower()` first").

---

## 13. Recap

You now know:

- Why we test: regression, design, documentation.
- How `pytest` discovers tests by file and function name.
- How to write assertions, including messages and exceptions.
- How fixtures share setup, and how scope controls their lifetime.
- How parametrize turns one test into many.
- The TDD loop: red, green, refactor.

Next up, **Lecture 2** covers what to do when your code talks to the network, the file system, or anything else you don't want to actually invoke during a test — plus how to measure how much of your code your tests cover, and how to debug them when they fail.

---

## Self-check

1. What is the difference between `assert x == 5` and `assert x == 5, "x was {}".format(x)`?
2. Why does `pytest` find `test_widgets.py` but not `widget_tests.py` with default settings?
3. When would you use `scope="module"` instead of `scope="function"`?
4. Rewrite this with `@pytest.mark.parametrize`:

   ```python
   def test_double_1(): assert double(1) == 2
   def test_double_2(): assert double(2) == 4
   def test_double_3(): assert double(3) == 6
   ```

5. Describe a function that would be very hard to test, and explain *why*.
