# Homework Problem 4 — Overdue notice

> **Topic:** `MagicMock`, the `mocker` fixture, asserting on the POST payload, and no network
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) (sections 1–5)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** exercise 4 mocked a GET, where the whole story is the answer that comes back; this mocks a POST, where the interesting thing to check is the *payload you send out*, and the suite still has to pass with the network unplugged.

## The Brief

The tool library sends people a reminder when a tool comes back late. It does
not print a letter — it hands the message to a notification service over the
network. `notices.py` wraps that one job: it posts the reminder, and it returns
the confirmation id the service sends back so the library has a receipt.

You are going to test every part of that without a single packet leaving your
machine. A **mock** is a pretend object you hand to your code in place of the
real one. You tell the pretend object what to say, then check how your code
used it. Here the mock stands in for `requests.post`, the function that would
really talk to the network. Swap the real one for the pretend one and the whole
test can run with the wifi off, inside a locked-down CI box that has no way out,
or on a train going through a tunnel. If any of those breaks the suite, the
suite is quietly testing the network instead of your code.

## Starter

The module under test, already complete. Read it before you write a test — how
the import is written decides where you aim the patch:

```python
"""notices.py — post an overdue reminder to the notification service."""

import requests

NOTICE_URL = "https://notices.example.org/overdue"
TIMEOUT_SECONDS = 5


def send_overdue_notice(member_id: str, item: str) -> str:
    """Post an overdue notice and return the service's confirmation id.

    Raises ``requests.HTTPError`` on an error status and ``ValueError`` when the
    response body carries no confirmation id.
    """
    response = requests.post(
        NOTICE_URL,
        json={"member_id": member_id, "item": item},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    confirmation = response.json().get("confirmation_id", "")
    if not confirmation:
        raise ValueError(f"no confirmation id for member {member_id}")
    return confirmation
```

The test file you are here to write. `notices.py` says `import requests`, so in
this two-file layout the thing you patch is `"notices.requests.post"` — the
`post` name reached through the `notices` module:

```python
"""test_notices.py — tests for the overdue-notice client, with no network."""

from unittest.mock import MagicMock

import pytest
import requests

from notices import NOTICE_URL, send_overdue_notice


@pytest.fixture
def fake_response() -> MagicMock:
    """A stand-in for a successful requests Response."""
    response = MagicMock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {"confirmation_id": "cf-77"}
    return response


def test_returns_the_confirmation_id(mocker, fake_response) -> None:
    # TODO: mocker.patch("notices.requests.post", return_value=fake_response)
    # TODO: assert send_overdue_notice("m-1", "ladder") == "cf-77"


def test_posts_the_right_payload_once(mocker, fake_response) -> None:
    # TODO: keep a reference to the patched post
    # TODO: call send_overdue_notice("m-1", "ladder")
    # TODO: mock_post.assert_called_once_with(
    #           NOTICE_URL,
    #           json={"member_id": "m-1", "item": "ladder"},
    #           timeout=5)


def test_http_error_is_not_swallowed(mocker, fake_response) -> None:
    # TODO: fake_response.status_code = 503
    # TODO: fake_response.raise_for_status.side_effect = requests.HTTPError("503")
    # TODO: patch, then pytest.raises(requests.HTTPError) around the call


def test_missing_confirmation_raises_value_error(mocker, fake_response) -> None:
    # TODO: fake_response.json.return_value = {"status": "queued"}
    # TODO: patch, then pytest.raises(ValueError, match="no confirmation id")


def test_does_not_retry_on_success(mocker, fake_response) -> None:
    # TODO: keep a reference to the patched post
    # TODO: call send_overdue_notice("m-1", "ladder")
    # TODO: assert mock_post.call_count == 1
```

## Requirements

1. Every test patches the `requests.post` that `notices.py` actually calls. In
   this two-file layout the target is the string `"notices.requests.post"`. No
   test lets the real function run.
2. Use the `mocker` fixture from `pytest-mock`. It undoes each patch at
   teardown, so no test can leak a mock into the next one.
3. `test_posts_the_right_payload_once` asserts on the full call:
   `mock_post.assert_called_once_with(NOTICE_URL, json={"member_id": "m-1", "item": "ladder"}, timeout=5)`.
   The URL, the JSON body, and the timeout all in one line — not
   `assert mock_post.called`.
