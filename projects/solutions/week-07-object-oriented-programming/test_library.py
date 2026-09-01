"""Stretch goal: a pytest suite over borrowing, overdue detection and save/load.

    python -m pytest -q
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from book import Book
from librarian import Librarian
from library import Library
from member import Loan, Member

TODAY = date(2026, 3, 1)


@pytest.fixture()
def library() -> Library:
    lib = Library(name="Test Library")
    lib.add_book(Book("Fluent Python", "Luciano Ramalho", "isbn-1", 2))
    lib.add_book(Book("Think Python", "Allen B. Downey", "isbn-2", 1))
    lib.register_member(Member(name="Ada", member_id="M-001"))
    lib.register_member(Member(name="Grace", member_id="M-002"))
    return lib


# --- Book -----------------------------------------------------------------


def test_copies_available_is_derived() -> None:
    book = Book("T", "A", "i", 3)
    assert book.copies_available == 3
    book.loan_one()
    assert book.copies_available == 2
    book.return_one()
    assert book.copies_available == 3


def test_book_rejects_bad_counts() -> None:
    with pytest.raises(ValueError, match="at least one copy"):
        Book("T", "A", "i", 0)
    with pytest.raises(ValueError, match="no copies of 'T' available"):
        Book("T", "A", "i", 1, _copies_loaned=1).loan_one()
    with pytest.raises(ValueError, match="are loaned out"):
        Book("T", "A", "i", 1).return_one()


# --- borrowing ------------------------------------------------------------


def test_borrow_moves_a_copy_and_records_a_loan(library: Library) -> None:
    loan = library.borrow("M-001", "isbn-1", days=14, today=TODAY)
    assert loan == Loan(isbn="isbn-1", due_date=date(2026, 3, 15))
    assert library.get_book("isbn-1").copies_available == 1
    assert library.get_member("M-001").loans == [loan]


def test_borrow_rejects_unknown_ids(library: Library) -> None:
    with pytest.raises(ValueError, match="unknown member id"):
        library.borrow("nope", "isbn-1", today=TODAY)
    with pytest.raises(ValueError, match="unknown isbn"):
        library.borrow("M-001", "nope", today=TODAY)


def test_borrow_rejects_when_no_copies(library: Library) -> None:
    library.borrow("M-001", "isbn-2", today=TODAY)
    with pytest.raises(ValueError, match="no copies of 'Think Python' available"):
        library.borrow("M-002", "isbn-2", today=TODAY)


def test_double_borrow_rolls_the_book_back(library: Library) -> None:
    library.borrow("M-001", "isbn-1", today=TODAY)
    with pytest.raises(ValueError, match="already has"):
        library.borrow("M-001", "isbn-1", today=TODAY)
    # The rollback is the point: one loan out, not two.
    assert library.get_book("isbn-1").copies_loaned == 1


def test_return_restores_the_copy(library: Library) -> None:
    library.borrow("M-001", "isbn-1", today=TODAY)
    library.return_book("M-001", "isbn-1")
    assert library.get_book("isbn-1").copies_available == 2
    assert library.get_member("M-001").loans == []
    with pytest.raises(ValueError, match="has no loan for isbn"):
        library.return_book("M-001", "isbn-1")


# --- overdue --------------------------------------------------------------


def test_overdue_is_strictly_before_today(library: Library) -> None:
    library.borrow("M-001", "isbn-1", days=7, today=TODAY)
    due = TODAY + timedelta(days=7)
    assert library.overdue_loans(due) == []          # due today is not overdue
    rows = library.overdue_loans(due + timedelta(days=1))
    assert [m.member_id for m, _ in rows] == ["M-001"]


def test_fines_accrue_at_a_quarter_a_day(library: Library) -> None:
    library.borrow("M-001", "isbn-1", days=1, today=TODAY)
    when = TODAY + timedelta(days=5)   # due 2026-03-02, so 4 days late
    assert library.fines(when) == {"M-001": 1.0}


# --- persistence ----------------------------------------------------------


def test_save_load_round_trip(tmp_path, library: Library) -> None:
    library.register_member(Librarian(name="Kay", member_id="S-1"))
    library.borrow("M-001", "isbn-1", days=14, today=TODAY)
    path = tmp_path / "library.json"
    library.save(path)

    reloaded = Library.load(path)
    assert reloaded.to_dict() == library.to_dict()
    assert reloaded.get_book("isbn-1").copies_loaned == 1
    assert reloaded.get_member("M-001").loans[0].due_date == date(2026, 3, 15)
    assert isinstance(reloaded.get_member("S-1"), Librarian)


def test_load_rejects_inconsistent_state(tmp_path) -> None:
    payload = {
        "schema_version": 1,
        "name": "Broken",
        "books": [
            {"title": "T", "author": "A", "isbn": "i", "copies_total": 1,
             "copies_loaned": 0}
        ],
        "members": [
            {"name": "Ada", "member_id": "M-1", "role": "Member",
             "loans": [{"isbn": "i", "due_date": "2026-01-01"}]}
        ],
    }
    path = tmp_path / "broken.json"
    path.write_text(__import__("json").dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="member loan\\(s\\) found"):
        Library.load(path)


# --- protocols ------------------------------------------------------------


def test_library_is_iterable_and_sized(library: Library) -> None:
    assert len(library) == 2
    assert sorted(b.isbn for b in library) == ["isbn-1", "isbn-2"]
    assert "isbn-1" in library


def test_search_matches_title_or_author(library: Library) -> None:
    assert [b.isbn for b in library.search("python")] == ["isbn-1", "isbn-2"]
    assert [b.isbn for b in library.search("DOWNEY")] == ["isbn-2"]
    assert library.search("   ") == []
