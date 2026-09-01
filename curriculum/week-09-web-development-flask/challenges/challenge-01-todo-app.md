# Challenge 01 — Todo App

> **Topic:** routes, forms, in-memory state, template inheritance, and the Post/Redirect/Get pattern, all in one small app
> **Lecture:** [01 — Flask Hello World](../lecture-notes/01-flask-hello-world.md) · [02 — Templates and Static Files](../lecture-notes/02-templates-and-static.md) · [03 — Forms, Sessions, and Deployment](../lecture-notes/03-forms-sessions-deployment.md)
> **Difficulty:** Intermediate
> **Target time:** 2–4 hours
> **Why this one:** every move the mini-project needs — a form that validates on the server, a `POST` that redirects, a template that inherits its layout, a clean 404 for a bad id — is rehearsed here at half the size. And the twist is instructive: the Python you are handed already works. The part you have to build is the templates, which is exactly the part beginners underestimate.

## The Brief

Build a small todo app in Flask. The list of todos lives in a Python list in
memory (Week 10 replaces this with a real database). Restarts wipe
everything — that is fine.

Every visitor sees the same list, because module-level state is shared by the
whole process. That is also fine this week, and noticing *why* it is true —
the list lives in the module, not in any request — is one of the things this
challenge is for.

Read the skeleton below carefully before you write anything, because it is
not a stub: the five view functions already satisfy every requirement on this
page. What does not exist yet is `base.html` and `index.html`. The challenge
is to write templates good enough that the working Python shows through —
an add form, a count, one row per todo with a toggle button and a delete
button, flash messages, and an empty state.

## Starter

Suggested file layout:

```text
todo-app/
├── app.py
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css
```

Save this as `app.py`. It runs as pasted — until you write the templates,
every page load is a `TemplateNotFound`, which is your to-do list in error
form.

```python
"""Tiny in-memory todo app."""
from dataclasses import dataclass
from itertools import count

from flask import (
    Flask, abort, flash, redirect, render_template, request, url_for,
)

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

_id_seq = count(1)


@dataclass
class Todo:
    id: int
    text: str
    done: bool = False


TODOS: list[Todo] = []


def find_todo(todo_id: int) -> Todo:
    for t in TODOS:
        if t.id == todo_id:
            return t
    abort(404)


@app.route("/")
def index() -> str:
    return render_template("index.html", todos=TODOS)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if not text:
        flash("Todo text cannot be empty.", "error")
    elif len(text) > 200:
        flash("Todo text must be 200 characters or fewer.", "error")
    else:
        TODOS.append(Todo(next(_id_seq), text=text))
        flash("Added.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id: int):
    todo = find_todo(todo_id)
    todo.done = not todo.done
    flash("Marked done." if todo.done else "Marked undone.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id: int):
    todo = find_todo(todo_id)
    TODOS.remove(todo)
    flash("Deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

A new todo is created with `Todo(next(_id_seq), text=text)` — the
`itertools.count` object hands out 1, 2, 3, … and never repeats, so ids stay
unique without any bookkeeping.

You write the templates. `index.html` extends `base.html`, loops over the
todos, and shows two tiny forms per row (one to toggle, one to delete) —
each is a single submit button.

## Requirements

Your app must:

1. Show a list of todos at `GET /` with the count and each item's text.
2. Let the user add a todo via a form on the same page (`POST /add`).
3. Let the user mark a todo as **done** via a form button on each row
   (`POST /toggle/<int:todo_id>`).
4. Let the user delete a todo via a form button on each row
   (`POST /delete/<int:todo_id>`).
5. Flash a success message after each add/toggle/delete.
6. 404 cleanly when the user posts to `/toggle/999` or `/delete/999` for a
   non-existent id.

Use the Post / Redirect / Get pattern so refreshing never re-submits.

## Constraints

- **Toggle and delete are forms, not links.** An `<a href="/delete/3">` is a
  `GET`, and `GET` must never change state — not as a style rule but because
  the world will punish you for it. Browsers pre-fetch links, address bars
  pre-render them, and corporate mail scanners follow every URL they see. Any
  of those would silently empty your todo list. The routes are registered
  `methods=["POST"]` only, so a link cannot even reach them.
- **Every mutation ends in `redirect(url_for(...))`, never in
  `render_template(...)`.** That is the whole Post/Redirect/Get pattern: the
  page the user is looking at must always be the product of a `GET`, so a
  refresh re-issues something harmless.
- **The flash widget lives in `base.html`, not in `index.html`.** Read the
  queue once, in the layout, on every page. Rendered in one page template
  only, flashes queued on the way to any other page pile up unread and then
  dump out somewhere surprising.
- **Build the row controls with `url_for('toggle', todo_id=todo.id)`.** No
  hand-written `/toggle/3` strings. The keyword must match the route variable
  name — `todo_id` — not the attribute you read it from.
- **Keep `app.secret_key` set.** `flash` writes to the session, and the
  session is a signed cookie: no key, no signature, no flash. The hardcoded
  dev value is acceptable for a challenge that stores nothing; exercise 4
  showed the environment-variable pattern real apps use.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python challenge-01-todo-app-solution.py
GET  /                    -> 200
  <p class="count">0 todos.</p>
  <li class="empty">Nothing to do. Suspicious.</li>

POST /add text='Buy milk' -> 302  Location: /
  <li class="flash flash-success">Added.</li>
  <p class="count">1 todo.</p>
  <span class="text">Buy milk</span>

POST /add text='   '      -> 302, then:
  <li class="flash flash-error">Todo text cannot be empty.</li>
  todos stored: 1 (nothing was added)

POST /toggle/1            -> 302, then:
  <li class="flash flash-success">Marked done.</li>
  <li class="todo done">

The failure paths, all clean:
  GET  /toggle/1  -> 405 (a link cannot toggle; only a form can)
  POST /toggle/9999 -> 404
  POST /delete/9999 -> 404

POST /delete/1            -> 302, then:
  <li class="flash flash-success">Deleted.</li>
  <p class="count">0 todos.</p>
```

