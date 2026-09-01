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
