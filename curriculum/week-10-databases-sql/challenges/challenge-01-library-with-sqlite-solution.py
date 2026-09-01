"""challenge-01-library-with-sqlite-solution.py — the Week 7 library, on SQLite.

Books, members and loans live in a real database instead of a JSON file.
Every feature the challenge asks for is a function here: add a book, register
a member, borrow (refused when no copies are free), return, list every member
with what they have out, and report the most-borrowed book of a month.

This download runs against an in-memory database — ``:memory:`` — so it
needs no file, cannot collide with anything of yours, and leaves nothing
behind. Point ``connect()`` at a path instead and the same code runs a real
library file. The demo dates are fixed so the output is checkable.

Run it with::

    python challenge-01-library-with-sqlite-solution.py
"""

import sqlite3
from typing import Final

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    author       TEXT    NOT NULL,
    isbn         TEXT    UNIQUE,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0)
);

CREATE TABLE IF NOT EXISTS members (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE,
    joined_on TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id     INTEGER NOT NULL REFERENCES books(id),
    member_id   INTEGER NOT NULL REFERENCES members(id),
    borrowed_on TEXT    NOT NULL,
    due_on      TEXT    NOT NULL,
    returned_on TEXT
);

CREATE INDEX IF NOT EXISTS idx_loans_book_id   ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans(member_id);
"""


class LibraryError(Exception):
    """Raised when a library rule refuses an operation."""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the library database with foreign keys enforced."""
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the schema. Safe to call on every start — IF NOT EXISTS."""
    conn.executescript(SCHEMA)
    conn.commit()


def add_book(
    conn: sqlite3.Connection, title: str, author: str, isbn: str, total_copies: int
) -> int:
    """Insert a book and return its id."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO books (title, author, isbn, total_copies) "
            "VALUES (?, ?, ?, ?)",
            (title, author, isbn, total_copies),
        )
    return cursor.lastrowid


def register_member(
    conn: sqlite3.Connection, name: str, email: str, joined_on: str
) -> int:
    """Insert a member and return their id."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO members (name, email, joined_on) VALUES (?, ?, ?)",
            (name, email, joined_on),
        )
    return cursor.lastrowid


def available_copies(conn: sqlite3.Connection, book_id: int) -> int:
    """Return total copies minus the loans that have not come back."""
    cursor = conn.execute(
        """
        SELECT (SELECT total_copies FROM books WHERE id = ?)
             - (SELECT COUNT(*) FROM loans
                WHERE book_id = ? AND returned_on IS NULL)
        """,
        (book_id, book_id),
    )
    available = cursor.fetchone()[0]
    if available is None:
        raise LibraryError(f"no book with id {book_id}")
    return available


def borrow_book(
    conn: sqlite3.Connection,
    book_id: int,
    member_id: int,
    borrowed_on: str,
    due_on: str,
) -> int:
    """Create a loan and return its id. Refuse when no copies are free.

    The availability check and the insert run inside one transaction —
    ``with conn:`` — so a crash between them cannot leave a half-borrowed
    book behind.
    """
    with conn:
        if available_copies(conn, book_id) <= 0:
            title = conn.execute(
                "SELECT title FROM books WHERE id = ?", (book_id,)
            ).fetchone()[0]
            raise LibraryError(f"no copies of '{title}' available")
        cursor = conn.execute(
            "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) "
            "VALUES (?, ?, ?, ?)",
            (book_id, member_id, borrowed_on, due_on),
        )
    return cursor.lastrowid


def return_book(conn: sqlite3.Connection, loan_id: int, returned_on: str) -> None:
    """Close a loan by stamping its return date."""
    with conn:
        cursor = conn.execute(
            "UPDATE loans SET returned_on = ? "
            "WHERE id = ? AND returned_on IS NULL",
            (returned_on, loan_id),
        )
    if cursor.rowcount == 0:
        raise LibraryError(f"no open loan with id {loan_id}")


def members_with_loans(conn: sqlite3.Connection) -> list[tuple[str, str | None]]:
    """Return (member name, borrowed title or None), every member included.

    LEFT JOIN keeps members with nothing out — their title comes back NULL.
    """
    cursor = conn.execute(
        """
        SELECT m.name, b.title
        FROM members AS m
        LEFT JOIN loans AS l ON l.member_id = m.id AND l.returned_on IS NULL
        LEFT JOIN books AS b ON b.id = l.book_id
        ORDER BY m.name, b.title
        """
    )
    return cursor.fetchall()


def most_popular(conn: sqlite3.Connection, month: str) -> list[tuple[str, int]]:
    """Return (title, loan count) for a month like '2026-04', busiest first."""
    cursor = conn.execute(
        """
        SELECT b.title, COUNT(*) AS loan_count
        FROM loans AS l
        INNER JOIN books AS b ON b.id = l.book_id
        WHERE l.borrowed_on LIKE ? || '-%'
        GROUP BY b.id
        ORDER BY loan_count DESC, b.title
        """,
        (month,),
    )
    return cursor.fetchall()


def main() -> None:
    """Walk the six required features against fixed demo data."""
    conn = connect()
    try:
        init_db(conn)
        print("Library open (in-memory database for this demo).")

        automate = add_book(
            conn, "Automate the Boring Stuff", "Al Sweigart", "978-1593279929", 2
        )
        think = add_book(
            conn, "Think Python", "Allen B. Downey", "978-1491939369", 1
        )
        add_book(
            conn, "The Pragmatic Programmer", "David Thomas", "978-0135957059", 1
        )
        priya = register_member(conn, "Priya Raman", "priya@example.com", "2026-01-10")
        marcus = register_member(conn, "Marcus Webb", "marcus@example.com", "2026-02-01")
        anaya = register_member(conn, "Anaya Torres", "anaya@example.com", "2026-03-15")
        print("Catalogued 3 books; registered 3 members.")

        print("\n-- Borrowing --")
        loan_1 = borrow_book(conn, automate, priya, "2026-04-02", "2026-04-16")
        print(f"loan {loan_1}: Priya Raman borrowed 'Automate the Boring Stuff'")
        loan_2 = borrow_book(conn, automate, marcus, "2026-04-03", "2026-04-17")
        print(f"loan {loan_2}: Marcus Webb borrowed 'Automate the Boring Stuff'")
        try:
            borrow_book(conn, automate, anaya, "2026-04-04", "2026-04-18")
        except LibraryError as exc:
            print(f"rejected: {exc}")
        loan_3 = borrow_book(conn, think, anaya, "2026-04-04", "2026-04-18")
        print(f"loan {loan_3}: Anaya Torres borrowed 'Think Python'")

        print("\n-- Returning --")
        return_book(conn, loan_2, "2026-04-10")
        print(f"loan {loan_2} returned on 2026-04-10; a copy is free again")
        loan_4 = borrow_book(conn, automate, anaya, "2026-04-11", "2026-04-25")
        print(f"loan {loan_4}: Anaya Torres borrowed 'Automate the Boring Stuff'")

        print("\n-- Who has what (LEFT JOIN keeps everyone) --")
        for name, title in members_with_loans(conn):
            print(f"  {name:<13} {title if title else '(no books out)'}")

        print("\n-- Most borrowed in 2026-04 --")
        for title, count in most_popular(conn, "2026-04"):
            noun = "loan" if count == 1 else "loans"
            print(f"  {count} {noun:<6} {title}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
