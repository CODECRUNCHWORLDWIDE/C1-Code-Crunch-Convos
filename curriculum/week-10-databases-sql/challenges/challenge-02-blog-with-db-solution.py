"""challenge-02-blog-with-db-solution.py — the Week 9 blog's data, on SQLite.

This is the storage layer the challenge asks for: users with hashed
passwords, posts, and comments, all in one SQLite schema, every value bound
through ``?``. Your Flask routes from Week 9 stay your own — each route
becomes one call into this module, which is the point of keeping every line
of SQL in one file.

The password hashing is standard library only: PBKDF2 via
``hashlib.pbkdf2_hmac`` with a random salt, compared with
``hmac.compare_digest``. No plain-text password is ever stored or printed.

This download runs against an in-memory database, walks the six required
features with fixed timestamps, and leaves nothing behind. Point
``connect()`` at a path and the same module backs a real blog.

Run it with::

    python challenge-02-blog-with-db-solution.py
"""

import hashlib
import hmac
import secrets
import sqlite3
from typing import Final

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id    INTEGER NOT NULL REFERENCES users(id),
    title        TEXT NOT NULL,
    body         TEXT NOT NULL,
    published_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id    INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id  INTEGER REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_posts_author    ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_comments_post   ON comments(post_id);
"""

PBKDF2_ITERATIONS: Final[int] = 600_000


class BlogError(Exception):
    """Raised when a blog rule refuses an operation."""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the blog database with foreign keys (and so ON DELETE) enforced."""
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the schema. Safe to call on every start — IF NOT EXISTS."""
    conn.executescript(SCHEMA)
    conn.commit()


def hash_password(password: str) -> str:
    """Return a salted PBKDF2 hash, self-describing and safe to store.

    Format: ``pbkdf2_sha256$<iterations>$<salt hex>$<digest hex>``. The salt
    is random per user, so two users with the same password store different
    hashes and a stolen table cannot be attacked with one precomputed list.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(stored: str, candidate: str) -> bool:
    """Check a login attempt against a stored hash, in constant time."""
    algorithm, iterations, salt_hex, digest_hex = stored.split("$")
    if algorithm != "pbkdf2_sha256":
        raise BlogError(f"unknown hash algorithm: {algorithm}")
    attempt = hashlib.pbkdf2_hmac(
        "sha256",
        candidate.encode("utf-8"),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(attempt.hex(), digest_hex)


def create_user(
    conn: sqlite3.Connection, username: str, password: str, created_at: str
) -> int:
    """Sign a user up. The password is hashed before it touches the database."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, created_at) "
            "VALUES (?, ?, ?)",
            (username, hash_password(password), created_at),
        )
    return cursor.lastrowid


def authenticate(conn: sqlite3.Connection, username: str, password: str) -> int | None:
    """Return the user's id when the password checks out, else None."""
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    if row is None:
        return None
    user_id, stored = row
    return user_id if verify_password(stored, password) else None


def create_post(
    conn: sqlite3.Connection, author_id: int, title: str, body: str, published_at: str
) -> int:
    """Insert a post and return its id. The route checks login; this inserts."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO posts (author_id, title, body, published_at) "
            "VALUES (?, ?, ?, ?)",
            (author_id, title, body, published_at),
        )
    return cursor.lastrowid


def list_posts(conn: sqlite3.Connection) -> list[tuple[int, str, str, str]]:
    """Return (id, published_at, username, title), newest first — the homepage."""
    cursor = conn.execute(
        """
        SELECT p.id, p.published_at, u.username, p.title
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.author_id
        ORDER BY p.published_at DESC, p.id DESC
        """
    )
    return cursor.fetchall()


def get_post(conn: sqlite3.Connection, post_id: int) -> tuple[str, str, str, str]:
    """Return (title, body, username, published_at) for one post."""
    row = conn.execute(
        """
        SELECT p.title, p.body, u.username, p.published_at
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.author_id
        WHERE p.id = ?
        """,
        (post_id,),
    ).fetchone()
    if row is None:
        raise BlogError(f"no post with id {post_id}")
    return row


def comments_for(conn: sqlite3.Connection, post_id: int) -> list[tuple[str, str, str | None]]:
    """Return (created_at, body, username or None) for a post's comments.

    LEFT JOIN, because a guest comment has a NULL author_id and must still
    appear — an INNER JOIN would silently drop it.
    """
    cursor = conn.execute(
        """
        SELECT c.created_at, c.body, u.username
        FROM comments AS c
        LEFT JOIN users AS u ON u.id = c.author_id
        WHERE c.post_id = ?
        ORDER BY c.created_at, c.id
        """,
        (post_id,),
    )
    return cursor.fetchall()


def add_comment(
    conn: sqlite3.Connection,
    post_id: int,
    author_id: int | None,
    body: str,
    created_at: str,
) -> int:
    """Insert a comment. author_id may be None — that is a guest."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO comments (post_id, author_id, body, created_at) "
            "VALUES (?, ?, ?, ?)",
            (post_id, author_id, body, created_at),
        )
    return cursor.lastrowid


