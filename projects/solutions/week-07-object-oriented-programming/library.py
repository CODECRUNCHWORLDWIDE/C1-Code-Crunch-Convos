"""`Library`: the one object that owns the books, the members, and the rules."""

from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from book import Book
from librarian import Librarian
from member import Loan, Member

# Which class to rebuild for each "role" written by `Member.to_dict`.
MEMBER_CLASSES: dict[str, type[Member]] = {
    "Member": Member,
    "Librarian": Librarian,
}

FINE_PER_DAY = 0.25


class Library:
    """Hand-written (not a dataclass) because it owns two dictionaries and the
    invariants that tie them together.

    Every relationship here is composition: a Library *has* books and members;
    a Member *has* loans. Nothing inherits from anything except the one stretch
    goal, `Librarian`.
    """

    SCHEMA_VERSION = 1

    def __init__(self, name: str = "Crunch Community Library") -> None:
        self.name = name
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}

    # --- catalogue --------------------------------------------------------

    def add_book(self, book: Book) -> None:
        """Add a new catalogue entry, or fold extra copies into an existing one."""
        existing = self.books.get(book.isbn)
        if existing is None:
            self.books[book.isbn] = book
            return
        if existing.title != book.title or existing.author != book.author:
            raise ValueError(
                f"isbn {book.isbn} is already registered to "
                f"{existing.title!r} by {existing.author}"
            )
        existing.copies_total += book.copies_total

    def register_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise ValueError(f"member id {member.member_id!r} is already registered")
        self.members[member.member_id] = member

    # --- lookups ----------------------------------------------------------

    def get_book(self, isbn: str) -> Book:
        try:
            return self.books[isbn]
        except KeyError:
            raise ValueError(f"unknown isbn {isbn!r}") from None

    def get_member(self, member_id: str) -> Member:
        try:
            return self.members[member_id]
        except KeyError:
            raise ValueError(f"unknown member id {member_id!r}") from None

    # --- circulation ------------------------------------------------------

    def borrow(
        self,
        member_id: str,
        isbn: str,
        days: int = 14,
        *,
        today: date | None = None,
    ) -> Loan:
        """Lend one copy of `isbn` to `member_id` for `days` days.

        `today` is keyword-only and exists purely so tests can pin the clock.
        """
        if days < 1:
            raise ValueError(f"loan length must be at least 1 day, got {days!r}")

        member = self.get_member(member_id)
        book = self.get_book(isbn)

        loan = Loan(isbn=isbn, due_date=(today or date.today()) + timedelta(days=days))

        book.loan_one()          # may raise: no copies available
        try:
            member.add_loan(loan)  # may raise: member already holds this isbn
        except ValueError:
            book.return_one()      # roll back so the counts never drift
            raise
        return loan

    def return_book(self, member_id: str, isbn: str) -> None:
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        member.remove_loan(isbn)   # raises if this member does not hold it
        book.return_one()

    def overdue_loans(self, today: date | None = None) -> list[tuple[Member, Loan]]:
        """Every (member, loan) pair whose due date is before `today`."""
        when = today or date.today()
        return [
            (member, loan)
            for member in self.members.values()
            for loan in member.loans
            if loan.is_overdue(when)
        ]

    # --- stretch goals ----------------------------------------------------

    def search(self, query: str) -> list[Book]:
        """Case-insensitive partial match on title or author."""
        needle = query.strip().lower()
        if not needle:
            return []
        return [
            book
            for book in self.books.values()
            if needle in book.title.lower() or needle in book.author.lower()
        ]

    def fines(self, today: date | None = None) -> dict[str, float]:
        """`{member_id: amount owed}` at $0.25 per overdue day. Only debtors."""
        owed: dict[str, float] = {}
        for member, loan in self.overdue_loans(today):
            amount = loan.days_overdue(today) * FINE_PER_DAY
            owed[member.member_id] = round(owed.get(member.member_id, 0.0) + amount, 2)
        return owed

    # --- persistence ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.SCHEMA_VERSION,
            "name": self.name,
            "books": [book.to_dict() for book in self.books.values()],
            "members": [member.to_dict() for member in self.members.values()],
        }

    def save(self, path: str | Path) -> None:
        """Write the whole library to JSON, creating parent folders as needed."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Library":
        version = data.get("schema_version", 1)
        if version != cls.SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {version!r}; "
                f"this build reads version {cls.SCHEMA_VERSION}"
            )
        library = cls(name=data.get("name", "Crunch Community Library"))
        for raw_book in data.get("books", []):
            library.books[raw_book["isbn"]] = Book.from_dict(raw_book)
        for raw_member in data.get("members", []):
            member_cls = MEMBER_CLASSES.get(raw_member.get("role", "Member"), Member)
            member = member_cls.from_dict(raw_member)
            library.members[member.member_id] = member
        library.check_invariants()
        return library

    @classmethod
    def load(cls, path: str | Path) -> "Library":
        source = Path(path)
        with source.open("r", encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    def check_invariants(self) -> None:
        """Every loan must point at a known book, and the loaned counts must add up."""
        counted: dict[str, int] = {}
        for member in self.members.values():
            for loan in member.loans:
                if loan.isbn not in self.books:
                    raise ValueError(
                        f"member {member.member_id!r} holds unknown isbn {loan.isbn!r}"
                    )
                counted[loan.isbn] = counted.get(loan.isbn, 0) + 1
        for isbn, book in self.books.items():
            actual = counted.get(isbn, 0)
            if actual != book.copies_loaned:
                raise ValueError(
                    f"isbn {isbn}: {book.copies_loaned} copies recorded as loaned "
                    f"but {actual} member loan(s) found"
                )

    # --- protocol niceties ------------------------------------------------

    def __len__(self) -> int:
        """Number of distinct catalogue entries."""
        return len(self.books)

    def __iter__(self) -> Iterator[Book]:
        """Stretch goal: `for book in library:` works."""
        return iter(self.books.values())

    def __contains__(self, isbn: object) -> bool:
        return isbn in self.books

    def __repr__(self) -> str:
        return (
            f"Library(name={self.name!r}, books={len(self.books)}, "
            f"members={len(self.members)})"
        )
