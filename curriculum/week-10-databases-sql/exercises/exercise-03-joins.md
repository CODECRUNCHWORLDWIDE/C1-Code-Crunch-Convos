# Exercise 3 — Joining Users and Posts

> **Topic:** Two tables, a foreign key, and an `INNER JOIN` that puts them back together
> **Lecture:** [02 — JOINs and Aggregations](../lecture-notes/02-joins-and-aggregations.md), sections 1–4
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** a single table is a spreadsheet. The moment you have two tables and a foreign key between them, you have a *database*, and the join is the only way to ask a question that spans both. Every real schema you meet after this week is three or more tables, and the mini-project on Friday joins two of them on the first screen.

## The Brief

You are building the data layer for a small community blog. Two tables:
`users`, one row per person, and `posts`, one row per article. A post
belongs to exactly one user, and that ownership is stored as `posts.user_id`
pointing at `users.id` — a foreign key.

Storing the author's name inside every post row would be simpler for about
a week, right up until someone changes their display name and you have to
rewrite it in forty places. Instead the name lives in one row in one table
and the join fetches it on demand — a little work at read time in exchange
for one authoritative copy of every fact.

Four users are in the seed data and only three have written anything. That
fourth user is not padding. `INNER JOIN` will drop them, and noticing *why*
is half of what this exercise teaches.

## Starter

Create `exercise-03-joins.py` in your practice repo.

```python
"""exercise-03-joins.py — two tables, one foreign key, one INNER JOIN.

Builds a tiny community blog in blog.db and lists every post next to the
name of the person who wrote it.
"""

import sqlite3
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


def connect() -> sqlite3.Connection:
    """Open the database with foreign-key enforcement switched on."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild both tables and insert the seed rows."""
    conn.executescript(SCHEMA)
    # TODO: executemany USERS into users (username, joined_on)
    # TODO: executemany POSTS into posts (user_id, title, published_on)
    conn.commit()


def posts_with_authors(conn: sqlite3.Connection) -> list[tuple[str, str, str]]:
    """Return (published_on, username, title) for every post with an author."""
    # TODO: SELECT p.published_on, u.username, p.title
    #       FROM posts AS p
    #       INNER JOIN users AS u ON p.user_id = u.id
    #       ORDER BY p.published_on
    return []


def posts_since(conn: sqlite3.Connection, cutoff: str) -> list[tuple[str, str, str]]:
    """Same join, filtered to posts published on or after `cutoff`."""
    # TODO: the same query with WHERE p.published_on >= ?
    #       The date is a bound parameter, never an f-string.
    return []


def post_count(conn: sqlite3.Connection, username: str) -> int:
    """Return how many posts a given user has written."""
    # TODO: COUNT(*) over the same join, WHERE u.username = ?
    return 0


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


if __name__ == "__main__":
    main()
```

## Requirements

1. `seed` inserts the users **before** the posts. The posts carry
   `user_id` values of 1, 2 and 3, and with foreign keys enforced those
   users have to exist first.
2. Both joins use table aliases (`posts AS p`, `users AS u`) and name their
   columns. No `SELECT *`.
3. `posts_with_authors` returns 5 rows ordered by `published_on` ascending.
4. `posts_since` takes the cutoff as a bound parameter and returns 3 rows.
5. `post_count('devon')` returns `0`, and `devon` appears in none of the
   joined output.
6. The join condition is `p.user_id = u.id`. Joining `p.id = u.id` also
   runs, also returns rows, and is wrong — see the Constraints.
7. The output matches the Expected output block exactly, including the two
   spaces after the date and the seven-column username field.

## Constraints

- **Enable `PRAGMA foreign_keys = ON` on every connection, and insert
  parents before children.** SQLite ships with foreign-key enforcement
  *off* for backwards compatibility, and the pragma is per-connection, not
  stored in the file. Declaring `FOREIGN KEY` in your schema and never
  turning the pragma on gives you documentation, not a guarantee: SQLite
  will happily accept a post owned by user 99. With it on, a post whose
  `user_id` has no matching user raises at insert time — that error is the
  feature working, not a bug to route around.
