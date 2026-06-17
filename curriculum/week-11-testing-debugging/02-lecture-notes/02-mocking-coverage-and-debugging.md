# Lecture 2 — Mocking, Coverage, and Debugging

> "First, solve the problem. Then, write the code." — John Johnson

Lecture 1 got you writing pytest. Now we tackle the parts of testing that frustrate beginners the most: dependencies you can't (or shouldn't) call for real, knowing whether you have tested *enough*, and debugging the failures that pop up along the way.

---

## 1. When to mock — and when not to

A **mock** is a stand-in object that pretends to be something real. You use it when calling the real thing during a test is slow, flaky, expensive, or destructive.

Good candidates for mocking:

- Network calls (`requests.get`, `httpx.post`).
- External services (Stripe API, SendGrid, AWS).
- Time and randomness (`datetime.now`, `random.random`).
- File system writes you don't want to actually perform.

Bad candidates for mocking:

- Pure functions you wrote. Just call them.
- Standard library data structures. Mock `dict` and you have proven nothing.
- The thing you are testing. If you mock the system under test, your test is meaningless.

A useful heuristic: **mock at the boundary**. The boundary is where your code meets something you don't control. Inside the boundary, use the real objects.

---

## 2. `unittest.mock` — the standard library mock toolkit

`unittest.mock` ships with Python. The two stars are `MagicMock` and `patch`.

### 2.1 `MagicMock`

A `MagicMock` is an object that responds to any attribute access and any method call without complaint:

```python
from unittest.mock import MagicMock

response = MagicMock()
response.status_code = 200
response.json.return_value = {"id": 1, "name": "Ada"}

print(response.status_code)   # 200
print(response.json())        # {'id': 1, 'name': 'Ada'}
print(response.headers["X-Foo"])  # MagicMock instance — fine, no error
```

You then check what was called:

```python
response.json.assert_called_once()
```

### 2.2 `patch`

`patch` swaps a name in some module for a mock, then restores it when the block ends. Use it as a context manager:

```python
from unittest.mock import patch
import myapp


def test_fetch_user() -> None:
    fake_response = MagicMock()
    fake_response.json.return_value = {"id": 1, "name": "Ada"}
    fake_response.status_code = 200

    with patch("myapp.requests.get", return_value=fake_response) as mocked_get:
        user = myapp.fetch_user(1)

    assert user == {"id": 1, "name": "Ada"}
    mocked_get.assert_called_once_with("https://api.example.com/users/1", timeout=5)
```

The single most-asked question about `patch`: **what string do I pass?** Rule: patch the name *where it is looked up*, not where it is defined. If `myapp.py` does `import requests`, you patch `myapp.requests.get`. If `myapp.py` does `from requests import get`, you patch `myapp.get`. See <https://docs.python.org/3/library/unittest.mock.html#where-to-patch>.

### 2.3 `patch` as a decorator

If a whole test needs the same patch, decorate it:

```python
@patch("myapp.requests.get")
def test_fetch_user(mocked_get: MagicMock) -> None:
    mocked_get.return_value.json.return_value = {"id": 1, "name": "Ada"}
    mocked_get.return_value.status_code = 200

    user = myapp.fetch_user(1)

    assert user["name"] == "Ada"
```

The mock object is injected as a parameter. With multiple decorators, the order is **bottom-up** — the closest decorator becomes the first parameter.

---

## 3. `monkeypatch` — pytest's lightweight alternative

For simple patches, `pytest`'s `monkeypatch` fixture is friendlier. It automatically undoes everything at test teardown:

```python
def test_now_is_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    import datetime

    class FakeDatetime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 1, 1, 12, 0, 0)

    monkeypatch.setattr("myapp.datetime.datetime", FakeDatetime)
    assert myapp.greeting() == "Happy New Year!"
```

`monkeypatch` is also the right tool for environment variables:

```python
def test_uses_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "fake-key-123")
    assert myapp.load_api_key() == "fake-key-123"
```

Cite: <https://docs.pytest.org/en/stable/how-to/monkeypatch.html>

**When to use which?**

- `monkeypatch` — simple attribute and env-var swaps. Pytest-native.
- `unittest.mock.patch` — you need a `MagicMock` with assertion methods (`assert_called_once_with`).

There is no wrong answer. Pick one style per project and stick with it.

---

## 4. `pytest-mock` — `unittest.mock` as a fixture

`pytest-mock` is a wrapper that exposes `unittest.mock.patch` as the `mocker` fixture. Install it:

```bash
pip install pytest-mock
```

Then:

```python
def test_fetch_user(mocker) -> None:
    fake_get = mocker.patch("myapp.requests.get")
    fake_get.return_value.json.return_value = {"id": 1, "name": "Ada"}
    fake_get.return_value.status_code = 200

    user = myapp.fetch_user(1)

    assert user["name"] == "Ada"
    fake_get.assert_called_once()
```

