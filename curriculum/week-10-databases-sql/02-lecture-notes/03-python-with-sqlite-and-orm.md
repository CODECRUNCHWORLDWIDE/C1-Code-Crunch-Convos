# Lecture 3 — Python with SQLite and the SQLAlchemy ORM

> Reading time: ~35 minutes. We finally connect Python and the database. Pay extra attention to Section 5 on SQL injection — it is the single most important security topic of the week.

In Lectures 1 and 2 we wrote SQL by hand. Today we drive that SQL from Python. We'll use the standard library `sqlite3` module first, then take a tour of **SQLAlchemy**, the de-facto Python toolkit for talking to relational databases.

## 1. The `sqlite3` module — first contact

The `sqlite3` module ships with Python — no installation needed. The official docs are at <https://docs.python.org/3/library/sqlite3.html>.

A minimal example:

```python
import sqlite3

# Open (or create) a database file
conn: sqlite3.Connection = sqlite3.connect("bookshop.db")
cursor: sqlite3.Cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL
    )
""")

cursor.execute(
    "INSERT INTO books (title, price) VALUES (?, ?)",
    ("Clean Code", 32.50),
)

conn.commit()

cursor.execute("SELECT id, title, price FROM books")
for row in cursor.fetchall():
    print(row)

conn.close()
```

A few terms:

- **Connection** — a handle to one database file. Created with `sqlite3.connect(path)`.
- **Cursor** — a stateful object you use to issue queries and iterate over results.
- **`execute`** — runs one SQL statement.
- **`fetchall`** — returns all remaining rows as a list of tuples.
- **`commit`** — saves any pending writes.

## 2. The connection lifecycle and `with`

Forgetting to `commit` is a classic bug. Forgetting to `close` leaks file handles. Fortunately the `sqlite3.Connection` is a **context manager**:

```python
import sqlite3

with sqlite3.connect("bookshop.db") as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, price) VALUES (?, ?)", ("Refactoring", 47.99))
    # No explicit commit needed — leaving the `with` block commits on success,
    # or rolls back on exception.

# The connection is still open here in Python's sqlite3 implementation —
# call `conn.close()` if you want to release the file.
```

A slightly fuller pattern that handles closing too:

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect("bookshop.db")) as conn:
    with conn:                       # transaction
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, price) VALUES (?, ?)", ("Refactoring", 47.99))
```

`closing` is a stdlib helper from `contextlib` that calls `.close()` on the wrapped object when the `with` block ends.

## 3. Reading results: `fetchone`, `fetchall`, iteration

After `cursor.execute(some_select_query)`, you have several ways to read rows:

```python
cursor.execute("SELECT id, title FROM books ORDER BY id")

row = cursor.fetchone()              # one row, or None if no more
rows = cursor.fetchall()             # list of every remaining row

# Or iterate:
cursor.execute("SELECT id, title FROM books ORDER BY id")
for row in cursor:
    print(row)
```

Each row is a **tuple** by default. Indexing by column name is much nicer; tell SQLite you want `Row` objects:

```python
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT id, title FROM books")
row = cursor.fetchone()
print(row["title"], row[1])          # works either way
print(dict(row))                     # convert to a real dict
```

Set `row_factory` *once* on the connection right after opening it. Every cursor created afterward will use it.

## 4. `executemany` — bulk inserts done right

When you need to insert (or update) many rows, the wrong way is to loop:

```python
# DON'T do this for thousands of rows
for title, price in many_books:
    cursor.execute("INSERT INTO books (title, price) VALUES (?, ?)", (title, price))
```

The right way is `executemany`, which lets the database batch the operation:

```python
many_books: list[tuple[str, float]] = [
    ("Domain-Driven Design", 49.99),
    ("Working Effectively with Legacy Code", 44.99),
    ("Designing Data-Intensive Applications", 54.99),
]
cursor.executemany(
    "INSERT INTO books (title, price) VALUES (?, ?)",
    many_books,
)
conn.commit()
```

For loading large CSVs, `executemany` is often 10x faster than a loop. Wrap it in a single transaction (no `commit` until the end) and it's faster still.

## 5. SQL Injection — the most important section of the week

Read this section twice. Then read it again before bed.

### The wrong way (do not do this)

Suppose you're building a "search by title" feature. You take user input and you build a SQL string the obvious way:

```python
# DO NOT DO THIS — this is a SQL injection vulnerability.
title_search: str = input("Search: ")
query: str = f"SELECT * FROM books WHERE title = '{title_search}'"   # NO
cursor.execute(query)
```

What happens when the user types this:

```
'; DROP TABLE books; --
```

Your final query string becomes:

```sql
SELECT * FROM books WHERE title = ''; DROP TABLE books; --'
```

Three statements: an empty select, a `DROP TABLE`, and a comment that swallows the trailing quote. Goodbye, books.

This is **SQL injection**. It is the #1 web application vulnerability historically, and it is *almost always* the result of mixing user input into SQL via string formatting (`f"..."`, `% "..."`, `+`, `.format()`, etc.).

The good news: the fix is one of the easiest fixes in security. Use **parameterized queries**.

### The right way: parameterized queries

You write SQL with **placeholders** instead of values, and pass the values as a separate argument:

```python
# CORRECT — parameterized query.
title_search: str = input("Search: ")
cursor.execute(
    "SELECT * FROM books WHERE title = ?",
    (title_search,),                  # a tuple of parameters
)
```

SQLite uses `?` as the placeholder. The database receives the query and the values *separately*; the values are never parsed as SQL. Even if the user types `'; DROP TABLE books; --`, that whole string is matched as a literal title — which won't be in the table, so it returns no rows. No drop. No tears.

