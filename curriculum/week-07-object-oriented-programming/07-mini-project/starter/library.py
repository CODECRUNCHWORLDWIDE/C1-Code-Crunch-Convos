"""library.py — Library class for the mini-project.

The Library *composes* books and members; it does not inherit from
anything. Most operations are validated wrappers around methods on
the contained objects.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from book import Book
from member import Loan, Member


class Library:
    """Top-level container that owns books and members."""

    def __init__(self, name: str = "Code Crunch Library") -> None:
        self.name = name
        # Composition: a Library *has* dictionaries of books and members.
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}

    # ------------------------------------------------------------------
    # Registration / catalog operations.
    # ------------------------------------------------------------------
    def add_book(self, book: Book) -> None:
        """Add a new book to the catalog. ISBN must be unique."""
        if book.isbn in self.books:
            raise ValueError(f"a book with ISBN {book.isbn!r} already exists")
        self.books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        """Register a new member. member_id must be unique."""
        if member.member_id in self.members:
            raise ValueError(f"member_id {member.member_id!r} is already registered")
        self.members[member.member_id] = member

    # ------------------------------------------------------------------
    # Borrow / return.
    # ------------------------------------------------------------------
    def borrow(self, member_id: str, isbn: str, days: int = 14) -> Loan:
        """Borrow a copy of ``isbn`` for ``member_id`` for ``days`` days.

        Raises
        ------
        ValueError
            If the member or book is unknown, no copy is available, or the
            member already has a copy of this title on loan.
        """
        member = self._require_member(member_id)
        book = self._require_book(isbn)

        if member.has_loan_for(isbn):
            raise ValueError(
                f"{member.name} already has a copy of {book.title!r} on loan"
            )

        # Reduce inventory first; only build the loan once the book
        # operation has succeeded.
        book.loan_one()
        loan = Loan(isbn=isbn, due_date=date.today() + timedelta(days=days))
        member.add_loan(loan)
        return loan

    def return_book(self, member_id: str, isbn: str) -> None:
        """Return a borrowed book."""
        member = self._require_member(member_id)
        book = self._require_book(isbn)
        member.remove_loan(isbn)        # raises if member has no such loan
        book.return_one()

    # ------------------------------------------------------------------
    # Reporting.
    # ------------------------------------------------------------------
    def overdue_loans(self, today: date | None = None) -> list[tuple[Member, Loan]]:
        """Return every (member, loan) pair where due_date < today."""
        today = today or date.today()
        result: list[tuple[Member, Loan]] = []
        for member in self.members.values():
            for loan in member.loans:
                if loan.is_overdue(today):
                    result.append((member, loan))
        return result

    # ------------------------------------------------------------------
    # JSON persistence.
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()],
        }

    def save(self, path: str | Path) -> None:
        """Write the whole library state to a JSON file."""
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "Library":
        """Read a library back from a JSON file produced by :meth:`save`."""
        data = json.loads(Path(path).read_text())
        lib = cls(name=data.get("name", "Code Crunch Library"))
        for book_data in data.get("books", []):
            lib.books[book_data["isbn"]] = Book.from_dict(book_data)
        for member_data in data.get("members", []):
            m = Member.from_dict(member_data)
            lib.members[m.member_id] = m
        return lib

    # ------------------------------------------------------------------
    # Internal helpers — `_` prefix flags them as protected.
    # ------------------------------------------------------------------
    def _require_book(self, isbn: str) -> Book:
        if isbn not in self.books:
            raise ValueError(f"no book with ISBN {isbn!r} in the catalog")
        return self.books[isbn]

    def _require_member(self, member_id: str) -> Member:
        if member_id not in self.members:
            raise ValueError(f"no member with id {member_id!r} is registered")
        return self.members[member_id]

    # ------------------------------------------------------------------
    # Display.
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        # Library "size" = number of distinct titles.
        return len(self.books)

    def __repr__(self) -> str:
        return (
            f"Library(name={self.name!r}, "
            f"books={len(self.books)}, members={len(self.members)})"
        )


if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book(title="Fluent Python", author="L. Ramalho", isbn="A", copies_total=2))
    lib.add_book(Book(title="The Pragmatic Programmer", author="Hunt & Thomas", isbn="B"))
    lib.register_member(Member(name="Ada", member_id="M001"))
    lib.borrow("M001", "A")
    print(lib)
    print(lib.books["A"])
    lib.save("library-demo.json")
    again = Library.load("library-demo.json")
    print(again)
    print(again.books["A"])
