"""problem-05-fine-schedule-solution.py — coverage, statement and branch, headless.

``fines.py`` clamps an overdue fine to a house cap. A test file covers every
*statement* and still leaves one *branch* untaken — the clamp has only ever been
asked to fire, never to leave a small fine alone. This script writes the module
and tests to a scratch folder and shells out to ``pytest --cov`` three times to
show the gap, printing only the stable numbers it parses back.

Run it with::

    python problem-05-fine-schedule-solution.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

FINES_PY = '''\
"""fines.py — the overdue fine schedule."""

CAP_CENTS: int = 2_000


def fine_cents(days_late: int, is_student: bool = False) -> int:
    """Return the overdue fine in whole cents, clamped to the house cap."""
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    rate = 10 if is_student else 25
    fine = days_late * rate
    if fine > CAP_CENTS:
        fine = CAP_CENTS
    return fine
'''

TEST_FINES_PY = '''\
"""test_fines.py — coverage-driven tests for fines.py."""

import pytest

from fines import CAP_CENTS, fine_cents


def test_over_cap_standard() -> None:
    assert fine_cents(1_000) == CAP_CENTS


def test_over_cap_student() -> None:
    assert fine_cents(1_000, is_student=True) == CAP_CENTS


def test_negative_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        fine_cents(-1)


def test_normal_day_standard() -> None:
    assert fine_cents(2) == 50


def test_zero_is_free() -> None:
    assert fine_cents(0) == 0
'''

# The two tests the starter shipped with, versus the rounds you add.
STARTER_ONLY = "over_cap"
ROUND_ONE = "over_cap or negative_rejected"


def run_coverage(folder: Path, branch: bool, select: str | None) -> list[str]:
    """Run pytest --cov in *folder* and return the parsed ``fines.py`` row."""
    cmd = [sys.executable, "-m", "pytest", "--cov=fines",
           "--cov-report=term-missing", "-p", "no:cacheprovider", "-q"]
    if branch:
        cmd.append("--cov-branch")
    if select:
        cmd += ["-k", select]
    result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    for line in result.stdout.splitlines():
        if line.startswith("fines.py"):
            return line.split()
    return ["fines.py", "(no coverage row — is pytest-cov installed?)"]


def main() -> None:
    """Write the module and tests, then narrate coverage in three runs."""
    print("Statement coverage can be 100% while a branch is never taken.")
    print()
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "fines.py").write_text(FINES_PY, encoding="utf-8")
        (folder / "test_fines.py").write_text(TEST_FINES_PY, encoding="utf-8")

        name, stmts, miss, cover, *missing = run_coverage(folder, False, STARTER_ONLY)
        print("Statement coverage, the two starter tests only:")
        print(f"  {stmts} statements, {miss} missed, {cover}   missing lines "
              f"{' '.join(missing) or '(none)'}")

        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, ROUND_ONE)
        print("Branch coverage, after adding the negative-days test:")
        print(f"  {stmts} statements, {miss} missed, {branch} branches, "
              f"{brpart} partial, {cover}   missing arc {' '.join(missing) or '(none)'}")

        name, stmts, miss, branch, brpart, cover, *missing = run_coverage(
            folder, True, None)
        print("Branch coverage, all five tests:")
        print(f"  {stmts} statements, {miss} missed, {branch} branches, "
              f"{brpart} partial, {cover}   missing arc {' '.join(missing) or '(none)'}")

    print()
    print("The middle run reached 100% statements while the clamp's 'leave a small")
    print("fine alone' branch stayed untested. The last run's under-cap test closes it.")


if __name__ == "__main__":
    main()