def delete_post(conn: sqlite3.Connection, post_id: int, requester_id: int) -> None:
    """Delete a post — but only when the requester wrote it.

    The ownership check is in the WHERE clause, so checking and deleting are
    one statement: there is no window where the check has passed and the
    delete has not happened. Comments go with the post via ON DELETE CASCADE.
    """
    with conn:
        cursor = conn.execute(
            "DELETE FROM posts WHERE id = ? AND author_id = ?",
            (post_id, requester_id),
        )
    if cursor.rowcount == 0:
        raise BlogError("only the author may delete a post")


def count(conn: sqlite3.Connection, table: str) -> int:
    """Row count for one of this module's tables, name checked by lookup.

    A table name cannot travel through a ``?`` placeholder — it is syntax,
    not a value — so it is validated against the fixed set of tables this
    schema owns before it is ever placed in the query.
    """
    if table not in {"users", "posts", "comments"}:
        raise BlogError(f"unknown table: {table}")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]  # noqa: S608


def main() -> None:
    """Walk the six required features against fixed demo data."""
    conn = connect()
    try:
        init_db(conn)
        print("Blog storage ready (in-memory database for this demo).")

        print("\n-- Signup: hashes stored, never passwords --")
        ada = create_user(conn, "ada", "correct horse battery", "2026-05-01")
        alan = create_user(conn, "alan", "hut 8 forever", "2026-05-01")
        scheme = conn.execute(
            "SELECT password_hash FROM users WHERE id = ?", (ada,)
        ).fetchone()[0].split("$")[0]
        print(f"created users ada (id {ada}) and alan (id {alan})")
        print(f"stored for ada: a {scheme} hash; the password itself is nowhere")

        print("\n-- Login --")
        print(f"ada + wrong password  -> {authenticate(conn, 'ada', 'password123')}")
        print(f"ada + right password  -> user id {authenticate(conn, 'ada', 'correct horse battery')}")

        print("\n-- Posts (homepage: newest first, author joined in) --")
        first = create_post(
            conn, ada, "Parameterize everything",
            "The one habit Week 10 exists to install.", "2026-05-01",
        )
        create_post(
            conn, ada, "The day my JSON file gave up",
            "Forty megabytes, rewritten on every save.", "2026-05-02",
        )
        create_post(
            conn, alan, "Reading EXPLAIN QUERY PLAN",
            "SCAN means the database read everything.", "2026-05-03",
        )
        for post_id, published_at, username, title in list_posts(conn):
            print(f"  {published_at}  {username:<5} {title}")

        print("\n-- One post, with its comments (guests included) --")
        add_comment(conn, first, alan, "Placeholders from day one.", "2026-05-01 10:15")
        add_comment(conn, first, None, "What about table names?", "2026-05-01 11:40")
        title, body, username, published_at = get_post(conn, first)
        print(f"  {title} (by {username}, {published_at})")
        for created_at, comment_body, commenter in comments_for(conn, first):
            print(f"    {created_at}  {commenter or 'guest':<6} {comment_body}")

        print("\n-- Deleting: only the author, comments cascade --")
        try:
            delete_post(conn, first, alan)
        except BlogError as exc:
            print(f"alan tried to delete post {first}: refused ({exc})")
        comments_before = count(conn, "comments")
        delete_post(conn, first, ada)
        print(f"ada deleted post {first}: its {comments_before} comments went with it")
        print(f"posts remaining: {count(conn, 'posts')}, comments remaining: {count(conn, 'comments')}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
