# Challenge 01 — Library Management with SQLite

> **Topic:** porting a JSON-backed system onto a real database — schema, foreign keys, `?` placeholders, transactions, a LEFT JOIN, and a GROUP BY report
> **Lecture:** [01 — Relational Databases & SQL](../lecture-notes/01-relational-databases-and-sql.md) · [02 — JOINs and Aggregations](../lecture-notes/02-joins-and-aggregations.md) · [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md)
> **Difficulty:** Intermediate
> **Target time:** 3–5 hours
> **Why this one:** you already know what a library system does — Week 7 made you build one. That is exactly why it is the right thing to rebuild. Nothing about the *problem* is new, so every hour you spend goes into the storage layer, which is the only part that changed. And the habit this page drills — every value into SQL through a placeholder, no exceptions — is the one that protects the users of everything you ship after this week.

## The Brief

In Week 7 your library was made of Python objects. `Book`, `Member` and
`Loan` sat in a list in memory, and when the program ended you dumped the
whole lot into a JSON file.

Think of that JSON file as a whiteboard. One person writing on it is fine.
Two people writing on it at the same time is a disaster, because to change
one book you have to rub out the whole board and write it all again. The
second person to finish erases everything the first one did. There is no
way to change one line of a JSON file. There is only rewriting all of it.

A database is not a whiteboard. It is a librarian. You ask for one thing,
the librarian does that one thing, in ink, and notes it in a ledger. Two
people can ask at once and the librarian keeps them in order. Nothing else
gets rewritten just because one thing changed.

Your job is to keep the library and replace the floor under it. Same books,
same members, same loans, the same six things the system could always do —
but stored in SQLite, through Python's standard-library `sqlite3` module.
The public shape of your code barely moves. You are swapping the storage,
not redesigning the system.

One rule sits above all the others, and it is the reason this challenge
exists. **Every value that goes into a SQL statement goes in through a `?`
placeholder.** Never an f-string. Never a `+`. Never `.format()`. The
Constraints section says plainly what it costs when someone gets that
wrong, and it is not a style point.

## Starter

Save this as `library.py`, in a folder of its own — it is about to create a
database file beside itself.

Do **not** name your file `challenge-01-library-with-sqlite-solution.py`.
That name belongs to the finished answer at the bottom of this page. Yours
is `library.py`, so the two can sit in the same folder without one eating
the other.

It runs as pasted. It will create `library.db` with a single `books` table
in it and then tell you how much is left to do.

