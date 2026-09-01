# Exercise 2 — Parameterized Queries

> **Topic:** Watch SQL injection happen on your own throwaway file, then close it with `?` placeholders
> **Lecture:** [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md), section 5
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** you will read the words "always parameterize" in a hundred places and they will not stick until you have watched a single apostrophe hand over an entire table. Once you have seen it, f-strings in SQL start to look wrong on sight, and that reflex is the whole point. This is the exercise that protects the users of everything you build after Week 10.

## Read this before you run anything

This exercise attacks a database file that **you create, on your own
machine, in your own folder**, seeded with four made-up members. It is
built to be destroyed — delete `injection_demo.db` and it is gone. Nothing
here touches a network, a server, or a machine belonging to anyone else.

You are being shown the attack so that you recognise the vulnerable
pattern in your own code and remove it. Running this technique against any
system you do not own is a crime in most countries and gets you thrown out
of this community. The defence is the deliverable; the attack is only here
because the defence does not make sense without it.

## The Brief

A community org keeps a `members` table with names, emails, and a member
code. Someone has written the obvious "look up a member by name" feature:
take what the user typed, drop it into a SQL string with an f-string, run
it. It works. Every test passes. The demo goes fine. Then someone types
`' OR '1'='1` into the search box.

Your job is to build both versions of that lookup — the broken one and the
fixed one — and run the same hostile string through each. Same input, same
table, two very different outcomes. Then you will try a nastier input that
tries to drop the table, and discover that Python's `sqlite3` module blocks
it for a reason that has nothing to do with your code being safe.

## Starter

Create `exercise-02-parameterized.py` in your practice repo.

