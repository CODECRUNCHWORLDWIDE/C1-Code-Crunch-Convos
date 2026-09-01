# Week 9 — Exercises

Four small Flask apps that build on each other. Do them in order; each one
introduces one new idea on top of the previous.

Each exercise is a **page**, not a file you download. It gives you the brief,
a starter you copy into your own `.py` file in your practice repo, the exact
output to aim for, and a list of the errors you are most likely to hit. You
create the files; the page is the prompt.

## Index

| # | Exercise | New idea | Difficulty | Est. time |
|---|----------|----------|-----------:|----------:|
| 1 | [exercise-01-hello-flask.md](./exercise-01-hello-flask.md) | Minimal Flask app, one route | Beginner | 20 min |
| 2 | [exercise-02-multiple-routes.md](./exercise-02-multiple-routes.md) | Multiple routes, URL converters | Easy | 40 min |
| 3 | [exercise-03-template-loop.md](./exercise-03-template-loop.md) | `render_template`, `{% for %}` loop | Easy | 1 hr |
| 4 | [exercise-04-form-echo.md](./exercise-04-form-echo.md) | `POST`, `request.form`, flash | Medium | 1 hr 15 min |

Exercises 1 and 2 are single files. Exercises 3 and 4 are folders, because
Flask looks for templates in a `templates/` directory next to your app. Each
of those pages shows the full directory tree and the complete contents of
every file in it.

---

## How to run

For the single-file exercises (`exercise-01`, `exercise-02`), from the folder
where you saved them:

```bash
python exercise-01-hello-flask.py
```

For the folder-style exercises (`exercise-03`, `exercise-04`):

```bash
cd exercise-03-template-loop
python app.py
```

Then visit <http://127.0.0.1:5000> in your browser.

Stop the server with **Ctrl-C**.

---

## Prerequisites

You need Flask installed, plus `python-dotenv` for exercise 4:

```bash
pip install flask python-dotenv
```

If `python -c "import flask"` runs without error, you are good.

---

## Tips

- Keep the terminal visible while you click around. Every request prints a
  log line; if you do not see one, the request did not reach the server.
- If you change a `.py` file while the server is running with
  `debug=True`, the server auto-reloads. If you change a template, Flask
  re-reads it on the next request — just refresh the browser.
- `debug=True` belongs on your laptop and nowhere else. The debug traceback
  page has an interactive Python console in it, so on a public host it is a
  way for strangers to run code on your machine.
- When something looks wrong, open the browser DevTools Network tab and
  click the request. The status code and response body tell you almost
  everything.
- `curl` is often a better reader than a browser: it shows you the exact
  bytes, does not cache, and does not ask for a favicon. `curl -i URL`
  includes the status line and headers.

---

## What to turn in

Nothing — these are practice. The "real" deliverable for the week is the
mini-project. Use these exercises as a warm-up.
