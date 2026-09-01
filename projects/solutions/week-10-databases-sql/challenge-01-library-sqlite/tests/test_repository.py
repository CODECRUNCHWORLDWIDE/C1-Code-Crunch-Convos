#!/usr/bin/env python3
"""Tests for the repository layer. Run from the project root:

    python tests/test_repository.py

The challenge only asks for three meaningful tests; there are nine here,
because each of the six required features deserves one and the interesting
failures (no copies left, double return, foreign key rejected) deserve one
each too. Week 11 turns these into pytest; today it is `assert` and a runner.

Each test gets its own database file in a temporary directory, so nothing
leaks between tests and nothing touches your real library.db.
"""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from library import repository as repo          # noqa: E402
from library.db import init_db                  # noqa: E402
from library.models import (                    # noqa: E402
    LibraryError,
    NoCopiesAvailable,
    NotFound,
)


class Fixture:
    """A throwaway database with two books and two members already in it."""

    def __init__(self, tmpdir: str) -> None:
        self.path = str(Path(tmpdir) / "test.db")
        init_db(self.path)
        self.dune = repo.add_book("Dune", "Frank Herbert", "978-0441013593", 2, self.path)
        self.gita = repo.add_book("Kindred", "Octavia Butler", "978-0807083697", 1, self.path)
        self.ada = repo.register_member("Ada Lovelace", "ada@example.com",
                                        "2026-01-05", self.path)
        self.alan = repo.register_member("Alan Turing", "alan@example.com",
                                         "2026-01-06", self.path)


def with_fixture(body: Callable[[Fixture], None]) -> Callable[[], None]:
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            body(Fixture(tmpdir))
    run.__name__ = body.__name__
    return run


# ---------------------------------------------------------------------------


@with_fixture
def test_add_book_and_member(fx: Fixture) -> None:
    book = repo.get_book(fx.dune, fx.path)
    assert book.title == "Dune"
    assert book.total_copies == 2
    member = repo.get_member(fx.ada, fx.path)
    assert member.email == "ada@example.com"
    assert member.joined_on == "2026-01-05"


@with_fixture
def test_duplicate_isbn_is_refused(fx: Fixture) -> None:
    try:
        repo.add_book("Dune (reprint)", "Frank Herbert", "978-0441013593", 3, fx.path)
    except LibraryError as exc:
        assert "UNIQUE constraint failed: books.isbn" in str(exc), str(exc)
    else:
        raise AssertionError("the UNIQUE constraint on isbn did not fire")


@with_fixture
def test_borrow_reduces_availability(fx: Fixture) -> None:
    assert repo.available_copies(fx.dune, fx.path) == 2
    repo.borrow_book(fx.dune, fx.ada, "2026-02-01", "2026-01-18", fx.path)
    assert repo.available_copies(fx.dune, fx.path) == 1


@with_fixture
def test_borrow_refuses_when_no_copies_left(fx: Fixture) -> None:
    repo.borrow_book(fx.gita, fx.ada, "2026-02-01", "2026-01-18", fx.path)
    assert repo.available_copies(fx.gita, fx.path) == 0
    try:
        repo.borrow_book(fx.gita, fx.alan, "2026-02-01", "2026-01-18", fx.path)
    except NoCopiesAvailable:
        pass
    else:
        raise AssertionError("borrowing the last copy twice should fail")


@with_fixture
def test_foreign_key_is_enforced(fx: Fixture) -> None:
    """PRAGMA foreign_keys = ON is doing real work, not decoration."""
    try:
        repo.borrow_book(fx.dune, 999, "2026-02-01", "2026-01-18", fx.path)
    except NotFound as exc:
        assert "999" in str(exc)
    else:
        raise AssertionError("a loan for a non-existent member was accepted")


@with_fixture
def test_return_frees_the_copy_and_refuses_twice(fx: Fixture) -> None:
    loan_id = repo.borrow_book(fx.gita, fx.ada, "2026-02-01", "2026-01-18", fx.path)
    loan = repo.return_book(loan_id, "2026-01-25", fx.path)
    assert loan.returned_on == "2026-01-25"
    assert repo.available_copies(fx.gita, fx.path) == 1
    try:
        repo.return_book(loan_id, "2026-01-26", fx.path)
    except LibraryError as exc:
        assert "already returned" in str(exc)
    else:
        raise AssertionError("a loan was returned twice")


