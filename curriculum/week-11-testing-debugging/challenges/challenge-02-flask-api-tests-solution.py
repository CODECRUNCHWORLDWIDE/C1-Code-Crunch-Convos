"""challenge-02-flask-api-tests-solution.py — integration tests for a Flask blog.

The Week 9 blog opened with a module-level ``app = Flask(__name__)``, which is
the one line that makes it untestable: there is exactly one app, built the
moment the module imports, so a test cannot ask for a *different* app with a
throwaway database. The fix is an **app factory** — ``create_app(config)`` — and
almost everything else in this challenge follows from it.

Your real deliverable is a folder: ``blog/`` (the factory, db, views, auth,
templates) and ``tests/`` (conftest fixtures and the test modules). A published
answer is run as a plain script, so this one file folds all of that together —
templates in a ``DictLoader``, an in-memory SQLite database, and the test suite
— and a ``main()`` drives pytest itself and prints a plain, same-every-time
report.

Run it with::

    python challenge-02-flask-api-tests-solution.py
"""

from __future__ import annotations

import contextlib
import io
import logging
import sqlite3
from collections.abc import Iterator
from functools import wraps
from typing import Any, Callable, Mapping

import pytest
from flask import (
    Flask,
    Response,
    abort,
    current_app,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from jinja2 import DictLoader
from werkzeug.wrappers import Response as WerkzeugResponse

log = logging.getLogger("blog")

# --------------------------------------------------------------------------- #
# Templates — templates/*.html in your build, constants in this download
# --------------------------------------------------------------------------- #

TEMPLATES: dict[str, str] = {
    "base.html": """\
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>{% block title %}Crunch Blog{% endblock %}</title></head>
  <body>
    <header><h1><a href="{{ url_for('views.index') }}">Crunch Blog</a></h1></header>
    <main>{% block content %}{% endblock %}</main>
    <footer><small>Built with Flask. Tested with pytest.</small></footer>
  </body>
</html>
""",
    "index.html": """\
{% extends "base.html" %}
{% block content %}
  <h2>Posts</h2>
  {% for post in posts %}
    <article><a href="{{ url_for('views.show_post', post_id=post['id']) }}">{{ post['title'] }}</a></article>
  {% else %}
    <p class="empty">No posts yet. <a href="{{ url_for('views.new_post') }}">Write the first one.</a></p>
  {% endfor %}
{% endblock %}
""",
    "post.html": """\
{% extends "base.html" %}
{% block title %}{{ post['title'] }} — Crunch Blog{% endblock %}
{% block content %}<article><h2>{{ post['title'] }}</h2><p>{{ post['body'] }}</p></article>{% endblock %}
""",
    "new.html": """\
{% extends "base.html" %}
{% block content %}
  <h2>New post</h2>
  {% if error %}<p class="error">{{ error }}</p>{% endif %}
  <form method="post" action="{{ url_for('views.create_post') }}">
    <input name="title" value="{{ title }}">
    <textarea name="body">{{ body }}</textarea>
    <button type="submit">Publish</button>
  </form>
{% endblock %}
""",
    "about.html": """\
{% extends "base.html" %}
{% block content %}<h2>About</h2><p>A tiny blog that exists to be tested.</p>{% endblock %}
""",
    "login.html": """\
{% extends "base.html" %}
{% block content %}
  <h2>Log in</h2>
  {% if error %}<p class="error">{{ error }}</p>{% endif %}
  <form method="post" action="{{ url_for('auth.login') }}">
    <input name="password" type="password">
    <button type="submit">Log in</button>
  </form>
{% endblock %}
""",
    "404.html": """\
{% extends "base.html" %}
{% block content %}<h2>404 — nothing here</h2><p><a href="{{ url_for('views.index') }}">Back home</a></p>{% endblock %}
""",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body  TEXT NOT NULL
);
"""

DEFAULT_CONFIG: dict[str, Any] = {
    "DATABASE": ":memory:",
    "SECRET_KEY": "dev-only-not-a-real-secret",
    "ADMIN_PASSWORD": "correct horse",
    "TESTING": False,
}

TITLE_MAX = 120
BODY_MAX = 10_000

# --------------------------------------------------------------------------- #
# blog/db.py — one connection per application, deliberately
# --------------------------------------------------------------------------- #


def init_db(app: Flask) -> None:
    """Open the single long-lived connection this app will use, and build it.

    An in-memory SQLite database lives *inside* its connection, so opening a new
    connection per request would hand every request an empty database. One
    connection per app is simpler and correct for a test client; a file-backed
    production deployment would use ``g`` + ``teardown_appcontext`` instead.
    """
    connection = sqlite3.connect(app.config["DATABASE"], check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    connection.commit()
    app.extensions["blog_db"] = connection


def get_db() -> sqlite3.Connection:
    """The current app's connection. Needs an application context to resolve."""
    return current_app.extensions["blog_db"]


def list_posts() -> list[sqlite3.Row]:
    """Every post, newest id first."""
    return get_db().execute("SELECT * FROM posts ORDER BY id DESC").fetchall()


def get_post(post_id: int) -> sqlite3.Row | None:
    """One post by id, or None."""
    return get_db().execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()


def add_post(title: str, body: str) -> int:
    """Insert a post and return its new id."""
    db = get_db()
    cursor = db.execute("INSERT INTO posts (title, body) VALUES (?, ?)", (title, body))
    db.commit()
    return int(cursor.lastrowid)


def delete_post(post_id: int) -> int:
    """Delete a post, returning how many rows went (0 if it did not exist)."""
    db = get_db()
    cursor = db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return cursor.rowcount


# --------------------------------------------------------------------------- #
# blog/auth.py — the smallest credible login gate
# --------------------------------------------------------------------------- #


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    """Send anonymous callers to the login page instead of running the view."""

    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if not session.get("is_admin"):
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def _validate(title: str, body: str) -> str | None:
    """Return an error message for a bad post, or None if it is fine."""
    if not title or not body:
        return "Title and body are both required."
    if len(title) > TITLE_MAX:
        return f"Title must be {TITLE_MAX} characters or fewer."
    if len(body) > BODY_MAX:
        return f"Body must be {BODY_MAX} characters or fewer."
    return None


# --------------------------------------------------------------------------- #
# The app factory — one app, one database, per caller
# --------------------------------------------------------------------------- #


def create_app(config: Mapping[str, Any] | None = None) -> Flask:
    """Build and return a configured blog app. This is the whole challenge."""
    app = Flask(__name__)
    app.jinja_loader = DictLoader(TEMPLATES)
    app.config.from_mapping(DEFAULT_CONFIG)
    if config is not None:
        app.config.from_mapping(config)

    init_db(app)

    from flask import Blueprint

    views = Blueprint("views", __name__)
    auth = Blueprint("auth", __name__)

    @views.route("/")
    def index() -> str:
        return render_template("index.html", posts=list_posts())

    @views.route("/about")
    def about() -> str:
        return render_template("about.html")

    @views.route("/posts/<int:post_id>")
    def show_post(post_id: int) -> str:
        post = get_post(post_id)
        if post is None:
            abort(404)
        return render_template("post.html", post=post)

    @views.route("/new")
    def new_post() -> str:
        return render_template("new.html", title="", body="", error=None)

    @views.route("/posts", methods=["POST"])
    def create_post() -> Any:
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        error = _validate(title, body)
        if error is not None:
            return render_template("new.html", title=title, body=body, error=error), 400
        add_post(title, body)
        return redirect(url_for("views.index"))

    @views.route("/posts/<int:post_id>", methods=["DELETE"])
    @views.route("/posts/<int:post_id>/delete", methods=["POST"])
    @login_required
    def remove_post(post_id: int) -> WerkzeugResponse:
        if delete_post(post_id) == 0:
            abort(404)
        return redirect(url_for("views.index"))

    @auth.route("/login", methods=["GET", "POST"])
    def login() -> Any:
        if request.method == "POST":
            if request.form.get("password") == current_app.config["ADMIN_PASSWORD"]:
                session["is_admin"] = True
                return redirect(url_for("views.index"))
            return render_template("login.html", error="Wrong password."), 401
        return render_template("login.html", error=None)

    @auth.route("/logout", methods=["POST"])
    def logout() -> WerkzeugResponse:
        session.clear()
        return redirect(url_for("views.index"))

    def page_not_found(error: Exception) -> tuple[str, int]:
        log.warning("404 Not Found: %s", request.path)
        return render_template("404.html"), 404

    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_error_handler(404, page_not_found)
    return app


# --------------------------------------------------------------------------- #
# tests/conftest.py — six fixtures, one app object per test
# --------------------------------------------------------------------------- #

TEST_CONFIG = {"TESTING": True, "DATABASE": ":memory:", "SECRET_KEY": "test-secret"}


@pytest.fixture
def app() -> Iterator[Flask]:
    """A fresh app with an empty in-memory database, closed on teardown."""
    flask_app = create_app(TEST_CONFIG)
    yield flask_app
    flask_app.extensions["blog_db"].close()


@pytest.fixture
def client(app: Flask) -> Any:
    """A test client bound to the fresh app."""
    return app.test_client()


@pytest.fixture
def seeded_app(app: Flask) -> Flask:
    """The SAME app, with three posts inserted. Newest id is 3."""
    with app.app_context():
        for number in (1, 2, 3):
            add_post(f"Seed post {number}", f"Body of seed post {number}.")
    return app


@pytest.fixture
def seeded_client(seeded_app: Flask) -> Any:
    """A client bound to the seeded app."""
    return seeded_app.test_client()


@pytest.fixture
def admin_client(seeded_app: Flask) -> Any:
    """A logged-in client. The cookie jar keeps the session across calls."""
    client = seeded_app.test_client()
    response = client.post("/login", data={"password": "correct horse"})
    assert response.status_code == 302, "fixture failed to log in"
    return client


# --------------------------------------------------------------------------- #
# tests/test_blog.py + test_auth.py — the required tests and three stretch tests
# --------------------------------------------------------------------------- #


def test_index_returns_200(client: Any) -> None:
    assert client.get("/").status_code == 200


def test_index_lists_seeded_posts(seeded_client: Any) -> None:
    assert b"Seed post 3" in seeded_client.get("/").data


def test_show_post_returns_200_for_existing_post(seeded_client: Any) -> None:
    assert seeded_client.get("/posts/1").status_code == 200


def test_show_missing_post_returns_404(client: Any) -> None:
    assert client.get("/posts/9999").status_code == 404


def test_unknown_url_returns_404(client: Any) -> None:
    assert client.get("/no/such/page").status_code == 404


def test_create_post_redirects_and_shows_up_on_the_index(client: Any) -> None:
    response = client.post("/posts", data={"title": "Hello", "body": "First post."})
    assert response.status_code == 302
    assert b"Hello" in client.get("/").data


@pytest.mark.parametrize(
    "form",
    [{"title": "", "body": "no title"}, {"title": "no body", "body": ""}, {}],
    ids=["no-title", "no-body", "empty"],
)
def test_create_post_rejects_incomplete_forms(client: Any, form: dict[str, str]) -> None:
    assert client.post("/posts", data=form).status_code == 400


def test_delete_via_form_route_removes_the_post(admin_client: Any) -> None:
    assert admin_client.post("/posts/2/delete").status_code == 302
    assert admin_client.get("/posts/2").status_code == 404


def test_delete_via_http_delete_removes_the_post(admin_client: Any) -> None:
    assert admin_client.delete("/posts/3").status_code == 302
    assert admin_client.get("/posts/3").status_code == 404


def test_delete_missing_post_returns_404(admin_client: Any) -> None:
    assert admin_client.post("/posts/9999/delete").status_code == 404


def test_delete_redirects_anonymous_callers_to_login(seeded_client: Any) -> None:
    response = seeded_client.post("/posts/1/delete")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_two_apps_do_not_share_a_database() -> None:
    one, two = create_app(TEST_CONFIG), create_app(TEST_CONFIG)
    with one.app_context():
        add_post("only in app one", "body")
    with two.app_context():
        assert list_posts() == []
    one.extensions["blog_db"].close()
    two.extensions["blog_db"].close()


def test_404_logs_a_warning(client: Any, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING", logger="blog"):
        client.get("/posts/9999")
    assert any("404 Not Found: /posts/9999" in record.message for record in caplog.records)


@pytest.mark.parametrize("path", ["/", "/about", "/posts/1"])
def test_public_pages_return_200(seeded_client: Any, path: str) -> None:
    assert seeded_client.get(path).status_code == 200


# --------------------------------------------------------------------------- #
# The driver — run the suite the way pytest would, and report deterministically
# --------------------------------------------------------------------------- #


class _Collector:
    """A pytest plugin that records each test's name and outcome, in order."""

    def __init__(self) -> None:
        self.results: list[tuple[str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.results.append((report.nodeid.split("::")[-1], report.outcome))


def run_suite() -> list[tuple[str, str]]:
    """Run this file's own tests through pytest and hand back the outcomes."""
    collector = _Collector()
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        pytest.main([__file__, "-p", "no:cacheprovider", "-q"], plugins=[collector])
    return collector.results


def main() -> None:
    """Run the integration suite against the factory and print the outcomes."""
    print("Integration tests for the blog, each on its own app + in-memory database.")
    print()
    print("The tests, run the way pytest runs them:")
    results = run_suite()
    for name, outcome in results:
        print(f"  {'PASS' if outcome == 'passed' else 'FAIL'}  {name}")

    passed = sum(1 for _, outcome in results if outcome == "passed")
    failed = len(results) - passed
    print()
    print(f"{passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
