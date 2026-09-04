# Homework Problem 2 — Base template

> **Topic:** `{% extends %}` / `{% block %}` inheritance, `{% include %}` partials, and one layout worn by every page
> **Lecture:** [02 — Templates and Static Files](../lecture-notes/02-templates-and-static.md)
> **Difficulty:** Beginner
> **Target time:** 1 hour
> **Why this one:** duplication in templates is not a style problem, it is a time bomb — change the nav in five files and you will miss one. This refactor is also what makes every later problem cheap: the custom 404 is six lines, the login link is a two-line nav change, and a whole new page is one file plus two block overrides. Extract the layout the moment there are two pages.

## The Brief

If you have not already done this in the mini-project, extract a `base.html`
and refactor `index.html` and `post.html` to extend it. Move the doctype and
`<head>`, the `<header>` with its `<nav>`, the flash-messages widget, and
the `<footer>` into the base template, so each of those exists in **exactly
one file**.

The rule that makes inheritance work is also the one that trips people:
in a template that extends another, **only block contents are rendered**.
Anything you write outside a block is silently discarded — no error, no
warning. The shipped file proves this on a page built to trigger it.

This is a refactor of your mini-project blog. The shipped file beside this
page is a self-contained slice of that blog after the refactor, so the
finished shape runs anywhere as one file.

## Starter

Save as `problem-02-base-template.py`. It runs as pasted and renders two
pages — but every template carries its own full layout, which is the disease
this problem cures. Your job is the refactor described in the `TODO`s.

