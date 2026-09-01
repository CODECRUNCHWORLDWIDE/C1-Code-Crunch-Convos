"""exercise-05-coverage-gap-solution.py — coverage, statement and branch, headless.

Coverage answers exactly one question — which lines ran — and people read it as
an answer to a different one: is this code tested. This file watches the gap
between those two questions open twice, once at 78 % and once at 96 %.

A coverage run needs a real module and a real test file on disk, so this script
writes ``holds.py`` and ``test_holds.py`` into a throwaway folder, then shells
out to ``pytest --cov`` four times — once per column of the story — and prints
only the stable numbers it parses back. No timings, no banners: the report is
the same on every machine.

Run it with::

    python exercise-05-coverage-gap-solution.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------- #
# The two files coverage will measure — written to a temp folder at run time
# --------------------------------------------------------------------------- #

HOLDS_PY = '''\
"""holds.py — shelf status, fee caps, and member notices."""

FEE_CAP_CENTS: int = 1_000


def shelf_status(copies: int, holds: int) -> str:
    """Return the shelf status for an item.

    Raises:
        ValueError: If either count is negative.
    """
    if copies < 0 or holds < 0:
        raise ValueError("counts cannot be negative")
    if copies == 0:
        return "waitlist"
    if holds >= copies:
        return "reserved"
    return "available"


def apply_cap(fee_cents: int) -> int:
    """Clamp a late fee to the house maximum."""
    if fee_cents > FEE_CAP_CENTS:
        fee_cents = FEE_CAP_CENTS
    return fee_cents


def notify(status: str, email: str | None = None) -> str:
    """Build the notice line for a member."""
    message = f"Your item is {status}."
    if email:
        message = f"{message} We emailed {email}."
    return message
'''

TEST_HOLDS_PY = '''\
"""test_holds.py — coverage-driven tests for holds.py."""

import pytest

from holds import FEE_CAP_CENTS, apply_cap, notify, shelf_status


def test_copies_free_and_no_holds_is_available() -> None:
    assert shelf_status(3, 1) == "available"


def test_notify_without_an_email() -> None:
    assert notify("available") == "Your item is available."


def test_cap_clamps_a_big_fee() -> None:
    assert apply_cap(5_000) == FEE_CAP_CENTS


def test_zero_copies_is_waitlist() -> None:
    assert shelf_status(0, 2) == "waitlist"


def test_holds_equal_to_copies_is_reserved() -> None:
    assert shelf_status(3, 3) == "reserved"


def test_negative_copies_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        shelf_status(-1, 0)


def test_notify_with_an_email() -> None:
    assert notify("reserved", "ada@example.org") == (
        "Your item is reserved. We emailed ada@example.org."
    )


def test_cap_leaves_a_small_fee_alone() -> None:
    assert apply_cap(250) == 250
'''

# The three tests the starter shipped with, versus the two rounds you add.
STARTER_ONLY = "available or notify_without_an_email or cap_clamps_a_big_fee"
WITHOUT_ROUND_TWO = "not cap_leaves_a_small_fee_alone"


def run_coverage(folder: Path, branch: bool, select: str | None) -> list[str]:
    """Run pytest --cov in *folder* and return the parsed ``holds.py`` row."""
    cmd = [sys.executable, "-m", "pytest", "--cov=holds",
           "--cov-report=term-missing", "-p", "no:cacheprovider", "-q"]
    if branch:
        cmd.append("--cov-branch")
    if select:
        cmd += ["-k", select]
    result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    for line in result.stdout.splitlines():
        if line.startswith("holds.py"):
            return line.split()
    return ["holds.py", "(no coverage row — is pytest-cov installed?)"]


def main() -> None:
    """Write the module and tests, then narrate coverage in four runs."""
    print("Coverage measures which lines ran, nothing more. Watch the gap open twice.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "holds.py").write_text(HOLDS_PY, encoding="utf-8")
        (folder / "test_holds.py").write_text(TEST_HOLDS_PY, encoding="utf-8")

        # 1. statement coverage, the three starter tests only
        name, stmts, miss, cover, *missing = run_coverage(folder, False, STARTER_ONLY)
        print("Statement coverage, the three starter tests only:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        # 2. statement coverage, all eight tests
        name, stmts, miss, cover, *missing = run_coverage(folder, False, None)
        print("Statement coverage, all eight tests:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        # 3. branch coverage, everything except the round-two test
        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, WITHOUT_ROUND_TWO)
        print("Branch coverage, all eight tests EXCEPT the small-fee test:")
        print(f"  {stmts} statements, {branch} branches, {brpart} partial, {cover}"
              f"   missing arc {' '.join(missing) or '(none)'}")

        # 4. branch coverage, all eight tests
        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, None)
        print("Branch coverage, all eight tests:")
        print(f"  {stmts} statements, {branch} branches, {brpart} partial, {cover}"
              f"   missing arc {' '.join(missing) or '(none)'}")

    print()
    print("Even at 100% branch coverage, shelf_status never checks whether the")
    print("member already holds a copy. Coverage cannot see a rule nobody wrote down.")


if __name__ == "__main__":
    main()