**The shipped file starts no server** — it walks the acceptance checklist
with `app.test_client()`, printing what each round trip proved, and exits.
Your own build ends in `app.run(debug=True)` and you click through the same
sequence in a browser, watching the terminal log a `302` and a `200` for
every button press.

## Steps

1. Create the folder, paste the skeleton into `app.py`, and run it. Load
   <http://127.0.0.1:5000> and read the `TemplateNotFound` traceback — it
   names the file it wants, which is your next move.
2. Write `base.html` first: doctype, head, a header with the app name, the
   flash widget from lecture 3, a `{% block content %}{% endblock %}`, and a
   footer. Nothing else.
3. Write `index.html` as `{% extends "base.html" %}` plus a content block
   holding the add form and an empty `<ul>`. Reload — the page renders, the
   form posts, and flashes appear. That is requirement 2 and 5 working.
4. Add the todo loop: one `<li>` per todo with the text and the two
   single-button forms. Use `{% else %}` on the loop for the empty state.
5. Add the count line with `{{ todos|length }}`, not a number you typed.
6. Click through every requirement: add, add-empty, toggle, toggle back,
   delete, refresh after each. No refresh may re-submit.
7. Test the failure paths on purpose: `curl -X POST` to `/toggle/9999`, and a
   plain `GET` to `/toggle/1`. A `404` and a `405` — and know why they
   differ before moving on.
8. Style it. `static/style.css`, linked from `base.html` with
   `url_for('static', filename='style.css')`. A `form.inline { display:
   inline; }` rule is the one you will actually need — forms are block
   elements and will otherwise stack your buttons vertically.

## The Solution