> **Style note**: when you have one parameter, the tuple still needs the trailing comma: `(title_search,)`. Without it, Python sees `(title_search)` — just parentheses around a string — not a 1-tuple.

### Named placeholders

For longer queries, named placeholders are clearer:

```python
cursor.execute(
    "SELECT * FROM books WHERE title = :title AND price <= :max_price",
    {"title": "Clean Code", "max_price": 40.0},
)
```

Named placeholders use a dictionary and avoid the "which `?` is which?" problem. SQLite supports both styles; pick one per project and stick with it.

### Things you cannot parameterize

Parameters bind **values**, not **identifiers** (table names, column names) or SQL keywords (`ASC`/`DESC`, `LIMIT N`, etc.). If you need to vary the table name or sort direction based on user input, you must validate it against a whitelist:

```python
def safe_sort(direction: str) -> str:
    if direction.upper() not in {"ASC", "DESC"}:
        raise ValueError("direction must be ASC or DESC")
    return direction.upper()

cursor.execute(f"SELECT * FROM books ORDER BY price {safe_sort(user_input)}")
```

Even here we still parameterize every actual *value*. Only the small set of safe-listed keywords is interpolated.

### Why this is non-negotiable

- It is *not* hard.
- It is *not* slower (parameterized queries are often **faster**, because the database can cache the query plan).
- It eliminates the largest class of database security bugs that exist.
- Every Python DB driver supports parameterization.

If you remember nothing else from Week 10, remember **parameterized queries**.

## 6. Transactions in Python

By default, `sqlite3` implicitly begins a transaction before any modifying statement. You commit with `conn.commit()` and roll back with `conn.rollback()`:

```python
import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()
try:
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (100, 1))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (100, 2))
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

The `with conn:` block is equivalent: leaving the block commits on success, rolls back on exception:

```python
with sqlite3.connect("bank.db") as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
```

If either statement raises, neither balance changes. That's atomicity in action.

## 7. Helper: a reusable connection function

In a real project you'll put database access behind a small helper module. Here's a starter:

```python
import sqlite3
from contextlib import contextmanager
from collections.abc import Iterator
from typing import Final

DB_PATH: Final[str] = "tasks.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")        # enforce foreign keys per connection
    return conn

@contextmanager
def db_cursor() -> Iterator[sqlite3.Cursor]:
    conn = get_connection()
    try:
        with conn:
            yield conn.cursor()
    finally:
        conn.close()
```

Usage:

```python
with db_cursor() as cur:
    cur.execute("INSERT INTO tasks (title) VALUES (?)", ("Read Lecture 3",))
```

This single pattern handles connecting, enabling foreign keys, beginning the transaction, committing on success, rolling back on error, and closing the connection. Worth the 15 lines.

## 8. SQLAlchemy: when SQL strings stop scaling

Raw `sqlite3` is wonderful for small scripts. Once your queries grow longer than a screen, you'll want a tool that:

- Lets you compose queries from Python objects rather than concatenated strings.
- Works across databases (SQLite today, PostgreSQL tomorrow) with one codebase.
- Maps rows to Python classes automatically.

That tool is **SQLAlchemy**: <https://www.sqlalchemy.org/>.

SQLAlchemy has two layers:

- **Core** — a SQL expression language. You build query *trees* in Python; SQLAlchemy renders them to SQL.
- **ORM** — Object Relational Mapper. You define Python classes that map to tables; you work with objects, not rows.

Both layers share the same Core engine; the ORM is *built on* Core.

Install it:

```bash
pip install sqlalchemy
```

## 9. SQLAlchemy Core — a quick taste

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, insert

engine = create_engine("sqlite:///bookshop.db", echo=True)
metadata = MetaData()

books = Table(
    "books", metadata,
    Column("id",    Integer, primary_key=True),
    Column("title", String,  nullable=False),
    Column("price", Float),
)

metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(insert(books), [
        {"title": "The Mythical Man-Month", "price": 24.99},
        {"title": "Peopleware",             "price": 19.99},
    ])

with engine.connect() as conn:
    result = conn.execute(select(books).where(books.c.price < 25))
    for row in result:
        print(row.id, row.title, row.price)
```

