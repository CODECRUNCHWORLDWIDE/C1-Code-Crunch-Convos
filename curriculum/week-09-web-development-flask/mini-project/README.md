# Mini-Project — Personal Blog

> **Topic:** A whole small Flask app: routes, templates, a form, and flash
> **Lecture:** [03 — Forms, sessions, deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Medium
> **Target time:** 4-6 hours
> **Why this one:** every route, template and form idea from the week meets in one
> place here. It is the smallest thing that still feels like a real website, and
> it is the exact shape Week 10 will pour a database into without changing the
> routes at all.

## The Brief

Build a personal blog. Not a big one: a page that lists posts newest-first, a
page that shows one post, and a form that adds a new one. When you publish, the
post appears at the top of the list.

Think of it like a whiteboard on a wall. The list page is the whole board. Each
post is a card pinned to it. The form is the marker you use to write a new card,
and pinning it up puts it at the top where everyone sees it next.

Nothing here is stored to disk yet. The posts live in a plain Python list while
the program runs, which is all you need to learn the routing and the forms. Week
10 swaps that list for a database and barely touches the routes, and that swap
is the point of building it tidily now.

## Starter

Build it in a folder of your own, route by route, working from the
specification in Requirements below. You are writing `blog.py` plus four templates under
`templates/`. The specification in Requirements below is the whole contract; the
starter gives you the skeleton and the data model.

The finished answer that ships beside this page,
[personal_blog.py](./personal_blog.py), keeps all four templates inside the one
file using Jinja's `DictLoader`, so the download is a single file you can run.
Yours does not have to: real Flask apps keep templates in a `templates/` folder,
and that is the layout the starter and the specification describe.

## Requirements

1. **Five routes**, exactly these:

   | Method | URL | Behaviour |
   |--------|-----|-----------|
   | GET | `/` | List all posts, newest first, title and a short excerpt |
   | GET | `/post/<int:post_id>` | Show one post in full |
   | GET | `/new` | Show the create-post form |
   | POST | `/new` | Validate, store, flash, then redirect to `/` |
   | GET | `/static/style.css` | Your stylesheet, which Flask serves for you |

2. **A 404 for an unknown post.** `GET /post/9999` must return 404 with
   `abort(404)`. Because the route uses `<int:post_id>`, `GET /post/seven` also
   404s, before your view even runs.
3. **Four templates**, and the three content templates all extend `base.html`
   so the layout is written once.
4. **Every link goes through `url_for`.** No hard-coded `/post/1` anywhere.
5. **The form validates and re-renders on failure.** Reject an empty title or
   body, a title over 120 characters, and a body over 10,000. On rejection,
   re-render the form with the error shown and the typed text still in the
   boxes; do not throw the draft away.
6. **Publish uses Post/Redirect/Get.** A successful `POST /new` redirects to `/`
   with a 302, so a refresh does not publish the post a second time.

## Constraints

- **Posts live in a module-level list, not a database.** A database is Week 10,
  and adding one now would hide the routing lesson behind a second new thing.
- **`app.secret_key` comes from the environment, with a dev fallback.** `flash`
  signs the session cookie and cannot sign without a key. A key typed into the
  code is a key that ships in the code; read it from `os.environ` and fall back
  to an obvious dev-only string so a missing key is loud, not silent.
- **No `debug=True` in anything you hand in.** The debug traceback page is an
  interactive Python console open to whoever hits an error. It is a local
  convenience and a production disaster; keep it out of the deliverable.

## Expected output

The shipped answer proves every route with `app.test_client()` instead of
starting a server, so it runs headless, with no port and no browser, and its
output is the same every time. Captured on CPython 3.13.2 with Flask 3.1:

```text
Driving the finished blog with app.test_client() — no port, no browser.

GET  /                  -> 200
  empty state shown     : True
GET  /new               -> 200 (the form)

Validation — the draft survives every rejection:
POST /new (no title)    -> 200 (re-rendered, not redirected)
  <li class="flash flash-error">Title is required.</li>
  the typed body is still in the form: True
  <li class="flash flash-error">Title must be 120 characters or fewer.</li>
  <li class="flash flash-error">Body must be 10,000 characters or fewer.</li>

Publishing — Post / Redirect / Get:
POST /new 'Hello, Flask'  -> 302  Location: /
  <li class="flash flash-success">Post published.</li>
  refresh repeats nothing: flash gone -> True
  index order, newest first: ['Second post', 'Hello, Flask']

The single-post page and the failure paths:
GET  /post/1            -> 200
  full body shown       : True
GET  /post/9999         -> 404
GET  /post/seven        -> 404 (the int converter, before any view ran)

GET  /static/style.css  -> 200 text/css; charset=utf-8
templates carrying their own layout: 1 of 4 (only base.html)
```

## Steps

1. Get `GET /` rendering one hard-coded post. Do not add the form yet.
2. Add `GET /post/<int:post_id>` and the `abort(404)` for unknown ids.
3. Add `GET /new`: just the form, no handling.
4. Add `POST /new`: validate, and on success append to the list, flash, and
   redirect. Watch the terminal; Flask prints every request and every template
   error.
5. Add the validation failures one at a time, checking each re-renders with the
   typed text intact.
6. Style it with a small `style.css`, linked through `url_for`.
7. Read the terminal whenever something looks wrong: the answer is almost always
   printed there already.

## The Solution

The download keeps its four templates in a `DictLoader` so it is one runnable
file. In your own version they live under `templates/`; the routing and the
validation are identical.

```python
"""personal_blog.py — the finished answer to Week 9's mini-project.

The whole blog from the spec, in one runnable file: a homepage listing posts
newest first, a single-post page, a create-post form with server-side
validation and Post/Redirect/Get, flash messages, a 404 for unknown ids, and
a small stylesheet. Posts live in a module-level list; a restart wipes them,
and Week 10 replaces the list with SQLite.

Your own build is a folder — `app.py`, `templates/`, `static/` — and that
folder is what you hand in. This download exists so the reference answer runs
anywhere as one file, so it makes three packaging moves your build does not
need:

1. **Templates travel inside the file.** The four templates sit in constants
   and reach Jinja through a ``DictLoader``. Same text, same names, same
   autoescaping; no folder required.
2. **The stylesheet is served by a one-line route.** Your build puts
   `style.css` in `static/` and Flask serves it automatically. A single file
   has no `static/` folder, so a literal route answers the same URL — the
   templates still link it with ``url_for('static', filename='style.css')``,
   and that URL still works.
3. **No server starts.** Instead of ``app.run()``, the ``__main__`` block
   drives the app with ``app.test_client()`` — Flask's in-process fake
   browser — walks the whole rubric, prints each round trip, and exits. The
   download proves the routes work without occupying a port; ``flask run``
   is what you use when you want to click around.

Run it with::

    python personal_blog.py
"""

from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
import os
import sys

# The summary this script prints uses an arrow; a legacy Windows console
# cannot encode it and would mangle or crash on it. UTF-8 fixes that.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for
from jinja2 import DictLoader

# --------------------------------------------------------------------------- #
# Templates — templates/*.html in your build, constants in this download
# --------------------------------------------------------------------------- #

#: templates/base.html — everything true of every page, exactly once.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
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

    <footer>
      <small>Built with Flask. Posts live in memory until Week 10.</small>
    </footer>
  </body>
</html>
"""

#: templates/index.html — the list, newest first, title plus excerpt.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>
  {% for post in posts %}
    <article>
      <h3><a href="{{ url_for('show_post', post_id=post.id) }}">{{ post.title }}</a></h3>
      <p class="meta">{{ post.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
      <p>{{ post.body|truncate(120) }}</p>
    </article>
  {% else %}
    <p>No posts yet. <a href="{{ url_for('new_post') }}">Write the first one.</a></p>
  {% endfor %}
{% endblock %}
"""

#: templates/post.html — one post in full.
POST_HTML: str = """\
{% extends "base.html" %}

{% block title %}{{ post.title }} — Crunch Blog{% endblock %}

{% block content %}
  <article>
    <h2>{{ post.title }}</h2>
    <p class="meta">{{ post.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
    <p>{{ post.body }}</p>
    <p><a href="{{ url_for('index') }}">&larr; Back to all posts</a></p>
  </article>
{% endblock %}
"""

#: templates/new.html — the create form. On a validation error it re-renders
#: with the values the user typed, so nobody loses a draft.
NEW_HTML: str = """\
{% extends "base.html" %}

{% block title %}New post — Crunch Blog{% endblock %}

{% block content %}
  <h2>New post</h2>
  <form method="post" action="{{ url_for('new_post') }}">
    <label for="title">Title</label>
    <input type="text" id="title" name="title" value="{{ title }}"
           maxlength="120" required>

    <label for="body">Body</label>
    <textarea id="body" name="body" rows="10" required>{{ body }}</textarea>

    <button type="submit">Publish</button>
  </form>
{% endblock %}
"""

#: static/style.css in your build — served here by the literal route below.
STYLE_CSS: str = """\
* { box-sizing: border-box; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  max-width: 40rem;
  margin: 2rem auto;
  padding: 0 1rem;
  color: #222;
  background: #fafafa;
  line-height: 1.6;
}

header h1 a { color: #222; text-decoration: none; }
nav a { margin-right: 0.75rem; }

article { border-bottom: 1px solid #ddd; padding: 0.75rem 0; }
p.meta { color: #666; font-size: 0.875rem; }

label { display: block; font-weight: 600; margin-top: 0.75rem; }
input[type="text"], textarea { width: 100%; padding: 0.5rem; font: inherit; }
button {
  margin-top: 0.75rem;
  padding: 0.4rem 0.75rem;
  font: inherit;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  background: #fff;
}

ul.flashes { list-style: none; padding: 0; }
.flash { padding: 0.5rem 0.75rem; border-radius: 0.25rem; margin: 0.25rem 0; }
.flash-success { background: #d4edda; color: #155724; }
.flash-error { background: #f8d7da; color: #721c24; }

footer { margin-top: 3rem; color: #666; font-size: 0.875rem; }
"""

# --------------------------------------------------------------------------- #
# The app
# --------------------------------------------------------------------------- #

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {
        "base.html": BASE_HTML,
        "index.html": INDEX_HTML,
        "post.html": POST_HTML,
        "new.html": NEW_HTML,
    }
)

# flash() needs a signing key. From the environment, never from the source;
# the fallback is deliberately named so it screams if it ever reaches a log.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

MAX_TITLE_LEN: int = 120
MAX_BODY_LEN: int = 10_000


@dataclass
class Post:
    """One blog post."""

    id: int
    title: str
    body: str
    created_at: datetime = field(default_factory=datetime.now)


POSTS: list[Post] = []
_id_seq = count(1)


def newest_first() -> list[Post]:
    """The posts, most recent on top. Ties break toward the higher id."""
    return sorted(POSTS, key=lambda p: (p.created_at, p.id), reverse=True)


def find_post(post_id: int) -> Post:
    """Return the post with *post_id*, or unwind the request with a 404."""
    for post in POSTS:
        if post.id == post_id:
            return post
    abort(404)


@app.route("/")
def index() -> str:
    """List all posts, newest first, with title and excerpt."""
    return render_template("index.html", posts=newest_first())


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    """Show one post in full. Unknown ids 404 before this body runs far."""
    return render_template("post.html", post=find_post(post_id))


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str | Response:
    """Show the form on GET; validate, store, flash, and redirect on POST."""
    if request.method == "POST":
        title: str = request.form.get("title", "").strip()
        body: str = request.form.get("body", "").strip()

        errors: list[str] = []
        if not title:
            errors.append("Title is required.")
        if not body:
            errors.append("Body is required.")
        if len(title) > MAX_TITLE_LEN:
            errors.append(f"Title must be {MAX_TITLE_LEN} characters or fewer.")
        if len(body) > MAX_BODY_LEN:
            errors.append(f"Body must be {MAX_BODY_LEN:,} characters or fewer.")

        if errors:
            for problem in errors:
                flash(problem, category="error")
            # Re-render with what they typed so the draft survives.
            return render_template("new.html", title=title, body=body)

        POSTS.append(Post(next(_id_seq), title=title, body=body))
        flash("Post published.", category="success")
        return redirect(url_for("index"))

    return render_template("new.html", title="", body="")


@app.route("/static/style.css")
def stylesheet() -> Response:
    """Serve the stylesheet from the constant above.

    Only this single-file download needs the route: in your build the file
    sits in `static/` and Flask's built-in static route serves it. A literal
    rule outranks the dynamic `/static/<path:filename>`, so this wins here.
    """
    return Response(STYLE_CSS, mimetype="text/css")


# --------------------------------------------------------------------------- #
# The demo run — the rubric, walked end to end
# --------------------------------------------------------------------------- #


def flash_lines(page: str) -> list[str]:
    """Pull the rendered flash <li> lines out of a page, stripped."""
    return [line.strip() for line in page.splitlines() if 'class="flash ' in line]


def titles_in_order(page: str) -> list[str]:
    """The post titles on the index, top to bottom."""
    import re

    return re.findall(r'href="/post/\d+">([^<]+)</a></h3>', page)


def main() -> None:
    """Drive the finished blog through every rubric line and print the trip."""
    client = app.test_client()

    print("Driving the finished blog with app.test_client() — no port, no browser.")
    print()

    response = client.get("/")
    print(f"GET  /                  -> {response.status_code}")
    print(f"  empty state shown     : {'No posts yet.' in response.get_data(as_text=True)}")

    response = client.get("/new")
    print(f"GET  /new               -> {response.status_code} (the form)")

    print()
    print("Validation — the draft survives every rejection:")
    response = client.post("/new", data={"title": "", "body": "A body without a title."})
    body = response.get_data(as_text=True)
    print(f"POST /new (no title)    -> {response.status_code} (re-rendered, not redirected)")
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"  the typed body is still in the form: {'A body without a title.</textarea>' in body}")

    response = client.post("/new", data={"title": "x" * 121, "body": "hi"})
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")

    response = client.post("/new", data={"title": "ok", "body": "y" * 10_001})
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")

    print()
    print("Publishing — Post / Redirect / Get:")
    response = client.post(
        "/new",
        data={"title": "Hello, Flask", "body": "The first post, straight from the form."},
    )
    print(f"POST /new 'Hello, Flask'  -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/").get_data(as_text=True)
    for line in flash_lines(body):
        print(f"  {line}")
    body = client.get("/").get_data(as_text=True)
    print(f"  refresh repeats nothing: flash gone -> {not flash_lines(body)}")

    client.post("/new", data={"title": "Second post", "body": "Newer, so it lists first."})
    body = client.get("/").get_data(as_text=True)
    print(f"  index order, newest first: {titles_in_order(body)}")

    print()
    print("The single-post page and the failure paths:")
    response = client.get("/post/1")
    print(f"GET  /post/1            -> {response.status_code}")
    print(f"  full body shown       : {'straight from the form.' in response.get_data(as_text=True)}")
    print(f"GET  /post/9999         -> {client.get('/post/9999').status_code}")
    print(f"GET  /post/seven        -> {client.get('/post/seven').status_code} (the int converter, before any view ran)")

    print()
    response = client.get("/static/style.css")
    print(f"GET  /static/style.css  -> {response.status_code} {response.headers['Content-Type']}")

    doctypes = sum(
        "<!doctype html>" in text for text in (BASE_HTML, INDEX_HTML, POST_HTML, NEW_HTML)
    )
    print(f"templates carrying their own layout: {doctypes} of 4 (only base.html)")


if __name__ == "__main__":
    main()
```

**Why it works.** The whole app is three ideas stacked up. The routes map a URL
to a function. The templates turn data into HTML, once per shape of page, with
`base.html` holding the parts every page shares. And the form does the one thing
that makes a form trustworthy: when it rejects your input, it hands your input
back so you can fix it instead of retyping it.

The publish path is the piece worth staring at. `POST /new` does not render a
page; on success it redirects. The browser then does a fresh `GET /`, which is
the page you actually wanted. That extra hop is Post/Redirect/Get, and it is why
refreshing the published page does not publish again: a refresh re-runs the
`GET`, not the `POST`. The flash message survives exactly one request, so it
shows once on the redirected page and is gone on the next refresh.

## Download and run

<!-- no-runnable-file: the deliverable is a folder in your own repository, blog.py plus the templates and a stylesheet and a commit history, not a single script. The finished answer ships as personal_blog.py, which folds the templates into one file so it runs on its own, and is linked below. -->

Download [personal_blog.py](./personal_blog.py) and run it:

```bash
pip install flask
python personal_blog.py
```

It drives itself with the test client and prints the run above, with no server
and no port. To see it in a browser instead, the file's docstring shows the two
lines that start a real dev server.

## Common bugs to catch

- **The form throws your text away on an error.** You re-rendered the template
  with no values, so the boxes came back empty. Pass the submitted title and
  body back into the template on the failure path.
- **Refreshing the published page publishes again.** Your `POST /new` rendered
  the index instead of redirecting to it. Return a `redirect(url_for(...))` on
  success; the browser's refresh then repeats a harmless `GET`.
- **`RuntimeError: The session is unavailable because no secret key was set.`**
  `flash` needs `app.secret_key`. Set it from the environment before the first
  request.
- **A hard-coded `/post/1` breaks when the route name changes.** Requirement 4
  exists for this. `url_for` follows the route wherever it moves.
- **`GET /post/seven` errors instead of 404ing.** You used `<post_id>` not
  `<int:post_id>`, so Flask handed your view the string `"seven"`. The `int`
  converter rejects it with a 404 before your code runs.

## Under the hood

<details>
<summary>Under the hood - what a session cookie actually holds, and why signed is not encrypted</summary>

`flash` stores its message in the session, and the session is a cookie. Open
your browser's devtools after a flash and you will see a cookie whose value is
base64 text with two dots in it, the same shape as a JSON Web Token. Decode the
first part and you can read your own flash message in plain text.

That is the point to understand: the session cookie is signed, not encrypted.
`app.secret_key` does not hide the contents; it stamps them so the server can
tell its own cookie from a forged one. Anyone can read what is in there. So a
session is fine for "you are logged in as user 7" and wrong for "here is user
7's password": the first is not a secret, the second is.

Change the secret key and every existing cookie stops validating, which is why
rotating the key logs everybody out. It is also why a key committed to Git is a
real problem: anyone with the key can mint a cookie the server will trust.

</details>

## Acceptance checklist

- [ ] `GET /` lists posts newest-first, each title linking to its detail page.
- [ ] `GET /post/<id>` shows the full post; an unknown id 404s.
- [ ] `GET /new` renders the form; `POST /new` validates, stores, flashes, and
      redirects.
- [ ] A failed submission re-renders with the typed text still in the boxes.
- [ ] All three content templates extend `base.html`.
- [ ] Every link uses `url_for`; the stylesheet is linked with `url_for` too.
- [ ] `app.secret_key` is read from the environment, not typed into the code.
- [ ] Nothing you hand in runs with `debug=True`.
- [ ] Committed to Git with a clear message, e.g. `feat(blog): personal blog mini-project`.

## Stretch

- **Custom 404 page.** Register an error handler and render a friendly template
  instead of Flask's default.
- **Tags.** Add a comma-separated tags field and a `/tag/<name>` route that
  filters the list.
- **Search.** A `?q=` query on `/` that keeps only posts whose title or body
  contains the term.
- **Deploy it.** Put it on a free host, set `SECRET_KEY` as a real environment
  variable there, and confirm `debug` is off.
