# Homework Problem 4 — Post tags

> **Topic:** a `list[str]` field on a dataclass, cleaning typed-in text once at the boundary, a dynamic `/tag/<tag>` route, and `abort(404)`
> **Lecture:** [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Intermediate
> **Target time:** 1.5 hours
> **Why this one:** people type messily and they always will. `Python`, `python `, `PYTHON` and `python` are one idea and four different strings, and if you let all four into your data you will spend the rest of the week comparing them. Clean the text **once**, at the door, and every page downstream gets simple. That habit — normalise at the boundary — is the same one that keeps email addresses, usernames, and search queries from rotting later.

## The Brief

Think of a library. Every book gets little coloured stickers on the spine —
*mystery*, *space*, *funny* — and you can walk to a shelf and pull every
book with the same sticker. Tags are those stickers, and `/tag/python` is
the walk to the shelf.

Your blog post is going to grow a `tags` field: a list of short words. The
person writing a post types them into one plain text box, separated by
commas, because that is what humans do:

```text
Python, flask ,, PYTHON, web
```

That is one string, and it is a mess. Look at what is wrong with it: a
capital `P` on the first tag, a stray space before a comma, two commas in a
row with nothing between them, and `PYTHON` which is the same tag as
`Python` wearing a different hat.

Your job is to turn that one messy string into a clean list, on the server,
the moment it arrives:

```text
["python", "flask", "web"]
```

Split on the commas. Trim the spaces off each piece. Lowercase it. Throw
away the empty pieces. Keep only the first copy of anything repeated. Do all
of that **once**, before the post is saved — so from then on, every tag
already stored in your blog is guaranteed clean, and the rest of the app
never has to think about it again.

Then use it. Print each tag as a small pill under the post title, make each
pill a link, and add a route `GET /tag/<tag>` that lists every post carrying
that tag. If no post carries it, that page is a 404 — the shelf does not
exist.

This is a change to your mini-project blog. The file shipped beside this
page is a self-contained slice of that blog with the change already made, so
the finished shape runs anywhere as one file.

## Starter

Save as `problem-04-post-tags.py`. It runs as pasted — a tiny blog that creates
posts and lists them, with no tags anywhere. Your job is the five `TODO`s.

```python
"""problem-04-post-tags.py — starter: the blog, one step before tags.

Run with: python problem-04-post-tags.py
"""

import os
from dataclasses import dataclass
from itertools import count

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from jinja2 import DictLoader

# TODO 1: give Post a `tags` field: `tags: list[str] = field(default_factory=list)`.
#         Import `field` from dataclasses. Never write `= []` here.
# TODO 2: write parse_tags(raw) -> list[str]: split on commas, strip each piece,
#         lowercase it, drop the empty ones, keep the typed order, no repeats.
# TODO 3: add a `tags` text input to NEW_HTML, and read it in new_post() with
#         request.form.get("tags", ""). Store parse_tags(raw_tags) on the Post.
# TODO 4: under each title in INDEX_HTML, print one pill per tag, linking to
#         url_for('show_tag', tag=tag).
# TODO 5: add the /tag/<tag> route and a tag.html template. Lowercase the tag
#         from the URL, collect the posts carrying it, and abort(404) if none do.

BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <header><h1><a href="{{ url_for('index') }}">Crunch Blog</a></h1></header>
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
  {% for post in posts %}
    <article><h3>{{ post.title }}</h3></article>
  {% else %}
    <p>No posts yet.</p>
  {% endfor %}
  <p><a href="{{ url_for('new_post') }}">New post</a></p>
{% endblock %}
"""

NEW_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>New post</h2>
  <form method="post" action="{{ url_for('new_post') }}">
    <label for="title">Title</label>
    <input type="text" id="title" name="title" value="{{ title }}" required>

    <label for="body">Body</label>
    <textarea id="body" name="body" rows="8" required>{{ body }}</textarea>

    <button type="submit">Publish</button>
  </form>
{% endblock %}
"""

app: Flask = Flask(__name__)
app.jinja_loader = DictLoader(
    {"base.html": BASE_HTML, "index.html": INDEX_HTML, "new.html": NEW_HTML}
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")

_id_seq = count(1)


@dataclass
class Post:
    """One blog post. It has no tags yet — that is TODO 1."""

    id: int
    title: str
    body: str


POSTS: list[Post] = []


@app.route("/")
def index() -> str:
    return render_template("index.html", posts=list(reversed(POSTS)))


@app.route("/new", methods=["GET", "POST"])
def new_post() -> str | Response:
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            flash("Title and body are both required.", "error")
            return render_template("new.html", title=title, body=body)
        POSTS.append(Post(next(_id_seq), title=title, body=body))
        flash("Post published.", "success")
        return redirect(url_for("index"))
    return render_template("new.html", title="", body="")


def main() -> None:
    """Drive the app with Flask's in-process fake browser."""
    client = app.test_client()
    response = client.post("/new", data={"title": "Tag soup", "body": "No tags yet."})
    print(f"POST /new -> {response.status_code}")
    print(f"  stored: {POSTS[0]}")
    print(f"GET /    -> {client.get('/').status_code}")


if __name__ == "__main__":
    main()
```

In your own blog this is the same change across real files: `Post` grows a
field, `templates/new.html` grows one input, `templates/index.html` grows
the pill loop, and `templates/tag.html` appears as a new page.

## Requirements

1. `Post` has a `tags: list[str]` field, declared with
   `field(default_factory=list)`, so a post created without tags gets its
   own empty list.
2. The create-post form has an `<input name="tags">` and a label that tells
   the writer the tags are comma separated.
3. `parse_tags(raw)` turns the raw string into clean tags: split on `,`,
   strip whitespace, lowercase, drop empties, drop repeats, keep the typed
   order. It is a plain function of a string, so you can test it without a
   browser.
4. Creating a post with `python, flask, web` saves exactly three tags.
5. The blog index shows a pill under each title, one per tag, each pill a
   link built with `url_for('show_tag', tag=tag)`.
6. `GET /tag/<tag>` lists only the posts carrying that tag, newest first,
   and says how many it found.
7. An unknown tag — `GET /tag/zzz` — returns **404**, and the browser shows
   your custom 404 page from problem 1.

## Constraints

- **`tags: list[str] = []` is not allowed, and Python will stop you.** A
  default written that way is created once, when the class is defined, and
  then *shared* by every post you ever make — tag one post, and every post
  is tagged. `dataclass` refuses it outright with `ValueError: mutable
  default`. Write `field(default_factory=list)`, which means "call `list()`
  fresh for each new post".
- **Clean at the boundary, exactly once.** The cleaning happens in one
  place: on the way in, before the post is stored. Not in the template, not
  in each route, not in a comparison. If you find yourself writing
  `.lower()` on a tag anywhere except `parse_tags` and the one line that
  reads the tag out of the URL, the boundary has leaked.
- **`parse_tags` is a separate function, not code inside the route.** A
  route needs a request to run; a function needs a string. Keeping it apart
  means you can check it against ten messy inputs in one second, and the
  shipped file does exactly that before it touches a single URL.
- **The pill's link is `url_for`, never a hand-built string.** Writing
  `href="/tag/{{ tag }}"` looks identical today and breaks silently the day
  you rename the route — and it does not escape a tag containing a space or
  a `&`. `url_for` re-derives the path from the route table and encodes the
  value for you.
- **Read the form field with `.get`, not `[...]`.** `request.form["tags"]`
  raises if the field is missing, and it *will* be missing — an old bookmark,
  a hand-written `curl`, a form you edited yesterday. `request.form.get("tags", "")`
  gives you the empty string, and `parse_tags("")` gives you `[]`, which is
  a perfectly good answer.
- **Lowercase the tag coming out of the URL too.** Everything stored is
  lowercase, so `/tag/PYTHON` has to be folded down before the comparison or
  it will 404 on a tag that plainly exists. One `.strip().lower()` at the
  top of the route.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-04-post-tags.py
parse_tags at work:
  'Python, flask ,, PYTHON'    -> ['python', 'flask']
  '  web , WEB,web '           -> ['web']
  ''                           -> []

POST /new tags='Python, flask ,, PYTHON, web' -> 302
  stored on the post: ['python', 'flask', 'web']
  pills on the index link to: ['/tag/python', '/tag/flask', '/tag/web']

GET /tag/python -> 200
  the page counts: True
GET /tag/PYTHON -> 200 (normalised on the way in)
GET /tag/zzz    -> 404
```

Read the first block before anything else. `'Python, flask ,, PYTHON'` has
four pieces between its commas and comes out with two tags: the empty piece
vanished, and `PYTHON` was folded onto the `python` already there. That one
line is the whole problem.

## Steps

1. Add `tags: list[str] = field(default_factory=list)` to `Post`, and add
   `field` to the `from dataclasses import ...` line. Run the file. It
   should still work, with every post carrying an empty list.
2. Write `parse_tags(raw)`. Start an empty list, walk `raw.split(",")`,
   `strip().lower()` each piece, and append it only if it is not empty and
   not already in the list.
3. Test `parse_tags` on its own, before you touch a template. Feed it
   `"Python, flask ,, PYTHON"`, `"  web , WEB,web "`, and `""`. Print the
   results. Fix it here, where there is no browser in the way.
4. Add the tags input to `new.html`, with a label and a
   `placeholder="python, flask, web"` so nobody has to guess the format.
5. In `new_post`, read `request.form.get("tags", "")` into `raw_tags` and
   pass `parse_tags(raw_tags)` to the new `Post`.
6. Still in `new_post`: when the title or body is missing and you re-render
   the form, hand the template back `raw_tags` — the exact string the person
   typed — not the parsed list. They are mid-sentence; do not rewrite it
   under them.
7. Add the pill loop to `index.html`, wrapped in `{% if post.tags %}` so a
   post with none does not leave an empty stub.
8. Add the `/tag/<tag>` route: lowercase the tag, build the matching list,
   `abort(404)` if it is empty, otherwise render `tag.html`.
9. Write `tag.html` — extends the base, one heading, the count, the list of
   titles, a link home.
10. Click a pill. Then edit the URL by hand to `/tag/PYTHON` (still works)
    and `/tag/zzz` (your 404 page from problem 1).

## The Solution

```python
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
```

**Everything hard happens in `parse_tags`, and it is nine lines.** The
function walks the pieces between the commas, cleans each one, and appends
it only if it survives two checks: it is not empty, and it is not already
in the list. `if tag and tag not in seen` is doing both jobs — an empty
string is falsy in Python, so the first half throws away what was between
those two commas, and the second half throws away the second `PYTHON`.
Order is kept because a list appends to the end, so the tags come out in
the order they were typed.

**Cleaning once means everything after it is a plain comparison.** Because
every tag in `POSTS` was cleaned on the way in, the tag route's filter is
just `wanted in p.tags` — no lowercasing, no stripping, no "well, unless
they typed it differently". That is the payoff for doing the work at the
boundary. Do it late instead, and every single place that touches a tag has
to remember to clean it, and one of them will forget.

**The route still folds the tag from the URL.** `wanted = tag.strip().lower()`
is not a contradiction of the rule above — the URL is *also* a boundary.
Anyone can type `/tag/PYTHON` in the address bar, so the value arriving
there is untrusted text just like the form field was, and it gets the same
one-line treatment on arrival. The captured output proves it: `/tag/PYTHON`
answers 200.

**`abort(404)` is a jump, not a return.** The line reads like a function
call, and it is, but it never comes back — it raises an exception that Flask
catches and turns into a 404 response. That is why `return render_template(...)`
on the next line is safe to write without an `else`: if the tag was unknown,
control never reaches it. And because it produces a real 404, your custom
404 page from problem 1 renders automatically. You did not have to wire
anything up.

**The pills and the URLs cannot disagree.** The pill text is `{{ tag }}` and
the pill link is `url_for('show_tag', tag=tag)` — the same variable, twice.
The captured output shows the pills pointing at `/tag/python`, `/tag/flask`,
and `/tag/web`, which are exactly the three tags stored on the post. There
is no third place where a mismatch could hide.

**The failed-validation branch re-renders `raw_tags`, not the parsed list.**
Look closely at that line. If the writer forgot a title, they get the form
back with their tag box exactly as they left it — `Python, flask ,, PYTHON`
and all. Handing back `['python', 'flask']` instead would silently rewrite
what they were typing, mid-thought, which feels like the page fighting them.
Clean the data on the way to storage; show people their own words on the
way back to the form.

**`{% for ... %}{% else %}` is a Jinja gift.** In `index.html`, the `else`
branch after the post loop runs when the list was empty — no posts at all —
so the "No posts yet." message costs nothing extra. Python's `for/else`
means something different and stranger; Jinja's is the useful one.

## Run it

Copy the worked answer on this page into `problem-04-post-tags.py` and run it:

```bash
python problem-04-post-tags.py
```

It needs Flask installed and nothing else, and it exits on its own — no
server to stop, because it drives itself with `app.test_client()`, Flask's
in-process fake browser. In your own blog the same change lands as a field
on `Post`, one input in `templates/new.html`, the pill loop in
`templates/index.html`, and a new `templates/tag.html`.

The `-solution` in the filename keeps this file from colliding with your own
`problem-04-post-tags.py`.

## Common bugs to catch

- **A `ValueError` the moment the file is imported, before any route runs.**
  You wrote `tags: list[str] = []`. Python is refusing on purpose, because
  that one list would be shared by every post:

  ```text
  ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory
  ```

  Write `tags: list[str] = field(default_factory=list)` and import `field`
  from `dataclasses`.

- **A post has a tag that is the empty string, and its pill links nowhere.**
  You split on commas and forgot to drop the empty pieces, so `"a,,b"` gave
  you three tags. The empty one then breaks `url_for`, because the default
  URL part refuses to be empty:

  ```text
  werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'show_tag' with values ['tag']
  ```

  Filter with `if tag`.

- **`/tag/Python` returns 404 but `/tag/python` works.** The tags in storage
  are lowercase and the tag from the URL is not. Add `.strip().lower()` to
  the value the route receives, so both sides of the comparison are folded
  the same way.

- **`werkzeug.exceptions.BadRequestKeyError: 400 Bad Request` with
  `KeyError: 'tags'` underneath.** You used `request.form["tags"]` and the
  request did not carry that field. `request.form.get("tags", "")` returns
  the empty string instead, which `parse_tags` happily turns into `[]`.

- **The same tag shows up twice under one title.** No duplicate check. The
  writer typed `Python` and `PYTHON`; after lowercasing they are the same
  string, so `if tag not in seen` catches it. Do the lowercasing *before*
  the duplicate check, or it will not.

- **A `BuildError` naming the endpoint `show_tag`.** No route named
  `show_tag` exists yet, or the function has a different name — you renamed
  it and left the template alone. `url_for` looks up the *function's* name,
  not the URL — so `@app.route("/tag/<tag>")` over `def show_tag(tag)`
  is what makes `url_for('show_tag', tag=...)` resolve.

- **`TypeError: show_tag() got an unexpected keyword argument 'tag'`.** The
  placeholder in the route is `<tag>` but the function takes something else,
  or takes nothing. The name inside the angle brackets and the parameter
  name have to match, letter for letter — that is how the value gets in.

- **The tag page lists every post, not the matching ones.** The filter
  compares against the wrong thing, usually `if wanted in p` or
  `if wanted in p.title`. It is `if wanted in p.tags` — membership in the
  post's tag list.

## Under the hood

<details>
<summary>Under the hood — why a mutable default is banned, and what default_factory actually does</summary>

A dataclass turns your class body into a generated `__init__`. If a field's
default is a plain value, that value becomes the default argument of the
generated function — and Python evaluates default arguments **once**, when
the function is defined, not each time it is called. So `tags: list[str] = []`
would produce something equivalent to:

```python
def __init__(self, id, title, body, tags=[]):  # the classic bug
    ...
```

Every post created without tags would receive *the same list object*.
Appending to one post's tags would appear on all of them, silently, and the
bug would only surface much later when the data looked haunted.

`dataclasses` detects this at class-creation time by checking whether the
default is an instance of `list`, `dict`, or `set` — an explicit
`isinstance` test in `dataclasses._process_class` — and raises `ValueError`
rather than let it through. `field(default_factory=list)` stores the
callable instead, and the generated `__init__` calls it once per instance:

```python
def __init__(self, id, title, body, tags=_HAS_DEFAULT_FACTORY):
    if tags is _HAS_DEFAULT_FACTORY:
        tags = list()
    ...
```

The check is a type check, not a mutability check, so a custom mutable class
as a default slips past it. The `field(default_factory=...)` habit is the
one to keep, not the error message.

</details>

<details>
<summary>Under the hood — what the tag placeholder in a route really matches, and what a slash does to it</summary>

`/tag/<tag>` uses Werkzeug's default converter, `string`. It matches any
text **except a forward slash**, and it refuses to match the empty string
(`minlength=1`). Both facts explain real behaviour:

- A tag containing a slash — `c/c++` — never reaches your route at all. The
  URL `/tag/c/c++` has too many segments and 404s in the router, before any
  of your code runs. If you genuinely want that, `<path:tag>` matches
  slashes too, at the cost of making the route greedy.
- An empty tag cannot be built. `url_for('show_tag', tag='')` raises
  `BuildError`, which is the router protecting you from a URL that could
  never be matched back.

Other converters exist and are worth knowing: `<int:id>` matches digits and
hands your function an `int` (not a string), `<float:x>`, `<uuid:x>`, and
`<path:x>`. `@app.route("/post/<int:post_id>")` is why `/post/abc` 404s
without you writing a single validation line — the converter refused it
before your function was called.

Spaces and `&` in tag values are handled by `url_for` too: it percent-encodes
them, so a tag `data science` becomes `/tag/data%20science` and arrives back
in your function as the original text, decoded. Hand-writing
`href="/tag/{{ tag }}"` skips that step and produces a broken link.

</details>

<details>
<summary>Under the hood — abort(404), the exception it raises, and why your custom page appears</summary>

`abort(404)` looks up 404 in Werkzeug's table of HTTP exceptions and
**raises** `werkzeug.exceptions.NotFound`, which is a subclass of
`HTTPException`. The raise unwinds out of your view function, and Flask's
request-handling loop catches `HTTPException` on the way out, hands it to
`handle_user_exception`, and looks for a registered handler for its code.
Your `@app.errorhandler(404)` from problem 1 is that handler, so your
template renders — and if you had not registered one, Werkzeug's plain
default page would.

Two consequences follow from "it raises":

- Code after `abort(...)` in the same branch is unreachable. Writing
  `else:` around the happy path is harmless but unnecessary.
- A bare `except Exception:` anywhere between the abort and Flask will
  swallow your 404 and turn it into a 500. If you wrap view logic in a
  try/except, re-raise `HTTPException` explicitly.

`abort(404)` and `return render_template("404.html"), 404` produce the same
response; the difference is reach. `abort` works from any depth — a helper
three calls down can stop the request — while the return form only works
from the view function itself.

</details>

<details>
<summary>Under the hood — the cost of a list membership test, and when to switch to a set</summary>

`wanted in p.tags` scans the list from the front until it finds a match, so
it costs time proportional to the number of tags on that post. With five
tags per post that is nothing. The route also scans every post, so the whole
tag page is roughly *posts x tags per post* comparisons — fine for a blog
that lives in a Python list, and irrelevant next to the cost of rendering
the page.

`in` on a `set` or a `dict` key is different: it hashes the value and jumps
straight to a bucket, so the cost does not grow with size. A set would be
the natural type for tags if order did not matter — it also de-duplicates
for free. Order does matter here, though: the tags should appear in the
order they were typed, and a set has no order to give.

The de-duplicating list built with `if tag not in seen` is quadratic in the
number of tags on a single post, which for a handful of tags is faster in
practice than building a set, because there is no hashing. If you ever needed
the fast version and still wanted order, `list(dict.fromkeys(cleaned))` does
it in one line: dictionaries have kept insertion order since Python 3.7, and
keys are unique by definition.

The real fix at scale is not a Python data structure at all. Once posts live
in a database (Week 10), tags become their own table with an index, and
`/tag/python` becomes a query the database answers without reading every
post.

</details>

<details>
<summary>Under the hood — 404 or empty page? The argument for each</summary>

The brief says an unknown tag is a 404, and that is the right default for
this problem, but the choice is a real design decision and worth seeing
argued.

**404 says the thing does not exist.** A tag with no posts is not a tag —
nobody ever applied it. Returning 404 keeps search engines from indexing
infinite made-up URLs (`/tag/aaa`, `/tag/aab`, ...), and it tells an
automated client the truth in a status code rather than in prose it cannot
read.

**An empty page says the thing exists but is currently empty.** That is the
right answer when the tag *is* real and just has nothing in it right now —
a tag whose last post was deleted, or a category list you control. Returning
404 there is a lie, and it makes a bookmarked page break for no reason.

The deciding question is whether the resource exists independently of its
contents. In this blog, a tag exists only because a post carries it, so
unknown tag means unknown resource, so 404. In Week 10, when tags might get
their own table, a tag row could exist with zero posts — and then the empty
page becomes correct.

</details>

## Acceptance checklist

- [ ] `Post` has `tags: list[str] = field(default_factory=list)`, and two
      posts created with no tags do not share a list.
- [ ] Creating a post with `python, flask, web` saves exactly three tags.
- [ ] `parse_tags("Python, flask ,, PYTHON")` returns `['python', 'flask']`
      — lowercased, stripped, empties dropped, no repeats.
- [ ] The blog index shows tag pills under each title, and a post with no
      tags shows no empty pill row.
- [ ] Clicking a tag goes to `/tag/python` and lists only matching posts.
- [ ] `/tag/PYTHON` shows the same page as `/tag/python`.
- [ ] An unknown tag (`/tag/zzz`) returns 404 and renders your custom 404
      page from problem 1.
- [ ] Every pill link is built with `url_for` — `grep -n 'href="/tag/'` in
      your templates finds nothing.

## Stretch

- Build a tag cloud on the index: every tag used anywhere, with a count
  beside it. `collections.Counter` over every post's tags gives you the
  counts in one line, and `.most_common()` gives you them sorted.
- Add `/tags` — a page listing every tag in the blog, alphabetically, each
  one a link. Now a reader can find a shelf without first finding a book
  that sits on it.
- Cap it. Refuse more than eight tags on one post, or any tag longer than
  twenty characters, and flash a clear message saying which rule was broken.
  Decide whether you truncate or reject, and write down why.
- Allow multiple tags in one URL: `/tag/python+flask` listing posts that
  carry both. Split the value on `+` and filter with `all(...)`. Then try
  `set(wanted) <= set(post.tags)`, and see which version you would rather
  read in a month.
- Make the tag page tell the truth about an empty result in a nicer way:
  when there is no exact match, look for tags that *start with* what was
  asked for and offer them — "no posts tagged `pyth`; did you mean
  `python`?" — while still answering 404.
