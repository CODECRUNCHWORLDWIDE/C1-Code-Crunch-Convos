# Exercise 4 — Mocking a Network Call

> **Topic:** `MagicMock`, the `mocker` fixture, patching the boundary, and asserting on the call
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) (sections 1–5)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** every project you build after this week talks to something you do not control — an API, a clock, a payment processor. If you cannot fake that boundary, you will either write no tests for the interesting half of your code or write tests that fail on the train. Mocking is also the single most common place beginners patch the wrong thing and quietly test nothing at all, so it is worth doing slowly once.

## The Brief

The tool library shares a catalog service with four other neighborhood
libraries. Given a tool id, the service returns a JSON record with a display
name. `catalog.py` wraps that call and does three small jobs: it asks the
service, it refuses to swallow an error status, and it cleans up the name before
handing it back. That last part matters because volunteers type the catalog
entries by hand and roughly one in ten arrives with a trailing space.

You are going to test all of it without a single packet leaving your machine. A
**mock** is a pretend object you hand to your code in place of the real one; you
tell it what to return, then check how your code used it. Here the mock stands in
for `requests.get`, so the suite must pass with your wifi off, in a CI runner
with no outbound network, and on the day the catalog service is down for
maintenance. If any of those break it, the suite is testing the wrong thing.

## Starter

The module under test, already complete. Read it before you write a test — the
patch target depends on how the import is written:

```python
"""catalog.py — look up tool records in the shared catalog service."""

import requests

CATALOG_URL = "https://catalog.example.org/tools"
TIMEOUT_SECONDS = 5


def fetch_tool_name(tool_id: str) -> str:
    """Return the display name for a tool id from the catalog service.

    Args:
        tool_id: The catalog identifier, e.g. ``"t-014"``.

    Returns:
        The trimmed display name.

    Raises:
        requests.HTTPError: If the service answers with an error status.
        ValueError: If the response body carries no usable name.
    """
    response = requests.get(f"{CATALOG_URL}/{tool_id}", timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    name = response.json().get("name", "").strip()
    if not name:
        raise ValueError(f"catalog returned no name for tool {tool_id}")
    return name
```

The test file you are here to write:

```python
"""test_catalog.py — tests for the catalog client, with no network access."""

from unittest.mock import MagicMock

import pytest
import requests

from catalog import fetch_tool_name


@pytest.fixture
def fake_response() -> MagicMock:
    """A stand-in for a successful requests Response."""
    response = MagicMock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {"id": "t-014", "name": "Circular Saw"}
    return response


def test_returns_the_name_from_the_payload(mocker, fake_response) -> None:
    # TODO: mocker.patch("catalog.requests.get", return_value=fake_response)
    # TODO: assert fetch_tool_name("t-014") == "Circular Saw"


def test_trims_whitespace_from_the_name(mocker, fake_response) -> None:
    # TODO: set fake_response.json.return_value to {"name": "  Hedge Trimmer \n"}
    # TODO: patch, call, assert the result is exactly "Hedge Trimmer"


def test_calls_the_catalog_url_once_with_a_timeout(mocker, fake_response) -> None:
    # TODO: keep a reference to the patched get
    # TODO: call fetch_tool_name("t-014")
    # TODO: mock_get.assert_called_once_with(
    #           "https://catalog.example.org/tools/t-014", timeout=5)


def test_http_error_is_not_swallowed(mocker, fake_response) -> None:
    # TODO: fake_response.status_code = 404
    # TODO: fake_response.raise_for_status.side_effect = requests.HTTPError("404")
    # TODO: patch, then pytest.raises(requests.HTTPError) around the call


def test_missing_name_raises_value_error(mocker, fake_response) -> None:
    # TODO: fake_response.json.return_value = {"id": "t-014"}
    # TODO: patch, then pytest.raises(ValueError, match="no name")
```

## Requirements

1. Every test patches the `requests.get` that `catalog.py` calls. In your
   two-file layout the target is the string `"catalog.requests.get"`. No test
   lets the real function run.
2. Use the `mocker` fixture from `pytest-mock`. It undoes each patch at
   teardown, so no test can leak a mock into the next one.
3. `test_calls_the_catalog_url_once_with_a_timeout` asserts on the full call:
   the exact URL string *and* `timeout=5`. Use `assert_called_once_with`, not
   `assert mock_get.called`.
4. `test_trims_whitespace_from_the_name` asserts equality against
   `"Hedge Trimmer"` with no surrounding whitespace. An `in` check would pass
   even if the trim never happened.
5. `test_http_error_is_not_swallowed` drives the failure through
   `raise_for_status.side_effect`, the same way the real library does — not by
   raising from the patched `get` itself.
