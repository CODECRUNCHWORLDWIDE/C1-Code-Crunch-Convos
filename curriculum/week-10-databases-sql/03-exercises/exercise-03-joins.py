"""Exercise 03 — INNER JOIN on two related tables.

Goal
----
Build two tables (`users` and `posts`) linked by a foreign key, insert
sample data, then run an INNER JOIN to list every post together with
its author's name.

Run it
------
    python exercise-03-joins.py

Stretch
-------
After you get the INNER JOIN working, change it to a LEFT JOIN and add
a user with zero posts. Confirm the LEFT JOIN keeps the post-less user
in the output while the INNER JOIN drops them.

Docs
----
SQLite JOIN syntax: https://www.sqlite.org/lang_select.html#fromclause
"""

from __future__ import annotations

import sqlite3
from typing import Final

DB_PATH: Final[str] = "exercise-03.db"


def setup(conn: sqlite3.Connection) -> None:
    """Create users and posts; insert sample data."""
    conn.executescript(
        """
        DROP TABLE IF EXISTS posts;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title   TEXT NOT NULL,
            body    TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    users: list[tuple[str, str]] = [
        ("Ada",   "ada@example.com"),
        ("Alan",  "alan@example.com"),
        ("Grace", "grace@example.com"),
    ]
    conn.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        users,
    )

    # user_id values match the auto-incremented ids above (1, 2, 3).
    posts: list[tuple[int, str, str]] = [
        (1, "Notes on the Analytical Engine",  "A machine that computes anything..."),
        (1, "On Bernoulli numbers",            "The first algorithm."),
        (2, "Computing Machinery and Intelligence", "Can machines think?"),
        (3, "COBOL field report",              "Compiling is finally usable."),
        (3, "Bug discovered in Mark II",       "Found a moth in the relay."),
    ]
    conn.executemany(
        "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)",
        posts,
    )


def list_posts_with_authors(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return every post joined to its author's name and email."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT  p.id    AS post_id,
                p.title AS post_title,
                u.name  AS author_name,
                u.email AS author_email
        FROM    posts AS p
        INNER JOIN users AS u ON u.id = p.user_id
        ORDER BY u.name, p.id
        """
    )
    return cursor.fetchall()


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")    # enforce the foreign key
        setup(conn)

        rows = list_posts_with_authors(conn)
        print(f"Found {len(rows)} posts via INNER JOIN:")
        for row in rows:
            print(
                f"  post #{row['post_id']:>2}: {row['post_title']!r:50}  "
                f"by {row['author_name']} <{row['author_email']}>"
            )


if __name__ == "__main__":
    main()