```python
"""challenge-01-todo-app-solution.py — the todo app, proven headless.

The app is the challenge skeleton, unchanged — it already satisfies all six
requirements, and noticing that is half the lesson. The two templates are the
part you had to write yourself, and they are here in full.

Your own build keeps `base.html` and `index.html` in a `templates/` folder
and a stylesheet in `static/`. This download carries the templates inside the
file, handed to Jinja through a ``DictLoader``, so one file runs anywhere.
And instead of ending in ``app.run(debug=True)`` and waiting for a browser,
it drives the app with ``app.test_client()`` — Flask's in-process fake
browser, cookie jar included — walks the whole acceptance checklist, prints
each round trip, and exits.

Run it with::

    python challenge-01-todo-app-solution.py
"""

from dataclasses import dataclass
from itertools import count

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from jinja2 import DictLoader

#: templates/base.html — layout, flash widget, stylesheet link. Everything
#: that is true of every page lives here exactly once.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Todos{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('index') }}">Todos</a></h1>
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
      <small>In memory only. A restart wipes the list.</small>
    </footer>
  </body>
</html>
"""

#: templates/index.html — the add form, the count, and one row per todo with
#: its two single-button forms.
INDEX_HTML: str = """\
{% extends "base.html" %}

{% block title %}Todos ({{ todos|length }}){% endblock %}

{% block content %}
  <form class="add" method="post" action="{{ url_for('add') }}">
    <label for="text">New todo</label>
    <input type="text" id="text" name="text" maxlength="200"
           placeholder="Finish challenge 01" autofocus>
    <button type="submit">Add</button>
  </form>

  <p class="count">{{ todos|length }} todo{{ '' if todos|length == 1 else 's' }}.</p>

  <ul class="todos">
    {% for todo in todos %}
      <li class="todo {{ 'done' if todo.done else 'open' }}">
        <span class="text">{{ todo.text }}</span>
        <form class="inline" method="post"
              action="{{ url_for('toggle', todo_id=todo.id) }}">
          <button type="submit">{{ 'Undo' if todo.done else 'Done' }}</button>
        </form>
        <form class="inline" method="post"
              action="{{ url_for('delete', todo_id=todo.id) }}">
          <button type="submit" class="danger">Delete</button>
        </form>
      </li>
    {% else %}
      <li class="empty">Nothing to do. Suspicious.</li>
    {% endfor %}
  </ul>
{% endblock %}
"""

app = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "index.html": INDEX_HTML})
app.secret_key = "dev-only-change-me"

_id_seq = count(1)


@dataclass
class Todo:
    id: int
    text: str
    done: bool = False


TODOS: list[Todo] = []


def find_todo(todo_id: int) -> Todo:
    for t in TODOS:
        if t.id == todo_id:
            return t
    abort(404)


@app.route("/")
def index() -> str:
    return render_template("index.html", todos=TODOS)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if not text:
        flash("Todo text cannot be empty.", "error")
    elif len(text) > 200:
        flash("Todo text must be 200 characters or fewer.", "error")
    else:
        TODOS.append(Todo(next(_id_seq), text=text))
        flash("Added.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id: int):
    todo = find_todo(todo_id)
    todo.done = not todo.done
    flash("Marked done." if todo.done else "Marked undone.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id: int):
    todo = find_todo(todo_id)
    TODOS.remove(todo)
    flash("Deleted.", "success")
    return redirect(url_for("index"))


def line_with(page: str, needle: str) -> str:
    """Return the first line of *page* containing *needle*, stripped."""
    for line in page.splitlines():
        if needle in line:
            return line.strip()
    return f"(no line contains {needle!r})"


def flash_lines(page: str) -> list[str]:
    """Pull the rendered flash <li> lines out of a page, stripped."""
    return [line.strip() for line in page.splitlines() if 'class="flash ' in line]


def main() -> None:
    """Walk the acceptance checklist and print every round trip."""
    client = app.test_client()

    body = client.get("/").get_data(as_text=True)
    print("GET  /                    -> 200")
    print(f"  {line_with(body, 'class=\"count\"')}")
    print(f"  {line_with(body, 'class=\"empty\"')}")

    print()
    response = client.post("/add", data={"text": "Buy milk"})
    print(f"POST /add text='Buy milk' -> {response.status_code}  Location: {response.headers['Location']}")
    body = client.get("/").get_data(as_text=True)
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"  {line_with(body, 'class=\"count\"')}")
    print(f"  {line_with(body, 'class=\"text\"')}")

    print()
    response = client.post("/add", data={"text": "   "}, follow_redirects=True)
    print("POST /add text='   '      -> 302, then:")
    for line in flash_lines(response.get_data(as_text=True)):
        print(f"  {line}")
    print(f"  todos stored: {len(TODOS)} (nothing was added)")

    print()
    todo_id = TODOS[0].id
    response = client.post(f"/toggle/{todo_id}", follow_redirects=True)
    print(f"POST /toggle/{todo_id}            -> 302, then:")
    body = response.get_data(as_text=True)
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"  {line_with(body, '<li class=\"todo ')}")

    print()
    print("The failure paths, all clean:")
    print(f"  GET  /toggle/{todo_id}  -> {client.get(f'/toggle/{todo_id}').status_code} (a link cannot toggle; only a form can)")
    print(f"  POST /toggle/9999 -> {client.post('/toggle/9999').status_code}")
    print(f"  POST /delete/9999 -> {client.post('/delete/9999').status_code}")

    print()
    response = client.post(f"/delete/{todo_id}", follow_redirects=True)
    print(f"POST /delete/{todo_id}            -> 302, then:")
    body = response.get_data(as_text=True)
    for line in flash_lines(body):
        print(f"  {line}")
    print(f"  {line_with(body, 'class=\"count\"')}")


if __name__ == "__main__":
    main()
```