```python
"""library.py — the Week 7 library, rebuilt on SQLite. Stubs to fill in."""

import sqlite3
from typing import Final

# TODO: add `members` and `loans` here, then the two indexes.
#
# members: id, name, email (UNIQUE), joined_on
# loans:   id, book_id REFERENCES books(id), member_id REFERENCES members(id),
#          borrowed_on, due_on, returned_on
#
# `returned_on` is allowed to be NULL, and that is the whole trick of this
# challenge: NULL means "this book is still out".
SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    author       TEXT    NOT NULL,
    isbn         TEXT    UNIQUE,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0)
);
"""


class LibraryError(Exception):
    """Raised when a library rule refuses an operation."""


def connect(path: str = "library.db") -> sqlite3.Connection:
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
    # TODO: one INSERT, four `?` placeholders, return cursor.lastrowid.
    raise NotImplementedError


def register_member(
    conn: sqlite3.Connection, name: str, email: str, joined_on: str
) -> int:
    """Insert a member and return their id."""
    # TODO: same shape as add_book.
    raise NotImplementedError


def available_copies(conn: sqlite3.Connection, book_id: int) -> int:
    """Return total copies minus the loans that have not come back."""
    # TODO: one SELECT. total_copies for this book, minus a COUNT of the
    # loans for this book where returned_on IS NULL.
    raise NotImplementedError


def borrow_book(
    conn: sqlite3.Connection,
    book_id: int,
    member_id: int,
    borrowed_on: str,
    due_on: str,
) -> int:
    """Create a loan and return its id. Refuse when no copies are free."""
    # TODO: inside one `with conn:` block — check availability, raise
    # LibraryError if it is zero, otherwise INSERT the loan.
    raise NotImplementedError


def return_book(conn: sqlite3.Connection, loan_id: int, returned_on: str) -> None:
    """Close a loan by stamping its return date."""
    # TODO: UPDATE the loan WHERE id = ? AND returned_on IS NULL.
    # If cursor.rowcount is 0, nothing matched — raise LibraryError.
    raise NotImplementedError


def members_with_loans(conn: sqlite3.Connection) -> list[tuple[str, str | None]]:
    """Return (member name, borrowed title or None), every member included."""
    # TODO: LEFT JOIN loans, LEFT JOIN books. Members holding nothing must
    # still appear, with None where the title would be.
    raise NotImplementedError


def most_popular(conn: sqlite3.Connection, month: str) -> list[tuple[str, int]]:
    """Return (title, loan count) for a month like '2026-04', busiest first."""
    # TODO: GROUP BY the book, COUNT the loans, ORDER BY that count.
    raise NotImplementedError


def main() -> None:
    conn = connect()
    try:
        init_db(conn)
        print("Database ready. Six features to go.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

**Where this goes when it grows.** One file is the right size to start and
the wrong size to finish. As the features land, split it:

```text
library/
├── schema.sql
├── library/
│   ├── __init__.py
│   ├── db.py                 # connection helper, context managers
│   ├── models.py             # Book, Member, Loan dataclasses
│   ├── repository.py         # all SQL lives here
│   └── cli.py                # thin command-line interface
├── tests/
│   └── test_repository.py
└── README.md
```

The point of the `repository.py` split is that **everything touching SQL is
in one file**. To audit the whole system for injection bugs you then read
one file, not twelve. It also means the day you move to PostgreSQL, you
rewrite one file.

## Requirements

Your library must:

1. Create three tables — `books` (`id`, `title`, `author`, `isbn`,
   `total_copies`), `members` (`id`, `name`, `email`, `joined_on`), and
   `loans` (`id`, `book_id`, `member_id`, `borrowed_on`, `due_on`,
   `returned_on`, which is nullable).
2. Declare the two foreign keys on `loans` **and** enforce them with
   `PRAGMA foreign_keys = ON`.
3. Keep the schema in a `schema.sql` file in your repo, and bootstrap a
   fresh database from it on first run.
4. **Add a book** — insert a row into `books`, return the new id.
5. **Register a member** — insert a row into `members`, return the new id.
6. **Borrow a book** — create a row in `loans`. Refuse when the book has no
   free copies, where "free" is `total_copies` minus the loans with
   `returned_on IS NULL`.
7. **Return a book** — update the matching `loans` row, setting
   `returned_on`. A loan that is already back, or does not exist, is an
   error, not a silent no-op.
8. **List members with what they have out** — a JOIN across `members`,
   `loans` and `books`. Members holding nothing must still appear, which
   means LEFT JOIN.
9. **Report the most borrowed book of a month** — `GROUP BY` the book over
   `loans`, sorted by the count.
10. Index `loans(book_id)` and `loans(member_id)`.

## Constraints

Every bound here has a reason, and the reason is the point.

- **Every value goes into SQL through a `?` placeholder.** Zero f-strings,
  zero `+`, zero `%`, zero `.format()` inside a SQL string. Here is what it
  costs when you get it wrong. Build the lookup as
  `f"SELECT * FROM members WHERE name = '{name}'"` and it works all day —
  until someone types a name with an apostrophe in it, like O'Brien, and
  the statement falls apart with a syntax error. That is the *lucky*
  version, because it is loud. The unlucky version is someone typing
  `' OR '1'='1` into the same box and quietly walking off with every row in
  the table, or typing `'; DROP TABLE members; --` and taking the table
  with them. Same hole, same day, different visitor. With a `?`, the
  apostrophe is just a character in a name and the attack is just a very
  odd name that nobody has.
- **A `?` stands for a value, never for a table or a column name.**
  `SELECT * FROM ?` is a syntax error, and `ORDER BY ?` is worse — it runs,
  sorts by nothing, and hands you a wrong answer with a straight face. If a
  user must choose a sort column, check what they typed against a list of
  allowed names you wrote yourself, then paste the name you chose, not the
  one they sent.
