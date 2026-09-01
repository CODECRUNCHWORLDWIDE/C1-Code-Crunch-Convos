"""Every SQL statement in this project lives in this file.

That is the entire point of the repository split. When someone asks "is this
codebase safe from SQL injection?", the answer is a five-minute read of one
file rather than a grep across the whole tree. Search this file for `f"` and
`%` and `.format(` and `+ ` inside a string: there are none.

Reading order: availability first (it defines what "available" means), then
borrow/return, then the two reports, then the stretch goals.
"""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Final

from .db import read_cursor, transaction
from .models import (
    Book,
    LibraryError,
    Loan,
    Member,
    MemberLoans,
    NoCopiesAvailable,
    NotFound,
    OverdueLoan,
    PopularBook,
)

#: One SELECT of a loan row, used by three functions. Naming it once means the
#: column list can never drift between them.
_LOAN_BY_ID_SQL: Final[str] = (
    "SELECT id, book_id, member_id, borrowed_on, due_on, returned_on "
    "FROM loans WHERE id = ?"
)

#: Default loan length, in days. Policy, not data -- so it lives in Python.
LOAN_DAYS: Final[int] = 14

#: Late fee per day, in whatever currency the library uses.
DEFAULT_FEE_PER_DAY: Final[float] = 0.25


# ---------------------------------------------------------------------------
# Feature 1 and 2: adding books and members
# ---------------------------------------------------------------------------


def add_book(
    title: str,
    author: str,
    isbn: str | None,
    total_copies: int,
    db_path: str | Path | None = None,
) -> int:
    """Insert one catalogue entry and return its id.

    `isbn` is UNIQUE in the schema, so a duplicate raises sqlite3.IntegrityError
    with "UNIQUE constraint failed: books.isbn". We translate it rather than
    letting a driver exception leak into the CLI.
    """
    with _transaction(db_path) as cur:
        try:
            cur.execute(
                "INSERT INTO books (title, author, isbn, total_copies) VALUES (?, ?, ?, ?)",
                (title, author, isbn, total_copies),
            )
        except sqlite3.IntegrityError as exc:
            raise LibraryError(f"could not add book: {exc}") from exc
        new_id = cur.lastrowid
    assert new_id is not None
    return new_id


def register_member(
    name: str,
    email: str,
    joined_on: str | None = None,
    db_path: str | Path | None = None,
) -> int:
    """Insert one member and return the new id.

    When `joined_on` is None we let the column DEFAULT (DATE('now')) fill it in
    by naming only the columns we are supplying. Passing NULL explicitly would
    *override* the default with NULL and hit the NOT NULL constraint -- a
    genuinely surprising SQLite behaviour worth meeting once on purpose.
    """
    with _transaction(db_path) as cur:
        try:
            if joined_on is None:
                cur.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
            else:
                cur.execute(
                    "INSERT INTO members (name, email, joined_on) VALUES (?, ?, ?)",
                    (name, email, joined_on),
                )
        except sqlite3.IntegrityError as exc:
            raise LibraryError(f"could not register member: {exc}") from exc
        new_id = cur.lastrowid
    assert new_id is not None
    return new_id


def get_book(book_id: int, db_path: str | Path | None = None) -> Book:
    with _read(db_path) as cur:
        cur.execute(
            "SELECT id, title, author, isbn, total_copies FROM books WHERE id = ?",
            (book_id,),
        )
        row = cur.fetchone()
    if row is None:
        raise NotFound(f"no book with id {book_id}")
    return Book.from_row(row)


def get_loan(loan_id: int, db_path: str | Path | None = None) -> Loan:
    with _read(db_path) as cur:
        cur.execute(_LOAN_BY_ID_SQL, (loan_id,))
        row = cur.fetchone()
    if row is None:
        raise NotFound(f"no loan with id {loan_id}")
    return Loan.from_row(row)


def get_member(member_id: int, db_path: str | Path | None = None) -> Member:
    with _read(db_path) as cur:
        cur.execute(
            "SELECT id, name, email, joined_on FROM members WHERE id = ?", (member_id,)
        )
        row = cur.fetchone()
    if row is None:
        raise NotFound(f"no member with id {member_id}")
    return Member.from_row(row)


