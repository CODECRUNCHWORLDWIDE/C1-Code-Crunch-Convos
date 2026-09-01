# Homework Problem 4 — Mock API Client

> **Topic:** the five REST verbs as five methods on a class, with no server anywhere
> **Lecture:** [01 — HTTP and REST](../lecture-notes/01-http-and-rest.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** you can recite "POST creates, PATCH edits part, DELETE removes" and still not own it. Building the server's half yourself — deciding who picks the id, what a missing id raises, what happens to fields you did not send — is how the vocabulary becomes judgement. It is also Week 7's classes doing real work, and a preview of the mocks Week 11 will hand you ready-made.

## The Brief

A REST API for to-do items is five sentences:

```text
list   -> GET    /todos          the whole collection
get    -> GET    /todos/{id}     one item
create -> POST   /todos          make a new one, server picks the id
update -> PATCH  /todos/{id}     change some fields, leave the rest
delete -> DELETE /todos/{id}     remove it
```

You are building `MockTodoClient` — a class with those five methods that
keeps everything in a plain dict in memory. **No `requests`, no sockets, no
network of any kind.** From the outside it behaves like a client talking to a
real server; on the inside it *is* the server, which means every rule a real
server enforces is now yours to enforce:

- A "todo" is a dict shaped `{"id": 1, "title": "...", "done": False}`.
- **The server picks the id.** Ids start at 1 and count up. The caller never
  supplies one — that is the entire difference between `POST` and `PUT`.
- **Deleted ids are never reused.** Someone holding a stale id gets a clean
  "not found", never somebody else's data.
- **`update` has PATCH semantics.** The fields you name change; the fields
  you do not name keep their values.
- **A missing id raises.** The brief asks for a `KeyError`; the shipped
  answer raises `TodoNotFound`, a `KeyError` subclass — the same thing, with
  a better name. Under the hood explains why that trick costs nothing.

Why fake a server instead of calling one? Because a fake is *fast*,
*offline*, and *yours*. Exercise 1 put the network behind a seam and injected
a recording; this problem is the same idea grown to a whole object. Week 11
will call this a **mock** and use it to test code that talks to servers,
without servers.

## Starter

Save this as `hw04_mock_client.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — `create` and `list` half-work, everything else
raises `NotImplementedError`:

```python
"""An in-memory stand-in for a REST to-do API."""

from __future__ import annotations

from typing import Any


class MockTodoClient:
    """A to-do collection that behaves like a REST API, minus the network."""

    def __init__(self) -> None:
        """Start with an empty collection and the next id at 1."""
        self._todos: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def list(self) -> list[dict[str, Any]]:
        """Return every to-do, oldest first."""
        # TODO: return copies, not the stored dicts themselves.
        return list(self._todos.values())

    def get(self, todo_id: int) -> dict[str, Any]:
        """Return one to-do, or raise KeyError if the id is unknown."""
        raise NotImplementedError

    def create(self, title: str, done: bool = False) -> dict[str, Any]:
        """Add a new to-do and return it, id included. The server picks the id."""
        todo = {"id": self._next_id, "title": title, "done": done}
        self._todos[self._next_id] = todo
        # TODO: advance the id counter. Should a delete ever rewind it?
        return todo

    def update(self, todo_id: int, **fields: Any) -> dict[str, Any]:
        """Change some fields of one to-do, leaving the rest alone (PATCH)."""
        # TODO: unknown id raises. Unknown field names raise ValueError.
        #       Changing "id" is refused.
        raise NotImplementedError

    def delete(self, todo_id: int) -> None:
        """Remove one to-do, or raise KeyError if the id is unknown."""
        raise NotImplementedError


if __name__ == "__main__":
    client = MockTodoClient()
    first = client.create("write the homework")
    assert first == {"id": 1, "title": "write the homework", "done": False}
    assert client.create("read the lecture")["id"] == 2
    assert [t["id"] for t in client.list()] == [1, 2]
    # TODO: eight or more asserts in total -- exercise every method,
    #       including get/update/delete on an id that does not exist.
    print("all checks passed")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-04-mock-api-client.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The five methods exist with these signatures, type-hinted:
   `list() -> list[dict]`, `get(todo_id) -> dict`,
   `create(title, done=False) -> dict`, `update(todo_id, **fields) -> dict`,
   `delete(todo_id) -> None`.
2. `create` returns the new to-do with its server-assigned id; ids start at 1
   and increment; a deleted id is never handed out again.
3. `get`, `update` and `delete` on an unknown id raise a `KeyError` (or a
   subclass of one).
4. `update` changes only the fields it is given and returns the whole updated
   to-do. Trying to change `id`, or a field that does not exist, raises
   `ValueError`.
5. `list` returns to-dos oldest first, and mutating anything it returned does
   not change the stored collection.
6. Eight or more `assert` statements under `if __name__ == "__main__":`
   exercise every method, including every error case.

## Constraints

- **No `requests`, no `socket`, no network.** The point is the semantics, and
  semantics need no wire. Anything imported beyond the standard library is a
  sign the problem drifted.

- **Return copies, never the stored dicts.** A real client cannot hand you a
  reference into the server's memory — the network copies everything by
  making it bytes and back. Your mock must be as safe: if
  `client.list()[0]["title"] = "vandalised"` changes what `get` returns
  later, the mock has a door a real API physically cannot have, and code
  tested against it learns habits that break in production.

- **The id counter only ever goes up.** Reusing id 2 after its delete means a
  stale reference — a bookmark, a queued job, a log line — silently points at
  the *new* record. "Not found" is an error you can see; the wrong record is
  one you cannot.

- **Refuse field names you do not know.** `update(1, ttile="x")` with a
  typo'd field must raise, not quietly add a `ttile` key beside `title`.
  Validate at the edge, so the inside can trust its own shape.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-04-mock-api-client-solution.py
ok  a new client is empty
ok  create returned {'id': 1, 'title': 'write the homework', 'done': False}
ok  the second id is 2, not 1
ok  list returns both, oldest first
ok  get finds one by id
ok  update changed done and left title alone: {'id': 1, 'title': 'write the homework', 'done': True}
ok  delete removed it
ok  ids are not reused: after deleting 2, the next one is 3
ok  get(99) raised TodoNotFound(99)
ok  update(99) raised TodoNotFound(99)
ok  delete(99) raised TodoNotFound(99)
ok  update refused to change the id: cannot set id
ok  editing what list() returned did not edit the collection

13 checks passed.
```

Your own `hw04_mock_client.py` prints whatever your harness prints. What must
agree is the behaviour each line describes.

## Steps

1. Copy the starter into `hw04_mock_client.py` and run it. The three starter
   asserts pass already — `create` and `list` half-work.
2. Finish `create`: advance `self._next_id`. Decide now, on purpose, that
   nothing ever rewinds it.
3. Write `get`: check membership, raise on a miss, return a **copy** on a
   hit. Test both paths before moving on.
4. Write `delete` the same shape: check, raise or remove.
5. Write `update` last — it has the most rules. Check the id exists, check
   every field name against the set of allowed ones, apply with
   `dict.update`, return a copy.
6. Now go back and make `list` and `create` return copies too, and add the
   vandalism test: take a dict out of `list()`, scribble on it, prove the
   collection did not change.
7. Grow the harness to eight-plus asserts. The three error cases (`get`,
   `update`, `delete` on id 99) and the id-reuse rule are the ones people
   skip and the ones that catch real bugs.

## The Solution

```python
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
```

**The whole server is a dict and a counter.** `self._todos` maps id to
record; `self._next_id` remembers the next id to hand out. Both names start
with an underscore — Python's convention for "internal, reach in at your own
risk" — because the five methods *are* the API, and everything a caller may
do goes through them. That boundary is the design.

**Every read path ends in `deepcopy`, and the last check proves why.** The
harness takes a dict out of `list()`, scribbles `"vandalised"` on it, and
shows the collection unhurt. Hand out the stored dict instead and that
scribble would change what every later `get` returns — mutation at a
distance, the class of bug where the crash is nowhere near the cause. A real
network client gets this protection free, because serialising to bytes and
back *is* a deep copy; the mock has to buy it explicitly to be honest.
`deepcopy` rather than `dict(todo)` is deliberate future-proofing: the day a
todo grows a nested list of tags, a shallow copy would share it.

**`update` enforces PATCH, not PUT.** `self._todos[todo_id].update(fields)`
merges the named fields into the record — everything unnamed survives, which
is what PATCH means. The two guards ahead of it do the server's other job:
an unknown id is `TodoNotFound` (a 404 in exception form), and an unknown
field name — including `id` — is `ValueError` (a 400). The allow-list
spelling, `set(fields) - allowed`, names every offender at once instead of
failing on the first.

**`create` embodies "the server picks the id".** It ignores any opinion the
caller might have, stamps the next counter value, and advances the counter —
one direction, forever. Delete 2, create again, get 3: the harness pins that
down because it is the rule people accidentally break first, usually by
deriving ids from `len(self._todos)`, which reuses an id the moment anything
is deleted.

**`sorted(self._todos.items())` is oldest-first by construction.** Ids are
assigned in creation order, so sorting by id *is* sorting by age. Modern
dicts would iterate in insertion order anyway, but saying `sorted` makes the
promise visible instead of inherited.

**The three error cases share one test, written as data.** Three
`(label, lambda)` pairs and one loop — the same trick `RULES` pulled in
problem 1. When several cases differ only in data, make them data.

## Download and run

Download
[problem-04-mock-api-client-solution.py](./problem-04-mock-api-client-solution.py)
and run it:

```bash
python problem-04-mock-api-client-solution.py
```

It needs nothing installed and never touches the network — that is the whole
premise. The `-solution` in the filename keeps it from colliding with your
own `hw04_mock_client.py`.

## Common bugs to catch

- **Handing out the stored dict.** No error, no warning — until something
  edits a "result" and every later read sees the edit. The vandalism assert
  is the tripwire:

  ```text
  AssertionError
  ```

  on `client.get(1)["title"] == "write the homework"`. If that line just
  failed, some read path returns the real dict. Check `list`, `get`,
  `create` *and* `update` — people fix the first three and forget that
  `update` returns a dict too.

- **Ids from `len(self._todos) + 1`.** Works until the first delete: with
  items 1 and 2, delete 2, create — `len` is 1, so the "new" id is 2,
  resurrecting the dead id with different contents. The check
  `ids are not reused` exists for exactly this. A counter that only
  increments cannot make the mistake.

- **`update` with PUT semantics by accident.**

  ```python
  self._todos[todo_id] = {"id": todo_id, **fields}
  ```

  replaces the whole record, so `update(1, done=True)` silently *deletes the
  title*. The harness catches it: `patched` is missing a key. PATCH merges;
  PUT replaces; the brief asked for PATCH.

- **`except KeyError` around `update(1, id=42)` in your tests.** That call
  raises `ValueError`, not `KeyError` — if your test passes while catching
  the wrong exception, it would also pass on a client with no guard at all.
  Assert on the *specific* exception each rule promises.

- **`client.list` without parentheses.**

  ```text
  TypeError: 'method' object is not subscriptable
  ```

  from `client.list[0]`. `client.list` is the method object itself;
  `client.list()` calls it. (Naming a method `list` also shadows the
  built-in *inside the class body* — harmless here, worth noticing. A real
  codebase might prefer `list_all` and dodge both.)

- **Forgetting `return` in `update`.** The merge happens, the collection is
  right, and the caller gets `None` — so the *next* line of their code
  crashes with `TypeError: 'NoneType' object is not subscriptable`. Methods
  that change things should return the changed thing; every REST API you
  will meet sends the updated record back in the response body for the same
  reason.

## Under the hood

<details>
<summary>Under the hood — why TodoNotFound subclasses KeyError, and how exception hierarchies work for you</summary>

`except` matches by **is-a**, not by exact type. A
`try / except KeyError` block catches `KeyError` and every subclass of it —
so when `TodoNotFound(KeyError)` came along, every existing handler kept
working, and new code gained the option of catching the precise, readable
name instead. Both of these run the handler:

```python
try:
    client.get(99)
except KeyError:        # catches TodoNotFound too -- it is-a KeyError
    ...

try:
    client.get(99)
except TodoNotFound:    # catches only the specific one
    ...
```

This is the standard library's own pattern, and you have been using it all
course without ceremony: `FileNotFoundError` is a subclass of `OSError`,
`json.JSONDecodeError` of `ValueError`, and over in `requests`, every
exception from `HTTPError` to `ReadTimeout` descends from
`RequestException` — which is the only reason Exercise 5 could funnel five
failure modes through one `except`.

The design rule hiding in it: **subclass the exception your error is-a,
then raise the specific one.** A missing to-do *is* a missing key, so
`KeyError` is the honest parent. If it subclassed `Exception` directly,
handlers written before it existed would miss it; if the code raised bare
`KeyError`, handlers could not tell a missing to-do from a typo'd dict
lookup three lines away.

One inherited quirk worth knowing before it confuses you:

```text
>>> str(TodoNotFound(99))
'99'
>>> str(TodoNotFound("no todo 99"))
"'no todo 99'"
```

`KeyError.__str__` prints the `repr` of its argument — those extra quotes —
because the missing *key* might itself be a string containing anything.
That is why the harness prints `exc.args[0]` instead of `exc`, and why
custom messages on KeyError subclasses look odd until you override
`__str__` (which real libraries, like `requests`' own `HTTPError`
hierarchy, sometimes do).

</details>

<details>
<summary>Under the hood — from this mock to the real thing: the same five calls over HTTP</summary>

The interface you built maps one-to-one onto a real client. Here is the same
class where every method body became a request — against
[JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free fake API
for exactly this kind of practice:

```python
import requests

class TodoClient:
    """The same five verbs, over a real wire."""

    BASE = "https://jsonplaceholder.typicode.com/todos"

    def __init__(self, *, timeout: float = 5.0) -> None:
        self._session = requests.Session()
        self._timeout = timeout

    def list(self) -> list[dict]:
        response = self._session.get(self.BASE, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def get(self, todo_id: int) -> dict:
        response = self._session.get(f"{self.BASE}/{todo_id}", timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def create(self, title: str, done: bool = False) -> dict:
        response = self._session.post(
            self.BASE, json={"title": title, "completed": done}, timeout=self._timeout
        )
        response.raise_for_status()
        return response.json()

    def update(self, todo_id: int, **fields) -> dict:
        response = self._session.patch(
            f"{self.BASE}/{todo_id}", json=fields, timeout=self._timeout
        )
        response.raise_for_status()
        return response.json()

    def delete(self, todo_id: int) -> None:
        response = self._session.delete(f"{self.BASE}/{todo_id}", timeout=self._timeout)
        response.raise_for_status()
```

Read the two side by side and the correspondences line up: your
`TodoNotFound` is its `HTTPError` for a 404; your `ValueError` on a bad
field is its 400; your deepcopy boundary is its network; your id counter is
its database sequence. Even the field-name mismatch is a real lesson — this
API says `completed` where yours says `done`, and real client classes spend
a surprising share of their lines translating between their caller's
vocabulary and the server's.

Two things the mock quietly skipped that the real one must face. **Paging:**
`list()` here returns 200 items because that is all there are; GitHub's
version of the same call is [Exercise 4](../exercises/exercise-04-pagination.md)'s
whole subject. **Partial failure:** the mock's `update` either fully works
or raises; over a network, the request can succeed *after* your timeout
fired, and you cannot know which — which is why idempotency (problem 1's
Under the hood) matters so much for retries.

Swap-ability is the payoff: any function written against "something with
these five methods" runs against either class. Type that promise as a
`Protocol` (Week 7) and the checker enforces it. Week 11 names the testing
half of this pattern — hand the mock to code under test, hand the real one
to production — and you have now built both halves yourself.

</details>

## Acceptance checklist

- [ ] All five methods exist, type-hinted, and the script runs clean.
- [ ] `create` assigns ids 1, 2, 3, ... and returns the new to-do.
- [ ] After deleting id 2, the next create returns id 3, not 2.
- [ ] `get`/`update`/`delete` on id 99 raise a `KeyError` (or subclass), and
      a test proves each one.
- [ ] `update(1, done=True)` changes `done` and leaves `title` alone.
- [ ] `update(1, id=42)` and `update(1, nonsense="x")` raise `ValueError`.
- [ ] Scribbling on anything a method returned does not change the
      collection.
- [ ] Eight or more asserts, all passing.
- [ ] Committed with a message like `Add Week 8 homework 4: mock API client`.

## Stretch

- Add paging to `list`: `list(page=1, per_page=10)` returning a dict shaped
  `{"items": [...], "next_page": 2 | None}` — then compare your design with
  the four real paging schemes in Exercise 4's Under the hood.

- Write `TodoClient` from Under the hood (or your own version of it) against
  JSONPlaceholder, and run the same eight asserts against both classes.
  Where they disagree — JSONPlaceholder does not really persist writes — you
  have discovered why test fakes exist.

- Define the shared interface as a `typing.Protocol` with the five method
  signatures, annotate a function `complete_all(client: TodoApi) -> int`
  that marks every to-do done, and check it runs against both
  implementations unchanged.

Once your mock enforces all five verbs, move on to
[Homework Problem 5 — Link Header Parser](./problem-05-link-header-parser.md).
