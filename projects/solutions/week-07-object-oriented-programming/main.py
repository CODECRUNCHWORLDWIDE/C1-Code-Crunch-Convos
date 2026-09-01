"""A tiny REPL over the library.

    python main.py           # interactive menu
    python main.py --demo    # non-interactive walkthrough, no input needed
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

from book import Book
from librarian import Librarian
from library import Library
from member import Member

SAVE_PATH = Path("library.json")

MENU = """
=== Crunch Community Library ===
1) Add a book
2) Register a member
3) Borrow a book
4) Return a book
5) List overdue loans
6) Save
7) Load
8) List catalogue
9) Search
0) Quit
"""


def _ask(prompt: str) -> str:
    return input(prompt).strip()


def _ask_int(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"  not a number: {raw!r}; using {default}")
        return default


def repl(library: Library) -> None:
    actions = {
        "1": _add_book,
        "2": _register_member,
        "3": _borrow,
        "4": _return,
        "5": _overdue,
        "6": _save,
        "7": _load,
        "8": _catalogue,
        "9": _search,
    }
    while True:
        print(MENU)
        choice = _ask("choose: ")
        if choice == "0":
            print("bye")
            return
        action = actions.get(choice)
        if action is None:
            print(f"  unknown option {choice!r}")
            continue
        try:
            result = action(library)
        except ValueError as exc:
            print(f"  error: {exc}")
            continue
        if isinstance(result, Library):   # _load hands back a new object
            library = result


def _add_book(library: Library) -> None:
    book = Book(
        title=_ask("title: "),
        author=_ask("author: "),
        isbn=_ask("isbn: "),
        copies_total=_ask_int("copies", 1),
    )
    library.add_book(book)
    print(f"  added: {library.get_book(book.isbn)}")


def _register_member(library: Library) -> None:
    name = _ask("name: ")
    member_id = _ask("member id: ")
    staff = _ask("staff? (y/N): ").lower().startswith("y")
    member: Member = (Librarian if staff else Member)(name=name, member_id=member_id)
    library.register_member(member)
    print(f"  registered: {member}")


def _borrow(library: Library) -> None:
    member_id = _ask("member id: ")
    isbn = _ask("isbn: ")
    days = _ask_int("days", 14)
    loan = library.borrow(member_id, isbn, days=days)
    print(f"  loaned: {loan}")


def _return(library: Library) -> None:
    library.return_book(_ask("member id: "), _ask("isbn: "))
    print("  returned")


def _overdue(library: Library) -> None:
    rows = library.overdue_loans()
    if not rows:
        print("  nothing overdue")
        return
    fines = library.fines()
    for member, loan in rows:
        print(f"  {member.name} ({member.member_id}): {loan} "
              f"[{loan.days_overdue()} day(s) late]")
    for member_id, amount in fines.items():
        print(f"  fine: {member_id} owes ${amount:.2f}")


def _save(library: Library) -> None:
    library.save(SAVE_PATH)
    print(f"  saved to {SAVE_PATH.resolve()}")


def _load(library: Library) -> Library:
    loaded = Library.load(SAVE_PATH)
    print(f"  loaded {loaded!r}")
    return loaded


def _catalogue(library: Library) -> None:
    if not len(library):
        print("  catalogue is empty")
        return
    for book in library:
        print(f"  {book}")


def _search(library: Library) -> None:
    hits = library.search(_ask("query: "))
    if not hits:
        print("  no matches")
        return
    for book in hits:
        print(f"  {book}")


def demo() -> None:
    """Everything the rubric asks for, in one non-interactive run."""
    today = date(2026, 3, 1)
    library = Library(name="Crunch Community Library")

    library.add_book(Book("Fluent Python", "Luciano Ramalho", "978-1492056355", 2))
    library.add_book(Book("Python Crash Course", "Eric Matthes", "978-1718502703", 1))
    library.add_book(Book("Think Python", "Allen B. Downey", "978-1491939369", 3))
    print(repr(library))

    ada = Member(name="Ada Lovelace", member_id="M-001")
    grace = Member(name="Grace Hopper", member_id="M-002")
    staff = Librarian(name="Kay Sims", member_id="S-100")
    library.register_member(ada)
    library.register_member(grace)
    library.register_member(staff)
    staff.register_member(library, Member(name="Alan Turing", member_id="M-003"))
    print("members:", sorted(library.members))

    # --- borrowing -----------------------------------------------------
    loan = library.borrow("M-001", "978-1492056355", days=14, today=today)
    print("loan:", loan)
    library.borrow("M-002", "978-1492056355", days=14, today=today)
    print("after two loans:", library.get_book("978-1492056355"))

    try:
        library.borrow("M-003", "978-1492056355", today=today)
    except ValueError as exc:
        print("ValueError:", exc)

    try:
        library.borrow("M-999", "978-1492056355", today=today)
    except ValueError as exc:
        print("ValueError:", exc)

    # Double-borrow is rejected, and the rollback keeps the counts honest.
    library.borrow("M-001", "978-1491939369", today=today)
    try:
        library.borrow("M-001", "978-1491939369", today=today)
    except ValueError as exc:
        print("ValueError:", exc)
    print("after rollback:", library.get_book("978-1491939369"))

    # --- overdue -------------------------------------------------------
    library.borrow("M-003", "978-1718502703", days=7, today=today - timedelta(days=30))
    later = today + timedelta(days=1)
    for member, overdue_loan in library.overdue_loans(later):
        print(f"overdue: {member.name} -> {overdue_loan} "
              f"({overdue_loan.days_overdue(later)} days late)")
    print("fines:", library.fines(later))

    # --- save / load ---------------------------------------------------
    path = Path("library-demo.json")
    library.save(path)
    reloaded = Library.load(path)
    print("reloaded:", repr(reloaded))
    print("round-trip identical:", reloaded.to_dict() == library.to_dict())
    print("loan survived reload:", reloaded.get_member("M-001").loans)
    print("counts survived reload:", reloaded.get_book("978-1492056355"))

    # --- returning -----------------------------------------------------
    reloaded.return_book("M-001", "978-1492056355")
    print("after return:", reloaded.get_book("978-1492056355"))
    try:
        reloaded.return_book("M-001", "978-1492056355")
    except ValueError as exc:
        print("ValueError:", exc)

    # --- search --------------------------------------------------------
    print("search 'python':", [b.title for b in reloaded.search("python")])
    print("search 'downey':", [b.title for b in reloaded.search("downey")])

    path.unlink()
    print("demo complete")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        repl(Library())
