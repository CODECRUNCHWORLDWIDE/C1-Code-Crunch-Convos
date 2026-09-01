"""Signup, login, logout, and the login_required decorator.

Required feature 1. The rule that matters: this module stores a *hash* and
never sees the plaintext password again after `generate_password_hash` returns.
"""

from __future__ import annotations

import functools
import sqlite3
from collections.abc import Callable
from typing import Any

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user() -> None:
    """Put the current user (or None) on `g` before every request.

    The session cookie holds only an integer id. Everything else about the
    user is looked up fresh, so a rename or a deletion takes effect on the
    next request instead of living on in a stale cookie.
    """
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return
    g.user = get_db().execute(
        "SELECT id, username, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if g.user is None:
        # The account was deleted while the cookie survived. Clean up.
        session.clear()


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    """Send anonymous visitors to the login page instead of running the view."""

    @functools.wraps(view)
    def wrapped(**kwargs: Any) -> Any:
        if g.user is None:
            flash("Please log in first.")
            return redirect(url_for("auth.login", next=request.path))
        return view(**kwargs)

    return wrapped


@bp.route("/register", methods=("GET", "POST"))
def register() -> str | Response:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        error: str | None = None
        if not username:
            error = "Username is required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                # UNIQUE constraint failed: users.username. Letting the
                # database decide is better than SELECT-then-INSERT, which has
                # a race between the two statements.
                error = f"User {username} is already registered."
            else:
                flash("Account created. Please log in.")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> str | Response:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_db().execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        # One message for both failures on purpose. "No such user" tells an
        # attacker which usernames exist; "wrong password" does not need to.
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Incorrect username or password.")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['username']}.")
            target = request.form.get("next") or request.args.get("next")
            # Only ever redirect to a path on this site. An open redirect is a
            # phishing tool: /auth/login?next=https://evil.example is a link
            # that starts on your domain and ends on theirs.
            if target and target.startswith("/") and not target.startswith("//"):
                return redirect(target)
            return redirect(url_for("index"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout() -> Response:
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))
