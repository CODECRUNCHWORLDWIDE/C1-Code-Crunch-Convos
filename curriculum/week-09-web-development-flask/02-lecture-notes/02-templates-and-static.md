# Lecture 2 — Templates and Static Files

> **Goal:** by the end of this lecture you can build real HTML pages with
> Jinja2 templates: passing variables in, looping over collections, using
> filters, splitting layouts into a base + child templates with `{% extends %}`
> and `{% block %}`, including reusable partials, and serving CSS from the
> `static/` folder.

In lecture 1 you returned strings from view functions. That works for one or
two lines of HTML; it falls apart fast. The fix is **server-side templates**:
HTML files with little Python-like placeholders that Flask fills in for each
request.

---

## 1. Why templates?

Compare these two ways to render a list of post titles.

The **string-concatenation** approach (from lecture 1):

```python
@app.route("/")
def index() -> str:
    links = "<br>".join(
        f'<a href="/post/{pid}">{title}</a>' for pid, title in posts.items()
    )
    return f"<html><body><h1>Blog</h1>{links}</body></html>"
```

The **template** approach (this lecture):

```python
from flask import render_template

@app.route("/")
def index() -> str:
    return render_template("index.html", posts=posts)
```

```jinja
<!-- templates/index.html -->
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Blog</title></head>
  <body>
    <h1>Blog</h1>
    {% for pid, title in posts.items() %}
      <p><a href="{{ url_for('show_post', post_id=pid) }}">{{ title }}</a></p>
    {% endfor %}
  </body>
</html>
```

The template version is:

- **Readable** — designers (or future-you) can edit HTML without reading
  Python.
- **Safe by default** — Jinja2 escapes HTML in variables so that
  `posts = {1: "<script>alert(1)</script>"}` does not pop an alert on your
  homepage.
- **Reusable** — `{% extends %}` and `{% include %}` keep your layout in one
  file.

---

## 2. The template folder

Flask looks for templates in a folder called **`templates/`** next to your
`app.py` (unless you configure otherwise). For our blog app the layout is:

```text
my-blog/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── post.html
└── static/
    └── style.css
```

This is convention, not magic — but it is the convention Flask documents
and that everyone in the ecosystem uses. Stick with it.

---

## 3. Jinja2 syntax in one screen

Jinja2 has three kinds of delimiters:

| Delimiter      | Meaning                       | Example                            |
|----------------|-------------------------------|------------------------------------|
| `{{ ... }}`    | Output an expression          | `{{ post.title }}`                 |
| `{% ... %}`    | A statement (if, for, etc.)   | `{% if user %}` ... `{% endif %}`  |
| `{# ... #}`    | A comment (not rendered)      | `{# TODO: paginate #}`             |

Inside `{{ ... }}` and `{% ... %}` you write things that look like Python, with
a few important differences:

- Attribute access uses `.` or `[...]` — `post.title` and `post["title"]` are
  equivalent for dicts.
- There is no `len()` — use the `length` filter: `{{ posts|length }}`.
- Comments are `{# ... #}`, not `#`.
- Function calls work: `{{ url_for("index") }}`.

### Variables

```jinja
<p>Hello, {{ name }}!</p>
<p>You have {{ posts|length }} posts.</p>
<p>Today is {{ today }}.</p>
```

Pass these in from your view:

```python
from datetime import date

@app.route("/")
def index() -> str:
    return render_template(
        "index.html",
        name="Ada",
        posts=[...],
        today=date.today().isoformat(),
    )
```

### `if` / `elif` / `else`

```jinja
{% if posts %}
  <p>You have {{ posts|length }} post(s).</p>
{% elif drafts %}
  <p>Only drafts so far.</p>
{% else %}
  <p>No posts yet. <a href="{{ url_for('new_post') }}">Write one?</a></p>
{% endif %}
```

Note the `{% endif %}`. Every block tag needs a closing partner. Jinja will
yell at you if you forget.

### `for` loops

```jinja
<ul>
  {% for post in posts %}
    <li>{{ post.title }} — {{ post.body|truncate(60) }}</li>
  {% else %}
    <li><em>No posts yet.</em></li>
  {% endfor %}
</ul>
```

Two surprises here, both lovely:

- A `for` loop can have an **`{% else %}`** branch that runs when the
  iterable is empty.
- Inside the loop you can use a special **`loop`** variable: `loop.index`
  (1-based), `loop.index0` (0-based), `loop.first`, `loop.last`, `loop.length`.

```jinja
{% for post in posts %}
  <p>{{ loop.index }}. {{ post.title }}</p>
{% endfor %}
```

### Filters

Filters transform a value with the pipe `|` operator. Some of the most useful:

```jinja
{{ name|upper }}              {# ADA #}
{{ name|lower }}              {# ada #}
{{ name|title }}              {# Ada #}
{{ "hello"|length }}          {# 5 #}
{{ body|truncate(60) }}       {# trims long text #}
{{ posts|length }}            {# 7 #}
{{ tags|join(", ") }}         {# python, flask, web #}
{{ today|default("today") }}  {# fallback if undefined #}
{{ user_html|safe }}          {# disable auto-escaping (use with care!) #}
```