`echo=True` makes SQLAlchemy log the SQL it generates — invaluable while learning.

Even at this layer you never write a query string with user data — SQLAlchemy always parameterizes for you.

## 10. SQLAlchemy ORM — defining models

The ORM lets you write Python classes that *are* your tables:

```python
from sqlalchemy import create_engine, String, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    """Common base class for all ORM models."""
    pass

class Task(Base):
    __tablename__ = "tasks"

    id:       Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:    Mapped[str]   = mapped_column(String, nullable=False)
    priority: Mapped[int]   = mapped_column(Integer, default=3)
    done:     Mapped[bool]  = mapped_column(default=False)

    def __repr__(self) -> str:
        status = "x" if self.done else " "
        return f"<Task [{status}] {self.id} {self.title!r} p={self.priority}>"

engine = create_engine("sqlite:///tasks.db", echo=False)
Base.metadata.create_all(engine)

# A Session is a unit-of-work: a workspace for objects to be saved together
with Session(engine) as session:
    session.add_all([
        Task(title="Finish Week 10 quiz", priority=1),
        Task(title="Review SQL injection notes", priority=2),
        Task(title="Pet the cat", priority=5),
    ])
    session.commit()

with Session(engine) as session:
    from sqlalchemy import select
    stmt = select(Task).where(Task.done == False).order_by(Task.priority)
    for task in session.scalars(stmt):
        print(task)
```

Three things to notice:

1. **No SQL strings**. We build queries from Python expressions: `Task.done == False` is not a Python boolean — it's a SQL expression object that renders to `tasks.done = 0`.
2. **No manual cursors**. The `Session` object manages the cursor and transaction.
3. **Type hints work**. The `Mapped[int]` syntax lets your IDE and type checker understand columns.

### Relationships

The ORM really shines when you add relationships. A user owns many tasks:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id:    Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:  Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id:        Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:     Mapped[str] = mapped_column(String, nullable=False)
    owner_id:  Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    owner:     Mapped[User | None] = relationship(back_populates="tasks")
```

Now `user.tasks` is a Python list that SQLAlchemy loads from the database on demand. Adding a task to a user is just `user.tasks.append(task)` — no manual `INSERT`.

## 11. Migrations — what they are, why you'll need them

The first time your schema changes after your app has live data, you have a problem: how do you change the table without losing the data?

A **migration** is a small, ordered script that changes the schema and (often) the data to match. Migrations are version-controlled, just like your code. The canonical Python tool is **Alembic** (<https://alembic.sqlalchemy.org/>), which is built by the SQLAlchemy team.

A migration file looks roughly like:

```python
def upgrade() -> None:
    op.add_column("tasks", sa.Column("due_date", sa.Date(), nullable=True))

def downgrade() -> None:
    op.drop_column("tasks", "due_date")
```

You won't write migrations in Week 10 — that's a Week 11+ topic. For now, just know:

- Manual `ALTER TABLE` works for hobby projects.
- Real projects use migration tools so the schema lives in source control alongside the code.

## 12. Putting it all together: a mini pattern

Here's the pattern your Friday mini-project will use, in miniature:

```python
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Final

DB_PATH: Final[str] = "tasks.db"

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS tasks (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 3,
    done     INTEGER NOT NULL DEFAULT 0
);
"""

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)

@contextmanager
def cursor() -> Iterator[sqlite3.Cursor]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn.cursor()
    finally:
        conn.close()

def add_task(title: str, priority: int = 3) -> int:
    with cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)",
            (title, priority),
        )
        return cur.lastrowid                          # the id of the new row

def list_tasks(only_open: bool = False) -> list[sqlite3.Row]:
    query = "SELECT * FROM tasks"
    params: tuple[object, ...] = ()
    if only_open:
        query += " WHERE done = ?"
        params = (0,)
    query += " ORDER BY priority, id"
    with cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()
```

Notice every value goes through `?` placeholders. No `f""`. No `%`. No `+`. That habit will save you (and your users) from real harm.

## 13. Recap

- `sqlite3.connect`, cursors, `execute`, `executemany`, `fetchone`, `fetchall`, `commit`, `rollback`.
- Use `with` blocks (and `contextlib.closing`) for clean resource handling.
- **Always parameterize**. `?` for positional, `:name` for named. Never f-string a value into SQL.
- SQLAlchemy gives you Core (SQL expressions) and ORM (Python classes as tables).
- Alembic is the migration tool — note that it exists, return to it later.

Time to practice. Open `exercises/exercise-01-first-table.py` and go.

### References

- Python `sqlite3`: <https://docs.python.org/3/library/sqlite3.html>
- SQLAlchemy Unified Tutorial: <https://docs.sqlalchemy.org/en/20/tutorial/index.html>
- OWASP on SQL injection: <https://owasp.org/www-community/attacks/SQL_Injection>
