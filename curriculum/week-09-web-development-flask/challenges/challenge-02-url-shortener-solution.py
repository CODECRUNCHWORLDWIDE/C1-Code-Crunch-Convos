"""challenge-02-url-shortener-solution.py — the URL shortener, proven headless.

The app is the challenge skeleton plus one change: `shorten` also stashes the
short link in the session so `index` can show it as a clickable `<a>`, not
just flash it as text. The two templates are the part you had to write, and
they are here in full — the stylesheet lives in a `<style>` block in
`base.html`, because a two-page app does not need a `static/` folder yet.

Your own build ends in ``app.run(debug=True)`` and you follow slugs in a
browser. This download drives the app with ``app.test_client()`` — Flask's
in-process fake browser — walks the acceptance checklist, prints each round
trip, and exits. The slugs are minted by ``secrets``, so they differ on every
run; the printout therefore reports facts about the slug (length, alphabet)
rather than the slug itself.

Run it with::

    python challenge-02-url-shortener-solution.py
"""

import secrets
import string
from urllib.parse import urlparse

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)
from jinja2 import DictLoader

#: templates/base.html — layout, flash widget, and the whole stylesheet.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Crunch Links{% endblock %}</title>
    <style>
      * { box-sizing: border-box; }
      body {
        font-family: system-ui, -apple-system, sans-serif;
        max-width: 40rem; margin: 2rem auto; padding: 0 1rem;
        color: #222; background: #fafafa; line-height: 1.6;
      }
      header h1 a { color: #222; text-decoration: none; }
      form.shorten { display: flex; flex-wrap: wrap; gap: 0.5rem; }
      form.shorten label { flex: 0 0 100%; font-weight: 600; }
      input[type="url"] { flex: 1 1 16rem; padding: 0.5rem; font: inherit; }
      button { padding: 0.4rem 0.75rem; font: inherit; cursor: pointer;
               border: 1px solid #ccc; border-radius: 0.25rem; background: #fff; }
      ul.flashes { list-style: none; padding: 0; }
      .flash { padding: 0.5rem 0.75rem; border-radius: 0.25rem; margin: 0.25rem 0;
               word-break: break-all; }
      .flash-success { background: #d4edda; color: #155724; }
      .flash-error { background: #f8d7da; color: #721c24; }
      .short { font-size: 1.1rem; word-break: break-all; }
      footer { margin-top: 3rem; color: #666; font-size: 0.875rem; }
    </style>
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">Crunch Links</a></h1>
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
      <small>In memory only. A restart forgets every link.</small>
    </footer>
  </body>
</html>
"""

#: templates/index.html — the form, plus the freshly minted link when there is one.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block title %}Shorten a URL — Crunch Links{% endblock %}

{% block content %}
  <form class="shorten" method="post" action="{{ url_for('shorten') }}">
    <label for="url">Long URL</label>
    <input type="url" id="url" name="url" maxlength="2000"
           placeholder="https://example.com/a/very/long/path" required autofocus>
    <button type="submit">Shorten</button>
  </form>

  {% if last_short %}
    <p class="short">
      Your short link: <a href="{{ last_short }}">{{ last_short }}</a>
    </p>
  {% endif %}
{% endblock %}
"""

app = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "index.html": INDEX_HTML})
app.secret_key = "dev-only-change-me"

ALPHABET = string.ascii_letters + string.digits
LINKS: dict[str, str] = {}


def new_slug(length: int = 6) -> str:
    """Generate a slug that is not already taken."""
    while True:
        s = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if s not in LINKS:
            return s


def looks_like_url(s: str) -> bool:
    """True for http(s) URLs with a host, under 2000 characters."""
    if not s or len(s) > 2000:
        return False
    parts = urlparse(s)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)


@app.route("/")
def index() -> str:
    # pop, not get: the link is shown once, like a flash. It lives in the
    # session so it is per-browser -- a module-level global would show your
    # link to every other visitor.
    return render_template("index.html", last_short=session.pop("last_short", None))


@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form.get("url", "").strip()
    if not looks_like_url(long_url):
        flash("Please enter a valid http:// or https:// URL.", "error")
        return redirect(url_for("index"))

    slug = new_slug()
    LINKS[slug] = long_url
    short = url_for("follow", slug=slug, _external=True)
    session["last_short"] = short
    flash(f"Short URL: {short}", "success")
    return redirect(url_for("index"))


@app.route("/<slug>")
def follow(slug: str):
    long_url = LINKS.get(slug)
    if long_url is None:
        abort(404)
    return redirect(long_url)


def main() -> None:
    """Walk the acceptance checklist and print what each round trip proved."""
    client = app.test_client()

    response = client.get("/")
    print(f"GET  /        -> {response.status_code} (the form)")

    print()
    response = client.post("/shorten", data={"url": "https://example.com"})
    print(f"POST /shorten url='https://example.com' -> {response.status_code}  Location: {response.headers['Location']}")
    slug, target = next(iter(LINKS.items()))
    body = client.get("/").get_data(as_text=True)
    print(f"  links stored          : {len(LINKS)}")
    print(f"  slug length           : {len(slug)}")
    print(f"  slug is base62        : {all(c in ALPHABET for c in slug)}")
    print(f"  it maps to the URL    : {target == 'https://example.com'}")
    print(f"  the flash shows it    : {f'Short URL: http://localhost/{slug}' in body}")
    print(f"  the link is clickable : {f'href=\"http://localhost/{slug}\"' in body}")
    print(f"  a refresh repeats it  : {f'/{slug}' in client.get('/').get_data(as_text=True)}")
    print(f"  ...or mints a new one : {len(LINKS) != 1}")

    print()
    response = client.get(f"/{slug}")
    print(f"GET  /<that slug> -> {response.status_code}  Location: {response.headers['Location']}")
    print(f"GET  /nope404     -> {client.get('/nope404').status_code}")

    print()
    print("Garbage in, flash out, nothing stored:")
    for bad in ("", "   ", "not-a-url", "javascript:alert(1)", "ftp://example.com",
                "https://" + "x" * 2000):
        before = len(LINKS)
        response = client.post("/shorten", data={"url": bad}, follow_redirects=True)
        rejected = ("Please enter a valid" in response.get_data(as_text=True)
                    and len(LINKS) == before)
        print(f"  rejected {bad[:24]!r:28} -> {rejected}")

    print()
    print("Routing edges:")
    print(f"  GET  /shorten -> {client.get('/shorten').status_code} (matched /<slug>, found no such slug)")
    print(f"  POST /        -> {client.post('/').status_code}")

    print()
    for _ in range(200):
        client.post("/shorten", data={"url": "https://example.org/x"})
    print(f"200 more shortens -> {len(LINKS)} links, zero collisions")


if __name__ == "__main__":
    main()