4. `test_http_error_is_not_swallowed` drives the failure through
   `fake_response.raise_for_status.side_effect`, the same way the real library
   does — not by raising from the patched `post` itself.
5. `test_missing_confirmation_raises_value_error` uses
   `match="no confirmation id"`.
6. `pytest -v` reports 5 passed, and the run finishes in well under a second.
7. No test mocks `send_overdue_notice` itself — mock the network boundary and
   let the function run for real.

## Constraints

- **A test that makes a real HTTP call is not a unit test.** A unit test
  isolates one function and gives the same answer every time. A real call drags
  in DNS, TLS, someone else's uptime, someone else's rate limit, and whatever
  data is in their database this morning. When it goes red you cannot tell
  whether your code broke or their server did, and a red light you cannot read
  is worse than no light.
- **Real calls also make the suite slow and unrunnable offline.** A mocked call
  comes back in microseconds; a network round trip takes tens or hundreds of
  milliseconds. Multiply by a few hundred tests and the suite stops being
  something you run on every save — and a suite you cannot run on a plane or in
  a tunnel is a suite people start skipping.
- **You cannot summon a 503 on demand from a healthy server.** The sad path is
  where the bugs hide, and mocking is the only reliable way to visit it. Setting
  `raise_for_status.side_effect = requests.HTTPError(...)` hands you a broken
  server whenever you want one.
- **Patch where the name is looked up, not where it is defined.** `notices.py`
  writes `import requests` and calls `requests.post` at run time, so the target
  is `notices.requests.post`. Aim there and the test survives a refactor.
- **Do not mock `send_overdue_notice` itself.** Mocking the thing you are
  testing produces a test that only proves your mock returns what you told it
  to. Mock at the boundary — the network — and let everything inside run.
- **Assert on the payload and the return value — the contract.** What you are
  really promising is *this member id and this item go out as JSON*, and *the
  confirmation id comes back*. Do not pin `response.json.call_count`; that
  freezes the implementation and breaks on a harmless refactor.

## Expected output

The shipped answer folds `notices.py`, the five tests, and a driver into one
file so it runs as a plain script. Because it is a single module, it patches the
boundary with `mocker.patch.object(requests, "post", ...)` — the
object-and-name form of the same idea. It runs the suite through pytest and
reports:

```text
$ python problem-04-overdue-notice-solution.py
Five tests that 'post a reminder' without touching the network.
Every call is a MagicMock standing in for requests.post('https://notices.example.org/overdue').

The five tests, run the way pytest runs them:
  PASS  test_returns_the_confirmation_id
  PASS  test_posts_the_right_payload_once
  PASS  test_http_error_is_not_swallowed
  PASS  test_missing_confirmation_raises_value_error
  PASS  test_does_not_retry_on_success

5 passed, 0 failed
```

Doing it for real, you run `pytest -v` and see five `PASSED` lines in a fraction
of a second — that speed is itself the evidence that nothing left the machine.

## Steps

1. Install the plugin: `python -m pip install pytest-mock`. Confirm it loaded —
   `pytest -v` prints a `plugins: mock-...` line in the header.
2. Save `notices.py` and `test_notices.py` side by side.
3. Fill in the first test. Run `pytest -v -k returns`. One passed.
4. Fill in the rest one at a time, running after each. Resist writing all five
   and then debugging five failures at once.
5. Run `pytest -v`. Five passed, well under a second.
6. The real check: turn off your wifi and run `pytest -v` again. Identical
   output. If anything changes, a test is reaching the network.
7. Break the patch string on purpose — `"notices.request.post"`, missing the
   `s` — and read the error. Learn to recognize it now, not at midnight.

## The Solution

