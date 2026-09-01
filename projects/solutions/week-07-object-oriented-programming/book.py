"""The `Book` class: a title on the shelf, plus how many copies are out."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Book:
    """One catalogue entry.

    `copies_total` is how many physical copies the library owns.
    `_copies_loaned` is how many of those are currently in someone's bag.
    `copies_available` is the difference and is never stored — deriving it means
    the two numbers can never drift apart.
    """

    title: str
    author: str
    isbn: str
    copies_total: int = 1
    _copies_loaned: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("a book needs a non-empty title")
        if not self.isbn.strip():
            raise ValueError(f"{self.title!r}: isbn must not be empty")
        if self.copies_total < 1:
            raise ValueError(
                f"{self.title!r}: a book needs at least one copy, got {self.copies_total!r}"
            )
        if not 0 <= self._copies_loaned <= self.copies_total:
            raise ValueError(
                f"{self.title!r}: loaned count {self._copies_loaned} is outside "
                f"0..{self.copies_total}"
            )

    # --- derived state ----------------------------------------------------

    @property
    def copies_available(self) -> int:
        """Copies a member could borrow right now."""
        return self.copies_total - self._copies_loaned

    @property
    def copies_loaned(self) -> int:
        """Read-only view of the protected counter."""
        return self._copies_loaned

    # --- state transitions ------------------------------------------------

    def loan_one(self) -> None:
        """Move one copy off the shelf."""
        if self.copies_available == 0:
            raise ValueError(f"no copies of {self.title!r} available")
        self._copies_loaned += 1

    def return_one(self) -> None:
        """Move one copy back onto the shelf."""
        if self._copies_loaned == 0:
            raise ValueError(f"no copies of {self.title!r} are loaned out")
        self._copies_loaned -= 1

    # --- serialization ----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "copies_total": self.copies_total,
            "copies_loaned": self._copies_loaned,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Book":
        """Rebuild a Book from `to_dict` output.

        Note this restores `copies_loaned` too. The version in lecture 03 does
        not, which silently resets every loan on load — a real bug once you add
        save/load.
        """
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            copies_total=data.get("copies_total", 1),
            _copies_loaned=data.get("copies_loaned", 0),
        )

    # --- display ----------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"{self.title!r} by {self.author} "
            f"({self.copies_available}/{self.copies_total} available)"
        )
