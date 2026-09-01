# Homework Problem 2 — A Migration Script

> **Topic:** changing a database that already has data in it, atomically, without losing a single row
> **Lecture:** [01 — Relational Databases & SQL](../lecture-notes/01-relational-databases-and-sql.md) (the transactions section)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** the schema you designed in Problem 1 was for an empty database. Real databases are never empty when you need to change them — they are full of live data you cannot lose. A migration is how you change the shape of a table that already has rows in it, and wrapping it in one transaction is how you make sure a change either fully happens or does not happen at all.

## The Brief

You have a blog database with two tables already full of rows —
`users` and `posts`, the same ones from this week's exercises. The
product team wants posts sorted into categories. That means three
changes at once:

1. A new `categories` table.
2. A new `category_id` column on the existing `posts` table.
3. Some starter categories, and every old post filed under a default one.

The catch is that the database is *live*. You cannot drop `posts` and
recreate it — that throws away every post ever written. You have to
**alter** the table in place, add the column, and backfill the existing
rows, all without losing data.

The tool for "several changes that must all happen together, or none of
them" is a **transaction**: `BEGIN` starts it, `COMMIT` makes every
change permanent at once, and if anything in between fails, the whole
thing rolls back and the database is exactly as it was. Your migration
lives inside one `BEGIN`/`COMMIT`.

The deliverable is two SQL scripts: `001_initial.sql` (the starting
schema, so the demo has something to migrate) and `002_add_categories.sql`
(the migration). The Python around them plays the story out on an
in-memory database with rows already in it: state before, migrate, state
after, and a row-count proof that nothing vanished.

## Starter

Save this as `migrate_demo.py` and fill in the `TODO`s. It runs as
pasted — with an empty migration it just prints the "before" state twice.

```python
"""Migrate a live blog database to add categories, without losing a post."""

import sqlite3
from typing import Final

INITIAL_SQL: Final[str] = """
CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL UNIQUE,
    joined_on TEXT NOT NULL
);
CREATE TABLE posts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    title        TEXT    NOT NULL,
    published_on TEXT    NOT NULL
);
"""

MIGRATION_SQL: Final[str] = """
BEGIN;
-- TODO 1: CREATE TABLE categories (id, name UNIQUE)
-- TODO 2: ALTER TABLE posts ADD COLUMN category_id ... (nullable, no default)
-- TODO 3: INSERT the three starter categories: Tech, Life, Other
-- TODO 4: UPDATE posts SET category_id = the id of 'Other' WHERE category_id IS NULL
COMMIT;
"""


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.executescript(INITIAL_SQL)
        conn.executemany(
            "INSERT INTO users (username, joined_on) VALUES (?, ?)",
            [("anaya", "2026-01-04"), ("marcus", "2026-01-11")],
        )
        conn.executemany(
            "INSERT INTO posts (user_id, title, published_on) VALUES (?, ?, ?)",
            [(1, "First post", "2026-03-01"), (2, "Second post", "2026-03-02")],
        )
        conn.commit()
        before = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        print(f"Before: {before} posts")
        conn.executescript(MIGRATION_SQL)
        after = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        print(f"After:  {after} posts")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/homework/problem-02-migration-script.md) and run it there.

## Requirements

1. `002_add_categories.sql` creates a `categories` table with a unique
   `name`.
2. It adds a `category_id` column to `posts` that references
   `categories(id)`, is **nullable**, and has **no default**.
3. It inserts three starter categories: `Tech`, `Life`, `Other`.
4. It backfills — every existing post with a NULL `category_id` is set to
   the id of `Other`.
5. The whole migration is wrapped in one `BEGIN`/`COMMIT` so it is atomic.
6. Running the file prints the post count and category before and after,
   and proves the count did not change.

## Constraints

- **The new column must be nullable with no default.** Adding a
  `NOT NULL` column to a table that already has rows fails immediately —
  every existing row would violate it the instant it appears. Add the
  column nullable, backfill it, and only *then* could you tighten it if
  you wanted to (a second migration).
- **Backfill in SQL, in the same transaction.** The `UPDATE ... SET
  category_id = (SELECT id FROM categories WHERE name = 'Other')` runs
  inside the same `BEGIN`/`COMMIT` as the `ALTER` and the `INSERT`s.
  Splitting it into a separate step outside the transaction leaves a
  window where the column exists but the old posts have no category.
- **One `BEGIN`/`COMMIT`, so it is all-or-nothing.** If the migration
  fails halfway — a typo in the last statement — you want the database
  back exactly as it started, not half-migrated. That is the entire
  reason to wrap it in a transaction. A half-applied migration is the
  worst possible state: neither the old shape nor the new one.
- **Never format a table or column name into the SQL.** When the Python
  needs to ask "does `posts` have a `category_id` column yet?", it binds
  both names as parameters to `pragma_table_info(?)` — the same
  discipline the rest of the week drills, applied to the migration's own
  bookkeeping.

## Expected output

```text
Before the migration:
  posts: 3, category_id column: False
  2026-03-01  Reading a query plan out loud   -> (no category column yet)
  2026-03-02  Why my JSON file finally broke  -> (no category column yet)
  2026-03-05  Three things WHERE will not do  -> (no category column yet)