- **Anything that is more than one statement runs inside one transaction.**
  Borrowing is a check *and* an insert. If the program dies between them —
  power cut, exception, a stray `Ctrl-C` — you want both or neither, never
  a half-borrowed book. `with conn:` gives you exactly that.
- **`PRAGMA foreign_keys = ON` goes on every connection you open.** SQLite
  reads `REFERENCES` in your schema and then, by default, ignores it. The
  pragma is per connection, not per database, so setting it once in the
  `sqlite3` shell proves nothing about your program.
- **Bootstrapping must be idempotent** — a fancy word for "running it twice
  is safe". Use `CREATE TABLE IF NOT EXISTS`. A program that crashes on its
  second start is a program nobody can deploy.
- **The `.db` file never gets committed.** Add `*.db` to `.gitignore`.
  It is a build artefact, it is binary, and git cannot merge it.

## Expected output

A real run of the shipped answer, captured on CPython 3.13.2:

```bash
cd challenges
python challenge-01-library-with-sqlite-solution.py
```

```text
Library open (in-memory database for this demo).
Catalogued 3 books; registered 3 members.

-- Borrowing --
loan 1: Priya Raman borrowed 'Automate the Boring Stuff'
loan 2: Marcus Webb borrowed 'Automate the Boring Stuff'
rejected: no copies of 'Automate the Boring Stuff' available
loan 3: Anaya Torres borrowed 'Think Python'

-- Returning --
loan 2 returned on 2026-04-10; a copy is free again
loan 4: Anaya Torres borrowed 'Automate the Boring Stuff'

-- Who has what (LEFT JOIN keeps everyone) --
  Anaya Torres  Automate the Boring Stuff
  Anaya Torres  Think Python
  Marcus Webb   (no books out)
  Priya Raman   Automate the Boring Stuff

-- Most borrowed in 2026-04 --
  3 loans  Automate the Boring Stuff
  1 loan   Think Python
```

Your own build prints whatever your `main()` prints — the numbers are what
must agree. Three copies of one popular book exist across the month, one
member is holding two books at once, one member is holding nothing and
still shows up in the list, and one borrow attempt was refused.

## Steps

1. Make the folder, paste the starter into `library.py`, run it. Then look
   at what it made: `sqlite3 library.db ".schema"` prints the `books` table
   and nothing else. That gap is your to-do list.
2. Finish the schema. Add `members` and `loans` to the `SCHEMA` string, then
   the two indexes at the bottom. Run the file again — `IF NOT EXISTS`
   means the second run is quiet, and that is requirement 3 working.
3. Move the SQL out to `schema.sql` and load it with
   `Path("schema.sql").read_text(encoding="utf-8")`. Now the schema is
   readable by a human who does not speak Python, which includes future you
   at 2am.
4. Write `add_book` and `register_member`. Four `?` and three `?`. Return
   `cursor.lastrowid` — the id SQLite just assigned. Check your work in the
   shell: `sqlite3 library.db "SELECT * FROM books;"`.
5. Write `available_copies` as one SELECT with two subqueries: the book's
   `total_copies`, minus a `COUNT(*)` of its loans where
   `returned_on IS NULL`. Nothing is stored. It is counted, every time.
6. Write `borrow_book`. Open `with conn:`, ask `available_copies`, raise
   `LibraryError` if it is zero or less, otherwise INSERT. Test the refusal
   on purpose: borrow a one-copy book twice.
7. Write `return_book`. `UPDATE loans SET returned_on = ? WHERE id = ? AND
   returned_on IS NULL`. Then check `cursor.rowcount` — zero means nothing
   matched, so the loan id was wrong or the book was already back. Borrow
   the same book again afterwards and watch it succeed, because a copy is
   free now.
8. Write `members_with_loans` with LEFT JOIN, and test it with a member who
   has nothing out. If that member disappears from the results, read the
   Common bugs section — the fix is a two-word move, and it is the single
   most common JOIN mistake there is.
9. Write `most_popular`. `INNER JOIN` this time, because a book nobody
   borrowed has nothing to report. `GROUP BY` the book, `COUNT(*)` the
   loans, `ORDER BY` that count descending.
