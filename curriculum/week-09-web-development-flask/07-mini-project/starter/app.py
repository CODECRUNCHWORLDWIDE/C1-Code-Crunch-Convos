"""
Mini-project starter — Personal Blog (Flask)
============================================

A minimal scaffold for the Week 9 personal-blog mini-project. Read the
mini-project README for the full spec and rubric.

What works out of the box
-------------------------
* GET /             -> renders index.html with one seed post
* GET /post/<id>    -> 501 Not Implemented (you fill this in)
* GET /new          -> 501 Not Implemented (you fill this in)
* POST /new         -> 501 Not Implemented (you fill this in)

Run it
------
    pip install flask
    python app.py

Then open http://127.0.0.1:5000.
"""
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count

from flask import Flask, abort, render_template

app: Flask = Flask(__name__)
# Required for flash() and session() once you add the form. In a real app,
# load this from an environment variable (see lecture 3).
app.secret_key = "dev-only-change-me"

_id_seq = count(1)


@dataclass
class Post:
    """A single blog post."""
    id: int
    title: str
    body: str
    created_at: datetime = field(default_factory=datetime.now)


# Module-level "database" — wiped on every restart. Week 10 replaces this
# with SQLite. For now this is enough to learn Flask without DB friction.
POSTS: list[Post] = [
    Post(
        id=next(_id_seq),
        title="Welcome to my blog",
        body=(
            "This is the seed post in the starter scaffold. Edit me, "
            "delete me, or build the /new form and replace me with your "
            "first real post."
        ),
    ),
]


def find_post(post_id: int) -> Post:
    """Return the post with this id, or 404."""
    for post in POSTS:
        if post.id == post_id:
            return post
    abort(404)


@app.route("/")
def index() -> str:
    """List all posts, newest first."""
    posts_newest_first = sorted(POSTS, key=lambda p: p.created_at, reverse=True)
    return render_template("index.html", posts=posts_newest_first)


@app.route("/post/<int:post_id>")
def show_post(post_id: int):
    """Render one post in full. You will implement post.html."""
    # TODO (you):
    #   1. Fetch the post with find_post(post_id).
    #   2. Create templates/post.html that extends base.html.
    #   3. Return render_template("post.html", post=post).
    return ("Not implemented — render the post here.", 501)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    """Show the create-post form on GET; create a post on POST."""
    # TODO (you):
    #   - GET:  render templates/new.html with empty title/body.
    #   - POST: read request.form, validate (see rubric in README),
    #           on error flash and re-render with typed values,
    #           on success append to POSTS, flash, redirect("/").
    return ("Not implemented — build the form here.", 501)


if __name__ == "__main__":
    app.run(debug=True)
