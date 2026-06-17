# Week 9 — Exercises

Four small, runnable Flask apps that build on each other. Do them in order;
each one introduces one new idea on top of the previous.

| # | File                                              | New idea                              |
|---|---------------------------------------------------|---------------------------------------|
| 1 | `exercise-01-hello-flask.py`                      | Minimal Flask app, one route          |
| 2 | `exercise-02-multiple-routes.py`                  | Multiple routes, URL converters       |
| 3 | `exercise-03-template-loop/app.py` + template     | `render_template`, `{% for %}` loop   |
| 4 | `exercise-04-form-echo/app.py` + template         | `POST`, `request.form`, flash         |

---

## How to run

For the single-file exercises (`exercise-01`, `exercise-02`):

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

You need Flask installed:

```bash
pip install flask
```

If `python -c "import flask"` runs without error, you are good.

---

## Tips

- Keep the terminal visible while you click around. Every request prints a
  log line; if you do not see one, the request did not reach the server.
- If you change a `.py` file while the server is running with
  `debug=True`, the server auto-reloads. If you change a template, Flask
  re-reads it on the next request — just refresh the browser.
- When something looks wrong, open the browser DevTools Network tab and
  click the request. The status code and response body tell you almost
  everything.

---

## What to turn in

Nothing — these are practice. The "real" deliverable for the week is the
mini-project. Use these exercises as a warm-up.
