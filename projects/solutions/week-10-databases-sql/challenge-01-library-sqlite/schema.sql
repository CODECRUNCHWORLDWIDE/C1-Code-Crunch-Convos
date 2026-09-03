-- ---------------------------------------------------------------------------
-- Library schema. Every statement is IF NOT EXISTS, so bootstrapping is
-- idempotent: running the app twice cannot crash.
--
-- Foreign keys are declared here, but declaring is not enforcing -- SQLite only
-- enforces them when a connection runs `PRAGMA foreign_keys = ON`, which
-- library/db.py does on every connect().
-- ---------------------------------------------------------------------------

-- books: one row per catalogue entry, not per physical copy. total_copies is
-- how many copies the library owns; "available" is derived at query time as
-- total_copies minus the count of unreturned loans, so the two numbers can
-- never drift apart.
CREATE TABLE IF NOT EXISTS books (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT    NOT NULL,
    author        TEXT    NOT NULL,
    isbn          TEXT    UNIQUE,
    total_copies  INTEGER NOT NULL CHECK (total_copies >= 0)
);

-- members: one row per person who may borrow.
CREATE TABLE IF NOT EXISTS members (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    joined_on  TEXT NOT NULL DEFAULT (DATE('now'))
);

-- loans: one row per borrow event. returned_on IS NULL means "still out",
-- which is the definition of an active loan everywhere in this project.
CREATE TABLE IF NOT EXISTS loans (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id      INTEGER NOT NULL REFERENCES books(id)   ON DELETE RESTRICT,
    member_id    INTEGER NOT NULL REFERENCES members(id) ON DELETE RESTRICT,
    borrowed_on  TEXT    NOT NULL DEFAULT (DATE('now')),
    due_on       TEXT    NOT NULL,
    returned_on  TEXT,
    CHECK (returned_on IS NULL OR returned_on >= borrowed_on)
);

-- reservations (stretch goal): a queue of members waiting for a copy.
-- fulfilled_on IS NULL means "still waiting"; the queue is ordered by
-- placed_on then id, so ties break in insertion order.
CREATE TABLE IF NOT EXISTS reservations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id       INTEGER NOT NULL REFERENCES books(id)   ON DELETE CASCADE,
    member_id     INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    placed_on     TEXT    NOT NULL DEFAULT (DATE('now')),
    fulfilled_on  TEXT
);

-- Required by the challenge: both foreign-key columns on loans are indexed.
-- Without these, "is this book available?" and "what has this member got out?"
-- are full scans of loans, and loans is the table that grows forever.
CREATE INDEX IF NOT EXISTS idx_loans_book_id   ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans(member_id);

-- Availability and overdue reports both filter on "returned_on IS NULL".
-- A partial index stores ONLY the active loans, so it stays small forever
-- even as the history table grows to millions of returned rows.
CREATE INDEX IF NOT EXISTS idx_loans_active
    ON loans(book_id, member_id) WHERE returned_on IS NULL;

CREATE INDEX IF NOT EXISTS idx_reservations_queue
    ON reservations(book_id, placed_on, id) WHERE fulfilled_on IS NULL;
