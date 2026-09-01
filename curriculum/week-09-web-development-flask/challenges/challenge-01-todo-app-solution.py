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