The full list is at <https://jinja.palletsprojects.com/en/stable/templates/#list-of-builtin-filters>.
Bookmark it — when you find yourself writing Python inside a template, there
is almost always a filter that does the job better.

### Whitespace

By default Jinja keeps your indentation in the output. If that bothers you,
strip whitespace with `-`:

```jinja
{%- for post in posts -%}
  {{ post.title }}
{%- endfor -%}
```

For HTML this rarely matters — browsers collapse whitespace.

---

## 4. `render_template`

The bridge between Python and Jinja is one function:

```python
from flask import render_template

@app.route("/")
def index() -> str:
    return render_template("index.html", posts=posts, name="Ada")
```

Rules:

- The first argument is the **template file name**, relative to the
  `templates/` folder. Subdirectories work: `render_template("posts/list.html")`.
- All other keyword arguments become **variables inside the template**.
- The return value is a string (the rendered HTML), which Flask turns into a
  200 response.

A subtle nice thing: `url_for`, `request`, `session`, `g`, and `config` are
**already available** inside every template — you do not have to pass them in.

---

## 5. Template inheritance: `{% extends %}` and `{% block %}`

You will never write the `<!doctype html>...<body>` boilerplate more than
once. Instead, create a **base template** with named *blocks*, and have each
page **extend** it.

`templates/base.html`:

```jinja
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}My Blog{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">My Blog</a></h1>
      <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('new_post') }}">New post</a>
      </nav>
    </header>

    <main>
      {% block content %}{% endblock %}
    </main>

    <footer>
      <small>Built with Flask &copy; 2026</small>
    </footer>
  </body>
</html>
```

`templates/index.html`:

```jinja
{% extends "base.html" %}

{% block title %}Home — My Blog{% endblock %}

{% block content %}
  <h2>Latest posts</h2>
  {% for post in posts %}
    <article>
      <h3><a href="{{ url_for('show_post', post_id=post.id) }}">
        {{ post.title }}
      </a></h3>
      <p>{{ post.body|truncate(120) }}</p>
    </article>
  {% else %}
    <p>No posts yet.</p>
  {% endfor %}
{% endblock %}
```

`templates/post.html`:

```jinja
{% extends "base.html" %}

{% block title %}{{ post.title }} — My Blog{% endblock %}

{% block content %}
  <article>
    <h2>{{ post.title }}</h2>
    <p>{{ post.body }}</p>
    <p><a href="{{ url_for('index') }}">&larr; Back to all posts</a></p>
  </article>
{% endblock %}
```

That is it. Every page now has the same header, footer, stylesheet link, and
`<title>` pattern, defined exactly once. Add a new page? Extend `base.html`
and fill in two blocks. Forget to set a title? You get the default,
`"My Blog"`, automatically.

A few rules:

- A child template **must** start with `{% extends "base.html" %}` (or
  whatever the parent file is named).
- Blocks in the child template can use `{{ super() }}` to include the parent
  block's content, then add to it.
- You can nest blocks. A common pattern is `{% block extra_head %}{% endblock %}`
  inside `<head>` so individual pages can add their own `<meta>` or
  `<script>` tags.

---

## 6. Includes: `{% include %}`

For small reusable snippets — a flash-messages widget, a footer fragment, a
post card — use `{% include %}`:

`templates/_flashes.html`:

```jinja
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class="flashes">
      {% for category, message in messages %}
        <li class="flash flash-{{ category }}">{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

Then in `base.html`:

```jinja
<main>
  {% include "_flashes.html" %}
  {% block content %}{% endblock %}
