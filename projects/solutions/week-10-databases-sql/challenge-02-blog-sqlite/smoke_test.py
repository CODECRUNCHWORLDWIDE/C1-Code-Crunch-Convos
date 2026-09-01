#!/usr/bin/env python3
"""Drive every required feature through Flask's test client.

    python smoke_test.py

The test client is an in-process fake browser: it calls the WSGI application
directly, so nothing binds a port and there is no browser to click. It keeps a
cookie jar, so `session` and flashes work exactly as they do in Chrome.

Each check prints ok/FAIL and the script exits non-zero if anything failed.
The database is a throwaway file in a temporary directory; your blog.db is
never touched.
"""

from __future__ import annotations

import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app          # noqa: E402
from db import get_db, init_db      # noqa: E402
from seed import load_sample_data   # noqa: E402

PASSED = 0
FAILED = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"ok    {label}")
    else:
        FAILED += 1
        print(f"FAIL  {label}" + (f"\n      {detail}" if detail else ""))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmpdir:
        app = create_app({
            "TESTING": True,
            "SECRET_KEY": "smoke-test",
            "DATABASE": str(Path(tmpdir) / "smoke.db"),
        })
        with app.app_context():
            init_db()
            load_sample_data(get_db())

        client = app.test_client()

        # ---- Feature 3: homepage lists posts newest-first with the author ---
        page = client.get("/")
        body = page.get_data(as_text=True)
        check("homepage returns 200", page.status_code == 200, str(page.status_code))
        check("homepage shows the joined author name", "ada" in body)
        newest = body.index("On computable numbers")
        oldest = body.index("Notes on the Analytical Engine")
        check("homepage is newest-first", newest < oldest,
              f"newest at {newest}, oldest at {oldest}")

        # ---- Feature 4: detail page shows body plus comments ---------------
        detail = client.get("/post/1").get_data(as_text=True)
        check("detail page shows the post body", "Jacquard loom" in detail)
        check("detail page shows a member comment", "This is the first program." in detail)
        check("detail page shows a guest comment as 'guest'",
              "Reading this a century later." in detail and "guest" in detail)
        check("missing post 404s", client.get("/post/999").status_code == 404)

        # ---- Feature 2: creating a post requires login ---------------------
        redirected = client.get("/create")
        check("anonymous /create redirects to login",
              redirected.status_code == 302 and "/auth/login" in redirected.headers["Location"],
              redirected.headers.get("Location", ""))

        # ---- Feature 1: register, then log in ------------------------------
        registered = client.post("/auth/register",
                                 data={"username": "grace", "password": "compiler-1952"},
                                 follow_redirects=True)
        check("register succeeds", "Please log in" in registered.get_data(as_text=True))

        duplicate = client.post("/auth/register",
                                data={"username": "grace", "password": "compiler-1952"})
        check("duplicate username is refused",
              "already registered" in duplicate.get_data(as_text=True))

        bad = client.post("/auth/login", data={"username": "grace", "password": "wrong"})
        check("wrong password is refused",
              "Incorrect username or password" in bad.get_data(as_text=True))

        good = client.post("/auth/login",
                           data={"username": "grace", "password": "compiler-1952"},
                           follow_redirects=True)
        check("login succeeds", "Welcome back, grace" in good.get_data(as_text=True))

        # ---- passwords are hashed, not stored -----------------------------
        with app.app_context():
            row = get_db().execute(
                "SELECT password_hash FROM users WHERE username = ?", ("grace",)
            ).fetchone()
        check("password is hashed", "compiler-1952" not in row["password_hash"],
              row["password_hash"])
        check("hash uses a real KDF", row["password_hash"].startswith(("scrypt:", "pbkdf2:")),
              row["password_hash"][:24])

        # ---- Feature 2: create a post as grace ----------------------------
        created = client.post("/create",
                              data={"title": "Bugs, literal", "body": "A moth in relay 70."},
                              follow_redirects=True)
        check("post created", "A moth in relay 70." in created.get_data(as_text=True))

        with app.app_context():
            new_id = get_db().execute(
                "SELECT id FROM posts WHERE title = ?", ("Bugs, literal",)
            ).fetchone()["id"]

        # ---- Feature 5: comment as a logged-in user -----------------------
        client.post(f"/post/{new_id}/comment", data={"body": "Taped into the logbook."},
                    follow_redirects=True)
        with app.app_context():
            comment = get_db().execute(
                "SELECT author_id, body FROM comments WHERE post_id = ?", (new_id,)
            ).fetchone()
        check("member comment records author_id", comment["author_id"] is not None)

        # ---- Feature 6: only the author may delete ------------------------
        forbidden = client.post("/post/1/delete")      # post 1 belongs to ada
        check("deleting someone else's post is 403", forbidden.status_code == 403,
              str(forbidden.status_code))

        client.get("/auth/logout")
        anon_comment = client.post(f"/post/{new_id}/comment",
                                   data={"body": "A guest passing through."},
                                   follow_redirects=True)
        check("guests may comment",
              "A guest passing through." in anon_comment.get_data(as_text=True))
        with app.app_context():
            guest = get_db().execute(
                "SELECT author_id FROM comments WHERE body = ?",
                ("A guest passing through.",),
            ).fetchone()
        check("guest comment has NULL author_id", guest["author_id"] is None)

        anon_delete = client.post(f"/post/{new_id}/delete")
        check("anonymous delete redirects to login",
              anon_delete.status_code == 302
              and "/auth/login" in anon_delete.headers["Location"])

        # ---- Feature 6: cascade ------------------------------------------
        client.post("/auth/login", data={"username": "grace", "password": "compiler-1952"})
        with app.app_context():
            before = get_db().execute(
                "SELECT COUNT(*) AS n FROM comments WHERE post_id = ?", (new_id,)
            ).fetchone()["n"]
        check("the post has comments before deletion", before == 2, str(before))

        client.post(f"/post/{new_id}/delete", follow_redirects=True)
        with app.app_context():
            db = get_db()
            gone = db.execute("SELECT COUNT(*) AS n FROM posts WHERE id = ?",
                              (new_id,)).fetchone()["n"]
            orphans = db.execute("SELECT COUNT(*) AS n FROM comments WHERE post_id = ?",
                                 (new_id,)).fetchone()["n"]
        check("post is deleted", gone == 0)
        check("comments cascaded away", orphans == 0, f"{orphans} orphan comments left")

        # ---- Injection payloads are stored, not executed -------------------
        payload = "Grace'); DROP TABLE posts; --"
        client.post("/create", data={"title": payload, "body": "still here"},
                    follow_redirects=True)
        with app.app_context():
            db = get_db()
            stored = db.execute("SELECT title FROM posts WHERE title = ?",
                                (payload,)).fetchone()
            try:
                total = db.execute("SELECT COUNT(*) AS n FROM posts").fetchone()["n"]
            except sqlite3.OperationalError as exc:
                total = -1
                print(f"      {exc}")
        check("injection payload stored verbatim", stored is not None)
        check("posts table survived", total == 4, str(total))

    print(f"\n{PASSED} passed, {FAILED} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
