# 03 — Authentication and Secrets

> Read this after `02-using-requests.md`. By the end you will know how to authenticate to APIs that require it, how to keep credentials out of git, and how to be a polite client that respects rate limits.

Most "free" APIs we use this week need no authentication at all — that is why we picked them. But the moment you reach for OpenAI, Stripe, Twilio, Reddit, or your employer's internal services, you will need credentials. This note covers the three common authentication schemes, where to put the secrets, and how to back off when an API tells you to slow down.

---

## 1. The three authentication schemes you will meet

In rough order of frequency:

1. **API key** — a long random string, usually passed as a header or query parameter. Identifies *your application*. Used by Open-Meteo's commercial tier, Anthropic, Mailgun, weather APIs, most public services.
2. **Bearer token** — a longer string in the `Authorization` header. Often issued by OAuth or signed (JWT). Used by GitHub, Spotify, every "Login with…" flow.
3. **HTTP Basic Auth** — a username and password sent in every request. Older, less common, still used by some internal APIs and `httpbin` for practice.

There are others — OAuth flows, AWS SigV4, mutual TLS, HMAC — but those three cover roughly 95% of beginner cases.

---

## 2. API keys

The most common pattern. The provider gives you a string like `sk_live_abc123...` and you include it on every request. There are two places to put it:

**As a header (preferred):**

```python
import requests

API_KEY = "sk_live_abc123..."

r = requests.get(
    "https://api.example.com/v1/items",
    headers={"X-API-Key": API_KEY},
    timeout=5,
)
r.raise_for_status()
```

Headers are not logged by most web servers, so this is the safer place.

**As a query parameter (only if the API requires it):**

```python
import requests

API_KEY = "sk_live_abc123..."

r = requests.get(
    "https://api.example.com/v1/items",
    params={"api_key": API_KEY, "limit": 10},
    timeout=5,
)
```

