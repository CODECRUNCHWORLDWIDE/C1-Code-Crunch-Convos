# Challenge 02 — Flask Blog backed by SQLite

> **Topic:** moving a Flask blog's data into SQLite — a schema with foreign keys, hashed passwords, JOINs that fetch the author's name, `ON DELETE CASCADE`, and every single value bound through a placeholder
> **Lecture:** [01 — Relational Databases & SQL](../lecture-notes/01-relational-databases-and-sql.md) · [02 — JOINs and Aggregations](../lecture-notes/02-joins-and-aggregations.md) · [03 — Python with SQLite and the SQLAlchemy ORM](../lecture-notes/03-python-with-sqlite-and-orm.md)
> **Difficulty:** Intermediate
> **Target time:** 3–5 hours
> **Why this one:** in Week 9 your blog kept its posts in a dict, and a restart forgot everything. This is the week the data stops being a Python object and starts being a table. It is also the first time your app takes words typed by a stranger and puts them into a sentence the database will obey — which is where the single most damaging bug in web programming lives. Get the habit here, on a blog you wrote yourself, and you will have it for good.

## The Brief

You already have a blog. In Week 9 you built it in Flask: a homepage that
lists posts, a page for one post, a form for comments, a login. The posts
lived in a Python dict or a JSON file, and every restart wiped them.

Your job is to swap the storage out for a real database. Same routes, same
templates, same thing on the screen. Underneath, SQLite.

Here is the idea that makes the whole week worth it. When you talk to a
database you send it a **sentence** — `SELECT`, `INSERT`, `DELETE`. Some
parts of that sentence come from you, and some parts come from whoever is
typing in the browser. Those two things must never be mixed on the same
piece of paper.

Think of a recipe. You hand the cook the recipe first, with blanks in it:
"add ___ cups of sugar". Then, separately, you hand over the number. The
cook has already read the steps, so the number can never become a step. It
is an ingredient, forever.

Now imagine you instead wrote one page with the number typed right into the
sentence. Someone hands you an "ingredient" that reads *"two cups, then set
the kitchen on fire"*, you copy it onto the page, and the cook does exactly
what the page says. That is SQL injection. It is not exotic and it is not
rare — it is the ordinary result of building a query with an f-string.

The blank is called a **placeholder**, and in `sqlite3` it is a question
mark:

```python
# Right. The value travels separately, in the tuple.
conn.execute("SELECT id FROM users WHERE username = ?", (username,))

# Wrong. Never do this, not once, not "just for a test".
conn.execute(f"SELECT id FROM users WHERE username = '{username}'")
```

What the wrong one costs, concretely. A visitor types their username as:

```text
' OR '1'='1
```

Your f-string turns that into `WHERE username = '' OR '1'='1'`, which is
true for every row, and the login hands them the first account in the
table. A visitor who types `'; DROP TABLE users; --` gets your users table
deleted. The placeholder version treats both of those as what they are:
a silly username that matches nobody.

So: **every value goes in through a placeholder, in every route, with no
exceptions.** That is the one rule this challenge exists to install.

The shipped answer below is the storage layer — the schema and all the SQL,
in one module. Your Flask routes stay yours; each one becomes a single call
into it. Keeping every line of SQL in one file is a real technique, not a
teaching trick: it means you can audit the whole app for injection bugs by
reading one file.

## Starter

Save this as `blog_db.py` — **not** as the `-solution` name, or the finished
answer will land where your own work belongs. It runs as pasted: with the
schema half-written it just reports what it managed to build.

