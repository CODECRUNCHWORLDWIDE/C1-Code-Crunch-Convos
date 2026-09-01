# Reference solution — Challenge 01: Library Management with SQLite

This is a complete, running answer to
[`challenge-01-library-with-sqlite.md`](../../../../curriculum/week-10-databases-sql/challenges/challenge-01-library-with-sqlite.md).
It is the Week 7 library system with its JSON persistence layer replaced by
SQLite, using the standard-library `sqlite3` module and nothing else.

The challenge page itself carries the walkthrough — the answer, and the
reasoning behind each decision this README only states. Read it alongside the
code.

## Run it

No dependencies. Python 3.10 or newer (it uses `X | Y` type syntax and
`dataclass(slots=True)`).

```bash
cd challenge-01-library-sqlite

# The schema bootstraps itself on the first command.
python -m library.cli add-book "Dune" "Frank Herbert" --isbn 978-0441013593 --copies 2
python -m library.cli add-book "Kindred" "Octavia Butler" --isbn 978-0807083697 --copies 1
python -m library.cli add-member "Ada Lovelace" ada@example.com
python -m library.cli add-member "Alan Turing" alan@example.com

python -m library.cli borrow 2 1        # Ada takes the only copy of Kindred
python -m library.cli available 2       # -> 0
python -m library.cli borrow 2 2        # -> refused, exit code 1

python -m library.cli reserve 2 2       # Alan joins the queue
python -m library.cli return 1          # Ada returns it; Alan gets it automatically
python -m library.cli members
python -m library.cli popular
python -m library.cli overdue
python -m library.cli explain 2         # EXPLAIN QUERY PLAN for the availability query
```

The database file is `library.db` next to this README. Point the app at a
throwaway file with the `LIBRARY_DB` environment variable:

```bash
LIBRARY_DB=scratch.db python -m library.cli members
```

`.db` files are gitignored, as the challenge's submission checklist requires.

## Run the tests

```bash
python tests/test_repository.py
```

```text
ok    test_add_book_and_member
ok    test_duplicate_isbn_is_refused
ok    test_borrow_reduces_availability
ok    test_borrow_refuses_when_no_copies_left
ok    test_foreign_key_is_enforced
ok    test_return_frees_the_copy_and_refuses_twice
ok    test_members_with_loans_keeps_members_who_have_nothing_out
ok    test_returned_loans_do_not_show_as_current
ok    test_most_popular_this_month
ok    test_overdue_fees
ok    test_reservation_is_fulfilled_on_return
ok    test_injection_payload_is_stored_as_a_title

12 passed, 0 failed
```

Each test builds its own database in a temporary directory, so the suite never
touches `library.db` and tests cannot leak state into each other.

## What is where

Read the files in this order:

| File | What it holds |
|---|---|
| [`schema.sql`](./schema.sql) | Every table and index. The single source of truth for the shape of the data. |
| [`library/db.py`](./library/db.py) | Connections, `PRAGMA foreign_keys = ON`, the transaction context manager. Knows nothing about books. |
| [`library/models.py`](./library/models.py) | Frozen dataclasses — a typed shape for a row once it has been read. No SQL. |
| [`library/repository.py`](./library/repository.py) | Every SQL statement in the project. All of them. |
| [`library/cli.py`](./library/cli.py) | Argument parsing and printing. Not one `execute`. |
| [`tests/test_repository.py`](./tests/test_repository.py) | Twelve tests, one per required feature plus the interesting failures. |
| [`migrations/002_add_category.sql`](./migrations/002_add_category.sql) | Stretch goal: add `books.category_id` to a live database without losing data. |

## How it maps to the spec

| Requirement | Where |
|---|---|
| Three tables, FKs declared **and** enforced | `schema.sql` + `db.connect()` |
| `schema.sql` bootstraps a fresh DB | `db.init_db()`, called by `cli.main()` |
| 1. Add a book | `repository.add_book` |
| 2. Register a member | `repository.register_member` |
| 3. Borrow, rejecting when no copies | `repository.borrow_book` + `_available_on_cursor` |
| 4. Return a book | `repository.return_book` |
| 5. Members with current loans, LEFT JOIN | `repository.members_with_loans` |
| 6. Most popular book this month | `repository.most_popular_this_month` |
| Every value parameterized | `repository.py` — zero f-strings in SQL |
| Transactions for multi-statement work | `db.transaction`, used by borrow / return / reserve |
| Indexes on `loans(book_id)`, `loans(member_id)` | `schema.sql` |
| Idempotent bootstrap | every statement in `schema.sql` is `IF NOT EXISTS` |
| Stretch: reservations | `reservations` table + `place_reservation` / `return_book_and_fulfil` |
| Stretch: late fees | `repository.overdue_loans` |
| Stretch: category migration | `migrations/002_add_category.sql` |
| Stretch: `EXPLAIN QUERY PLAN` | `repository.explain_availability`, `cli explain` |

## The one design decision worth arguing about

There is no `available_copies` column. Availability is derived every time it is
asked for:

```sql
SELECT (SELECT total_copies FROM books WHERE id = ?)
     - (SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned_on IS NULL)
```

The alternative — a stored counter that borrow decrements and return
increments — is faster to read and one crash away from being wrong forever.
Once a stored counter drifts from the loans table there is no way to tell
which one is lying. The derived version cannot drift, and the partial index
`idx_loans_active` keeps it cheap:

```text
$ python -m library.cli explain 2
SCAN CONSTANT ROW
SCALAR SUBQUERY 1
SEARCH books USING INTEGER PRIMARY KEY (rowid=?)
SCALAR SUBQUERY 2
SEARCH loans USING INDEX idx_loans_active (book_id=?)
```

`SEARCH ... USING INDEX`, not `SCAN loans`. Drop the indexes and the last line
becomes `SCAN loans` — a full read of every loan ever made, to answer one
question about one book.