Applying 002_add_categories.sql ...

After the migration:
  posts: 3, category_id column: True
  2026-03-01  Reading a query plan out loud   -> Other
  2026-03-02  Why my JSON file finally broke  -> Other
  2026-03-05  Three things WHERE will not do  -> Other
  categories seeded: Tech, Life, Other

Row-count proof: 3 posts before, 3 after. Nothing lost.
```

## Steps

1. Run the starter unchanged. It prints the same post count twice,
   because the migration is empty. That is your baseline.
2. Fill in `TODO 1` and `TODO 2` — the `CREATE TABLE` and the
   `ALTER TABLE ... ADD COLUMN`. Rerun. The column now exists.
3. Fill in `TODO 3`, the three category inserts. Rerun and query
   `categories` to confirm three rows.
4. Fill in `TODO 4`, the backfill `UPDATE`. Rerun and confirm every post
   now shows `Other`.
5. Prove the transaction: introduce a deliberate typo in the last line of
   the migration, run it, and confirm the *whole* migration rolled back —
   the column is gone again, because `COMMIT` never ran. Then fix it.

## The Solution

```python
"""problem-02-migration-script-solution.py — change a live schema without losing a row.

Two SQL scripts, exactly as the problem asks: ``INITIAL_SQL`` is
``001_initial.sql``, the bare users and posts tables from this week's
exercises, and ``MIGRATION_SQL`` is ``002_add_categories.sql`` — it creates a
categories table, bolts a nullable ``category_id`` onto posts, seeds three
categories, and backfills every existing post to "Other". The whole
migration sits inside one BEGIN/COMMIT, so it either all happens or none of
it does.

Running this file plays the story out on an in-memory database with rows
already in it: state before, migrate, state after, and the row-count proof
that nothing was lost. Nothing is written to disk.

Run it with::

    python problem-02-migration-script-solution.py
"""

import sqlite3
from typing import Final

#: 001_initial.sql — the schema the database already has, with data in it.
INITIAL_SQL: Final[str] = """
CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL UNIQUE,
    joined_on TEXT NOT NULL
);

CREATE TABLE posts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    title        TEXT    NOT NULL,
    published_on TEXT    NOT NULL
);
"""

#: 002_add_categories.sql — the migration under test.
MIGRATION_SQL: Final[str] = """
BEGIN;

-- 1. The new table.
CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. The new column: nullable, no default, so existing rows stay legal
--    the instant it appears. (Adding a NOT NULL column to a table with
--    rows in it fails for exactly that reason.)
ALTER TABLE posts ADD COLUMN category_id INTEGER REFERENCES categories(id);

-- 3. Three starter categories.
INSERT INTO categories (name) VALUES ('Tech'), ('Life'), ('Other');

-- 4. Backfill: every post that predates categories lands in 'Other'.
UPDATE posts
SET category_id = (SELECT id FROM categories WHERE name = 'Other')
WHERE category_id IS NULL;

COMMIT;
"""

USERS: Final[list[tuple[str, str]]] = [
    ("anaya",  "2026-01-04"),
    ("marcus", "2026-01-11"),
]

POSTS: Final[list[tuple[int, str, str]]] = [
    (1, "Reading a query plan out loud",  "2026-03-01"),
    (2, "Why my JSON file finally broke", "2026-03-02"),
    (1, "Three things WHERE will not do", "2026-03-05"),
]