Query parameters end up in server logs, browser history, and Referer headers. Avoid this when you have a choice — but some APIs (notably older weather services and Google's URL Shortener) only accept query-string keys. In that case, use it and shrug.

Whichever location: **never hardcode the literal string in your source file**. We will fix this in section 5.

---

## 3. Bearer tokens

The modern standard, defined in [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750.html). You receive a token from an OAuth flow or a "create token" page in the provider's dashboard, then send it as:

```
Authorization: Bearer <token>
```

In Python:

```python
import requests

TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

r = requests.get(
    "https://api.github.com/user",
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=5,
)
r.raise_for_status()
print(r.json()["login"])
```

The `f"Bearer {TOKEN}"` literal is on purpose: the spec wants the word "Bearer", a single space, and the token. Get this wrong and the server returns `401`.

GitHub accepts both `Bearer` and the older `token` prefix; new code should use `Bearer`. Some APIs use the `Authorization` header with no prefix at all (`Authorization: <token>`) — read their docs.

---

## 4. HTTP Basic Auth

The oldest scheme. You send `Authorization: Basic <base64(user:password)>`. `requests` does the base64 step for you:

```python
import requests

r = requests.get(
    "https://httpbin.org/basic-auth/alice/secret",
    auth=("alice", "secret"),
    timeout=5,
)
r.raise_for_status()
print(r.json())
```

The `auth=` argument accepts a `(username, password)` tuple. There is also `requests.auth.HTTPBasicAuth(user, pwd)` for explicitness, and `HTTPDigestAuth` for the digest variant.

Basic Auth is **not encryption**. Anyone who sniffs the wire can base64-decode the header instantly. It only makes sense over HTTPS.

---

## 5. Keeping secrets out of source control

If you remember nothing else from this note, remember: **API keys and tokens must never end up in git.**

The path to leaked credentials is depressingly predictable: you paste the key into your script, commit, push to GitHub, two minutes later GitHub's secret-scanner DMs you that your key is public, two days later someone has racked up $4,000 in API charges on your account. People build bots that scrape every new public commit. Treat any key that has touched a public repo as **already compromised** — rotate it immediately.

The professional pattern:

1. Put secrets in a file called `.env`.
2. Add `.env` to `.gitignore`.
3. Commit a `.env.example` file with **placeholders** so collaborators know which variables to set.
4. Load `.env` at runtime with `python-dotenv`.
5. Read the values from `os.environ` in your code.

Step by step:

### 5a. The `.env` file

Plain text, key=value, one per line, no quotes needed:

```
# .env  — never commit this file
OPENMETEO_KEY=
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APP_ENV=dev
```

(Open-Meteo's free tier needs no key, hence the empty value — included for the mini-project's optional commercial-tier mode.)

### 5b. The `.gitignore` entry

Add (or verify) this line in `.gitignore` at the project root:

```
.env
.env.local
```

Run `git status` after touching `.env`. If `.env` shows up as untracked, you are safe; if it shows up as modified, you committed it earlier and need to scrub history (and rotate the key — see above).

### 5c. The `.env.example` file

Commit this. It documents the schema for the next person who clones your repo:

```
# .env.example — commit this; fill in real values in .env
OPENMETEO_KEY=
GITHUB_TOKEN=
APP_ENV=dev
```

### 5d. Loading with `python-dotenv`

Install it once:

```bash
python -m pip install python-dotenv
```

At the top of your entry-point script (and only there — not in library modules):

```python
"""app.py"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into os.environ

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
APP_ENV = os.getenv("APP_ENV", "dev")  # default if missing
```

`os.environ["KEY"]` raises `KeyError` if the variable is missing. `os.getenv("KEY", default)` returns the default instead. Use the strict form for things that *must* be set, the loose form for things that are optional.

### 5e. Bonus — fail loud on startup

A common production trick: validate required env vars at import time, so a misconfigured deploy crashes immediately instead of half-way through a customer request:

```python
"""config.py"""
import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED = ["GITHUB_TOKEN"]
missing = [k for k in REQUIRED if not os.environ.get(k)]
if missing:
    raise RuntimeError(f"Missing required env vars: {missing}")

GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
```

---

## 6. Environment variables in real life

`python-dotenv` is a development convenience. In production you usually do **not** ship a `.env` file at all — your hosting platform injects environment variables for you:

- **Heroku / Render / Railway / Fly.io** — set them in the dashboard.
- **Docker** — `docker run -e GITHUB_TOKEN=... your-image` or a `--env-file .env`.
- **Kubernetes** — `Secret` objects mounted as env vars or files.
- **GitHub Actions** — repository secrets, exposed as env vars in workflow steps.

The point of using `os.environ` in code (rather than reading `.env` directly) is that the same code works in every environment. Local development reads from `.env`; production reads from the cloud provider. Your Python is unchanged.

---

## 7. Rate limits

APIs limit how often you can call them. Hitting the limit is normal, expected, and not an error in your code — but you must handle it gracefully.

There are two common rate-limit signals:

**Hard limit — `429 Too Many Requests`.** The server flat-out refuses. The response usually carries a `Retry-After` header telling you how long to wait (in seconds, or as an HTTP date):

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

**Quota headers.** Many APIs (GitHub, Twitter, Stripe) include current quota state on every response:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 12
X-RateLimit-Reset: 1747144800
```

Read these and slow down *before* you hit `429`. Snippet:

```python
import requests

r = requests.get("https://api.github.com/users/octocat", timeout=5)
remaining = int(r.headers.get("X-RateLimit-Remaining", "1"))
if remaining < 5:
    print(f"Slowing down — only {remaining} requests left this window.")
```

---

## 8. Backoff with `time.sleep`

The simplest possible retry-after-429 loop:

```python
import time
import requests

def get_with_backoff(url: str, *, max_attempts: int = 5, timeout: float = 5.0) -> requests.Response:
    delay = 1.0  # seconds
    for attempt in range(1, max_attempts + 1):
        r = requests.get(url, timeout=timeout)
        if r.status_code != 429:
            return r
        wait = int(r.headers.get("Retry-After", delay))
        print(f"[attempt {attempt}] 429; sleeping {wait}s")
        time.sleep(wait)
        delay *= 2  # exponential backoff if no Retry-After header
    return r  # caller can still inspect / raise
```

The pattern is:

1. Try the request.
2. If it succeeds (or fails with anything other than `429`), return.
3. Read the `Retry-After` header if present; otherwise fall back to a doubling timer.
4. Sleep, then loop.

For anything beyond a toy script, prefer the `HTTPAdapter` + `Retry` approach from lecture 2 — it already handles `429` and `Retry-After` correctly, and it also retries `5xx` transient failures. Hand-rolled loops are useful when you want custom logging or jitter.

### 8a. Exponential backoff with jitter

If many clients all retry exactly `1, 2, 4, 8` seconds after a server outage, they all hit the recovering server at the same instant — a "thundering herd". The fix is **jitter**: add a random component:

```python
import random
import time

def jittered_sleep(base: float) -> None:
    """Sleep base seconds plus 0–base seconds of random jitter."""
    time.sleep(base + random.uniform(0, base))
```

Use it inside the backoff loop. The `Retry` class supports this with `backoff_jitter=…` since urllib3 2.0.

---

## 9. Putting it all together — a polite client

A minimal, production-shaped GitHub client:

```python
"""github_client.py — a small, polite client for the GitHub REST API."""

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # optional; raises rate limit


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "code-crunch-bootcamp/1.0",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if GITHUB_TOKEN:
        s.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    retry = Retry(
        total=4,
        backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def get_user(login: str) -> dict[str, Any]:
    with _session() as s:
        r = s.get(f"https://api.github.com/users/{login}", timeout=5)
        _watch_rate_limit(r)
        r.raise_for_status()
        return r.json()


def _watch_rate_limit(r: requests.Response) -> None:
    remaining = r.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) < 5:
        reset = int(r.headers.get("X-RateLimit-Reset", "0"))
        wait = max(0, reset - int(time.time()))
        print(f"!! only {remaining} GitHub requests left; resets in {wait}s")


if __name__ == "__main__":
    print(get_user("octocat")["name"])
```

This file demonstrates every idea in this lecture:

- Token from `.env` via `python-dotenv`.
- `Bearer` token in the `Authorization` header.
- `User-Agent` so GitHub knows who is calling.
- `Session` with `HTTPAdapter` + `Retry` so transient `5xx` and `429` are handled automatically.
- A pro-active rate-limit check on the response headers.
- `raise_for_status()` for hard failures.

Reread it after Exercise 05 and the patterns will feel obvious.

---

## 10. What to remember

- Three common schemes: **API key**, **Bearer token**, **HTTP Basic Auth**.
- Put secrets in `.env`, add `.env` to `.gitignore`, commit a `.env.example`.
- Load with `python-dotenv` in your entry point, read via `os.environ`.
- Production replaces `.env` with platform-injected env vars — your code does not change.
- `429 Too Many Requests` + `Retry-After` is the standard rate-limit signal.
- Use **exponential backoff with jitter**, or just configure `urllib3.util.retry.Retry` and let `requests` do it.

You now have everything you need for the rest of Week 8. Start the exercises.