```python
"""blog_db.py — every line of SQL the blog needs, in one file."""

import sqlite3
from typing import Final

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

-- TODO: CREATE TABLE posts     — author_id REFERENCES users(id), title, body,
--       published_at. All NOT NULL.
-- TODO: CREATE TABLE comments  — post_id REFERENCES posts(id) ON DELETE CASCADE,
--       author_id REFERENCES users(id) and nullable (that is a guest), body,
--       created_at.
-- TODO: CREATE INDEX on posts(author_id) and on comments(post_id).
"""


class BlogError(Exception):
    """Raised when a blog rule refuses an operation."""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the blog database."""
    conn = sqlite3.connect(path)
    # TODO: PRAGMA foreign_keys = ON. Without it SQLite accepts the words
    # ON DELETE CASCADE and then ignores them.
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the schema. Safe to call on every start — IF NOT EXISTS."""
    conn.executescript(SCHEMA)
    conn.commit()


def hash_password(password: str) -> str:
    """TODO: return a salted hash. Never return the password."""
    raise NotImplementedError


def verify_password(stored: str, candidate: str) -> bool:
    """TODO: hash the candidate the same way and compare."""
    raise NotImplementedError


def create_user(
    conn: sqlite3.Connection, username: str, password: str, created_at: str
) -> int:
    """TODO: INSERT INTO users (...) VALUES (?, ?, ?) and return lastrowid."""
    raise NotImplementedError


def authenticate(conn: sqlite3.Connection, username: str, password: str) -> int | None:
    """TODO: SELECT the hash for this username, then verify. None on failure."""
    raise NotImplementedError


def create_post(
    conn: sqlite3.Connection, author_id: int, title: str, body: str, published_at: str
) -> int:
    """TODO: INSERT INTO posts (...) VALUES (?, ?, ?, ?) and return lastrowid."""
    raise NotImplementedError


def list_posts(conn: sqlite3.Connection) -> list[tuple[int, str, str, str]]:
    """TODO: SELECT posts INNER JOIN users, newest first."""
    raise NotImplementedError


def get_post(conn: sqlite3.Connection, post_id: int) -> tuple[str, str, str, str]:
    """TODO: one post plus its author's username. Raise BlogError if missing."""
    raise NotImplementedError


def comments_for(conn: sqlite3.Connection, post_id: int) -> list[tuple[str, str, str | None]]:
    """TODO: a post's comments. LEFT JOIN, so guest comments survive."""
    raise NotImplementedError


def add_comment(
    conn: sqlite3.Connection,
    post_id: int,
    author_id: int | None,
    body: str,
    created_at: str,
) -> int:
    """TODO: INSERT INTO comments (...). author_id may be None."""
    raise NotImplementedError


def delete_post(conn: sqlite3.Connection, post_id: int, requester_id: int) -> None:
    """TODO: DELETE ... WHERE id = ? AND author_id = ?.

    Raise BlogError when rowcount is 0 — that means it was not their post.
    """
    raise NotImplementedError


def main() -> None:
    """Report what the schema built, so the stub is runnable from minute one."""
    conn = connect()
    try:
        init_db(conn)
        rows = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        built = ", ".join(name for (name,) in rows) or "(none yet)"
        on = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        print(f"tables built    : {built}")
        print(f"foreign keys on : {bool(on)}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

Pasted and run untouched, that prints:

```text
tables built    : users
foreign keys on : False
```

Two `TODO`s done and both lines change. That is your progress bar for the
first hour.

Your Flask app then imports it and never writes SQL of its own:

```python
import blog_db
from flask import Flask, g, render_template

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = blog_db.connect("blog.sqlite3")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html", posts=blog_db.list_posts(get_db()))
```

## Requirements

Your blog must:

1. **User signup and login.** Passwords are stored as hashes, never as plain
   text. A hash is a one-way squash: easy to compute, impossible to undo. If
   your database is ever stolen, the thief gets the squash, not the password.
2. **Create a post** — logged-in users only. Inserts one row into `posts`.
3. **List posts** — the homepage shows posts newest-first, with each
   author's username. The username lives in `users`, so this needs a
   **JOIN**: one query, two tables, stitched on `users.id = posts.author_id`.
4. **View a post** — the detail page shows the post body plus all of its
   comments, each with its author's name.
5. **Comment on a post** — inserts into `comments`. A logged-in commenter
   gets their `author_id`; a guest leaves it `NULL`.
6. **Delete your own post** — only the author may delete, and the post's
   comments go with it.

The minimum schema:

- `users` — `id`, `username`, `password_hash`, `created_at`.
- `posts` — `id`, `author_id` (foreign key to `users`), `title`, `body`,
  `published_at`.
- `comments` — `id`, `post_id` (foreign key), `author_id` (foreign key,
  nullable for guests), `body`, `created_at`.

Use `INTEGER PRIMARY KEY AUTOINCREMENT` for ids, and ISO-8601 strings for
timestamps (`DATE('now')`, `DATETIME('now')`). SQLite has no date type;
`2026-05-03` sorts correctly as plain text, which is exactly why the ISO
order — year, month, day — is the one worth using.

You may build the storage either way:

- **Option A** — `sqlite3` from the standard library, with SQL you write
  yourself. This is what the shipped answer does, and what the rest of the
  page teaches.
- **Option B** — the SQLAlchemy ORM, directly or through `Flask-SQLAlchemy`.

Pick one and stay in it. Mixing handwritten SQL and ORM objects over the
same tables gets confusing fast, and the two disagree about who owns the
transaction.

## Constraints

- **Every value passes through a placeholder or an ORM binding. No
  exceptions, in any route.** Not for integers, not for values you are
  certain about, not "just while I test it". The moment there is one
  f-string in one query, the file is no longer auditable — a reader has to
  check every line instead of trusting the pattern. What it costs when
  someone gets it wrong is at the top of this page: a login anyone can walk
  through, and a `users` table anyone can delete.
- **A table name is not a value, and cannot use a placeholder.** `?` binds
  *data*; a table name is *grammar*, and the database has to know it before
  the query is even planned. When you genuinely need a dynamic table name —
  the shipped answer's `count()` does — check it against a fixed set you
  wrote yourself first, then interpolate. Never against user input directly.
- **The connection is per-request.** In Flask that is the `g.db` pattern
  shown in the Starter: open on first use, close in `teardown_appcontext`.
  One module-level connection shared by every request is a bug that only
  appears under load, and SQLite will tell you so — see Common bugs.
- **One source of truth for the schema.** One `schema.sql` file, or one
  `SCHEMA` string, or one set of ORM models. Two copies drift, and the
  moment they drift one of them is lying.
- **`PRAGMA foreign_keys = ON`, on every connection.** SQLite ships with
  foreign keys switched *off* for backwards compatibility. It will accept
  your `REFERENCES` and `ON DELETE CASCADE` and then quietly ignore them.
  The pragma is per-connection, not per-database, so it belongs inside your
  `connect()` and nowhere else.
- **Bootstrapping is idempotent.** `CREATE TABLE IF NOT EXISTS` everywhere,
  so running the app twice cannot crash. Ship a seed command — a `seed.py`
  or a Flask CLI command — that drops, recreates, and loads sample data, so
  a reviewer can get a working blog in one line.

## Expected output

A real run of the shipped answer. It uses an in-memory database and fixed
dates, so it prints the same thing every time and leaves no file behind.
Captured on CPython 3.13.

```bash
$ python challenge-02-blog-with-db-solution.py
```

```text
Blog storage ready (in-memory database for this demo).

