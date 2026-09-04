# Challenge 2 — Integration tests for the Week 9 Flask blog

> **Topic:** The app factory, the Flask test client, fixtures that build a fresh app per test, and integration testing a whole web app
> **Lecture:** [02 — Mocking, Coverage, and Debugging](../lecture-notes/02-mocking-coverage-and-debugging.md) · [Week 9 — Flask](../../week-09-web-development-flask/README.md)
> **Difficulty:** Advanced
> **Target time:** 3 hours
> **Why this one:** clicking around in a browser tests your app for one person, once. A test suite tests it for every person, on every push, forever. This is where the whole week comes together — fixtures, parametrize, the test client — on something the size of a real application, and where you learn the one refactor that makes any Flask app testable.

## The Brief

In Week 9 you built a small Flask blog: routes for listing, reading, and
creating posts. You tested it by clicking around. That does not scale.

Flask ships a **test client** — a fake browser that fires requests straight at
your views without starting a server and hands you back the response to assert
on. Combine it with pytest fixtures and you can build a fresh app plus a fresh
database for every single test, exercise every route, and tear it all down, in
well under a second.

But there is a catch, and it is the whole challenge. The Week 9 blog opened with
a single module-level `app = Flask(__name__)`. That one line is why it cannot be
tested: there is exactly one app, built the instant the module imports, and a
test cannot ask for a *different* one with a throwaway database. The first thing
you build this week is the seam that fixes it — an **app factory**, a function
`create_app(config)` that returns a freshly configured app. Everything else
follows from having that seam.

## Starter

Your real deliverable is a package, not one file:

```text
challenge-02-flask-blog-tests/
├── blog/
│   ├── __init__.py      # create_app — the factory
│   ├── db.py            # SQLite storage
│   ├── views.py         # the public routes
│   ├── auth.py          # the login gate
│   └── templates/       # base, index, post, new, login, about, 404
├── tests/
│   ├── conftest.py      # the fixtures
│   └── test_blog.py     # the required + stretch tests
└── pyproject.toml
```

Start `tests/conftest.py` with the two fixtures every other test leans on:

```python
"""conftest.py — shared fixtures for the Flask blog tests."""

import pytest
from flask import Flask

from blog import create_app


@pytest.fixture
def app() -> Flask:
    """A fresh app configured for tests: in-memory DB, TESTING on."""
    return create_app({"TESTING": True, "DATABASE": ":memory:", "SECRET_KEY": "test-secret"})


@pytest.fixture
def client(app: Flask):
    """A test client bound to that app."""
    return app.test_client()
```

If your Week 9 project has no `create_app` yet, **introduce one**: move the
module-level `app = Flask(__name__)` and its config into a function that takes a
config dict and returns the app. That single change is the biggest testability
win in the whole week.

## Requirements

Write at least these seven tests. The shipped answer writes eighteen.

1. **`GET /` returns 200** and the page renders.
2. **`GET /posts/<id>` returns 200** for a post that exists.
3. **`GET /posts/9999` returns 404** for one that does not.
4. **`POST /posts` creates a post** — assert the redirect (`302`) *and* that a
   later `GET /` shows the new title. Status alone would pass for a route that
   redirects and stores nothing.
5. **`POST /posts` with missing fields returns 400**, re-rendering the form.
6. **Delete removes the post** — via the form route `POST /posts/<id>/delete`
   *and* via `DELETE /posts/<id>`, because browsers only speak GET and POST.
7. **A protected route rejects anonymous callers** — `POST /posts/<id>/delete`
   without a session redirects to the login page.

Plus the three stretch tests: a `caplog` assertion that a 404 logs a warning, a
parametrized "these paths all return 200", and a fixture that seeds three posts.

## Constraints

- **One app per test, one database per app.** Every test must get its own app
  object and its own empty in-memory database, so no test can leak state into
  the next. `test_two_apps_do_not_share_a_database` writes that promise down as
  an assertion — it is the most valuable test in the suite, because if it ever
  fails, every other test is lying.
- **In-memory SQLite means one connection per *app*, not per request.** An
  in-memory database lives *inside* its connection. Open a new connection per
  request — the usual Flask pattern — and every request sees an empty database.
  Here, one long-lived connection per app is correct; a file-backed production
  deployment would use `g` + `teardown_appcontext` instead, and the `db`
  docstring must say so, so nobody copies the test pattern into production.
