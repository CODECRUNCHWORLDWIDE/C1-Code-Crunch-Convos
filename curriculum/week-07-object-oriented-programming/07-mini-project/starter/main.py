"""main.py — Tiny REPL driver for the Library mini-project.

Run with::

    python main.py

This is a *driver*, not graded UI — the menu exists so you can manually
exercise every feature of your library.
"""

from __future__ import annotations

from datetime import date

from book import Book
from library import Library
from member import Member

MENU = """
Code Crunch Library
-------------------
1. Add book
2. Register member
3. Borrow book
4. Return book
5. List overdue loans
6. Save to JSON
7. Load from JSON
8. Show library summary
0. Quit
"""


def prompt(label: str) -> str:
    return input(f"  {label}: ").strip()


def run() -> None:
    library = Library()

    while True:
        print(MENU)
        choice = prompt("choose")

        try:
            if choice == "0":
                print("bye!")
                return

            elif choice == "1":
                title = prompt("title")
                author = prompt("author")
                isbn = prompt("isbn")
                copies = int(prompt("copies (default 1)") or "1")
                library.add_book(Book(title=title, author=author, isbn=isbn, copies_total=copies))
                print("  -> added")

            elif choice == "2":
                name = prompt("name")
                mid = prompt("member_id")
                library.register_member(Member(name=name, member_id=mid))
                print("  -> registered")

            elif choice == "3":
                mid = prompt("member_id")
                isbn = prompt("isbn")
                days = int(prompt("days (default 14)") or "14")
                loan = library.borrow(mid, isbn, days=days)
                print(f"  -> due {loan.due_date.isoformat()}")

            elif choice == "4":
                mid = prompt("member_id")
                isbn = prompt("isbn")
                library.return_book(mid, isbn)
                print("  -> returned")

            elif choice == "5":
                today_str = prompt("today (YYYY-MM-DD, blank for actual today)")
                today = date.fromisoformat(today_str) if today_str else None
                overdue = library.overdue_loans(today=today)
                if not overdue:
                    print("  -> nothing overdue")
                else:
                    for member, loan in overdue:
                        book = library.books[loan.isbn]
                        print(f"  - {member.name} has {book.title!r} overdue (due {loan.due_date})")

            elif choice == "6":
                path = prompt("path") or "library.json"
                library.save(path)
                print(f"  -> saved to {path}")

            elif choice == "7":
                path = prompt("path") or "library.json"
                library = Library.load(path)
                print(f"  -> loaded {library}")

            elif choice == "8":
                print(f"  -> {library}")
                for b in library.books.values():
                    print(f"     {b}")
                for m in library.members.values():
                    print(f"     {m}")

            else:
                print("  ?")
        except (ValueError, FileNotFoundError) as exc:
            print(f"  error: {exc}")


if __name__ == "__main__":
    run()
