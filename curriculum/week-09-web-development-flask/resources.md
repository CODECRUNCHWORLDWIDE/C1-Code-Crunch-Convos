# Week 9 Resources — Flask, Jinja2, and Friends

Curated, beginner-friendly references for everything covered this week. Skim
each link's table of contents at least once so you know where to come back
when you get stuck.

---

## Official documentation (read these first)

- **Flask documentation** — <https://flask.palletsprojects.com/>
  The canonical reference. Start with the *Quickstart*; come back for the
  *Tutorial* once you finish this week.
- **Flask Quickstart** — <https://flask.palletsprojects.com/en/stable/quickstart/>
  A 30-minute tour of routes, templates, requests, and sessions. This is the
  single best link on this page; read it once before lecture 1 and once after
  lecture 3.
- **Flask Tutorial (Flaskr)** — <https://flask.palletsprojects.com/en/stable/tutorial/>
  Walks you through a small blog app called Flaskr — very close to our
  mini-project, but with SQLite (which you will meet in Week 10).
- **Jinja2 documentation** — <https://jinja.palletsprojects.com/>
  Jinja is the template engine Flask ships with. The *Template Designer
  Documentation* page is the one you will bookmark.
- **Werkzeug** — <https://werkzeug.palletsprojects.com/>
  The WSGI utility library that powers Flask. You will rarely import it
  directly, but `request`, `Response`, and the routing system come from here.

---

## HTML and CSS refreshers

- **MDN — HTML basics** — <https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics>
  Tags, attributes, nesting, document structure. 15-minute read.
- **MDN — CSS first steps** — <https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps>
  Selectors, the box model, and how to link a stylesheet. Enough CSS to make
  your blog not look like 1995.
- **MDN — HTML forms** — <https://developer.mozilla.org/en-US/docs/Learn/Forms>
  Every form attribute you will see this week, with examples.

---

## Tutorials and long-form reading

- **Real Python — Flask by Example** — <https://realpython.com/tutorials/flask/>
  A library of tutorials at every level. Start with *Flask by Example, Part 1*.
- **Miguel Grinberg — The Flask Mega-Tutorial** — <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world>
  The definitive long-form Flask course on the internet. 20+ chapters. You
  don't need all of it now, but bookmark it for Weeks 10–12.
- **Patrick Kennedy — TestDriven.io Flask track** — <https://testdriven.io/courses/learn-flask/>
  Mostly paid, but the blog has many excellent free articles.

---

## Sessions, security, and forms

- **Flask — Sessions** — <https://flask.palletsprojects.com/en/stable/quickstart/#sessions>
- **Flask — Message Flashing** — <https://flask.palletsprojects.com/en/stable/patterns/flashing/>
- **OWASP Cheat Sheet — Cross-Site Request Forgery (CSRF)** —
  <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- **Flask-WTF** — <https://flask-wtf.readthedocs.io/>
  Adds form classes and CSRF protection. Optional for this week, recommended
  for any real project.

---

## Application factory and blueprints

- **Flask — Application Factories** — <https://flask.palletsprojects.com/en/stable/patterns/appfactories/>
- **Flask — Modular Applications with Blueprints** —
  <https://flask.palletsprojects.com/en/stable/blueprints/>

---

## Deployment

- **Flask — Deploying to Production** — <https://flask.palletsprojects.com/en/stable/deploying/>
- **Fly.io — Python (Flask) docs** — <https://fly.io/docs/python/>
- **Render — Deploy a Flask app** — <https://render.com/docs/deploy-flask>
- **Railway — Flask quickstart** — <https://docs.railway.app/guides/flask>
- **Gunicorn** — <https://gunicorn.org/> — the production WSGI server you will
  use behind any of the hosts above.

---

## Secrets and config

- **`python-dotenv`** — <https://pypi.org/project/python-dotenv/>
- **The Twelve-Factor App — Config** — <https://12factor.net/config>
  Why secrets belong in environment variables, not in your code.

---

## Cheat sheets and quick references

- **Flask quick reference (PDF)** — search "Flask cheat sheet" on
  <https://www.pythoncheatsheet.org/> for a one-page handout.
- **Jinja2 template designer docs** — <https://jinja.palletsprojects.com/en/stable/templates/>
  Bookmark this. The list of built-in filters
  (<https://jinja.palletsprojects.com/en/stable/templates/#list-of-builtin-filters>)
  is gold.

---

## Videos (optional, for visual learners)

- **Corey Schafer — Flask tutorials** on YouTube — search "Corey Schafer
  Flask". The first 5 episodes mirror Weeks 9–10 of this bootcamp almost
  exactly.
- **Tech With Tim — Flask in 1 hour** — good overview to watch *before* you
  read lecture 1.

---

## Tooling

- **`httpie`** — <https://httpie.io/> — a friendly `curl` alternative for
  poking at your own routes.
- **Visual Studio Code — Python extension** — has a "Flask: Launch" debug
  configuration baked in.
- **Browser DevTools** — open the Network tab while your Flask app is running.
  Watching requests fly by is the fastest way to understand HTTP.
