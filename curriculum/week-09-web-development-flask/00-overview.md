# Week 9 — Web Development with Flask

Welcome to Week 9 of **Code Crunch Convos**. Last week you learned to *consume*
HTTP APIs with `requests`. This week you turn the tables and **serve** HTTP
yourself: you will write a tiny web application in **Flask**, render HTML
templates with **Jinja2**, handle form submissions, store data temporarily in
sessions, and (optionally) deploy your app for free on the public internet.

By the end of the week you will have built a **personal blog web app** —
multiple posts, a single-post page, a "create post" form, and a tiny CSS
stylesheet — running locally and (if you choose) reachable from any phone or
laptop in the world.

This is the week where Python stops being "a script you run" and starts being
"a service other people can use".

---

## Learning objectives

After this week you will be able to:

1. Describe the **client/server model** and what an HTTP **request** and
   **response** look like at the wire level.
2. Explain what a **web framework** does, what **WSGI** is, and where Flask
   fits in the Python web ecosystem.
3. Install Flask, write a minimal app, and run it with the development server
   in debug mode.
4. Define **routes** with `@app.route(...)` and write **view functions** that
   return strings, HTML, redirects, and status codes.
5. Capture **URL parameters** (`/post/<int:post_id>`) and read **query strings**
   from `request.args`.
6. Render **Jinja2 templates** with `render_template`, including variable
   interpolation, `{% if %}` / `{% for %}` control flow, filters, includes,
   and template inheritance with `{% extends %}` / `{% block %}`.
7. Serve **static files** (CSS, images, JS) from the `static/` folder and link
   them with `url_for('static', filename=...)`.
8. Build **HTML forms**, handle **GET vs POST**, read `request.form`, and do
   basic server-side validation.
9. Use **flash messages** and **sessions** (with a real secret key), and
   understand why sessions need one.
10. Sketch out a small project using the **application factory** pattern and
    **blueprints**, and know when those tools earn their weight.
11. Deploy a Flask app for free to a host like Fly.io, Render, or Railway, and
    keep secrets out of the repo with `python-dotenv`.

---

## Prerequisites

You should be comfortable with everything from Weeks 1–8:

- **Week 1–5** — Python syntax, control flow, functions, data structures.
- **Week 6** — reading files, exception handling, context managers.
- **Week 7** — classes and `@dataclass` (we will use a `Post` dataclass).
- **Week 8** — HTTP basics: methods (`GET`, `POST`), status codes (`200`,
  `404`, `500`), headers, JSON. **If you skipped Week 8, read the HTTP section
  there before starting lecture 1.**

You do not need to be an HTML/CSS expert. You will see just enough HTML to be
dangerous, and we will keep the CSS deliberately small.

---

## Topics covered

- Web app fundamentals: client/server, request/response, HTML/CSS/JS in one
  paragraph each
- WSGI and where Flask sits
- Flask Hello World
- Routes and view functions
- URL converters (`<int:>`, `<string:>`, `<path:>`) and query strings
- Jinja2 templates: variables, filters, control flow, includes, layouts
- `render_template` and `url_for`
- Static files: CSS, images, favicon
- Forms: GET vs POST, `request.form`, server-side validation
- Flash messages and `session` (and the `SECRET_KEY`)
- Application factory pattern and blueprints (light)
- Free deployment: Fly.io, Render, Railway (overview)
- `python-dotenv` for secrets, `gunicorn` as a production WSGI server

---

## Suggested schedule (~36 hours)

| Day | Focus                                                       | Hours |
|----:|-------------------------------------------------------------|------:|
| 1   | Read `lecture-notes/01-flask-hello-world.md`                |   4   |
| 2   | Exercises 01–02 (hello, multiple routes)                    |   4   |
| 3   | Read `lecture-notes/02-templates-and-static.md`             |   5   |
| 4   | Exercise 03 (template loop) + Challenge 01 (todo app)       |   5   |
| 5   | Read `lecture-notes/03-forms-sessions-deployment.md`        |   5   |
| 6   | Exercise 04 (form echo) + Challenge 02 (URL shortener)      |   5   |
| 7   | Quiz + homework problems                                    |   4   |
| 8   | Mini-project: personal blog                                 |   4   |

Total: **~36 hours**. The mini-project is the centerpiece — if any lecture
clicks fast, spend the saved time polishing the blog.

---

## Navigation

```text
week-09-web-development-flask/
├── README.md                    <- you are here
├── resources.md
├── quiz.md
├── homework.md
├── lecture-notes/
│   ├── 01-flask-hello-world.md
│   ├── 02-templates-and-static.md
│   └── 03-forms-sessions-deployment.md
├── exercises/
│   ├── README.md
│   ├── exercise-01-hello-flask.py
│   ├── exercise-02-multiple-routes.py
│   ├── exercise-03-template-loop/
│   │   ├── app.py
│   │   └── templates/list.html
│   └── exercise-04-form-echo/
│       ├── app.py
│       └── templates/form.html
├── challenges/
│   ├── README.md
│   ├── challenge-01-todo-app.md
│   └── challenge-02-url-shortener.md
└── mini-project/
    ├── README.md
    └── starter/
        ├── app.py
        ├── templates/
        │   ├── base.html
        │   └── index.html
        └── static/style.css
```

**Recommended order:** lecture 01 → exercises 01–02 → lecture 02 → exercise 03
→ challenge 01 → lecture 03 → exercise 04 → challenge 02 → quiz → homework →
mini-project.

---

## Setup

You only need one new package this week:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install flask python-dotenv
```

Verify the install:

```bash
python -c "import flask; print(flask.__version__)"
```

You should see something like `3.0.0` or newer. Flask 2.x will also work for
everything in this module; if you are on Flask 1.x, upgrade.

---

## Stretch goals

If you finish early, pick any of these:

- Add **pagination** to the blog index (`/?page=2`) so it only shows 5 posts
  per page.
- Add a JSON endpoint `/api/posts` that returns your posts as a JSON array
  (bringing back Week 8 skills from the server side).
- Convert the blog from in-memory storage to a **`pickle` file** that survives
  restarts. (Week 10 will replace this with a real database.)
- Style the blog with a tiny CSS framework like
  [Pico.css](https://picocss.com/) — drop in one `<link>` tag and admire the
  result.
- Add a `/healthz` route that returns `OK, 200` for load-balancer health
  checks, then deploy and curl it from your phone.
- Read about **CSRF protection** in the Flask docs and add `Flask-WTF` to your
  create-post form.

---

## Up next

**Week 10 — Databases & SQL.** Your blog will graduate from a Python list
stored in memory to a real **SQLite** database that survives restarts. You
will learn `SELECT` / `INSERT` / `UPDATE` / `DELETE`, table design, and how to
wire SQLite into Flask through `sqlite3` and (briefly) SQLAlchemy. The Flask
patterns you learn this week are exactly the shape of the views you will write
on top of that database.

See `../week-10-databases-sql/`.
