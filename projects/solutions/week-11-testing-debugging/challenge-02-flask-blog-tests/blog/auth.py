"""A single-password admin gate.

The Week 9 blog had no authentication. Required test 7 asks for one protected
route, so this adds the smallest credible gate: a password in config, a flag in
the session, and a ``login_required`` decorator. Only the delete route is
protected, so the other five routes keep their Week 9 behaviour.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar, cast

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.wrappers import Response

bp = Blueprint("auth", __name__)

ViewT = TypeVar("ViewT", bound=Callable[..., Any])


def login_required(view: ViewT) -> ViewT:
    """Redirect anonymous callers to the login page instead of running *view*."""

    @functools.wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if not session.get("is_admin"):
            return redirect(url_for("auth.login_form", next=request.path))
        return view(*args, **kwargs)

    return cast(ViewT, wrapped)


@bp.get("/login")
def login_form() -> str:
    """Render the login form."""
    return render_template("login.html")


@bp.post("/login")
def login() -> Response | tuple[str, int]:
    """Check the password and start an admin session."""
    password = request.form.get("password", "")
    if password != current_app.config["ADMIN_PASSWORD"]:
        flash("Wrong password.", "error")
        return render_template("login.html"), 401
    session["is_admin"] = True
    flash("Logged in.", "success")
    return redirect(url_for("blog.index"))


@bp.post("/logout")
def logout() -> Response:
    """End the admin session."""
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("blog.index"))
