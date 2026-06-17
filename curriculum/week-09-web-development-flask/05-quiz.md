# Week 9 Quiz — Flask Fundamentals

10 multiple-choice questions covering HTTP methods, Jinja2, routing, the
request object, sessions, and deployment. Try them with your notes closed
first; check the answer key at the bottom and re-read the relevant lecture
section for anything you missed.

---

### 1. Which decorator registers `home` as the handler for `GET /` in Flask?

A. `@app.handler("/")`
B. `@app.route("/")`
C. `@app.get("/")`  *(note: this works in Flask >= 2.0, but the canonical
form is B)*
D. `@route(app, "/")`

---

### 2. What does `app.run(debug=True)` enable that the production server does NOT?

A. Auto-reload on code changes, plus an interactive in-browser traceback.
B. HTTPS support.
C. Database connection pooling.
D. Multiple worker processes.

---

### 3. In the route `@app.route("/post/<int:post_id>")`, what happens when a
user visits `/post/seven`?

A. Flask passes the string `"seven"` to the view function.
B. Flask raises a 500 error.
C. Flask returns a 404 BEFORE the view function runs.
D. Flask coerces the string to `0` and calls the function.

---

### 4. Which of these correctly reads `?q=flask&page=2` from the URL inside a
view function?

A. `q = request.form.get("q")`
B. `q = request.args.get("q", "")`
C. `q = request.query["q"]`
D. `q = request.body.get("q")`

---

### 5. Inside a Jinja2 template, which line is the correct way to render a
variable while letting Jinja escape any HTML it contains?

A. `<p>{% post.title %}</p>`
B. `<p>{{ post.title|safe }}</p>`
C. `<p>{{ post.title }}</p>`
D. `<p>{# post.title #}</p>`

---

### 6. Which template tag prints the 1-based index of the current iteration
inside a `{% for item in items %}` loop?

A. `{{ loop.index }}`
B. `{{ loop.i }}`
C. `{{ index }}`
D. `{{ loop.position }}`

---

### 7. Why must you set `app.secret_key` before using `flash()` or `session`?

A. To encrypt user passwords.
B. To sign the session cookie so it cannot be tampered with.
C. To enable HTTPS.
D. It is optional — Flask works fine without it.

---

### 8. You have a form that creates a new post. After a successful POST, what
should the view function return?

A. `render_template("index.html", ...)`
B. `"OK", 200`
C. `redirect(url_for("index"))` (the Post / Redirect / Get pattern)
D. The new post's HTML directly, as a string.

---

### 9. In a template, what does `{{ url_for('show_post', post_id=3) }}` evaluate to,
assuming the route is `@app.route("/post/<int:post_id>")`?

A. `show_post(3)`
B. `/post/3`
C. `/show_post?post_id=3`
D. `/post?id=3`

---

### 10. Which is the correct production setup for deploying a Flask app to a
free host like Render or Fly.io?

A. `python app.py` with `debug=True`.
B. `gunicorn "app:app" --bind 0.0.0.0:$PORT` with `SECRET_KEY` set as an
   environment variable.
C. Open port 5000 on your laptop and leave it running overnight.
D. Run the Flask CLI's `flask run --debug` in the cloud container.

---

## Answer key

<details>
<summary>Click to expand</summary>

1. **B.** `@app.route("/")` is the canonical form. (C, `@app.get("/")`, is a
   newer shortcut in Flask 2.0+ that is exactly equivalent for `GET`-only
   routes, but B is what most documentation uses.)

2. **A.** Debug mode gives you the auto-reloader and the interactive
   debugger. It does NOT give you HTTPS, pooling, or multi-process workers
   — those are deployment concerns. **Never** run debug mode in production:
   the debugger lets visitors execute Python on your server.

3. **C.** The `<int:>` converter only matches integer-shaped segments. If
   the segment is not parseable as `int`, Flask returns 404 immediately and
   your view function never runs.

4. **B.** Query strings live in `request.args`. `request.form` holds POST
   bodies; the other two attributes do not exist.

5. **C.** `{{ post.title }}` renders with Jinja's default auto-escaping,
   which is what you want 99% of the time. `|safe` *disables* escaping —
   only use it for HTML you generated yourself.

6. **A.** Jinja's special `loop` object exposes `loop.index` (1-based),
   `loop.index0` (0-based), `loop.first`, `loop.last`, and `loop.length`.

7. **B.** Flask sessions are stored in a *signed* cookie. The secret key is
   what makes the signature unforgeable. (Note: signed ≠ encrypted — the
   user can still read the contents, so never put secrets in `session`.)

8. **C.** The Post / Redirect / Get pattern: after a state-changing POST,
   `redirect` to a fresh GET so that refreshing the destination page is
   safe.

9. **B.** `url_for` reverse-resolves the view function name and parameters
   back into the URL pattern. Keyword arguments that match route variables
   fill in the path; anything else becomes a query-string parameter.

10. **B.** Production runs need a real WSGI server (`gunicorn` is the
    standard), bind to all interfaces (`0.0.0.0`), use the host's `$PORT`,
    and load secrets from environment variables — never from code, never
    from a committed file.

</details>