**Every mutation is a `POST`, and every `POST` ends in a redirect.** That is
the Post/Redirect/Get pattern, and it is the whole reason the app feels
normal. When you click **Done**, the browser experiences
`POST /toggle/3 -> 302` then `GET / -> 200`. The page you are *looking at*
was produced by a `GET`; refresh it and the browser re-issues that `GET` —
harmless. Had `toggle` returned `render_template(...)` directly, refresh
would re-toggle, and you would meet the "Confirm Form Resubmission" dialog
you have seen on badly built sites.

**Toggle and delete are forms because a link is a `GET`.** Each row carries
two one-button forms, and the routes accept `POST` only — which is why the
shipped run shows `GET /toggle/1 -> 405`, not a toggled todo. The `405` is
Werkzeug saying "the URL matched, the method did not", and its `Allow:
POST, OPTIONS` header names what it wanted. This is also why the CSS needs
`form.inline { display: inline; }` — a `<form>` is a block element and would
otherwise shove each button onto its own line.

**`abort(404)` unwinds the request.** `find_todo` is annotated `-> Todo` even
though the loop can fall through, and that is honest: `flask.abort` raises
`werkzeug.exceptions.NotFound`, Flask catches it at the top of the request,
and nothing after the `abort` in *any* caller runs. That is what lets
`toggle` say `todo = find_todo(todo_id)` on line one and then use `todo`
fearlessly.

**`TODOS.remove(todo)` works because `@dataclass` generates `__eq__`.**
`list.remove` scans for the first item that compares equal, and a dataclass
compares field-by-field. Since `id` comes from `itertools.count`, no two
todos are ever equal, so exactly the intended row is removed.

**`{{ todos|length }}` instead of `len(todos)`.** Jinja has no `len`; it has
a `length` filter. The pluralisation trick,
`{{ '' if todos|length == 1 else 's' }}`, is Jinja's inline conditional — the
same shape as Python's ternary.

**Where the state lives is the quiet lesson.** `TODOS` is a module-level
list: it survives between requests, dies on restart, and is shared by every
visitor at once. The flash messages live in the signed session cookie, so
they are per-browser and consumed the first time they render. Nothing lives
in a view-function local, because a view function is called once per request
and forgets everything when it returns.

## Download and run

Download
[challenge-01-todo-app-solution.py](./challenge-01-todo-app-solution.py)
and run it:

```bash
python challenge-01-todo-app-solution.py
```

It needs Flask installed and nothing else, and it exits on its own — the two
templates travel inside the file, so no `templates/` folder is required. To
click around the same app in a browser, build the folder version this page
assigns; the Python is identical, and the templates in the constants above
are exactly the two files you were asked to write.

The `-solution` in the filename keeps this file from colliding with your own
`app.py`.

## Common bugs to catch

- **`405 Method Not Allowed` when you click Done or Delete.** You made the
  control an `<a href=...>` link. A link is a `GET`, and the route accepts
  `POST` only. The `Allow: POST, OPTIONS` header in the response names what
  the route wanted. Do not "fix" this by adding `"GET"` to `methods=` — fix
  it by making the control a form.