```python
"""problem-02-base-template.py — starter: two pages, two copies of the layout.

Run with: python problem-02-base-template.py
"""

import os

from flask import Flask, render_template
from jinja2 import DictLoader

# TODO 1: write BASE_HTML holding everything true of every page — doctype,
#         head with a {% block title %} default, header + nav, a
#         {% include "_flashes.html" %}, {% block content %}, footer.
# TODO 2: write FLASHES_HTML as a partial holding the get_flashed_messages
#         loop, and register it as "_flashes.html".
# TODO 3: shrink both page templates below to {% extends "base.html" %} plus
#         a title block and a content block. Nothing else survives.

INDEX_HTML: str = """\
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Crunch Blog</title></head>
  <body>
    <header><h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1></header>
    <main>
      <h2>Latest posts</h2>
      <p><a href="{{ url_for('show_post') }}">Hello, Flask</a></p>
    </main>
    <footer><small>Built with Flask. Posts live in memory until Week 10.</small></footer>
  </body>
</html>
"""

POST_HTML: str = """\
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Hello, Flask — Crunch Blog</title></head>
  <body>
    <header><h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1></header>
    <main>
      <article>
        <h2>Hello, Flask</h2>
        <p>The first post. This layout is a copy — that is the bug.</p>
      </article>
    </main>
    <footer><small>Built with Flask. Posts live in memory until Week 10.</small></footer>
  </body>
</html>
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"index.html": INDEX_HTML, "post.html": POST_HTML})
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/post/1")
def show_post() -> str:
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

In your own blog this is the same refactor across real files:
`templates/base.html` and `templates/_flashes.html` appear, and every page
template shrinks to extends-plus-blocks.

## Requirements

1. `base.html` contains the `<!doctype html>`, `<head>`, header, nav, flash
   widget, and footer — each exactly once in the whole project.
2. `index.html` and `post.html` each contain only `{% extends "base.html" %}`,
   a `{% block title %}` where they need one, and their `{% block content %}`.
3. The `title` block has a default in the base, so a page that never
   overrides it still gets a sensible tab label.
4. The flash widget renders on every page, from the layout — queue a flash on
   any route and it shows wherever the browser lands next, once.
5. Adding a new page is one new file plus two block overrides.

## Constraints

- **Count the doctypes.** `grep -c "doctype" templates/*.html` — exactly one
  file may be non-zero. Two doctypes means two layouts, which means the
  refactor is not done.
- **The flash widget is an `{% include %}`, not a copy.** `extends` is "this
  page *is a* layout" — one per template, restructuring the whole file.
  `include` is "paste this fragment here" — as many as you like. The widget
  is a fragment reused inside one layout; the layout is the shape of every
  page. The leading underscore in `_flashes.html` is the convention that says
  "partial, not a page", so nobody goes looking for its route.
- **Everything a child renders must be inside a block.** Content between
  `{% extends %}` and the first block is discarded silently. This is not an
  edge case; it is the number-one source of "why does my paragraph never
  appear" in template inheritance, and the shipped file demonstrates it.
- **No hard-coded `href="/post/1"` anywhere.** `url_for` re-derives every
  URL from the route table at render time; a literal path is silently wrong
  the day the route changes.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-02-base-template.py
GET /       -> 200
  doctype count in the page : 1
  footer from base.html     : True
  title (the default block) : <title>Crunch Blog</title>
GET /post/1 -> 200
  footer from base.html     : True
  title (overridden)        : <title>Hello, Flask — Crunch Blog</title>

Templates carrying their own <!doctype html>: 1 of 5
  (only base.html — every other file is extends plus blocks)

The trap — in a child template, content outside a block is dropped:
  'OUTSIDE ANY BLOCK' reached the page: False
  <p>Inside the block. Only this line reaches the page.</p>

The flash widget lives in the layout, so every page renders it once:
  POST /ping -> 302  Location: /
  <li class="flash flash-success">Pong.</li>
  shown again on the next page: False
```

## Steps

1. Write `base.html`: doctype, head with
   `{% block title %}Crunch Blog{% endblock %}`, header and nav, the
   `{% include "_flashes.html" %}`, `{% block content %}{% endblock %}`,
   footer.
2. Pull the `get_flashed_messages` loop into `_flashes.html`.
3. Rewrite `index.html`: delete everything except what is unique to the
   page, wrap that in `{% block content %}`, and put
   `{% extends "base.html" %}` on line one.
4. Same for `post.html`, adding its `{% block title %}` override.
5. Load both pages. View source on each and count doctypes — one per page,
   and the page-specific title on `/post/1`.
6. Trigger the trap on purpose: put a `<p>` between `{% extends %}` and the
   first block, reload, and confirm it silently vanishes. Remove it.
7. In your blog: `grep -c "doctype" templates/*.html` and confirm only
   `base.html` is non-zero.

## The Solution

```python
"""problem-02-base-template-solution.py — one layout, worn by every page.

The blog's templates, refactored so that everything true of every page —
doctype, head, header, nav, flash widget, footer — lives in ``base.html``
exactly once, and each page is nothing but ``{% extends %}`` plus two block
overrides.

Your own build keeps these in a `templates/` folder. This download carries
the same text in constants, handed to Jinja through a ``DictLoader``, so one
file runs anywhere. It drives the app with ``app.test_client()`` — Flask's
in-process fake browser — and prints the proof that the layout exists once,
that pages inherit it, and that the classic trap (content outside a block)
really is silently discarded.

Run it with::

    python problem-02-base-template-solution.py
"""

import os

from flask import Flask, Response, flash, redirect, render_template, url_for
from jinja2 import DictLoader

#: templates/base.html — the one and only layout.
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
      </nav>
    </header>

    <main>
      {% include "_flashes.html" %}
      {% block content %}{% endblock %}
    </main>

    <footer>
      <small>Built with Flask. Posts live in memory until Week 10.</small>
    </footer>
  </body>
</html>
"""

#: templates/_flashes.html — the flash widget, pulled out as a partial. The
#: leading underscore is a convention: a fragment, not a page.
FLASHES_HTML: str = """\
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class="flashes">
      {% for category, message in messages %}
        <li class="flash flash-{{ category }}">{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
"""

#: templates/index.html — extends, two blocks, nothing else.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>
  <p><a href="{{ url_for('show_post') }}">Hello, Flask</a></p>
{% endblock %}
"""

#: templates/post.html — a whole page in twelve lines.
POST_HTML: str = """\
{% extends "base.html" %}

{% block title %}Hello, Flask — Crunch Blog{% endblock %}

{% block content %}
  <article>
    <h2>Hello, Flask</h2>
    <p>The first post. The layout around it came from base.html.</p>
    <p><a href="{{ url_for('index') }}">&larr; Back to all posts</a></p>
  </article>
{% endblock %}
"""

#: templates/stray.html — the trap, kept on purpose so the demo below can
#: prove it: in a template that extends, content outside a block is DROPPED.
STRAY_HTML: str = """\
{% extends "base.html" %}
<p>OUTSIDE ANY BLOCK — this paragraph is silently discarded.</p>
{% block content %}
  <p>Inside the block. Only this line reaches the page.</p>
{% endblock %}
"""

TEMPLATES: dict[str, str] = {
    "base.html": BASE_HTML,
    "_flashes.html": FLASHES_HTML,
    "index.html": INDEX_HTML,
    "post.html": POST_HTML,
    "stray.html": STRAY_HTML,
}

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(TEMPLATES)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")


@app.route("/")
def index() -> str:
    """The blog index, wearing the layout."""
    return render_template("index.html")


@app.route("/post/1")
def show_post() -> str:
    """One post, wearing the same layout with its own title."""
    return render_template("post.html")


@app.route("/stray")
def stray() -> str:
    """The trap page, kept so the demo can show what extends drops."""
    return render_template("stray.html")


@app.route("/ping", methods=["POST"])
def ping() -> Response:
    """Queue a flash and redirect — the layout renders it, once."""
    flash("Pong.", "success")
    return redirect(url_for("index"))


def line_with(page: str, needle: str) -> str:
    """Return the first line of *page* containing *needle*, stripped."""
    for line in page.splitlines():
        if needle in line:
            return line.strip()
    return f"(no line contains {needle!r})"


def main() -> None:
    """Prove the layout is defined once, inherited everywhere, and consumed right."""
    client = app.test_client()

    body = client.get("/").get_data(as_text=True)
    print("GET /       -> 200")
    print(f"  doctype count in the page : {body.count('<!doctype html>')}")
    print(f"  footer from base.html     : {'Built with Flask.' in body}")
    print(f"  title (the default block) : {line_with(body, '<title>')}")

    body = client.get("/post/1").get_data(as_text=True)
    print("GET /post/1 -> 200")
    print(f"  footer from base.html     : {'Built with Flask.' in body}")
    print(f"  title (overridden)        : {line_with(body, '<title>')}")

    print()
    doctypes = sum("<!doctype html>" in text for text in TEMPLATES.values())
    print(f"Templates carrying their own <!doctype html>: {doctypes} of {len(TEMPLATES)}")
    print("  (only base.html — every other file is extends plus blocks)")

    print()
    print("The trap — in a child template, content outside a block is dropped:")
    body = client.get("/stray").get_data(as_text=True)
    print(f"  'OUTSIDE ANY BLOCK' reached the page: {'OUTSIDE ANY BLOCK' in body}")
    print(f"  {line_with(body, 'Inside the block')}")

    print()
    print("The flash widget lives in the layout, so every page renders it once:")
    response = client.post("/ping")
    print(f"  POST /ping -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/").get_data(as_text=True)
    print(f"  {line_with(body, 'class=\"flash ')}")
    body = client.get("/").get_data(as_text=True)
    print(f"  shown again on the next page: {'class=\"flash ' in body}")


if __name__ == "__main__":
    main()
```

**Inheritance runs parent-first.** When you render `post.html`, Jinja loads
`base.html`, walks *its* structure, and substitutes the child's blocks
wherever the parent defined one. A child template is not "the base plus your
HTML" — it is a set of *overrides*. Which is exactly why content outside a
block is discarded: the parent decides the structure, and anything the child
writes outside an override point has nowhere to go. The `stray.html` demo
makes this visible.

**`{% block title %}Crunch Blog{% endblock %}` gives you a default.** A page
that never overrides `title` gets `Crunch Blog` and still has a sensible tab
label — the first output block shows both the default and an override.
Blocks are override points with fallbacks, not required slots.

**`{% include %}` and `{% extends %}` are not competitors.** `extends` is
"this page *is a* layout" — one per template. `include` is "paste this
fragment here" — as many as you like. The flash widget is an `include`
because it is a fragment reused inside one layout; the layout is an
`extends` because it is the shape of every page.

**The flash widget in the layout means every page consumes the queue.**
`POST /ping` queues a flash and redirects; the next page renders it, and the
page after shows nothing — reading the queue empties it. Render the widget
in only one page template and flashes queued on the way to any other page
pile up unread, then dump out somewhere surprising.

**The payoff is measurable.** `404.html` (problem 1), `tag.html`
(problem 4), and `login.html` (problem 6) are all added later as one file
plus two block overrides — none contains a `<html>` tag, a stylesheet link,
or a nav. That is requirement 5, checked by living it.

## Run it

Copy the worked answer on this page into `problem-02-base-template.py` and run it:

```bash
python problem-02-base-template.py
```

It needs Flask installed and nothing else, and it exits on its own. In your
own blog the same refactor lands as `templates/base.html`,
`templates/_flashes.html`, and page templates shrunk to extends-plus-blocks.

The `-solution` in the filename keeps this file from colliding with your own
`problem-02-base-template.py`.

## Common bugs to catch

- **A paragraph in a child template never appears, with no error.** It sits
  outside every block. In a template that extends another, only block
  contents render. Move it inside `{% block content %}`.

- **`jinja2.exceptions.TemplateNotFound: base.html`.** The child's
  `{% extends "base.html" %}` names a file that is not in `templates/` (or,
  single-file version, not in the `DictLoader` dict). The message names the
  file it wanted; check its exact spelling and location.

- **The nav changed on four pages and not the fifth.** You copied the layout
  into every page "just for now" instead of extracting it. This is the exact
  failure the refactor exists to prevent, and the doctype grep is how you
  prove it cannot happen again.

- **Flashes pile up and dump out on the wrong page.** The
  `get_flashed_messages` loop lives in one page template instead of the
  layout. Read the queue once, in `base.html`, on every page.

- **`{% extends base.html %}` (no quotes) raises
  `jinja2.exceptions.UndefinedError`.** The template name is a string.
  Quote it.

## Acceptance checklist

- [ ] `base.html` holds doctype, head, header, nav, flash widget, footer —
      once each.
- [ ] `index.html` and `post.html` are extends plus blocks, nothing else.
- [ ] `grep -c "doctype" templates/*.html` is non-zero for exactly one file.
- [ ] A flash queued on any route renders once, on the next page, wherever
      that is.
- [ ] You triggered the outside-a-block trap on purpose and watched the
      content vanish.

## Stretch

- Add a third page — an "About" page — and time yourself. If the refactor is
  right, it is one file, two blocks, one route, and under five minutes.
- Add a `{% block extra_head %}{% endblock %}` to the base just before
  `</head>`, and use it from one page to add a page-specific `<meta>` tag.
  Empty blocks in the parent cost nothing and buy per-page extension points.
- Read about `{{ super() }}`: a child block that wants to *add to* the
  parent's default rather than replace it calls `super()` first. Try it on
  the title block.