# ---------------------------------------------------------------------------
# Availability -- the definition everything else depends on
# ---------------------------------------------------------------------------

#: How many copies of a book are on the shelf right now.
#:
#: We do NOT store an `available_copies` column. Storing it would mean two
#: numbers that must be kept in step by application code, and the day they
#: disagree you cannot tell which one is lying. Deriving it from the loans
#: table means it is always right by construction.
_AVAILABLE_SQL: Final[str] = """
SELECT (SELECT total_copies FROM books WHERE id = ?)
     - (SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned_on IS NULL)
       AS available
"""


def _available_on_cursor(cur: sqlite3.Cursor, book_id: int) -> int:
    """Availability, computed on a cursor the caller already owns.

    Taking a cursor rather than opening one is what lets borrow_book() check
    availability and insert the loan inside a *single* transaction. Two
    separate connections would leave a window where another process could
    borrow the last copy between the check and the insert.
    """
    cur.execute(_AVAILABLE_SQL, (book_id, book_id))
    available = cur.fetchone()["available"]
    if available is None:          # the book subquery returned no row
        raise NotFound(f"no book with id {book_id}")
    return int(available)


def available_copies(book_id: int, db_path: str | Path | None = None) -> int:
    with _read(db_path) as cur:
        return _available_on_cursor(cur, book_id)


# ---------------------------------------------------------------------------
# Feature 3 and 4: borrow and return
# ---------------------------------------------------------------------------


def borrow_book(
    book_id: int,
    member_id: int,
    due_on: str | None = None,
    borrowed_on: str | None = None,
    db_path: str | Path | None = None,
) -> int:
    """Create a loan, or refuse because every copy is out.

    Check-then-insert is only correct because both statements run inside one
    transaction on one connection: SQLite takes a write lock at the INSERT and
    holds it to COMMIT, so nobody can slip a competing borrow in between.
    """
    borrowed = borrowed_on or date.today().isoformat()
    due = due_on or (date.fromisoformat(borrowed) + timedelta(days=LOAN_DAYS)).isoformat()

    with _transaction(db_path) as cur:
        if _available_on_cursor(cur, book_id) <= 0:
            raise NoCopiesAvailable(f"every copy of book {book_id} is out on loan")
        try:
            cur.execute(
                "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) "
                "VALUES (?, ?, ?, ?)",
                (book_id, member_id, borrowed, due),
            )
        except sqlite3.IntegrityError as exc:
            # FOREIGN KEY constraint failed -> the member does not exist.
            raise NotFound(f"no member with id {member_id}") from exc
        loan_id = cur.lastrowid
    assert loan_id is not None
    return loan_id


def return_book(
    loan_id: int,
    returned_on: str | None = None,
    db_path: str | Path | None = None,
) -> Loan:
    """Close one loan and hand back its final state.

    Refuses twice: once if the loan id is unknown, once if it was already
    returned. The second check is what stops a double-return from silently
    overwriting the original return date.
    """
    when = returned_on or date.today().isoformat()
    with _transaction(db_path) as cur:
        cur.execute(_LOAN_BY_ID_SQL, (loan_id,))
        row = cur.fetchone()
        if row is None:
            raise NotFound(f"no loan with id {loan_id}")
        if row["returned_on"] is not None:
            raise LibraryError(f"loan {loan_id} was already returned on {row['returned_on']}")

        cur.execute("UPDATE loans SET returned_on = ? WHERE id = ?", (when, loan_id))
        cur.execute(_LOAN_BY_ID_SQL, (loan_id,))
        return Loan.from_row(cur.fetchone())


# ---------------------------------------------------------------------------
# Feature 5: members and what they currently have out
# ---------------------------------------------------------------------------

