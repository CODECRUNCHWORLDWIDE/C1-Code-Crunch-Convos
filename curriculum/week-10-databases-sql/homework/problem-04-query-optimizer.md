# Homework Problem 4 — Query Optimizer Puzzle

> **Topic:** why a query is slow, which index fixes it, and how to *see* the database change its mind
> **Lecture:** [02 — Joins and Aggregations](../lecture-notes/02-joins-and-aggregations.md)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** the difference between a page that loads instantly and one that hangs for four seconds is often a single index — and knowing *which* index is a skill you can learn to reason about instead of guess. This problem turns a paper write-up into something you can run: you watch `EXPLAIN QUERY PLAN` say "SCAN" and then, after one `CREATE INDEX`, say "SEARCH". The word changing is the whole lesson.

## The Brief

Here is a query that has gone slow. There is an `events` table with a
million rows — every click, login, and page view a product has ever
recorded — and this query finds the ten users with the most logins in the
last 30 days:

```sql
SELECT user_id, COUNT(*) AS event_count
FROM   events
WHERE  event_type = 'login'
  AND  occurred_at >= DATE('now', '-30 days')
GROUP BY user_id
ORDER BY event_count DESC
LIMIT 10;
```

It takes four seconds. Your job is to make it fast, and — more
importantly — to *understand and prove* why the fix works.

The reason it is slow is that the database has no shortcut to the login
rows. To answer the query it reads **every one of the million rows**,
checks each one's `event_type`, and throws away the 750,000 that are not
logins. That is a **full table scan**, and it is what an index removes:
an index is a pre-sorted lookup structure that lets the database jump
straight to the matching rows instead of reading all of them.

But which index? On which columns? And in what order? Those are real
questions with real answers, and the tool that answers them is
`EXPLAIN QUERY PLAN` — you put those words in front of any query and
SQLite tells you *how* it intends to run it, without actually running it.
`SCAN` means "read the whole table". `SEARCH ... USING INDEX` means "jump
straight to the rows". Your write-up is the reasoning; this script is the
proof, because it builds the table, runs the plan four times — no index,
one-column index, composite index, covering index — and prints each one
so you can watch `SCAN` turn into `SEARCH`.

## Starter

Save this as `optimizer.py` and fill in the `TODO`s. It runs as pasted —
it builds the table and prints the plan with no index; you add the
indexed stages.

```python
"""Watch EXPLAIN QUERY PLAN change as indexes are added to a slow query."""

import sqlite3
from datetime import date, timedelta

QUERY = """
SELECT user_id, COUNT(*) AS event_count
FROM   events
WHERE  event_type = ?
  AND  occurred_at >= ?
GROUP BY user_id
ORDER BY event_count DESC
LIMIT 10
"""


def explain(conn: sqlite3.Connection, params: tuple) -> list[str]:
    """Return the 'detail' text of EXPLAIN QUERY PLAN for QUERY."""
    cursor = conn.execute("EXPLAIN QUERY PLAN " + QUERY, params)
    return [detail for (_, _, _, detail) in cursor.fetchall()]


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        "CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, "
        "event_type TEXT, occurred_at TEXT, payload TEXT)"
    )
    # TODO: seed a few thousand deterministic rows with executemany
    cutoff = (date(2026, 8, 1) - timedelta(days=30)).isoformat()
    params = ("login", cutoff)
    print("-- no index --")
    for detail in explain(conn, params):
        print(f"  {detail}")
    # TODO: CREATE INDEX on event_type, print the plan again
    # TODO: CREATE INDEX on (event_type, occurred_at), print again
    conn.close()


if __name__ == "__main__":
    main()
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-10-databases-sql/homework/problem-04-query-optimizer.md) and run it there. `sqlite3` is all it needs.

## Requirements

1. Build the `events` table in memory and seed it **deterministically**
   (no `random`), so the plan and the answer are the same on every
   machine.
2. Run `EXPLAIN QUERY PLAN` for the query at four stages: no index, a
   single-column index on `event_type`, a composite index on
   `(event_type, occurred_at)`, and a covering index on
   `(event_type, occurred_at, user_id)`.
3. Print each plan so the reader can see `SCAN` become `SEARCH`, and see
   the covering index announced as `USING COVERING INDEX`.
4. The date is a **bound parameter**, not `DATE('now', ...)`, so the
   output does not depend on today's date.
5. Confirm the *answer* (the ten rows) is identical at every stage — an
   index changes the route, never the destination.

## Constraints

- **Pin the date; do not use `DATE('now', '-30 days')`.** A query that
  depends on today's date gives different output every day and cannot be
  checked against an Expected output block. Fix a `REPORT_DATE`, compute
  the cutoff from it, and bind it as a parameter. The plan is identical
  either way — this only makes the run reproducible.
- **Seed with arithmetic, not randomness.** `random` gives a different
  table every run, so the ten winning users would change. Deriving each
  row from its index (`user_id = i * 7 % USERS`) builds the exact same
  table everywhere, which is what lets the answer be a fixed fact.
- **Timings go to stderr, never stdout.** How many milliseconds a query
  takes depends on the machine, so it cannot be part of comparable
  output. The *plan* is deterministic and belongs in stdout; the clock is
  machine-dependent and belongs in stderr.
- **An index must never change the answer.** If the ten rows differ
  between stages, something is wrong — an index is only ever a faster
  route to the same result. The script asserts this so a mistake shows up
  loudly.

## Expected output

Timings go to stderr; the plans and the answer are the comparable output:

```text
events table: 20000 rows, 200 users, window 2026-07-02 .. 2026-08-01