6. `test_missing_name_raises_value_error` uses `match="no name"`.
7. `pytest -v` reports 5 passed, and the run finishes in well under a second.

## Constraints

- **A test that makes a real HTTP call is not a unit test.** A unit test
  isolates one function and gives the same answer every time. A real call brings
  in DNS, TLS, someone else's uptime, someone else's rate limit, and whatever
  data happens to be in their database this morning. When it goes red you cannot
  tell whether your code broke or their server did, and a red light you cannot
  interpret is worse than no light.
- **Real calls also make the suite slow and unrunnable offline.** A mocked call
  returns in microseconds; a network round trip takes tens or hundreds of
  milliseconds. Multiply by a few hundred tests and the suite stops being
  something you run on every save. And a suite you cannot run on a plane, in a
  tunnel, or in a locked-down CI runner is a suite people start skipping.
- **You cannot summon a 404 on demand from a healthy server.** The sad path is
  where the bugs live, and mocking is the only way to test it reliably. Setting
  `side_effect = requests.HTTPError(...)` gives you a 404 whenever you want one.
- **Patch where the name is looked up, not where it is defined.** `catalog.py`
  writes `import requests` and calls `requests.get` at run time, so the target is
  `catalog.requests.get`. Patching the global `requests.get` happens to work too
  — same module object — until someone rewrites the import as
  `from requests import get`, at which point the global patch stops intercepting
  and your test silently hits the network. Patch the path the calling module
  actually uses and the test survives the refactor.
- **Do not mock `fetch_tool_name` itself.** Mocking the thing you are testing
  produces a test that asserts your mock returns what you told it to return.
  Mock at the boundary — the network — and let everything inside run for real.
- **Do not assert on `response.json.call_count`.** That pins the implementation:
  a refactor that caches the parsed body breaks the test without breaking the
  behavior. Assert on what `fetch_tool_name` returns and on the outbound call it
  makes. Those are the contract.

## Expected output

The shipped answer below folds `catalog.py`, the five tests, and a driver into
one file so it runs as a plain script. Because it is one module, it patches the
boundary with `mocker.patch.object(requests, "get", ...)` — the object-and-name
form of the same idea. It runs the suite through pytest and reports:

```text
$ python exercise-04-mocking-solution.py
Five tests that 'talk to an API' without touching the network.
Every call is a MagicMock standing in for requests.get('https://catalog.example.org/tools/t-014').

The five tests, run the way pytest runs them:
  PASS  test_returns_the_name_from_the_payload
  PASS  test_trims_whitespace_from_the_name
  PASS  test_calls_the_catalog_url_once_with_a_timeout
  PASS  test_http_error_is_not_swallowed
  PASS  test_missing_name_raises_value_error

5 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see five `PASSED` lines in a fraction
of a second — that speed is itself the evidence that nothing left the machine.

## Steps

1. Install the plugin: `python -m pip install pytest-mock`. Confirm it loaded —
   `pytest -v` prints a `plugins: mock-...` line in the header.
2. Save `catalog.py` and `test_catalog.py` side by side.
3. Fill in the first test. Run `pytest -v -k returns`. One passed.
4. Fill in the rest one at a time, running after each. Resist writing all five
   and then debugging five failures at once.
5. Run `pytest -v`. Five passed, well under a second.
6. The real check: turn off your wifi and run `pytest -v` again. Identical
   output. If anything changes, a test is reaching the network.
7. Break the patch string on purpose — `"catalog.request.get"`, missing the `s`
   — and read the error. Learn to recognize it now rather than at midnight.

## The Solution

```python
"""exercise-04-mocking-solution.py — mocked network tests, proven headless.

Normally you keep ``catalog.py`` and ``test_catalog.py`` in two files and run
``pytest``. A published answer is run as a plain script, so this one file
carries the module, the five tests, and a ``main()`` that drives pytest itself
and prints a plain, same-every-time report.

Not one packet leaves the machine. ``requests.get`` is never really called: a
``MagicMock`` — a stand-in object that answers however you tell it to — takes
its place, so the tests run with the wifi off, in a locked-down CI box, on a
train in a tunnel, all identically. That is the whole point of a *unit* test:
it must answer the same way every time, which a real network cannot promise.

Run it with::

    python exercise-04-mocking-solution.py
"""

from __future__ import annotations

import contextlib
import io
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

# --------------------------------------------------------------------------- #
# catalog.py — the module under test, given complete
# --------------------------------------------------------------------------- #

CATALOG_URL = "https://catalog.example.org/tools"
TIMEOUT_SECONDS = 5


