# Homework Problem 1 — Custom 404 page

> **Topic:** `@app.errorhandler(404)`, and keeping the status code honest while you change the page
> **Lecture:** [01 — Flask Hello World](../lecture-notes/01-flask-hello-world.md) · [02 — Templates and Static Files](../lecture-notes/02-templates-and-static.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** the whole problem is nine lines, and one of them — the `, 404` — is the difference between a page that tells the truth and a page that lies to every non-human client. It is also the first payoff of the base template: a 404 page that wears the site's own layout costs six lines, because `{% extends %}` brings everything else along.

## The Brief

Right now, visiting `/post/9999` on your blog shows Flask's default
"Not Found" page — bare, unstyled, and obviously not yours. Replace it with a
friendly one that extends `base.html`, so a lost visitor still sees your
header, your footer, and a link back home.

The mechanism is an **error handler**: a function you register for a status
code rather than a URL. When any part of the app produces a 404 — your own
`abort(404)`, a URL that matches no route, an id the `<int:>` converter
rejects — Flask calls your handler instead of rendering its stock page. One
handler, every 404 in the app.

This is a change to your mini-project blog. The shipped file beside this page
is a self-contained slice of that blog — a layout, an index, a post page,
and the two pieces this problem adds — so the answer runs anywhere as one
file.

## Starter

Save as `problem-01-custom-404-page.py` and fill in the `TODO`s. The
templates are given complete; the work is the handler and the 404 template's
registration.

```python
"""problem-01-custom-404-page.py — starter: a blog slice that still shows stock 404s.

Run with: python problem-01-custom-404-page.py
"""

from flask import Flask, abort, render_template
from jinja2 import DictLoader

BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <header><h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1></header>
    <main>{% block content %}{% endblock %}</main>
    <footer><small>Built with Flask. Posts live in memory until Week 10.</small></footer>
  </body>
</html>
"""

INDEX_HTML: str = """\
{% extends "base.html" %}
{% block content %}
  <h2>Latest posts</h2>
  {% for post_id, title in posts.items() %}
    <p><a href="{{ url_for('show_post', post_id=post_id) }}">{{ title }}</a></p>
  {% endfor %}
{% endblock %}
"""

POST_HTML: str = """\
{% extends "base.html" %}
{% block title %}{{ title }} — Crunch Blog{% endblock %}
{% block content %}<article><h2>{{ title }}</h2></article>{% endblock %}
"""

# TODO: write NOT_FOUND_HTML — extends base.html, a title block, and a content
# block with a short apology and a url_for('index') link back home.

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {
        "base.html": BASE_HTML,
        "index.html": INDEX_HTML,
        "post.html": POST_HTML,
        # TODO: register "404.html" here too
    }
)

POSTS: dict[int, str] = {
    1: "Hello, Flask",
    2: "Templates all the way down",
}


@app.route("/")
def index() -> str:
    """List every post title."""
    return render_template("index.html", posts=POSTS)


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    """Show one post, or 404 for an id that was never published."""
    if post_id not in POSTS:
        abort(404)
    return render_template("post.html", title=POSTS[post_id])


# TODO: register a handler with @app.errorhandler(404) that renders 404.html
# AND returns status 404. The status does not come along for free — see the
# Constraints.


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

In your own blog the same change is two files: the handler at the bottom of
`app.py`, and `templates/404.html`.

## Requirements

1. `/post/9999` returns status **404** AND renders your custom page.
2. The page uses the same header/footer as the rest of the site — it extends
   `base.html`, and the footer text proves it.
3. `/post/seven` (rejected by the `<int:>` converter) and `/nonsense`
   (matching no route at all) land on the same custom page, with the same
   404 status.
4. Refreshing any *existing* page still works — you did not break the happy
   path.

## Constraints

- **Return `render_template("404.html"), 404` — the tuple, not the bare
  string.** `render_template` returns a plain string, and a handler that
  returns a bare string gets wrapped in a **200**, exactly like any view.
  You get a page that says "not found" over a status code that says
  everything is fine. Browsers render both identically; search engines,
  monitoring, and `curl -i` do not. There is no error and no warning when
  you get this wrong, which is why the shipped file builds a second,
  deliberately careless app to show it.
- **Register on the status code, not on a path.** `@app.route("/404")` is a
  page *at the URL* `/404` — nothing will ever send visitors there. The
  decorator is `@app.errorhandler(404)` and it takes the number.
- **The handler receives the exception object.** That is the `error`
  parameter, and you are free to ignore it — but the signature must accept
  it.
- **Keep the template six lines.** Everything else — doctype, header, nav,
  footer — arrives from `{% extends "base.html" %}`. If your 404 template
  contains a `<html>` tag, you are duplicating the layout, which is problem
  2's whole subject.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-01-custom-404-page-solution.py
GET /            -> 200 (the happy path still works)
GET /post/1      -> 200

GET /post/9999   -> 404
  the custom page rendered   : True
  it wears base.html's layout: True

Two 404s your code never sees, caught by the same handler:
  GET /post/seven -> 404 (the int converter rejected it before any view ran)
  GET /nonsense   -> 404 (no rule matched at all)

The bug this problem exists to prevent — a handler without ', 404':
  GET /boom -> 200 (the page says not found; the status says everything is fine)
```

## Steps

1. Write `NOT_FOUND_HTML` (or `templates/404.html` in your blog): extends,
   a title block, a short message, a `url_for('index')` link home.
2. Register it with the loader (in your blog: just save the file in
   `templates/`).
3. Write the handler. Return the rendered template **and** the status, as a
   tuple.
4. Hit `/post/9999`, `/post/seven`, and `/nonsense`. All three should show
   your page. In a terminal, confirm the status with
   `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/post/9999`.
5. Hit `/` and `/post/1` to prove the happy path survived.
6. Now break it on purpose: remove the `, 404` and re-run step 4's `curl`.
   Read the `200`. Put it back.

## The Solution

```python
"""problem-01-custom-404-page-solution.py — one handler, every 404 in the app.

A small slice of the blog — a layout, an index, a post page — plus the two
pieces this problem actually asks for: an ``@app.errorhandler(404)`` and a
``404.html`` that extends ``base.html``.

Your own build keeps the templates in a `templates/` folder. This download
carries the same text in constants, handed to Jinja through a ``DictLoader``,
so one file runs anywhere. And instead of ending in ``app.run(debug=True)``,
it drives the app with ``app.test_client()`` — Flask's in-process fake
browser — prints what every kind of 404 returns, and exits.

It also builds a second, deliberately careless app whose handler forgets the
``, 404`` — so you can see the bug this problem exists to prevent: a page
that says "not found" over a status code that says everything is fine.

Run it with::

    python problem-01-custom-404-page-solution.py
"""

from flask import Flask, abort, render_template
from jinja2 import DictLoader

#: templates/base.html — the layout every page wears, the footer included.
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
    </header>
    <main>
      {% block content %}{% endblock %}
    </main>
    <footer>
      <small>Built with Flask. Posts live in memory until Week 10.</small>
    </footer>
  </body>
</html>
"""

#: templates/index.html
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>
  {% for post_id, title in posts.items() %}
    <p><a href="{{ url_for('show_post', post_id=post_id) }}">{{ title }}</a></p>
  {% endfor %}
{% endblock %}
"""

#: templates/post.html
POST_HTML: str = """\
{% extends "base.html" %}

{% block title %}{{ title }} — Crunch Blog{% endblock %}

{% block content %}
  <article>
    <h2>{{ title }}</h2>
  </article>
{% endblock %}
"""

#: templates/404.html — the whole answer to this problem is six lines long,
#: because {% extends %} brings the header, nav and footer along for free.
NOT_FOUND_HTML: str = """\
{% extends "base.html" %}

{% block title %}Not found — Crunch Blog{% endblock %}

{% block content %}
  <h2>404 — nothing here</h2>
  <p>
    That page does not exist. It may have been a typo, or a post id that was
    never published (posts live in memory, so a restart clears them).
  </p>
  <p><a href="{{ url_for('index') }}">&larr; Back to all posts</a></p>
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {
        "base.html": BASE_HTML,
        "index.html": INDEX_HTML,
        "post.html": POST_HTML,
        "404.html": NOT_FOUND_HTML,
    }
)

POSTS: dict[int, str] = {
    1: "Hello, Flask",
    2: "Templates all the way down",
}


@app.route("/")
def index() -> str:
    """List every post title."""
    return render_template("index.html", posts=POSTS)


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    """Show one post, or 404 for an id that was never published."""
    if post_id not in POSTS:
        abort(404)
    return render_template("post.html", title=POSTS[post_id])


@app.errorhandler(404)
def page_not_found(error: Exception) -> tuple[str, int]:
    """Render the custom page AND keep the honest status code."""
    return render_template("404.html"), 404


def main() -> None:
    """Show every road to a 404 landing on the same page, status intact."""
    client = app.test_client()

    print(f"GET /            -> {client.get('/').status_code} (the happy path still works)")
    print(f"GET /post/1      -> {client.get('/post/1').status_code}")

    print()
    response = client.get("/post/9999")
    body = response.get_data(as_text=True)
    print(f"GET /post/9999   -> {response.status_code}")
    print(f"  the custom page rendered   : {'404 — nothing here' in body}")
    print(f"  it wears base.html's layout: {'Built with Flask.' in body}")

    print()
    print("Two 404s your code never sees, caught by the same handler:")
    print(f"  GET /post/seven -> {client.get('/post/seven').status_code} (the int converter rejected it before any view ran)")
    print(f"  GET /nonsense   -> {client.get('/nonsense').status_code} (no rule matched at all)")

    print()
    print("The bug this problem exists to prevent — a handler without ', 404':")
    careless: Flask = Flask("careless")

    @careless.route("/boom")
    def boom() -> str:
        abort(404)

    @careless.errorhandler(404)
    def whoops(error: Exception) -> str:  # <- returns a bare string: no ", 404"
        return "custom not found page"

    status = careless.test_client().get("/boom").status_code
    print(f"  GET /boom -> {status} (the page says not found; the status says everything is fine)")


if __name__ == "__main__":
    main()
```

**`abort(404)` raises `werkzeug.exceptions.NotFound`.** Flask catches it
while unwinding the request, looks for a handler registered for that status,
and calls yours instead of rendering its own stock page. The handler receives
the exception object — that is the `error` parameter, ignored here, honestly.

**The `, 404` is the entire problem.** A view returns either a body or a
`(body, status)` tuple, and `render_template` returns a plain string. Return
it bare from an error handler and Flask does what it does for any view: wraps
a string in a **200**. The careless app at the bottom of the file proves it —
`/boom` aborts with 404, the handler answers with a bare string, and the
client sees `200`. Always assert on the status, not on the words in the page.

**One handler covers 404s your code never produces.** `/post/seven` is
rejected by the `<int:>` converter before `show_post` is called, and
`/nonsense` matches no rule at all — both produce a `NotFound`, and both get
your page. That is why the handler registers on the *status code* and not on
any route.

**The template is six lines because of problem 2.** `{% extends
"base.html" %}` brings the header, footer, and stylesheet along; the check
`it wears base.html's layout: True` works by finding the footer string that
only exists in the base template. That is how you *prove* inheritance rather
than assert it.

## Download and run

Download
[problem-01-custom-404-page-solution.py](./problem-01-custom-404-page-solution.py)
and run it:

```bash
python problem-01-custom-404-page-solution.py
```

It needs Flask installed and nothing else, and it exits on its own — the
templates travel inside the file, so no folder is required. In your own blog
the same answer is the handler in `app.py` plus `templates/404.html`.

The `-solution` in the filename keeps this file from colliding with your own
`problem-01-custom-404-page.py`.

## Common bugs to catch

- **The custom page shows but `curl -i` says `200 OK`.** You dropped the
  `, 404` from the handler's return. There is no error, no warning, no red
  text — only the wrong status. The shipped file's careless app exists so
  you can see this one on purpose.

- **Nothing ever reaches your handler.** You wrote `@app.route("/404")`
  instead of `@app.errorhandler(404)`. A route is a page at a URL; a handler
  is a hook on a status code. Nothing redirects visitors to `/404` for you.

- **`jinja2.exceptions.TemplateNotFound: 404.html`.** In your blog, the file
  is not in `templates/`; in the single-file version, it is missing from the
  `DictLoader` dict. Worth knowing what happens next: with `debug=True` you
  see this traceback in the browser, because an exception *inside* an error
  handler is a new 500. With debug off you get Flask's stock 500 page and a
  mystery. Check the template's location first.

- **`TypeError: page_not_found() takes 0 positional arguments but 1 was
  given.`** Your handler's signature is `def page_not_found():`. Flask
  passes the exception object; accept it, even if you ignore it.

## Acceptance checklist

- [ ] `/post/9999` returns status **404** AND renders your custom page.
- [ ] The page extends `base.html` — the site footer appears on it.
- [ ] `/post/seven` and `/nonsense` land on the same page with the same
      status.
- [ ] Refreshing any *existing* page still works.
- [ ] You broke the handler on purpose once, read the `200`, and fixed it.

## Stretch

- Register an `@app.errorhandler(500)` with its own friendly template, then
  cause a 500 on purpose (divide by zero in a view) with debug **off** and
  watch your page appear instead of Flask's stock one. With debug **on**
  the interactive traceback wins — which is one more reason debug never
  ships.
- Make the 404 page more useful: list the three most recent posts, so a
  visitor who followed a dead link has somewhere to go. The handler can pass
  context to `render_template` exactly like a view can.
- Read the exception parameter instead of ignoring it:
  `error.description` holds Werkzeug's human-readable explanation. Log it
  with `app.logger.info(...)` and watch your terminal on each 404.
