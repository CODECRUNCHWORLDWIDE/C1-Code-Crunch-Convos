# Homework Problem 5 — Search filter

> **Topic:** `method="get"` forms, reading `request.args`, filtering before you render, and the auto-escaping that keeps a stranger's text harmless
> **Lecture:** [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Beginner
> **Target time:** 1 hour
> **Why this one:** this is the first form in the course that is *not* a POST, and the difference is the whole lesson — a search is a question, not a change, so the question belongs in the address bar where it can be bookmarked, shared, and refreshed. It is also the first time a stranger's typing lands inside your HTML, which is where auto-escaping stops being a footnote and starts being the thing standing between your visitors and someone else's JavaScript.

## The Brief

Put a search box at the top of your blog index. Type something, press
Search, and the page shows only the posts whose **title or body** contains
what you typed. Capital letters must not matter: `Flask`, `flask`, and
`FLASK` all find the same posts.

Think of your posts as a shelf of books. The search box is a sticky note
that says "only put the ones with *flask* on the cover or inside on the
table". The shelf never changes. You are only choosing what to lay out.

The one decision that shapes everything else: the form is
`method="get"`. A GET form does not mail a sealed envelope to the server.
The browser takes the field named `q`, glues it onto the end of the
address, and asks for `/?q=flask`. **The search becomes the URL.** So you
can bookmark a search, paste it to a friend, and hit refresh without the
browser popping up "Confirm Form Resubmission". No POST, no redirect, no
session — one route, one form, one filter.

This is a change to your mini-project blog. The shipped file beside this
page is a self-contained slice of that blog with the search working, so
the finished shape runs anywhere as one file.

## Starter

Save this as `problem-05-search-filter.py` in your `homework/` folder. It runs as
pasted and lists all three posts — it just has no way to search them yet.
Fill in the `TODO`s.

```python
"""problem-05-search-filter.py — starter: a blog index with no way to search it.

Run with: python problem-05-search-filter.py
"""

from dataclasses import dataclass

from flask import Flask, render_template, request
from jinja2 import DictLoader

# TODO 1: add a <form method="get" action="{{ url_for('index') }}"> at the top
#         of INDEX_HTML, holding one text field named "q". Give that field
#         value="{{ request.args.get('q', '') }}" so it keeps what was typed.
# TODO 2: in index(), read the query with request.args.get("q", "").strip().
#         Keep the raw text for showing back; lowercase a copy for matching.
# TODO 3: filter POSTS with the lowered copy — a post matches when that text
#         is in its lowered title OR its lowered body. Empty query filters
#         nothing, so every post shows.
# TODO 4: pass the raw query and the match count to the template, and use them
#         in {% block title %} and in the <h2>, so a search reads
#         "Search results for 'flask' (1 found)".

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

INDEX_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Latest posts</h2>

  {% for post in posts %}
    <article>
      <h3>{{ post.title }}</h3>
      <p>{{ post.body }}</p>
    </article>
  {% else %}
    <p>No posts yet.</p>
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
    """List posts. It ignores ?q= completely right now — that is the job."""
    return render_template("index.html", posts=list(reversed(POSTS)))


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

In your own blog this is the same change across real files: a form at the
top of `templates/index.html`, and four new lines in the `index` view.

## Requirements

1. `index.html` carries a `<form method="get" action="/">` with exactly one
   text field, named `q`, and a submit button.
2. The index view reads the query with
   `q = request.args.get("q", "").strip()` and filters the posts **before**
   handing them to `render_template`.
3. Matching ignores case on both sides: lowercase the query, and compare it
   against a lowercased title and body.
4. A post matches when the text appears in its title **or** in its body.
5. An empty `q` shows every post. That is the plain default, not a special
   branch bolted on somewhere else.
6. The query travels back to the reader in the heading and the tab title:
   `Search results for 'flask' (1 found)`.
7. The text field keeps what was typed after the page reloads, via
   `value="{{ request.args.get('q', '') }}"`.
8. No input at all produces a traceback — not accented letters, not emoji,
   not text that looks like HTML.

## Constraints

- **The form is GET, not POST, and the reason is what a search *is*.** POST
  means "change something on the server". GET means "show me something". A
  search changes nothing, so it gets a GET, and the payoff is concrete: the
  question ends up in the address bar. `/?q=flask` can be bookmarked, sent
  in a message, and refreshed. A POST search cannot do any of those, and
  refreshing one makes the browser ask whether to resend.

- **Filter in the view, not in the template.** A template's job is the
  *shape* of the page; deciding which posts belong is a decision, and
  decisions live in Python where you can read them and test them. There is
  a practical reason too: the heading needs the count of what survived, and
  a template that filters while it loops has no way to know that number
  until the loop is over.

- **Two variables, one query.** Keep the raw text for showing back and a
  lowered copy for matching. Somebody who types `JINJA` and gets a heading
  that says `Search results for 'jinja'` will read that as your site
  quietly correcting them. The captured run below searches `JINJA` on
  purpose to prove the heading echoes it untouched.

- **`request.args.get("q", "")`, never `request.args["q"]`.** A plain `/`
  has no `q` at all. Square brackets on a missing key raise
  `werkzeug.exceptions.BadRequestKeyError` and the visitor gets a 400
  instead of your home page. `.get` with a default hands you `""` and the
  empty-query path just works.

- **Print the query with `{{ }}` and nothing else — this is the safety
  rule.** Whatever a stranger types has to appear on your page. If someone
  searches for `<script>alert(1)</script>`, those characters must land in
  the heading as *letters you can read*, never as a tag the browser runs.
  Jinja does this for you: in an HTML template it auto-escapes every
  `{{ }}`, turning `<` into `&lt;`, `>` into `&gt;`, `&` into `&amp;`, and
  `"` into `&#34;`. The browser then draws those characters and never
  treats them as markup. The captured run shows it:
  `raw <script> reached the page: False`. **Never put `|safe` on anything a
  visitor typed.** `|safe` switches the escaping off, and that is exactly
  how a search box turns into a way to run someone else's JavaScript inside
  your visitors' browsers.

- **Nothing crashes on odd input, and you get that almost for free.**
  `request.args.get` always hands back a `str`. `.strip()`, `.lower()`, and
  `in` work on every string Python can hold, including `Zoë`, Arabic, and
  emoji, because Python strings are already unicode — there is no decoding
  step left for you to get wrong. The crashes come from *assuming* instead:
  `request.args.get("q")` with no default returns `None`, and `None` has no
  `.strip()`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-05-search-filter-solution.py
GET /                -> 200 (no query: everything shows)
  <h2>Latest posts</h2>
  posts on the page  : 3
GET /?q=flask        -> 200
  <h2>Search results for 'flask' (1 found)</h2>
  posts on the page  : 1
  the box keeps the typing: True
GET /?q=JINJA        -> 200 (case-insensitive, both sides)
  <h2>Search results for 'JINJA' (1 found)</h2>
GET /?q=             -> 200 (empty query: everything again)
  posts on the page  : 3

Hostile input, no traceback, nothing executed:
  GET /?q=<script>alert(1)</script> -> 200
  <h2>Search results for '&lt;script&gt;alert(1)&lt;/script&gt;' (0 found)</h2>
  raw <script> reached the page: False
  GET /?q=Zoë -> 200 (unicode is just text)
```

Read the hostile block closely. The search text is still there in the
heading — `&lt;script&gt;` is how a browser spells a literal `<script>` —
but no real `<script>` tag ever reached the page. That is auto-escaping
doing its job, and it is the difference between a search box and a hole.

## Steps

1. Copy the starter into `problem-05-search-filter.py` and run it. Visit `/` and
   then `/?q=flask`. Both show three posts, because nothing reads `q` yet.
2. Add the form to the top of `INDEX_HTML`:
   `<form method="get" action="{{ url_for('index') }}">`, one
   `<input type="search" name="q">`, one submit button. Reload, type
   something, press Search, and watch the address bar become `/?q=...`.
   That alone is worth stopping to look at.
3. In `index()`, add `raw_q = request.args.get("q", "").strip()` and a
   lowered copy, `needle = raw_q.lower()`. Pass `q=raw_q` to the template
   and print it in the heading. Reload and confirm the round-trip.
4. Add `value="{{ request.args.get('q', '') }}"` to the input. Search
   again — the box now keeps your words instead of blanking.
5. Filter. Guard it with `if needle:` so an empty query skips the filter
   entirely and every post shows. Match on
   `needle in p.title.lower() or needle in p.body.lower()`.
6. Pass `total=len(matches)` and use it in the heading and the
   `{% block title %}`. Check the number against the posts you can count on
   the page.
7. Add the empty state: a `{% for %}` / `{% else %}` that says
   "Nothing matched that search." when the filter found none, and
   "No posts yet." when there is genuinely nothing to show.
8. Now try to break it. Search `<script>alert(1)</script>`, then `Zoë`,
   then `"` on its own, then a very long paste. No traceback, and use
   View Source to confirm the `<script>` came through as `&lt;script&gt;`.
9. Bookmark `/?q=flask`, close the tab, open the bookmark. The search is
   still there. That is the whole argument for GET, in one action.

## The Solution

```python
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
```

**The URL is the state.** There is no saved search anywhere — no session
key, no database row, no hidden field. The view is handed `?q=flask` on
every single request and rebuilds the answer from scratch. That is why
refresh is safe, why the back button behaves, and why two people looking
at the same link see the same page. The rule generalises: put the thing
that describes *what you are looking at* in the URL, and put the thing
that describes *who you are* in the session.

**`raw_q` and `needle` are two variables on purpose.** `raw_q` is exactly
what the visitor typed, and it is what the heading shows. `needle` is the
lowercase copy, and it never leaves the matching line. Because `needle` is
lowered and both `p.title.lower()` and `p.body.lower()` are lowered,
`JINJA` finds `Jinja loops` — the captured run does this on purpose, and
the heading still reads `'JINJA'`.

**`if needle:` is the empty-query rule, written once.** An empty search box
sends `?q=`, and `"".strip().lower()` is `""`, which is falsy, so the
filter is skipped and `matches` stays as the full list. There is no second
code path for "no search" to drift out of step with — same route, same
template, same variables, one `if`.

**`in` on strings is a substring test, and that is deliberate here.**
`"flask" in "hello, flask"` is `True`. It also means searching `ask` finds
`flask`, which is fine for a blog with three posts and is the honest
starting point. What matters is that you *know* that is the rule you
chose.

**`total=len(matches)` is counted after filtering, not before.** It is the
length of the list that is actually about to be rendered, so the heading
and the page can never disagree. Passing `len(POSTS)` there is the classic
version of this bug: `3 found` above a page showing one post.

**The `{% for %} / {% else %}` is Jinja's, not Python's.** The `{% else %}`
branch runs when the loop had nothing to loop over. It gives you an empty
state without an extra `{% if %}`, and the inner `{% if q %}` splits the
two meanings of empty: "your search found nothing" is a very different
message from "this blog has no posts".

**The escaping is the load-bearing part, and it is invisible.** Jinja
turns on auto-escaping for templates whose name ends in `.html`, so every
`{{ q }}` on the page goes through an escape step before it is written
out. `<` becomes `&lt;`. The browser renders the characters and never
parses them as a tag. Nothing in the solution asks for this and nothing
must ever turn it off: no `|safe`, no `Markup(...)`, no building HTML
strings in Python and passing them through. That single habit is what
makes requirement 8 true for *every* input, not just the ones you thought
to test.

## Download and run

Download
[problem-05-search-filter-solution.py](./problem-05-search-filter-solution.py)
and run it:

```bash
python problem-05-search-filter-solution.py
```

It needs Flask installed and nothing else, and it exits on its own — it
drives the app with `app.test_client()`, Flask's in-process fake browser,
instead of starting a server. In your own blog the same change lands as a
form at the top of `templates/index.html` plus four lines in the `index`
view.

The `-solution` in the filename keeps this file from colliding with your
own `problem-05-search-filter.py`.

## Common bugs to catch

- **Visiting plain `/` returns a 400 with
  `werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: KeyError: 'q'`.**
  The view used `request.args["q"]`. There is no `q` on a plain `/`. Use
  `request.args.get("q", "")`.

- **`AttributeError: 'NoneType' object has no attribute 'strip'`.**
  `request.args.get("q")` with no default returns `None` when the key is
  missing, and `None` has no `.strip()`. Supply the default:
  `.get("q", "")`.

- **Searching `Flask` finds nothing but `flask` works.** Only one side was
  lowered. Both the query and the text being searched have to be lowered,
  every time.

- **The search box is empty again after every search.** The input has no
  `value` attribute. Add `value="{{ request.args.get('q', '') }}"`. The
  browser cannot remember it for you — a fresh page is a fresh page.

- **The heading says `3 found` above one post.** `total` was computed from
  the full list instead of the filtered one. Count `matches`, after the
  filter.

- **Refreshing a search pops "Confirm Form Resubmission".** The form is a
  POST. Change it to `method="get"`. The dialog exists because the browser
  cannot know whether resending a POST would charge a card twice; a GET
  never has that question.

- **An empty search shows zero posts instead of all of them.** The filter
  ran unguarded, so `"" in text` was never the test — something like
  `p.title.lower() == needle` was. Guard the filter with `if needle:` and
  leave the list alone when there is no query.

- **`<script>alert(1)</script>` shows up as visible text and you reach for
  `|safe` to "fix" it.** That is not a bug. That is the escaping working
  exactly as designed, and `|safe` is how you break it. Leave it alone.

- **Searching for a phrase with a space finds nothing you expected.** The
  browser sends `?q=hello+world`; Flask decodes that back to
  `hello world` before you see it, so the query really is the phrase — and
  `in` looks for that whole phrase, in order. Two separate words in a post
  will not match.

## Under the hood

<details>
<summary>Under the hood — why a search is a GET and a login is a POST</summary>

HTTP sorts its methods into groups, and the groups have names.

**Safe** means "asking this does not change anything". GET and HEAD are
safe. **Idempotent** means "asking it five times leaves the world in the
same state as asking it once". GET, HEAD, PUT and DELETE are idempotent;
POST is not. A search is safe and idempotent, so it is a GET. Creating a
post is neither, so it is a POST.

Browsers and the machines between you and the server act on this. A GET
may be cached, prefetched, and retried automatically after a dropped
connection. A POST is none of those things, which is exactly why the
browser stops to ask before resending one.

The cost of GET is that the query is visible and it travels. It shows in
the address bar, in browser history, in server access logs, in proxy logs,
and in the `Referer` header sent to any site you link out to. That is
harmless for `?q=flask` and unacceptable for a password — which is why
problem 6's login form is a POST even though a login "asks" for something.

There is a length ceiling too. The standards do not name one, but real
servers and browsers stop somewhere around 2,000 to 8,000 characters of
URL. Long free text, file uploads, and anything binary need a POST body.

</details>

<details>
<summary>Under the hood — what `request.args` actually is</summary>

`request.args` is not a plain dict. It is a Werkzeug `MultiDict`: a
mapping where one key may hold several values, because a URL is allowed to
repeat one — `/?tag=python&tag=flask` is legal and meaningful.

- `request.args.get("tag")` gives you the **first** value.
- `request.args.getlist("tag")` gives you **all** of them, as a list.
- It is immutable. You cannot edit the query string by assigning to it.

`.get` also takes a `type` argument, which converts and quietly falls back
instead of raising: `request.args.get("page", 1, type=int)` returns `1`
for a missing `page` *and* for `?page=banana`. That is the right shape for
user-supplied numbers, where a 500 would be a bad answer to a typo.

The decoding happens before you ever see the value. A URL may only carry a
limited set of characters, so the browser percent-encodes the rest: a
space becomes `+` or `%20`, and `Zoë` becomes `Zo%C3%AB` — that `C3 AB`
is the UTF-8 encoding of `ë`, written as two hex bytes. Werkzeug reverses
all of it and hands your view a normal Python `str`. This is why the
unicode case in the captured run is boring: by the time the query reaches
`index()`, it is just text.

</details>

<details>
<summary>Under the hood — what auto-escaping does, character by character</summary>

Jinja turns auto-escaping on for templates whose name ends in `.html`,
`.htm`, `.xml` or `.xhtml` — Flask configures this, and it is why the
templates in the shipped file are registered as `index.html` and not
`index`. Rename a template to `index.txt` and the escaping silently stops.

When it is on, every `{{ value }}` is passed through an escape function
that replaces five characters:

| character | becomes  | why it matters                        |
| --------- | -------- | ------------------------------------- |
| `&`       | `&amp;`  | must go first, or the others re-escape |
| `<`       | `&lt;`   | starts a tag                          |
| `>`       | `&gt;`   | ends a tag                            |
| `"`       | `&#34;`  | ends a double-quoted attribute        |
| `'`       | `&#39;`  | ends a single-quoted attribute        |

The last two are why `value="{{ request.args.get('q', '') }}"` is safe.
A query of `" onmouseover="alert(1)` would otherwise close the `value`
attribute and start a new one — a real attack, not a hypothetical. Escaped,
it is just a strange-looking search term sitting inside the box.

The mechanism is a type. `markupsafe.Markup` is a `str` subclass meaning
"already safe HTML"; escaping produces one, and Jinja skips anything that
is already a `Markup`. `|safe` simply wraps a value in `Markup` and tells
Jinja not to bother. So `|safe` is not a formatting choice — it is you
signing your name to the claim that this string is trustworthy HTML. For
text a stranger typed, that claim is false.

The class of bug this prevents is **cross-site scripting**, XSS: getting
your page to run someone else's JavaScript in your visitors' browsers,
with your site's cookies and your site's permissions. It stays in the top
handful of web vulnerabilities year after year, and the defence in this
problem is entirely "do nothing, and do not switch it off".

</details>

<details>
<summary>Under the hood — when `in` stops being good enough</summary>

`needle in text` is a substring scan. Python's implementation is a tuned
mix of Crochemore-Perrin two-way matching and a Bloom-filter skip; call it
roughly O(n) per post in practice, and the whole search O(number of posts
× post length). For three posts, or three hundred, that is free. It is
also completely fine to reach a few thousand before it matters.

What breaks first is not speed, it is meaning:

- Substrings ignore word edges. `for` matches `before` and `format`.
- No stemming. `run` does not find `running`; `mouse` does not find `mice`.
- No ranking. A title hit and a hit buried in paragraph nine are equal.
- No accent folding. `resume` does not find `résumé`.
- Multi-word queries are treated as one exact phrase, in order.

The usual next step is tokenising — split both sides into words, lowercase,
strip punctuation, and require that every query word appears somewhere.
After that, an index: a dictionary from word to the set of post ids
containing it, so lookup stops depending on the number of posts at all.

In Week 10 the posts move into SQLite, and two better options arrive with
them. `WHERE title LIKE '%flask%'` pushes this same substring scan into
the database. SQLite's FTS5 full-text index does the real thing —
tokenising, stemming, phrase queries and relevance ranking — and is worth
knowing exists long before you need it.

</details>

## Acceptance checklist

- [ ] `/?q=flask` shows only the matching posts.
- [ ] `/?q=` (empty) shows all posts, and so does a plain `/`.
- [ ] The form's text input keeps the typed value on reload, via
      `value="{{ request.args.get('q', '') }}"`.
- [ ] No traceback for any input, including unicode (`Zoë`) and
      HTML-looking strings (`<script>alert(1)</script>`).
- [ ] Searching `FLASK` and `flask` return the same posts.
- [ ] The heading count matches the number of posts actually on the page.
- [ ] You viewed source on a `<script>` search and saw `&lt;script&gt;`.
- [ ] You bookmarked a search URL, reopened it, and got the same results.

## Stretch

- Add an empty-state line that offers a way out: "Nothing matched
  *flask*." plus a link back to the unfiltered index. A dead end with no
  door is the most common search-box failure in real sites.
- Split the query on spaces and require **every** word to appear
  somewhere in the title or body. Then decide, and write down, whether
  `flask routes` should mean "both words" or "either word" — real search
  engines disagree about this, and the choice is yours to make on purpose.
- Highlight the match. Wrap the found text in `<mark>` inside the body
  preview. Do it in a Jinja filter and think hard about the escaping: you
  must escape the post text **first**, then insert the `<mark>` tags, then
  mark the finished string safe. Getting the order backwards re-opens the
  exact hole this problem closed.
- Add `?tag=` alongside `?q=` and make them combine, so
  `/?q=flask&tag=python` narrows twice. This is where `request.args`
  holding several keys starts to pay off, and where filtering in the view
  rather than the template stops being a style preference.