def fetch_tool_name(tool_id: str) -> str:
    """Return the display name for a tool id from the shared catalog service.

    Asks the service, refuses to swallow an error status, and trims the name
    before handing it back (volunteers type the entries by hand). Raises
    ``requests.HTTPError`` on an error status and ``ValueError`` when the body
    carries no usable name.
    """
    response = requests.get(f"{CATALOG_URL}/{tool_id}", timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    name = response.json().get("name", "").strip()
    if not name:
        raise ValueError(f"catalog returned no name for tool {tool_id}")
    return name


# --------------------------------------------------------------------------- #
# test_catalog.py — five tests, none of which touch the network
# --------------------------------------------------------------------------- #

TOOL_URL = "https://catalog.example.org/tools/t-014"


@pytest.fixture
def fake_response() -> MagicMock:
    """A stand-in for a successful requests Response."""
    response = MagicMock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {"id": "t-014", "name": "Circular Saw"}
    return response


def test_returns_the_name_from_the_payload(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A healthy lookup returns the name the service sent."""
    mocker.patch.object(requests, "get", return_value=fake_response)
    assert fetch_tool_name("t-014") == "Circular Saw"


def test_trims_whitespace_from_the_name(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A hand-typed entry with stray whitespace is cleaned before return."""
    fake_response.json.return_value = {"name": "  Hedge Trimmer \n"}
    mocker.patch.object(requests, "get", return_value=fake_response)
    assert fetch_tool_name("t-014") == "Hedge Trimmer"


def test_calls_the_catalog_url_once_with_a_timeout(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """Exactly one outbound call, to the right URL, carrying a timeout."""
    mock_get = mocker.patch.object(requests, "get", return_value=fake_response)
    fetch_tool_name("t-014")
    mock_get.assert_called_once_with(TOOL_URL, timeout=5)


def test_http_error_is_not_swallowed(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """An error status reaches the caller instead of being hidden."""
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.HTTPError("404")
    mocker.patch.object(requests, "get", return_value=fake_response)
    with pytest.raises(requests.HTTPError):
        fetch_tool_name("t-014")


def test_missing_name_raises_value_error(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A payload with no usable name is a data problem, and says so."""
    fake_response.json.return_value = {"id": "t-014"}
    mocker.patch.object(requests, "get", return_value=fake_response)
    with pytest.raises(ValueError, match="no name"):
        fetch_tool_name("t-014")


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Run the five mocked tests and report — no packet leaves the machine."""
    print("Five tests that 'talk to an API' without touching the network.")
    print(f"Every call is a MagicMock standing in for requests.get({TOOL_URL!r}).")
    print()
    print("The five tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
```

**A real HTTP call is not a unit test, and the reason is about what red means.**
A unit test isolates one function and answers the same way every run, so red
means *your code changed and broke*. Put a real network call in the middle and
the red light now has at least six possible causes: your code, their code, DNS,
TLS, their rate limiter, and whatever data is in their database this morning. A
signal you must investigate before you can read it is not a signal; it is a
chore, and teams silence chores. It is also not repeatable (the catalog can
retype a row overnight), not runnable (no wifi, a tunnel, a locked-down CI box),
and — worst — it cannot reach the interesting half: you cannot ask a healthy
server for a 404. `raise_for_status.side_effect = requests.HTTPError("404")`
hands you a broken server on demand, in microseconds.

**Patch the boundary, and patch the name the caller looks up.** In the two-file
layout, `catalog.py` holds its own reference to the `requests` module, so the
target is `catalog.requests.get`. This single-file download has no separate
`catalog` module, so it patches the same boundary through the object itself:
`mocker.patch.object(requests, "get", ...)` replaces `get` on the very
`requests` object `fetch_tool_name` calls. Both forms replace the same function;
what you must never do is patch `fetch_tool_name`, because then none of your code
runs and the test asserts nothing.

**The `side_effect` belongs on `raise_for_status`, not on the patched `get`.**
This looks fussy and is not. Both versions pass today, but only one tests the
line you care about. Delete `response.raise_for_status()` from `catalog.py` and
the correct test — the one that drives the error through `raise_for_status` — goes
red; the version that raises from `get` itself stays green, because it is only
asserting that a mock you configured does what you configured it to. Drive the
failure through the same object the real library drives it through.

**Assert on the whole call, not that a call happened.** `assert mock_get.called`
is satisfied by any call to any URL with any arguments.
`mock_get.assert_called_once_with(TOOL_URL, timeout=5)` pins three things at
once: exactly one request went out, the id landed in the path correctly, and the
timeout was passed. That last one matters more than it looks — a `requests.get`
with no timeout can hang forever, and there is no other way to notice a missing
timeout from the outside.

**`mocker` undoes its own work.** Every patch started through the `mocker`
fixture is reverted at teardown, so no test can leak a mock into the next one.
That is the whole reason to prefer it over calling `unittest.mock.patch(...)`
by hand, where forgetting to stop the patch leaves a mock alive in an unrelated
test file.

## Download and run

Download
[exercise-04-mocking-solution.py](./exercise-04-mocking-solution.py)
and run it:

```bash
python exercise-04-mocking-solution.py
```

It needs `pytest`, `pytest-mock`, and `requests` installed. It never opens a
socket. Your own work is `catalog.py` plus `test_catalog.py`, run with
`pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`catalog.py` and `test_catalog.py`.

## Common bugs to catch

- **`AttributeError: <module 'catalog'> does not have the attribute 'get'`.**
  You patched `catalog.get`. That name only exists if the module wrote
  `from requests import get`. This one writes `import requests`, so the target
  is `catalog.requests.get`.
- **`ModuleNotFoundError: No module named 'catlog'`.** A typo inside the patch
  string. Patch targets are plain strings, so your editor cannot check them and
  the mistake surfaces only at run time — this is the loud, good version of the
  failure.
- **`fixture 'mocker' not found`.** `pytest-mock` is missing, or installed in a
  different environment than the one running `pytest`. Check the `plugins:`
  line.
- **`requests.exceptions.ConnectionError: Failed to resolve 'catalog.example.org'`.**
  The patch was not active for that call. Either you patched inside a `with`
  block that had already exited, or you patched after the call instead of
  before. On Windows the same failure reads `[Errno 11001] getaddrinfo failed`.
- **The test passes even with the assertion deleted.** You mocked
  `fetch_tool_name` instead of the network, so none of your code ran. The patch
  target must end in `requests.get`, never the function under test.
- **`AssertionError: expected call not found`, with both calls printed below.**
  Read the two lines side by side. Usually the URL is right and `timeout=5` is
  missing from your expectation, or you wrote `timeout=5.0` where the code
  passes the integer `5`.
- **`test_http_error_is_not_swallowed` still passes after you delete
  `response.raise_for_status()` from `catalog.py`.** You attached the
  `side_effect` to the patched `get` instead of to
  `fake_response.raise_for_status`, so the error fires before your code reaches
  the line you meant to test.

## Under the hood

<details>
<summary>Under the hood — proving there is no network, and finding the real boundary</summary>

The exercise says to turn off your wifi. Here is a version you can keep, that
proves the claim without leaving the terminal. Drop this `conftest.py` next to
the tests:

```python
"""conftest.py — prove that no test in this folder touches the network."""

import socket

import pytest


@pytest.fixture(autouse=True)
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make any attempt to resolve a host or open a socket fail loudly."""

    def refuse(*args: object, **kwargs: object) -> None:
        raise RuntimeError("this test tried to use the network")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
```

`autouse=True` means every test in the folder gets it for free. With the five
correct tests in place, nothing changes. Remove one `mocker.patch` line and the
guard names the offender immediately — a far better failure than a DNS timeout.

Notice it patches `socket.getaddrinfo` as well as `socket.socket`. Guarding only
`socket.socket` is not enough: name resolution happens first and would still go
out to your DNS server. That is the same lesson as the patch target, one layer
down — find the boundary the code actually crosses, and block *that*.

</details>

## Acceptance checklist

- [ ] Every test patches the network boundary via the `mocker` fixture, never
      the function under test.
- [ ] `pytest -v` reports 5 passed in under a second.
- [ ] The suite passes with the network disconnected.
- [ ] One test asserts the exact outbound URL and `timeout=5`.
- [ ] Both the 404 path and the missing-name path are covered.
- [ ] No test mocks `fetch_tool_name` itself.
- [ ] Committed with a message like
      `Add Week 11 exercise 4: mocked tests for the catalog client`.

## Stretch

- Rewrite one test with `unittest.mock.patch` as a context manager and another
  with `@patch` as a decorator. Same coverage, three styles. Pick the one you
  would want to read in six months and write down why.
- Read `CATALOG_URL` from the environment in `catalog.py`, then test it with
  `monkeypatch.setenv`. Environment variables are the other boundary you will
  patch constantly.
- Give `fake_response.json` a `side_effect` that raises when the service returns
  HTML instead of JSON, then decide what `fetch_tool_name` should do about it
  and make it do that.

When your five are green and the suite runs offline, move on to
[Exercise 5 — Finding the Missing Branch](./exercise-05-coverage-gap.md).
