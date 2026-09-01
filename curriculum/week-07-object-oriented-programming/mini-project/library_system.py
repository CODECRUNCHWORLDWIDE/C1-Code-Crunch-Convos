"""library_system.py — the finished answer to Week 7's mini-project.

A small library that tracks books, members and loans, and can write its whole
state to a JSON file and read it back. Run it with::

    python library_system.py

With no answers typed at it, it runs a scripted demo in a temporary folder:
it stocks a library, registers two members, borrows and returns, finds the
overdue loans against a fixed date, saves to JSON, loads it back, and proves
the two libraries agree. Then it offers the interactive menu the brief asks
for, and takes "no" for an answer when nobody is typing.

The classes are the project. `ask`, `run_demo` and `menu_loop` are the harness
around them.
"""

from __future__ import annotations

import json
import sys
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

DEFAULT_LOAN_DAYS = 14
FINE_CENTS_PER_DAY = 25


# --- errors ---------------------------------------------------------------


class LibraryError(ValueError):
    """Anything the library refuses to do.

    It subclasses ValueError, so a caller who wrote `except ValueError` around
    a borrow still catches it, while a caller who cares can name the exact
    problem. Same move as InsufficientFunds in Exercise 5.
    """


class UnknownBook(LibraryError):
    """Raised when an ISBN is not on the shelves."""


class UnknownMember(LibraryError):
    """Raised when a member id is not registered."""


class NoCopiesAvailable(LibraryError):
    """Raised when every copy of a book is already out on loan."""


class NotBorrowed(LibraryError):
    """Raised when a member returns a book they do not have."""


# --- the three nouns ------------------------------------------------------


@dataclass(frozen=True)
class Loan:
    """One book, out with one member, due back on one day.

    Frozen because a loan is a fact, not a thing that changes. Returning a
    book removes the loan; it never edits it. Frozen also makes it hashable,
    which is what lets `set(member.loans)` work in a test.
    """

    isbn: str
    due_date: date

    def is_overdue(self, today: date) -> bool:
        """True when the due date has already passed on `today`."""
        return self.due_date < today

    def days_overdue(self, today: date) -> int:
        """How many days late this loan is, or 0 if it is not late."""
        return max((today - self.due_date).days, 0)

    def to_dict(self) -> dict[str, str]:
        """A JSON-safe dict. The date becomes an ISO string."""
        return {"isbn": self.isbn, "due_date": self.due_date.isoformat()}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Loan":
        """Rebuild a Loan from the dict `to_dict` produced."""
        return cls(isbn=data["isbn"], due_date=date.fromisoformat(data["due_date"]))


