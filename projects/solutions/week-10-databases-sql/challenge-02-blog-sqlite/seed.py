"""Sample data for the blog.

Usable two ways:

    flask --app app seed        # drop, recreate, seed (the normal way)
    python seed.py              # same thing, without the flask CLI

Every insert here uses `executemany` with a parameterized statement, which is
both the fast way and the safe way. The passwords are hashed exactly as the
signup route hashes them -- there is no back door that stores plaintext "just
for the demo", because that is how plaintext passwords end up in production.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from werkzeug.security import generate_password_hash

# (username, password) -- these are demo credentials and are printed by the
# seed command. Never ship real ones in a repo.
DEMO_USERS: list[tuple[str, str]] = [
    ("ada", "analytical-engine"),
    ("alan", "turing-machine-42"),
]

# (author username, title, body, published_at)
DEMO_POSTS: list[tuple[str, str, str, str]] = [
    ("ada", "Notes on the Analytical Engine",
     "The engine weaves algebraic patterns just as the Jacquard loom weaves "
     "flowers and leaves.", "2026-05-01 09:00:00"),
    ("ada", "On Bernoulli numbers",
     "A worked example of what the engine could compute, written out in full.",
     "2026-05-04 11:30:00"),
    ("alan", "On computable numbers",
     "A machine that reads a tape, one symbol at a time, is enough.",
     "2026-05-06 14:15:00"),
]

# (post title, author username or None for a guest, body, created_at)
DEMO_COMMENTS: list[tuple[str, str | None, str, str]] = [
    ("Notes on the Analytical Engine", "alan", "This is the first program.",
     "2026-05-02 08:00:00"),
    ("Notes on the Analytical Engine", None, "Reading this a century later.",
     "2026-05-03 19:45:00"),
    ("On computable numbers", "ada", "The halting argument is beautiful.",
     "2026-05-07 07:20:00"),
]


def load_sample_data(conn: sqlite3.Connection) -> dict[str, Any]:
    """Insert the demo rows into an already-created schema.

    Assumes the tables exist and are empty -- `flask --app app seed` runs
    init_db() first. Everything happens in one transaction: a half-seeded
    database is more confusing than an empty one.
    """
    conn.executemany(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        [(username, generate_password_hash(password)) for username, password in DEMO_USERS],
    )

    # Look the ids back up rather than assuming AUTOINCREMENT handed out 1, 2.
    # It will have, today. It will not after you delete a user and reseed.
    user_ids = {
        row["username"]: row["id"]
        for row in conn.execute("SELECT id, username FROM users")
    }

    conn.executemany(
        "INSERT INTO posts (author_id, title, body, published_at) VALUES (?, ?, ?, ?)",
        [(user_ids[author], title, body, when) for author, title, body, when in DEMO_POSTS],
    )

    post_ids = {row["title"]: row["id"] for row in conn.execute("SELECT id, title FROM posts")}

    conn.executemany(
        "INSERT INTO comments (post_id, author_id, body, created_at) VALUES (?, ?, ?, ?)",
        [
            (post_ids[title], user_ids[author] if author else None, body, when)
            for title, author, body, when in DEMO_COMMENTS
        ],
    )
    conn.commit()

    return {
        "users": len(DEMO_USERS),
        "posts": len(DEMO_POSTS),
        "comments": len(DEMO_COMMENTS),
        "credentials": DEMO_USERS,
    }


def main() -> int:
    from app import create_app
    from db import get_db, init_db

    app = create_app()
    with app.app_context():
        init_db()
        info = load_sample_data(get_db())
    print(f"Seeded {info['users']} users, {info['posts']} posts, "
          f"{info['comments']} comments.")
    for username, password in info["credentials"]:
        print(f"  login: {username} / {password}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
