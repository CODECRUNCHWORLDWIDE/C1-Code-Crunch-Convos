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