- **Keep views thin.** A view reads the request, calls one storage function,
  and renders a template. The only real logic — form validation — lives in a
  helper a unit test can call directly. That is the testing pyramid at file
  scope: unit-test the rules, and leave the test client to check the wiring,
  which is the only thing it is uniquely good at.
- **Assert on relative `Location` headers.** Werkzeug stopped making redirect
  `Location` headers absolute in 2.1. Assert `"/login" in location`, not
  `== "http://localhost/login"`, or use `follow_redirects=True`.

## Expected output

The shipped answer folds the whole app — factory, database, views, auth,
templates in a `DictLoader` — plus the fixtures and the test suite into one file
so it runs as a plain script. It runs the suite through pytest and reports:

```text
$ python challenge-02-flask-api-tests.py
Integration tests for the blog, each on its own app + in-memory database.

The tests, run the way pytest runs them:
  PASS  test_index_returns_200
  PASS  test_index_lists_seeded_posts
  PASS  test_show_post_returns_200_for_existing_post
  PASS  test_show_missing_post_returns_404
  PASS  test_unknown_url_returns_404
  PASS  test_create_post_redirects_and_shows_up_on_the_index
  PASS  test_create_post_rejects_incomplete_forms[no-title]
  PASS  test_create_post_rejects_incomplete_forms[no-body]
  PASS  test_create_post_rejects_incomplete_forms[empty]
  PASS  test_delete_via_form_route_removes_the_post
  PASS  test_delete_via_http_delete_removes_the_post
  PASS  test_delete_missing_post_returns_404
  PASS  test_delete_redirects_anonymous_callers_to_login
  PASS  test_two_apps_do_not_share_a_database
  PASS  test_404_logs_a_warning
  PASS  test_public_pages_return_200[/]
  PASS  test_public_pages_return_200[/about]
  PASS  test_public_pages_return_200[/posts/1]

18 passed, 0 failed
```

Doing it for real, you run `pytest -v` inside the package and read the same
names, one per line.

## Steps

1. Copy your Week 9 blog into a fresh folder. `pip install flask pytest pytest-cov`.
2. Introduce `create_app(config)` if you do not have it. Everything hinges on it.
3. Add `tests/conftest.py` with the `app` and `client` fixtures above.
4. Write `test_index_returns_200` first. Run `pytest`. Green.
5. Work down the seven requirements, one test at a time. When a test needs data,
   reach for a `seeded_app` fixture rather than inserting rows in the test body.
6. Add the login gate for requirement 7 — one password in config, one
   `session["is_admin"]` flag, one `login_required` decorator on the delete route
   only, so the other routes keep their Week 9 behaviour.
7. Add the three stretch tests. Run `pytest --cov=blog --cov-branch` and read
   what is left uncovered.

## The Solution

```python
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
```

**The app factory is the whole challenge.** `create_app(config)` builds a new
`Flask` object, loads defaults, overlays the caller's config, opens the
database, and registers the routes. Because it is a function, every test gets its
*own* app and its *own* empty database — which is what makes the suite
order-independent. `test_two_apps_do_not_share_a_database` proves it: write a
post into app one, ask app two for its posts, get an empty list.

**One connection per app is the genuinely open decision, and the reference takes
the unusual side.** The Flask-idiomatic pattern is a connection in `g`, opened
per request. Here that would be *actively wrong*: an in-memory database lives
inside its connection, so per-request connections would give every request an
empty database — `POST /posts` would 302, `GET /` would show nothing, and your
test would fail for reasons that have nothing to do with your views. `init_db`
opens one connection and stores it on `app.extensions`, and the `app` fixture
closes it in teardown. For a real file-backed deployment, switch to `g` +
`teardown_appcontext`; the docstring says exactly that.

**Thin views keep integration tests honest.** Every view reads the request,
calls one function in the storage layer, and renders. The only branching logic —
`_validate` — is pulled out where a unit test could call it directly, so the
test client is left doing the one thing it is uniquely good at: proving the
routes are wired together.

**The fixture graph makes "two apps in one test" impossible.** `seeded_app`
returns the *same* object as `app` (with three rows added), and `admin_client`
and `seeded_client` are both built from it. A test can depend on `seeded_app`
and `client` at once and still be talking to one app with one database. Two apps
in one test is the single most confusing Flask-test bug there is, and the graph
should make it impossible rather than merely unlikely.

**The assertion *inside* `admin_client` earns its keep.** `assert
response.status_code == 302, "fixture failed to log in"` turns a silent setup
failure into an error at setup, with a sentence explaining it — instead of a
mystery failure ten lines away in whatever test used the fixture.

