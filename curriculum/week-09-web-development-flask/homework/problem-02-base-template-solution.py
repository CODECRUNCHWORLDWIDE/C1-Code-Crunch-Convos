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