class Book:
    """One title on the shelves, and how many of its copies are out.

    Written by hand rather than as a dataclass, because the loaned count is
    guarded: it moves only through `loan_one` and `return_one`, and it can
    never go below zero or above the number of copies the library owns. That
    is the same shape as the balance in Exercise 5.
    """

    def __init__(
        self, title: str, author: str, isbn: str, copies_total: int
    ) -> None:
        """Stock one title, refusing anything that is not a real book."""
        if not title.strip():
            raise LibraryError("a book needs a non-empty title")
        if not isbn.strip():
            raise LibraryError(f"{title}: a book needs a non-empty isbn")
        if not isinstance(copies_total, int) or isinstance(copies_total, bool):
            raise TypeError(
                f"{title}: copies_total must be an int, got {copies_total!r}"
            )
        if copies_total < 1:
            raise LibraryError(
                f"{title}: copies_total must be at least 1, got {copies_total}"
            )
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies_total = copies_total
        self._copies_loaned = 0

    @property
    def copies_loaned(self) -> int:
        """How many copies are out. Read-only from outside the class."""
        return self._copies_loaned

    @property
    def copies_available(self) -> int:
        """Copies on the shelf right now. Derived, never stored."""
        return self.copies_total - self._copies_loaned

    def loan_one(self) -> None:
        """Take one copy off the shelf, or refuse if there are none."""
        if self.copies_available < 1:
            raise NoCopiesAvailable(
                f"{self.title!r}: all {self.copies_total} copies are on loan"
            )
        self._copies_loaned += 1

    def return_one(self) -> None:
        """Put one copy back, or refuse if none were out."""
        if self._copies_loaned < 1:
            raise LibraryError(f"{self.title!r}: no copies are on loan")
        self._copies_loaned -= 1

    def to_dict(self) -> dict[str, object]:
        """A JSON-safe dict, including the loaned count so state survives."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "copies_total": self.copies_total,
            "copies_loaned": self._copies_loaned,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Book":
        """Rebuild a Book from the dict `to_dict` produced."""
        book = cls(
            title=str(data["title"]),
            author=str(data["author"]),
            isbn=str(data["isbn"]),
            copies_total=int(data["copies_total"]),  # type: ignore[arg-type]
        )
        loaned = int(data.get("copies_loaned", 0))  # type: ignore[arg-type]
        if not 0 <= loaned <= book.copies_total:
            raise LibraryError(
                f"{book.title!r}: copies_loaned {loaned} is outside "
                f"0..{book.copies_total}"
            )
        book._copies_loaned = loaned
        return book

    def __str__(self) -> str:
        """Reader form, e.g. `Fluent Python by Luciano Ramalho (2/3 available)`."""
        return (
            f"{self.title} by {self.author} "
            f"({self.copies_available}/{self.copies_total} available)"
        )

    def __repr__(self) -> str:
        """Developer form, showing the raw counts."""
        return (
            f"Book(title={self.title!r}, author={self.author!r}, "
            f"isbn={self.isbn!r}, copies_total={self.copies_total!r}, "
            f"copies_loaned={self._copies_loaned!r})"
        )


@dataclass
class Member:
    """One person and the loans they are currently holding."""

    name: str
    member_id: str
    loans: list[Loan] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Refuse a member with no name or no id."""
        if not self.name.strip():
            raise LibraryError("a member needs a non-empty name")
        if not self.member_id.strip():
            raise LibraryError(f"{self.name}: a member needs a non-empty id")

    def add_loan(self, loan: Loan) -> None:
        """Record one loan against this member."""
        self.loans.append(loan)

    def remove_loan(self, isbn: str) -> Loan:
        """Drop this member's earliest loan of `isbn` and return it."""
        for index, loan in enumerate(self.loans):
            if loan.isbn == isbn:
                return self.loans.pop(index)
        raise NotBorrowed(f"{self.name} has no loan for isbn {isbn}")

    def to_dict(self) -> dict[str, object]:
        """A JSON-safe dict, loans included."""
        return {
            "name": self.name,
            "member_id": self.member_id,
            "loans": [loan.to_dict() for loan in self.loans],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Member":
        """Rebuild a Member, and their loans, from the dict `to_dict` made."""
        raw_loans: Iterable[dict[str, str]] = data.get("loans", [])  # type: ignore[assignment]
        return cls(
            name=str(data["name"]),
            member_id=str(data["member_id"]),
            loans=[Loan.from_dict(item) for item in raw_loans],
        )

    def __str__(self) -> str:
        """Reader form, e.g. `Ada Lovelace (M-001), 2 on loan`."""
        return f"{self.name} ({self.member_id}), {len(self.loans)} on loan"


# --- the thing that owns them --------------------------------------------


class Library:
    """Books and members, and every operation that touches both.

    `Library` **has** books and **has** members. Nothing here inherits from
    anything: a library is not a kind of book and a member is not a kind of
    library, so composition is the only honest relationship in the file.
    """

    def __init__(self) -> None:
        """Open an empty library."""
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}

    # --- stocking ---------------------------------------------------------

    def add_book(self, book: Book) -> None:
        """Shelve a book, or add copies if the ISBN is already stocked."""
        existing = self.books.get(book.isbn)
        if existing is None:
            self.books[book.isbn] = book
            return
        if existing.title != book.title:
            raise LibraryError(
                f"isbn {book.isbn} is already {existing.title!r}, "
                f"not {book.title!r}"
            )
        existing.copies_total += book.copies_total

    def register_member(self, member: Member) -> None:
        """Add a member, refusing a duplicate id."""
        if member.member_id in self.members:
            raise LibraryError(f"member id {member.member_id} is already registered")
        self.members[member.member_id] = member

    # --- lookups that refuse to guess -------------------------------------

    def get_book(self, isbn: str) -> Book:
        """The book with this ISBN, or a clear refusal."""
        try:
            return self.books[isbn]
        except KeyError:
            raise UnknownBook(f"no book with isbn {isbn}") from None

    def get_member(self, member_id: str) -> Member:
        """The member with this id, or a clear refusal."""
        try:
            return self.members[member_id]
        except KeyError:
            raise UnknownMember(f"no member with id {member_id}") from None

    def search(self, query: str) -> list[Book]:
        """Every book whose title or author contains `query`, case-insensitively."""
        needle = query.strip().lower()
        if not needle:
            return []
        return [
            book
            for book in self.books.values()
            if needle in book.title.lower() or needle in book.author.lower()
        ]

    # --- the two operations that move a book ------------------------------

    def borrow(
        self,
        member_id: str,
        isbn: str,
        days: int = DEFAULT_LOAN_DAYS,
        *,
        on: date | None = None,
    ) -> Loan:
        """Lend one copy of `isbn` to `member_id` and return the new Loan.

        `on` is the day the loan starts. It defaults to today; the demo and any
        test pass a fixed date instead, so the due dates never move.
        """
        member = self.get_member(member_id)   # both lookups first, so an
        book = self.get_book(isbn)            # unknown id changes nothing
        if days < 1:
            raise LibraryError(f"a loan must run at least 1 day, got {days}")
        book.loan_one()                       # may raise NoCopiesAvailable
        loan = Loan(isbn=isbn, due_date=(on or date.today()) + timedelta(days=days))
        member.add_loan(loan)
        return loan

    def return_book(self, member_id: str, isbn: str) -> None:
        """Take one copy of `isbn` back from `member_id`."""
        member = self.get_member(member_id)
        book = self.get_book(isbn)
        member.remove_loan(isbn)              # may raise NotBorrowed
        book.return_one()

    # --- reporting --------------------------------------------------------

    def overdue_loans(self, today: date | None = None) -> list[tuple[Member, Loan]]:
        """Every (member, loan) pair whose due date is before `today`."""
        when = today or date.today()
        overdue = [
            (member, loan)
            for member in self.members.values()
            for loan in member.loans
            if loan.is_overdue(when)
        ]
        overdue.sort(key=lambda pair: (pair[1].due_date, pair[0].member_id))
        return overdue

    def fine_cents(self, today: date | None = None) -> int:
        """Total fines owed, at 25 cents per overdue day, in whole cents."""
        when = today or date.today()
        return sum(
            loan.days_overdue(when) * FINE_CENTS_PER_DAY
            for _member, loan in self.overdue_loans(when)
        )

    # --- persistence ------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """The whole library as one JSON-safe dict."""
        return {
            "books": [book.to_dict() for book in self.books.values()],
            "members": [member.to_dict() for member in self.members.values()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Library":
        """Rebuild a library from the dict `to_dict` produced."""
        library = cls()
        raw_books: Iterable[dict[str, object]] = data.get("books", [])  # type: ignore[assignment]
        for item in raw_books:
            book = Book.from_dict(item)
            library.books[book.isbn] = book
        raw_members: Iterable[dict[str, object]] = data.get("members", [])  # type: ignore[assignment]
        for item in raw_members:
            member = Member.from_dict(item)
            library.members[member.member_id] = member
        library._check_loans_agree_with_books()
        return library

    def _check_loans_agree_with_books(self) -> None:
        """Refuse a saved file where the loans and the shelf counts disagree."""
        counted: dict[str, int] = {}
        for member in self.members.values():
            for loan in member.loans:
                if loan.isbn not in self.books:
                    raise UnknownBook(
                        f"{member.name} holds a loan for unknown isbn {loan.isbn}"
                    )
                counted[loan.isbn] = counted.get(loan.isbn, 0) + 1
        for isbn, book in self.books.items():
            held = counted.get(isbn, 0)
            if held != book.copies_loaned:
                raise LibraryError(
                    f"{book.title!r}: {book.copies_loaned} copies marked on loan "
                    f"but {held} loans recorded"
                )

    def save(self, path: str | Path) -> None:
        """Write the library to `path` as UTF-8 JSON."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    @classmethod
    def load(cls, path: str | Path) -> "Library":
        """Read a library back from `path`."""
        source = Path(path)
        with source.open("r", encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    def __len__(self) -> int:
        """How many distinct titles are stocked."""
        return len(self.books)

    def __repr__(self) -> str:
        """Developer form: the two sizes, not the two collections."""
        return f"Library(books={len(self.books)}, members={len(self.members)})"


# --- the harness ----------------------------------------------------------


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to `demo` when nobody is typing.

    The prompt goes to stderr, never to `input()`'s own prompt argument, so
    `python library_system.py > out.txt` saves the answers and not the
    questions. On EOF — no keyboard, a pipe, a test harness — the prompt and
    the fallback are echoed to stdout so the saved transcript still reads like
    a session.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def format_usd(cents: int) -> str:
    """Render a whole number of cents as `$1,234.56`."""
    dollars, remainder = divmod(cents, 100)
    return f"${dollars:,}.{remainder:02d}"


def build_sample_library() -> Library:
    """A library with three titles and two members, and nothing on loan."""
    library = Library()
    for title, author, isbn, copies in [
        ("Fluent Python", "Luciano Ramalho", "978-1492056355", 2),
        ("The Pragmatic Programmer", "Andy Hunt", "978-0135957059", 1),
        ("Refactoring", "Martin Fowler", "978-0134757599", 3),
    ]:
        library.add_book(Book(title, author, isbn, copies))
    library.register_member(Member("Ada Lovelace", "M-001"))
    library.register_member(Member("Grace Hopper", "M-002"))
    return library


def run_demo(workspace: Path) -> None:
    """Drive every feature once, against fixed dates, and print what happened."""
    today = date(2026, 3, 15)
    library = build_sample_library()

    print("--- stock ---")
    for book in library.books.values():
        print(f"  {book}")
    print(f"  {library!r}")

    print("--- borrowing ---")
    # Borrowed three weeks ago on a 14-day loan, so it is already late.
    late = library.borrow("M-001", "978-1492056355", on=date(2026, 2, 22))
    print(f"  Ada borrows Fluent Python, due {late.due_date}")
    fresh = library.borrow("M-002", "978-1492056355", on=today)
    print(f"  Grace borrows Fluent Python, due {fresh.due_date}")
    print(f"  {library.get_book('978-1492056355')}")

    print("--- the third copy does not exist ---")
    try:
        library.borrow("M-001", "978-1492056355", on=today)
    except NoCopiesAvailable as exc:
        print(f"  refused: {exc}")

    print("--- unknown ids ---")
    for label, call in [
        ("member", lambda: library.borrow("M-999", "978-0134757599", on=today)),
        ("book", lambda: library.borrow("M-001", "000-0000000000", on=today)),
    ]:
        try:
            call()
        except LibraryError as exc:
            print(f"  refused ({label}): {exc}")

    print("--- overdue on 2026-03-15 ---")
    for member, loan in library.overdue_loans(today):
        book = library.get_book(loan.isbn)
        print(
            f"  {member.name}: {book.title} was due {loan.due_date} "
            f"({loan.days_overdue(today)} days late)"
        )
    print(f"  fines owed: {format_usd(library.fine_cents(today))}")

    print("--- returning ---")
    library.return_book("M-002", "978-1492056355")
    print(f"  Grace returns Fluent Python -> {library.get_book('978-1492056355')}")
    try:
        library.return_book("M-002", "978-1492056355")
    except NotBorrowed as exc:
        print(f"  refused: {exc}")

    print("--- search ---")
    for book in library.search("python"):
        print(f"  {book}")

    print("--- save and load ---")
    path = workspace / "library.json"
    library.save(path)
    print(path.read_text(encoding="utf-8"), end="")
    reloaded = Library.load(path)
    print(f"  reloaded: {reloaded!r}")
    print(f"  same json: {reloaded.to_dict() == library.to_dict()}")
    print(f"  Ada still holds: {reloaded.get_member('M-001')}")
    print(f"  overdue survives: {len(reloaded.overdue_loans(today))}")

    print("--- a corrupt file is refused ---")
    broken = json.loads(path.read_text(encoding="utf-8"))
    broken["books"][0]["copies_loaned"] = 0     # a loan with no copy behind it
    bad_path = workspace / "broken.json"
    bad_path.write_text(json.dumps(broken), encoding="utf-8")
    try:
        Library.load(bad_path)
    except LibraryError as exc:
        print(f"  refused: {exc}")


MENU = """
1. Add a book
2. Register a member
3. Borrow a book
4. Return a book
5. List overdue loans
6. Save
7. Load
8. Quit
"""


def menu_loop(library: Library, path: Path) -> None:
    """The tiny REPL the brief asks for. Every branch calls the library."""
    while True:
        print(MENU)
        choice = ask("choice> ", "8").strip()
        try:
            if choice == "1":
                library.add_book(
                    Book(
                        ask("title: ", "Untitled"),
                        ask("author: ", "Unknown"),
                        ask("isbn: ", "000-0000000000"),
                        int(ask("copies: ", "1")),
                    )
                )
            elif choice == "2":
                library.register_member(
                    Member(ask("name: ", "Anon"), ask("member id: ", "M-000"))
                )
            elif choice == "3":
                loan = library.borrow(ask("member id: ", "M-001"), ask("isbn: ", ""))
                print(f"due {loan.due_date}")
            elif choice == "4":
                library.return_book(ask("member id: ", "M-001"), ask("isbn: ", ""))
                print("returned")
            elif choice == "5":
                for member, loan in library.overdue_loans():
                    print(f"{member.name}: {loan.isbn} due {loan.due_date}")
            elif choice == "6":
                library.save(path)
                print(f"saved to {path}")
            elif choice == "7":
                library = Library.load(path)
                print(f"loaded {library!r}")
            elif choice == "8":
                print("bye")
                return
            else:
                print(f"no such choice: {choice!r}")
        except (LibraryError, TypeError, ValueError) as exc:
            print(f"refused: {exc}")


def main() -> None:
    """Run the scripted demo, then offer the menu to whoever is typing."""
    with tempfile.TemporaryDirectory() as scratch:
        workspace = Path(scratch)
        run_demo(workspace)

        print("--- interactive menu ---")
        if ask("Open the menu? [y/N]: ", "n").strip().lower().startswith("y"):
            menu_loop(build_sample_library(), workspace / "library.json")
        else:
            print("  skipped — nothing on stdin, so the demo above is the whole run")


if __name__ == "__main__":
    main()