10. Add the indexes if you have not, then prove they are doing something:
    `EXPLAIN QUERY PLAN SELECT * FROM loans WHERE book_id = 1;` should
    mention `USING INDEX`, not `SCAN loans`.
11. Try to break it. Add a book whose title is `O'Brien's Big Book`. Add
    one called `'; DROP TABLE books; --`. Both should store cleanly and
    read back exactly as typed. If either one throws a syntax error, you
    have an f-string somewhere and you have just found it the friendly way.

## The Solution

```python
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
```

**Every value rides in on a `?`, and that is not a shortcut for quoting.**
When you call `conn.execute(sql, values)`, SQLite compiles the SQL text
first, on its own, with `?` standing in for "a value goes here". Only then
are your values attached to the finished statement. The value arrives after
the sentence is already built, so it cannot change the sentence. A book
titled `'; DROP TABLE books; --` gets stored as a book title — a silly one,
but a title — because by the time it arrives there is no longer any SQL
left to alter. This is also why it is *faster*: the same compiled statement
gets reused with different values.

**`with conn:` is a transaction, not a file.** On the way out it commits;
if an exception escapes the block, it rolls back instead. It does not close
the connection — that is why `main` still has `finally: conn.close()`. In
`borrow_book`, the availability check and the INSERT sit inside one such
block on purpose: they are one decision, so they succeed together or vanish
together. Two people asking for the last copy at the same moment is exactly
the case a whiteboard cannot survive.

**Availability is counted, never stored.** There is no `copies_out` column.
`available_copies` subtracts a live `COUNT(*)` of the open loans from
`total_copies`, every time it is asked. A stored counter would be a second
place where the truth lives, and every crash, every missed update, every
half-finished transaction is a chance for the two to disagree. Then you
have a number nobody believes. Counting is a little slower and always
right.

**`returned_on IS NULL` is the entire loan lifecycle.** A loan with a date
in that column came back. A loan with NULL is still out. There is no
`is_returned` flag to keep in step with the date, because the date already
knows. Note it is `IS NULL`, not `= NULL` — in SQL, NULL is not equal to
anything, including itself, so `= NULL` matches nothing, ever, quietly.

**In `members_with_loans`, the loan filter lives in the `ON` clause, not in
`WHERE`.** Look closely: `LEFT JOIN loans AS l ON l.member_id = m.id AND
l.returned_on IS NULL`. A LEFT JOIN promises to keep every member, filling
in NULLs where there is no matching loan. Move that `AND` down into a
`WHERE` and the promise is broken — `WHERE` runs *after* the join and
throws away the NULL rows the LEFT JOIN just created, so every member
holding nothing disappears. Same words, different place, opposite meaning.

**`WHERE l.borrowed_on LIKE ? || '-%'` keeps the month a value.** The `||`
is SQL's string glue, and it runs inside the database, joining your month
to the wildcard *after* the statement is compiled. The tempting version,
`f"LIKE '{month}-%'"`, would put user text back into the SQL text and undo
the whole lesson. Dates are stored as `TEXT` in `YYYY-MM-DD` form for
exactly this reason: it sorts correctly as plain text, and `2026-04` is a
prefix of every day in April.

**`cursor.rowcount` is how `return_book` knows nothing happened.** An
UPDATE that matches no rows is not an error to SQLite — it did what it was
asked, which was nothing. `rowcount == 0` means the loan id was wrong or
the book was already back, and turning that silence into a `LibraryError`
is the difference between a system that tells you and a system that
shrugs.

**The download runs on `:memory:`.** Passing `":memory:"` to
`sqlite3.connect` builds the whole database in RAM: no file, no collision
with your `library.db`, nothing left behind when it exits. Change that one
argument to a path and the identical code runs a real library. And the
schema is inlined in the file only so the download is a single file — in
your repo it belongs in `schema.sql`, as requirement 3 says.

## Download and run

Download
[challenge-01-library-with-sqlite-solution.py](./challenge-01-library-with-sqlite-solution.py)
and run it:

```bash
python challenge-01-library-with-sqlite-solution.py
```

It needs nothing installed — `sqlite3` ships with Python — and it exits on
its own. It writes no files, because the database lives in memory.