```python
"""problem-04-overdue-notice-solution.py — a mocked POST, proven headless.

``send_overdue_notice`` posts a reminder to a notification service. Exercise 4
mocked a GET; this one mocks a POST, where the interesting assertion is on the
*payload* you send, not just the URL. Not one packet leaves the machine: a
``MagicMock`` stands in for ``requests.post``, so the tests run offline and the
same way every time.

One file carries the module, the tests, and a ``main()`` that drives pytest and
prints a plain, same-every-time report.

Run it with::

    python problem-04-overdue-notice-solution.py
"""

from __future__ import annotations

import contextlib
import io
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

# --------------------------------------------------------------------------- #
# notices.py — the module under test, given complete
# --------------------------------------------------------------------------- #

NOTICE_URL = "https://notices.example.org/overdue"
TIMEOUT_SECONDS = 5


def send_overdue_notice(member_id: str, item: str) -> str:
    """Post an overdue notice and return the service's confirmation id.

    Raises ``requests.HTTPError`` on an error status and ``ValueError`` when the
    response body carries no confirmation id.
    """
    response = requests.post(
        NOTICE_URL,
        json={"member_id": member_id, "item": item},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    confirmation = response.json().get("confirmation_id", "")
    if not confirmation:
        raise ValueError(f"no confirmation id for member {member_id}")
    return confirmation


# --------------------------------------------------------------------------- #
# test_notices.py — five tests, none of which touch the network
# --------------------------------------------------------------------------- #


@pytest.fixture
def fake_response() -> MagicMock:
    """A stand-in for a successful requests Response."""
    response = MagicMock()
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {"confirmation_id": "cf-77"}
    return response


def test_returns_the_confirmation_id(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A healthy post returns the id the service sent back."""
    mocker.patch.object(requests, "post", return_value=fake_response)
    assert send_overdue_notice("m-1", "ladder") == "cf-77"


def test_posts_the_right_payload_once(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """Exactly one post, to the right URL, with the member and item as JSON."""
    mock_post = mocker.patch.object(requests, "post", return_value=fake_response)
    send_overdue_notice("m-1", "ladder")
    mock_post.assert_called_once_with(
        NOTICE_URL,
        json={"member_id": "m-1", "item": "ladder"},
        timeout=5,
    )


def test_http_error_is_not_swallowed(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """An error status reaches the caller instead of being hidden."""
    fake_response.status_code = 503
    fake_response.raise_for_status.side_effect = requests.HTTPError("503")
    mocker.patch.object(requests, "post", return_value=fake_response)
    with pytest.raises(requests.HTTPError):
        send_overdue_notice("m-1", "ladder")


def test_missing_confirmation_raises_value_error(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A body with no confirmation id is a data problem, and says so."""
    fake_response.json.return_value = {"status": "queued"}
    mocker.patch.object(requests, "post", return_value=fake_response)
    with pytest.raises(ValueError, match="no confirmation id"):
        send_overdue_notice("m-1", "ladder")


def test_does_not_retry_on_success(
    mocker: MockerFixture, fake_response: MagicMock
) -> None:
    """A single successful notice makes a single call."""
    mock_post = mocker.patch.object(requests, "post", return_value=fake_response)
    send_overdue_notice("m-1", "ladder")
    assert mock_post.call_count == 1


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
    print("Five tests that 'post a reminder' without touching the network.")
    print(f"Every call is a MagicMock standing in for requests.post({NOTICE_URL!r}).")
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

**A real HTTP call is not a unit test, and the whole argument is about what red
means.** A unit test isolates one function and answers the same way every run,
so red means *your code changed and broke*. Put a real network call in the
middle and the red light now has half a dozen possible causes: your code, their
code, DNS, TLS, their rate limiter, and whatever data is in their database this
morning. A signal you must investigate before you can even read it is not a
signal; it is a chore, and teams silence chores. It also cannot reach the
interesting half — you cannot ask a healthy server for a 503.
`raise_for_status.side_effect = requests.HTTPError("503")` hands you a broken
server on demand, in microseconds.

**Patch the boundary, and patch the name the caller looks up.** In the two-file
layout, `notices.py` holds its own reference to the `requests` module, so the
target is `notices.requests.post`. This single-file download has no separate
`notices` module, so it patches the same boundary through the object itself:
`mocker.patch.object(requests, "post", ...)` replaces `post` on the very
`requests` object `send_overdue_notice` calls. Both forms replace the same
function; what you must never do is patch `send_overdue_notice`, because then
none of your code runs and the test asserts nothing.

**The assertion is on the payload, because the payload is the promise.** A GET
test mostly cares about the URL and the answer. A POST *sends* something, and
that something is the point: `assert_called_once_with(NOTICE_URL, json={"member_id": "m-1", "item": "ladder"}, timeout=5)`
pins four things at once — exactly one request went out, it went to the right
URL, the member and item were shaped into the JSON body correctly, and a
timeout was passed. Get the body wrong and the real service reminds the wrong
person about the wrong tool; nothing else in the test would catch that.

**The `side_effect` belongs on `raise_for_status`, not on the patched `post`.**
This looks fussy and is not. Both versions pass today, but only one tests the
line you care about. Delete `response.raise_for_status()` from `notices.py` and
the correct test — the one that drives the error through `raise_for_status` —
goes red; the version that raises from `post` itself stays green, because it is
only asserting that a mock you configured does what you configured it to. Drive
the failure through the same object the real library drives it through.

**`mocker` undoes its own work.** Every patch started through the `mocker`
fixture is reverted at teardown, so no test can leak a mock into the next one.
That is the whole reason to prefer it over calling `unittest.mock.patch(...)` by
hand, where forgetting to stop the patch leaves a mock alive in an unrelated
test file.

## Download and run

Download
[problem-04-overdue-notice-solution.py](./problem-04-overdue-notice-solution.py)
and run it:

```bash
python problem-04-overdue-notice-solution.py
```

It needs `pytest`, `pytest-mock`, and `requests` installed. It never opens a
socket. Your own work is `notices.py` plus `test_notices.py`, run with
`pytest -v`.

The `-solution` in the filename keeps this file from colliding with your own
`notices.py` and `test_notices.py`.

## Common bugs to catch

- **`AttributeError: <module 'notices'> does not have the attribute 'post'`.**
  You patched `notices.post`. That name only exists if the module wrote
  `from requests import post`. This one writes `import requests`, so the target
  is `notices.requests.post`.
- **`ModuleNotFoundError: No module named 'notice'`.** A typo inside the patch
  string — you dropped the `s`. Patch targets are plain strings, so your editor
  cannot check them and the mistake surfaces only at run time. This is the loud,
  good version of the failure.
- **`fixture 'mocker' not found`.** `pytest-mock` is missing, or installed in a
  different environment than the one running `pytest`. Check the `plugins:` line
  in the header.
- **`requests.exceptions.ConnectionError` / `[Errno 11001] getaddrinfo failed`.**
  The patch was not active for that call. Either you patched inside a `with`
  block that had already exited, or you patched after the call instead of
  before.
- **The test passes even with the assertion deleted.** You mocked
  `send_overdue_notice` instead of the network, so none of your code ran. The
  patch target must end in `requests.post`, never the function under test.
- **`AssertionError: expected call not found`, with both calls printed below.**
  Read the two lines side by side. Usually the `json=` payload dict differs by a
  key or a value, or `timeout=5` is missing from your expectation.

## Under the hood

<details>
<summary>Under the hood — proving there is no network, and where the boundary really is</summary>

The homework says to turn off your wifi. Here is a version you can keep, that
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

Notice it guards `socket.getaddrinfo` as well as `socket.socket`. Blocking only
`socket.socket` is not enough: before your code can open a socket it has to turn
`notices.example.org` into an address, and that name lookup — `getaddrinfo` —
happens first and would still go out to your DNS server. That is the same lesson
as the patch target, one layer down: find the boundary the code actually
crosses, and block *that* one.

</details>

## Acceptance checklist

- [ ] Every test patches the network boundary via the `mocker` fixture, never
      the function under test.
- [ ] `pytest -v` reports 5 passed in under a second.
- [ ] The suite passes with the network disconnected.
- [ ] One test asserts the full outbound call: URL, `json={...}` payload, and
      `timeout=5`.
- [ ] Both the 503 path and the missing-confirmation-id path are covered.
- [ ] No test mocks `send_overdue_notice` itself.
- [ ] Committed with a message like
      `Add Week 11 homework problem 4: mocked POST for the overdue-notice client`.

## Stretch

- Read `NOTICE_URL` from the environment in `notices.py`, then test it with
  `monkeypatch.setenv`. Environment variables are the other boundary you will
  patch constantly.
- Give `fake_response.json` a `side_effect` that raises when the service returns
  HTML instead of JSON, then decide what `send_overdue_notice` should do about
  it and make it do that.
- Add a retry-once behaviour: on the first failed post, try a second time. Test
  it by giving the patched `post` a `side_effect` list and asserting
  `mock_post.call_count == 2`.

When your five are green and the suite runs offline, move on to
[Problem 5 — Fine schedule](./problem-05-fine-schedule.md).
