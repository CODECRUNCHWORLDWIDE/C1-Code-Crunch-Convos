# Week 10 — Homework

Six problems, one page each. They are not one long project the way Week 9's
were — each stands alone — but they circle the same two ideas the whole week is
built on: **send the question to the database instead of fetching the data and
answering it yourself,** and **every value goes into SQL through a `?`
placeholder, never an f-string.** Design a schema, migrate it, load a file into
it, make a query fast, reach it through an ORM, and back it up safely — and by
the end you have touched a database from every angle a small app needs.

Each shipped answer runs **offline and unattended**. A database program usually
wants a file on disk and a few commands typed at it; these do not. Every answer
builds its own database in a temporary folder or in memory, drives itself, prints
what happened, and cleans up — so `python <name>.py` finishes on its own and
prints the same thing on any machine. Each page shows the one-line change that
points it back at a real database file you keep.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the query receives and
   what it should send back — half the bugs this week are answered by naming the
   shape of the result before you write it.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block, character for character.
5. Only then read The Solution and Why it works.

Five of the six need nothing but the standard library — `sqlite3` ships with
Python — and those five say so on the page: you can solve them in the browser
with no install. Only Problem 5 reaches for a third-party package (SQLAlchemy),
so it is the one that wants a real `pip install`.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Design an e-commerce schema](./problem-01-ecommerce-schema.md) | Tables, keys, and constraints that make bad data impossible to store | Intermediate | 45 min |
| 2 | [A migration script](./problem-02-migration-script.md) | Changing a table that already holds live rows, atomically, losing none | Intermediate | 45 min |
| 3 | [CSV → SQLite importer](./problem-03-csv-importer.md) | Loading a file you did not write — and the one thing a `?` cannot carry | Intermediate | 45 min |
| 4 | [Query optimizer puzzle](./problem-04-query-optimizer.md) | Why a query is slow, which index fixes it, and seeing the plan change | Intermediate | 45 min |
| 5 | [ORM relationships](./problem-05-orm-relationships.md) | One-to-many as Python objects, letting SQLAlchemy write the SQL | Intermediate | 45 min |
| 6 | [Backup and restore script](./problem-06-backup-restore.md) | Snapshotting a live database safely, with honest exit codes | Intermediate | 1 hr |

Total target time: about 5 hours. The [week schedule](../README.md) leaves
Saturday and Sunday for the homework, and both numbers are honest — the figures
here are how long a problem takes when it goes well, and the schedule allows for
getting stuck and reading back over the lecture notes.

**Problem 3 carries the week's sharpest lesson, and it is easy to miss.** A `?`
placeholder protects every *value* you send to SQL, but it cannot carry a table
or column *name* — and that gap is where a whole class of injection bugs lives.
Read how that problem sanitises a name before you copy the pattern anywhere.

## What you hand in

Six scripts (and a couple of `.sql` and `.md` files) of your own, one per
problem, named as each page tells you — not the `-solution.py` names, which
belong to the published answers. Keep them together in a folder called
`homework/` inside your fork:

```text
homework/
    problem-01-ecommerce-schema.sql      (or .py, per the page)
    problem-02-migration-script.sql
    problem-03-csv-importer.py
    problem-04-query-optimizer.md        (a short write-up)
    problem-05-orm-relationships.py
    problem-06-backup-restore.py
```

House rules the same everywhere:

- **Every Python file uses type hints** on every signature, a module docstring
  with an example invocation, and narrow `except` clauses — never a bare
  `except:`.
- **Every SQL file is readable:** uppercase keywords, one column per line in a
  long `SELECT`, `JOIN` and `WHERE` clauses indented.
- **No value is ever f-strung into SQL.** Every value travels as a bound `?`
  parameter. This is the one rule the week refuses to bend on, and it is the
  first thing a reviewer looks for.

When you are done, push the `homework/` folder to a public GitHub repo and share
the link. Reviewing it, we will:

- Run the SQL files against a fresh SQLite database.
- Run each Python script.
- Read your write-up for Problem 4.
- Look for f-strings in SQL — there should be none.

Have fun. The next time you see a `.json` file pretending to be a database,
you will know exactly what to do.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference is the bug — read it rather than guessing, and when a query surprises
you, open the SQLite shell (`python -m sqlite3 your.db`), run the `SELECT` by
hand, and look at the rows before you wrap it back in Python.
