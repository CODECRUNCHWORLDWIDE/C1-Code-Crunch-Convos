"""SQLite storage for the blog.

One connection per **application object**, not per request. That is unusual for
Flask, and it is deliberate: an in-memory SQLite database lives and dies with
its single connection, so if every request opened its own connection every
request would see its own empty database and the tests would pass while
proving nothing.

For a real deployment against a file database you would open the connection in
``g`` and close it in ``teardown_appcontext``. For a single-process app plus a
test client, one long-lived connection is simpler and correct.
"""

from __future__ import annotations

import sqlite3
from typing import cast

from flask import Flask, current_app

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_app(app: Flask) -> None:
    """Open the application's connection and make sure the schema exists."""
    connection = sqlite3.connect(app.config["DATABASE"], check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    connection.commit()
    app.extensions["blog_db"] = connection


def get_db() -> sqlite3.Connection:
    """Return the connection owned by the current application."""
    return cast(sqlite3.Connection, current_app.extensions["blog_db"])


def list_posts() -> list[sqlite3.Row]:
    """Return every post, newest first."""
    rows = get_db().execute("SELECT id, title, body, created_at FROM posts ORDER BY id DESC")
    return cast(list[sqlite3.Row], rows.fetchall())


def get_post(post_id: int) -> sqlite3.Row | None:
    """Return one post, or ``None`` if no post has that id."""
    row = get_db().execute("SELECT id, title, body, created_at FROM posts WHERE id = ?", (post_id,))
    return cast("sqlite3.Row | None", row.fetchone())


def create_post(title: str, body: str) -> int:
    """Insert a post and return its new id."""
    connection = get_db()
    cursor = connection.execute("INSERT INTO posts (title, body) VALUES (?, ?)", (title, body))
    connection.commit()
    return cast(int, cursor.lastrowid)


def delete_post(post_id: int) -> bool:
    """Delete a post. Return True if a row was actually removed."""
    connection = get_db()
    cursor = connection.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    return cursor.rowcount > 0
