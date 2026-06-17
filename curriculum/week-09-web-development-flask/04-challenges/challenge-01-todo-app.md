# Challenge 01 — Todo App

Build a small todo app in Flask. The list of todos lives in a Python list in
memory (we will replace this with a real database in Week 10). Restarts
wipe everything — that is fine.

---

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

---

## Suggested data shape

```python
from dataclasses import dataclass, field
from itertools import count

_id_seq = count(1)

@dataclass
class Todo:
    id: int
    text: str
    done: bool = False

TODOS: list[Todo] = []
```

A new todo is created with `Todo(next(_id_seq), text=text)`.

---

## Suggested file layout

```text
todo-app/
├── app.py
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css
```

`index.html` extends `base.html`, loops over the todos, and shows two tiny
forms per row (one to toggle, one to delete) — each is a single submit
button.

---

## Skeleton (start here, fill in the gaps)

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
    app.run(debug=True)
```

You write the templates.

---

## Acceptance checklist

- [ ] Adding a todo flashes "Added." and shows the item.
- [ ] Toggling a todo strikes through (or otherwise styles) the text.
- [ ] Deleting removes the row.
- [ ] Refreshing after any action does NOT re-submit.
- [ ] Visiting `/toggle/9999` (with `curl -X POST`) returns a 404.
- [ ] Empty submissions flash an error and do not add a row.

---

## Stretch goals

- Add a counter at the top: "3 of 8 done."
- Add a "Clear completed" button that posts to `/clear` and removes all
  `done=True` rows.
- Persist `TODOS` to a JSON file on every change, and load it on start. Now
  restarts are not lossy. (You will replace this with SQLite in Week 10.)
- Add `?filter=open|done|all` query-string filtering on the index.
- Show the time each todo was created using `datetime.now()` and the
  Jinja filter `{{ todo.created_at.strftime('%Y-%m-%d %H:%M') }}`.

---

## References

- Flask quickstart — <https://flask.palletsprojects.com/en/stable/quickstart/>
- Flashing pattern — <https://flask.palletsprojects.com/en/stable/patterns/flashing/>
- Jinja `for` loops — <https://jinja.palletsprojects.com/en/stable/templates/#for>
