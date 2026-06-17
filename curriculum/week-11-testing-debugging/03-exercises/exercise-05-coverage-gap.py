"""
Exercise 05 — Find the missing branch with coverage.

Goal: run pytest with branch coverage, notice that one branch of
``shipping_cost`` is never tested, and add the missing test.

Step 1 — install pytest-cov if you have not yet:

    python -m pip install pytest pytest-cov

Step 2 — run pytest with branch coverage:

    pytest exercise-05-coverage-gap.py --cov=. --cov-branch --cov-report=term-missing

Step 3 — read the report. You should see a missing branch in
``shipping_cost``. The two existing tests below cover only one of the
two paths through the ``if cart_total >= FREE_SHIPPING_THRESHOLD``
branch.

Step 4 — add the missing test (see TODO at the bottom) so coverage
reaches 100% for both line *and* branch.

Reference:
    https://pytest-cov.readthedocs.io/
    https://coverage.readthedocs.io/en/latest/branch.html
"""

from __future__ import annotations

FREE_SHIPPING_THRESHOLD: float = 50.0
FLAT_SHIPPING_FEE: float = 4.99


# ---------------------------------------------------------------------------
# Code under test.
# ---------------------------------------------------------------------------


def shipping_cost(cart_total: float) -> float:
    """Return the shipping fee for an order.

    Orders at or above ``FREE_SHIPPING_THRESHOLD`` ship for free.
    Orders below it pay the flat ``FLAT_SHIPPING_FEE``.
    Negative totals are not allowed and raise ``ValueError``.
    """
    if cart_total < 0:
        raise ValueError("cart_total cannot be negative")
    if cart_total >= FREE_SHIPPING_THRESHOLD:
        return 0.0
    return FLAT_SHIPPING_FEE


# ---------------------------------------------------------------------------
# Existing tests — DO NOT delete these. Just add the missing one.
# ---------------------------------------------------------------------------


def test_shipping_cost_above_threshold_is_free() -> None:
    """A 60-dollar cart should ship for free."""
    assert shipping_cost(60.0) == 0.0


def test_shipping_cost_at_threshold_is_free() -> None:
    """Exactly the threshold should also ship free (``>=``, not ``>``)."""
    assert shipping_cost(50.0) == 0.0


# ---------------------------------------------------------------------------
# TODO 1: add a test for the *other* branch — a cart **below** the
# threshold should pay ``FLAT_SHIPPING_FEE``. Name your test something
# like ``test_shipping_cost_below_threshold_pays_flat_fee``.
#
# TODO 2 (bonus): add a test that asserts a negative cart total raises
# ``ValueError``. Once both TODOs are done, re-run the coverage command
# from the top of this file. You should see 100% line and 100% branch
# coverage for this module.
# ---------------------------------------------------------------------------
