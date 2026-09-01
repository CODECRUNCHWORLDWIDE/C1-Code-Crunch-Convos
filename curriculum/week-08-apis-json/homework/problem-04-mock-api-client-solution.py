"""problem-04-mock-api-client-solution.py — a REST API with no server behind it.

A tiny to-do client that keeps everything in memory. No requests, no sockets,
no network of any kind. The five methods are named after the five things a REST
collection does, and writing them is how the vocabulary stops being vocabulary.

    list   -> GET    /todos          the whole collection
    get    -> GET    /todos/{id}     one item
    create -> POST   /todos          make a new one, server picks the id
    update -> PATCH  /todos/{id}     change some fields, leave the rest
    delete -> DELETE /todos/{id}     remove it

Run it with::

    python problem-04-mock-api-client-solution.py
"""

from __future__ import annotations

import copy
from typing import Any


class TodoNotFound(KeyError):
    """Raised when an id does not exist. A KeyError, because that is what it is.

    Subclassing KeyError means ``except KeyError`` still catches it, so nothing
    that already handled a missing key has to change, while code that cares
    about to-do items specifically can catch this one instead.
    """


class MockTodoClient:
    """An in-memory stand-in for a REST to-do API.

    Ids start at 1 and never get reused, exactly as a real server would do it:
    a deleted id stays deleted, so a stale reference gets a clean 404 instead
    of somebody else's data.
    """

    def __init__(self) -> None:
        """Start with an empty collection and the next id at 1."""
        self._todos: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def list(self) -> list[dict[str, Any]]:
        """Return every to-do, oldest first.

        Returns:
            A list of copies, in id order. Editing them does not edit the
            collection, which is what a real client over a network gives you
            whether it means to or not.
        """
        return [copy.deepcopy(todo) for _, todo in sorted(self._todos.items())]

    def get(self, todo_id: int) -> dict[str, Any]:
        """Return one to-do.

        Args:
            todo_id: The id to look up.

        Returns:
            A copy of that to-do.

        Raises:
            TodoNotFound: no to-do has that id.
        """
        if todo_id not in self._todos:
            raise TodoNotFound(todo_id)
        return copy.deepcopy(self._todos[todo_id])

    def create(self, title: str, done: bool = False) -> dict[str, Any]:
        """Add a new to-do and return it, id included.

        The server chooses the id, not the caller. That is the whole difference
        between POST and PUT, and it is why calling this twice with the same
        title makes two to-dos rather than one.

        Args:
            title: What the to-do says.
            done: Whether it starts out finished.

        Returns:
            A copy of the newly created to-do.
        """
        todo = {"id": self._next_id, "title": title, "done": done}
        self._todos[self._next_id] = todo
        self._next_id += 1
        return copy.deepcopy(todo)

    def update(self, todo_id: int, **fields: Any) -> dict[str, Any]:
        """Change some fields of one to-do, leaving the rest alone.

        These are PATCH semantics: the fields you name are changed, and the
        fields you do not name keep their values. PUT would replace the whole
        item, and a missing field would become missing.

        Args:
            todo_id: The id to change.
            **fields: The fields to change. "id" is refused.

        Returns:
            A copy of the updated to-do.

        Raises:
            TodoNotFound: no to-do has that id.
            ValueError: an unknown field, or an attempt to change the id.
        """
        if todo_id not in self._todos:
            raise TodoNotFound(todo_id)
        allowed = {"title", "done"}
        unknown = set(fields) - allowed
        if unknown:
            raise ValueError(f"cannot set {', '.join(sorted(unknown))}")
        self._todos[todo_id].update(fields)
        return copy.deepcopy(self._todos[todo_id])

    def delete(self, todo_id: int) -> None:
        """Remove one to-do.

        Args:
            todo_id: The id to remove.

        Raises:
            TodoNotFound: no to-do has that id.
        """
        if todo_id not in self._todos:
            raise TodoNotFound(todo_id)
        del self._todos[todo_id]


def check() -> int:
    """Run every example and report.

    Returns:
        The number of checks that ran.
    """
    checks = 0
    client = MockTodoClient()

    assert client.list() == []
    print("ok  a new client is empty")
    checks += 1

    first = client.create("write the homework")
    assert first == {"id": 1, "title": "write the homework", "done": False}, first
    print(f"ok  create returned {first}")
    checks += 1

    second = client.create("read the lecture", done=True)
    assert second["id"] == 2, second
    print(f"ok  the second id is {second['id']}, not {first['id']}")
    checks += 1

    assert [todo["id"] for todo in client.list()] == [1, 2]
    print("ok  list returns both, oldest first")
    checks += 1

    assert client.get(1)["title"] == "write the homework"
    print("ok  get finds one by id")
    checks += 1

    patched = client.update(1, done=True)
    assert patched == {"id": 1, "title": "write the homework", "done": True}, patched
    print(f"ok  update changed done and left title alone: {patched}")
    checks += 1

    client.delete(2)
    assert [todo["id"] for todo in client.list()] == [1]
    print("ok  delete removed it")
    checks += 1

    third = client.create("start week 9")
    assert third["id"] == 3, third
    print(f"ok  ids are not reused: after deleting 2, the next one is {third['id']}")
    checks += 1

    for label, call in (
        ("get", lambda: client.get(99)),
        ("update", lambda: client.update(99, done=True)),
        ("delete", lambda: client.delete(99)),
    ):
        try:
            call()
        except TodoNotFound as exc:
            print(f"ok  {label}(99) raised TodoNotFound({exc.args[0]})")
            checks += 1
        else:  # pragma: no cover - only reached if a guard is removed
            raise AssertionError(f"{label}(99) should have raised")

    try:
        client.update(1, id=42)
    except ValueError as exc:
        print(f"ok  update refused to change the id: {exc}")
        checks += 1
    else:  # pragma: no cover - only reached if the guard is removed
        raise AssertionError("update(1, id=42) should have raised")

    stolen = client.list()[0]
    stolen["title"] = "vandalised"
    assert client.get(1)["title"] == "write the homework"
    print("ok  editing what list() returned did not edit the collection")
    checks += 1

    return checks


if __name__ == "__main__":
    total = check()
    print()
    print(f"{total} checks passed.")