- **`werkzeug.routing.exceptions.BuildError: Could not build url for
  endpoint 'toggle' with values ['id']. Did you forget to specify values
  ['todo_id']?`** `url_for('toggle', id=todo.id)` looks reasonable and blows
  up at render time. The keyword has to match the *route variable name* —
  `<int:todo_id>` — not the attribute you read it from. Werkzeug even names
  the one you meant.

- **`RuntimeError: The session is unavailable because no secret key was set.
  Set the secret_key on the application to something unique and secret.`**
  You removed or forgot `app.secret_key`. The app boots and `/` renders —
  the explosion waits for the first `flash()`, because `flash` is a list
  stored in the session and the session is a signed cookie. No key, no
  signature, no session, no flash.

- **`jinja2.exceptions.TemplateNotFound: index.html`.** The template is not
  at `templates/index.html` relative to where the app started. Check for
  `template/` singular, and check which directory you launched `python
  app.py` from.

- **Flashes appear late, in a clump, on the wrong page.** You rendered
  `get_flashed_messages()` in `index.html` instead of `base.html`. It works
  until a second page exists; then flashes queued on the way to that page
  pile up unread and dump onto the next page that happens to render the
  widget. Read the queue once, in the layout.

- **Refreshing after an action re-submits it.** One of your mutating views
  returns `render_template(...)` instead of `redirect(url_for("index"))`.
  The tell is the status code in the terminal: a mutation should always log
  `302`, never `200`.

## Under the hood

<details>
<summary>Under the hood — why the id comes from itertools.count and not len(TODOS)</summary>

The tempting id scheme is `len(TODOS) + 1`. It works until the first delete:
add three todos, delete the second, add another — `len` is 3 again, so the
new todo gets id 3, which the third todo already holds. Now `find_todo`
returns whichever one it meets first, and `delete` removes the wrong row.

`itertools.count(1)` never re-issues a number, because it never looks at the
list at all — it is an independent, infinite iterator, and `next(_id_seq)`
is the only way anything touches it. Uniqueness by construction beats
uniqueness by bookkeeping.

The same idea has a second act in the stretch goals: the moment you persist
todos to a file and reload them on start-up, you must also persist *the
counter's position* — `count(max(ids) + 1)` — or the first new todo after a
restart collides with an old id. Any time auto-incrementing ids outlive the
process, the counter has to outlive it too. Week 10 hands the whole problem
to SQLite's `INTEGER PRIMARY KEY`, which is one of the quieter arguments for
using a database.

</details>

## Acceptance checklist

- [ ] Adding a todo flashes "Added." and shows the item.
- [ ] Toggling a todo strikes through (or otherwise styles) the text.
- [ ] Deleting removes the row.
- [ ] Refreshing after any action does NOT re-submit.
- [ ] Visiting `/toggle/9999` (with `curl -X POST`) returns a 404.
- [ ] A plain `GET` to `/toggle/<id>` returns a 405, and you can say why.
- [ ] Empty submissions flash an error and do not add a row.
- [ ] The flash widget lives in `base.html`, and every mutation logs a `302`.

## Stretch

- Add a counter at the top: "3 of 8 done."
- Add a "Clear completed" button that posts to `/clear` and removes all
  `done=True` rows.
- Persist `TODOS` to a JSON file on every change, and load it on start. Now
  restarts are not lossy — and re-read the Under the hood block before you
  do, because the id counter has to be persisted too. (You will replace this
  with SQLite in Week 10.)
- Add `?filter=open|done|all` query-string filtering on the index. Validate
  against a whitelist and fall back to `all` — anything a user can type into
  a URL bar is untrusted input, including the harmless-looking parts.
- Show the time each todo was created using `datetime.now()` and the
  Jinja filter `{{ todo.created_at.strftime('%Y-%m-%d %H:%M') }}`.

References:

- Flask quickstart — <https://flask.palletsprojects.com/en/stable/quickstart/>
- Flashing pattern — <https://flask.palletsprojects.com/en/stable/patterns/flashing/>
- Jinja `for` loops — <https://jinja.palletsprojects.com/en/stable/templates/#for>