No `with` block, no decorators, automatic cleanup. Many teams standardize on `mocker`. Cite: <https://pytest-mock.readthedocs.io/>

---

## 5. Mocking a network call end-to-end

Suppose this lives in `weather.py`:

```python
import requests


def get_temperature(city: str) -> float:
    url = f"https://api.example.com/weather?city={city}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return float(response.json()["temp_c"])
```

A complete test:

```python
from unittest.mock import MagicMock
import pytest
from weather import get_temperature


def test_get_temperature_happy_path(mocker) -> None:
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"temp_c": 18.5}
    fake_response.raise_for_status.return_value = None

    mock_get = mocker.patch("weather.requests.get", return_value=fake_response)

    temp = get_temperature("Boston")

    assert temp == 18.5
    mock_get.assert_called_once_with(
        "https://api.example.com/weather?city=Boston",
        timeout=5,
    )


def test_get_temperature_raises_on_404(mocker) -> None:
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    mocker.patch("weather.requests.get", return_value=fake_response)

    with pytest.raises(requests.HTTPError):
        get_temperature("Atlantis")
```

Notice the two tests cover the **happy path** (200 OK) and the **sad path** (404). Always test both. Real systems fail.

---

## 6. Test coverage

A test that passes proves only that *some* code worked. **Coverage** answers: how much of the code did the tests actually exercise?

Install `pytest-cov`:

```bash
pip install pytest-cov
```

Run:

```bash
pytest --cov=src --cov-report=term-missing
```

Output (excerpt):

```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/myapp/core.py        42      3    93%   17-19
src/myapp/util.py        11      0   100%
---------------------------------------------------
TOTAL                    53      3    94%
```

The `Missing` column shows the line numbers your tests never reached. Open the file at those lines and write a test.

### 6.1 Line vs branch coverage

Line coverage tells you whether each line ran. Branch coverage tells you whether each branch of an `if`/`elif`/`else` ran. They differ. Consider:

```python
def safe_divide(a: float, b: float) -> float:
    if b == 0:
        return 0.0
    return a / b
```

A single test `safe_divide(10, 2)` hits both lines of the function. Line coverage: 100 %. But the `if b == 0` branch where the condition is **True** never ran. Branch coverage catches that:

```bash
pytest --cov=src --cov-branch --cov-report=term-missing
```

Cite: <https://coverage.readthedocs.io/en/latest/branch.html>

### 6.2 Configuring coverage in `pyproject.toml`

```toml
[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 90
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

`fail_under` is gold — it fails the CI build if coverage drops below the threshold.

### 6.3 What 100 % does *not* guarantee

100 % coverage means every line ran. It does **not** mean every line was meaningfully tested. This passes coverage but proves nothing:

```python
def test_pointless() -> None:
    safe_divide(10, 2)
    safe_divide(10, 0)
```

Both branches ran. There is no `assert`. Coverage is a floor, not a ceiling. **Always pair coverage with assertions you would defend in code review.**

---

## 7. Debugging tools

When a test fails and you cannot tell why, you have four tools in order of escalation.

### 7.1 `print` debugging

The classic. Sprinkle `print(thing)` lines, run, read, remove. It works. It is also slow once the bug is more than two layers deep.

Two improvements every Python programmer should know:

```python
print(f"{user=}")           # f-string self-documenting form (Python 3.8+)
import pprint; pprint.pp(user)   # pretty-print for nested data
```

When the test captures stdout, pass `-s` to disable capture and see your prints:

```bash
pytest -s
```

### 7.2 `breakpoint()`

Since Python 3.7, the built-in `breakpoint()` drops you into a debugger:

```python
def slugify(text: str) -> str:
    breakpoint()
    return text.lower().replace(" ", "-")
