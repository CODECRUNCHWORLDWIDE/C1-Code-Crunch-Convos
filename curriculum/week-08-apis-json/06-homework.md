# Week 8 — Homework

Six problems. Submit one `.py` (or `.md` where the problem asks for prose) per problem in a folder called `homework/` inside your fork. Type hints on every function. No external network in problems 4 and 5 — those test pure logic.

| # | Problem | Files |
|---|---|---|
| 1 | HTTP method matcher | `hw01_method_matcher.py` |
| 2 | JSON deeply nested traversal | `hw02_json_walker.py` |
| 3 | Rate-limit decorator | `hw03_rate_limit.py` |
| 4 | Mock API client class (no network) | `hw04_mock_client.py` |
| 5 | Parse `Link` headers | `hw05_link_header.py` |
| 6 | Tiny URL-shortener client | `hw06_url_shortener.py` |

---

## Problem 1 — HTTP method matcher

Write a function `recommend_method(intent: str) -> str` that returns the recommended HTTP method for an intent string.

**Mapping:**

| Intent (lowercase) contains | Method |
|---|---|
| `"create"` or `"add"` or `"submit"` | `POST` |
| `"replace"` or `"overwrite"` | `PUT` |
| `"update"` or `"modify"` or `"edit"` | `PATCH` |
| `"remove"` or `"delete"` | `DELETE` |
| `"fetch"` or `"read"` or `"get"` or `"list"` | `GET` |
| anything else | `GET` (default) |

Order matters: if both `"add"` and `"update"` appear, the *first* match in the table above wins.

**Examples:**

```python
recommend_method("add a new user")        == "POST"
recommend_method("delete order 42")       == "DELETE"
recommend_method("read the catalog")      == "GET"
recommend_method("modify the title")      == "PATCH"
recommend_method("")                      == "GET"
```

Write 6+ tests using `assert` statements inside `if __name__ == "__main__":`. Bonus: explain in a docstring why "submit" is `POST` and not `PUT`.

---

## Problem 2 — JSON deeply nested traversal

Given a JSON document loaded as a Python `dict`/`list` structure, write a generator that yields every primitive value (str, int, float, bool, None) along with its **dotted path**.

**Signature:**

```python
def walk(node, path: str = "") -> Iterator[tuple[str, Any]]: ...
```

**Path rules:**

- Top-level dict keys: `name`, `address.city`.
- List indices: `friends[0]`, `friends[1].name`.

**Example:**

```python
data = {
    "name": "Ada",
    "age": 207,
    "address": {"city": "London", "zip": "E1 6AN"},
    "friends": [{"name": "Bob"}, {"name": "Carol"}],
}

list(walk(data)) == [
    ("name", "Ada"),
    ("age", 207),
    ("address.city", "London"),
    ("address.zip", "E1 6AN"),
    ("friends[0].name", "Bob"),
    ("friends[1].name", "Carol"),
]
```

Include 4+ test cases (one with an empty dict, one with deeply nested lists). Useful for debugging real API responses.

---

## Problem 3 — Rate-limit decorator

Write a decorator `@rate_limited(calls_per_second: float)` that enforces a minimum gap between successive calls to the decorated function (by sleeping if needed).

**Behavior:**

- `@rate_limited(2.0)` allows at most 2 calls per second.
- The first call goes through immediately. Each subsequent call within the window sleeps until the window opens.
- The decorator preserves the wrapped function's name and docstring (`functools.wraps`).
- The decorator is thread-safe enough for a single-threaded program — you do not need to handle multiple threads, but document the limitation.

**Sketch:**

```python
@rate_limited(2.0)
def hello(name: str) -> None:
    print(f"hello {name}")

t0 = time.perf_counter()
for n in ["a", "b", "c", "d"]:
    hello(n)
elapsed = time.perf_counter() - t0
assert elapsed >= 1.5  # 4 calls at 2/sec = ~1.5s minimum
```

Hint: store the last-call timestamp on the wrapper function itself (`wrapper._last_call = ...`).

---

## Problem 4 — Mock API client (no real network)

Build a tiny `MockTodoClient` class that simulates a REST API in memory. **No `requests`; no `socket`.** This is pure OOP practice (Week 7) on top of the API mental model you built this week.

**Required interface:**

```python
class MockTodoClient:
    def list(self) -> list[dict]: ...
    def get(self, todo_id: int) -> dict: ...                # KeyError if missing
    def create(self, title: str, done: bool = False) -> dict: ...  # returns new todo with auto id
    def update(self, todo_id: int, **fields) -> dict: ...   # partial update (PATCH semantics)
    def delete(self, todo_id: int) -> None: ...
```

A "todo" is a dict like `{"id": 1, "title": "...", "done": False}`. Ids increment from 1.

**Tests:** in `if __name__ == "__main__":`, write 8+ `assert` statements that exercise every method, including the error cases (`get` on missing id, `delete` on missing id).

This problem locks in CRUD semantics — `list` (GET collection), `get` (GET single), `create` (POST), `update` (PATCH), `delete` (DELETE). Once you have written the mock, you have internalized the REST verbs.

---

## Problem 5 — Parse `Link` headers

GitHub (and many other paginated APIs) return a `Link` header that explicitly lists the URLs of the next/prev/first/last pages:

```
Link: <https://api.github.com/repositories?page=2>; rel="next",
      <https://api.github.com/repositories?page=15>; rel="last"
```

Write `parse_link_header(header: str) -> dict[str, str]` that turns this into:

```python
{
  "next": "https://api.github.com/repositories?page=2",
  "last": "https://api.github.com/repositories?page=15",
}
```

**Edge cases to handle:**

- An empty or `None` input returns `{}`.
- Whitespace and newlines between entries.
- A `rel` value may contain spaces or be in single or double quotes.
- Unknown rels should still be included.

You may **not** use the `requests` library's built-in `r.links` for this — write the parser yourself. (You may, however, use it to *verify* your output against a real GitHub response.) Hint: split on `,` first, then on `;`. Beware: URLs themselves never contain `,` or `;` outside their query strings in this header, but inside the `< >` brackets they can — split carefully.

Write 5+ test cases.

---

## Problem 6 — Tiny URL-shortener client

Build `class URLShortenerClient:` that wraps the [is.gd](https://is.gd/) free shortening API (no key required).

**API:**

- `GET https://is.gd/create.php?format=json&url=<long-url>` returns `{"shorturl": "https://is.gd/xxxxx"}` on success, or `{"errorcode": ..., "errormessage": "..."}` on failure.

**Required interface:**

```python
class URLShortenerClient:
    def __init__(self, *, timeout: float = 5.0): ...
    def shorten(self, long_url: str) -> str: ...
    def close(self) -> None: ...           # close the underlying Session
    # Bonus: __enter__ / __exit__ for `with` support
```

**Requirements:**

- One `requests.Session` per client instance (set User-Agent).
- `shorten` raises a custom `ShortenError` on API errors or network failure.
- `shorten` validates that `long_url` starts with `http://` or `https://` before calling the API.
- A `__main__` block that shortens 2–3 hard-coded URLs and prints the results.

Bonus 1: implement `__enter__` and `__exit__` so the class works as a context manager.

Bonus 2: add a `@functools.lru_cache(maxsize=128)`-style cache on `shorten` so the same URL is not shortened twice in a session.
