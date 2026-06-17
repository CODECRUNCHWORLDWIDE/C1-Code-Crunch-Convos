# Week 10 Homework

Six problems. Some are pure SQL on paper, some require Python. Aim to spend roughly 30–60 minutes on each. Submit your answers as a single repo with the structure below; clear commit messages welcome.

```
week-10-homework/
├── problem-1-ecommerce-schema/
│   └── schema.sql
├── problem-2-migration/
│   ├── 001_initial.sql
│   └── 002_add_categories.sql
├── problem-3-csv-importer/
│   ├── importer.py
│   └── sample.csv
├── problem-4-query-optimizer/
│   └── notes.md
├── problem-5-orm-relationships/
│   ├── models.py
│   └── demo.py
└── problem-6-backup-restore/
    └── backup.py
```

All Python must use type hints. All SQL must be readable: uppercase keywords, one column per line in long `SELECT`s, indented `JOIN`/`WHERE` clauses.

---

## Problem 1 — Design an e-commerce schema (SQL only)

Design the schema for a small e-commerce website. **Do not write any Python.** Hand in a `schema.sql` file with `CREATE TABLE` statements (and indexes) for the following entities and relationships:

- **Customers** — id, name, email (unique), created_at.
- **Addresses** — many per customer, one of which is the default.
- **Products** — id, sku (unique), name, description, price, stock.
- **Categories** — hierarchical (a category can have a parent category).
- **Products ↔ Categories** — many-to-many.
- **Orders** — header info (customer, status, totals, dates).
- **Order items** — line items linking an order to a product with quantity and price-at-time-of-purchase.
- **Reviews** — by customer, on a product, with a rating from 1–5 and a body.

Things to include:

- All primary keys, foreign keys, and `NOT NULL`/`UNIQUE` constraints that make sense.
- A `CHECK` constraint where it adds value (e.g., positive price, rating in 1–5).
- At least three indexes you think will help common queries.
- A comment at the top of each table explaining its purpose.

You don't need to populate it — just the DDL. Verify it loads cleanly into SQLite:

```bash
sqlite3 ecommerce.db < schema.sql
```

---

## Problem 2 — A migration script

You have a database that already has data in it, created by the schema in `001_initial.sql` (just the bare `posts` and `users` tables from the Week 10 exercises). Write a migration script `002_add_categories.sql` that:

1. Creates a `categories` table.
2. Adds a `category_id` column to the existing `posts` table that references `categories(id)` (nullable, no default).
3. Inserts three starter categories ("Tech", "Life", "Other").
4. Backfills existing posts to have `category_id` = the id of "Other".

The migration must be runnable on a database that already contains rows, **without losing any data**. Use `BEGIN`/`COMMIT` so the whole thing is atomic.

SQLite quirk: older versions can't add a column with a foreign-key constraint in one go. If you hit that, use the "create new table, copy data, drop old, rename" pattern — and write a comment explaining what you did.

---

## Problem 3 — CSV → SQLite importer

Write `importer.py` that:

- Reads any CSV file whose path is given on the command line.
- Infers the columns from the CSV header.
- Creates a SQLite table (named after the CSV file, sanitized) whose columns are all `TEXT` for simplicity.
- Inserts all rows using `executemany` and a parameterized query.
- Wraps the whole import in a single transaction so a bad row rolls everything back.
- Prints the row count and time taken at the end.

Include a tiny `sample.csv` (maybe 10 rows of fake people) so we can run it. Sample invocation:

```bash
python importer.py sample.csv
```

The bonus marks question: what's the table name if the user passes a CSV named `2026 Sales / Q1.csv`? Document how you handle that in the docstring.

---

## Problem 4 — Query optimizer puzzle (write-up only)

You're given this slow query against a `events` table with 1,000,000 rows. The table has columns `id` (PK), `user_id`, `event_type`, `occurred_at`, `payload`.

```sql
SELECT user_id, COUNT(*) AS event_count
FROM   events
WHERE  event_type = 'login'
  AND  occurred_at >= DATE('now', '-30 days')
GROUP BY user_id
ORDER BY event_count DESC
LIMIT 10;
```

It currently takes 4 seconds. Your task: write a 300–500 word `notes.md` answering:

1. What is the query doing in plain English?
2. Without any indexes, what does the database have to do? (Hint: a full table scan.)
3. Which **one** index would you add, and on what column(s)? Why?
4. Could a *composite* index do even better? Sketch it and explain.
5. How would `EXPLAIN QUERY PLAN` help you confirm your guess?

You don't need a real million-row database. This is a reasoning exercise. Cite "Use The Index, Luke" (<https://use-the-index-luke.com/>) if it helps your answer.

---

## Problem 5 — ORM relationships (one-to-many)

Using SQLAlchemy ORM, model a blog with **Authors** and **Posts**:

- An Author has many Posts.
- A Post belongs to exactly one Author.

Required:

- `models.py` defines `Base`, `Author`, and `Post` with appropriate columns, a `ForeignKey`, and a bidirectional `relationship`. Use modern `Mapped`/`mapped_column` typing.
- `demo.py` opens an in-memory SQLite database (`sqlite:///:memory:` or `sqlite://`), creates the tables, inserts at least two authors and at least five posts spread across them, and prints:
  - Each author and the count of their posts.
  - The titles of every post written by the most prolific author.
- All access goes through ORM queries (`select(...)`) — no raw SQL strings.

Sample expected output:

```
Authors:
  Ada Lovelace (3 posts)
  Alan Turing  (2 posts)

Most prolific: Ada Lovelace
  - Notes on the Analytical Engine
  - On Bernoulli numbers
  - Reflections on the difference engine
```

---

## Problem 6 — Backup and restore script

Write `backup.py`, a small Python script with two subcommands:

- `python backup.py backup <source.db> <backup.db>` — creates a snapshot of the source database.
- `python backup.py restore <backup.db> <target.db>` — restores the snapshot to a target file.

Requirements:

- Use the `Connection.backup()` method from `sqlite3` (<https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup>) — not `shutil.copy`. The reason: `Connection.backup()` is safe even if the source is actively being written to.
- Print progress messages.
- Refuse to overwrite an existing target file unless `--force` is passed.
- Return a non-zero exit code on any error.
- Include a docstring at the top explaining the trade-offs vs. a file copy.

Sample run:

```bash
python backup.py backup tasks.db tasks.backup.db
# Backed up 312 pages to tasks.backup.db (4096 bytes/page).
```

---

## Submission

Push your folder to a public GitHub repo and share the link. We will:

- Run the SQL files against a fresh SQLite database.
- Run each Python script.
- Read your `notes.md` for Problem 4.
- Look for f-strings in SQL (there should be none).

Have fun. The next time you see a `.json` file pretending to be a database, you'll know exactly what to do.