#: The join condition `l.returned_on IS NULL` sits in the ON clause, not in a
#: WHERE clause. That is the whole trick of this query. In a LEFT JOIN, ON
#: decides which right-hand rows get attached; WHERE runs afterwards over the
#: joined result and would throw away the all-NULL rows that a LEFT JOIN
#: produces for members with nothing out -- silently turning it back into an
#: INNER JOIN, which is exactly what the requirement forbids.
_MEMBERS_WITH_LOANS_SQL: Final[str] = """
SELECT   m.id                       AS member_id,
         m.name                     AS name,
         m.email                    AS email,
         GROUP_CONCAT(b.title, '|') AS titles
FROM     members AS m
LEFT JOIN loans AS l
       ON l.member_id = m.id
      AND l.returned_on IS NULL
LEFT JOIN books AS b
       ON b.id = l.book_id
GROUP BY m.id, m.name, m.email
ORDER BY m.name
"""


def members_with_loans(db_path: str | Path | None = None) -> list[MemberLoans]:
    """Every member, each with the titles they currently hold (possibly none)."""
    with _read(db_path) as cur:
        cur.execute(_MEMBERS_WITH_LOANS_SQL)
        rows = cur.fetchall()
    return [
        MemberLoans(
            member_id=row["member_id"],
            name=row["name"],
            email=row["email"],
            # GROUP_CONCAT over an all-NULL group returns NULL, not "".
            titles=tuple(row["titles"].split("|")) if row["titles"] else (),
        )
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Feature 6: most popular book this month
# ---------------------------------------------------------------------------

_POPULAR_SQL: Final[str] = """
SELECT   b.id                AS book_id,
         b.title             AS title,
         b.author            AS author,
         COUNT(*)            AS times_borrowed
FROM     loans AS l
INNER JOIN books AS b ON b.id = l.book_id
WHERE    strftime('%Y-%m', l.borrowed_on) = ?
GROUP BY l.book_id, b.title, b.author
ORDER BY times_borrowed DESC, b.title ASC
LIMIT    ?
"""


def most_popular_this_month(
    month: str | None = None,
    limit: int = 5,
    db_path: str | Path | None = None,
) -> list[PopularBook]:
    """Books ranked by how many times they were borrowed in one calendar month.

    `month` is 'YYYY-MM' and defaults to the current month. It is passed as a
    parameter, not formatted into the SQL -- including LIMIT, which SQLite is
    happy to bind. The INNER JOIN is deliberate here: a book nobody borrowed
    has no loans row, so it has no business in a popularity ranking.
    """
    target = month or date.today().strftime("%Y-%m")
    with _read(db_path) as cur:
        cur.execute(_POPULAR_SQL, (target, limit))
        rows = cur.fetchall()
    return [
        PopularBook(
            book_id=row["book_id"],
            title=row["title"],
            author=row["author"],
            times_borrowed=row["times_borrowed"],
        )
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Stretch goal: late fees
# ---------------------------------------------------------------------------

_OVERDUE_SQL: Final[str] = """
SELECT   l.id     AS loan_id,
         b.title  AS title,
         m.name   AS member_name,
         l.due_on AS due_on,
         CAST(JULIANDAY(?) - JULIANDAY(l.due_on) AS INTEGER) AS days_overdue
FROM     loans AS l
INNER JOIN books   AS b ON b.id = l.book_id
INNER JOIN members AS m ON m.id = l.member_id
WHERE    l.returned_on IS NULL
  AND    l.due_on < ?
ORDER BY days_overdue DESC, m.name
"""


def overdue_loans(
    as_of: str | None = None,
    fee_per_day: float = DEFAULT_FEE_PER_DAY,
    db_path: str | Path | None = None,
) -> list[OverdueLoan]:
    """Active loans past their due date, with the fee each has accrued.

    JULIANDAY() converts an ISO date to a day number, so subtracting two of
    them gives a difference in days that SQLite can compute without Python
    reading a single row. The fee itself is multiplied in Python because the
    rate is policy: it changes without a schema migration.
    """
    today = as_of or date.today().isoformat()
    with _read(db_path) as cur:
        cur.execute(_OVERDUE_SQL, (today, today))
        rows = cur.fetchall()
    return [
        OverdueLoan(
            loan_id=row["loan_id"],
            title=row["title"],
            member_name=row["member_name"],
            due_on=row["due_on"],
            days_overdue=row["days_overdue"],
            fee=round(row["days_overdue"] * fee_per_day, 2),
        )
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Stretch goal: reservations
# ---------------------------------------------------------------------------


def place_reservation(
    book_id: int, member_id: int, placed_on: str | None = None,
    db_path: str | Path | None = None
) -> int:
    """Put a member in the queue for a book."""
    with _transaction(db_path) as cur:
        try:
            if placed_on is None:
                cur.execute(
                    "INSERT INTO reservations (book_id, member_id) VALUES (?, ?)",
                    (book_id, member_id),
                )
            else:
                cur.execute(
                    "INSERT INTO reservations (book_id, member_id, placed_on) "
                    "VALUES (?, ?, ?)",
                    (book_id, member_id, placed_on),
                )
        except sqlite3.IntegrityError as exc:
            raise NotFound(f"unknown book {book_id} or member {member_id}") from exc
        reservation_id = cur.lastrowid
    assert reservation_id is not None
    return reservation_id


def return_book_and_fulfil(
    loan_id: int,
    returned_on: str | None = None,
    db_path: str | Path | None = None,
) -> tuple[Loan, int | None]:
    """Return a book and hand the freed copy to the head of its queue.

    Returns (closed loan, new loan id or None). The return, the reservation
    update and the new loan are one transaction: if the new loan fails, the
    reservation is not marked fulfilled and the book is not marked returned,
    so the queue never loses a member's place.
    """
    when = returned_on or date.today().isoformat()
    with _transaction(db_path) as cur:
        cur.execute(_LOAN_BY_ID_SQL, (loan_id,))
        row = cur.fetchone()
        if row is None:
            raise NotFound(f"no loan with id {loan_id}")
        if row["returned_on"] is not None:
            raise LibraryError(f"loan {loan_id} was already returned on {row['returned_on']}")
        book_id = row["book_id"]

        cur.execute("UPDATE loans SET returned_on = ? WHERE id = ?", (when, loan_id))

        new_loan_id: int | None = None
        if _available_on_cursor(cur, book_id) > 0:
            cur.execute(
                "SELECT id, member_id FROM reservations "
                "WHERE book_id = ? AND fulfilled_on IS NULL "
                "ORDER BY placed_on, id LIMIT 1",
                (book_id,),
            )
            waiting = cur.fetchone()
            if waiting is not None:
                due = (date.fromisoformat(when) + timedelta(days=LOAN_DAYS)).isoformat()
                cur.execute(
                    "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) "
                    "VALUES (?, ?, ?, ?)",
                    (book_id, waiting["member_id"], when, due),
                )
                new_loan_id = cur.lastrowid
                cur.execute(
                    "UPDATE reservations SET fulfilled_on = ? WHERE id = ?",
                    (when, waiting["id"]),
                )

        cur.execute(_LOAN_BY_ID_SQL, (loan_id,))
        return Loan.from_row(cur.fetchone()), new_loan_id


# ---------------------------------------------------------------------------
# Stretch goal: proving the indexes are used
# ---------------------------------------------------------------------------


def explain_availability(book_id: int, db_path: str | Path | None = None) -> list[str]:
    """Return SQLite's plan for the availability query, one line per step.

    This is the one `+` on a SQL string in the project, and both operands are
    module constants -- no user value is anywhere near it. The parameters are
    still bound with `?`, because EXPLAIN QUERY PLAN needs the same bindings
    the real query would get.
    """
    with _read(db_path) as cur:
        cur.execute("EXPLAIN QUERY PLAN " + _AVAILABLE_SQL, (book_id, book_id))
        return [row["detail"] for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# Small private helpers so every function above can take an optional db_path
# ---------------------------------------------------------------------------


def _transaction(db_path: str | Path | None):
    return transaction() if db_path is None else transaction(db_path)


def _read(db_path: str | Path | None):
    return read_cursor() if db_path is None else read_cursor(db_path)