</main>
```

**Convention:** name include-only templates with a leading underscore
(`_flashes.html`, `_post_card.html`). It signals "this isn't a page; it's a
partial."

---

## 7. `url_for` (again, properly)

Hard-coding `/post/3` in a template is a bug waiting to happen — if you ever
rename the route to `/posts/3`, every link breaks. **Use `url_for`.**

```jinja
<a href="{{ url_for('show_post', post_id=post.id) }}">{{ post.title }}</a>
<a href="{{ url_for('index') }}">Home</a>
<form action="{{ url_for('new_post') }}" method="post">...</form>
```

The first argument is the **view function name** (the Python function, not
the URL pattern). Extra keyword arguments become URL parameters. Any
keyword that does *not* match a route parameter becomes a query string:

```jinja
{{ url_for("search", q="flask", page=2) }}
{# → /search?q=flask&page=2 #}
```

This is also how you link to static files, which is the next section.

---

## 8. Static files

Flask serves anything you put in a folder called **`static/`** at the URL
prefix `/static/`. CSS, images, JavaScript, fonts — all live there.

```text
my-blog/
├── app.py
├── templates/
│   └── ...
└── static/
    ├── style.css
    └── logo.png
```

Link them with `url_for("static", filename=...)`:

```jinja
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<img src="{{ url_for('static', filename='logo.png') }}" alt="Logo">
```

Why not just write `<link href="/static/style.css">`? Two reasons:

1. If you ever change the static URL prefix (e.g., to `/assets/`), `url_for`
   updates automatically.
2. Flask appends a cache-busting query string when you set
   `SEND_FILE_MAX_AGE_DEFAULT`. You do not have to think about it.

### A minimal `style.css`

Drop this in `static/style.css` for an instantly-less-ugly blog:

```css
/* static/style.css */
:root {
  --fg: #222;
  --bg: #fafafa;
  --accent: #2b6cb0;
}

* { box-sizing: border-box; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  max-width: 42rem;
  margin: 2rem auto;
  padding: 0 1rem;
  color: var(--fg);
  background: var(--bg);
  line-height: 1.6;
}

header h1 a { color: var(--fg); text-decoration: none; }

nav a {
  margin-right: 1rem;
  color: var(--accent);
}

article {
  border-bottom: 1px solid #ddd;
  padding: 1rem 0;
}

footer {
  margin-top: 3rem;
  color: #666;
  font-size: 0.875rem;
}
```

You will reuse and extend this in the mini-project.

---

## 9. Autoescaping (a 30-second security note)

By default Jinja2 **escapes** every variable rendered in an HTML template. If
`title` is `"<script>alert(1)</script>"`, Jinja outputs
`&lt;script&gt;alert(1)&lt;/script&gt;` — visible text, not executed code.
This is what prevents the simplest form of XSS.

The escape hatch is the `|safe` filter, or the `Markup` class in Python:

```jinja
{{ trusted_html|safe }}
```

**Use it almost never.** Only use it when you wrote the HTML yourself (e.g.,
output of a Markdown library). If the value came from a form, a URL, or a
database row, never mark it safe — that is the canonical XSS bug.

---

## 10. Putting it all together

Here is a tiny, complete app that uses everything in this lecture. Save the
files in the layout shown above and run `python app.py`.

`app.py`:

```python
"""A tiny blog app demonstrating templates, inheritance, and static files."""
from dataclasses import dataclass

from flask import Flask, abort, render_template

app: Flask = Flask(__name__)


@dataclass
class Post:
    id: int
    title: str
    body: str


POSTS: list[Post] = [
    Post(1, "Hello, Flask", "First post. Jinja templates are clearer than f-strings."),
    Post(2, "Templates rule", "Inheritance keeps your header in one place."),
    Post(3, "Static files", "CSS lives in /static and is linked via url_for."),
]


@app.route("/")
def index() -> str:
    return render_template("index.html", posts=POSTS)


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    for post in POSTS:
        if post.id == post_id:
            return render_template("post.html", post=post)
    abort(404)


@app.route("/new")
def new_post() -> str:
    # Real form arrives in lecture 3
    return "TODO: form coming next lecture"


if __name__ == "__main__":
    app.run(debug=True)
```

`templates/base.html`, `templates/index.html`, and `templates/post.html` are
the three files from section 5 above. `static/style.css` is the file from
section 8. Together that is a complete, server-rendered blog — minus the
form. Form handling is lecture 3.

---

## 11. Debugging templates

When templates break, Flask shows you the *Jinja* traceback alongside the
Python one. The most common gotchas:

- **`TemplateNotFound: index.html`** — your file is not under `templates/`,
  or the filename has a typo. Run `ls templates/` from your project root.
- **`UndefinedError: 'post' is undefined`** — you forgot to pass `post=` to
  `render_template`, or you mistyped it.
- **A literal `{{ post.title }}` in the page** — the file is being served as
  static, not rendered. Make sure you are calling `render_template`, not
  reading the file yourself.

In debug mode, Flask also auto-reloads templates when you save them — no need
to restart the server.

---

## 12. Recap and what is next

You can now:

- Render HTML from Jinja2 templates with `render_template`.
- Use variables, `if`, `for`, and filters inside templates.
- Build a base layout with `{% extends %}` and `{% block %}`, and reuse
  partials with `{% include %}`.
- Link to other routes with `url_for("view_name", ...)`.
- Serve CSS and images from `static/` and link them with
  `url_for("static", filename=...)`.

Your blog can now *display* posts. It still cannot accept new ones. That is
what forms are for — and they bring with them `POST` requests, validation,
flash messages, and sessions. All of that is lecture 3.

> **Practice:** finish `exercises/exercise-03-template-loop/` before reading
> lecture 3. You should be able to scaffold a new template + view pair
> without looking at the boilerplate.

---

## References

- Jinja2 template designer docs — <https://jinja.palletsprojects.com/en/stable/templates/>
- Built-in Jinja filters — <https://jinja.palletsprojects.com/en/stable/templates/#list-of-builtin-filters>
- Flask templating guide — <https://flask.palletsprojects.com/en/stable/templating/>
- Flask `url_for` reference — <https://flask.palletsprojects.com/en/stable/api/#flask.url_for>
- MDN HTML basics — <https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics>
