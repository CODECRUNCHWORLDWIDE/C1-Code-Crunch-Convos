"""
Exercise 04 — Mocking ``requests.get``.

Goal: test a function that calls a real HTTP API, without ever making a
real HTTP call. We use ``unittest.mock.patch`` (the standard library
mock) to swap ``requests.get`` for a fake.

Run with:

    pytest exercise-04-mocking.py -v

If you do not have ``requests`` installed::

    python -m pip install requests pytest pytest-mock

Reference:
    https://docs.python.org/3/library/unittest.mock.html
    https://docs.pytest.org/en/stable/how-to/monkeypatch.html
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests


# ---------------------------------------------------------------------------
# Code under test.
# ---------------------------------------------------------------------------


def get_github_user(username: str) -> dict:
    """Return the JSON payload describing a GitHub user.

    Raises ``requests.HTTPError`` for any non-2xx response.
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


def test_get_github_user_happy_path() -> None:
    """When the API returns 200, the function returns the JSON payload."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "login": "octocat",
        "id": 583231,
        "name": "The Octocat",
    }
    fake_response.raise_for_status.return_value = None

    # TODO 1: patch ``requests.get`` in *this* module so the call inside
    # ``get_github_user`` is intercepted.
    #
    # Hint: the function uses ``requests.get``, imported at the top of
    # this file. The patch target is the name where it is *looked up*,
    # which is ``__main__.requests.get`` when this file is run directly
    # — but when pytest runs it, the target is this module's full dotted
    # name. The portable solution is to patch the ``requests`` module
    # directly:
    #
    #     with patch("requests.get", return_value=fake_response) as mocked_get:
    #         user = get_github_user("octocat")
    #
    # Replace ``assert False`` below with the patch + call + assertions.
    assert False, "replace me with a patched call to get_github_user"


def test_get_github_user_calls_correct_url() -> None:
    """We should request the user-by-name endpoint with a timeout."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"login": "octocat"}
    fake_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=fake_response) as mocked_get:
        get_github_user("octocat")

    # TODO 2: assert that ``mocked_get`` was called exactly once with the
    # URL "https://api.github.com/users/octocat" and ``timeout=5``.
    # Hint: ``mocked_get.assert_called_once_with(...)``.
    assert False, "replace me"


def test_get_github_user_raises_on_404() -> None:
    """A 404 response must raise ``requests.HTTPError``."""
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    # TODO 3: patch ``requests.get`` to return ``fake_response`` and assert
    # that ``get_github_user("nope-not-a-real-user")`` raises HTTPError.
    # Use ``pytest.raises(requests.HTTPError)``.
    assert False, "replace me"
