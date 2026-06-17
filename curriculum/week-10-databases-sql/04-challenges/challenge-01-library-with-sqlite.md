# Challenge 01 — Library Management with SQLite

In Week 7 you built a library system using object-oriented Python. Books, Members, and Loans lived in memory and were persisted to JSON. That works for a hobby project — but the moment two people try to use the library at the same time, the JSON file becomes a problem. Time to upgrade to a real database.

## Goal

Take your Week 7 library system and re-implement its persistence layer using **SQLite**, via the standard-library `sqlite3` module. The public API of your `Library`, `Book`, and `Member` classes can stay roughly the same — you're swapping out the storage, not redesigning the system.

## Requirements

### Schema

Design a minimum of three tables:

- `books` — `id`, `title`, `author`, `isbn`, `total_copies`.
- `members` — `id`, `name`, `email`, `joined_on`.
- `loans` — `id`, `book_id` (FK), `member_id` (FK), `borrowed_on`, `due_on`, `returned_on` (nullable).

Foreign keys must be declared **and** enforced (`PRAGMA foreign_keys = ON`).

Save your schema as `schema.sql` in your repo. Your Python code should be able to bootstrap a fresh database from it on first run.

### Required features

1. **Add a book** — insert a row into `books`.
2. **Register a member** — insert a row into `members`.
3. **Borrow a book** — create a row in `loans`. Reject if the book has no available copies (compute "available" as `total_copies - active_loans`).
4. **Return a book** — update the matching `loans` row, setting `returned_on`.
5. **List members with their currently borrowed books** — use a JOIN between `members`, `loans`, and `books`. Members with no active loans must still appear (LEFT JOIN).
6. **Report: most popular book this month** — `GROUP BY book_id` over `loans`, sorted by count.

### Non-negotiables

- **Every value** that goes into SQL must be passed as a parameter. Zero f-strings into SQL.
- Use transactions for any multi-statement operation (e.g., borrowing a book and decrementing available stock if you choose to track it explicitly).
- Sensible indexes: at minimum, index `loans(book_id)` and `loans(member_id)`.
- The schema migration / bootstrap must be idempotent — running the app twice cannot crash.

### Suggested project structure

```
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

The point of the `repository.py` split is that **everything that touches SQL is in one file**. That makes it easy to audit for injection bugs and easy to swap implementations later.

## Sample SQL to get you started

```sql
CREATE TABLE IF NOT EXISTS books (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT    NOT NULL,
    author        TEXT    NOT NULL,
    isbn          TEXT    UNIQUE,
    total_copies  INTEGER NOT NULL CHECK (total_copies >= 0)
);

CREATE INDEX IF NOT EXISTS idx_loans_book_id   ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans(member_id);
```

And a parameterized "borrow" outline:

```python
def borrow_book(conn: sqlite3.Connection, book_id: int, member_id: int, due_on: str) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT (SELECT total_copies FROM books WHERE id = ?)
             - (SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned_on IS NULL)
        """,
        (book_id, book_id),
    )
    available: int = cursor.fetchone()[0]
    if available <= 0:
        raise RuntimeError("No copies available")
    cursor.execute(
        "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) VALUES (?, ?, DATE('now'), ?)",
        (book_id, member_id, due_on),
    )
    return cursor.lastrowid
```

## Stretch goals

- Add a reservations system: members can put a book on hold, then a returned copy is auto-assigned to the first reservation in line.
- Add late-fee calculation: a query that computes overdue days per active loan.
- Migrate the schema to add a `category` column to `books` without losing data. (Write the `ALTER TABLE` and the small data-migration script.)
- Use `EXPLAIN QUERY PLAN` to confirm your indexes are being used; document one query before/after.

## Rubric (out of 100)

| Area                                    | Points |
|-----------------------------------------|--------|
| Correct schema + foreign keys enforced  | 20     |
| All 6 required features work end-to-end | 30     |
| Parameterized queries everywhere        | 15     |
| Transactions used where appropriate     | 10     |
| Sensible repository / module structure  | 10     |
| README + how-to-run instructions        | 5      |
| Tests (at least three)                  | 10     |

A submission that uses an f-string anywhere inside a SQL statement loses **all** "parameterized queries" points and is flagged in code review.
