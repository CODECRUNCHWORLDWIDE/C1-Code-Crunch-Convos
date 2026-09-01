"""Stretch goal: a `Librarian` is a `Member` who can also register other members.

Kept in its own module so the core three files stay exactly the shape the
mini-project spec asks for. `Library` is imported only for type checking, so
there is no import cycle at runtime.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from member import Member

if TYPE_CHECKING:  # pragma: no cover - typing only
    from library import Library


class Librarian(Member):
    """A member with staff privileges.

    This is the one place inheritance is honest in this project: a librarian
    *is a* member — they have a card, they borrow books, they show up in the
    overdue report — and they gain one extra capability. Nothing is removed.
    """

    def register_member(self, library: "Library", member: Member) -> None:
        """Delegate registration to the library.

        The librarian does not own the member dictionary; the library does.
        This method exists so the *permission* lives on the role while the
        *data* stays with its owner.
        """
        library.register_member(member)

    def __str__(self) -> str:
        return f"{super().__str__()} [staff]"
