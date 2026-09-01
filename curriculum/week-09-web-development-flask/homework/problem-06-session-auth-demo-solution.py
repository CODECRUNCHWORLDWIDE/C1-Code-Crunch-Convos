"""problem-06-session-auth-demo-solution.py — session auth. DEMO ONLY.

DO NOT DEPLOY THIS. It is a demonstration of how a Flask session works, not
authentication. The password is a plaintext constant compared with ``==``,
there is no hashing, no CSRF token, no rate limiting, and no user model.
Every one of those absences is a real vulnerability; the homework's stretch
section names them one by one. What this file is FOR is the mechanism: a
signed cookie carrying ``is_admin``, a guard at the top of a view, and a
POST-only logout.

Both secrets read from the environment with an obviously fake dev fallback,
so the file runs out of the box and a real deployment overrides both.

Templates travel inside the file via a ``DictLoader``; the app is driven by
``app.test_client()`` — Flask's in-process fake browser, cookie jar included
— instead of ``app.run()``. The harness ends by splitting the session cookie
at its dots and base64-decoding the payload, so you can see with your own
eyes that a session is signed, not encrypted.

Run it with::

    python problem-06-session-auth-demo-solution.py
"""

import base64
import os

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
from jinja2 import DictLoader

#: templates/base.html — the nav branches on session.get('is_admin'), which
#: Flask injects into every template context. No view passes it in.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1>
      <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('new_post') }}">New post</a>
        {% if session.get('is_admin') %}
          <form class="inline" method="post" action="{{ url_for('logout') }}">
            <button type="submit" class="linklike">Log out</button>
          </form>
        {% else %}
          <a href="{{ url_for('login') }}">Log in</a>
        {% endif %}
      </nav>
    </header>
    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flashes">
            {% for category, message in messages %}
              <li class="flash flash-{{ category }}">{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
"""

INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>
  <p>The posts are not the point this time. Look at the nav.</p>
{% endblock %}
"""

#: templates/login.html — the warning sits where a reader will actually see it.
LOGIN_HTML: str = """\
{% extends "base.html" %}

{% block title %}Log in — Crunch Blog{% endblock %}

{% block content %}
  <h2>Log in</h2>
  <p class="warning">
    Demo authentication only. The password is a constant in the source and
    there is no CSRF protection, no rate limiting, and no password hashing.
    Never ship this pattern.
  </p>
  <form method="post" action="{{ url_for('login') }}">
    <label for="password">Password</label>
    <input type="password" id="password" name="password" required autofocus>
    <button type="submit">Log in</button>
  </form>
{% endblock %}
"""

NEW_HTML: str = """\
{% extends "base.html" %}

{% block title %}New post — Crunch Blog{% endblock %}

{% block content %}
  <h2>New post</h2>
  <p>Only a logged-in admin ever sees this form.</p>
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {
        "base.html": BASE_HTML,
        "index.html": INDEX_HTML,
        "login.html": LOGIN_HTML,
        "new.html": NEW_HTML,
    }
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

# Hardcoded-password auth is a DEMO of how sessions work, not a way to
# protect anything. The env var keeps even the demo value out of production.
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "letmein")


@app.route("/")
def index() -> str:
    """The blog index. Its nav flips with the session."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """Demo-only password login."""
    if request.method == "POST":
        if request.form.get("password", "") == app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            flash("Logged in.", "success")
            return redirect(url_for("index"))
        flash("Wrong password.", "error")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout() -> Response:
    """Drop the admin flag. POST-only so a stray link cannot log you out."""
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"))


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str | Response:
    """The gated route. The guard comes first, above the method branch."""
    if not session.get("is_admin"):
        flash("Please log in to create posts.", "error")
        return redirect(url_for("login"))
    return render_template("new.html")


def nav_shows(page: str) -> str:
    """Which auth control the nav is currently rendering."""
    return "Log out" if "Log out" in page else "Log in"


def decode_session_payload(cookie_value: str) -> str:
    """Base64-decode the payload third of a Flask session cookie.

    The cookie is `payload.timestamp.signature`. The payload is plain
    urlsafe-base64 JSON — readable by anyone holding the cookie. Only the
    signature, computed from SECRET_KEY, stops them changing it.
    """
    payload = cookie_value.split(".")[0]
    payload += "=" * (-len(payload) % 4)  # restore the padding base64 wants
    return base64.urlsafe_b64decode(payload).decode("utf-8")


def main() -> None:
    """Walk the whole flow, then open the cookie and read it."""
    print("DEMO ONLY — this shows how sessions work, not how to build auth.")
    print()

    client = app.test_client()

    response = client.get("/new")
    print(f"GET  /new (logged out)         -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/login").get_data(as_text=True)
    print(f"  flash on the login page: {'Please log in to create posts.' in body}")
    print(f"  nav shows: {nav_shows(body)}")

    print()
    response = client.post("/login", data={"password": "wrong"})
    body = response.get_data(as_text=True)
    print(f"POST /login password='wrong'   -> {response.status_code} (re-rendered)")
    print(f"  flash: {'Wrong password.' in body}")

    print()
    response = client.post("/login", data={"password": "letmein"})
    print(f"POST /login password='letmein' -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/").get_data(as_text=True)
    with client.session_transaction() as sess:
        print(f"  session['is_admin'] is now : {sess.get('is_admin')}")
    print(f"  nav shows: {nav_shows(body)}")
    print(f"  GET /new -> {client.get('/new').status_code} (the guard lets an admin through)")

    print()
    print("The session cookie itself, split at its dots:")
    cookie = client.get_cookie("session")
    assert cookie is not None
    print(f"  payload, base64-decoded: {decode_session_payload(cookie.value)}")
    print("  signed, not encrypted: anyone can READ it; only the key can CHANGE it.")

    print()
    response = client.post("/logout")
    print(f"POST /logout                   -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/").get_data(as_text=True)
    with client.session_transaction() as sess:
        print(f"  session['is_admin'] is now : {sess.get('is_admin')}")
    print(f"  nav shows: {nav_shows(body)}")


if __name__ == "__main__":
    main()
