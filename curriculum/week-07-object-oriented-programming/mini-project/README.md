# Mini-Project — Library Management System

> **Topic:** every idea from the week in one program — composition, dataclasses, properties, guarded state, and JSON persistence from Week 6
> **Lecture:** all three — [01 — Classes and Instances](../lecture-notes/01-classes-and-instances.md) · [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md) · [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Difficulty:** Advanced
> **Target time:** 6–8 hours
> **Why this one:** it is the week's capstone, and it is the first program where the *design* question — what is an object here, and what does each one own? — matters more than any single method. Week 6 taught your programs to survive a restart; Week 7 taught them to guard their own state. This project is where the two meet: objects whose state round-trips through a JSON file and comes back still guarded. Done well, it looks great in a beginner portfolio.

<!-- no-runnable-file: this page is the project brief, and the project's deliverable is a folder in your own repository holding your classes, the JSON file they saved, and a commit history. The runnable answer is library_system.py, which ships beside this page and is linked from Download and run. It is named after the project rather than the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

You are building a small **library management system** that tracks books,
members, and loans — and can write its entire state to a JSON file and read
it back, so members and their borrowed books survive a program restart.

There are three nouns in that sentence and one thing that owns them, and
that is the whole class design:

- **`Loan`** — one book, out with one member, due back on one day. A loan is
  a *fact*, not a thing that changes: returning a book removes the loan, it
  never edits it. So `Loan` is a **frozen dataclass**.
- **`Book`** — one title on the shelves, and how many of its copies are out.
  The loaned count is guarded: it moves only through `loan_one()` and
  `return_one()`, and it can never go below zero or above the number of
  copies the library owns. That is the same shape as the balance in
  [Exercise 5](../exercises/exercise-05-bank-account.md), so `Book` is a
  **hand-written class**, not a dataclass.
- **`Member`** — one person and the loans they are currently holding. A
  plain **dataclass** with validation in `__post_init__`.
- **`Library`** — books and members, and every operation that touches both:
  stocking, registering, borrowing, returning, overdue reports, fines,
  search, and save/load.

`Library` **has** books and **has** members. `Member` **has** loans. Nothing
here inherits from anything — a library is not a kind of book, and a member
is not a kind of library — so composition is the only honest relationship in
the file. The one exception hierarchy is the *errors*: a small family under
`LibraryError(ValueError)`, so a caller who wrote `except ValueError` still
catches everything, while a caller who cares can name the exact problem.

The program has two faces. Run with nobody typing at it, it performs a
scripted demo against **fixed dates** — stocks a library, borrows, returns,
finds the overdue loans, computes the fines, saves to JSON, loads it back,
and proves the two libraries agree. Then it offers the interactive menu the
brief asks for, and takes "no" for an answer when there is nothing on stdin.
That design is what makes the whole thing testable: same input, same output,
every run.

## Starter

There is no separate starter folder for this project — the skeleton below
is the whole of the scaffolding, and it is the shape the finished program
takes. Save it as `library.py` and fill in the `TODO` markers. The errors,
`Loan`, the display methods, and the entire demo harness are given
complete; the guarded state and the operations are yours.

```python
"""library.py — a small library that tracks books, members and loans.

    python library.py

With no answers typed at it, it runs a scripted demo against fixed dates,
then offers the interactive menu and takes "no" for an answer.
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
    """Anything the library refuses to do."""


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
    """One book, out with one member, due back on one day."""

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
    """One title on the shelves, and how many of its copies are out."""

    def __init__(
        self, title: str, author: str, isbn: str, copies_total: int
    ) -> None:
        """Stock one title, refusing anything that is not a real book."""
        # TODO: refuse an empty title or isbn (LibraryError), a
        # copies_total that is not an int — remember bool IS an int —
        # (TypeError), or one below 1 (LibraryError). Then store title,
        # author, isbn, copies_total, and start self._copies_loaned at 0.

    @property
    def copies_loaned(self) -> int:
        """How many copies are out. Read-only from outside the class."""
        # TODO

    @property
    def copies_available(self) -> int:
        """Copies on the shelf right now. Derived, never stored."""
        # TODO: copies_total minus the loaned count.

    def loan_one(self) -> None:
        """Take one copy off the shelf, or refuse if there are none."""
        # TODO: raise NoCopiesAvailable naming the title and the count
        # when nothing is available; otherwise bump the loaned count.

    def return_one(self) -> None:
        """Put one copy back, or refuse if none were out."""
        # TODO

    def to_dict(self) -> dict[str, object]:
        """A JSON-safe dict, including the loaned count so state survives."""
        # TODO: title, author, isbn, copies_total, copies_loaned.

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Book":
        """Rebuild a Book from the dict `to_dict` produced."""
        # TODO: build the Book, then restore copies_loaned — refusing a
        # value outside 0..copies_total with LibraryError.

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
        # TODO: LibraryError on an empty (or all-whitespace) name or id.

    def add_loan(self, loan: Loan) -> None:
        """Record one loan against this member."""
        # TODO

    def remove_loan(self, isbn: str) -> Loan:
        """Drop this member's earliest loan of `isbn` and return it."""
        # TODO: find it, pop it, return it — or raise NotBorrowed naming
        # the member and the isbn.

    def to_dict(self) -> dict[str, object]:
        """A JSON-safe dict, loans included."""
        # TODO

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Member":
        """Rebuild a Member, and their loans, from the dict `to_dict` made."""
        # TODO

    def __str__(self) -> str:
        """Reader form, e.g. `Ada Lovelace (M-001), 2 on loan`."""
        return f"{self.name} ({self.member_id}), {len(self.loans)} on loan"


# --- the thing that owns them --------------------------------------------


class Library:
    """Books and members, and every operation that touches both."""

    def __init__(self) -> None:
        """Open an empty library."""
        # TODO: self.books keyed by isbn, self.members keyed by member_id.

    def add_book(self, book: Book) -> None:
        """Shelve a book, or add copies if the ISBN is already stocked."""
        # TODO: a new isbn goes in as-is. A known isbn with the SAME title
        # adds its copies to the existing book; a known isbn with a
        # DIFFERENT title is a LibraryError.

    def register_member(self, member: Member) -> None:
        """Add a member, refusing a duplicate id."""
        # TODO

    def get_book(self, isbn: str) -> Book:
        """The book with this ISBN, or a clear refusal."""
        # TODO: raise UnknownBook, chained `from None`.

    def get_member(self, member_id: str) -> Member:
        """The member with this id, or a clear refusal."""
        # TODO: raise UnknownMember, chained `from None`.

    def search(self, query: str) -> list[Book]:
        """Every book whose title or author contains `query`, case-insensitively."""
        # TODO: an empty (or all-whitespace) query returns [].

    def borrow(
        self,
        member_id: str,
        isbn: str,
        days: int = DEFAULT_LOAN_DAYS,
        *,
        on: date | None = None,
    ) -> Loan:
        """Lend one copy of `isbn` to `member_id` and return the new Loan.

        `on` is the day the loan starts. It defaults to today; the demo and
        any test pass a fixed date instead, so the due dates never move.
        """
        # TODO: BOTH lookups first, so an unknown id changes nothing.
        # Refuse days < 1. Then book.loan_one(), build the Loan due
        # (on or date.today()) + timedelta(days=days), record it on the
        # member, and return it.

    def return_book(self, member_id: str, isbn: str) -> None:
        """Take one copy of `isbn` back from `member_id`."""
        # TODO: both lookups, remove the member's loan, then return_one().

    def overdue_loans(self, today: date | None = None) -> list[tuple[Member, Loan]]:
        """Every (member, loan) pair whose due date is before `today`."""
        # TODO: default `today` to date.today(); sort by (due_date,
        # member_id) so the report order is stable.

    def fine_cents(self, today: date | None = None) -> int:
        """Total fines owed, at 25 cents per overdue day, in whole cents."""
        # TODO: days_overdue times FINE_CENTS_PER_DAY, summed.

    def to_dict(self) -> dict[str, object]:
        """The whole library as one JSON-safe dict."""
        # TODO: {"books": [...], "members": [...]} via their to_dict()s.

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Library":
        """Rebuild a library from the dict `to_dict` produced."""
        # TODO: rebuild every book and member, then call
        # _check_loans_agree_with_books() before returning.

    def _check_loans_agree_with_books(self) -> None:
        """Refuse a saved file where the loans and the shelf counts disagree."""
        # TODO: count the loans per isbn across all members. A loan for an
        # unknown isbn is an UnknownBook; a count that differs from that
        # book's copies_loaned is a LibraryError naming both numbers.

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


# --- the harness (given complete — do not edit) -----------------------------


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to `demo` when nobody is typing.

    The prompt goes to stderr, never to `input()`'s own prompt argument, so
    `python library.py > out.txt` saves the answers and not the questions.
    On EOF — no keyboard, a pipe, a test harness — the prompt and the
    fallback are echoed to stdout so the saved transcript still reads like
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
```

The harness is given complete because it is not the project — the classes
are. `run_demo` doubles as your test suite: it exercises every feature once,
against **fixed dates**, so your output either matches the transcript below
character for character or it does not, and either way you know.

## Requirements

1. `Loan` is a frozen dataclass holding `isbn` and `due_date`, with
   `is_overdue`, `days_overdue`, and `to_dict`/`from_dict` that store the
   date as an ISO string.
2. `Book` validates its title, ISBN and copy count on construction;
   `copies_available` is a derived `@property`, never a stored field; the
   loaned count moves only through `loan_one()` and `return_one()`, which
   raise on under- and overflow.
3. `Member` is a dataclass that refuses an empty name or id in
   `__post_init__`, and can add and remove loans — removing a loan it does
   not hold raises `NotBorrowed`.
4. `Library` keys books by ISBN and members by id. `add_book` merges copies
   of an already-stocked ISBN and refuses the same ISBN under a different
   title. `register_member` refuses a duplicate id.
5. `borrow(member_id, isbn, days=14, *, on=None)` looks **both** ids up
   before touching anything, refuses `days < 1`, decrements the book
   through `loan_one`, records a `Loan` on the member, and returns it.
6. `return_book` removes the member's loan, then returns the copy.
7. `overdue_loans(today)` returns every late `(member, loan)` pair, sorted
   by due date then member id; `fine_cents` charges 25 cents per overdue
   day, in whole cents.
8. `save`/`load` round-trip the whole library through `to_dict`/`from_dict`
   as UTF-8 JSON, and `load` refuses a file whose loans disagree with its
   shelf counts.
9. Every refusal raises from the `LibraryError` family, which subclasses
   `ValueError`.
10. Prompts go to stderr; with nothing on stdin the program still runs to
    completion using the demo answers.
11. Do not edit `run_demo()`, the harness, or `main()`.

## Constraints

- **Composition throughout — the only inheritance is the error family.**
  A library is not a kind of book and a member is not a kind of library.
  `Library` *has* books and members; `Member` *has* loans. If you feel the
  urge to subclass, re-read
  [lecture 02 §9](../lecture-notes/02-inheritance-and-composition.md).
- **`copies_available` is derived, never stored.** Store it as a field and
  the day arrives when it disagrees with `copies_total` and the loan
  records — and no error is raised, and you never find out which one lied.
  One `@property`, one subtraction, no drift. This is the week's central
  move at its smallest.
- **`Loan` is frozen.** A loan is a fact. Returning a book removes the
  fact; nothing ever edits it. Frozen also makes it hashable, which is what
  lets `set(member.loans)` work in a test.
- **Both lookups before any mutation in `borrow`.** Validate the member,
  validate the book, *then* take a copy off the shelf. Mutate first and an
  unknown member id leaks a loaned copy that no member holds.
- **The demo runs on fixed dates, and `borrow` takes `on=`.** `date.today()`
  moves; a demo built on it produces different output every day and can
  never be checked against a transcript. Passing the clock in as a
  parameter — a default of today, a fixed date in tests — is the smallest
  form of dependency injection, and you will use it for the rest of your
  career.
- **All persistence goes through `to_dict`/`from_dict`.** `save` and `load`
  are thin wrappers over them. Scatter `json.dump` knowledge through the
  classes and the schema lives in five places or in none.
- **Prompts to stderr, results to stdout.** `input("prompt")` writes the
  prompt to stdout, so `python library.py > run.txt` would save the
  questions into the transcript. The given `ask()` already does this
  correctly — the constraint is to leave it that way.
- **Standard library only, Python 3.10+.** Everything this needs is already
  installed.

## Expected output

Real stdout from the shipped answer, captured on CPython 3.13.2 with
nothing on stdin. The one prompt (`Open the menu? [y/N]: `) goes to
stderr; on EOF the harness echoes it to stdout with the demo answer, which
is why the transcript's last two lines look the way they do.

```bash
$ python library_system.py
```

```text
--- stock ---
  Fluent Python by Luciano Ramalho (2/2 available)
  The Pragmatic Programmer by Andy Hunt (1/1 available)
  Refactoring by Martin Fowler (3/3 available)
  Library(books=3, members=2)
--- borrowing ---
  Ada borrows Fluent Python, due 2026-03-08
  Grace borrows Fluent Python, due 2026-03-29
  Fluent Python by Luciano Ramalho (0/2 available)
--- the third copy does not exist ---
  refused: 'Fluent Python': all 2 copies are on loan
--- unknown ids ---
  refused (member): no member with id M-999
  refused (book): no book with isbn 000-0000000000
--- overdue on 2026-03-15 ---
  Ada Lovelace: Fluent Python was due 2026-03-08 (7 days late)
  fines owed: $1.75
--- returning ---
  Grace returns Fluent Python -> Fluent Python by Luciano Ramalho (1/2 available)
  refused: Grace Hopper has no loan for isbn 978-1492056355
--- search ---
  Fluent Python by Luciano Ramalho (1/2 available)
--- save and load ---
{
  "books": [
    {
      "title": "Fluent Python",
      "author": "Luciano Ramalho",
      "isbn": "978-1492056355",
      "copies_total": 2,
      "copies_loaned": 1
    },
    {
      "title": "The Pragmatic Programmer",
      "author": "Andy Hunt",
      "isbn": "978-0135957059",
      "copies_total": 1,
      "copies_loaned": 0
    },
    {
      "title": "Refactoring",
      "author": "Martin Fowler",
      "isbn": "978-0134757599",
      "copies_total": 3,
      "copies_loaned": 0
    }
  ],
  "members": [
    {
      "name": "Ada Lovelace",
      "member_id": "M-001",
      "loans": [
        {
          "isbn": "978-1492056355",
          "due_date": "2026-03-08"
        }
      ]
    },
    {
      "name": "Grace Hopper",
      "member_id": "M-002",
      "loans": []
    }
  ]
}
  reloaded: Library(books=3, members=2)
  same json: True
  Ada still holds: Ada Lovelace (M-001), 1 on loan
  overdue survives: 1
--- a corrupt file is refused ---
  refused: 'Fluent Python': 0 copies marked on loan but 1 loans recorded
--- interactive menu ---
Open the menu? [y/N]: n
  skipped — nothing on stdin, so the demo above is the whole run
```

Check the arithmetic yourself. Ada borrowed on 2026-02-22 for 14 days, so
the due date is 2026-03-08; on 2026-03-15 that is 7 days late, and
7 × 25¢ = **$1.75**. Grace borrowed on the 15th, due 2026-03-29 — not
late, no fine. `same json: True` is the round-trip proof: the reloaded
library serialises to exactly the dict the original produced. And the last
section is the guard earning its keep — a saved file edited to claim zero
loaned copies while a loan record still exists is refused by name.

## Steps

1. Save the starter and run it. It fails at the very first demo line with
   `AttributeError: 'Library' object has no attribute 'books'` —
   `Library.__init__` is still a comment, and a method whose body is only
   a comment does nothing at all.
2. Build bottom-up, the order the data nests: `Loan` is given — read it,
   it is the model for everything else. Then **`Book`**: constructor
   validation, the two properties, `loan_one`/`return_one`. Check it alone
   in a REPL before touching `Library`:

   ```bash
   python -c "
   from library import Book
   b = Book('Fluent Python', 'Luciano Ramalho', '978-1492056355', 2)
   b.loan_one(); b.loan_one()
   print(b, b.copies_available)
   b.loan_one()"
   ```

   Two loans succeed, the third raises `NoCopiesAvailable`.

3. Then **`Member`**: `__post_init__`, `add_loan`, `remove_loan`.
4. Then **`Library`** stocking and lookups: `__init__`, `add_book`,
   `register_member`, `get_book`, `get_member`, `search`. Run the demo —
   the `--- stock ---` section should now print correctly.
5. Then **`borrow`** and **`return_book`**. Lookups first, mutation last.
   The demo's borrowing, refusal and returning sections come right.
6. Then **`overdue_loans`** and **`fine_cents`** — the overdue section, and
   check the $1.75 by hand.
7. Then persistence: the four `to_dict`/`from_dict` methods and
   `_check_loans_agree_with_books`. The save/load section should print the
   JSON, `same json: True`, and the corrupt-file refusal.
8. Run the whole thing and compare against the transcript, character for
   character. Then run it *interactively* — `python library.py`, answer
   `y` — and put the menu through its paces, including a few refusals.
9. Commit as you go, one commit per stage, not one at the end. The history
   is part of what you hand in.

## The Solution

The reference answer is one file. The classes are the project; `ask`,
`run_demo` and `menu_loop` are the harness around them.

```python
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
```

**Why it works.**

**Four kinds of class, each chosen for a reason, and the choosing is the
lesson.** `Loan` is a *frozen dataclass*: pure data, compared by value,
immutable because a loan is a fact. `Member` is a *mutable dataclass*:
mostly data, one guarded operation (`remove_loan`), validation in
`__post_init__`. `Book` is *hand-written*: its whole point is that
`_copies_loaned` moves only through two methods, and a dataclass would
advertise it as a freely writable field. `Library` is hand-written too,
because it is all behaviour and owns its two dictionaries. One project,
four positions on the "how much machinery do I need?" scale — and each
class sits exactly where its guarantees require.

**`copies_available` is the one-fact rule at its clearest.** Two facts are
stored — how many copies the library owns, how many are out — and the
number a borrower cares about is derived with a subtraction, every time it
is asked for. There is no third field to forget to update. The same rule
shapes `Library.to_dict`: the schema lives in one method per class, and
`save`, `load`, the round-trip check and the corrupt-file guard all go
through it.

**`borrow` orders its work so failure is harmless.** Both lookups first —
an unknown member or ISBN raises before anything has changed. Then the
`days` check. Then `book.loan_one()`, which can still refuse. Only when
every refusal has had its chance does the loan get built and recorded. Read
it top to bottom: at any line where it can raise, nothing has been mutated
yet. That property — *validate, then commit* — is what makes the error
family safe to catch and carry on from, which is exactly what the menu
loop does.

**The error family turns `except` into a sentence.** Every refusal is a
`LibraryError`, which is a `ValueError` — so the REPL catches the lot with
one clause, a test can pin the exact subclass, and a caller who only knows
built-ins still catches it. `UnknownBook`, `UnknownMember`,
`NoCopiesAvailable` and `NotBorrowed` cost four lines and make every
refusal message in the transcript self-describing. Same move as
`InsufficientFunds` in Exercise 5, one size larger.

**`load` does not trust the file.** JSON round-tripping *usually* works,
which is exactly why the failure case needs designing. The file stores the
loaned count per book *and* the loan records per member — the same fact,
twice — and `_check_loans_agree_with_books` refuses any file where the two
disagree. The demo's last section edits a saved file by hand and watches
the load fail loudly instead of opening a library that disagrees with
itself.

**The clock is a parameter.** `borrow(..., on=date(2026, 2, 22))` and
`overdue_loans(today)` take the date instead of reading it, defaulting to
`date.today()` for real use. That single decision is why the demo can
create an *already overdue* loan and why every run of this file prints the
identical transcript. Code that reaches for the wall clock cannot be
tested; code that is handed the time can.

**`ask` keeps stdout clean.** The prompt goes to stderr, so redirecting
stdout captures a readable transcript rather than a jumble of questions and
answers; on EOF it echoes prompt and fallback to stdout so the saved
transcript still reads like a session. That is the Week 6 stdout/stderr
split, applied to `input()`.

## Download and run

The answer to this project is a **folder in your own repository** — your
`library.py`, the JSON file it saved, and a commit history showing how you
got there. That is why this page carries no `README.py`.

The runnable answer ships beside it, named after the project:

Download [library_system.py](./library_system.py) and run it:

```bash
python library_system.py
```

With nothing on stdin it runs the scripted demo in a temporary folder,
declines its own menu, and leaves nothing behind — so it works from a clean
checkout with nothing set up. Run it in a terminal and answer `y` to drive
the interactive menu the brief asks for.

Save your own copy as `library.py`, and commit that one. The longer
download name is there so it cannot overwrite your work.

## Common bugs to catch

- **`TypeError: Object of type date is not JSON serializable`.** You handed
  `json.dump` a dict with a real `date` in it. JSON has no date type — the
  honest representation is an ISO string, `d.isoformat()` on the way out
  and `date.fromisoformat(s)` on the way back, which is exactly what
  `Loan.to_dict`/`from_dict` exist to do.

- **`copies_available` stored as a field.** It starts equal to
  `copies_total`, and then one code path decrements it, another forgets,
  and a reloaded library recomputes it wrongly. Nothing raises — the object
  just quietly disagrees with itself. If you typed
  `self.copies_available = ...` anywhere, that is the bug.

- **`borrow` mutates before it validates.** Call `book.loan_one()` before
  `get_member(member_id)` and an unknown member id leaves a copy marked as
  loaned that no member holds. The demo's `--- unknown ids ---` section
  passes either way — the shelf count is only wrong *afterwards*, which is
  what makes this one nasty. Lookups first, mutation last.

- **`dataclasses.FrozenInstanceError: cannot assign to field 'due_date'`.**
  You tried to extend a loan by editing it. A frozen `Loan` cannot change,
  on purpose: an extension is `remove_loan` plus a new `Loan` with the new
  date. If you find yourself wanting mutation, the design is telling you a
  renewal is a new fact, not an edited old one.

- **`load` accepts any well-formed JSON.** Round-tripping your own saves
  works, so everything looks fine — until a hand-edited or truncated file
  loads into a library whose counts disagree with its loans, and *then*
  fails somewhere far away. The cross-check in `from_dict` is the
  difference between "refused at the door, by name" and "corrupted state
  discovered at return time".

- **`input("Open the menu? ")` with the prompt as argument.** The prompt
  lands in stdout, so `python library.py > run.txt` saves the questions
  into the transcript and the diff against the expected output fails on
  line one. Prompts are diagnostics: stderr.

- **`add_book` replacing instead of merging.** Stocking a second batch of
  an ISBN you already hold should add copies, not overwrite the book —
  overwriting resets `_copies_loaned` to zero while members still hold
  loans, which the load-time cross-check would catch, but only after a
  save/load cycle. Merge, and refuse the same ISBN under a different title.

## Under the hood

<details>
<summary>Under the hood — storing a fact twice on purpose: redundancy as a corruption detector</summary>

This whole week says *store each fact once*, and then `to_dict` goes and
stores the loaned count twice: once as each book's `copies_loaned`, and
once implicitly, as the number of loan records sitting on members. Is that
a violation?

It is — a deliberate one, and the distinction is worth having words for.

*Inside a running program*, redundancy is a liability. Two copies of a
fact must be updated together forever, no error tells you when they drift,
and the class design exists precisely to make drift impossible —
`copies_available` is derived, the loaned count moves only through two
methods.

*At a trust boundary*, redundancy becomes an asset. A JSON file on disk is
outside the guarantees: anyone can edit it, a partial write can truncate
it, another program can produce it. When the same fact arrives twice by
two routes, agreement is evidence of integrity and disagreement is proof
of corruption. That is what `_check_loans_agree_with_books` is: a
consistency check that is only possible *because* the format is redundant.
Checksums, double-entry bookkeeping and RAID parity are the same idea at
other scales — deliberate redundancy, verified at the boundary.

The rule of thumb this project wants you to leave with: **derive inside,
verify at the edges.** One copy of every fact in memory, where your
methods can protect it; and where data crosses a boundary you do not
control, welcome the second copy and check it against the first.

Two smaller things in the same spirit:

**The demo runs in `tempfile.TemporaryDirectory()`.** The context manager
creates a real folder, hands over the path, and deletes it — and
everything in it — on the way out, even on a crash. The download can
exercise save/load without littering your checkout, which is why you can
run it from anywhere. It is the same `with` guarantee from Week 6, one
level up from a file.

**`from None` on the lookup errors.** `get_book` catches `KeyError` and
raises `UnknownBook` — and without `from None`, the traceback would print
the internal `KeyError` first under "During handling of the above
exception, another exception occurred". The caller asked a
library-shaped question and deserves a library-shaped answer; the dict is
an implementation detail the traceback has no business exposing.

</details>

## Acceptance checklist

- [ ] `python library.py` runs to completion with no traceback and no
      typing, and the output matches the transcript character for
      character.
- [ ] Borrowing refuses an unknown member, an unknown ISBN, and an
      exhausted title — each with its own exception from the
      `LibraryError` family.
- [ ] Returning a book the member does not hold raises `NotBorrowed`.
- [ ] `same json: True` — the library survives a save/load round trip.
- [ ] The hand-corrupted file is refused, naming both disagreeing counts.
- [ ] `python library.py > out.txt` leaves the prompt on the screen and a
      clean transcript in the file.
- [ ] Run interactively with `y`, the menu can add, register, borrow,
      return, list, save, load, and quit — and refusals print instead of
      crashing the loop.
- [ ] No inheritance anywhere except the exception family.
- [ ] `copies_available` is a `@property`, not a field.
- [ ] Every signature is type-hinted and every function has a docstring.
- [ ] Committed in stages, not in one lump, and pushed to your fork.

## Stretch

- Add a `Librarian(Member)` subclass with the extra method
  `register_member(library, other)` — then write two sentences on whether
  it *earned* the inheritance, or whether a `role: str` field on `Member`
  would have been honester. (This is the one place the project invites you
  to break the no-inheritance rule so you can judge it.)
- Add reservations: when every copy is out, `reserve(member_id, isbn)`
  queues the member, and `return_book` reports who to notify next. Decide
  which class owns the queue and defend the choice.
- Give `Member` a `statement()` method: every current loan, one per line,
  with its due date and the fine so far, using `format_usd`. Then decide
  where per-member fines belong — on `Member`, or on `Library` — knowing
  only `Library` can resolve an ISBN to a title.
- Write a small `pytest` suite: borrowing decrements availability, the
  overdue report catches exactly the late loan, save/load round-trips, and
  the corrupt file raises. The `on=` parameter is what makes the date
  tests possible — notice you never have to monkeypatch the clock.
- Replace the menu REPL with an `argparse` CLI — `library.py borrow M-001
  978-...` — persisting to a JSON file between invocations. Week 6's
  atomic-save helper (homework problem 6) is exactly what `save` should
  use once real data is at stake.

## Up next

Your `Library` is a well-behaved object that can save and restore itself.
In [Week 8 — APIs & JSON](../../week-08-apis-json/) the JSON stops coming
from your own disk and starts coming from other people's servers — and the
first thing you will build is a class that wraps an API the way `Library`
wraps its dictionaries: a few well-named methods guarding a messy
resource.