- **Join on `p.user_id = u.id`, never on `p.id = u.id`.** Both columns are
  integers, both joins execute, and the wrong one returns five rows of
  confident nonsense — post 1 credited to user 1, post 2 to user 2 — which
  even looks plausible with this seed data. A join that runs is not a join
  that is right. Check that the two columns you name are the foreign key
  and the primary key it points at.
- **Use `INNER JOIN` here even though `LEFT JOIN` returns more rows.** The
  question is "who wrote each post", and a post with no author is not an
  answer to it. Reach for `LEFT JOIN` when the question is "every user, and
  their posts if any" — that is the stretch task.
- **Store dates as ISO-8601 strings (`2026-03-05`).** SQLite has no date
  type, and ISO-8601 is the one text format where alphabetical sorting and
  chronological sorting are the same thing. Store `03/05/2026` and your
  `ORDER BY` silently sorts by month.
- **Commit after seeding, and close in a `finally`.** `sqlite3` opens a
  transaction for your inserts but never ends one. Skip the commit and the
  rows are discarded when the connection closes — no exception, no warning,
  just an empty join result that looks like a broken query.
- **Every value in a `WHERE` clause is a `?` parameter.** The cutoff date is
  a constant in your own file today. It will be a query-string argument the
  first time this becomes a web page.

## Expected output

```text
$ python exercise-03-joins.py
Seeded blog.db: 4 users, 5 posts.

Every post with its author (INNER JOIN):
2026-03-01  anaya   Reading a query plan out loud
2026-03-02  marcus  Why my JSON file finally broke
2026-03-05  anaya   Three things WHERE will not do
2026-03-06  priya   A foreign key saved my weekend
2026-03-11  marcus  Indexes are not magic
5 rows.

Posts published on or after 2026-03-05:
2026-03-05  anaya   Three things WHERE will not do
2026-03-06  priya   A foreign key saved my weekend
2026-03-11  marcus  Indexes are not magic
3 rows.

devon has 0 posts and does not appear above. INNER JOIN dropped that row.
```

Four users went in and three come out. The join produced one row per
*match*, and `devon` matched nothing.

## Steps

1. Create the file and fill in `seed`. Run it and confirm the seeded line
   before writing any join.
2. Look at the raw tables by hand: `python -m sqlite3 blog.db`, then
   `SELECT * FROM posts;` and `SELECT * FROM users;`. Trace one `user_id`
   to its user with your finger before you make SQL do it.
3. Write `posts_with_authors`. Run it. Five rows, oldest first.
4. Write `posts_since`. Note that `>=` includes the 5th, so three rows come
   back, not two. Then write `post_count` and confirm `devon` reports 0.
5. Break it on purpose: change the join condition to `p.id = u.id` and
   rerun. You still get rows. Read them and work out which authors are now
   wrong. Change it back.
6. Delete `blog.db` and run clean.

## The Solution

```python
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
```

**Why it works.**

**A join is the lookup you would do with your finger, written down once.**
Each post row carries a `user_id`, and that is all it carries — a number.
To find out who wrote the post you slide your finger over to the `users`
table and stop at the row whose `id` is that number.
`INNER JOIN users AS u ON p.user_id = u.id` is that finger movement spelled
out in words, and the database performs it for all five posts in one pass.

**Foreign keys are only enforced if you ask, on every connection.**
`connect()` runs `PRAGMA foreign_keys = ON` the moment the database opens.
That setting lives on the connection, not in the file, so a new connection
starts with it off again. Without it, `FOREIGN KEY (user_id) REFERENCES
users(id)` in the schema is a comment with good intentions — SQLite would
accept a post owned by user 99 and never say a word.

**The three queries are constants, so the functions are two lines each.**
`POSTS_WITH_AUTHORS_SQL`, `POSTS_SINCE_SQL` and `POST_COUNT_SQL` sit at the
top as plain triple-quoted strings with the clauses stacked one per line.
Underneath, each function just runs its constant and hands back the rows.
When a query is wrong there is exactly one place to fix it, and you can
paste the constant straight into the SQLite shell without unpicking it from
Python.

**The `?` is a slot for a value, not a hole in the wall.** `posts_since`
passes the date as `(cutoff,)` beside the query. SQLite drops the *value*
into the slot and never treats it as SQL to run. Glue the same date in with
an f-string and the day that date arrives from a web form, whatever is
typed into that form becomes part of your query. The `?` is what stops
that, and it costs nothing.