-- Signup: hashes stored, never passwords --
created users ada (id 1) and alan (id 2)
stored for ada: a pbkdf2_sha256 hash; the password itself is nowhere

-- Login --
ada + wrong password  -> None
ada + right password  -> user id 1

-- Posts (homepage: newest first, author joined in) --
  2026-05-03  alan  Reading EXPLAIN QUERY PLAN
  2026-05-02  ada   The day my JSON file gave up
  2026-05-01  ada   Parameterize everything

-- One post, with its comments (guests included) --
  Parameterize everything (by ada, 2026-05-01)
    2026-05-01 10:15  alan   Placeholders from day one.
    2026-05-01 11:40  guest  What about table names?

-- Deleting: only the author, comments cascade --
alan tried to delete post 1: refused (only the author may delete a post)
ada deleted post 1: its 2 comments went with it
posts remaining: 2, comments remaining: 0
```

Read that as the six required features in order: signup, login, list,
detail, comment, delete. The last three lines are the whole ownership-and-
cascade rule proved out loud — alan is refused, ada succeeds, and the two
comments leave with the post they belonged to.

Your own build starts a server instead and you click through it in a
browser. The moment worth watching by hand is the delete: press it on
somebody else's post and you should get a refusal, not a traceback.

## Steps

1. **Write the schema first, before any Python.** Three `CREATE TABLE`
   statements. Run the starter after each one and watch `tables built`
   grow. Get `PRAGMA foreign_keys = ON` into `connect()` now, not later —
   the line `foreign keys on : True` is your proof.
2. **Hash a password and look at it.** Print the stored string for a test
   user. It should be unreadable, and hashing the *same* password twice
   should give two different strings, because each one gets its own random
   salt. If those two strings match, you forgot the salt.
3. **Write `create_user` and `authenticate`.** Log in with the wrong
   password and confirm you get `None`, not a crash and not a login.
4. **Write `create_post` and `list_posts`.** `list_posts` is your first
   JOIN. Start with `SELECT * FROM posts`, see that you only have an
   `author_id` number, then join `users` to turn that number into a name.
5. **Write `get_post` and `comments_for`.** Add one comment as a logged-in
   user and one as a guest (`author_id = None`). Then check: do *both*
   appear? If the guest comment vanished, you used an `INNER JOIN` where a
   `LEFT JOIN` belongs. This is the bug the page's LEFT JOIN exists to
   prevent, and it is silent — no error, just a missing comment.
6. **Write `delete_post`.** Put the ownership check in the `WHERE` clause,
   not in an `if` above it, and raise when `rowcount` is 0. Then delete a
   post that has comments and count the comments afterwards. Zero means
   your cascade works; two means the pragma is off.
7. **Wire it into Flask.** Each route becomes one call. A route that looks
   like this is the target:

   ```python
   @app.route("/post/<int:post_id>")
   def view_post(post_id: int) -> str:
       db = get_db()
       try:
           post = blog_db.get_post(db, post_id)
       except blog_db.BlogError:
           abort(404)
       return render_template(
           "blog/view.html", post=post, comments=blog_db.comments_for(db, post_id)
       )
   ```

   Note what is *not* in that route: any SQL. And note the `<int:post_id>`
   converter — Flask has already refused anything that is not a number
   before your function starts.
8. **Audit yourself.** Search your whole project for `f"SELECT`, `f"INSERT`,
   `f"UPDATE`, `f"DELETE`, and for `+` next to a quote. On a clean build you
   find nothing but the allow-listed table name in `count()`.

## The Solution

```python
"""challenge-02-blog-with-db-solution.py — the Week 9 blog's data, on SQLite.

This is the storage layer the challenge asks for: users with hashed
passwords, posts, and comments, all in one SQLite schema, every value bound
through ``?``. Your Flask routes from Week 9 stay your own — each route
becomes one call into this module, which is the point of keeping every line
of SQL in one file.

The password hashing is standard library only: PBKDF2 via
``hashlib.pbkdf2_hmac`` with a random salt, compared with
``hmac.compare_digest``. No plain-text password is ever stored or printed.

This download runs against an in-memory database, walks the six required
features with fixed timestamps, and leaves nothing behind. Point
``connect()`` at a path and the same module backs a real blog.

Run it with::

    python challenge-02-blog-with-db-solution.py
"""

import hashlib
import hmac
import secrets
import sqlite3
from typing import Final

SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id    INTEGER NOT NULL REFERENCES users(id),
    title        TEXT NOT NULL,
    body         TEXT NOT NULL,
    published_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id    INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id  INTEGER REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_posts_author    ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_comments_post   ON comments(post_id);
"""

PBKDF2_ITERATIONS: Final[int] = 600_000


class BlogError(Exception):
    """Raised when a blog rule refuses an operation."""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the blog database with foreign keys (and so ON DELETE) enforced."""
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the schema. Safe to call on every start — IF NOT EXISTS."""
    conn.executescript(SCHEMA)
    conn.commit()


def hash_password(password: str) -> str:
    """Return a salted PBKDF2 hash, self-describing and safe to store.

    Format: ``pbkdf2_sha256$<iterations>$<salt hex>$<digest hex>``. The salt
    is random per user, so two users with the same password store different
    hashes and a stolen table cannot be attacked with one precomputed list.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(stored: str, candidate: str) -> bool:
    """Check a login attempt against a stored hash, in constant time."""
    algorithm, iterations, salt_hex, digest_hex = stored.split("$")
    if algorithm != "pbkdf2_sha256":
        raise BlogError(f"unknown hash algorithm: {algorithm}")
    attempt = hashlib.pbkdf2_hmac(
        "sha256",
        candidate.encode("utf-8"),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(attempt.hex(), digest_hex)


def create_user(
    conn: sqlite3.Connection, username: str, password: str, created_at: str
) -> int:
    """Sign a user up. The password is hashed before it touches the database."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, created_at) "
            "VALUES (?, ?, ?)",
            (username, hash_password(password), created_at),
        )
    return cursor.lastrowid


def authenticate(conn: sqlite3.Connection, username: str, password: str) -> int | None:
    """Return the user's id when the password checks out, else None."""
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    if row is None:
        return None
    user_id, stored = row
    return user_id if verify_password(stored, password) else None


def create_post(
    conn: sqlite3.Connection, author_id: int, title: str, body: str, published_at: str
) -> int:
    """Insert a post and return its id. The route checks login; this inserts."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO posts (author_id, title, body, published_at) "
            "VALUES (?, ?, ?, ?)",
            (author_id, title, body, published_at),
        )
    return cursor.lastrowid


def list_posts(conn: sqlite3.Connection) -> list[tuple[int, str, str, str]]:
    """Return (id, published_at, username, title), newest first — the homepage."""
    cursor = conn.execute(
        """
        SELECT p.id, p.published_at, u.username, p.title
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.author_id
        ORDER BY p.published_at DESC, p.id DESC
        """
    )
    return cursor.fetchall()


def get_post(conn: sqlite3.Connection, post_id: int) -> tuple[str, str, str, str]:
    """Return (title, body, username, published_at) for one post."""
    row = conn.execute(
        """
        SELECT p.title, p.body, u.username, p.published_at
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.author_id
        WHERE p.id = ?
        """,
        (post_id,),
    ).fetchone()
    if row is None:
        raise BlogError(f"no post with id {post_id}")
    return row


def comments_for(conn: sqlite3.Connection, post_id: int) -> list[tuple[str, str, str | None]]:
    """Return (created_at, body, username or None) for a post's comments.

    LEFT JOIN, because a guest comment has a NULL author_id and must still
    appear — an INNER JOIN would silently drop it.
    """
    cursor = conn.execute(
        """
        SELECT c.created_at, c.body, u.username
        FROM comments AS c
        LEFT JOIN users AS u ON u.id = c.author_id
        WHERE c.post_id = ?
        ORDER BY c.created_at, c.id
        """,
        (post_id,),
    )
    return cursor.fetchall()


def add_comment(
    conn: sqlite3.Connection,
    post_id: int,
    author_id: int | None,
    body: str,
    created_at: str,
) -> int:
    """Insert a comment. author_id may be None — that is a guest."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO comments (post_id, author_id, body, created_at) "
            "VALUES (?, ?, ?, ?)",
            (post_id, author_id, body, created_at),
        )
    return cursor.lastrowid


def delete_post(conn: sqlite3.Connection, post_id: int, requester_id: int) -> None:
    """Delete a post — but only when the requester wrote it.

    The ownership check is in the WHERE clause, so checking and deleting are
    one statement: there is no window where the check has passed and the
    delete has not happened. Comments go with the post via ON DELETE CASCADE.
    """
    with conn:
        cursor = conn.execute(
            "DELETE FROM posts WHERE id = ? AND author_id = ?",
            (post_id, requester_id),
        )
    if cursor.rowcount == 0:
        raise BlogError("only the author may delete a post")


def count(conn: sqlite3.Connection, table: str) -> int:
    """Row count for one of this module's tables, name checked by lookup.

    A table name cannot travel through a ``?`` placeholder — it is syntax,
    not a value — so it is validated against the fixed set of tables this
    schema owns before it is ever placed in the query.
    """
    if table not in {"users", "posts", "comments"}:
        raise BlogError(f"unknown table: {table}")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]  # noqa: S608


