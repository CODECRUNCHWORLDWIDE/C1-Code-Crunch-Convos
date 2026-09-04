# Homework Problem 6 — Session auth (demo only)

> **Topic:** `session` as a signed cookie, a password gate in front of one route, and a nav that knows who you are
> **Lecture:** [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** every app you will ever write has to remember, on page two, something it learned on page one. Flask does that with one dictionary called `session`, and this problem is the smallest honest use of it. It is also the first time the course asks you to build something and then refuses to let you ship it — which is the more important lesson of the two.

## The Brief

> **Security warning — read this before you write a line.**
> This problem demonstrates **how a Flask session works**, NOT how to build
> real authentication. The password is hardcoded in the source file. Real
> apps store *hashed* passwords in a database and defend against timing
> attacks, brute force, and CSRF, none of which exist here.
> **Do not deploy this auth pattern anywhere real.** It is a working model
> of a lock the way a cardboard model of a car is a working model of a car.

Think about a wristband at a fair. You pay once at the gate, and someone snaps
a paper band on your wrist. After that you do not carry your receipt from ride
to ride. The ride operator glances at your wrist and waves you through. The
band is tamper-proof: anyone can *read* what is printed on it, but the little
seal means you cannot fake one at home.

A Flask **session** is that wristband. It is a dictionary you write to on one
page and read on the next, and Flask keeps it in a cookie in the visitor's
browser. The cookie is *signed* with your `SECRET_KEY` — the seal. Anyone
holding the cookie can read what is in it. Nobody without the key can change
it without Flask noticing. The shipped file below cracks its own cookie open
at the end and prints the contents, so you can see both halves of that
sentence with your own eyes.

Your job: put a lock on the `/new` (create-post) route of your blog. A visitor
who is not logged in gets bounced to a login page with a message. A visitor who
types the right password gets a wristband — `session["is_admin"] = True` — and
sails through. A "Log out" button takes the band off.

The password is one hardcoded string. That is the part you must never repeat
outside this exercise, and the reason is spelled out again under *Constraints*.

## Starter

Save this as `problem-06-session-auth-demo.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted, and it prints the bug: `/new` answers `200` to a
complete stranger.

```python
"""problem-06-session-auth-demo.py — starter: the blog with no lock on the door.

Run with: python problem-06-session-auth-demo.py
"""

import os

from flask import Flask, render_template
from jinja2 import DictLoader

# TODO 1: read ADMIN_PASSWORD out of the environment into app.config,
#         with "letmein" as the fallback so the file still runs.
# TODO 2: write LOGIN_HTML — extends base.html, one password field, and the
#         demo-only warning as visible text — and register it in the
#         DictLoader as "login.html". Then add a GET/POST /login route: GET
#         renders it, POST compares request.form["password"] with the config
#         value. On a match set session["is_admin"] = True, flash success and
#         redirect to index; otherwise flash an error and re-render the form.
# TODO 3: add a POST-only /logout route that pops "is_admin" and redirects.
# TODO 4: guard /new — first lines of the view, before anything else.
# TODO 5: branch the nav in BASE_HTML on session.get('is_admin') so it shows
#         a "Log out" button when logged in and a "Log in" link when not.

BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1>
      <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('new_post') }}">New post</a>
      </nav>
    </header>
    <main>
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

