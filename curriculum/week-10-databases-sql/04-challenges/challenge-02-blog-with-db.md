# Challenge 02 — Flask Blog backed by SQLite

In Week 9 you built a Flask blog. Posts probably lived in a Python dict or a JSON file. This challenge replaces the storage layer with a real database — your choice of plain `sqlite3` or the SQLAlchemy ORM.

## Goal

Refactor your Week 9 blog so all post data, comment data, and user data live in a SQLite database. The routes, templates, and visible behavior should change as little as possible.

You may use:

- **Option A**: `sqlite3` from the standard library with handwritten SQL.
- **Option B**: SQLAlchemy ORM (either directly or via the `Flask-SQLAlchemy` extension).

Pick one. Don't mix the two; it gets confusing.

## Schema

Minimum schema:

- `users` — `id`, `username`, `password_hash`, `created_at`.
- `posts` — `id`, `author_id` (FK to `users`), `title`, `body`, `published_at`.
- `comments` — `id`, `post_id` (FK), `author_id` (FK, nullable for guests), `body`, `created_at`.

Use `INTEGER PRIMARY KEY AUTOINCREMENT` for ids and ISO-8601 strings for timestamps (`DATE('now')`, `DATETIME('now')`).

## Required features

1. **User signup / login** — passwords stored as hashes, never as plain text. Use `werkzeug.security.generate_password_hash` and `check_password_hash`.
2. **Create a post** — only logged-in users. Inserts into `posts`.
3. **List posts** — homepage shows posts newest-first. Use a JOIN to include the author's username.
4. **View a post** — detail page shows the post body plus all its comments (joined to author).
5. **Comment on a post** — inserts into `comments`. Logged-in users have `author_id` set; otherwise it stays NULL.
6. **Delete your own post** — only the author may delete. Cascading delete should remove related comments (either with `ON DELETE CASCADE` or an explicit transaction).

## Non-negotiables

- **All values pass through parameters / ORM bindings.** Never f-string a value into SQL, in any route.
- Database connection is scoped per-request (`g.db` in Flask is the classic pattern, or a SQLAlchemy session).
- A single source of truth for the schema (one `schema.sql` file or one set of ORM models).
- A `seed.py` or Flask CLI command that drops + recreates the schema and loads sample data.

## Recommended structure (Option A: `sqlite3`)

```
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

This mirrors the Flask tutorial at <https://flask.palletsprojects.com/en/stable/tutorial/>, which is an excellent reference.

## Recommended structure (Option B: SQLAlchemy)

```
blog/
├── app.py
├── extensions.py        # db = SQLAlchemy()
├── models.py            # User, Post, Comment
├── auth.py
├── blog.py
└── templates/
```

If you go this route, also read <https://flask-sqlalchemy.palletsprojects.com/>.

## Example: a parameterized route (Option A)

```python
from flask import Blueprint, abort, g, render_template

bp = Blueprint("blog", __name__)

@bp.route("/post/<int:post_id>")
def view_post(post_id: int) -> str:
    cursor = g.db.cursor()
    cursor.execute(
        """
        SELECT  p.id, p.title, p.body, p.published_at, u.username AS author
        FROM    posts AS p
        INNER JOIN users AS u ON u.id = p.author_id
        WHERE   p.id = ?
        """,
        (post_id,),
    )
    post = cursor.fetchone()
    if post is None:
        abort(404)
    cursor.execute(
        """
        SELECT c.body, c.created_at, u.username AS author
        FROM   comments AS c
        LEFT JOIN users AS u ON u.id = c.author_id
        WHERE  c.post_id = ?
        ORDER BY c.created_at
        """,
        (post_id,),
    )
    comments = cursor.fetchall()
    return render_template("blog/view.html", post=post, comments=comments)
```

## Stretch goals

- Add a tag system (many-to-many): a `tags` table and a `post_tags` junction table.
- Add full-text search using SQLite's FTS5 module on `posts.title` and `posts.body`.
- Paginate the homepage (`LIMIT` + `OFFSET`).
- Add a real migration tool (Alembic) and write one migration that adds an `edited_at` column to `posts`.
- Add `EXPLAIN QUERY PLAN` output for the slowest query you can find, and add an index that improves it.

## Rubric (out of 100)

| Area                                                                | Points |
|---------------------------------------------------------------------|--------|
| Schema design + foreign keys                                        | 15     |
| Auth: hashed passwords, login required where it should be           | 15     |
| All six required features work in the browser                       | 30     |
| Parameterized queries / ORM bindings everywhere                     | 15     |
| Per-request connection / session handling                           | 10     |
| Templates render correctly with joined data                         | 5      |
| README with run instructions, seed command, sample credentials      | 10     |
