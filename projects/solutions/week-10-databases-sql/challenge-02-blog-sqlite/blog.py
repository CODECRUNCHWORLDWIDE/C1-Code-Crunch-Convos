"""Post and comment routes. Required features 2 to 6.

Every query in this file passes its values as `?` parameters. Every query that
shows an author's name gets it from a JOIN rather than from a second round
trip, because "one query per row" is how a fast page becomes a slow one.
"""

from __future__ import annotations

import sqlite3

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.wrappers import Response

from auth import login_required
from db import get_db

bp = Blueprint("blog", __name__)

# INNER JOIN, not LEFT: posts.author_id is NOT NULL and cascades on user
# delete, so a post without an author cannot exist. Using INNER states that.
INDEX_SQL = """
SELECT   p.id           AS id,
         p.title        AS title,
         p.body         AS body,
         p.published_at AS published_at,
         u.username     AS author,
         (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) AS comment_count
FROM     posts AS p
INNER JOIN users AS u ON u.id = p.author_id
ORDER BY p.published_at DESC, p.id DESC
"""

POST_SQL = """
SELECT   p.id           AS id,
         p.title        AS title,
         p.body         AS body,
         p.published_at AS published_at,
         p.author_id    AS author_id,
         u.username     AS author
FROM     posts AS p
INNER JOIN users AS u ON u.id = p.author_id
WHERE    p.id = ?
"""

# LEFT JOIN here, because comments.author_id is nullable -- a guest comment
# has no user row to match, and an INNER JOIN would silently hide it.
COMMENTS_SQL = """
SELECT   c.id         AS id,
         c.body       AS body,
         c.created_at AS created_at,
         u.username   AS author
FROM     comments AS c
LEFT JOIN users AS u ON u.id = c.author_id
WHERE    c.post_id = ?
ORDER BY c.created_at, c.id
"""


@bp.route("/")
def index() -> str:
    """Feature 3 -- homepage, newest first, author joined in."""
    posts = get_db().execute(INDEX_SQL).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(post_id: int, check_author: bool = False) -> sqlite3.Row:
    """Fetch one post or 404. Optionally 403 if the visitor is not its author."""
    post = get_db().execute(POST_SQL, (post_id,)).fetchone()
    if post is None:
        abort(404, f"Post {post_id} does not exist.")
    if check_author and post["author_id"] != g.user["id"]:
        abort(403)
    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> str | Response:
    """Feature 2 -- create a post. Logged-in users only."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title:
            flash("Title is required.")
        else:
            db = get_db()
            cursor = db.execute(
                "INSERT INTO posts (author_id, title, body) VALUES (?, ?, ?)",
                (g.user["id"], title, body),
            )
            db.commit()
            return redirect(url_for("blog.view", post_id=cursor.lastrowid))
    return render_template("blog/create.html")


@bp.route("/post/<int:post_id>")
def view(post_id: int) -> str:
    """Feature 4 -- one post plus its comments."""
    post = get_post(post_id)
    comments = get_db().execute(COMMENTS_SQL, (post_id,)).fetchall()
    return render_template("blog/view.html", post=post, comments=comments)


@bp.route("/post/<int:post_id>/comment", methods=("POST",))
def comment(post_id: int) -> Response:
    """Feature 5 -- comment on a post. Guests allowed; author_id stays NULL."""
    get_post(post_id)                      # 404 before writing anything
    body = request.form.get("body", "").strip()
    if not body:
        flash("Comment cannot be empty.")
        return redirect(url_for("blog.view", post_id=post_id))

    # g.user is None for a guest, and None becomes SQL NULL when bound. This
    # is the whole implementation of "nullable for guests".
    author_id = g.user["id"] if g.user else None
    db = get_db()
    db.execute(
        "INSERT INTO comments (post_id, author_id, body) VALUES (?, ?, ?)",
        (post_id, author_id, body),
    )
    db.commit()
    flash("Comment posted.")
    return redirect(url_for("blog.view", post_id=post_id))


@bp.route("/post/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id: int) -> Response:
    """Feature 6 -- delete your own post. Comments go with it.

    There is no second DELETE for the comments. `comments.post_id` is declared
    ON DELETE CASCADE and every connection runs PRAGMA foreign_keys = ON, so
    SQLite removes them inside the same statement. That is one atomic
    operation instead of two that could half-fail.
    """
    get_post(post_id, check_author=True)
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    flash("Post deleted.")
    return redirect(url_for("index"))