def main() -> None:
    """Walk the six required features against fixed demo data."""
    conn = connect()
    try:
        init_db(conn)
        print("Blog storage ready (in-memory database for this demo).")

        print("\n-- Signup: hashes stored, never passwords --")
        ada = create_user(conn, "ada", "correct horse battery", "2026-05-01")
        alan = create_user(conn, "alan", "hut 8 forever", "2026-05-01")
        scheme = conn.execute(
            "SELECT password_hash FROM users WHERE id = ?", (ada,)
        ).fetchone()[0].split("$")[0]
        print(f"created users ada (id {ada}) and alan (id {alan})")
        print(f"stored for ada: a {scheme} hash; the password itself is nowhere")

        print("\n-- Login --")
        print(f"ada + wrong password  -> {authenticate(conn, 'ada', 'password123')}")
        print(f"ada + right password  -> user id {authenticate(conn, 'ada', 'correct horse battery')}")

        print("\n-- Posts (homepage: newest first, author joined in) --")
        first = create_post(
            conn, ada, "Parameterize everything",
            "The one habit Week 10 exists to install.", "2026-05-01",
        )
        create_post(
            conn, ada, "The day my JSON file gave up",
            "Forty megabytes, rewritten on every save.", "2026-05-02",
        )
        create_post(
            conn, alan, "Reading EXPLAIN QUERY PLAN",
            "SCAN means the database read everything.", "2026-05-03",
        )
        for post_id, published_at, username, title in list_posts(conn):
            print(f"  {published_at}  {username:<5} {title}")

        print("\n-- One post, with its comments (guests included) --")
        add_comment(conn, first, alan, "Placeholders from day one.", "2026-05-01 10:15")
        add_comment(conn, first, None, "What about table names?", "2026-05-01 11:40")
        title, body, username, published_at = get_post(conn, first)
        print(f"  {title} (by {username}, {published_at})")
        for created_at, comment_body, commenter in comments_for(conn, first):
            print(f"    {created_at}  {commenter or 'guest':<6} {comment_body}")

        print("\n-- Deleting: only the author, comments cascade --")
        try:
            delete_post(conn, first, alan)
        except BlogError as exc:
            print(f"alan tried to delete post {first}: refused ({exc})")
        comments_before = count(conn, "comments")
        delete_post(conn, first, ada)
        print(f"ada deleted post {first}: its {comments_before} comments went with it")
        print(f"posts remaining: {count(conn, 'posts')}, comments remaining: {count(conn, 'comments')}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

**Why it works.**

**The schema does the arguing.** Look at how much of the blog's rulebook is
in the `CREATE TABLE` statements rather than in Python. `username TEXT NOT
NULL UNIQUE` means two people cannot claim the same name — not "your code
checks", but *cannot*, even if two signups land at the same instant.
`author_id INTEGER NOT NULL REFERENCES users(id)` means a post without a
real author cannot exist. `comments.author_id` has no `NOT NULL`, and that
single omission is what makes guest comments legal. Rules in the table are
enforced once, for everybody. Rules in Python are enforced wherever you
remembered to write the `if`.

**Every value is a `?`, and you can check that by eye.** Scan the file: each
`execute` call is a string with question marks in it and a tuple beside it.
The string never changes shape at runtime. That is what makes the file
auditable — a reader confirms the pattern instead of reasoning about each
query. The recipe and the ingredients arrive separately, so an ingredient
can never become a step.

**The one f-string in the file, and why it is not a hole.** `count()` builds
`f"SELECT COUNT(*) FROM {table}"`. A table name is grammar, not data, so no
placeholder can carry it. The safety comes from the line above:

```python
if table not in {"users", "posts", "comments"}:
    raise BlogError(f"unknown table: {table}")
```

The value that reaches the query is one of three strings this file wrote
itself. Anything else was rejected before the SQL existed. That is the only
safe shape for a dynamic identifier: an allow-list you control, checked
first.

**Passwords are stored as a self-describing hash.** The stored string is
`pbkdf2_sha256$600000$<salt>$<digest>`. It carries its own algorithm, its
own iteration count, and its own salt, so a future version can raise the
iterations and still check old passwords. The random salt per user means two
people with the same password store different rows — so a thief cannot crack
them all at once with one precomputed list. `hmac.compare_digest` does the
final comparison; a plain `==` stops early on the first wrong character, and
the time it takes leaks how much of the guess was right.

**The JOINs are two different questions.** `list_posts` uses `INNER JOIN`:
every post has an author, and a post with no author is broken data you want
to notice. `comments_for` uses `LEFT JOIN`: a guest comment has `author_id =
NULL`, matches no user row, and an `INNER JOIN` would throw it away in
silence. LEFT means "keep the left-hand rows even when the right-hand side
has nothing" — the comment survives, and `username` comes back `None`, which
the print turns into `guest`.

**Deleting is one statement, on purpose.** `delete_post` does not read the
post, check the author, and then delete. It puts the ownership test in the
`WHERE` clause, so checking and deleting are the same instant, and asks
`cursor.rowcount` afterwards. Zero rows means the post was missing *or* was
not theirs — either way, refuse. Split it into two statements and you open a
gap between them where the post could change hands.

**The comments disappear because the database chose to, not because Python
remembered to.** `ON DELETE CASCADE` on `comments.post_id` does it — but
only because `connect()` runs `PRAGMA foreign_keys = ON` first. That pragma
is the difference between a rule and a comment.

**`with conn:` is the transaction.** Every write is wrapped in it. On a
clean exit it commits; on an exception it rolls back. It is not a
"close the connection" block — this is the one Python `with` that does not
close the thing it opened, which is worth knowing before it surprises you.

## Download and run

Download
[challenge-02-blog-with-db-solution.py](./challenge-02-blog-with-db-solution.py)
and run it:

```bash
python challenge-02-blog-with-db-solution.py
```

Nothing to install. The storage layer is standard library only — `sqlite3`,
`hashlib`, `hmac`, `secrets` — and SQLite ships inside Python. It builds its
database in memory, prints the run above, and exits leaving no file behind.
Point `connect()` at a path like `blog.sqlite3` and the same module backs a
real blog.

The Flask half is yours to build, and *that* needs one install:

```bash
pip install Flask
```

If you take Option B, add `pip install Flask-SQLAlchemy` as well.

The `-solution` in the filename is there so this file cannot collide with
your own `blog_db.py`. Keep them separate — copy the starter into your own
name and work there.

## Common bugs to catch

- **Anyone can log in as anyone.** Your login builds the query with an
  f-string, and a username of `' OR '1'='1` matches every row. There is no
  exception and no error message; the app just works for the attacker. The
  fix is the placeholder, everywhere, with no survivors.

- **`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The
  current statement uses 1, and there are 3 supplied.`** You passed
  `("ada")` instead of `("ada",)`. Without the comma that is just a string
  in brackets, and Python reads its three characters as three separate
  values. A one-item tuple always needs the trailing comma.

- **`sqlite3.IntegrityError: UNIQUE constraint failed: users.username`**
  The schema is working exactly as designed — somebody tried to sign up
  with a taken name. Catch it in the signup route and flash "that username
  is taken", rather than letting it become a 500.

- **`sqlite3.IntegrityError: FOREIGN KEY constraint failed`** You inserted a
  comment on a post id that does not exist, or a post for a missing user.
  Again, the schema is doing its job. Either check first, or catch it and
  return a 404.

- **You deleted a post and its comments are still there.** `ON DELETE
  CASCADE` is in your schema but `PRAGMA foreign_keys = ON` is not in your
  `connect()`. SQLite parsed the cascade, stored it, and ignored it. The
  pragma is per-connection: setting it once in a script does nothing for the
  next connection Flask opens.

- **A guest's comment never appears on the page.** `INNER JOIN users` on
  `comments`. The guest row has `author_id = NULL`, matches no user, and
  gets dropped without a word. `LEFT JOIN` keeps it. Silent data loss is
  worse than a crash, so test with a guest comment every time.

- **Everything works, then a restart and it is all gone.** You never
  committed. `sqlite3` opens a transaction for you on the first write and
  waits — nothing is durable until `conn.commit()`, or until a `with conn:`
  block exits cleanly. Wrap every write.

- **`sqlite3.ProgrammingError: SQLite objects created in a thread can only
  be used in that same thread.`** You made one connection at module level
  and shared it across requests. Flask handles requests on different
  threads. Use the per-request `g.db` pattern from the Starter — one
  connection per request, closed in `teardown_appcontext`.

- **Passwords in the table are readable.** You stored `password` where
  `password_hash` belongs. Open the file with `sqlite3 blog.sqlite3` and run
  `SELECT * FROM users;` — if you can read a password, so can anyone who
  ever copies that file. Hash before the value touches the database, which
  is why `create_user` calls `hash_password` inside the `execute` call and
  never keeps the plain text.

- **Two users with the same password have identical hashes.** You hashed
  without a salt. It means one cracked password cracks both accounts, and a
  precomputed table cracks them without any work at all. `secrets.token_bytes(16)`
  per user, stored alongside the digest, fixes it.

## Under the hood

<details>
<summary>Under the hood — what the database actually does with a placeholder</summary>

The placeholder is not string quoting with extra steps. Nothing gets
escaped, and no quotes are added. Two separate things travel to the
database.

First the SQL text goes down on its own and is **prepared** — parsed into a
tree, planned, compiled into a little bytecode program for SQLite's virtual
machine. At that moment the shape of the statement is fixed forever: which
tables, which columns, which comparisons. The `?` is a numbered slot in that
program.

Then the values are **bound** into the slots, as typed data — an integer as
an integer, a string as a string, `None` as SQL `NULL`. They are never
parsed as SQL, because parsing already happened.

That is why injection is impossible rather than merely difficult. A username
of `'; DROP TABLE users; --` becomes a 24-character string sitting in slot
one. There is no path from a bound value back into the grammar.

You can watch the split with the driver's own trace:

```python
conn.set_trace_callback(print)
conn.execute("SELECT id FROM users WHERE username = ?", ("ada",))
# SELECT id FROM users WHERE username = ?
```

The statement is logged with the question mark still in it. The value is not
part of the statement.

Two practical consequences fall out of this:

- **Prepared statements are reusable and faster.** Run the same `INSERT`
  five hundred times with different values and the parse-and-plan work
  happens once. That is what `executemany` is for, and why a bulk import
  written with `executemany` beats a loop of f-strings by a wide margin —
  quite apart from being safe.
- **`LIKE` patterns need care anyway.** Binding `?` for a `LIKE` value is
  still correct, but `%` and `_` inside the *value* are wildcards to `LIKE`.
  That is not injection — the worst case is a search that matches too much —
  but if you want a literal `%`, escape it and add `ESCAPE '\'`.

Named placeholders exist too, and read better once a query has more than
three or four values:

```python
conn.execute(
    "INSERT INTO posts (author_id, title, body, published_at) "
    "VALUES (:author_id, :title, :body, :published_at)",
    {"author_id": 1, "title": t, "body": b, "published_at": when},
)
```

Other drivers use other marks — `%s` in `psycopg2` and `mysqlclient`, `?` in
`sqlite3`. It is called the *paramstyle*, and it is a property of the driver,
not of SQL. `sqlite3.paramstyle` will tell you which one you are holding.
The `%s` in `psycopg2` is **not** Python's `%` formatting, however much it
looks like it — pass the values as a second argument and let the driver do
it.

</details>

<details>
<summary>Under the hood — why a table name cannot be a placeholder</summary>

Because of the paragraph above. The statement is compiled *before* the
values arrive, and the compiler cannot plan a query without knowing which
table it reads. The name is part of the grammar. So is a column name, so is
`ASC` versus `DESC`, so is the whole `ORDER BY` clause.

`conn.execute("SELECT * FROM ?", ("users",))` therefore fails with a syntax
error, and the failure is the database being honest rather than being
awkward.

The safe pattern is the one in `count()`: an allow-list you wrote, checked
before the string is built.

```python
SORTS = {"newest": "published_at DESC", "oldest": "published_at ASC"}

def list_sorted(conn, sort_key):
    order = SORTS.get(sort_key)          # user input picks a key, never text
    if order is None:
        raise BlogError(f"unknown sort: {sort_key}")
    return conn.execute(f"SELECT id, title FROM posts ORDER BY {order}").fetchall()
```

The user's input never reaches the SQL. It only ever selects *from* strings
the file already contained. Sanitising a table name with a regex is the
wrong move — allow-lists say yes to a known-good set, blocklists try to
guess every bad input, and the second one has lost this argument for thirty
years.

`# noqa: S608` on that line in the shipped answer is a note to the linter:
flake8's Bandit rules flag any f-string near `SELECT`, correctly, and this
one has been checked by hand.

</details>

<details>
<summary>Under the hood — why 600,000 iterations, and what a slow hash buys</summary>

A password hash is deliberately, expensively slow. That reads like a bug and
is the entire feature.

Hashing is one-way: easy forwards, impossible backwards. But an attacker
holding your stolen `users` table does not need to go backwards. They guess
forwards — take a list of common passwords, hash each one, compare. With a
fast hash like a bare SHA-256, a normal graphics card gets through billions
of guesses a second and the whole common-password list falls in minutes.

PBKDF2 fixes that by making one guess cost 600,000 SHA-256 rounds instead of
one. Your login gets slower by a fraction of a second, which nobody notices.
The attacker's billions per second becomes thousands, and the arithmetic
that made the attack cheap stops working.

The number is not permanent. It is set to track OWASP's current guidance,
which rises as hardware does — and because the iteration count is stored
inside each hash string, you can raise it for new passwords while old ones
keep verifying at their old count. That is what the `$`-separated format
buys you.

The salt solves a different problem. Without it, identical passwords give
identical hashes, so an attacker sees at a glance which accounts share one,
and a rainbow table — an enormous precomputed hash-to-password lookup —
cracks everyone at once. A random 16-byte salt per user means every hash is
unique and every attack has to be run per-account.

In a real Flask blog you would reach for
`werkzeug.security.generate_password_hash` and `check_password_hash`, which
ship with Flask and do exactly this, in this format, with sensible defaults.
The shipped answer spells it out in standard library calls only so the whole
mechanism is visible — and so the download needs nothing installed. Both are
correct. Neither is `hashlib.sha256(password)`, which is not.

Modern alternatives — Argon2id, scrypt, bcrypt — are memory-hard as well as
slow, which blunts custom hardware in a way PBKDF2 cannot. If you are
starting fresh and can add a dependency, `argon2-cffi` is the better pick.

</details>

<details>
<summary>Under the hood — indexes, and reading EXPLAIN QUERY PLAN</summary>

An index is the index at the back of a book. Without one, "find every
mention of penguins" means reading every page. With one, you look up
`penguins` and jump.

`comments_for` filters on `post_id`, so `idx_comments_post` exists. Ask
SQLite what it intends to do:

```sql
EXPLAIN QUERY PLAN
SELECT c.created_at, c.body FROM comments AS c WHERE c.post_id = 1;
```

```text
SEARCH c USING INDEX idx_comments_post (post_id=?)
```

`SEARCH` means it jumped. Drop the index and the same query says:

```text
SCAN c
```

`SCAN` means it read every row. With forty comments you will never feel the
difference. With four million you will feel nothing else.

Indexes are not free — each one is a second copy of that column, kept sorted,
updated on every write. Index the columns you filter and join on; do not
index everything and hope. Primary keys are indexed already, so
`WHERE id = ?` is fast without you doing anything.

`EXPLAIN QUERY PLAN` is the first tool to reach for when a page gets slow.
It is a plan, not a measurement — it tells you what the database intends,
which is usually enough to spot the missing index.

</details>

<details>
<summary>Under the hood — the two project layouts, and the ORM road</summary>

Option A, handwritten `sqlite3`, laid out the way the Flask tutorial does
it:

```text
blog/
├── app.py
├── schema.sql
├── db.py                # get_db(), close_db(), init_db_command()
├── auth.py              # login/logout/register routes
├── blog.py              # post + comment routes
├── templates/
│   ├── base.html
│   ├── auth/
│   └── blog/
└── static/
```

The official tutorial at <https://flask.palletsprojects.com/en/stable/tutorial/>
builds almost exactly this and is worth reading start to finish.

Option B, SQLAlchemy:

```text
blog/
├── app.py
├── extensions.py        # db = SQLAlchemy()
├── models.py            # User, Post, Comment
├── auth.py
├── blog.py
└── templates/
```

An ORM — object-relational mapper — lets you write `Post.query.filter_by(
author_id=1)` and hands you Python objects instead of tuples. It builds the
SQL for you, and it parameterises by default, so the injection rule is kept
for you rather than by you.

What you give up is knowing what ran. The classic trap is the **N+1 query**:
you loop over a hundred posts printing `post.author.username`, and the ORM
quietly issues one query for the posts and then a hundred more, one per
author. The handwritten `INNER JOIN` in `list_posts` does it in one. The fix
in SQLAlchemy is eager loading — `joinedload` or `selectinload` — but you
have to know to ask for it, and you only know by looking at the SQL it
emitted.

That is the honest trade, and the reason this week starts with the SQL:
an ORM is a good tool once you can read what it produces, and a fog machine
before that. Set `SQLALCHEMY_ECHO = True` and watch the queries scroll past
for a while. Docs: <https://flask-sqlalchemy.palletsprojects.com/>.

</details>

## Acceptance checklist

- [ ] `PRAGMA foreign_keys = ON` runs on every connection, and you can show
      it returning `1`.
- [ ] Signing up twice with the same username raises `IntegrityError`
      instead of creating a second account.
- [ ] `SELECT * FROM users;` in the `sqlite3` shell shows no readable
      password, and two users with the same password have different hashes.
- [ ] Logging in with the wrong password fails; logging in with the right
      one returns the user id.
- [ ] The homepage lists posts newest-first with each author's username,
      from one JOINed query.
- [ ] A post page shows a logged-in user's comment **and** a guest's
      comment.
- [ ] Deleting somebody else's post is refused, and refused with a message
      rather than a traceback.
- [ ] Deleting your own post removes its comments too, and you can prove it
      with a `COUNT(*)`.
- [ ] Searching the whole project for `f"SELECT`, `f"INSERT`, `f"UPDATE`,
      `f"DELETE` finds nothing but an allow-listed identifier.
- [ ] The app survives a restart with its data, and a second run of the
      bootstrap without crashing.

Marked out of 100:

| Area | Points |
|---|---|
| Schema design and foreign keys | 15 |
| Auth: hashed passwords, login required where it should be | 15 |
| All six required features work in the browser | 30 |
| Parameterised queries / ORM bindings everywhere | 15 |
| Per-request connection or session handling | 10 |
| Templates render correctly with joined data | 5 |
| README with run instructions, seed command, sample credentials | 10 |

## Stretch

- **Tags, the many-to-many way.** A `tags` table and a `post_tags` junction
  table holding `(post_id, tag_id)` as a composite primary key. A post has
  many tags, a tag has many posts, and neither table needs to know how many.
- **Full-text search** with SQLite's FTS5 module over `posts.title` and
  `posts.body`. `CREATE VIRTUAL TABLE posts_fts USING fts5(...)`, then
  `WHERE posts_fts MATCH ?` — placeholder, still.
- **Paginate the homepage** with `LIMIT` and `OFFSET`. Then read up on why
  large offsets get slow: the database still walks the rows it is skipping.
  Keyset pagination — `WHERE published_at < ?` — does not.
- **A real migration tool.** Add Alembic and write one migration that adds
  an `edited_at` column to `posts`. `ALTER TABLE` in SQLite is more limited
  than elsewhere; finding out how Alembic works around it is the lesson.
- **Find your slowest query** and run `EXPLAIN QUERY PLAN` on it. Add an
  index that turns a `SCAN` into a `SEARCH`, and record both plans in your
  README.
- **Soft delete.** Replace `DELETE` with an `deleted_at` column and filter
  it out of every read. Then notice how many queries you had to remember to
  change, and why a view or a repository function is the usual answer.

References:

- `sqlite3` — <https://docs.python.org/3/library/sqlite3.html>
- SQLite foreign key support — <https://www.sqlite.org/foreignkeys.html>
- SQLite query planning — <https://www.sqlite.org/queryplanner.html>
- Flask tutorial (blog with SQLite) — <https://flask.palletsprojects.com/en/stable/tutorial/>
- OWASP password storage guidance — <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