```python
"""exercise-02-parameterized.py — see SQL injection, then prevent it.

Runs against a throwaway local file, injection_demo.db, which this script
creates and destroys. Never point this technique at a system you do not own.
"""

import sqlite3
from typing import Final

DB_PATH: Final[str] = "injection_demo.db"

SCHEMA: Final[str] = """
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    secret_code TEXT NOT NULL
);
"""

MEMBERS: Final[list[tuple[str, str, str]]] = [
    ("Ada Lovelace",      "ada@example.com",       "CC-1001"),
    ("Grace Hopper",      "grace@example.com",     "CC-1002"),
    ("Alan Turing",       "alan@example.com",      "CC-1003"),
    ("Katherine Johnson", "katherine@example.com", "CC-1004"),
]

HOSTILE_INPUT: Final[str] = "' OR '1'='1"
DROP_ATTEMPT: Final[str] = "'; DROP TABLE members; --"


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild the demo table from scratch and insert the four members."""
    conn.executescript(SCHEMA)
    # TODO: executemany an INSERT with three ? placeholders over MEMBERS
    conn.commit()


def unsafe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the wrong way. Never write this in real code.

    Builds the query by string formatting, so the caller's text becomes
    part of the SQL instead of staying a value.
    """
    query: str = ...  # TODO: f"SELECT id, name, email FROM members WHERE name = '{name}'"
    print(f"Query sent: {query}")
    # TODO: conn.execute(query) and return fetchall()
    return []


def safe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the right way, with a bound parameter."""
    query: Final[str] = "SELECT id, name, email FROM members WHERE name = ?"
    print(f"Query sent: {query}")
    print(f'Parameter: "{name}"')
    # TODO: conn.execute(query, (name,)) and return fetchall()
    return []


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    """Return True if a table with this name is in the schema."""
    # TODO: SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?
    return False


def show(rows: list[tuple[int, str, str]]) -> None:
    """Print a row count and then each row."""
    print(f"{len(rows)} row(s) returned.")
    for row in rows:
        print(f"  {row}")


def main() -> None:
    """Run the same two inputs through the broken and the fixed lookup."""
    conn = sqlite3.connect(DB_PATH)
    try:
        seed(conn)
        print(f"Seeded {DB_PATH} with {len(MEMBERS)} members.")

        print("\n--- Unsafe lookup: normal input ---")
        show(unsafe_lookup(conn, "Ada Lovelace"))

        print("\n--- Unsafe lookup: hostile input ---")
        show(unsafe_lookup(conn, HOSTILE_INPUT))
        print("The whole table leaked. One quote did that.")

        print("\n--- Safe lookup: same hostile input, ? placeholder ---")
        show(safe_lookup(conn, HOSTILE_INPUT))
        print("Nothing matched, because the input was treated as a name, not as SQL.")

        print("\n--- Multi-statement attempt through execute() ---")
        try:
            unsafe_lookup(conn, DROP_ATTEMPT)
        except sqlite3.ProgrammingError as exc:
            print(f"sqlite3.ProgrammingError: {exc}")
        print("execute() refuses a second statement. That is a seatbelt, not a fix:")
        print("the leak above needed only one statement.")

        print(f"\nmembers table still present: {table_exists(conn, 'members')}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

## Requirements

1. `seed` inserts all four members with an `executemany` and three `?`
   placeholders, then commits.
2. `unsafe_lookup` builds its query with an f-string. This is the one place
   in the entire bootcamp where that is allowed, and only because the
   failure is the lesson.
3. `safe_lookup` uses the `?` placeholder and passes `(name,)` — with the
   trailing comma — as the parameter tuple.
4. The hostile input `' OR '1'='1` returns **4 rows** through the unsafe
   path and **0 rows** through the safe path. Same string, same data.
5. `table_exists` queries `sqlite_master` with two bound parameters and
   returns a real `bool`, not the raw count.
6. After the drop attempt, the final line prints
   `members table still present: True`.
7. The `secret_code` column is never selected. It is there to make the
   point that a leak gives away whatever is in the row, not just what the
   feature was meant to show.

## Constraints

- **The f-string lives in exactly one function, and that function's
  docstring says never to write it.** Do not let the pattern spread to
  `seed` or `table_exists`. If you catch yourself formatting a second
  query, you have learned the wrong half of the lesson.
- **Use `?`, not `.format()`, `%`, or `+`, in every other query.** All four
  build the same kind of string; the database cannot tell which one you
  used and neither can the attacker. Only a bound parameter is sent to
  SQLite separately from the SQL text, and that separation is the defence.
- **Do not "fix" the unsafe version by escaping quotes yourself.** Every
  hand-rolled escaper has a hole — doubled quotes, backslashes, Unicode
  lookalikes, numeric contexts with no quotes at all. Parameter binding is
  not a better escaper; it means the value is never parsed as SQL at all.
- **Commit after seeding and close in a `finally`.** Without the commit,
  `sqlite3` rolls the inserts back when the connection closes, silently and
  with no traceback — your unsafe lookup would then leak an empty table and
  you would draw the wrong conclusion from a clean-looking run.
- **`executescript` is used only on the trusted `SCHEMA` constant.** It
  runs multiple statements, which is exactly the door `execute` keeps shut.
  Never hand it a string with user input anywhere in it. Delete
  `injection_demo.db` when you are done, and keep `*.db` in `.gitignore`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-parameterized-solution.py
Seeded injection_demo.db with 4 members.

--- Unsafe lookup: normal input ---
Query sent: SELECT id, name, email FROM members WHERE name = 'Ada Lovelace'
1 row(s) returned.
  (1, 'Ada Lovelace', 'ada@example.com')

--- Unsafe lookup: hostile input ---
Query sent: SELECT id, name, email FROM members WHERE name = '' OR '1'='1'
4 row(s) returned.
  (1, 'Ada Lovelace', 'ada@example.com')
  (2, 'Grace Hopper', 'grace@example.com')
  (3, 'Alan Turing', 'alan@example.com')
  (4, 'Katherine Johnson', 'katherine@example.com')
The whole table leaked. One quote did that.

--- Safe lookup: same hostile input, ? placeholder ---
Query sent: SELECT id, name, email FROM members WHERE name = ?
Parameter: "' OR '1'='1"
0 row(s) returned.
Nothing matched, because the input was treated as a name, not as SQL.

--- Multi-statement attempt through execute() ---
Query sent: SELECT id, name, email FROM members WHERE name = ''; DROP TABLE members; --'
sqlite3.ProgrammingError: You can only execute one statement at a time.
execute() refuses a second statement. That is a seatbelt, not a fix:
the leak above needed only one statement.

members table still present: True
```

