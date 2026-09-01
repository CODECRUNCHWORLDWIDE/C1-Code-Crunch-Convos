"""Plain dataclasses. No SQL, no behaviour, no database connection.

In Week 7 these classes *were* the system: they held the data and the rules.
Here the database holds the data and enforces the rules (NOT NULL, UNIQUE,
CHECK, foreign keys), so these shrink to what they always should have been --
a typed shape for a row once it has been read.

`from_row` is the only conversion in the project. Keeping it here, instead of
sprinkling `row["title"]` through the CLI, means a column rename touches two
places: the SQL in repository.py and the mapping here.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    id: int
    title: str
    author: str
    isbn: str | None
    total_copies: int

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> Book:
        return cls(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            total_copies=row["total_copies"],
        )


@dataclass(frozen=True, slots=True)
class Member:
    id: int
    name: str
    email: str
    joined_on: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> Member:
        return cls(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            joined_on=row["joined_on"],
        )


@dataclass(frozen=True, slots=True)
class Loan:
    id: int
    book_id: int
    member_id: int
    borrowed_on: str
    due_on: str
    returned_on: str | None

    @property
    def is_active(self) -> bool:
        """A loan is active until it is returned. This is the whole rule."""
        return self.returned_on is None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> Loan:
        return cls(
            id=row["id"],
            book_id=row["book_id"],
            member_id=row["member_id"],
            borrowed_on=row["borrowed_on"],
            due_on=row["due_on"],
            returned_on=row["returned_on"],
        )


@dataclass(frozen=True, slots=True)
class MemberLoans:
    """One member plus the titles they currently have out (possibly none)."""

    member_id: int
    name: str
    email: str
    titles: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PopularBook:
    """A row of the "most borrowed this month" report."""

    book_id: int
    title: str
    author: str
    times_borrowed: int


@dataclass(frozen=True, slots=True)
class OverdueLoan:
    """An active loan whose due_on is in the past, plus the fee it has earned."""

    loan_id: int
    title: str
    member_name: str
    due_on: str
    days_overdue: int
    fee: float


class LibraryError(RuntimeError):
    """Base class for the errors this library raises at its own callers."""


class NotFound(LibraryError):
    """A referenced book, member or loan does not exist."""


class NoCopiesAvailable(LibraryError):
    """Every copy of the requested book is already out on loan."""