NEW_HTML: str = """\
{% extends "base.html" %}

{% block title %}New post — Crunch Blog{% endblock %}

{% block content %}
  <h2>New post</h2>
  <p>Right now ANYONE can read this page. That is the bug.</p>
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {"base.html": BASE_HTML, "index.html": INDEX_HTML, "new.html": NEW_HTML}
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str:
    # TODO 4: the guard goes here, above everything else in the view.
    return render_template("new.html")


def main() -> None:
    client = app.test_client()
    print(f"GET /new (nobody logged in) -> {client.get('/new').status_code}")
    print("  ...and it should have been a 302 to /login.")


if __name__ == "__main__":
    main()
```

In your own blog this is the same work spread across real files: the nav
branch lands in `templates/base.html`, a new `templates/login.html` appears,
and three routes join `app.py`.

## Requirements

1. `app.config["ADMIN_PASSWORD"]` is read with
   `os.environ.get("ADMIN_PASSWORD", "letmein")`, so a real environment can
   override the demo value without editing the file.
2. `GET /login` shows a form with a single `password` field.
   `POST /login` compares `request.form["password"]` with
   `app.config["ADMIN_PASSWORD"]`. On a match it sets
   `session["is_admin"] = True` and redirects to `/`. On a miss it flashes an
   error and shows the form again.
3. `POST /logout` pops `is_admin` out of the session and redirects.
4. `/new` is guarded. At the very top of the view:
   ```python
   if not session.get("is_admin"):
       flash("Please log in to create posts.", "error")
       return redirect(url_for("login"))
   ```
5. The nav shows a "Log in" link or a "Log out" control depending on
   `session.get("is_admin")` — and no view function passes that value in.

## Constraints

- **The password lives in one place, and that place is the config.** Not
  scattered through three views. When the value moves — and in a real app it
  moves into a database on day one — you want exactly one line to change.

- **Never compare a real password with `==`.** This file does, because it is a
  demo of sessions, not of passwords. `==` on strings stops at the first
  character that differs, so a patient attacker can time the comparison and
  learn the password one letter at a time. Real code stores a *hash* — a
  scrambled fingerprint of the password that cannot be un-scrambled — and
  compares hashes with a function built to take the same time every call.
  Werkzeug ships `generate_password_hash` and `check_password_hash` for
  exactly this, and they are one import away.

- **Logout is `POST`-only.** If logging out were an ordinary link, anything
  that quietly fetches URLs — a browser prefetcher, an image tag on someone
  else's page, a crawler — could log your visitors out. `GET` is supposed to
  mean "just show me"; anything that *changes* something is a `POST`. So the
  nav control is a tiny one-button `<form method="post">`, not an `<a>`.

- **The guard is the first thing in the view, above the method branch.** Put
  it inside `if request.method == "POST"` and `GET /new` walks straight past
  it. Deny first, then work.

- **Nothing secret goes in the session.** The cookie is *signed*, not
  *encrypted*: the signature stops people changing it, but the contents are
  plain readable text to anyone holding the cookie. `is_admin` is a flag, and
  a flag is fine. An API key is not.

- **`SECRET_KEY` comes from the environment.** A key committed to a repo is a
  key everyone has, and anyone with the key can forge a wristband that says
  `is_admin`. The dev fallback here is named `dev-only-not-a-real-secret` so
  that it is obvious in a log when the real one was never set.

- **No hardcoded `href="/login"`.** `url_for('login')` re-derives the URL from
  the route table every time it renders, so it stays right the day the route
  moves.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-06-session-auth-demo.py
DEMO ONLY — this shows how sessions work, not how to build auth.

GET  /new (logged out)         -> 302  Location: /login
  flash on the login page: True
  nav shows: Log in

POST /login password='wrong'   -> 200 (re-rendered)
  flash: True

POST /login password='letmein' -> 302  Location: /
  session['is_admin'] is now : True
  nav shows: Log out
  GET /new -> 200 (the guard lets an admin through)

The session cookie itself, split at its dots:
  payload, base64-decoded: {"is_admin":true}
  signed, not encrypted: anyone can READ it; only the key can CHANGE it.

POST /logout                   -> 302  Location: /
  session['is_admin'] is now : None
  nav shows: Log in
```

The block about the cookie is the one to stare at. The wristband's printing is
right there in plain text, readable by anyone who has the cookie. Only the
seal is hard to fake.

## Steps

1. Add the config line and confirm the app still starts.
2. Write `login.html`: a heading, the demo-only warning as visible text on the
   page, and a form with one `password` field posting to `url_for('login')`.
3. Write the `/login` view. Do the `GET` half first — load the page and look
   at it before any logic exists.
4. Add the `POST` half. Try a wrong password first and confirm you get the
   form back with a flash, not a crash.
5. Log in with the right password. Then print the session inside the view, or
   use `client.session_transaction()`, and confirm `is_admin` is really there.
6. Add the guard to `/new`. Log out, hit `/new`, and confirm the redirect and
   the flash.
7. Add the `/logout` route as `POST`-only, and the one-button form in the nav.
8. Branch the nav on `session.get('is_admin')`. Reload while logged in and
   while logged out and watch it flip. No view passes `is_admin` in — Flask
   puts `session` into every template context by itself.
9. Open your browser's developer tools, find the `session` cookie, and read
   it. Then change one character of it by hand, reload, and watch Flask throw
   the whole session away.

## The Solution

```python
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
```

**The session is a dictionary that survives the trip home.**
`session["is_admin"] = True` in the login view; `session.get("is_admin")` in
the `/new` view, on a completely separate request, minutes later. In between,
Flask turned that dictionary into JSON, signed it with `SECRET_KEY`, and sent
it to the browser as a cookie; the browser sent it back on the next request,
and Flask checked the signature before handing it to you. The whole round trip
is invisible, which is exactly why it is worth taking apart once.

**Signed is not encrypted, and the demo proves it.** `decode_session_payload`
splits the cookie at its dots and base64-decodes the first third. Out comes
`{"is_admin":true}` in plain text. Base64 is not a lock — it is a way of
writing bytes using only the characters a cookie is allowed to contain, and
undoing it needs no key. What the key protects is *change*: edit one byte and
the signature no longer matches, so Flask discards the session and treats you
as a stranger. Read: anyone. Write: only the key.

**The guard runs before the work.** In `new_post`, the
`if not session.get("is_admin")` block is the first thing in the function,
above any `request.method` branch. Every path into that view passes through
it. A guard you have to remember to reach is not a guard.

**`session.get("is_admin")` never raises, and `session.pop("is_admin", None)`
never raises either.** A visitor who has never logged in has no such key.
`.get` answers `None`, which is falsy, which sends them to the login page —
the right behaviour with no special case. `.pop` with a default lets logout be
harmless when it happens twice.

**The nav is not handed the answer; it looks it up.** Flask injects `session`
into every template context, so `{% if session.get('is_admin') %}` works in
`base.html` without a single view function mentioning it. That is what makes
requirement 5 one edit in one file, instead of a keyword argument added to
every `render_template` call in the app.

**Logout is a form, not a link.** The nav renders a one-button
`<form method="post" action="{{ url_for('logout') }}">`. `GET` is for reading
and `POST` is for changing, and a browser will happily fetch a `GET` on its
own — prefetching a link, loading an image, following a crawler's nose. A
logout hiding behind a `GET` gets triggered by accident.

**Both secrets read from the environment, with an obviously fake fallback.**
`os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")` runs out of the
box and gives itself away in a log if it was never overridden. The
alternative — a real key typed into the file — is a key in your git history
forever.

**And it is still not authentication.** One shared password, in the source,
compared with `==`, with no account, no hash, no lockout, and no CSRF token.
The mechanism above is real and reusable. The lock is a prop.

## Run it

Copy the worked answer on this page into `problem-06-session-auth-demo.py` and run it:

```bash
python problem-06-session-auth-demo.py
```

It needs Flask installed and nothing else. There is no `app.run()` and no
browser: the file drives itself with `app.test_client()`, Flask's in-process
fake browser, which keeps a cookie jar exactly like a real one. It exits on
its own.

The `-solution` in the filename keeps this file from colliding with your own
`problem-06-session-auth-demo.py`.

## Common bugs to catch

- **`RuntimeError: The session is unavailable because no secret key was set.`**
  You touched `session` before setting `app.secret_key`. Flask cannot sign a
  cookie without a key, so it refuses rather than shipping an unsigned one.
  Set `app.secret_key` right after you create the app.

- **`GET /new` still returns `200` when logged out.** The guard is inside
  `if request.method == "POST"`. Move it to the top of the view, above every
  branch.

- **`KeyError: 'is_admin'` on logout.** `session.pop("is_admin")` with no
  default explodes when the key is not there — logging out twice, or a
  visitor who never logged in. Pass the default:
  `session.pop("is_admin", None)`.

- **`werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: KeyError: 'password'`
  on login.** `request.form["password"]` when the form did not send that
  field — usually a missing `name="password"` on the `<input>`, or a form
  that submitted by `GET`. Use `request.form.get("password", "")` and fix the
  `name`.

- **`405 Method Not Allowed` on logout.** The route is `methods=["POST"]` but
  something sent a `GET` — an `<a href>` in the nav instead of a one-button
  form. Keep the route `POST`-only and fix the nav.

- **`werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'login'.`**
  The template calls `url_for('login')` before a view function named `login`
  exists. `url_for` takes the *function name*, not the URL path.

- **The nav never flips, even though login clearly worked.** Either the
  template is checking a variable the view forgot to pass — use
  `session.get('is_admin')`, which is always available — or your client is
  throwing the cookie away. In `test_client()` a *new* client is a new browser
  with an empty cookie jar; reuse the same one across requests.

- **Everyone is logged out after every restart.** Your `SECRET_KEY` is being
  regenerated at startup — `os.urandom(...)` assigned directly, say — so every
  old cookie fails its signature check. Read it from the environment and keep
  it stable.

## Under the hood

<details>
<summary>Under the hood — what the three dots in a session cookie actually are</summary>

Flask signs cookies with **itsdangerous**. The cookie value is three parts
joined by dots:

```text
eyJpc19hZG1pbiI6dHJ1ZX0.aK1z9g.tR3q...   ->   payload . timestamp . signature
```

- **payload** — your session dictionary, JSON-encoded, then urlsafe-base64'd.
  Base64 is a character-set trick, not a cipher; the demo's
  `decode_session_payload` undoes it in three lines.
- **timestamp** — when it was issued, so an expiry can be enforced.
- **signature** — an HMAC-SHA1 of the first two parts, keyed with
  `SECRET_KEY`.

On the way back in, Flask recomputes the signature from the payload and the
key and compares it, in constant time, with the one in the cookie. A mismatch
means the session is silently dropped and the request runs as a stranger — no
error, no flash. That silence is worth knowing about when a session
mysteriously "does not stick".

Because the payload is a cookie, it is subject to the browser's roughly 4 KB
per-cookie limit. Sessions are for small facts: an id, a flag, a language
choice.

</details>

<details>
<summary>Under the hood — why `==` on a password is a real vulnerability</summary>

Python's `==` on strings returns as soon as it finds a differing byte.
Comparing `"a......"` against the true password takes measurably less time
than comparing `"letmei."`, because the second one gets six characters in
before it gives up. Over enough requests, an attacker who can time the
responses recovers the secret character by character. This is a **timing
attack**, and it is not theoretical — it is why the standard library ships
`hmac.compare_digest`, which always reads both inputs all the way to the end.

Real code does not compare passwords at all. It stores a hash:

```python
from werkzeug.security import check_password_hash, generate_password_hash

stored = generate_password_hash("letmein")   # at signup, saved to the database
check_password_hash(stored, submitted)       # at login
```

`generate_password_hash` is deliberately *slow* and salted, so a stolen
database cannot be reversed with a lookup table, and `check_password_hash`
does the comparison safely. Neither one appears in this homework, which is one
of the several reasons the file says DEMO ONLY.

</details>

<details>
<summary>Under the hood — CSRF, and why a POST-only logout is not the whole fix</summary>

Making logout a `POST` stops *accidental* triggering. It does not stop a
deliberate attack. Another site can host a form that posts to your `/logout`,
or your `/new`, and the browser will attach your cookies to it, because that
is what browsers do. That is **cross-site request forgery**.

The standard defence is a per-session random token, planted as a hidden field
in every form and checked on every state-changing request. An attacker's page
cannot read your token, so it cannot forge the request.
[Flask-WTF](https://flask-wtf.readthedocs.io/) does this for you with
`CSRFProtect(app)` and `{{ form.csrf_token }}`.

A second, cheaper layer is the `SameSite` cookie attribute, which tells the
browser not to send the cookie on cross-site requests at all:

```python
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,   # JavaScript cannot read the cookie
    SESSION_COOKIE_SECURE=True,     # HTTPS only
    SESSION_COOKIE_SAMESITE="Lax",  # not sent on cross-site POSTs
)
```

None of these are in the homework file.

</details>

<details>
<summary>Under the hood — server-side sessions, and why "log out everywhere" is hard</summary>

A Flask session is *client-side*: the whole state lives in the browser and the
server keeps nothing. That is wonderfully cheap, and it has one sharp edge —
the server cannot take a session back. Popping `is_admin` only works because
the visitor's own browser cooperates by sending the new, emptied cookie.
Somebody who copied the old cookie value still holds a valid, signed wristband
until it expires.

The fix is to keep sessions on the server and put only an opaque id in the
cookie, which is what
[Flask-Session](https://flask-session.readthedocs.io/) does with Redis, a
database, or the filesystem. Now "log out everywhere" is one delete, and
retiring a stolen session is possible at all. The trade is state: the server
has to store and expire those records.

The blunt version, available with no extra library, is to change
`SECRET_KEY` — which invalidates every session in the world at once,
including your own.

</details>

<details>
<summary>Under the hood — the `login_required` decorator, and Flask-Login</summary>

Copying the four-line guard into every protected view is how you end up with
one view that quietly lacks it. Lift it into a decorator instead:

```python
from functools import wraps


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please log in to create posts.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper
```

```python
@app.route("/new", methods=["GET", "POST"])
@login_required
def new_post(): ...
```

`@wraps` matters: without it every decorated view is named `wrapper`, and
Flask raises `AssertionError: View function mapping is overwriting an existing
endpoint` the moment you protect a second route.

[Flask-Login](https://flask-login.readthedocs.io/) is the grown-up version of
all of this — real user objects, `@login_required`, "remember me", session
protection, and `current_user` in every template.

</details>

## Acceptance checklist

- [ ] Unauthenticated `GET /new` redirects to `/login`, and the login page
      shows the flash.
- [ ] The correct password sets `session["is_admin"] = True` and redirects
      to `/`.
- [ ] A wrong password re-renders the form with an error flash and does not
      set the session.
- [ ] `POST /logout` clears `is_admin`, and calling it twice does not raise.
- [ ] The "Log in" link in the nav flips to "Log out" after logging in, with
      no view function passing `is_admin` into the template.
- [ ] The logout control is a `POST` form, not an `<a href>`.
- [ ] `SECRET_KEY` and `ADMIN_PASSWORD` both come from `os.environ.get` with
      a fallback, and neither real value is in the file.
- [ ] You opened the session cookie in devtools, read the payload, and
      corrupted one character to watch the session get dropped.

## Stretch

- **The security exercise, and it is the point of the problem.** Read the
  OWASP Session Management Cheat Sheet —
  <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
  — and write **three bullet points** describing what is wrong with the auth
  in this homework. You will not turn it in. The point is to be able to name
  the holes in something you built yourself.
- Replace the `==` comparison with `generate_password_hash` and
  `check_password_hash` from `werkzeug.security`. Store the hash in the config
  instead of the password, and confirm the flow still works.
- Pull the guard into a `login_required` decorator and protect a second route
  with it. Remember `@wraps`.
- Add the three cookie hardening settings (`SESSION_COOKIE_HTTPONLY`,
  `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`) plus
  `PERMANENT_SESSION_LIFETIME`, then work out why `SESSION_COOKIE_SECURE=True`
  breaks your local `http://` testing.
- Make login remember *where the visitor was going*: stash the blocked URL in
  the session before redirecting, and send them there after a successful login
  instead of to `/`. Then read about why blindly redirecting to a URL that came
  from a request is its own vulnerability, called an open redirect.
