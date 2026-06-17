"""member.py — Member and Loan classes for the Library mini-project.

A ``Loan`` records that a specific member has a specific book on loan
until a specific date. A ``Member`` owns a list of active loans.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Loan:
    """A single active loan. Frozen because, once created, only the
    library should add or remove loans — never mutate them in place.
    """

    isbn: str
    due_date: date

    def is_overdue(self, today: date | None = None) -> bool:
        today = today or date.today()
        return self.due_date < today

    def to_dict(self) -> dict:
        return {"isbn": self.isbn, "due_date": self.due_date.isoformat()}

    @classmethod
    def from_dict(cls, data: dict) -> "Loan":
        return cls(isbn=data["isbn"], due_date=date.fromisoformat(data["due_date"]))


@dataclass
class Member:
    """A library member."""

    name: str
    member_id: str
    loans: list[Loan] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("member name cannot be empty")
        if not self.member_id.strip():
            raise ValueError("member_id cannot be empty")

    # ------------------------------------------------------------------
    # Loan bookkeeping — Library calls these; users should not.
    # ------------------------------------------------------------------
    def add_loan(self, loan: Loan) -> None:
        # TODO: append the loan to self.loans.
        self.loans.append(loan)

    def remove_loan(self, isbn: str) -> Loan:
        """Remove and return the (first) loan whose isbn matches.

        Raises
        ------
        ValueError
            If this member has no active loan for ``isbn``.
        """
        for i, loan in enumerate(self.loans):
            if loan.isbn == isbn:
                return self.loans.pop(i)
        raise ValueError(f"{self.name} has no active loan for ISBN {isbn!r}")

    def has_loan_for(self, isbn: str) -> bool:
        return any(loan.isbn == isbn for loan in self.loans)

    # ------------------------------------------------------------------
    # JSON round-trip.
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "member_id": self.member_id,
            "loans": [loan.to_dict() for loan in self.loans],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        return cls(
            name=data["name"],
            member_id=data["member_id"],
            loans=[Loan.from_dict(d) for d in data.get("loans", [])],
        )

    def __str__(self) -> str:
        return f"Member {self.member_id} — {self.name} ({len(self.loans)} active loan(s))"


if __name__ == "__main__":
    from datetime import timedelta

    m = Member(name="Ada Lovelace", member_id="M001")
    m.add_loan(Loan(isbn="978-1492056355", due_date=date.today() + timedelta(days=14)))
    print(m)
    print(m.to_dict())
