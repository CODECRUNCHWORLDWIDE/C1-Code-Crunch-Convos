"""The blog's routes.

Every view is thin: it reads the request, calls one function in :mod:`blog.db`,
and renders a template. That thinness is the point — the interesting logic
lives in functions that a unit test can call directly, and the views are left
with only the wiring that an *integration* test (the Flask test client) is the
right tool for.
"""

from __future__ import annotations

import logging

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

# `redirect()` returns a *werkzeug* Response, not `flask.Response`. Annotating
# these views with `flask.Response` is the classic mypy trip-hazard here:
#   error: Incompatible return value type (got "werkzeug.wrappers.response.Response",
#   expected "flask.wrappers.Response")
from werkzeug.wrappers import Response

from blog import db
from blog.auth import login_required

logger = logging.getLogger(__name__)

bp = Blueprint("blog", __name__)

TITLE_MAX = 120
BODY_MAX = 10_000


@bp.get("/")
def index() -> str:
    """List every post, newest first."""
    return render_template("index.html", posts=db.list_posts())


@bp.get("/about")
def about() -> str:
    """A static page. Exists so the parametrized 'every page is 200' test has three rows."""
    return render_template("about.html")


@bp.get("/posts/new")
def new_post_form() -> str:
    """Render the create-a-post form.

    Registered *before* ``/posts/<int:post_id>`` for readability only — the
    ``int`` converter already refuses to match the literal string ``new``.
    """
    return render_template("new.html", title="", body="", error=None)


@bp.get("/posts/<int:post_id>")
def show_post(post_id: int) -> str:
    """Render one post, or 404 if it does not exist."""
    post = db.get_post(post_id)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


@bp.post("/posts")
def create_post() -> Response | tuple[str, int]:
    """Create a post from form data, or re-render the form with a 400."""
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    error = _validate(title, body)
    if error is not None:
        # 400 plus the form again, with what the user typed still in it. A bare
        # 400 with no body is technically correct and miserable to use.
        return render_template("new.html", title=title, body=body, error=error), 400

    post_id = db.create_post(title, body)
    flash("Post published.", "success")
    return redirect(url_for("blog.show_post", post_id=post_id))


@bp.route("/posts/<int:post_id>", methods=["DELETE"])
@bp.post("/posts/<int:post_id>/delete")
@login_required
def delete_post(post_id: int) -> Response:
    """Delete a post.

    Two rules, one view. ``DELETE /posts/<id>`` is what an API client sends;
    ``POST /posts/<id>/delete`` is what an HTML form can send, because browsers
    only speak GET and POST. Werkzeug routes on the method, so ``GET
    /posts/<id>`` still reaches :func:`show_post`.
    """
    if not db.delete_post(post_id):
        abort(404)
    flash("Post deleted.", "success")
    return redirect(url_for("blog.index"))


def _validate(title: str, body: str) -> str | None:
    """Return an error message for a bad post, or ``None`` if it is fine."""
    if not title or not body:
        return "Title and body are both required."
    if len(title) > TITLE_MAX:
        return f"Title must be {TITLE_MAX} characters or fewer."
    if len(body) > BODY_MAX:
        return f"Body must be {BODY_MAX} characters or fewer."
    return None


def page_not_found(error: object) -> tuple[str, int]:
    """Render the 404 page and log the miss.

    Registered on the *app* rather than the blueprint so it also catches URLs
    that match no route at all. The warning is what the ``caplog`` stretch test
    asserts on.
    """
    logger.warning("404 Not Found: %s", request.path)
    return render_template("404.html"), 404
