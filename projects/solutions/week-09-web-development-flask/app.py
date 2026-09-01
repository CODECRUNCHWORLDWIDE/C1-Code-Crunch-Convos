"""Personal blog web app -- Week 9 reference solution.

Covers the mini-project specification in full, plus homework problems 1-6 and
the week-level stretch goals (`/api/posts`, `/healthz`, pagination).

Posts live in a module-level list. Restarts wipe them; Week 10 swaps `POSTS`
for a SQLite table and almost none of the view code below has to change.

Run:
    pip install -r requirements.txt
    python app.py
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from weather import WeatherError, get_current_weather

load_dotenv()  # reads .env in development; a no-op when the file is absent

app: Flask = Flask(__name__)

# Signed-cookie sessions need a key. In development we fall back to a constant
# so the app runs straight out of the box; in production the environment must
# supply a real one (see .env.example and the Procfile).
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Homework problem 6. Hardcoded-password auth is a DEMO of how sessions work,
# not a way to protect anything. See 00-overview.md for what is wrong with it.
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "letmein")

TITLE_MAX = 120
BODY_MAX = 10_000
PAGE_SIZE = 5


@dataclass
class Post:
    """One blog post. `tags` arrives in homework problem 4."""

    id: int
    title: str
    body: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)


_id_seq = count(1)

POSTS: list[Post] = [
    Post(
        next(_id_seq),
        "Hello, Flask",
        "First post. Jinja templates are a great deal clearer than f-strings "
        "once you have more than two lines of HTML to produce.",
        tags=["flask", "python"],
    ),
    Post(
        next(_id_seq),
        "Templates rule",
        "Template inheritance keeps the header in exactly one place. Adding a "
        "page becomes one new file and two block overrides.",
        tags=["flask", "jinja"],
    ),
    Post(
        next(_id_seq),
        "Static files",
        "CSS lives in static/ and is linked with url_for so the path survives "
        "a change of prefix.",
        tags=["css", "flask"],
    ),
    Post(
        next(_id_seq),
        "Post, redirect, get",
        "Redirecting after a successful POST is what stops a refresh from "
        "publishing the same post twice.",
        tags=["http", "flask"],
    ),
    Post(
        next(_id_seq),
        "Sessions are signed, not encrypted",
        "The browser can read a Flask session cookie. It just cannot forge "
        "one. Never put a secret in there.",
        tags=["security", "flask"],
    ),
    Post(
        next(_id_seq),
        "Query strings",
        "request.args holds the part of the URL after the question mark. "
        "Always pass a default.",
        tags=["http", "python"],
    ),
    Post(
        next(_id_seq),
        "Deploying for free",
        "gunicorn binds 0.0.0.0 on the host's PORT, and the secret key comes "
        "from the environment.",
        tags=["deployment"],
    ),
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def find_post(post_id: int) -> Post:
    """Return the post with `post_id`, or 404 out of the request entirely."""
    for post in POSTS:
        if post.id == post_id:
            return post
    abort(404)


def newest_first() -> list[Post]:
    """Posts sorted newest first, with the id sequence breaking timestamp ties."""
    return sorted(POSTS, key=lambda p: (p.created_at, p.id), reverse=True)


def parse_tags(raw: str) -> list[str]:
    """Split a comma-separated tag field into clean, unique, lowercase tags.

    `"Python, flask ,, PYTHON"` -> `["python", "flask"]`.
    """
    seen: list[str] = []
    for chunk in raw.split(","):
        tag = chunk.strip().lower()
        if tag and tag not in seen:
            seen.append(tag)
    return seen


def paginate(items: list[Post], page: int) -> tuple[list[Post], int, int]:
    """Clamp `page` into range and return (visible slice, page, total pages)."""
    pages = max(1, math.ceil(len(items) / PAGE_SIZE))
    page = max(1, min(page, pages))
    start = (page - 1) * PAGE_SIZE
    return items[start : start + PAGE_SIZE], page, pages


# --------------------------------------------------------------------------
# Views
# --------------------------------------------------------------------------


@app.route("/")
def index() -> str:
    """List posts newest first, optionally filtered by `?q=` and paged."""
    # The raw value is what we echo back to the user; the lowered copy is what
    # we search with. Keeping them separate means the search box still shows
    # exactly what was typed.
    raw_q = request.args.get("q", "").strip()
    needle = raw_q.lower()

    matches = newest_first()
    if needle:
        matches = [
            p
            for p in matches
            if needle in p.title.lower() or needle in p.body.lower()
        ]

    visible, page, pages = paginate(matches, request.args.get("page", 1, type=int))
    return render_template(
        "index.html",
        posts=visible,
        q=raw_q,
        total=len(matches),
        page=page,
        pages=pages,
    )


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    """Show one post in full. Unknown ids 404 via `find_post`."""
    return render_template("post.html", post=find_post(post_id))


@app.route("/tag/<tag>")
def show_tag(tag: str) -> str:
    """List every post carrying `tag`. 404 when nothing matches."""
    wanted = tag.strip().lower()
    matches = [p for p in newest_first() if wanted in p.tags]
    if not matches:
        abort(404)
    return render_template("tag.html", tag=wanted, posts=matches)


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str | tuple[str, int]:
    """Create-post form, gated behind the demo session login."""
    if not session.get("is_admin"):
        flash("Please log in to create posts.", "error")
        return redirect(url_for("login"))  # type: ignore[return-value]

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        raw_tags = request.form.get("tags", "")

        errors: list[str] = []
        if not title:
            errors.append("Title is required.")
        elif len(title) > TITLE_MAX:
            errors.append(f"Title must be {TITLE_MAX} characters or fewer.")
        if not body:
            errors.append("Body is required.")
        elif len(body) > BODY_MAX:
            errors.append(f"Body must be {BODY_MAX:,} characters or fewer.")

        if errors:
            for message in errors:
                flash(message, "error")
            # Re-render with what the user typed so the draft is not lost.
            return render_template(
                "new.html", title=title, body=body, tags=raw_tags
            )

        POSTS.append(
            Post(next(_id_seq), title=title, body=body, tags=parse_tags(raw_tags))
        )
        flash("Post published.", "success")
        return redirect(url_for("index"))  # type: ignore[return-value]

    return render_template("new.html", title="", body="", tags="")


@app.route("/weather")
def weather() -> str:
    """Thin wrapper around the Week 8 Open-Meteo logic."""
    city = request.args.get("city", "").strip()
    if not city:
        return render_template("weather.html", city="", current=None)

    try:
        current = get_current_weather(city)
    except WeatherError as exc:
        # A user-caused or network-caused failure is a flash, never a traceback.
        flash(str(exc), "error")
        return render_template("weather.html", city=city, current=None)

    return render_template("weather.html", city=city, current=current)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Demo-only password login. Read the security note in 00-overview.md."""
    if request.method == "POST":
        if request.form.get("password", "") == app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            flash("Logged in.", "success")
            return redirect(url_for("index"))  # type: ignore[return-value]
        flash("Wrong password.", "error")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout() -> str:
    """Drop the admin flag. POST-only so a stray link cannot log you out."""
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"))  # type: ignore[return-value]


@app.route("/api/posts")
def api_posts() -> list[dict[str, object]]:
    """Stretch goal: the Week 8 client's view of this site, from the server."""
    return [
        {
            "id": p.id,
            "title": p.title,
            "body": p.body,
            "tags": p.tags,
            "created_at": p.created_at.isoformat(timespec="seconds"),
        }
        for p in newest_first()
    ]


@app.route("/healthz")
def healthz() -> tuple[str, int]:
    """Stretch goal: a load balancer's idea of a friendly greeting."""
    return "OK", 200


@app.errorhandler(404)
def page_not_found(error: Exception) -> tuple[str, int]:
    """Homework problem 1: a 404 page that wears the site's own layout."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
