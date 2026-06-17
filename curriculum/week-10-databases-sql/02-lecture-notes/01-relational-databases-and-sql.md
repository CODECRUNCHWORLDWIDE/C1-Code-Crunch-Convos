# Lecture 1 — Relational Databases & SQL

> Reading time: ~30 minutes. Code-along time: another 30. Don't skip the code-along.

## 1. Why use a database at all?

You've been storing data in two ways so far:

- **In memory**, in Python lists and dicts — fast, but gone the moment the program exits.
- **In files**, often as JSON — survives a restart, but every read or write means loading and saving the *entire* file.

That works fine for a hundred items. It falls apart at ten thousand. It catches fire at a million. Here are the four reasons databases exist:

1. **Durability**. The data is written to disk in a way that survives crashes — and survives them in a *consistent* state. If your laptop loses power halfway through a database write, a real DB will either have the whole change or none of it. Never half.
2. **Concurrency**. Two users (or two threads, or two processes) can read and write at the same time without corrupting the data. Try doing that with a JSON file. (You can't; you'll get a torn write the first time both processes save.)
3. **Query power**. Databases speak **SQL**, a declarative language for asking questions like *"give me the top 10 customers by total spend in the last 30 days, but only in California"*. With JSON you'd write 30 lines of Python. With SQL you write one query.
4. **Integrity**. A database can enforce rules: "every `order` must reference a real `customer`", "every `email` is unique", "every `price` is non-negative". The database refuses to save bad data, even if your code has a bug.

For the rest of the week we'll focus on **relational** databases — the kind whose data lives in tables.

## 2. The relational model

The relational model was invented by Edgar F. Codd at IBM in 1970. The core idea is shockingly simple: **store all your data in tables**, and use the values in those tables to relate them to each other.

A **table** is a named collection of **rows** (also called *records* or *tuples*). Every row has the same set of named **columns** (also called *fields* or *attributes*). Here is what a `books` table might look like:

| id | title              | author          | year | price |
|----|--------------------|-----------------|------|-------|
| 1  | The Pragmatic Programmer | Hunt & Thomas | 1999 | 29.95 |
| 2  | Code Complete      | Steve McConnell | 2004 | 39.95 |
| 3  | Clean Code         | Robert Martin   | 2008 | 32.50 |

The **schema** of the table is the part that doesn't change: the column names and their types. The **data** is the rows themselves.

### Primary keys

Every row should have something unique that identifies it — its **primary key**. In the table above, `id` is the primary key. Two rows can share the same `title` (different printings, different translations) but they can never share the same `id`.

A primary key is:

- **Unique** — no two rows have the same value.
- **Not null** — every row must have one.
- **Stable** — once assigned, it should not change.

The simplest and most common choice is an integer that auto-increments: row 1 gets `id = 1`, row 2 gets `id = 2`, etc.

### Foreign keys

Now suppose we have a second table, `reviews`:

| id | book_id | reviewer       | rating | comment              |
|----|---------|----------------|--------|----------------------|
| 1  | 1       | Alice          | 5      | "Life-changing."     |
| 2  | 1       | Bob            | 4      | "Worth the hype."    |
| 3  | 3       | Alice          | 5      | "A modern classic."  |

The `book_id` column **points at** the `id` column of the `books` table. We say `book_id` is a **foreign key** referencing `books(id)`. The database can be told to enforce this: if you try to insert a review with `book_id = 999` and there's no book with `id = 999`, the database will refuse.

Foreign keys are the *relational* part of the relational model. They are how tables connect.

## 3. Talking to a database: SQL

