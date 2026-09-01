"""problem-04-post-tags-solution.py — tags on posts, cleaned once at the boundary.

The blog's `Post` gains a ``tags`` field, the create form gains one text
input, and all the real work happens in ``parse_tags``: split on commas,
strip, lowercase, drop empties, de-duplicate — once, on the way in. From then
on every tag in the system is already clean, so `/tag/python` is a plain
membership test and the pills always agree with the URLs.

Templates travel inside the file via a ``DictLoader``; the app is driven by
``app.test_client()`` — Flask's in-process fake browser — instead of
``app.run()``.

Run it with::

    python problem-04-post-tags-solution.py
"""

import os
import re
from dataclasses import dataclass, field
from itertools import count

from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for
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

#: templates/index.html — titles with tag pills underneath.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>
  {% for post in posts %}
    <article>
      <h3>{{ post.title }}</h3>
      {% if post.tags %}
        <p class="tags">
          {% for tag in post.tags %}
            <a class="pill" href="{{ url_for('show_tag', tag=tag) }}">{{ tag }}</a>
          {% endfor %}
        </p>
      {% endif %}
    </article>
  {% else %}
    <p>No posts yet.</p>
  {% endfor %}
  <p><a href="{{ url_for('new_post') }}">New post</a></p>
{% endblock %}
"""

#: templates/new.html — the create form, now with a tags field.
NEW_HTML: str = """\
{% extends "base.html" %}

{% block title %}New post — Crunch Blog{% endblock %}

{% block content %}
  <h2>New post</h2>
  <form method="post" action="{{ url_for('new_post') }}">
    <label for="title">Title</label>
    <input type="text" id="title" name="title" value="{{ title }}" maxlength="120" required>

    <label for="body">Body</label>
    <textarea id="body" name="body" rows="8" required>{{ body }}</textarea>

    <label for="tags">Tags <span class="hint">(comma separated)</span></label>
    <input type="text" id="tags" name="tags" value="{{ tags }}" placeholder="python, flask, web">

    <button type="submit">Publish</button>
  </form>
{% endblock %}
"""

#: templates/tag.html — every post carrying one tag.
TAG_HTML: str = """\
{% extends "base.html" %}

{% block title %}Posts tagged '{{ tag }}' — Crunch Blog{% endblock %}

{% block content %}
  <h2>Posts tagged <span class="pill">{{ tag }}</span></h2>
  <p>{{ posts|length }} post{{ '' if posts|length == 1 else 's' }}.</p>
  {% for post in posts %}
    <article><h3>{{ post.title }}</h3></article>
  {% endfor %}
  <p><a href="{{ url_for('index') }}">&larr; Back to all posts</a></p>
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {
        "base.html": BASE_HTML,
        "index.html": INDEX_HTML,
        "new.html": NEW_HTML,
        "tag.html": TAG_HTML,
    }
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

_id_seq = count(1)


@dataclass
class Post:
    """One blog post. `tags` is this problem's new field."""

    id: int
    title: str
    body: str
    tags: list[str] = field(default_factory=list)


POSTS: list[Post] = []


def parse_tags(raw: str) -> list[str]:
    """Split a comma-separated tag field into clean, unique, lowercase tags.

    `"Python, flask ,, PYTHON"` -> `["python", "flask"]`.
    """
    seen: list[str] = []
    for chunk in raw.split(","):
        tag = chunk.strip().lower()
        if tag and tag not in seen:
            seen.append(tag)
    return seen


@app.route("/")
def index() -> str:
    """List posts, newest first, pills under each title."""
    return render_template("index.html", posts=list(reversed(POSTS)))


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str | Response:
    """Create a post; the tags arrive as one comma-separated string."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        raw_tags = request.form.get("tags", "")

        if not title or not body:
            flash("Title and body are both required.", "error")
            # Re-render with the RAW string the user typed, not the parsed list.
            return render_template("new.html", title=title, body=body, tags=raw_tags)

        POSTS.append(Post(next(_id_seq), title=title, body=body, tags=parse_tags(raw_tags)))
        flash("Post published.", "success")
        return redirect(url_for("index"))

    return render_template("new.html", title="", body="", tags="")


@app.route("/tag/<tag>")
def show_tag(tag: str) -> str:
    """List every post carrying `tag`. 404 when nothing matches."""
    wanted = tag.strip().lower()
    matches = [p for p in reversed(POSTS) if wanted in p.tags]
    if not matches:
        abort(404)
    return render_template("tag.html", tag=wanted, posts=matches)


def main() -> None:
    """Show the parser's decisions, then the routes built on top of them."""
    client = app.test_client()

    print("parse_tags at work:")
    for raw in ("Python, flask ,, PYTHON", "  web , WEB,web ", ""):
        print(f"  {raw!r:28} -> {parse_tags(raw)}")

    print()
    response = client.post(
        "/new",
        data={"title": "Tag soup", "body": "Three tags, typed sloppily.",
              "tags": "Python, flask ,, PYTHON, web"},
    )
    print(f"POST /new tags='Python, flask ,, PYTHON, web' -> {response.status_code}")
    print(f"  stored on the post: {POSTS[0].tags}")

    body = client.get("/").get_data(as_text=True)
    pills = re.findall(r'class="pill" href="([^"]+)"', body)
    print(f"  pills on the index link to: {pills}")

    print()
    response = client.get("/tag/python")
    print(f"GET /tag/python -> {response.status_code}")
    print(f"  the page counts: {'1 post.' in response.get_data(as_text=True)}")
    print(f"GET /tag/PYTHON -> {client.get('/tag/PYTHON').status_code} (normalised on the way in)")
    print(f"GET /tag/zzz    -> {client.get('/tag/zzz').status_code}")


if __name__ == "__main__":
    main()
