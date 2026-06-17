"""Exercise 02 — Parameterized queries vs. SQL injection.

Goal
----
Feel the difference between vulnerable string-formatted SQL and safe
parameterized SQL. The script builds a small `users` table, then runs
the same conceptual "login lookup" two ways:

  1. The wrong way (f-string interpolation). We feed it a malicious
     username and watch it return rows it should not have returned.
  2. The right way (parameterized). The same malicious input is treated
     as a literal value and matches nothing.

Run it
------
    python exercise-02-parameterized.py

Important
---------
Even after you understand this exercise, NEVER copy the vulnerable
function into real code. It is here for educational purposes only.

Docs
----
sqlite3 placeholders: https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
OWASP SQL injection: https://owasp.org/www-community/attacks/SQL_Injection
"""

from __future__ import annotations

import sqlite3
from typing import Final

DB_PATH: Final[str] = "exercise-02.db"


def setup(conn: sqlite3.Connection) -> None:
    """Build a small users table with three rows."""
    conn.executescript(
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        INSERT INTO users (username, password) VALUES
            ('alice', 'alice-secret'),
            ('bob',   'bob-secret'),
            ('admin', 'super-secret-do-not-share');
        """
    )


# ---------------------------------------------------------------------
# The WRONG way — DO NOT use in real code.
# ---------------------------------------------------------------------
def find_user_vulnerable(conn: sqlite3.Connection, username: str) -> list[sqlite3.Row]:
    """Build the SQL by string interpolation. This is the vulnerability."""
    # The line below is intentionally bad. Look at it. Understand it.
    # Never write code that looks like this. We are demonstrating an attack.
    query = f"SELECT id, username, password FROM users WHERE username = '{username}'"
    print(f"  [vulnerable] running: {query}")
    cursor = conn.cursor()
    # `executescript` allows multiple statements, which is what the attack exploits.
    cursor.executescript(query)
    cursor.execute("SELECT id, username, password FROM users")
    return cursor.fetchall()


# ---------------------------------------------------------------------
# The RIGHT way — always parameterize.
# ---------------------------------------------------------------------
def find_user_safe(conn: sqlite3.Connection, username: str) -> list[sqlite3.Row]:
    """Use a ? placeholder. The value is sent separately from the SQL."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,),                  # tuple with trailing comma — important
    )
    return cursor.fetchall()


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        setup(conn)

        # A perfectly normal lookup works in both versions.
        print("Normal lookup for username='alice':")
        print("  safe       :", [dict(r) for r in find_user_safe(conn, "alice")])

        # Now an attacker types a malicious username. With string formatting,
        # the trailing statement `DROP TABLE users` runs. The "safe" version
        # treats the whole thing as one literal username and returns nothing.
        evil: str = "alice'; DROP TABLE users; --"

        print("\nMalicious input on the SAFE query (should return nothing):")
        rows = find_user_safe(conn, evil)
        print(f"  rows returned: {len(rows)}")

        print("\nMalicious input on the VULNERABLE query (watch what happens):")
        try:
            find_user_vulnerable(conn, evil)
        except sqlite3.OperationalError as exc:
            # After the DROP succeeds, the follow-up SELECT fails because the
            # table no longer exists. That is the smoking gun.
            print(f"  follow-up query failed: {exc}")

        # Try to read the users table again. It's gone.
        try:
            conn.execute("SELECT COUNT(*) FROM users")
        except sqlite3.OperationalError as exc:
            print(f"\nVerified: table is gone — {exc}")
            print("Lesson: ALWAYS use parameterized queries. Never f-string SQL.")


if __name__ == "__main__":
    main()