-- no index at all --
  SCAN events
  USE TEMP B-TREE FOR GROUP BY
  USE TEMP B-TREE FOR ORDER BY

-- single-column index on event_type --
  SEARCH events USING INDEX idx_events_type (event_type=?)
  USE TEMP B-TREE FOR GROUP BY
  USE TEMP B-TREE FOR ORDER BY

-- composite index on (event_type, occurred_at) --
  SEARCH events USING INDEX idx_events_type_time (event_type=? AND occurred_at>?)
  USE TEMP B-TREE FOR GROUP BY
  USE TEMP B-TREE FOR ORDER BY

-- covering index on (event_type, occurred_at, user_id) --
  SEARCH events USING COVERING INDEX idx_events_type_time_user (event_type=? AND occurred_at>?)
  USE TEMP B-TREE FOR GROUP BY
  USE TEMP B-TREE FOR ORDER BY

Same ten rows at every stage - an index changes the route,
never the destination. Top three of the answer:
  user 197: 67 logins
  user 189: 67 logins
  user 181: 67 logins
```

(The script seeds 20,000 rows rather than a million — the plan a query
optimizer picks is the same shape at either size, and the point is the
plan, not the wait.)

## Steps

1. Run the starter. It prints one plan, and the first line reads
   `SCAN events`. That word is the problem — the whole table, every row.
2. Add `CREATE INDEX idx_events_type ON events(event_type)`, then print
   the plan again. `SCAN` becomes `SEARCH ... USING INDEX`. The database
   now jumps to the login rows instead of reading everything.
3. Add the composite index `(event_type, occurred_at)`. The `SEARCH` line
   now shows the date condition being used too — the index narrows on
   *both* the type and the time window.
4. Add the covering index `(event_type, occurred_at, user_id)` and watch
   `USING INDEX` become `USING COVERING INDEX`.
5. Read the four plans top to bottom. That progression *is* the write-up
   the problem asks for — now backed by output you produced.

## The Solution

```python
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
```

**Why it works.**

**Question by question, this is the write-up the problem asks for:**

*1. What is the query doing?* Counting, per user, how many `login`
events they have in the last 30 days, then returning the ten users with
the highest counts.

*2. Without an index, what does the database do?* A **full table scan**.
It has no way to find the login rows except to read every row and test
`event_type` on each. That is the `SCAN events` line, and on a million
rows it is the four seconds.

*3. Which one index?* A composite index on `(event_type, occurred_at)`.
The query filters on both columns, and this index lets SQLite jump to
`event_type = 'login'` and then, *within* the logins, walk only the rows
inside the date window. The plan proves it: `SEARCH events USING INDEX
idx_events_type_time (event_type=? AND occurred_at>?)` — both conditions
served by the one index.

*4. Could a composite do better than a single column?* Yes, and you can
see why. The single-column index on `event_type` alone still leaves the
date filter to be checked row by row (`event_type=?` only). Adding
`occurred_at` as the second column lets the index handle the range too.
Column *order* matters: `event_type` first because it is an equality
match, `occurred_at` second because it is a range — an index can use a
range only on its last consulted column.

*5. How does `EXPLAIN QUERY PLAN` confirm the guess?* It is the whole
proof. You do not have to believe the index helps; you put the words in
front of the query and read `SCAN` turn into `SEARCH`. The covering index
goes one step further — `USING COVERING INDEX` means every column the
query needs is *in the index itself*, so SQLite never touches the table
at all.

**The `TEMP B-TREE` lines are the part no index here removes, and that is
worth noticing.** Every plan still says `USE TEMP B-TREE FOR GROUP BY`
and `FOR ORDER BY`. The indexes speed up *finding* the rows; the grouping
and the final sort-by-count still happen in a temporary structure,
because the query orders by `COUNT(*)`, a value that does not exist until
after the grouping. That honesty — seeing exactly what an index does and
does not fix — is the difference between cargo-culting indexes and
understanding them.

## Run it

Copy the worked answer on this page into `problem-04-query-optimizer.py` and run it:
and run it:

```bash
python problem-04-query-optimizer.py
```

It builds the `events` table in memory, seeds it deterministically, and
walks the four indexing stages — printing each query plan and the
answer — then throws the database away. Per-stage timings go to stderr;
nothing is written to disk.

Your written hand-in, `notes.md`, is the five answers above in prose. The
script is what lets you write them from observation instead of from
faith.

## Common bugs to catch

- **The output changes every day.** You left `DATE('now', '-30 days')` in
  the query. Pin a report date and bind the cutoff as a parameter so the
  window is fixed.
- **The winning users change every run.** You seeded with `random`. Derive
  each row from its loop index so every machine builds the identical
  table.
- **`SEARCH` never appears, even with the index.** The index columns do
  not match the query's filter, or you indexed `occurred_at` first and
  `event_type` second — putting the range column ahead of the equality
  column, which the planner cannot use as well. Equality columns come
  first in a composite index.
- **`EXPLAIN QUERY PLAN` returns nothing / raises.** You ran it on a
  statement that is not a query, or forgot the space:
  `"EXPLAIN QUERY PLAN" + QUERY` glues the words together. Note the
  trailing space in `"EXPLAIN QUERY PLAN " + QUERY`.
- **You conclude the index made the query "correct".** It did not — the
  answer was already correct, just slow. If your ten rows changed when you
  added an index, you have a real bug, because an index must be invisible
  to the result.

## Under the hood

<details>
<summary>Under the hood — what a B-tree index actually is, and why order matters</summary>

An index is a second copy of some columns, kept sorted in a **B-tree** —
a shallow, wide tree the database can binary-search. Ask for
`event_type = 'login'` and it walks a handful of tree nodes to the block
of login entries, instead of reading a million rows. That is the whole
trick: sorted data is searchable in *log* time; unsorted data is not
searchable at all, only scannable.

For a *composite* index on `(event_type, occurred_at)`, picture a phone
book sorted by last name, then first name. Finding everyone named
"Turing" is instant — that is the first column. Finding everyone named
"Turing" whose first name is between "A" and "F" is also fast, because
within the Turings the first names are in order — that is the second
column, used as a range.

Now reverse it: a book sorted by *first* name, then last name. Finding
all the Turings means checking every page, because the Turings are
scattered under every first name. That is exactly why column order in a
composite index is not cosmetic: **equality columns first, then at most
one range column.** The query filters `event_type` by equality and
`occurred_at` by range, so `(event_type, occurred_at)` is right and
`(occurred_at, event_type)` is nearly useless for it.

A **covering** index adds the columns the query *reads* but does not
filter on — here, `user_id`. When every column the query touches lives in
the index, SQLite answers entirely from the index and never opens the
table. `USING COVERING INDEX` in the plan is the database telling you it
got everything it needed from the shortcut and did not walk back to the
main data at all.

</details>

<details>
<summary>Under the hood — why the TEMP B-TREE for the sort is so stubborn</summary>

Every plan in this problem, indexed or not, still shows
`USE TEMP B-TREE FOR ORDER BY`. It is worth understanding why no index
removes it, because it teaches the limit of what indexes do.

The query ends `ORDER BY event_count DESC`, where `event_count` is
`COUNT(*)` — a value that does not exist in any row. It is *computed* by
the `GROUP BY`, one number per user, and only after every login has been
counted. An index sorts stored columns; it cannot pre-sort a total that
has not been calculated yet. So SQLite counts everyone into a temporary
B-tree, then sorts that small result (200 users, not a million rows) to
find the top ten.

This is the right lesson to end on: indexes make **finding rows** fast,
and they are dramatic when a query reads a few rows out of millions. They
do nothing for work that happens *after* the rows are found — grouping,
aggregating, sorting by a computed value. When someone says "I added an
index and it did not help", this is very often why: the slow part was
never the lookup. `EXPLAIN QUERY PLAN` tells you which half you are
in — and that is why you read it before you reach for an index, not
after.

</details>

## Acceptance checklist

- [ ] The table is seeded deterministically; the answer is the same on
      every run.
- [ ] Four plans print: no index, single, composite, covering.
- [ ] `SCAN events` appears with no index and `SEARCH ...` appears with
      the indexes.
- [ ] The covering stage shows `USING COVERING INDEX`.
- [ ] The date is a bound parameter, not `DATE('now', ...)`.
- [ ] The ten-row answer is identical at every stage.
- [ ] Timings, if printed, go to stderr, not stdout.

## Stretch

- **Add a fifth stage that removes the sort.** Can you? Try indexing so
  the `GROUP BY` is served by an index (`(event_type, occurred_at,
  user_id)` already helps the grouping) and watch which `TEMP B-TREE`
  lines disappear and which stay.
- **Measure, do not just plan.** Bump `ROWS` to a million and time each
  stage (the script already times to stderr). Feel the gap between the
  scan and the search grow as the table does — the plan shape was the same
  at 20,000, but the *cost* of the wrong plan explodes.
- **Break column order.** Build the composite as `(occurred_at,
  event_type)` and read the plan. Explain, from the phone-book analogy,
  why the planner uses it far less effectively.
- **Read one page of "Use The Index, Luke"**
  (<https://use-the-index-luke.com/>) on composite indexes, and connect
  its "leftmost prefix" rule to what you saw in the four plans.

Next: [Problem 5 — ORM Relationships](./problem-05-orm-relationships.md),
where SQLAlchemy writes the SQL for you and you model a one-to-many
relationship as Python objects.