**`INNER JOIN` keeps only matches, which is exactly why `devon` is
missing.** Devon has a row in `users` and no rows in `posts`. An inner join
asks the two tables to pair up, and a row with no partner does not make it
into the result. `post_count(conn, 'devon')` runs the same join with a
`COUNT(*)` on top and gets `0` — that is the size of an empty result, which
is an honest answer, not a broken query.

**The shipped answer runs in a throwaway folder so it cannot tread on your
work.** `DB_PATH` is `"blog.db"` with no folder in front of it, so the
database appears wherever you are standing when you run the file.
`run_in_throwaway_folder` steps into a temporary directory first, calls
`main`, then steps back out and lets the directory be deleted. Your own
`exercise-03-joins.py` should *not* do this — you want `blog.db` left in
your folder so you can open it in the SQLite shell and trace the join by
hand. That wrapper is packaging around the exercise, not part of it.

## Download and run

Download [exercise-03-joins-solution.py](./exercise-03-joins-solution.py)
and run it:

```bash
python exercise-03-joins-solution.py
```

Nothing to install — `sqlite3` ships with Python. It builds the blog,
prints the three sections above, and takes its database with it on the way
out, so your folder ends up exactly as it started.

Your own file is `exercise-03-joins.py`. The `-solution` in the download's
name is what keeps the shipped answer from landing on top of the work you
did.

## Common bugs to catch

- **`sqlite3.IntegrityError: FOREIGN KEY constraint failed`.** You inserted
  posts before users, or a `user_id` in `POSTS` does not match a real user.
  With the pragma on, this fires at insert time — which is exactly when you
  want to hear about it.
- **`sqlite3.OperationalError: ambiguous column name: id`.** Both tables
  have an `id`, so a bare `id` in your `SELECT` or `ORDER BY` is a coin
  flip the parser refuses to make. Qualify it: `p.id` or `u.id`.
- **`sqlite3.OperationalError: no such column: u.name`.** The column is
  `username`. Ninety percent of database bugs are a mistyped column name,
  and the error tells you the exact one.
- **You get 20 rows instead of 5.** Your `ON` clause is missing, so SQLite
  produced a cross join — every post paired with every user, 5 × 4. If the
  row count is a suspiciously round multiple, look for the missing `ON`.
- **`devon` appears with an empty title.** You wrote `LEFT JOIN` starting
  from `users`. That is a valid query for a different question; this one
  asks about posts.
- **`ValueError: too many values to unpack (expected 3)`.** Your `SELECT`
  returns a different number of columns than `show` unpacks. The column
  list in the query is the contract; keep it to three.
- **`sqlite3.ProgrammingError: You can only execute one statement at a
  time.`** You passed the multi-statement `SCHEMA` to `execute`. It needs
  `executescript`.

## Acceptance checklist

- [ ] `PRAGMA foreign_keys = ON` runs on the connection before any insert.
- [ ] The first join prints 5 rows in date order with the correct author on each.
- [ ] The filtered join prints 3 rows and takes its cutoff as a `?` parameter.
- [ ] `devon` appears nowhere in the joined output and `post_count` reports 0.
- [ ] The join condition is `p.user_id = u.id`, and you can say why `p.id = u.id` is wrong.
- [ ] Seeding commits, and the connection closes in a `finally` block.
- [ ] The file is committed to Git with a message like `Add Week 10 exercise 3: joining users and posts`.

## Stretch

- Add `all_users_with_counts(conn)` using a `LEFT JOIN` from `users` and
  `COUNT(p.id)`, so `devon` finally shows up with `0`. Use `COUNT(p.id)`
  rather than `COUNT(*)`, and work out why the second one gives `devon` a
  count of 1.
- Add a `comments` table with a foreign key to `posts` and chain a
  three-table join: comment text, post title, and author name in one row.
- Try to insert a post with `user_id = 99` and read the error. Then turn the
  pragma off, try again, and see the orphan row land in the table.

Two tables down. Now summarise them:
[Exercise 4 — Aggregating Sales](./exercise-04-aggregate.md).
