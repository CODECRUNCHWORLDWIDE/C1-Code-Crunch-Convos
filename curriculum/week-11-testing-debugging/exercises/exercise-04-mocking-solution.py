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
