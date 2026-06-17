# 02 — Using `requests`

> Read this after `01-http-and-rest.md`. By the end of this note you will know `requests` well enough to call any public REST API on the internet.

Python's standard library ships `urllib.request`, but almost no one uses it directly. Kenneth Reitz's [`requests`](https://requests.readthedocs.io/) library wraps it in a humane API and has been the de-facto HTTP client for Python for over a decade. If you do one `pip install` this week, make it this one.

---

## 1. Install

`requests` is a third-party package. Install it from PyPI:

```bash
python -m pip install requests
```

Inside a virtual environment (you set one up in Week 4):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows PowerShell
python -m pip install requests
```

Verify:

```python
>>> import requests
>>> requests.__version__
'2.31.0'
```

A quick mention of an alternative: [`httpx`](https://www.python-httpx.org/) is a newer library with a nearly-identical API plus async support and HTTP/2. Everything in this note works in `httpx` with the import line changed. We stick with `requests` because it is the one you will see in every code base, tutorial, and Stack Overflow answer.

---

## 2. Your first GET

```python
import requests

response = requests.get("https://httpbin.org/get")
print(response.status_code)   # 200
print(response.text[:200])    # first 200 chars of the body
```

That is it. Two lines of meaningful code and you have spoken HTTP.

The function `requests.get(url)` opens the connection, sends the request, reads the response, closes the connection, and returns a `Response` object. We will spend the next several sections poking at that object.

There are sibling functions for every HTTP method: `requests.post`, `requests.put`, `requests.patch`, `requests.delete`, `requests.head`, `requests.options`. They all return the same kind of `Response`.

---

## 3. Query parameters with `params=`

Suppose you want to call `https://httpbin.org/get?city=paris&units=metric`. **Do not** build the URL with string concatenation:

```python
# BAD — special characters in user input will break this
url = "https://httpbin.org/get?city=" + city + "&units=metric"
```

Use `params=`:

```python
import requests

response = requests.get(
    "https://httpbin.org/get",
    params={"city": "paris", "units": "metric"},
)
print(response.url)
# https://httpbin.org/get?city=paris&units=metric
```

`requests` URL-encodes the keys and values for you. If `city` were `"São Paulo"`, the library produces `city=S%C3%A3o+Paulo` correctly, with no effort on your part. If you ever wrote `requests.get(f"...?q={user_input}")`, audit your old code — it has bugs.

Lists become repeated keys:

```python
requests.get("https://httpbin.org/get", params={"tag": ["python", "api"]}).url
# https://httpbin.org/get?tag=python&tag=api
```

`None` values are omitted:

```python
requests.get("https://httpbin.org/get", params={"city": "paris", "units": None}).url
# https://httpbin.org/get?city=paris
```

---

## 4. Headers

Headers carry metadata. You set them with the `headers=` argument:

```python
import requests

response = requests.get(
    "https://api.github.com/users/octocat",
    headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "code-crunch-bootcamp/1.0 (learning)",
    },
)
```

The three you will set most often:

| Header | What it does |
|---|---|
| `User-Agent` | Identifies your client. Many APIs reject the default `python-requests/2.x` UA. Set it to something descriptive. |
| `Accept` | Tells the server what response format you want. `application/json` is the common case. |
| `Content-Type` | Describes the *request* body. Required for `POST`/`PUT`/`PATCH`. `requests` sets this automatically when you use `json=`. |
| `Authorization` | API keys and bearer tokens go here (next lecture). |

Header names are case-insensitive in HTTP, but stick to the conventional capitalization (`Content-Type`, not `CONTENT-type`) so your code reads cleanly.

---

## 5. The `Response` object

Everything you need is on this object. Here are the attributes you will use weekly:

```python
import requests

r = requests.get("https://httpbin.org/get", params={"city": "paris"})

r.status_code   # 200
r.ok            # True if status_code < 400
r.reason        # 'OK'
r.url           # 'https://httpbin.org/get?city=paris'
r.headers       # case-insensitive dict of response headers
r.headers["content-type"]  # 'application/json'
r.text          # body as a str (decoded with r.encoding)
r.content       # body as raw bytes
r.json()        # parses body as JSON, returns dict or list
r.elapsed       # timedelta from send to last-byte-received
r.request       # the PreparedRequest that was sent
r.history       # list of intermediate Responses if redirects were followed
```

Two patterns to internalize:

**Parsing JSON.** `r.json()` is a method, not a property. It calls `json.loads(r.text)` and returns a Python object. If the body is not valid JSON it raises `requests.exceptions.JSONDecodeError`:

```python
import requests

r = requests.get("https://httpbin.org/get")
data = r.json()
print(type(data))   # <class 'dict'>
print(data["url"])  # 'https://httpbin.org/get'
```

**Checking status.** Don't manually check `if r.status_code == 200`. Use `r.raise_for_status()`:

```python
r = requests.get("https://httpbin.org/status/404")
r.raise_for_status()
# requests.exceptions.HTTPError: 404 Client Error: NOT FOUND for url: ...
```

It is a no-op for `1xx`/`2xx`/`3xx` and raises `HTTPError` for `4xx`/`5xx`. Combine with a `try`/`except` if you want a custom message.

---

## 6. POST with a JSON body

For `POST`, `PUT`, and `PATCH` you usually want to send a JSON document. The cleanest way is `json=`:

```python
import requests

payload = {"title": "Hello", "tags": ["python", "api"]}
r = requests.post("https://httpbin.org/post", json=payload)
r.raise_for_status()

echoed = r.json()["json"]
assert echoed == payload
```

`json=payload` does three things for you:

1. Calls `json.dumps(payload)` to serialize it.
2. Sets `Content-Type: application/json`.
3. Sends the result as the request body.

If you need to send form-encoded data (the kind `<form>` tags submit), use `data={...}` instead. If you need to upload a file, use `files={...}`. Plain bytes go in `data=b"..."`.

---

## 7. Timeouts — always set one

This is the single most important habit to build. By default, `requests` will wait **forever** for the server to respond. A hung process is worse than a failed one. Always pass `timeout=`:

```python
import requests

r = requests.get("https://httpbin.org/delay/2", timeout=5)
```

`timeout=5` is "5 seconds for *each* of connect-time and read-time". You can split them:

```python
r = requests.get(url, timeout=(3, 10))  # 3s to connect, 10s to read
```

If the server is slower than the timeout, `requests` raises `requests.exceptions.Timeout`. Catch it:

```python
import requests

try:
    r = requests.get(url, timeout=5)
except requests.exceptions.Timeout:
    print("Server too slow; giving up.")
```

Rule of thumb: **every request in production code has a `timeout=`**. If a reviewer sees a request without one, that is a bug.

---

## 8. Error handling — the full pattern

`requests` raises several exception types, all subclasses of `requests.exceptions.RequestException`. The ones you actually catch:

| Exception | Cause |
|---|---|
| `ConnectionError` | DNS failure, refused connection, network down |
| `Timeout` | `timeout=` exceeded |
| `HTTPError` | Raised by `raise_for_status()` for `4xx`/`5xx` |
| `TooManyRedirects` | More than 30 redirects (configurable) |
| `JSONDecodeError` | `.json()` called on a non-JSON body |
| `RequestException` | Base class — catch this for "any HTTP error" |

A robust call looks like this:

```python
import requests
from requests.exceptions import RequestException

def fetch_user(login: str) -> dict | None:
    url = f"https://api.github.com/users/{login}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        print(f"Could not fetch {login!r}: {exc}")
        return None
```

The `RequestException` catch-all covers every network failure mode. Inside the `try` block, `raise_for_status()` converts `4xx`/`5xx` responses into exceptions so the same handler covers them too. Exercise 05 has you build a more elaborate version of this with retries.

---

## 9. Sessions — reuse connections, share headers

If you make more than two requests to the same host, switch from the module-level `requests.get` to a `Session`:

```python
import requests

with requests.Session() as session:
    session.headers.update({
        "User-Agent": "code-crunch-bootcamp/1.0",
        "Accept": "application/json",
    })

    r1 = session.get("https://api.github.com/users/octocat")
    r2 = session.get("https://api.github.com/users/torvalds")
    r3 = session.get("https://api.github.com/users/gvanrossum")
```

Two benefits:

1. **Connection pooling.** The TCP+TLS handshake is reused across requests to the same host. With three requests, this saves roughly 100–300 ms.
2. **Shared state.** Headers, auth, and cookies set on the session apply to every call.

You can pass per-call overrides; they merge with the session defaults.

A `Session` is itself a context manager — the `with` statement closes the underlying connection pool when you exit. Use it.

---

## 10. Retries with `HTTPAdapter`

Networks fail. Servers blip. Anything `5xx` or a transient `Timeout` is usually fixed by trying again. `requests` ships with retry support via `urllib3`. Wire it onto a `Session` once and forget about it:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=5,                                     # at most 5 retries
        backoff_factor=1.0,                          # wait 1s, 2s, 4s, 8s, 16s
        status_forcelist=[429, 500, 502, 503, 504],  # retry these statuses
        allowed_methods=["GET", "HEAD", "OPTIONS"],  # idempotent only
        respect_retry_after_header=True,             # honor 429 Retry-After
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
```

Use it:

```python
session = make_session()
r = session.get("https://api.example.com/data", timeout=5)
r.raise_for_status()
```

Three things to notice:

- `allowed_methods` defaults to safe/idempotent methods. We *do not* retry `POST` automatically — see lecture 1 on idempotency.
- `backoff_factor=1.0` produces waits of `0, 2, 4, 8, 16` seconds (formula: `factor * (2 ** (n-1))`). Increase the factor if your API has tight rate limits.
- `respect_retry_after_header=True` is the polite default — when the server responds `429 Too Many Requests` with a `Retry-After: 30` header, the library waits 30 seconds.

Exercise 05 walks through this end to end.

---

## 11. A complete realistic example

Putting it all together — a function that fetches a Pokémon by name, with timeout, retries, error handling, and a typed return value:

```python
"""pokemon.py — minimal PokeAPI client."""

from typing import TypedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Pokemon(TypedDict):
    name: str
    height_dm: int      # decimetres in the API
    types: list[str]


def _session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "code-crunch-bootcamp/1.0",
        "Accept": "application/json",
    })
    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_pokemon(name: str, *, timeout: float = 5.0) -> Pokemon:
    """Fetch one Pokémon by name. Raises requests.HTTPError on failure."""
    with _session() as s:
        r = s.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=timeout)
        r.raise_for_status()
        data = r.json()
    return Pokemon(
        name=data["name"],
        height_dm=data["height"],
        types=[t["type"]["name"] for t in data["types"]],
    )


