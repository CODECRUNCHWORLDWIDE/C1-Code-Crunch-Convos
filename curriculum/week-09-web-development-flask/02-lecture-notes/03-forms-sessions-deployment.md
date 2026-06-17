# Lecture 3 — Forms, Sessions, and Deployment

> **Goal:** by the end of this lecture you can accept user input via HTML
> forms, handle `GET` vs `POST` cleanly, validate input on the server, give
> the user feedback with **flash messages**, keep small bits of state across
> requests with **sessions**, sketch a project with the **application factory**
> pattern, and deploy a Flask app for free on the public internet.

This is the lecture that turns your blog from read-only into something users
can interact with.

---

## 1. HTML forms in 90 seconds

An HTML form is a `<form>` element with one or more `<input>` (or `<textarea>`,
`<select>`, etc.) and a submit button. When the user clicks **Submit**, the
browser packages the field values into an HTTP request and sends it to the
URL in `action`, using the method in `method`.

```html
<form action="/new" method="post">
  <label for="title">Title</label>
  <input type="text" id="title" name="title" required>

  <label for="body">Body</label>
  <textarea id="body" name="body" rows="6" required></textarea>

  <button type="submit">Publish</button>
</form>
```

Key points to internalize:

- The **`name`** attribute is what the server sees as the form-field key. The
  `id` is only for the `<label for>` association. Forget `name` and your
  field will not be sent.
- **`required`** does *some* client-side validation, but a malicious user can
  bypass it. **Always validate on the server too.**
- The form's `action` should usually be the same URL as the page it is on
  (often `action=""` or omitted) so that posting back lands you in the same
  view function.

---

## 2. GET vs POST: which one do I use?

| Use case                                    | Method |
|---------------------------------------------|--------|
| Reading a page                              | `GET`  |
| Search forms (`/search?q=flask`)            | `GET`  |
| Submitting data that creates or changes     | `POST` |
| Login forms (passwords must never be in URL)| `POST` |
| Uploads                                     | `POST` |