The `-solution` in the filename is what keeps it from colliding with your
own `library.py`.

## Common bugs to catch

- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The
  current statement uses 1, and there are 12 supplied.`** You passed
  `("Think Python")` where a tuple was wanted. Parentheses do not make a
  tuple in Python — the comma does. Without it you handed sqlite3 a
  12-character string, and it counted 12 bindings. Write
  `("Think Python",)`. The lonely trailing comma looks like a typo and is
  not.

- **`sqlite3.OperationalError: near "Brien": syntax error`** You built the
  statement with an f-string and someone's title contains an apostrophe —
  `O'Brien's Big Book`. The quote closed your string early and SQLite tried
  to read the rest as SQL. Do not reach for `.replace("'", "''")`. Reach
  for `?`. This crash is the friendly face of a hole that has a very
  unfriendly one.

- **Foreign keys never complain, no matter what you insert.** No exception,
  no message, loans pointing at book 9999. You declared `REFERENCES` but
  never ran `PRAGMA foreign_keys = ON` on *this* connection. The pragma is
  per connection and defaults to off, so a connection helper that forgets
  it silently disables every foreign key in your schema.

- **`sqlite3.IntegrityError: FOREIGN KEY constraint failed`** The good
  version of the bug above — the pragma is on and it is doing its job. You
  are inserting a loan for a `book_id` or `member_id` that does not exist.
  Check the id you passed; a common cause is using the loan id where the
  book id belongs.

- **`sqlite3.OperationalError: no such table: loans`** Either `init_db` was
  never called, or you started Python from a different folder.
  `sqlite3.connect("library.db")` creates the file when it is missing and
  says nothing about it, so a typo in the path or a run from the wrong
  directory gives you a brand-new empty database rather than an error.

- **Everything works, then a restart and the data is gone.** You never
  committed. Writes live in an open transaction until `conn.commit()` — or
  the end of a `with conn:` block — makes them permanent. Closing without
  committing throws them away.

- **`sqlite3.ProgrammingError: You can only execute one statement at a
  time.`** You handed the whole multi-table schema to `execute`. That
  method runs exactly one statement, on purpose, and that limit is a real
  safety feature: it is why an injected `'; DROP TABLE books; --` cannot
  run a second statement even when the SQL was built badly. For your own
  schema, use `executescript`.

- **`sqlite3.OperationalError: near "?": syntax error`** You wrote
  `SELECT * FROM ?` or `SELECT ? FROM books`. A placeholder stands for a
  value. Table and column names are part of the sentence, not part of the
  data, and they have to be in the string when it is compiled.

- **`ORDER BY ?` runs, and sorts nothing.** No error at all. You passed the
  column name as a parameter, so SQLite sorted every row by the same
  constant string and left them in whatever order it found them. A wrong
  answer with no exception is the worst kind. Whitelist the column name
  instead.

- **Members holding no books vanish from the list.** Your
  `AND l.returned_on IS NULL` is in the `WHERE` clause. `WHERE` filters
  after the join, so it deletes exactly the NULL rows your LEFT JOIN made
  for members with nothing out. Move that condition up into the `ON`.

- **`sqlite3.IntegrityError: UNIQUE constraint failed: books.isbn`** You
  added the same ISBN twice. That is the constraint working. Decide what
  the library should do — refuse, or bump `total_copies` on the row that is
  already there — and write it down as a rule.

## Under the hood

<details>
<summary>Under the hood — what a `?` actually does, and why it is not escaping</summary>

It is tempting to imagine `?` as an automatic quote-doubler that runs over
your value and makes it safe. It is not, and the difference matters.

`conn.execute(sql, params)` does two separate things. First it *prepares*
the statement: SQLite parses the SQL text and compiles it into a small
program of bytecode operations, with each `?` becoming an instruction that
says "read parameter 1 from the register". At that instant the shape of the
statement is finished and frozen. Second, it *binds* your values into those
registers and runs the program.

Your value therefore never passes through the parser. It is not text being
made safe; it is data arriving on a different road entirely, after the road
for SQL text has closed. That is why the guarantee is total rather than
best-effort: there is no clever quoting you can invent that reaches the
parser, because the parser already finished.