Read the second `Query sent:` line slowly. The apostrophe the user typed
closed the string literal you opened, and `OR '1'='1'` became part of the
`WHERE` clause. The condition is now true for every row, so every row comes
back. Nothing was hacked. The database did exactly what the query said.

## Steps

1. Create the file and fill in `seed` first. Run it; you should get the
   seeded line and then three empty result sets.
2. Fill in `unsafe_lookup`. Run it and confirm the normal input returns one
   row before you try the hostile one.
3. Run the hostile input. Copy the printed query into a text editor and
   line up the quotes by hand until you can explain, out loud, why the
   `WHERE` clause is now always true.
4. Fill in `safe_lookup`. Run it. Same string, zero rows. Notice that the
   `Query sent:` line no longer changes shape when the input changes — that
   is the property you are buying.
5. Fill in `table_exists` and confirm the final line prints `True`.
6. See the seatbelt fail: swap `conn.execute(query)` for
   `conn.executescript(query)` inside `unsafe_lookup`, rerun, and watch
   `table_exists` print `False`. Change it straight back, then delete
   `injection_demo.db`. That is the whole argument against passing user
   input to `executescript`.

## The Solution

```python
"""exercise-02-parameterized-solution.py — see SQL injection, then prevent it.

Runs against a throwaway local file, injection_demo.db, which this script
creates and destroys. Never point this technique at a system you do not own.

Your own exercise-02-parameterized.py keeps injection_demo.db in the folder
you run it from and asks you to delete it afterwards. This shipped answer
runs the same code inside a temporary folder that is deleted on the way out,
so the deletion step is built in. The lookups are the whole exercise and know
nothing about the harness.

Run it with::

    python exercise-02-parameterized-solution.py
"""

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Final

DB_PATH: Final[str] = "injection_demo.db"

SCHEMA: Final[str] = """
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    secret_code TEXT NOT NULL
);
"""

MEMBERS: Final[list[tuple[str, str, str]]] = [
    ("Ada Lovelace",      "ada@example.com",       "CC-1001"),
    ("Grace Hopper",      "grace@example.com",     "CC-1002"),
    ("Alan Turing",       "alan@example.com",      "CC-1003"),
    ("Katherine Johnson", "katherine@example.com", "CC-1004"),
]

HOSTILE_INPUT: Final[str] = "' OR '1'='1"
DROP_ATTEMPT: Final[str] = "'; DROP TABLE members; --"


def seed(conn: sqlite3.Connection) -> None:
    """Rebuild the demo table from scratch and insert the four members."""
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO members (name, email, secret_code) VALUES (?, ?, ?)",
        MEMBERS,
    )
    conn.commit()


def unsafe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the wrong way. Never write this in real code.

    Builds the query by string formatting, so the caller's text becomes
    part of the SQL instead of staying a value.
    """
    query: str = f"SELECT id, name, email FROM members WHERE name = '{name}'"
    print(f"Query sent: {query}")
    return conn.execute(query).fetchall()


def safe_lookup(conn: sqlite3.Connection, name: str) -> list[tuple[int, str, str]]:
    """Look up a member the right way, with a bound parameter."""
    query: Final[str] = "SELECT id, name, email FROM members WHERE name = ?"
    print(f"Query sent: {query}")
    print(f'Parameter: "{name}"')
    return conn.execute(query, (name,)).fetchall()


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    """Return True if a table with this name is in the schema."""
    cursor = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?",
        ("table", table),
    )
    return cursor.fetchone()[0] > 0


def show(rows: list[tuple[int, str, str]]) -> None:
    """Print a row count and then each row."""
    print(f"{len(rows)} row(s) returned.")
    for row in rows:
        print(f"  {row}")


def main() -> None:
    """Run the same two inputs through the broken and the fixed lookup."""
    conn = sqlite3.connect(DB_PATH)
    try:
        seed(conn)
        print(f"Seeded {DB_PATH} with {len(MEMBERS)} members.")

        print("\n--- Unsafe lookup: normal input ---")
        show(unsafe_lookup(conn, "Ada Lovelace"))

        print("\n--- Unsafe lookup: hostile input ---")
        show(unsafe_lookup(conn, HOSTILE_INPUT))
        print("The whole table leaked. One quote did that.")

        print("\n--- Safe lookup: same hostile input, ? placeholder ---")
        show(safe_lookup(conn, HOSTILE_INPUT))
        print("Nothing matched, because the input was treated as a name, not as SQL.")

        print("\n--- Multi-statement attempt through execute() ---")
        try:
            unsafe_lookup(conn, DROP_ATTEMPT)
        except sqlite3.ProgrammingError as exc:
            print(f"sqlite3.ProgrammingError: {exc}")
        print("execute() refuses a second statement. That is a seatbelt, not a fix:")
        print("the leak above needed only one statement.")

        print(f"\nmembers table still present: {table_exists(conn, 'members')}")
    finally:
        conn.close()


def run_in_throwaway_folder() -> None:
    """Run main() inside a temporary folder that is deleted afterwards.

    DB_PATH is relative, so the demo database lands in the current folder.
    Moving into a temporary folder first means the file this attack runs
    against is created for the run and destroyed with it.
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

**The two lookups differ by one line, and that line is the entire lesson.**
`unsafe_lookup` glues the name into the query with an f-string, so the name
becomes part of the sentence SQLite reads. `safe_lookup` writes the sentence
once with a `?` where the name goes, and hands the name over beside it. Same
table, same columns, same four members. One leaks; one does not.

**Picture a printed form with a blank box.** The safe query is that form:
*find the member whose name is ______*. Whatever you write in the box is a
name — even if you write "or everybody", it is still just a name, and nothing
matches it. The unsafe query has no box. You are handing SQLite a sentence you
assembled yourself, so any punctuation the user typed is punctuation SQLite
obeys. The `'` closes the quote you opened, `OR '1'='1` bolts on a condition
that is true for every row, and the trailing `'` tidies up the end. Look at
the printed query in the output: `WHERE name = '' OR '1'='1'`. Perfectly
sensible SQL. Every row comes back.

