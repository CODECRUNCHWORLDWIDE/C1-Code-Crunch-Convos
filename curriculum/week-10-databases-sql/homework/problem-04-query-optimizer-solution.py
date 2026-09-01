"""problem-04-query-optimizer-solution.py — make the claim in the write-up observable.

The problem is a reasoning exercise: which index rescues a slow
top-users-by-login query? This script is the part of the answer you can run.
It builds the events table in memory, seeds it deterministically, and prints
EXPLAIN QUERY PLAN for the same query four times: with no index, with a
single-column index, with the composite index, and with a covering index.
Watch SCAN become SEARCH, then the temp sort disappear.

The report date is pinned (REPORT_DATE) and the cutoff is a bound
parameter, so the output never depends on today's date. Per-stage timings
are real but go to stderr — machine-dependent numbers do not belong in
comparable output.

Run it with::

    python problem-04-query-optimizer-solution.py
"""

import sqlite3
import sys
import time
from datetime import date, timedelta
from typing import Final

ROWS: Final[int] = 20_000
USERS: Final[int] = 200
EVENT_TYPES: Final[tuple[str, ...]] = ("login", "view", "purchase", "logout")
REPORT_DATE: Final[date] = date(2026, 8, 1)
WINDOW_DAYS: Final[int] = 30

#: The slow query from the problem, with the date as a parameter instead of
#: DATE('now', '-30 days') — same plan, but reproducible on any day.
QUERY: Final[str] = """
SELECT user_id, COUNT(*) AS event_count
FROM   events
WHERE  event_type = ?
  AND  occurred_at >= ?
GROUP BY user_id
ORDER BY event_count DESC
LIMIT 10
"""

SCHEMA: Final[str] = """
CREATE TABLE events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    event_type  TEXT    NOT NULL,
    occurred_at TEXT    NOT NULL,
    payload     TEXT    NOT NULL DEFAULT ''
);
"""

#: The four stages of the argument. Index names double as labels.
STAGES: Final[list[tuple[str, str | None]]] = [
    ("no index at all", None),
    ("single-column index on event_type",
     "CREATE INDEX idx_events_type ON events(event_type)"),
    ("composite index on (event_type, occurred_at)",
     "CREATE INDEX idx_events_type_time ON events(event_type, occurred_at)"),
    ("covering index on (event_type, occurred_at, user_id)",
     "CREATE INDEX idx_events_type_time_user "
     "ON events(event_type, occurred_at, user_id)"),
]


def seed(conn: sqlite3.Connection) -> None:
    """Insert ROWS deterministic events spread over 60 days.

    Pure arithmetic, no random module, so every machine builds the same
    table: user i*7 mod USERS, event type cycling through the four kinds,
    date walking backwards a day at a time from the report date.
    """
    rows = []
    for i in range(ROWS):
        user_id = (i * 7) % USERS + 1
        event_type = EVENT_TYPES[i % len(EVENT_TYPES)]
        occurred = REPORT_DATE - timedelta(days=(i % 60) + 1)
        rows.append((user_id, event_type, occurred.isoformat(), f"payload-{i}"))
    with conn:
        conn.executemany(
            "INSERT INTO events (user_id, event_type, occurred_at, payload) "
            "VALUES (?, ?, ?, ?)",
            rows,
        )


def explain(conn: sqlite3.Connection, params: tuple) -> list[str]:
    """Return the detail column of EXPLAIN QUERY PLAN for QUERY."""
    cursor = conn.execute("EXPLAIN QUERY PLAN " + QUERY, params)
    return [detail for (_, _, _, detail) in cursor.fetchall()]


def run_query(conn: sqlite3.Connection, params: tuple) -> list[tuple[int, int]]:
    """Run the real query and return its rows."""
    return conn.execute(QUERY, params).fetchall()


def main() -> None:
    """Build the table, then walk the four indexing stages."""
    cutoff = (REPORT_DATE - timedelta(days=WINDOW_DAYS)).isoformat()
    params = ("login", cutoff)

    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(SCHEMA)
        seed(conn)
        print(f"events table: {ROWS} rows, {USERS} users, "
              f"window {cutoff} .. {REPORT_DATE.isoformat()}")

        answer_before: list[tuple[int, int]] | None = None
        for label, index_sql in STAGES:
            if index_sql is not None:
                with conn:
                    conn.execute(index_sql)
            print(f"\n-- {label} --")
            for detail in explain(conn, params):
                print(f"  {detail}")
            started = time.perf_counter()
            answer = run_query(conn, params)
            elapsed = time.perf_counter() - started
            print(f"  [{elapsed * 1000:.1f} ms]", file=sys.stderr)
            if answer_before is None:
                answer_before = answer
            elif answer != answer_before:
                print("  WARNING: the answer changed - an index must never do that")

        print("\nSame ten rows at every stage - an index changes the route,")
        print("never the destination. Top three of the answer:")
        assert answer_before is not None
        for user_id, event_count in answer_before[:3]:
            print(f"  user {user_id:>3}: {event_count} logins")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