**SQL** (Structured Query Language, pronounced "sequel" or "ess-cue-ell" — both are fine; we'll use "sequel") is the standard language for relational databases. The same SQL works (mostly) across SQLite, PostgreSQL, MySQL, SQL Server, and Oracle. There are small dialect differences. We'll focus on standard SQL.

SQL is a **declarative** language. You say *what* you want, not *how* to get it. The database figures out the "how".

For the rest of this lecture we'll use **SQLite**, because it's already installed on your machine (Python's `sqlite3` module ships in the standard library). To follow along, open a terminal:

```bash
python -m sqlite3 bookshop.db
```

That gives you an interactive SQLite shell connected to a file called `bookshop.db`. Type `.help` to see commands and `.exit` to leave.

## 4. CREATE TABLE — designing the shape of your data

We tell the database what our tables look like with `CREATE TABLE`:

```sql
CREATE TABLE books (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    author  TEXT NOT NULL,
    year    INTEGER,
    price   REAL CHECK (price >= 0)
);
```

Let's read this carefully:

- `id INTEGER PRIMARY KEY AUTOINCREMENT` — `id` is an integer, it's the primary key, and SQLite will fill it in automatically when we insert a row.
- `title TEXT NOT NULL` — a string, and the database will refuse to store a row with no title.
- `author TEXT NOT NULL` — same deal.
- `year INTEGER` — nullable; the year is optional.
- `price REAL CHECK (price >= 0)` — a floating-point number, and the database checks that prices aren't negative.

SQLite is unusual in being loose with types (it has only five **storage classes**: `NULL`, `INTEGER`, `REAL`, `TEXT`, `BLOB`). PostgreSQL and others are strict — declaring a column `INTEGER` means it really must be an integer.

Now let's add the reviews table with a real foreign key:

```sql
CREATE TABLE reviews (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id   INTEGER NOT NULL,
    reviewer  TEXT NOT NULL,
    rating    INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment   TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
```

In SQLite, foreign-key enforcement is *off by default*. You turn it on per-connection with `PRAGMA foreign_keys = ON;` — we'll see this in Lecture 3.

### DROP TABLE and IF (NOT) EXISTS

Two useful variations:

```sql
DROP TABLE reviews;                         -- delete the table and all its data
CREATE TABLE IF NOT EXISTS books (...);     -- only create if missing; safe in setup scripts
```

The `IF NOT EXISTS` pattern is the right way to write a "create my schema" routine that you can run repeatedly without errors.

## 5. INSERT — adding rows

```sql
INSERT INTO books (title, author, year, price)
VALUES ('The Pragmatic Programmer', 'Hunt & Thomas', 1999, 29.95);
```

We don't supply `id` because we told SQLite to fill it in. You can insert several rows at once:

```sql
INSERT INTO books (title, author, year, price) VALUES
    ('Code Complete',  'Steve McConnell', 2004, 39.95),
    ('Clean Code',     'Robert Martin',   2008, 32.50),
    ('Refactoring',    'Martin Fowler',   2018, 47.99);
```

> **Real talk on syntax**: SQL strings are single-quoted: `'hello'`. Double quotes are for *identifiers* (column or table names with weird characters). This is the opposite of Python, and tripping over it is a rite of passage.

## 6. SELECT — asking questions

The workhorse statement. The full shape of a `SELECT` is:

```sql
SELECT columns
FROM   table
WHERE  condition
ORDER BY column ASC|DESC
LIMIT  n;
```

### Selecting all columns

```sql
SELECT * FROM books;
```

The `*` means "every column". Fine for poking around interactively. **Avoid `SELECT *` in production code** — name your columns so the query keeps working when the schema changes.

### Selecting specific columns

```sql
SELECT title, price FROM books;
```

### Filtering with WHERE

```sql
SELECT title, price FROM books WHERE year >= 2000;
```

`WHERE` accepts the usual comparison operators (`=`, `<>`, `<`, `<=`, `>`, `>=`), the boolean operators `AND`, `OR`, `NOT`, plus a few extras:

```sql
SELECT * FROM books WHERE year BETWEEN 2000 AND 2010;
SELECT * FROM books WHERE author IN ('Robert Martin', 'Martin Fowler');
SELECT * FROM books WHERE title LIKE '%Code%';
SELECT * FROM books WHERE year IS NULL;
```

A few sharp edges to remember:

- **Equality with NULL doesn't work**. `WHERE year = NULL` returns nothing. Use `WHERE year IS NULL` or `IS NOT NULL`.
- **`LIKE` patterns** use `%` (zero or more characters) and `_` (exactly one character). `'%Code%'` matches anything containing the substring `Code`.
- **String comparison is case-sensitive in some databases, not in others.** SQLite is case-sensitive by default for `=` but case-*insensitive* for `LIKE`. Don't rely on it; use `LOWER()` if you need portability.

### Sorting with ORDER BY

```sql
SELECT title, price FROM books ORDER BY price DESC;
SELECT title, year   FROM books ORDER BY year ASC, title ASC;
```

`ASC` is ascending (the default; you can leave it off). `DESC` is descending.

### Limiting results

```sql
SELECT title, price FROM books ORDER BY price DESC LIMIT 3;
```

Combined with `ORDER BY`, this gives you the "top N" pattern.

`OFFSET` skips rows, useful for pagination:

```sql
SELECT title FROM books ORDER BY id LIMIT 10 OFFSET 20;
-- page 3, with 10 items per page
```

## 7. UPDATE — changing existing rows

```sql
UPDATE books
SET    price = 24.99
WHERE  title = 'Clean Code';
```

**The `WHERE` clause is mandatory in spirit, not syntax**. If you forget it, SQL will happily update *every row in the table*. There is a story for every database engineer of the day they forgot the `WHERE`. Don't be that story. When in doubt, run the equivalent `SELECT` first to confirm which rows you're about to touch.

You can update several columns at once:

```sql
UPDATE books
SET    price = price * 0.9, year = 2020
WHERE  author = 'Martin Fowler';
```

Note the `price = price * 0.9` — `SET` accepts arbitrary expressions, including ones that reference the current column.

## 8. DELETE — removing rows

```sql
DELETE FROM books WHERE id = 4;
```

Same warning as `UPDATE`: **the `WHERE` clause is the difference between deleting one row and deleting the whole table**. Always run `SELECT` first.

If you really do want to wipe everything, the recommended way is:

```sql
DELETE FROM books;            -- removes every row, table still exists
```

To remove the table itself, schema and all:

```sql
DROP TABLE books;
```

## 9. A complete "CRUD" walkthrough

Here is one end-to-end example you can paste into the SQLite shell:

```sql
-- Create
CREATE TABLE IF NOT EXISTS contacts (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);

-- Insert (Create)
INSERT INTO contacts (name, email, phone) VALUES
    ('Ada Lovelace',   'ada@example.com',   '555-0100'),
    ('Alan Turing',    'alan@example.com',  '555-0101'),
    ('Grace Hopper',   'grace@example.com', NULL);

-- Read
SELECT id, name, email FROM contacts ORDER BY name;

-- Update
UPDATE contacts SET phone = '555-0102' WHERE name = 'Grace Hopper';

-- Delete
DELETE FROM contacts WHERE email = 'alan@example.com';

-- Read again
SELECT * FROM contacts;
```

If you ran every statement, you should see Ada and Grace remaining, with Grace's phone number filled in.

## 10. Transactions: all-or-nothing

A **transaction** is a group of statements that succeed together or fail together. SQLite begins one automatically before any modifying statement. You commit it with `COMMIT` (saving the changes) or undo it with `ROLLBACK` (throwing them away).

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

If the second update fails (say, account 2 doesn't exist), you can `ROLLBACK` and the first update is undone. The two changes are atomic — one without the other would be a bug (somebody just lost $100).

We'll see Python's transaction handling in Lecture 3. The big lesson today: **transactions exist; use them when several writes must happen together**.

## 11. Common mistakes to avoid

- Forgetting the `WHERE` clause on `UPDATE` or `DELETE`.
- Comparing with `= NULL` instead of `IS NULL`.
- Using `SELECT *` in real code, then being surprised when adding a column changes the result shape.
- Storing dates as raw strings without a consistent format. Prefer ISO-8601 (`'2026-05-13'`).
- Trusting user input in string-formatted queries. We'll talk about why in Lecture 3 — it's the single most important security topic of the week.

## 12. Recap

You now have the relational vocabulary: tables, rows, columns, primary keys, foreign keys, schemas. You can create tables, insert data, query with `SELECT`/`WHERE`/`ORDER BY`/`LIMIT`, update existing rows, and delete them. You know about transactions and you've heard the first whisper of the SQL injection warning.

In Lecture 2 we'll connect *multiple* tables with JOINs and summarize data with GROUP BY. In Lecture 3 we'll move from the SQLite shell into Python.

### References

- Python `sqlite3` module: <https://docs.python.org/3/library/sqlite3.html>
- SQLite "SQL As Understood" reference: <https://www.sqlite.org/lang.html>
- SQLBolt interactive lessons 1–6: <https://sqlbolt.com/>
