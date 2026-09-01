"""Required test 7 — a protected route rejects anonymous callers.

The Week 9 blog had no authentication at all, so the smallest credible gate was
added in ``blog/auth.py``: one password in config, one flag in the session, one
``login_required`` decorator on the delete route. These tests pin that gate.
"""

from __future__ import annotations

from flask.testing import FlaskClient

# ------------------------------------------ 7. Protected route is protected -


def test_delete_redirects_anonymous_callers_to_login(seeded_client: FlaskClient) -> None:
    response = seeded_client.post("/posts/1/delete")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_anonymous_delete_does_not_delete(seeded_client: FlaskClient) -> None:
    """The redirect is only half the story — prove the post survived."""
    seeded_client.post("/posts/1/delete")
    assert seeded_client.get("/posts/1").status_code == 200


def test_login_redirect_remembers_where_you_were_going(seeded_client: FlaskClient) -> None:
    response = seeded_client.delete("/posts/1")
    assert response.headers["Location"] == "/login?next=/posts/1"


# ---------------------------------------------------------- The gate itself -


def test_login_page_renders(client: FlaskClient) -> None:
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Admin password" in response.data


def test_correct_password_logs_you_in(client: FlaskClient, admin_password: str) -> None:
    response = client.post("/login", data={"password": admin_password})

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    with client.session_transaction() as session:
        assert session["is_admin"] is True


def test_wrong_password_returns_401(client: FlaskClient) -> None:
    response = client.post("/login", data={"password": "not-the-password"})

    assert response.status_code == 401
    assert b"Wrong password." in response.data
    with client.session_transaction() as session:
        assert "is_admin" not in session


def test_missing_password_returns_401(client: FlaskClient) -> None:
    assert client.post("/login", data={}).status_code == 401


def test_logout_clears_the_session(admin_client: FlaskClient) -> None:
    response = admin_client.post("/logout")

    assert response.status_code == 302
    with admin_client.session_transaction() as session:
        assert "is_admin" not in session

    # And the gate is closed again.
    assert admin_client.post("/posts/1/delete").status_code == 302
    assert admin_client.get("/posts/1").status_code == 200


def test_logout_is_idempotent(client: FlaskClient) -> None:
    """``session.pop(..., None)`` must not raise for a caller who was never in."""
    assert client.post("/logout").status_code == 302
