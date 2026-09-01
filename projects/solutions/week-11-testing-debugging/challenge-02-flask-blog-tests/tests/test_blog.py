"""The six required tests from challenge 2, plus the three stretch tests.

Section headings match the numbering in
``curriculum/week-11-testing-debugging/challenges/challenge-02-flask-api-tests.md``
so you can read the spec and the suite side by side.
"""

from __future__ import annotations

import pytest
from flask import Flask
from flask.testing import FlaskClient

from blog import db

# ------------------------------------------------- 1. GET / returns 200 ---


def test_index_returns_200(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"My Blog" in response.data


def test_index_lists_seeded_posts(seeded_client: FlaskClient) -> None:
    response = seeded_client.get("/")
    assert response.status_code == 200
    for n in (1, 2, 3):
        assert f"Seed post {n}".encode() in response.data


def test_index_says_so_when_empty(client: FlaskClient) -> None:
    assert b"No posts yet" in client.get("/").data


# ------------------------------ 2. GET /posts/<id> for an existing post ---


def test_show_post_returns_200_for_existing_post(seeded_client: FlaskClient) -> None:
    response = seeded_client.get("/posts/1")
    assert response.status_code == 200
    assert b"Seed post 1" in response.data
    assert b"Body of seed post 1." in response.data


# --------------------------------- 3. GET /posts/9999 returns 404 ---------


def test_show_missing_post_returns_404(seeded_client: FlaskClient) -> None:
    response = seeded_client.get("/posts/9999")
    assert response.status_code == 404
    assert b"Not found" in response.data


def test_unknown_url_returns_404(client: FlaskClient) -> None:
    assert client.get("/no-such-page").status_code == 404


# --------------------------------------- 4. POST /posts creates a post ----


def test_create_post_redirects_and_shows_up_on_the_index(client: FlaskClient) -> None:
    response = client.post("/posts", data={"title": "Crunch time", "body": "Shipped it."})

    assert response.status_code == 302
    assert response.headers["Location"] == "/posts/1"

    index = client.get("/")
    assert b"Crunch time" in index.data


def test_create_post_follow_redirects_lands_on_the_post(client: FlaskClient) -> None:
    response = client.post(
        "/posts",
        data={"title": "Crunch time", "body": "Shipped it."},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Shipped it." in response.data
    assert b"Post published." in response.data


def test_create_post_strips_surrounding_whitespace(client: FlaskClient, app: Flask) -> None:
    client.post("/posts", data={"title": "  Padded  ", "body": "  Body  "})
    with app.app_context():
        post = db.get_post(1)
    assert post is not None
    assert post["title"] == "Padded"
    assert post["body"] == "Body"


# ----------------------------- 5. POST /posts with missing fields -> 400 --


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({}, "nothing at all"),
        ({"title": "Only a title"}, "body missing"),
        ({"body": "Only a body"}, "title missing"),
        ({"title": "  ", "body": "  "}, "whitespace is not content"),
    ],
    ids=["empty-form", "no-body", "no-title", "whitespace-only"],
)
def test_create_post_rejects_incomplete_forms(
    client: FlaskClient, payload: dict[str, str], reason: str
) -> None:
    response = client.post("/posts", data=payload)
    assert response.status_code == 400, reason
    assert b"Title and body are both required." in response.data


def test_rejected_post_is_not_stored(client: FlaskClient) -> None:
    client.post("/posts", data={"title": "Only a title"})
    assert b"No posts yet" in client.get("/").data


def test_create_post_rejects_an_over_long_title(client: FlaskClient) -> None:
    response = client.post("/posts", data={"title": "x" * 121, "body": "fine"})
    assert response.status_code == 400
    assert b"120 characters or fewer" in response.data


def test_create_post_rejects_an_over_long_body(client: FlaskClient) -> None:
    response = client.post("/posts", data={"title": "fine", "body": "x" * 10_001})
    assert response.status_code == 400
    assert b"10000 characters or fewer" in response.data


def test_rejected_form_keeps_what_you_typed(client: FlaskClient) -> None:
    """A 400 that throws the draft away is a bug, not a validation."""
    response = client.post("/posts", data={"title": "Kept me", "body": ""})
    assert b'value="Kept me"' in response.data


# ---------------------------------------------------- The new-post form ---


def test_new_post_form_renders(client: FlaskClient) -> None:
    response = client.get("/posts/new")
    assert response.status_code == 200
    assert b"New post" in response.data


def test_new_is_not_parsed_as_a_post_id(client: FlaskClient) -> None:
    """The ``int`` converter is what keeps ``/posts/new`` off the detail route."""
    assert client.get("/posts/new").status_code == 200


# ------------------------------------------ 6. Deleting a post removes it -


def test_delete_via_form_route_removes_the_post(admin_client: FlaskClient) -> None:
    response = admin_client.post("/posts/2/delete")

    assert response.status_code == 302
    assert admin_client.get("/posts/2").status_code == 404
    assert admin_client.get("/posts/1").status_code == 200


def test_delete_via_http_delete_removes_the_post(admin_client: FlaskClient) -> None:
    response = admin_client.delete("/posts/3")

    assert response.status_code == 302
    assert admin_client.get("/posts/3").status_code == 404


def test_delete_missing_post_returns_404(admin_client: FlaskClient) -> None:
    assert admin_client.post("/posts/9999/delete").status_code == 404


# ------------------------------------------------------- Stretch tests ----


def test_404_logs_a_warning(client: FlaskClient, caplog: pytest.LogCaptureFixture) -> None:
    """Stretch: assert on a log record rather than on the response body."""
    with caplog.at_level("WARNING", logger="blog.views"):
        client.get("/posts/9999")

    assert any("404 Not Found: /posts/9999" in record.message for record in caplog.records)


@pytest.mark.parametrize("path", ["/", "/about", "/posts/1"])
def test_public_pages_return_200(seeded_client: FlaskClient, path: str) -> None:
    """Stretch: one test, three paths, three result rows."""
    assert seeded_client.get(path).status_code == 200


def test_seeded_app_fixture_pre_populates_three_posts(seeded_app: Flask) -> None:
    """Stretch: the ``seeded_app`` fixture itself is worth a test."""
    with seeded_app.app_context():
        posts = db.list_posts()

    assert len(posts) == 3
    assert [row["id"] for row in posts] == [3, 2, 1], "index shows newest first"