**Nothing was hacked.** The database was never tricked; it read a valid query
and answered it correctly. The *program* was tricked — it built a question it
did not mean to ask. That is why "escape the quotes better" is the wrong fix
and `?` is the right one.

**`(name,)` needs that comma.** In `safe_lookup` the parameters go in a tuple,
and a one-item tuple in Python is written with a trailing comma. Drop it and
you have passed a plain string; `sqlite3` then walks the string and offers
each character as its own parameter, which is where the "uses 1, and there are
11 supplied" error comes from.

**`table_exists` asks the database about itself.** `sqlite_master` is a table
SQLite keeps that lists every table in the file, so counting rows there tells
you whether `members` survived. Notice the table name travels as a `?` too. It
is text that came in from outside this function, and there is no "this one is
obviously safe" exception — that exception is how the habit dies.

**The drop attempt fails, but not for a reason you can rely on.**
`conn.execute()` runs exactly one statement, so `'; DROP TABLE members; --`
comes back as `ProgrammingError` and the table survives. That is a seatbelt
Python's `sqlite3` bolted on, not a defence you built. The leak two blocks
above needed only one statement and sailed straight through it. Step 6 proves
the point: swap in `executescript`, which happily runs several statements, and
the table is gone.

**`secret_code` is never selected, and it still matters.** It sits in every
row the unsafe lookup leaked. A widened `SELECT`, a `SELECT *`, or a slightly
cleverer injected query and it comes out too. A leak gives away what is in the
row, not what the feature meant to show.

**Why the shipped file differs from yours.** Your
`exercise-02-parameterized.py` leaves `injection_demo.db` in the folder you run
it from and asks you to delete it afterwards. The shipped answer runs the same
`main` inside a temporary folder that is deleted on the way out, so the
clean-up is built in. The lookups — the actual exercise — are identical.

<details>
<summary>Under the hood — why a bound parameter can never turn into SQL</summary>

When you call `conn.execute(query, params)`, SQLite does the work in two
separate passes, and the order is the whole defence.

First it **prepares** the statement: it parses the SQL text, checks the
grammar, resolves the table and column names, and compiles the result into a
little program for its internal virtual machine. Each `?` becomes a numbered
slot in that program — a hole the plan knows about, sized and shaped and
already decided.