**Requirement 6 is two routes for one view.** Browsers only speak GET and POST,
so the delete view is reachable at `DELETE /posts/<id>` (for API clients) and
`POST /posts/<id>/delete` (for an HTML form). Werkzeug routes on the method, so
`GET /posts/<id>` still lands on `show_post`. Both delete paths are tested.

## Run it

Copy the worked answer on this page into `challenge-02-flask-api-tests.py` and run it:

```bash
python challenge-02-flask-api-tests.py
```

It needs `flask` and `pytest` installed and opens no port and no network. Your
own deliverable is the `blog/` package plus `tests/` — the download folds them
into one file so the reference answer runs anywhere; the layout you hand in is
the folder the Starter section describes.

The `-solution` in the filename keeps this file from colliding with your own
work.

## Common bugs to catch

- **`RuntimeError: Working outside of application context.`** You called a `db`
  function in plain test code without pushing a context. During a
  `client.get(...)` Flask pushes one for you; in bare test code you push it
  yourself with `with app.app_context():`. Every reference test that calls `db.*`
  directly does exactly that.
- **Two apps in one test.** You asked for `seeded_app` but built your own client
  from a fresh `create_app()`, so you are querying an *empty* database while the
  seeded one sits untouched. The failure is confusing precisely because both
  objects look right. This is why `seeded_app` returns the same object as `app`.
- **`assert location == "http://localhost/login"` fails with `/login`.** Werkzeug
  2.1 stopped making `Location` headers absolute. Assert the relative path, or
  follow the redirect and assert on the page you land on.
- **The suite passes with `-k one_test` and fails with the full run.** Your `app`
  fixture is `scope="session"`, or your `DATABASE` is a file, so a delete in one
  test changes what the next test sees. Function scope, `:memory:`, and closing
  the connection in teardown are what make the suite order-independent.
- **Asserting only the status code on a create.** `assert status == 302` passes
  for a route that redirects and stores nothing. Requirement 4 asks you to follow
  up with a `GET /` for exactly this reason.

## Under the hood

<details>
<summary>Under the hood — the fixture graph, and what a grader is really checking</summary>

The fixtures fan out from one app object:

```text
app  ->  client
 |
 +----->  seeded_app  ->  seeded_client
 |                    ->  admin_client
```

`seeded_app` depending on `app` — rather than building its own — is what
guarantees a test can hold both and still see one database.

The rubric awards points for artifacts, but a human reading your work asks three
questions the rubric cannot:

1. **Did the app change, or only the tests?** Green tests without a factory means
   you kept a module-level `app` and your tests share state. Look for
   `create_app` and a `:memory:` database.
2. **Would a broken view actually turn a test red?** Comment out the `abort(404)`
   in `show_post` and rerun. If nothing fails, requirement 3 is untested no
   matter what the coverage report says.
3. **Does the suite pass in a different order?** Run the test modules in one
   order, then the reverse. Order dependence is the defect coverage cannot see.

Eight solid, independent tests plus an honest note about the two you could not
make work is worth more than eighteen that pass because they never really ran
the code.

</details>

## Acceptance checklist

- [ ] `create_app(config)` exists; each test gets its own app and `:memory:` DB.
- [ ] All seven required behaviours have a passing test.
- [ ] Delete is tested via both `POST /posts/<id>/delete` and `DELETE /posts/<id>`.
- [ ] An anonymous delete redirects to the login page.
- [ ] `test_two_apps_do_not_share_a_database` passes.
- [ ] The suite passes run in a different order (it is order-independent).
- [ ] `README.md` says what you changed in the Week 9 code to make it testable.

## Stretch

- Add `pytest --cov=blog --cov-branch --cov-fail-under=80`. The reference reaches
  100 % on every module, because the views are thin enough that there is nowhere
  for an untested line to hide — which is itself the argument for thin views.
- Write a `.github/workflows/ci.yml` that runs the suite on Python 3.11 and 3.12,
  with `concurrency: cancel-in-progress` so a re-push cancels the previous run.
- Add a `test_rejected_form_keeps_what_you_typed` test that submits a too-long
  title and asserts the typed body is still in the re-rendered form, so a future
  "simplification" cannot throw the draft away.

You have now tested a whole application end to end. Take the quiz, then build the
week's [mini-project](../mini-project/README.md) — a package tested to 100 %.
