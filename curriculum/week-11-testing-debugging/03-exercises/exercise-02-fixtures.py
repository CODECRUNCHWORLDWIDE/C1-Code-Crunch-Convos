"""
Exercise 02 — Sharing setup with fixtures.

Goal: use ``@pytest.fixture`` to provide sample data to several tests,
instead of building it inside every test.

Run with:

    pytest exercise-02-fixtures.py -v

Reference:
    https://docs.pytest.org/en/stable/how-to/fixtures.html
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Code under test.
# ---------------------------------------------------------------------------


def active_user_names(users: list[dict]) -> list[str]:
    """Return the names of users whose ``active`` flag is True."""
    return [u["name"] for u in users if u.get("active")]


def average_age(users: list[dict]) -> float:
    """Return the average ``age`` across all users.

    Raises ``ValueError`` if ``users`` is empty so that callers cannot
    silently divide by zero.
    """
    if not users:
        raise ValueError("cannot average an empty user list")
    return sum(u["age"] for u in users) / len(users)


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


# TODO 1: write a fixture named ``sample_users`` that returns the list below.
#
#     @pytest.fixture
#     def sample_users() -> list[dict]:
#         return [
#             {"id": 1, "name": "Ada",   "age": 36, "active": True},
#             {"id": 2, "name": "Linus", "age": 54, "active": False},
#             {"id": 3, "name": "Grace", "age": 79, "active": True},
#             {"id": 4, "name": "Alan",  "age": 41, "active": True},
#         ]


def test_active_user_names_returns_three(sample_users: list[dict]) -> None:
    """Three of the sample users are active."""
    # TODO 2: assert that ``active_user_names(sample_users)`` has length 3
    assert False, "replace me"


def test_active_user_names_order(sample_users: list[dict]) -> None:
    """The returned names should preserve input order."""
    # TODO 3: assert the result equals ["Ada", "Grace", "Alan"]
    assert False, "replace me"


def test_average_age(sample_users: list[dict]) -> None:
    """The average age across the fixture is (36 + 54 + 79 + 41) / 4 = 52.5."""
    # TODO 4: assert ``average_age(sample_users)`` equals 52.5
    assert False, "replace me"


def test_average_age_empty_list_raises() -> None:
    """Empty input should raise ``ValueError``."""
    # TODO 5: use ``pytest.raises`` to assert ValueError is raised.
    # Note: no fixture is needed here — pass [] directly.
    assert False, "replace me"


# ---------------------------------------------------------------------------
# Stretch goal — add a second fixture with ``scope="module"``.
# ---------------------------------------------------------------------------
#
# TODO 6 (optional): write a module-scoped fixture ``expensive_setup`` that
# prints "setting up" exactly once when the file is collected. Run pytest
# with ``-s`` to see the print and confirm the fixture runs only once.
