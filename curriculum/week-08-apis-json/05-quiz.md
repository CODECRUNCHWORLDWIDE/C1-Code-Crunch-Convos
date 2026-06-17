# Week 8 — Quiz

10 multiple-choice questions. Pick the **single best** answer for each. Aim for 8/10 or higher to pass. Answers and explanations are at the end of the file — try the quiz before looking.

---

**1. What does HTTP status code `204` mean?**

- a) The server is redirecting you to another URL.
- b) The request succeeded but the response has no body.
- c) The resource was not found.
- d) The server is overloaded; retry later.

---

**2. Which of the following is the most idiomatic way to pass query parameters with `requests`?**

- a) `requests.get(f"https://api.x.com/items?id={id}&sort=desc")`
- b) `requests.get("https://api.x.com/items", params={"id": id, "sort": "desc"})`
- c) `requests.get("https://api.x.com/items", data={"id": id, "sort": "desc"})`
- d) `requests.get("https://api.x.com/items", json={"id": id, "sort": "desc"})`

---

**3. You make `r = requests.get(url)` and the call hangs for ten minutes before you Ctrl+C it. What is the fix?**

- a) Add `r.raise_for_status()` after the call.
- b) Wrap the call in `try`/`except`.
- c) Pass `timeout=` to `requests.get`.
- d) Use `requests.post` instead of `requests.get`.

---

**4. Which HTTP method is BOTH safe AND idempotent?**

- a) `POST`
- b) `PUT`
- c) `GET`
- d) `PATCH`

---

**5. What is the correct format for a Bearer token in an HTTP header?**

- a) `Authorization: <token>`
- b) `Authorization: Bearer <token>`
- c) `Bearer-Authorization: <token>`
- d) `Token: Bearer <token>`

---

**6. What does `response.raise_for_status()` do?**

- a) Always raises an exception.
- b) Raises an exception if the status code is `>= 400`.
- c) Raises an exception if the status code is exactly `500`.
- d) Returns `True` on success and `False` on failure.

---

**7. You want to avoid hard-coding an API key in your source file. Which sequence is correct?**

- a) Put the key in `.env`, commit `.env`, read with `os.environ`.
- b) Put the key in `config.py`, commit it, import the constant.
- c) Put the key in `.env`, add `.env` to `.gitignore`, load with `python-dotenv`, read with `os.environ`.
- d) Put the key in `secrets.json`, commit it, load with `json.load`.

---

**8. An API returns `429 Too Many Requests` with `Retry-After: 30`. What should your client do?**

- a) Retry immediately.
- b) Wait 30 seconds and then retry.
- c) Give up and raise an error.
- d) Reduce the request body size and retry.

---

**9. Which statement about REST is TRUE?**

- a) REST is a Python library you `pip install`.
- b) REST requires that every API use the same URL path conventions defined by the W3C.
- c) REST is a set of conventions for HTTP APIs; resources are nouns, methods are verbs.
- d) REST APIs always return XML.

---

**10. You are fetching many pages from the same host. What is the best `requests` pattern?**

- a) Call `requests.get(url)` in a loop.
- b) Open a `requests.Session()` and reuse it; let it pool TCP connections.
- c) Use `requests.post(url)` for every page.
- d) Use `urllib.request.urlopen` instead of `requests`.

---

## Answers

<details>
<summary>Click to reveal</summary>

1. **b** — `204 No Content` means the request succeeded but there is no body. Common after a `DELETE`. Don't call `.json()` on a 204 response; it will fail.

2. **b** — `params=` builds and URL-encodes the query string for you. Option (a) breaks on special characters; (c) sends a form-encoded body (wrong for `GET`); (d) sends a JSON body (wrong for `GET`).

3. **c** — `timeout=` is the only fix. Without it, `requests` waits forever. Get into the habit of *always* passing one.

4. **c** — `GET` is both safe (does not change state) and idempotent (repeating yields the same result). `PUT` and `DELETE` are idempotent but not safe. `POST` is neither.

5. **b** — The literal word `Bearer`, a single space, then the token. See RFC 6750.

6. **b** — `raise_for_status()` is a no-op for 1xx/2xx/3xx and raises `requests.HTTPError` for 4xx/5xx.

7. **c** — `.env` must be gitignored, with the example file `.env.example` committed. `python-dotenv` loads it; `os.environ` reads from it.

8. **b** — That is exactly what `Retry-After` means. The `HTTPAdapter`+`Retry` combo from lecture 2 does this automatically when `respect_retry_after_header=True`.

9. **c** — REST is a convention, not a library and not a standard URL scheme. The defining characteristic is "resources are URLs, methods are HTTP verbs".

10. **b** — A `Session` pools the underlying TCP+TLS connection, so subsequent requests skip the handshake. It also gives you a shared place for headers, auth, and retry policy.

</details>

---

## Score yourself

- **10/10** — You are ready for the challenges and mini-project.
- **8–9/10** — Solid. Re-read the lecture section for the questions you missed.
- **6–7/10** — Skim the lecture notes again, then retake.
- **< 6/10** — Re-read all three lecture notes carefully. The week's exercises depend on these concepts.
