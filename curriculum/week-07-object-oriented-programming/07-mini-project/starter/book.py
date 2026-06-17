"""book.py — Book class skeleton for the Library mini-project.

Fill in each ``TODO``. The README in the parent folder has the full spec
and the grading rubric.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Book:
    """A book that the library owns.

    Attributes
    ----------
    title : str
        Display title.
    author : str
        Author's full name.
    isbn : str
        Unique identifier across the library.
    copies_total : int
        How many physical copies the library owns. Must be >= 1.
    """

    title: str
    author: str
    isbn: str
    copies_total: int = 1
    # `_copies_loaned` is "protected": clients should not touch it directly.
    # `repr=False` keeps it out of the auto-generated __repr__ for tidiness.
    _copies_loaned: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        # TODO: raise ValueError if copies_total < 1 or _copies_loaned < 0
        # or _copies_loaned > copies_total.
        if self.copies_total < 1:
            raise ValueError("a book needs at least one total copy")
        if self._copies_loaned < 0 or self._copies_loaned > self.copies_total:
            raise ValueError("invalid _copies_loaned value")

    # ------------------------------------------------------------------
    # Public read-only view of how many copies are on the shelf.
    # ------------------------------------------------------------------
    @property
    def copies_available(self) -> int:
        # TODO: return copies_total - _copies_loaned
        return self.copies_total - self._copies_loaned

    # ------------------------------------------------------------------
    # Mutating operations — narrow, validated.
    # ------------------------------------------------------------------
    def loan_one(self) -> None:
        """Mark one copy as loaned out."""
        # TODO: raise ValueError if copies_available == 0; otherwise increment.
        if self.copies_available == 0:
            raise ValueError(f"no copies of {self.title!r} are available")
        self._copies_loaned += 1

    def return_one(self) -> None:
        """Mark one copy as returned to the shelf."""
        # TODO: raise ValueError if nothing is loaned out; otherwise decrement.
        if self._copies_loaned == 0:
            raise ValueError(f"no copies of {self.title!r} are currently loaned out")
        self._copies_loaned -= 1

    # ------------------------------------------------------------------
    # JSON round-trip helpers.
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Serialize to a plain ``dict`` (safe to pass to ``json.dumps``)."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "copies_total": self.copies_total,
            "copies_loaned": self._copies_loaned,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Build a ``Book`` from a dict produced by ``to_dict``."""
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            copies_total=int(data.get("copies_total", 1)),
            _copies_loaned=int(data.get("copies_loaned", 0)),
        )

    # ------------------------------------------------------------------
    # Custom display (overrides the dataclass-generated __repr__/__str__).
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"{self.title!r} by {self.author} "
            f"[{self.copies_available}/{self.copies_total} available]"
        )


if __name__ == "__main__":
    # A small smoke test you can run with `python book.py`.
    b = Book(title="Fluent Python", author="Luciano Ramalho", isbn="978-1492056355", copies_total=2)
    print(b)
    b.loan_one()
    print(b)
    b.return_one()
    print(b)
    print(repr(b))
    print(b.to_dict())