Two useful consequences fall out of that. The prepared statement can be
reused with new values without re-parsing, which is why parameterised
queries in a loop are faster than string-built ones. And the parameters are
typed — bind a Python `int` and SQLite stores an integer, not the
characters of one.

The named form is worth knowing for statements with many values, where
counting question marks stops being fun:

```python
conn.execute(
    "INSERT INTO books (title, author, isbn, total_copies) "
    "VALUES (:title, :author, :isbn, :copies)",
    {"title": "Think Python", "author": "Allen B. Downey",
     "isbn": "978-1491939369", "copies": 1},
)
```

Same mechanism, same guarantee, friendlier to read.

</details>

<details>
<summary>Under the hood — why SQLite ignores foreign keys unless you ask</summary>

Every other database enforces foreign keys by default. SQLite makes you
turn them on, once per connection, which feels like a trap and is really a
promise being kept.

SQLite shipped in 2000 without foreign key enforcement. Support arrived in
version 3.6.19, in 2009, by which time an enormous amount of software was
already running on it — SQLite is in phones, browsers, aeroplanes and your
operating system, and there are more SQLite databases in the world than any
other kind. Some of that software had data that quietly violated its own
declared foreign keys. Turning enforcement on by default would have broken
those programs on an upgrade they never asked for.

So the default stayed off, and the project's compatibility promise held.
The cost is one line in your connection helper, forever:

```python
conn.execute("PRAGMA foreign_keys = ON")
```

Three details worth carrying: it is per connection, so every new connection
starts off again. It cannot be changed in the middle of a transaction — the
statement is silently ignored there, which is its own small trap. And
turning it on later does not check the rows already in the table; it only
guards what happens from now on.

</details>

<details>
<summary>Under the hood — what `with conn:` commits, and what it will not</summary>

`with conn:` is `sqlite3.Connection` used as a context manager, and it does
exactly one thing: commit on a clean exit, roll back if an exception
escapes. It does not open the connection, and it does not close it. Nesting
two of them does not give you nested transactions — the inner one commits
everything outstanding, including the outer one's work.

By default the module runs in a legacy mode where it starts a transaction
for you before an INSERT, UPDATE or DELETE, but not before a SELECT, and —
in older Pythons — not before DDL like `CREATE TABLE` either. That "helpful"
behaviour has surprised people for twenty years, so modern Python offers an
explicit alternative:

```python
conn = sqlite3.connect("library.db", autocommit=False)
```

Python 3.12 added `autocommit`, and setting it to `False` gives the
standard DB-API behaviour: a transaction is open at all times, and nothing
is permanent until you say so. The old default, `isolation_level=""`, still
works and is what this solution relies on.

The rule that survives every version: if two statements have to be true
together, put them in one `with conn:` block, and do not let a `SELECT` you
based a decision on drift outside it.

</details>

<details>
<summary>Under the hood — the number you store versus the number you count</summary>

Storing an `available_copies` column looks obviously better. It is one
read instead of a count, and the count gets slower as the loan table grows.

It is also how systems start lying. The moment the number is stored, there
are two answers to "how many copies are free": the column, and the truth
you could recompute from `loans`. They agree only as long as every single
code path that touches a loan also touches the column, forever, including
the ones written by someone in a hurry two years from now. One missed
update and the library refuses to lend a book that is sitting on the shelf.

Database people call the safe version *normalised*: each fact is stored in
exactly one place. Deliberately storing a fact twice for speed is
*denormalisation*, and it is a legitimate move — but the price is that you
now own the job of keeping the copies in step, and you should only pay it
once you have measured that counting is actually too slow.

When that day comes, the honest ways to buy the speed back are, in order: an
index on `loans(book_id)` so the count reads only the rows it needs; a
`VIEW` that computes availability so every caller shares one definition; or,
if you truly must cache the number, a `TRIGGER` that updates it inside the
same transaction as the loan, so the two cannot drift even if a caller
forgets.

</details>

<details>
<summary>Under the hood — what an index costs, and how to prove it is earning it</summary>

