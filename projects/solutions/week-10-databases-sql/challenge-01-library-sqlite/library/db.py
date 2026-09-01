"""Connections, PRAGMAs and transactions. Nothing here knows about books.

Three jobs, and only three:

1. Hand out connections that are configured the way this app always wants them
   (row factory, foreign keys on).
2. Bootstrap the schema idempotently from schema.sql.
3. Provide the transaction context manager that repository.py wraps every
   multi-statement operation in.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SCHEMA_PATH: Final[Path] = PROJECT_ROOT / "schema.sql"

#: Override with LIBRARY_DB when you want a throwaway database.
DB_PATH: Final[str] = os.environ.get("LIBRARY_DB", str(PROJECT_ROOT / "library.db"))


def connect(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    """Open a connection with this project's non-negotiable settings.

    `PRAGMA foreign_keys = ON` is per *connection*, not per database. Declaring
    `REFERENCES books(id)` in schema.sql does nothing on its own -- SQLite ships
    with foreign-key enforcement off for backwards compatibility, and every new
    connection starts off again. Forget this line on one connection and that
    connection can happily insert a loan for book 9999.
    """
    target = str(db_path)
    conn = sqlite3.connect(target, uri=target.startswith("file:"))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | Path = DB_PATH, schema_path: Path = SCHEMA_PATH) -> None:
    """Create the schema if it is not there. Safe to run on every start.

    Idempotent because every statement in schema.sql is `IF NOT EXISTS`.
    Running the app for the tenth time is a no-op, not a crash.
    """
    sql = schema_path.read_text(encoding="utf-8")
    with closing(connect(db_path)) as conn:
        with conn:
            conn.executescript(sql)


@contextmanager
def transaction(db_path: str | Path = DB_PATH) -> Iterator[sqlite3.Cursor]:
    """Yield a cursor inside one transaction; commit on success, roll back on error.

    `with conn:` is the transaction boundary. `closing(conn)` is the file
    handle. You want both: `with sqlite3.connect(...) as conn:` commits but
    never closes, which leaks handles and, on Windows, keeps the .db file
    locked long enough to be annoying.
    """
    with closing(connect(db_path)) as conn:
        with conn:
            yield conn.cursor()


@contextmanager
def read_cursor(db_path: str | Path = DB_PATH) -> Iterator[sqlite3.Cursor]:
    """Yield a cursor for read-only work. No transaction needed, still closes."""
    with closing(connect(db_path)) as conn:
        yield conn.cursor()
