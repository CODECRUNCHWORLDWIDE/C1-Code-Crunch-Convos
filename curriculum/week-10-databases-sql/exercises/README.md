# Week 10 Exercises

Five short exercises that take you from "hello, table" to "I built a thing with the ORM". Do them in order; each one builds on the previous habits.

## How to run

Each exercise is a page, not a file you download. Open it, read the brief, then copy its starter block into a real `.py` file in your own practice repo — name it after the exercise — and fill in the `TODO`s. From that folder:

```bash
python exercise-01-first-table.py
```

The first four use only the standard library — no `pip install` required. Exercise 5 needs SQLAlchemy:

```bash
pip install sqlalchemy
```

Each script creates its own `.db` file in the current directory. If you want a clean slate, just delete the file and rerun. Add `*.db` to your `.gitignore` before you commit anything this week.

## The exercises

| # | Exercise | What you'll practice | Difficulty | Est. time |
|---|----------|----------------------|-----------:|----------:|
| 1 | [exercise-01-first-table.md](./exercise-01-first-table.md) | Connect, create a table, insert rows, select them, print. | Beginner | 20 min |
| 2 | [exercise-02-parameterized.md](./exercise-02-parameterized.md) | See SQL injection in action; fix it with parameterization. | Easy | 25 min |
| 3 | [exercise-03-joins.md](./exercise-03-joins.md) | Two tables (`users`, `posts`), insert sample data, run an INNER JOIN. | Easy | 30 min |
| 4 | [exercise-04-aggregate.md](./exercise-04-aggregate.md) | `GROUP BY` totals over a sales table. | Medium | 30 min |
| 5 | [exercise-05-sqlalchemy-basic.md](./exercise-05-sqlalchemy-basic.md) | Reimplement Exercise 1 using the SQLAlchemy ORM. | Medium | 35 min |

## What to look for

- Read the Constraints and Common bugs sections — there's at least as much teaching in those as in the code.
- Every value passed into SQL goes through a `?` placeholder. Get used to seeing it. Exercise 2 is the one place a broken query appears on purpose, against a throwaway file you own, so that you can recognise the pattern and delete it from your own work.
- Every script commits before it reads and closes when it's done. A missing `conn.commit()` throws your rows away without an error message, which makes it the hardest bug of the week to spot.
- Run each script, then **change something** — add a column, change a `WHERE` clause, break the schema — and re-run. The fastest way to learn is to make small modifications and see what happens.

When you finish all five, tackle one of the challenges in `../challenges/`.
