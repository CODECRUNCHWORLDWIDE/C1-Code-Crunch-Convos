"""
Exercise 03 — Render a list of items with a Jinja2 template
===========================================================

Goal
----
Render an HTML page that loops over a Python list and prints one item per
line. Use `render_template` instead of building HTML by hand.

Layout
------
    exercise-03-template-loop/
    ├── app.py                  <- this file
    └── templates/
        └── list.html

Run it
------
    cd exercise-03-template-loop
    python app.py

Then visit:
    http://127.0.0.1:5000/

You should see a heading and a numbered list of items.

What to notice
--------------
* The `templates/` folder MUST sit next to `app.py`. Flask discovers it
  automatically.
* `render_template("list.html", items=ITEMS, title="My favourite languages")`
  passes `items` and `title` into the template as variables.
* Inside the template `{% for x in items %}` is a Jinja `for` loop;
  `{{ loop.index }}` gives a 1-based counter.
* `{% if items %} ... {% else %} ... {% endif %}` handles the empty-list
  case cleanly.

Stretch
-------
* Pass `items=[]` and reload — confirm the "no items yet" branch fires.
* Add a second route `/sorted` that passes `sorted(ITEMS)` to the same
  template.
* Use a Jinja filter: change `{{ item }}` to `{{ item|upper }}` and see
  the difference.
* Read about `loop.first` and `loop.last` and bold the first/last item.

References
----------
* `render_template`: https://flask.palletsprojects.com/en/stable/api/#flask.render_template
* Jinja for loops: https://jinja.palletsprojects.com/en/stable/templates/#for
"""
from flask import Flask, render_template

app: Flask = Flask(__name__)

ITEMS: list[str] = ["Python", "Flask", "Jinja2", "HTML", "CSS"]


@app.route("/")
def index() -> str:
    """Render the list of items as an HTML page."""
    return render_template(
        "list.html",
        title="My favourite web-stack pieces",
        items=ITEMS,
    )


if __name__ == "__main__":
    app.run(debug=True)