def column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    """True when `table` has `column` — asked via pragma_table_info with
    both names bound, so no name is ever formatted into the SQL."""
    cursor = conn.execute(
        "SELECT COUNT(*) FROM pragma_table_info(?) WHERE name = ?",
        (table, column),
    )
    return cursor.fetchone()[0] > 0


def post_count(conn: sqlite3.Connection) -> int:
    """The number the migration must not change."""
    return conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]


def show_posts(conn: sqlite3.Connection) -> None:
    """Print every post with its category, or '(none)' before the migration."""
    if column_exists(conn, "posts", "category_id"):
        cursor = conn.execute(
            """
            SELECT p.published_on, p.title, c.name
            FROM posts AS p
            LEFT JOIN categories AS c ON c.id = p.category_id
            ORDER BY p.published_on
            """
        )
        for published_on, title, category in cursor.fetchall():
            print(f"  {published_on}  {title:<31} -> {category}")
    else:
        cursor = conn.execute(
            "SELECT published_on, title FROM posts ORDER BY published_on"
        )
        for published_on, title in cursor.fetchall():
            print(f"  {published_on}  {title:<31} -> (no category column yet)")


def main() -> None:
    """Build the old world, migrate it, and prove nothing was lost."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.executescript(INITIAL_SQL)
        conn.executemany(
            "INSERT INTO users (username, joined_on) VALUES (?, ?)", USERS
        )
        conn.executemany(
            "INSERT INTO posts (user_id, title, published_on) VALUES (?, ?, ?)",
            POSTS,
        )
        conn.commit()

        before = post_count(conn)
        print("Before the migration:")
        print(f"  posts: {before}, category_id column: "
              f"{column_exists(conn, 'posts', 'category_id')}")
        show_posts(conn)

        print("\nApplying 002_add_categories.sql ...")
        conn.executescript(MIGRATION_SQL)

        after = post_count(conn)
        print("\nAfter the migration:")
        print(f"  posts: {after}, category_id column: "
              f"{column_exists(conn, 'posts', 'category_id')}")
        show_posts(conn)

        names = [name for (name,) in conn.execute(
            "SELECT name FROM categories ORDER BY id"
        ).fetchall()]
        print(f"  categories seeded: {', '.join(names)}")
        print(f"\nRow-count proof: {before} posts before, {after} after. "
              "Nothing lost.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

<!--@@INSERT:problem-02-migration-script-solution.py@@-->

**Why it works.**

**A migration is a diff between two schemas, expressed as SQL you can
run once.** `001_initial.sql` is where the database is; the migration is
the set of steps that move it to where you want it. Numbering them
(`001`, `002`) is how a real project keeps track of which migrations a
given database has already had applied.

**Nullable-then-backfill is the standard two-move for adding a required
column to a full table.** You cannot add `category_id NOT NULL` to a
table with three rows in it — those rows have no category, so they would
all violate the constraint the instant it exists. So you add the column
nullable (every old row gets NULL, which is legal), then fill the NULLs
in with a backfill `UPDATE`. The column is *effectively* required from
that point on because your code always sets it — and if you truly needed
the database to enforce it, that is a later migration, run once every
row already has a value.

**The whole thing is one transaction, so it cannot half-happen.**
`BEGIN` ... `COMMIT` wraps the create, the alter, the inserts, and the
backfill into a single atomic step. If the last statement has a typo,
SQLite rolls the entire migration back and the database is byte-for-byte
what it was before you started. There is no state where the column exists
but the backfill did not run.

**The proof is a row count, taken before and after.** The single most
important property of a migration is "I did not lose data". The script
counts posts before and after and prints both. Three equals three is not
decoration — it is the assertion that the operation was safe.

**`column_exists` binds its names.** Even the migration's own
housekeeping query — "does this column exist yet?" — passes `posts` and
`category_id` as bound parameters to `pragma_table_info(?)`, never
formatting them into the SQL string. The habit does not get a day off
just because the input came from you.

## Download and run

Download [problem-02-migration-script-solution.py](./problem-02-migration-script-solution.py)
and run it:

```bash
python problem-02-migration-script-solution.py
```

It builds the old two-table world in memory, fills it with rows, applies
the migration, and prints the before/after proof — then throws the
database away. Nothing touches disk.

Your hand-in is the two SQL files. Split `INITIAL_SQL` into
`001_initial.sql` and `MIGRATION_SQL` into `002_add_categories.sql`, then
confirm the pair applies cleanly to a real file:

```bash
sqlite3 blog.db < 001_initial.sql
sqlite3 blog.db < 002_add_categories.sql
```

## Common bugs to catch

- **`sqlite3.OperationalError: Cannot add a NOT NULL column with default
  value NULL`.** You wrote `ADD COLUMN category_id INTEGER NOT NULL`.
  There is no value to put in the existing rows. Add it nullable and
  backfill.
- **`sqlite3.IntegrityError: NOT NULL constraint failed` on the
  backfill.** The `SELECT id FROM categories WHERE name = 'Other'`
  returned nothing — you backfilled before inserting the categories, so
  the subquery gave NULL. Order matters: categories in, then backfill.
- **The migration "worked" but the column is gone on the next run.** You
  wrote `BEGIN` and forgot `COMMIT` (or a later statement raised and
  rolled it all back). Without a commit, SQLite discards the whole
  transaction when the connection closes. Confirm `COMMIT;` is the last
  line and nothing above it raised.
- **`sqlite3.OperationalError: near "ALTER": syntax error` inside
  `executescript`.** Some SQLite builds cannot add a foreign-key column
  in one `ALTER`. If you hit it, use the four-step "create new table,
  copy the data, drop the old, rename the new" pattern — and leave a
  comment saying why. The reference solution's simple `ADD COLUMN` works
  on the SQLite bundled with modern CPython.
- **Backfilling only some rows.** `WHERE category_id IS NULL` is the
  filter that means "only the old posts". Drop it and you re-file every
  post, including any a later run already categorised.

## Under the hood

<details>
<summary>Under the hood — why migrations are files, numbered, and never edited</summary>

The reason a migration is a *file* with a *number*, rather than a query
you type once, is that a database's schema has a history, and that
history has to be reproducible on every copy of the database.

Picture three databases: your laptop, a teammate's laptop, and the live
server. They all started from `001_initial.sql`. When you write
`002_add_categories.sql`, each database applies it once, in order, and
now all three have the same shape. A tool (Alembic, in the Python world)
records in a small table which migration numbers each database has seen,
so it knows `002` still needs applying to the server but not to your
laptop.

Two rules fall out of this, and they surprise people:

**You never edit a migration once it has run anywhere.** If `002` is
already applied on the server and you change the file, your laptop
applies the new `002` and the server applies nothing — they diverge, with
the same number meaning two different things. To change something, you
write `003`.

**Migrations only ever go forward in practice.** A "down" migration that
undoes a change sounds tidy, but reversing a change that dropped a column
cannot un-drop the data. Real teams roll *forward* to a fix far more
often than they roll back.

This is also why the transaction matters so much. A migration that half-
applies leaves one database in a shape no migration file describes, and
now the numbered history is a lie. All-or-nothing keeps the history
honest.

</details>

## Acceptance checklist

- [ ] `002_add_categories.sql` creates `categories` with a unique `name`.
- [ ] It adds `category_id` to `posts`, nullable, no default.
- [ ] It inserts `Tech`, `Life`, `Other`.
- [ ] It backfills every existing post to `Other`.
- [ ] The migration is inside one `BEGIN`/`COMMIT`.
- [ ] Running the file prints matching before/after post counts.
- [ ] A deliberate typo in the migration leaves the database unchanged.

## Stretch

- **Write the `003` that makes `category_id` required.** Now that every
  post has a category, add a migration that rebuilds `posts` with
  `category_id NOT NULL`. You will need the "create new, copy, drop,
  rename" pattern, because SQLite cannot tighten a column in place.
- **Add a "schema_migrations" table** that records each migration's
  number and the timestamp it was applied. Have the Python refuse to
  apply a migration whose number is already recorded — the beginning of a
  real migration runner.
- **Make the backfill data-driven.** Instead of everyone landing in
  `Other`, guess the category from a keyword in the title
  (`CASE WHEN title LIKE '%query%' THEN ...`). Notice how quickly a
  backfill grows from a rule into a judgement call.
- **Break it on purpose.** Remove the `BEGIN`/`COMMIT`, put a typo in the
  last statement, and run it. Confirm the database is now half-migrated —
  the column exists but the categories do not — and sit with how much
  worse that is than a clean failure.

Next: [Problem 3 — CSV → SQLite Importer](./problem-03-csv-importer.md),
where the data comes from a file you did not write.
