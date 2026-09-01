"""exercise-02-multiple-routes-solution.py — a tiny room directory, proven headless.

The four view functions are the exercise, unchanged in meaning from the
starter. Your own exercise-02-multiple-routes.py ends in
``app.run(debug=True)`` and you read the routes with curl; that is the right
way to work interactively. This shipped answer has to prove all four routes
work and then exit, so instead of binding a port it drives the app with
``app.test_client()`` — Flask's in-process fake browser — and prints each
status code and body. Same routes, same answers, no server.

Run it with::

    python exercise-02-multiple-routes-solution.py
"""

from flask import Flask, abort, request, url_for

app: Flask = Flask(__name__)

ROOMS: dict[int, dict[str, str]] = {
    1: {"name": "Loops and Lists", "host": "ada", "topic": "python"},
    2: {"name": "HTTP by Hand", "host": "grace", "topic": "web"},
    3: {"name": "Reading Tracebacks", "host": "ada", "topic": "python"},
}


@app.route("/")
def index() -> str:
    """List every room, one per line, as `id: name (host: who)`."""
    lines: list[str] = [
        f"{room_id}: {ROOMS[room_id]['name']} (host: {ROOMS[room_id]['host']})"
        for room_id in sorted(ROOMS)
    ]
    return "\n".join(lines)


@app.route("/room/<int:room_id>")
def show_room(room_id: int) -> str:
    """Show one room, or abort with 404 if the id is unknown."""
    if room_id not in ROOMS:
        abort(404)
    room: dict[str, str] = ROOMS[room_id]
    return "\n".join(
        [
            f"Room {room_id}: {room['name']}",
            f"Host: {room['host']}",
            f"Topic: {room['topic']}",
        ]
    )


@app.route("/host/<username>")
def show_host(username: str) -> str:
    """List the rooms this person hosts. Match the name case-insensitively."""
    who: str = username.strip().lower()
    hosted: list[int] = [
        room_id for room_id in sorted(ROOMS) if ROOMS[room_id]["host"] == who
    ]
    if not hosted:
        return f"{who} hosts no rooms."
    lines: list[str] = [f"{who} hosts {len(hosted)} room(s):"]
    lines += [f"{room_id}: {ROOMS[room_id]['name']}" for room_id in hosted]
    return "\n".join(lines)


@app.route("/search")
def search() -> str:
    """Match rooms by topic, read from the `topic` query parameter."""
    topic: str = request.args.get("topic", default="", type=str).strip().lower()
    if not topic:
        return f"Try {url_for('search', topic='python')}"
    matches: list[int] = [
        room_id for room_id in sorted(ROOMS) if ROOMS[room_id]["topic"] == topic
    ]
    lines: list[str] = [f"{len(matches)} room(s) match topic '{topic}':"]
    lines += [f"{room_id}: {ROOMS[room_id]['name']}" for room_id in matches]
    return "\n".join(lines)


#: Every URL the exercise page discusses, happy paths and failure paths alike.
REQUESTS: tuple[str, ...] = (
    "/",
    "/room/2",
    "/room/99",
    "/room/two",
    "/host/ADA",
    "/host/nobody",
    "/search?topic=python",
    "/search",
)


def main() -> None:
    """Hit every URL and print the status plus the body for the 200s."""
    client = app.test_client()
    for path in REQUESTS:
        response = client.get(path)
        print(f"GET {path} -> {response.status_code}")
        if response.status_code == 200:
            print(response.get_data(as_text=True))
        print()


if __name__ == "__main__":
    main()