An index is the thing at the back of a textbook. Without it, finding every
mention of "photosynthesis" means reading all 600 pages. With it, you look
up one word and jump straight to the pages.

SQLite builds that index as a B-tree: a wide, shallow, always-sorted tree
where finding a value takes a number of steps proportional to the
*logarithm* of the table size. Doubling the loans in your library adds one
step, not twice the work.

The cost is real and is paid on writes. Every INSERT into `loans` now
writes the row *and* updates two index trees, so the table takes more disk
and every write is a little slower. An index on a column nobody searches by
is pure loss. This is why you index `loans(book_id)` and
`loans(member_id)` — the two columns every JOIN and every count in this
challenge filters on — and not `borrowed_on`, which is only ever scanned as
a whole month.

Ask the database rather than guessing:

```sql
EXPLAIN QUERY PLAN SELECT * FROM loans WHERE book_id = 1;
```

`SEARCH loans USING INDEX idx_loans_book_id (book_id=?)` means the index is
being used. `SCAN loans` means every row is being read and the index is
either missing or unusable for that query. Run it before and after adding
an index and keep both outputs — that comparison is one of the stretch
goals, and it is the only way to know rather than hope.

</details>

## Acceptance checklist

- [ ] `sqlite3 library.db ".schema"` shows all three tables and both indexes.
- [ ] Running your program twice in a row does not crash the second time.
- [ ] Borrowing the only copy of a one-copy book twice is refused the second time, with a message naming the book.
- [ ] Returning that book and borrowing it again succeeds.
- [ ] Returning the same loan twice raises an error rather than doing nothing quietly.
- [ ] A member with nothing borrowed still appears in the "who has what" list.
- [ ] The monthly report counts a book that was borrowed, returned, and borrowed again as two loans.
- [ ] Inserting a loan for a book id that does not exist raises `sqlite3.IntegrityError: FOREIGN KEY constraint failed`.
- [ ] A book titled `O'Brien's Big Book` stores and reads back exactly as typed.
- [ ] Searching your whole repository for f-strings turns up none inside a SQL statement — not one.
- [ ] `EXPLAIN QUERY PLAN` on a loan lookup by `book_id` says `USING INDEX`.
- [ ] `*.db` is in `.gitignore` and no database file is committed.
- [ ] At least three tests, each one against a throwaway database.

How it is graded, out of 100:

| Area                                    | Points |
|-----------------------------------------|--------|
| Correct schema + foreign keys enforced  | 20     |
| All 6 required features work end-to-end | 30     |
| Parameterized queries everywhere        | 15     |
| Transactions used where appropriate     | 10     |
| Sensible repository / module structure  | 10     |
| README + how-to-run instructions        | 5      |
| Tests (at least three)                  | 10     |

A submission with an f-string anywhere inside a SQL statement loses **all**
of the "parameterized queries" points and is flagged in code review. That is
harsh on purpose. It is the one mistake on this page that hurts somebody
other than you.

## Stretch

- Add reservations: a member can put a book on hold, and when a copy comes
  back it is assigned to the first person in the queue. The interesting part
  is not the table — it is deciding what happens when the first person in
  line has since borrowed the book anyway.
- Add late fees: a query that computes overdue days per open loan, using
  `julianday('now') - julianday(due_on)`.
- Add a `category` column to `books` without losing the data already there.
  Write the `ALTER TABLE`, and a small migration script that can tell
  whether it has already run.
- Use `EXPLAIN QUERY PLAN` to prove one of your indexes earns its keep.
  Capture the plan before and after creating the index and put both in your
  README.
- Rebuild `repository.py` on SQLAlchemy Core, keeping the same function
  signatures, and see how little of the rest of the code has to change.
  That is the payoff for putting all the SQL in one file.
- Add a `--seed` flag to the CLI that loads a few dozen books and members
  from a CSV, then time `most_popular` with and without the indexes.

References:

- Python `sqlite3` — <https://docs.python.org/3/library/sqlite3.html>
- SQLite foreign key support — <https://www.sqlite.org/foreignkeys.html>
- SQLite query planner — <https://www.sqlite.org/queryplanner.html>
- SQLite datatypes and dates — <https://www.sqlite.org/datatype3.html>
