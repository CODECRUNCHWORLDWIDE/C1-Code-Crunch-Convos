-- ---------------------------------------------------------------------------
-- Migration 002 -- give books a category, without losing a single row.
--
-- Stretch goal for Challenge 01. Run it once against a database that already
-- has books, members and loans in it:
--
--     sqlite3 library.db < migrations/002_add_category.sql
--
-- or, with no sqlite3 CLI installed:
--
--     python -c "import sqlite3,sys; c=sqlite3.connect('library.db'); \
--       c.executescript(open(sys.argv[1],encoding='utf-8').read()); c.close()" \
--       migrations/002_add_category.sql
--
-- Run it twice and the second run stops at step 3 with
-- "duplicate column name: category_id" and changes nothing -- which is the
-- correct behaviour for a numbered migration. Migrations are applied once and
-- recorded; it is the *bootstrap* (schema.sql) that has to be idempotent.
--
-- Why this is safe on a live database:
--
--   * ALTER TABLE ... ADD COLUMN does not rewrite the table. SQLite stores the
--     new column's value as "missing" for existing rows and reports NULL when
--     you read it. It is O(1) and it cannot lose data.
--   * A column added with a REFERENCES clause is legal in SQLite *only* if its
--     default is NULL, which is exactly what we want: existing books get NULL
--     until the backfill below assigns them.
--   * BEGIN/COMMIT makes the four steps atomic. If the backfill fails, the
--     column addition is rolled back too and you can fix and rerun.
--
-- Migration 001 is schema.sql itself -- this project bootstraps rather than
-- migrating from empty, which is fine while there is only one schema version.
-- ---------------------------------------------------------------------------

BEGIN;

-- 1. The new table.
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. Seed it. ON CONFLICT DO NOTHING so this step alone is safe to repeat.
INSERT INTO categories (name) VALUES
    ('Fiction'),
    ('Non-fiction'),
    ('Reference'),
    ('Uncategorised')
ON CONFLICT(name) DO NOTHING;

-- 3. The new column. No DEFAULT, so every existing row reads back as NULL.
ALTER TABLE books ADD COLUMN category_id INTEGER REFERENCES categories(id);

-- 4. Backfill. Every book that has no category gets 'Uncategorised', so the
--    column is immediately usable for reporting instead of full of NULLs.
UPDATE books
SET    category_id = (SELECT id FROM categories WHERE name = 'Uncategorised')
WHERE  category_id IS NULL;

-- 5. Reports will filter and group on this column, so index it.
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category_id);

COMMIT;

-- ---------------------------------------------------------------------------
-- If your SQLite is old enough to reject step 3 with
--
--     Cannot add a REFERENCES column with non-NULL default value
--
-- then you supplied a DEFAULT. Remove it. If instead you need to add a
-- constraint that ALTER TABLE genuinely cannot express (a CHECK, a NOT NULL
-- with no default, dropping a column on SQLite < 3.35), the pattern is:
--
--     CREATE TABLE books_new (...the shape you want...);
--     INSERT INTO books_new (id, title, author, isbn, total_copies)
--         SELECT id, title, author, isbn, total_copies FROM books;
--     DROP TABLE books;
--     ALTER TABLE books_new RENAME TO books;
--     -- then recreate every index that lived on the old table
--
-- Do that inside the same BEGIN/COMMIT, and turn foreign keys OFF for the
-- duration (PRAGMA foreign_keys = OFF) so the DROP does not cascade into
-- loans. Homework Problem 2 walks through this version in full.
-- ---------------------------------------------------------------------------
