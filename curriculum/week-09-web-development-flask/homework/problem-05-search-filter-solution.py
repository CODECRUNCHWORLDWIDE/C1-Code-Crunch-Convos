"""problem-05-search-filter-solution.py — a search box that is just a GET form.

The whole trick is `method="get"` with one field named `q`: the browser
serialises the form into `/?q=flask`, the view filters before rendering, and
the URL becomes the search — bookmarkable, shareable, refresh-safe. No POST,
no redirect, no session.

Two variables on purpose: the raw query goes back to the user in the heading
exactly as typed; the lowered copy does the matching. Templates travel inside
the file via a ``DictLoader``; the app is driven by ``app.test_client()`` —
Flask's in-process fake browser — instead of ``app.run()``.

Run it with::

    python problem-05-search-filter-solution.py
"""

from dataclasses import dataclass

from flask import Flask, render_template, request
from jinja2 import DictLoader

#: templates/base.html
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
  </body>
</html>
"""

#: templates/index.html — the search form, the heading, and the empty state.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block title %}
  {%- if q -%}
    Search results for '{{ q }}' ({{ total }} found)
  {%- else -%}
    Home — Crunch Blog
  {%- endif -%}
{% endblock %}

{% block content %}
  <form class="search" method="get" action="{{ url_for('index') }}">
    <label for="q">Search</label>
    <input type="search" id="q" name="q" placeholder="title or body"
           value="{{ request.args.get('q', '') }}">
    <button type="submit">Search</button>
    {% if q %}<a href="{{ url_for('index') }}">Clear</a>{% endif %}
  </form>

  {% if q %}
    <h2>Search results for '{{ q }}' ({{ total }} found)</h2>
  {% else %}
    <h2>Latest posts</h2>
  {% endif %}

  {% for post in posts %}
    <article>
      <h3>{{ post.title }}</h3>
      <p>{{ post.body }}</p>
    </article>
  {% else %}
    <p>{% if q %}Nothing matched that search.{% else %}No posts yet.{% endif %}</p>
  {% endfor %}
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "index.html": INDEX_HTML})


@dataclass
class Post:
    """One blog post — just enough of it to search."""

    id: int
    title: str
    body: str


POSTS: list[Post] = [
    Post(1, "Hello, Flask", "A first look at routes and view functions."),
    Post(2, "Jinja loops", "Rendering a list with {% for %} and friends."),
    Post(3, "Week 10 preview", "The posts move into SQLite and survive restarts."),
]


@app.route("/")
def index() -> str:
    """List posts, filtered by `?q=` when one is given."""
    # The raw value is what we echo back to the user; the lowered copy is what
    # we search with. Keeping them separate means the heading shows exactly
    # what was typed.
    raw_q = request.args.get("q", "").strip()
    needle = raw_q.lower()

    matches = list(reversed(POSTS))
    if needle:
        matches = [
            p for p in matches
            if needle in p.title.lower() or needle in p.body.lower()
        ]

    return render_template("index.html", posts=matches, q=raw_q, total=len(matches))


def line_with(page: str, needle: str) -> str:
    """Return the first line of *page* containing *needle*, stripped."""
    for line in page.splitlines():
        if needle in line:
            return line.strip()
    return f"(no line contains {needle!r})"


def main() -> None:
    """Search every way a visitor might — including the hostile ways."""
    client = app.test_client()

    body = client.get("/").get_data(as_text=True)
    print("GET /                -> 200 (no query: everything shows)")
    print(f"  {line_with(body, '<h2>')}")
    print(f"  posts on the page  : {body.count('<article>')}")

    response = client.get("/?q=flask")
    body = response.get_data(as_text=True)
    print(f"GET /?q=flask        -> {response.status_code}")
    print(f"  {line_with(body, '<h2>')}")
    print(f"  posts on the page  : {body.count('<article>')}")
    print(f"  the box keeps the typing: {'value=\"flask\"' in body}")

    response = client.get("/?q=JINJA")
    body = response.get_data(as_text=True)
    print(f"GET /?q=JINJA        -> {response.status_code} (case-insensitive, both sides)")
    print(f"  {line_with(body, '<h2>')}")

    response = client.get("/?q=")
    body = response.get_data(as_text=True)
    print(f"GET /?q=             -> {response.status_code} (empty query: everything again)")
    print(f"  posts on the page  : {body.count('<article>')}")

    print()
    print("Hostile input, no traceback, nothing executed:")
    response = client.get("/?q=<script>alert(1)</script>")
    body = response.get_data(as_text=True)
    print(f"  GET /?q=<script>alert(1)</script> -> {response.status_code}")
    print(f"  {line_with(body, '<h2>')}")
    print(f"  raw <script> reached the page: {'<script>' in body}")
    response = client.get("/?q=Zoë")
    print(f"  GET /?q=Zoë -> {response.status_code} (unicode is just text)")


if __name__ == "__main__":
    main()
