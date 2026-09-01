"""Every acceptance criterion in the mini-project and homework, checked.

Plain `assert` statements and Flask's built-in test client -- no pytest, which
you do not meet until Week 11. The test client drives the app in-process, so
nothing listens on a port and no browser is involved.

Run:
    python smoke_test.py

Expected last line:
    ALL 46 CHECKS PASSED
"""

from __future__ import annotations

import json
import sys

import app as blog
from weather import CurrentWeather, WeatherError

CHECKS = 0


def check(label: str, condition: bool) -> None:
    """Assert `condition`, counting the check and naming it on failure."""
    global CHECKS
    CHECKS += 1
    if not condition:
        print(f"FAIL: {label}")
        sys.exit(1)
    print(f"  ok  {label}")


def main() -> None:
    blog.app.config["TESTING"] = True
    client = blog.app.test_client()

    # ---------------------------------------------------------------- index
    print("mini-project: GET /")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    check("GET / returns 200", resp.status_code == 200)
    check("index lists the newest post first", body.index("Deploying for free") < body.index("Query strings"))
    check("index shows 5 posts per page", body.count('<article>') == 5)
    check("titles link to the detail page", 'href="/post/7"' in body)
    check("stylesheet linked via url_for", 'href="/static/style.css"' in body)
    check("static file is served", client.get("/static/style.css").status_code == 200)

    # ------------------------------------------------------------ pagination
    print("stretch: pagination")
    page2 = client.get("/?page=2").get_data(as_text=True)
    check("page 2 holds the remaining 2 posts", page2.count("<article>") == 2)
    check("page 2 offers a Newer link", "Newer" in page2)
    check("out-of-range page clamps, no crash", client.get("/?page=99").status_code == 200)

    # ----------------------------------------------------------- single post
    print("mini-project: GET /post/<id>")
    one = client.get("/post/1")
    check("GET /post/1 returns 200", one.status_code == 200)
    check("post page shows the full body", "clearer than f-strings" in one.get_data(as_text=True))

    # ---------------------------------------------- homework 1: custom 404
    print("homework 1: custom 404")
    missing = client.get("/post/9999")
    missing_body = missing.get_data(as_text=True)
    check("GET /post/9999 returns 404", missing.status_code == 404)
    check("404 renders the custom page", "404 — nothing here" in missing_body)
    check("404 wears base.html's layout", "Built with Flask" in missing_body)

    # ------------------------------------------- homework 6: session auth
    print("homework 6: session auth")
    gated = client.get("/new")
    check("unauthenticated /new redirects", gated.status_code == 302)
    check("...to /login", gated.headers["Location"].endswith("/login"))
    check("nav shows 'Log in' when logged out", "Log in" in client.get("/").get_data(as_text=True))

    bad = client.post("/login", data={"password": "nope"}, follow_redirects=True)
    check("wrong password flashes an error", "Wrong password." in bad.get_data(as_text=True))

    good = client.post("/login", data={"password": "letmein"}, follow_redirects=True)
    check("correct password logs in", "Logged in." in good.get_data(as_text=True))
    with client.session_transaction() as sess:
        check("session['is_admin'] is set", sess.get("is_admin") is True)
    check("nav flips to 'Log out'", "Log out" in good.get_data(as_text=True))
    check("authenticated /new renders the form", client.get("/new").status_code == 200)

    # --------------------------------------------- mini-project: POST /new
    print("mini-project: POST /new")
    before = len(blog.POSTS)
    created = client.post(
        "/new",
        data={"title": "Ninth post", "body": "Written by the smoke test.", "tags": "Python, flask,, PYTHON"},
    )
    check("valid POST redirects (PRG)", created.status_code == 302)
    check("a post was appended", len(blog.POSTS) == before + 1)
    landed = client.get("/").get_data(as_text=True)
    check("success flash is rendered", "Post published." in landed)

    empty = client.post("/new", data={"title": "", "body": "kept draft", "tags": ""})
    empty_body = empty.get_data(as_text=True)
    check("empty title re-renders the form (200, not a redirect)", empty.status_code == 200)
    check("...with an error flash", "Title is required." in empty_body)
    check("...and the typed body preserved", 'kept draft' in empty_body)
    check("no post was created", len(blog.POSTS) == before + 1)

    too_long = client.post("/new", data={"title": "x" * 121, "body": "b", "tags": ""})
    check("over-long title is rejected", "Title must be 120 characters or fewer." in too_long.get_data(as_text=True))

    # ------------------------------------------------- homework 4: tags
    print("homework 4: tags")
    newest = blog.POSTS[-1]
    check("tags split, lowered, deduped, empties dropped", newest.tags == ["python", "flask"])
    check("tag pills link out of the index", 'href="/tag/python"' in landed or 'href="/tag/flask"' in landed)
    check("GET /tag/python lists matches", client.get("/tag/python").status_code == 200)
    check("GET /tag/zzz returns 404", client.get("/tag/zzz").status_code == 404)

    # ----------------------------------------------- homework 5: search
    print("homework 5: search")
    hits = client.get("/?q=jinja").get_data(as_text=True)
    check("?q=jinja narrows the list", hits.count("<article>") == 1)
    check("query round-trips into the title", "Search results for 'jinja' (1 found)" in hits)
    check("empty ?q= shows everything again", client.get("/?q=").get_data(as_text=True).count("<article>") == 5)
    check("HTML-looking and unicode input do not 500", client.get("/?q=<script>née</script>").status_code == 200)

    # ------------------------------------------------- autoescaping (XSS)
    print("security: Jinja autoescaping")
    client.post("/new", data={"title": "<script>alert(1)</script>", "body": "xss probe", "tags": ""})
    escaped = client.get("/").get_data(as_text=True)
    check("script tags are escaped, not executed", "&lt;script&gt;alert(1)&lt;/script&gt;" in escaped)

    # ------------------------------------------------- homework 3: weather
    print("homework 3: weather route")
    check("GET /weather shows the search form", 'name="city"' in client.get("/weather").get_data(as_text=True))

    blog.get_current_weather = lambda city, **kw: CurrentWeather(
        city="London", country="United Kingdom", temp=11.4, unit="°C", description="Overcast"
    )
    ok_weather = client.get("/weather?city=London").get_data(as_text=True)
    check("?city=London renders the reading", "11.4" in ok_weather and "Overcast" in ok_weather)

    def boom(city: str, **kw: object) -> CurrentWeather:
        raise WeatherError("No city called 'Nowheresville' was found.")

    blog.get_current_weather = boom
    failed = client.get("/weather?city=Nowheresville")
    check("a bad city flashes cleanly, no traceback", failed.status_code == 200
          and "No city called" in failed.get_data(as_text=True))

    # ------------------------------------------------------ stretch routes
    print("stretch: /api/posts and /healthz")
    api = client.get("/api/posts")
    payload = json.loads(api.get_data(as_text=True))
    check("/api/posts returns JSON", api.headers["Content-Type"].startswith("application/json"))
    check("/api/posts carries every post", len(payload) == len(blog.POSTS))
    health = client.get("/healthz")
    check("/healthz returns OK, 200", health.status_code == 200 and health.get_data(as_text=True) == "OK")

    # ------------------------------------------------------------- logout
    print("homework 6: logout")
    client.post("/logout")
    with client.session_transaction() as sess:
        check("logout clears is_admin", "is_admin" not in sess)

    print(f"\nALL {CHECKS} CHECKS PASSED")


if __name__ == "__main__":
    main()
