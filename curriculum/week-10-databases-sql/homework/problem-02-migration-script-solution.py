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
