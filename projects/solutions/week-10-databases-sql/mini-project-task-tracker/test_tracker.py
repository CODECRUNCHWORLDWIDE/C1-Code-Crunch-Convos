#!/usr/bin/env python3
"""test_tracker.py -- the mini-project's "tiny test suite" stretch goal.

No pytest yet (that is Week 11). This is plain `assert` plus a tiny runner, so
it works on a bare Python install:

    python test_tracker.py

Every test runs against an **in-memory** database. There is a wrinkle worth
understanding: tracker.py opens a fresh connection per operation, and a plain
`sqlite3.connect(":memory:")` creates a brand-new empty database for every
connection -- so the row you insert in add_task() would not exist by the time
list_tasks() connects. The fix is SQLite's shared-cache URI:

    file:tracker-test?mode=memory&cache=shared

Every connection that opens that URI reaches the *same* in-memory database.
The database lives as long as at least one connection to it is open, which is
why each test holds a `keepalive` connection open for its whole body.
"""

from __future__ import annotations

import sqlite3
import sys
from collections.abc import Callable
from contextlib import closing
from typing import Final

import tracker

MEMORY_URI: Final[str] = "file:tracker-test?mode=memory&cache=shared"


def fresh_db() -> sqlite3.Connection:
    """Open (and keep open) a clean shared in-memory database."""
    keepalive = tracker.connect(MEMORY_URI)
    keepalive.executescript("DROP TABLE IF EXISTS tasks;")
    keepalive.commit()
    tracker.init_db(MEMORY_URI)
    return keepalive


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------


def test_add_defaults_to_priority_3() -> None:
    with closing(fresh_db()):
        task_id = tracker.add_task("Pet the cat", None, 3, MEMORY_URI)
        rows = tracker.list_tasks(db_path=MEMORY_URI)
        assert task_id == 1, f"first task should get id 1, got {task_id}"
        assert len(rows) == 1
        assert rows[0]["priority"] == 3
        assert rows[0]["due_date"] is None
        assert rows[0]["done"] == 0


def test_filters_compose() -> None:
    with closing(fresh_db()):
        tracker.add_task("Finish quiz", "2026-05-15", 2, MEMORY_URI)
        tracker.add_task("Pet the cat", None, 5, MEMORY_URI)
        third = tracker.add_task("Review SQL notes", "2026-05-12", 2, MEMORY_URI)
        tracker.mark_done(third, MEMORY_URI)

        assert len(tracker.list_tasks(db_path=MEMORY_URI)) == 3
        assert len(tracker.list_tasks(priority=2, db_path=MEMORY_URI)) == 2
        assert len(tracker.list_tasks(status="open", db_path=MEMORY_URI)) == 2
        assert len(tracker.list_tasks(status="done", db_path=MEMORY_URI)) == 1
        # priority AND status together -- the composition that the rubric tests
        both = tracker.list_tasks(priority=2, status="open", db_path=MEMORY_URI)
        assert [r["title"] for r in both] == ["Finish quiz"], [r["title"] for r in both]


def test_done_and_delete_touch_exactly_one_row() -> None:
    with closing(fresh_db()):
        first = tracker.add_task("one", None, 3, MEMORY_URI)
        second = tracker.add_task("two", None, 3, MEMORY_URI)

        tracker.mark_done(first, MEMORY_URI)
        rows = {r["id"]: r["done"] for r in tracker.list_tasks(db_path=MEMORY_URI)}
        assert rows == {first: 1, second: 0}, rows

        tracker.delete_task(second, MEMORY_URI)
        remaining = [r["id"] for r in tracker.list_tasks(db_path=MEMORY_URI)]
        assert remaining == [first], remaining


def test_unknown_id_raises() -> None:
    with closing(fresh_db()):
        for operation in (tracker.mark_done, tracker.delete_task):
            try:
                operation(999, MEMORY_URI)
            except LookupError as exc:
                assert "999" in str(exc)
            else:
                raise AssertionError(f"{operation.__name__} accepted a missing id")


def test_check_constraint_rejects_bad_priority() -> None:
    """Validation lives in argparse, but the database is the second line."""
    with closing(fresh_db()):
        try:
            tracker.add_task("bad", None, 9, MEMORY_URI)
        except sqlite3.IntegrityError as exc:
            assert "CHECK constraint failed" in str(exc), str(exc)
        else:
            raise AssertionError("the CHECK constraint did not fire")


def test_injection_attempt_is_stored_as_plain_text() -> None:
    """The whole point of parameterization, as an executable assertion."""
    payload = "'); DROP TABLE tasks; --"
    with closing(fresh_db()):
        tracker.add_task(payload, None, 3, MEMORY_URI)
        rows = tracker.list_tasks(db_path=MEMORY_URI)
        assert len(rows) == 1
        assert rows[0]["title"] == payload, rows[0]["title"]


def test_table_matches_the_spec_sample() -> None:
    with closing(fresh_db()):
        tracker.add_task("Finish quiz", "2026-05-15", 2, MEMORY_URI)
        tracker.add_task("Pet the cat", None, 5, MEMORY_URI)
        third = tracker.add_task("Review SQL injection notes", "2026-05-12", 1, MEMORY_URI)
        tracker.mark_done(third, MEMORY_URI)
        expected = (
            "ID  Pri  Status  Due         Title\n"
            "--  ---  ------  ----------  -------------------------------\n"
            " 1    2  open    2026-05-15  Finish quiz\n"
            " 2    5  open    -           Pet the cat\n"
            " 3    1  done    2026-05-12  Review SQL injection notes"
        )
        actual = tracker.format_table(tracker.list_tasks(db_path=MEMORY_URI))
        assert actual == expected, f"\n--- expected ---\n{expected}\n--- actual ---\n{actual}"


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

TESTS: Final[list[Callable[[], None]]] = [
    test_add_defaults_to_priority_3,
    test_filters_compose,
    test_done_and_delete_touch_exactly_one_row,
    test_unknown_id_raises,
    test_check_constraint_rejects_bad_priority,
    test_injection_attempt_is_stored_as_plain_text,
    test_table_matches_the_spec_sample,
]


def main() -> int:
    failures = 0
    for test in TESTS:
        try:
            test()
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {test.__name__}\n      {exc}")
        else:
            print(f"ok    {test.__name__}")
    print(f"\n{len(TESTS) - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
