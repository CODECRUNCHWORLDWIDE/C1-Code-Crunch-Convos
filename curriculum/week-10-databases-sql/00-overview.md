# Week 10 — Databases & SQL with Python

Welcome to Week 10 of **Code Crunch Convos**. After last week's adventure with Flask, your apps can finally talk to the world. But there's a problem lurking in every project we've built so far: the moment the program stops, the data evaporates. JSON files patched that, but the patch starts to feel thin once your "database" is a 40 MB JSON file you have to rewrite every time a user clicks "save".

This week we step up to **real databases**. We will learn the relational model, write SQL by hand, then wire SQLite into Python with the standard library `sqlite3` module. By Friday you will have a working CLI **task tracker** that stores everything in a real database, supports filtering, and is ready to grow.

---

## Learning objectives

By the end of this week you will be able to:

- Explain **why** databases exist, and when to choose one over a flat file.
- Describe the **relational model**: tables, rows, columns, primary keys, foreign keys.
- Write SQL for all four CRUD operations: `CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
- Filter, sort, and limit results using `WHERE`, `ORDER BY`, and `LIMIT`.
- Combine data from two or more tables with `INNER JOIN` and `LEFT JOIN`.
- Summarize data using `GROUP BY` and the aggregate functions `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- Use transactions with `COMMIT` and `ROLLBACK` to keep your data safe.
- Connect to SQLite from Python using `sqlite3`, with cursors, `execute`, `executemany`, `fetchone`, and `fetchall`.
- Write **parameterized queries** and explain why they prevent SQL injection.
- Use SQLAlchemy Core and the ORM to define a model and query it without writing raw SQL.
- Understand what a migration is and why you will eventually need one.

---

## Prerequisites

You should be comfortable with:

- Weeks 1–6: Python syntax, control flow, functions, data structures, file I/O, exceptions.
- Week 7: Object-Oriented Programming — classes are how ORM models are defined.
- Week 8: APIs & JSON — last week's "store everything as JSON" pattern that we are now upgrading.
- Week 9: Flask basics — many of the challenges connect a web app to a database.

If any of those feel rusty, take an hour to revisit them before diving in. SQL is forgiving, but Python + SQL together moves fast.

---

## Topics covered

1. **Why a database?** — durability, concurrency, query power, integrity.
2. **The relational model** — tables, rows, columns, primary keys, foreign keys, normalization (lightly).
3. **SQL CRUD** — `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
4. **Filtering & sorting** — `WHERE`, `ORDER BY`, `LIMIT`.
5. **Joins** — `INNER JOIN`, `LEFT JOIN`, and when each is appropriate.
6. **Aggregations** — `GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
7. **Transactions** — `BEGIN`, `COMMIT`, `ROLLBACK`, and atomicity.
8. **SQLite** — a complete SQL database in a single file, zero config.
9. **Python `sqlite3` module** — `connect`, `cursor`, `execute`, `executemany`, `fetchone`/`fetchall`.
10. **Parameterized queries** — the *one* defense against SQL injection. Non-negotiable.
11. **SQLAlchemy Core vs ORM** — when to drop down, when to stay high-level.
12. **Migrations, briefly** — what they are and why Alembic exists.

---

## Schedule (~36 hours)

| Day       | Hours | Focus                                                                 |
|-----------|-------|-----------------------------------------------------------------------|
| Monday    | 6     | Read `lecture-notes/01`, complete `exercise-01-first-table.py`.       |
| Tuesday   | 6     | Practice SQL on sqlbolt.com, then `exercise-02-parameterized.py`.     |
| Wednesday | 6     | Read `lecture-notes/02`, complete `exercise-03-joins.py` and `04`.    |
| Thursday  | 6     | Read `lecture-notes/03`, complete `exercise-05-sqlalchemy-basic.py`.  |
| Friday    | 6     | Build the mini-project task tracker.                                  |
| Saturday  | 4     | Pick one challenge; take the quiz; start homework.                    |
| Sunday    | 2     | Finish homework, review notes, peek at Week 11.                       |

Adjust the pace to your reality — these are guidelines, not laws.

---

## Folder navigation

- `lecture-notes/` — three deep-dive notes covering SQL, joins/aggregations, and Python integration.
- `exercises/` — five short, focused drills. Run each one and make sure it works before moving on.
- `challenges/` — two bigger refactors that connect previous weeks to a database.
- `mini-project/` — the SQLite task tracker CLI.
- `quiz.md` — 10 multiple-choice questions to check your understanding.
- `homework.md` — six longer problems to stretch the concepts.
- `resources.md` — official documentation and the books / tutorials we recommend.

---

## Stretch goals

If the regular work feels too easy, try one (or more) of these:

- **Indexes**: add indexes to a slow query and measure the speedup with `EXPLAIN QUERY PLAN`.
- **Views**: build a SQL view that joins three tables for a "dashboard" report.
- **Bulk import**: use `executemany` to load a 100k-row CSV into SQLite in under 5 seconds.
- **Alembic**: write your first real migration with Alembic on top of the mini-project schema.
- **PostgreSQL**: install Postgres locally with Docker and port the task tracker over — almost all the SQL is identical.
- **Backup script**: write a Python script that snapshots your SQLite DB on a cron schedule.

---

## How to ask for help

Stuck? Drop into `#week-10` in the bootcamp Discord. When you ask, include:

1. The SQL or Python you ran.
2. The exact error message.
3. What you expected vs. what happened.

Ninety percent of database bugs are typos in column names. The other ten percent are forgetting to `COMMIT`.

---

## Up next

**Week 11 — Testing & Debugging.** You will be writing tests for everything you've built. After this week's database work you'll especially appreciate how `pytest` plus a temporary SQLite file lets you test database code without polluting your real data.

See `../week-11-testing-debugging/`.