```

By default this launches `pdb`. You can swap in better debuggers (`pdb++`, `ipdb`, the VS Code debugger) by setting `PYTHONBREAKPOINT`:

```bash
PYTHONBREAKPOINT=ipdb.set_trace pytest -s
```

Tell `pytest` not to capture stdout (`-s`), or you won't see the prompt. Cite: <https://docs.python.org/3/library/functions.html#breakpoint>

### 7.3 The `pdb` cheatsheet

You are at a `(Pdb)` prompt. The 12 commands you actually need:

| Command   | Short | Does                                                |
|-----------|-------|-----------------------------------------------------|
| `next`    | `n`   | Run the next line. Skip into function calls.        |
| `step`    | `s`   | Run the next line. Step into function calls.        |
| `continue`| `c`   | Run until the next breakpoint or program end.       |
| `return`  | `r`   | Run until the current function returns.             |
| `list`    | `l`   | Show 11 lines around the current line.              |
| `print`   | `p x` | Print the value of expression `x`.                  |
| `pp`      | `pp x`| Pretty-print `x`.                                   |
| `where`   | `w`   | Show the current call stack.                        |
| `up`      | `u`   | Move up one stack frame.                            |
| `down`    | `d`   | Move down one stack frame.                          |
| `break`   | `b 17`| Set a breakpoint at line 17 of the current file.    |
| `quit`    | `q`   | Exit the debugger.                                  |

Cite: <https://docs.python.org/3/library/pdb.html>

A common pdb session:

```
(Pdb) l                # show me where I am
(Pdb) pp users         # what's in this variable?
(Pdb) n                # advance one line
(Pdb) p users[0]["name"]
'Ada'
(Pdb) c                # resume
```

Two pro tips:

- Type `interact` to drop into a normal Python REPL with the current locals available. Useful for trying things without affecting the run.
- Type `pp locals()` to see every variable in scope.

### 7.4 VS Code debugger walkthrough

When you outgrow `pdb` (and you will), point-and-click is faster. In VS Code:

1. Open your project folder.
2. Click the gutter to the left of any line number — a red dot appears. That is a breakpoint.
3. Open the Run and Debug panel (`Shift+Cmd+D` / `Shift+Ctrl+D`).
4. Click **create a launch.json file** → **Python** → **Module** → enter `pytest`.

`launch.json` ends up looking like:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Pytest current file",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-s"],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

Hit `F5`. Execution pauses at your red dot. The left panel shows every local variable. Step controls are along the top. **Watch** lets you pin expressions. The Debug Console is a live Python REPL at the current frame — anything you could type in `pdb`, you can type there.

Once you have used a real debugger, you will rarely go back to `print`. Cite: <https://code.visualstudio.com/docs/python/debugging>

---

## 8. Logging vs printing

`print` is for humans during development. `logging` is for humans (and machines) in production.

```python
import logging

logger = logging.getLogger(__name__)


def fetch_user(user_id: int) -> dict:
    logger.info("Fetching user %s", user_id)
    response = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    if response.status_code != 200:
        logger.warning("Unexpected status %s for user %s", response.status_code, user_id)
    response.raise_for_status()
    return response.json()
```

Why bother?

- **Levels** — `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Filter what you see without editing code.
- **Configurable** — turn logging up to `DEBUG` when something breaks, back to `INFO` when it's calm.
- **Structured** — log JSON in production for parsing by tools like Datadog, ELK, or Grafana Loki.
- **No accidental leaks** — `print` debug output sometimes ships to production. Log statements at `DEBUG` level vanish.

Configure at the top of your entry point:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
```

`pytest`'s `caplog` fixture lets tests assert on log messages — useful for "this code path *should* warn":

```python
def test_unknown_user_warns(caplog) -> None:
    with caplog.at_level("WARNING"):
        fetch_user(99999)
    assert any("Unexpected status" in r.message for r in caplog.records)
```

Cite: <https://docs.python.org/3/library/logging.html>

---

## 9. The testing pyramid (in 200 words)

The pyramid is a heuristic for *how many* of each kind of test to write:

```
          ▲    (few)
         /e/   end-to-end:  full system, slowest, brittlest
        /---\
       / i  /   integration: a few modules together
      /-----\
     / unit  /  unit:        one function in isolation, fast
    /---------\
                (many)
```

A healthy suite is mostly unit tests (hundreds, milliseconds), some integration tests (dozens, seconds), and a small number of end-to-end tests (a handful, minutes). Inversions of this shape — the **ice-cream cone anti-pattern** — produce suites that are slow, flaky, and expensive to maintain.

This week you mostly write unit tests. In Week 9's challenge you saw integration tests with the Flask test client. End-to-end tools like Selenium and Playwright wait until later in your career.

---

## 10. Recap

- Mock at the **boundary** — network, time, randomness, external services.
- Patch where the name is **looked up**, not where it is defined.
- Coverage is a floor: 90 %+ with branch coverage is a reasonable target.
- `breakpoint()` is your first real debugger. `pdb` has 12 commands you actually need.
- The VS Code debugger is point-and-click `pdb`. Use it.
- Log when the user is the future you reading production. Print when the user is you, right now.
- Many small unit tests, a few integration tests, fewer end-to-end. The pyramid, not the cone.

Next up, **Lecture 3** is about the tools that run automatically every time you save, commit, or push — the quality net under the trapeze.

---

## Self-check

1. You patch `myapp.fetch` but the test still calls the real network. What is the most likely cause?
2. Your coverage report shows 100 % line coverage but a colleague says a branch is untested. How can both be true?
3. Inside `pdb`, how do you (a) see local variables, (b) move up the stack one frame, (c) inspect the current call stack?
4. Name two reasons to prefer `logging.info` over `print` in production code.
5. Sketch the layers of the testing pyramid and a one-sentence reason each layer exists.
