# Week 10 Exercises

Five short exercises that take you from "hello, table" to "I built a thing with the ORM". Do them in order; each one builds on the previous habits.

## How to run

Each exercise is a self-contained Python script. From this folder:

```bash
python exercise-01-first-table.py
```

The first four use only the standard library — no `pip install` required. Exercise 5 needs SQLAlchemy:

```bash
pip install sqlalchemy
```

Each script creates its own `.db` file in the current directory. If you want a clean slate, just delete the file and rerun.

## The exercises

| # | File                                | What you'll practice                                                  |
|---|-------------------------------------|-----------------------------------------------------------------------|
| 1 | `exercise-01-first-table.py`        | Connect, create a table, insert rows, select them, print.             |
| 2 | `exercise-02-parameterized.py`      | See SQL injection in action; fix it with parameterization.            |
| 3 | `exercise-03-joins.py`              | Two tables (`users`, `posts`), insert sample data, run an INNER JOIN. |
| 4 | `exercise-04-aggregate.py`          | `GROUP BY` totals over a sales table.                                 |
| 5 | `exercise-05-sqlalchemy-basic.py`   | Reimplement Exercise 1 using the SQLAlchemy ORM.                      |

## What to look for

- Read the comments — there's at least as much teaching in the comments as in the code.
- Every value passed into SQL goes through a `?` placeholder. Get used to seeing it.
- Run each script, then **change something** — add a column, change a `WHERE` clause, break the schema — and re-run. The fastest way to learn is to make small modifications and see what happens.

When you finish all five, tackle one of the challenges in `../challenges/`.