Rule of thumb: **if the request changes server state, use `POST`.** Anything
in a URL (a `GET`'s query string) ends up in browser history, in server
access logs, and in HTTP referer headers. That is fine for `?q=flask`. It is
catastrophic for `?password=hunter2`.

When you accept both methods on one route, you branch on `request.method`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        # handle submission
        ...
    return render_template("new.html")
```

---

## 3. Reading form data: `request.form`

Inside a `POST` view, the submitted fields live in `request.form` — a
dict-like `MultiDict`:

```python
title: str = request.form.get("title", "").strip()
body:  str = request.form.get("body", "").strip()
```

Use `.get("key", "")` rather than `request.form["key"]` so a missing field
returns an empty string instead of raising `KeyError`. Treat *all* incoming
strings as untrusted: `.strip()` them, length-check them, type-check them.

For checkboxes and multi-selects, use `getlist`:

```python
tags: list[str] = request.form.getlist("tags")
```

---

## 4. Server-side validation (the simple version)

Build a list of error messages, render the form again if there are any, and
only "save" the data if the list is empty:

```python
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "change-me-in-production"   # needed for flash + session

POSTS: list[dict[str, str]] = []


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body  = request.form.get("body", "").strip()

        errors: list[str] = []
        if not title:
            errors.append("Title is required.")
        if len(title) > 120:
            errors.append("Title must be 120 characters or fewer.")
        if not body:
            errors.append("Body is required.")

        if errors:
            for msg in errors:
                flash(msg, category="error")
            # Re-render the form with the typed values so the user does not
            # have to start over.
            return render_template("new.html", title=title, body=body)

        POSTS.append({"title": title, "body": body})
        flash("Post published.", category="success")
        return redirect(url_for("index"))

    return render_template("new.html", title="", body="")
```

This pattern is called **Post / Redirect / Get (PRG)**. After a successful
`POST`, you `redirect` so that refreshing the destination page does not
re-submit the form. Browsers warn you about this; PRG silences the warning by
making the destination an idempotent `GET`.

For richer validation (CSRF tokens, type coercion, field-level error
messages), reach for **Flask-WTF**:

```bash
pip install flask-wtf
```

It is optional this week; the homework includes a Flask-WTF stretch problem.

---

## 5. Flash messages

`flash()` stores a short message in the session, to be displayed on the *next*
page the user sees. It is perfect for "Saved!", "Login failed", and other
one-off notifications.

The pattern:

```python
from flask import flash, redirect, url_for

flash("Post published.", category="success")
return redirect(url_for("index"))
```

To render flashed messages, put this in `base.html` (or include it):

```jinja
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class="flashes">
      {% for category, message in messages %}
        <li class="flash flash-{{ category }}">{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

Each message is consumed once — refresh the destination page and it is gone.

Categories are arbitrary strings (`"success"`, `"error"`, `"warning"`); you
style them with CSS (`.flash-success { background: #d4edda }`, etc.). If you
omit `with_categories=true`, `get_flashed_messages()` returns a plain list of
message strings.

---

## 6. Sessions and the `SECRET_KEY`

`flash` works because Flask gives you a built-in **session** — a dictionary
that survives across requests for the *same* browser. It is implemented as a
cryptographically signed cookie, which is why Flask insists on a secret key.

```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "change-me-in-production"


@app.route("/visit")
def visit():
    session["count"] = session.get("count", 0) + 1
    return f"You have visited this page {session['count']} time(s)."


@app.route("/forget")
def forget():
    session.clear()
    return "Session cleared."
```

The browser receives a `Set-Cookie` header with the (signed) contents of
`session`. Every later request sends the cookie back. Flask verifies the
signature with your secret key before letting you read it.

Three rules of secret keys:

1. **It must be a long, random string.** A short or predictable key lets
   anyone forge cookies and impersonate users.
2. **Never commit it to git.** Put it in an environment variable; load it
   with `python-dotenv` in development and as a real env var in production.
3. **Changing it logs everyone out**, because their cookies will fail
   verification.

A reasonable generator:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

And the modern way to load it:

```python
import os
from dotenv import load_dotenv

load_dotenv()                                  # reads .env in dev
app.secret_key = os.environ["SECRET_KEY"]      # KeyError if missing — good
```

with a `.env` file (gitignored!):

```text
SECRET_KEY=replace-me-with-secrets-token-hex
```

Important: Flask sessions are **signed, not encrypted**. The user cannot
*forge* a session, but they can *read* it (it's base64-encoded JSON in the
cookie). Never store passwords, credit cards, or anything sensitive in
`session`.

---

## 7. Application factory and blueprints (light)

For a single-file app, `app = Flask(__name__)` at module top level is fine.
Once you have multiple views, configs, and tests, you want the
**application factory** pattern: a function that *builds and returns* an
app.

```python
# my_blog/__init__.py
import os
from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
    )
    if test_config:
        app.config.update(test_config)

    from . import posts
    app.register_blueprint(posts.bp)

    return app
```

A **blueprint** is a self-contained group of routes you can register on an
app. It lets you split a big app into modules:

```python
# my_blog/posts.py
from flask import Blueprint, render_template

bp = Blueprint("posts", __name__, url_prefix="/posts")


@bp.route("/")
def index() -> str:
    return render_template("posts/index.html", posts=[])
```

When you `url_for` a blueprint endpoint, you prefix the function name with
the blueprint name: `url_for("posts.index")`.

You do **not** need this for the mini-project. But you should be able to
recognise the pattern, because every nontrivial Flask app in the wild uses
it.

The Flask Tutorial walks through the full factory pattern step by step:
<https://flask.palletsprojects.com/en/stable/tutorial/factory/>.

---

## 8. Deploying for free

The two biggest jumps in any developer's career are:

1. "My code runs on my computer."
2. "My code runs on the internet and other people can use it."

Free-tier hosts make #2 a 15-minute exercise. The current good options for
small Flask apps:

- **Fly.io** — <https://fly.io/docs/python/>. Runs Docker containers; the
  `flyctl launch` command can detect a Flask app and generate a Dockerfile
  for you.
- **Render** — <https://render.com/docs/deploy-flask>. Simpler UI; point it
  at a GitHub repo, give it a build command and a start command, done.
- **Railway** — <https://docs.railway.app/guides/flask>. Similar to Render.

For all three, you will produce:

- A **`requirements.txt`** listing your dependencies:
  ```text
  flask>=3.0
  gunicorn>=21.0
  python-dotenv>=1.0
  ```
- A **`Procfile`** (Render/Railway) or a **start command** that runs your app
  in production:
  ```text
  web: gunicorn "app:app" --bind 0.0.0.0:$PORT
  ```

A few production-shaped reminders:

- **Do not** use `app.run(debug=True)` in production. The Flask dev server is
  single-threaded and the debugger is a remote-code-execution vector.
- Use **`gunicorn`** as your WSGI server. It is the de facto standard:
  ```bash
  pip install gunicorn
  gunicorn "app:app" --workers 2 --bind 0.0.0.0:8000
  ```
  The string `"app:app"` means *"the `app` object inside the `app` module"*.
- Set your **`SECRET_KEY`** in the host's environment-variable UI, not in
  the code.
- Set `debug=False` (the default) and turn off any verbose error pages.

You do **not** need to deploy for this week to count as finished. But once you
have a working blog, spending an hour deploying it is the single best use of
that hour. Send the URL to a friend. Watch them load it. That feeling is why
people become developers.

---

## 9. `python-dotenv` and `gunicorn` in one page

**`python-dotenv`** lets you keep configuration in a `.env` file during
development, without leaking it to the world.

`.env`:

```text
SECRET_KEY=cdb4ef2a8a3d8a0a3eaf7a2e4b1c5d6e
FLASK_DEBUG=1
```

`app.py`:

```python
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()                                   # populate os.environ

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
```

`.gitignore` (**critical**):

```text
.env
.venv/
__pycache__/
```

In production you do not ship `.env`; you set the same variables in your
host's dashboard.

**`gunicorn`** is your production WSGI server. Locally you can try it:

```bash
pip install gunicorn
gunicorn "app:app" --workers 2 --bind 127.0.0.1:8000
```

Then open <http://127.0.0.1:8000>. No `debug=True`, no auto-reload, but real
concurrency. This is closer to what your deployment will look like.

---

## 10. A complete create-post example

Putting it all together: a working "new post" page with validation, flash,
and PRG.

`app.py`:

```python
"""Mini blog with a real form. Run: python app.py"""
import os
from dataclasses import dataclass, field
from itertools import count

from dotenv import load_dotenv
from flask import (
    Flask, flash, redirect, render_template, request, url_for, abort,
)

load_dotenv()

app: Flask = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


@dataclass
class Post:
    id: int
    title: str
    body: str


_id_seq = count(1)
POSTS: list[Post] = [
    Post(next(_id_seq), "Hello", "First post."),
]


@app.route("/")
def index() -> str:
    return render_template("index.html", posts=POSTS)


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    for p in POSTS:
        if p.id == post_id:
            return render_template("post.html", post=p)
    abort(404)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body  = request.form.get("body", "").strip()

        errors: list[str] = []
        if not title:
            errors.append("Title is required.")
        if len(title) > 120:
            errors.append("Title must be 120 characters or fewer.")
        if not body:
            errors.append("Body is required.")

        if errors:
            for msg in errors:
                flash(msg, category="error")
            return render_template("new.html", title=title, body=body)

        POSTS.append(Post(next(_id_seq), title, body))
        flash("Post published.", category="success")
        return redirect(url_for("index"))

    return render_template("new.html", title="", body="")


if __name__ == "__main__":
    app.run(debug=True)
```

`templates/new.html`:

```jinja
{% extends "base.html" %}
{% block title %}New post — My Blog{% endblock %}
{% block content %}
  <h2>New post</h2>
  <form method="post" action="{{ url_for('new_post') }}">
    <label for="title">Title</label>
    <input type="text" id="title" name="title"
           value="{{ title }}" maxlength="120" required>

    <label for="body">Body</label>
    <textarea id="body" name="body" rows="8" required>{{ body }}</textarea>

    <button type="submit">Publish</button>
    <a href="{{ url_for('index') }}">Cancel</a>
  </form>
{% endblock %}
```

You now have a working mini-blog with a working form. This is exactly the
shape of the mini-project — you just need to put more polish on it.

---

## 11. Recap and what is next

You can now:

- Build HTML forms and read their data with `request.form`.
- Branch on `request.method` and follow the **Post/Redirect/Get** pattern.
- Validate input server-side and re-render with the user's typed values.
- Use `flash()` for one-shot messages and read them in templates with
  `get_flashed_messages`.
- Set a `SECRET_KEY` correctly and store small bits of state in `session`.
- Recognise the **application factory** + **blueprint** pattern.
- Deploy a Flask app for free with `gunicorn` behind a host like Fly.io,
  Render, or Railway.
- Keep secrets out of git with `python-dotenv`.

> **Practice:** finish `exercises/exercise-04-form-echo/` and at least one of
> the challenges. Then take a swing at the mini-project — the personal blog
> ties all three lectures together.

Week 10 replaces the in-memory list of posts with a real database, so
restarts no longer wipe your blog. Many of the Flask patterns you wrote this
week stay exactly as they are — you just swap `POSTS = []` for a SQL query.

---

## References

- Flask request data — <https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data>
- Flask sessions — <https://flask.palletsprojects.com/en/stable/quickstart/#sessions>
- Flask flashing pattern — <https://flask.palletsprojects.com/en/stable/patterns/flashing/>
- Flask application factories — <https://flask.palletsprojects.com/en/stable/patterns/appfactories/>
- Flask blueprints — <https://flask.palletsprojects.com/en/stable/blueprints/>
- Flask deploying to production — <https://flask.palletsprojects.com/en/stable/deploying/>
- `python-dotenv` — <https://pypi.org/project/python-dotenv/>
- Gunicorn docs — <https://docs.gunicorn.org/en/stable/>
- Flask-WTF (forms + CSRF) — <https://flask-wtf.readthedocs.io/>
