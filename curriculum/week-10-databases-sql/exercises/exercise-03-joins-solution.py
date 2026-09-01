"""exercise-03-joins-solution.py — two tables, one foreign key, one INNER JOIN.

Builds a tiny community blog in blog.db and lists every post next to the
name of the person who wrote it.

Your own exercise-03-joins.py keeps blog.db in the folder you run it from,
so you can open the SQLite shell on it afterwards and trace the join by
hand. This shipped answer runs the same code inside a throwaway temporary
folder instead, so the download never collides with a database of yours and
never leaves a file behind. The three query functions are the whole exercise
and know nothing about the harness.

Run it with::

    python exercise-03-joins-solution.py
"""

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Final

DB_PATH: Final[str] = "blog.db"

SCHEMA: Final[str] = """
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL UNIQUE,
    joined_on TEXT NOT NULL
);

CREATE TABLE posts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    title        TEXT    NOT NULL,
    published_on TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

USERS: Final[list[tuple[str, str]]] = [
    ("anaya",  "2026-01-04"),
    ("marcus", "2026-01-11"),
    ("priya",  "2026-02-02"),
    ("devon",  "2026-02-20"),
]

POSTS: Final[list[tuple[int, str, str]]] = [
    (1, "Reading a query plan out loud",   "2026-03-01"),
    (2, "Why my JSON file finally broke",  "2026-03-02"),
    (1, "Three things WHERE will not do",  "2026-03-05"),
    (3, "A foreign key saved my weekend",  "2026-03-06"),
    (2, "Indexes are not magic",           "2026-03-11"),
]

CUTOFF: Final[str] = "2026-03-05"

POSTS_WITH_AUTHORS_SQL: Final[str] = """
SELECT p.published_on, u.username, p.title
FROM posts AS p
INNER JOIN users AS u ON p.user_id = u.id
ORDER BY p.published_on
"""

POSTS_SINCE_SQL: Final[str] = """
SELECT p.published_on, u.username, p.title
FROM posts AS p
INNER JOIN users AS u ON p.user_id = u.id
WHERE p.published_on >= ?
ORDER BY p.published_on
"""

POST_COUNT_SQL: Final[str] = """
SELECT COUNT(*)
FROM posts AS p
INNER JOIN users AS u ON p.user_id = u.id
WHERE u.username = ?
"""


def connect() -> sqlite3.Connection:
    """Open the database with foreign-key enforcement switched on."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild both tables and insert the seed rows."""
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO users (username, joined_on) VALUES (?, ?)", USERS
    )
    conn.executemany(
        "INSERT INTO posts (user_id, title, published_on) VALUES (?, ?, ?)",
        POSTS,
    )
    conn.commit()


def posts_with_authors(conn: sqlite3.Connection) -> list[tuple[str, str, str]]:
    """Return (published_on, username, title) for every post with an author."""
    cursor = conn.execute(POSTS_WITH_AUTHORS_SQL)
    return cursor.fetchall()


def posts_since(conn: sqlite3.Connection, cutoff: str) -> list[tuple[str, str, str]]:
    """Same join, filtered to posts published on or after `cutoff`."""
    cursor = conn.execute(POSTS_SINCE_SQL, (cutoff,))
    return cursor.fetchall()


def post_count(conn: sqlite3.Connection, username: str) -> int:
    """Return how many posts a given user has written."""
    cursor = conn.execute(POST_COUNT_SQL, (username,))
    return cursor.fetchone()[0]


def show(rows: list[tuple[str, str, str]]) -> None:
    """Print one line per joined row, then the row count."""
    for published_on, username, title in rows:
        print(f"{published_on}  {username:<7} {title}")
    print(f"{len(rows)} rows.")


def main() -> None:
    """Seed the blog, then run the joins."""
    conn = connect()
    try:
        seed(conn)
        print(f"Seeded {DB_PATH}: {len(USERS)} users, {len(POSTS)} posts.")

        print("\nEvery post with its author (INNER JOIN):")
        show(posts_with_authors(conn))

        print(f"\nPosts published on or after {CUTOFF}:")
        show(posts_since(conn, CUTOFF))

        print(f"\ndevon has {post_count(conn, 'devon')} posts and does not "
              "appear above. INNER JOIN dropped that row.")
    finally:
        conn.close()


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_PATH is relative, so the database lands in the current folder. Moving
    into a temporary folder first means this download builds its blog, prints
    the joins, and leaves your disk exactly as it found it.
    """
    keep = Path.cwd()
    with tempfile.TemporaryDirectory() as workspace:
        os.chdir(workspace)
        try:
            main()
        finally:
            os.chdir(keep)


if __name__ == "__main__":
    run_in_throwaway_folder()