Only then does it **bind**: your values are copied into those slots as data.
The parser has already finished and gone home. There is no second pass over
the text, so there is no moment at which `' OR '1'='1` could be read as
grammar. It is a string sitting in slot 1, and a string in a slot compares
equal to a name or it does not.

The f-string version collapses those two passes into one. By the time SQLite
starts parsing, the user's text is already inside the sentence, indistinguishable
from the parts you wrote. Everything after that is SQLite doing its job
correctly on the wrong question.

There is a bonus. Because the prepared plan does not depend on the values,
the same plan can be reused with different values — which is why
`executemany` with one query and four rows is faster than four separate
queries. The safe habit and the fast habit are the same habit.

</details>

## Download and run

Download
[exercise-02-parameterized-solution.py](./exercise-02-parameterized-solution.py)
and run it:

```bash
python exercise-02-parameterized-solution.py
```

Standard library only. It builds `injection_demo.db` inside a throwaway
folder, runs the attack against that file and nothing else, and deletes the
folder on the way out — so the "delete the demo database" step is already
done for you. The `-solution` in the name keeps it from colliding with your
own `exercise-02-parameterized.py`.

## Common bugs to catch

- **The hostile input returns 0 rows from the unsafe lookup too.** You
  parameterized both functions. Check that `unsafe_lookup` really does use
  the f-string — if `?` appears anywhere in it, the exercise has no teeth.
- **`sqlite3.OperationalError: unrecognized token: "'"`.** Your f-string is
  missing one of the single quotes around `{name}`. The broken query has to
  be broken in the specific way real broken code is: quoted.
- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The
  current statement uses 1, and there are 11 supplied.`** In `safe_lookup`
  you passed `name` instead of `(name,)`. Python iterated the string and
  offered each character as a parameter. The trailing comma is what makes
  it a tuple.
- **`sqlite3.OperationalError: no such table: members` on the second run.**
  You ran the `executescript` swap from step 6 and never put it back. Rerun
  the script; `SCHEMA` starts with `DROP TABLE IF EXISTS` and rebuilds.
- **`table_exists` returns `1` instead of `True`.** `COUNT(*)` gives you an
  integer. The signature promises a `bool`, so compare or cast — and note
  that f-string interpolation of the table name here would have been
  another injection point, which is why it is a parameter.
- **`sqlite3.Warning: You can only execute one statement at a time.`
  instead of `ProgrammingError`.** You are on an older Python. The lesson
  is the same; widen the `except` clause to `(sqlite3.ProgrammingError,
  sqlite3.Warning)` and carry on.

## Acceptance checklist

- [ ] The unsafe lookup returns 4 rows for `' OR '1'='1` and you can explain the resulting SQL out loud.
- [ ] The safe lookup returns 0 rows for the same input.
- [ ] Every query except the one inside `unsafe_lookup` uses `?` placeholders.
- [ ] The drop attempt is caught and the final line prints `members table still present: True`.
- [ ] `seed` commits, and the connection closes in a `finally` block.
- [ ] You deleted `injection_demo.db` and `*.db` is in your `.gitignore`.
- [ ] The file is committed to Git with a message like `Add Week 10 exercise 2: parameterized queries`.

## Stretch

- Rewrite `safe_lookup` with a named placeholder — `WHERE name = :name` and
  a `{"name": name}` dictionary. Confirm the behaviour is identical, then
  decide which style you prefer for queries with five parameters.
- Add a `search(conn, fragment)` function using `WHERE name LIKE ?` with the
  parameter `f"%{fragment}%"`. The wildcards belong in the *value*, not in
  the SQL — building the pattern in Python and binding it is still safe.
- Write `sorted_members(conn, direction)` that must vary `ASC`/`DESC`, which
  cannot be parameterized. Validate against a set of two allowed strings and
  raise `ValueError` otherwise, as in Lecture 3 section 5. Then read the
  OWASP page linked at the end of that lecture.

Next up, two tables and the query that connects them:
[Exercise 3 — Joining Users and Posts](./exercise-03-joins.md).