@with_fixture
def test_members_with_loans_keeps_members_who_have_nothing_out(fx: Fixture) -> None:
    repo.borrow_book(fx.dune, fx.ada, "2026-02-01", "2026-01-18", fx.path)
    rows = {entry.name: entry.titles for entry in repo.members_with_loans(fx.path)}
    assert rows == {"Ada Lovelace": ("Dune",), "Alan Turing": ()}, rows


@with_fixture
def test_returned_loans_do_not_show_as_current(fx: Fixture) -> None:
    loan_id = repo.borrow_book(fx.dune, fx.alan, "2026-02-01", "2026-01-18", fx.path)
    repo.return_book(loan_id, "2026-01-20", fx.path)
    rows = {entry.name: entry.titles for entry in repo.members_with_loans(fx.path)}
    assert rows["Alan Turing"] == (), rows


@with_fixture
def test_most_popular_this_month(fx: Fixture) -> None:
    # Three January borrows of Dune, one of Kindred, one February borrow.
    for member, day in ((fx.ada, "2026-01-10"), (fx.alan, "2026-01-11")):
        loan = repo.borrow_book(fx.dune, member, "2026-02-01", day, fx.path)
        repo.return_book(loan, "2026-01-15", fx.path)
    loan = repo.borrow_book(fx.dune, fx.ada, "2026-02-01", "2026-01-20", fx.path)
    repo.return_book(loan, "2026-01-22", fx.path)
    repo.borrow_book(fx.gita, fx.alan, "2026-02-20", "2026-01-25", fx.path)
    repo.borrow_book(fx.dune, fx.alan, "2026-03-01", "2026-02-02", fx.path)

    january = repo.most_popular_this_month("2026-01", 5, fx.path)
    assert [(row.title, row.times_borrowed) for row in january] == [
        ("Dune", 3),
        ("Kindred", 1),
    ], january
    february = repo.most_popular_this_month("2026-02", 5, fx.path)
    assert [(row.title, row.times_borrowed) for row in february] == [("Dune", 1)], february


@with_fixture
def test_overdue_fees(fx: Fixture) -> None:
    repo.borrow_book(fx.gita, fx.ada, "2026-01-20", "2026-01-06", fx.path)
    rows = repo.overdue_loans("2026-01-30", 0.25, fx.path)
    assert len(rows) == 1, rows
    assert rows[0].days_overdue == 10, rows[0]
    assert rows[0].fee == 2.50, rows[0]
    # Nothing is overdue before the due date.
    assert repo.overdue_loans("2026-01-19", 0.25, fx.path) == []


@with_fixture
def test_reservation_is_fulfilled_on_return(fx: Fixture) -> None:
    loan_id = repo.borrow_book(fx.gita, fx.ada, "2026-02-01", "2026-01-18", fx.path)
    assert repo.available_copies(fx.gita, fx.path) == 0
    repo.place_reservation(fx.gita, fx.alan, "2026-01-19", fx.path)

    closed, new_loan_id = repo.return_book_and_fulfil(loan_id, "2026-01-25", fx.path)
    assert closed.returned_on == "2026-01-25"
    assert new_loan_id is not None, "the queued member should have got the copy"
    new_loan = repo.get_loan(new_loan_id, fx.path)
    assert new_loan.member_id == fx.alan
    assert new_loan.borrowed_on == "2026-01-25"
    assert new_loan.due_on == "2026-02-08"      # 14 days later
    # The copy went straight back out, so it is not available.
    assert repo.available_copies(fx.gita, fx.path) == 0


@with_fixture
def test_injection_payload_is_stored_as_a_title(fx: Fixture) -> None:
    payload = "Dune'); DROP TABLE books; --"
    book_id = repo.add_book(payload, "Nobody", None, 1, fx.path)
    assert repo.get_book(book_id, fx.path).title == payload
    # books still exists, with all three rows.
    assert repo.available_copies(fx.dune, fx.path) == 2


TESTS: Final[list[Callable[[], None]]] = [
    test_add_book_and_member,
    test_duplicate_isbn_is_refused,
    test_borrow_reduces_availability,
    test_borrow_refuses_when_no_copies_left,
    test_foreign_key_is_enforced,
    test_return_frees_the_copy_and_refuses_twice,
    test_members_with_loans_keeps_members_who_have_nothing_out,
    test_returned_loans_do_not_show_as_current,
    test_most_popular_this_month,
    test_overdue_fees,
    test_reservation_is_fulfilled_on_return,
    test_injection_payload_is_stored_as_a_title,
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