if __name__ == "__main__":
    print(fetch_pokemon("pikachu"))
```

Run it:

```bash
$ python pokemon.py
{'name': 'pikachu', 'height_dm': 4, 'types': ['electric']}
```

Every piece — `Session`, `timeout`, `raise_for_status`, retry policy, typed return — is exactly what you would write in a production code base.

---

## 12. Inspecting requests in flight

Two debugging tricks worth keeping in your toolbox.

**Print the prepared request.** `requests` builds a `PreparedRequest` before sending. You can introspect it:

```python
import requests

req = requests.Request("GET", "https://httpbin.org/get", params={"x": 1})
prep = req.prepare()
print(prep.method, prep.url)
print(prep.headers)
print(prep.body)
```

**Enable verbose HTTP logging.** Set the `urllib3` logger to DEBUG and you see every header on the wire:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
```

When something is mysteriously broken, this is usually how you find out.

---

## 13. Common gotchas

A short list of things that bite beginners. Read them now; you will recognize them in the wild later.

- **Forgetting `.json()`.** `r.text` is a string. `r.json()` is the parsed object. `r.text["url"]` is a `TypeError`.
- **Forgetting `timeout=`.** Your script will hang and you will think it's broken. It is — just slowly.
- **Building URLs by hand.** Always use `params=`. Special characters break naive string concatenation.
- **Reading huge files into memory.** For multi-megabyte downloads, pass `stream=True` and iterate `r.iter_content(chunk_size=8192)`.
- **Sharing `requests.get` across many calls.** Use a `Session` instead — connection pooling is free performance.
- **Trusting `r.encoding`.** It is guessed from the `Content-Type` header. If garbage comes out of `r.text`, try `r.content.decode("utf-8")` explicitly.
- **`.json()` on an empty body.** A `204 No Content` response has no body; `.json()` raises. Check `r.status_code != 204` first.

---

## 14. What to remember

- `requests.get/post/...` returns a `Response`. Inspect `.status_code`, `.headers`, `.json()`.
- Always set `timeout=`. Always.
- Use `params=` for query strings, `json=` for JSON bodies, `headers=` for headers.
- `r.raise_for_status()` converts `4xx`/`5xx` into exceptions.
- For more than one call to the same host, use a `requests.Session` (as a context manager).
- Attach an `HTTPAdapter` with `Retry` to retry idempotent calls on transient failures.

In `03-authentication-and-secrets.md` we add the missing piece: how to prove who you are to APIs that demand a key or token, and how to keep those secrets out of git.
