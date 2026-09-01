"""`Loan` and `Member`: who is holding what, and until when."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class Loan:
    """One book, out to one member, due on one day.

    Frozen because a loan is a *value*: once issued, its ISBN and due date do
    not change. You return it and drop it, or you renew it by creating a new
    one. Frozen also gets us `__hash__` for free, so loans can live in sets.
    """

    isbn: str
    due_date: date

    def __post_init__(self) -> None:
        if not self.isbn.strip():
            raise ValueError("a loan needs a non-empty isbn")
        if not isinstance(self.due_date, date):
            raise ValueError(
                f"due_date must be a datetime.date, got {type(self.due_date).__name__}"
            )

    def is_overdue(self, today: date | None = None) -> bool:
        """True when the due date is strictly in the past."""
        return self.due_date < (today or date.today())

    def days_overdue(self, today: date | None = None) -> int:
        """How many whole days late, or 0 if not late."""
        delta = (today or date.today()) - self.due_date
        return max(delta.days, 0)

    def to_dict(self) -> dict[str, Any]:
        return {"isbn": self.isbn, "due_date": self.due_date.isoformat()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Loan":
        return cls(isbn=data["isbn"], due_date=date.fromisoformat(data["due_date"]))

    def __str__(self) -> str:
        return f"{self.isbn} due {self.due_date.isoformat()}"


@dataclass
class Member:
    """Somebody with a library card and, possibly, some books."""

    name: str
    member_id: str
    loans: list[Loan] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("a member needs a non-empty name")
        if not self.member_id.strip():
            raise ValueError(f"{self.name!r}: member_id must not be empty")

    # --- loan bookkeeping -------------------------------------------------

    def has_loan(self, isbn: str) -> bool:
        return any(loan.isbn == isbn for loan in self.loans)

    def add_loan(self, loan: Loan) -> None:
        """Record a new loan. One copy of a given ISBN per member at a time."""
        if self.has_loan(loan.isbn):
            raise ValueError(
                f"{self.name!r} already has {loan.isbn} on loan"
            )
        self.loans.append(loan)

    def remove_loan(self, isbn: str) -> Loan:
        """Drop the loan for `isbn` and return it."""
        for index, loan in enumerate(self.loans):
            if loan.isbn == isbn:
                return self.loans.pop(index)
        raise ValueError(f"{self.name!r} has no loan for isbn {isbn!r}")

    def overdue(self, today: date | None = None) -> list[Loan]:
        return [loan for loan in self.loans if loan.is_overdue(today)]

    # --- serialization ----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "member_id": self.member_id,
            "role": type(self).__name__,
            "loans": [loan.to_dict() for loan in self.loans],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Member":
        return cls(
            name=data["name"],
            member_id=data["member_id"],
            loans=[Loan.from_dict(item) for item in data.get("loans", [])],
        )

    # --- protocol niceties ------------------------------------------------

    def __len__(self) -> int:
        return len(self.loans)

    def __iter__(self) -> Iterator[Loan]:
        return iter(self.loans)

    def __str__(self) -> str:
        if not self.loans:
            return f"{self.name} ({self.member_id}) — no books out"
        return f"{self.name} ({self.member_id}) — {len(self.loans)} book(s) out"
