# 01 — HTTP and REST

> Read this first. Everything else in Week 8 assumes you understand the request/response cycle, what a status code is, and what makes an API "RESTful".

When you type `https://en.wikipedia.org/wiki/Python` into a browser and press Enter, a *lot* of things happen. The browser opens a TCP connection to a Wikipedia server, sends a few hundred bytes of text describing what it wants, and the server sends back a response that the browser turns into the page you read. That conversation — the bytes that travel back and forth — speaks a protocol called **HTTP**, the HyperText Transfer Protocol. Every "API call" you will make this week is exactly the same kind of conversation, only your Python program plays the role the browser usually plays.

This note covers what is actually in those bytes, how to read status codes, what a URL really is, and what people mean when they call an API "RESTful".

---

## 1. The client–server model

HTTP is a **request/response** protocol between two roles: a **client** and a **server**.

```
                  HTTP REQUEST
        ─────────────────────────────►
┌────────────┐                        ┌─────────────┐
│            │                        │             │
│  CLIENT    │                        │   SERVER    │
│  (you)     │                        │  (api.x.com)│
│            │                        │             │
└────────────┘                        └─────────────┘
        ◄─────────────────────────────
                  HTTP RESPONSE
```

The client always speaks first. It opens a connection, sends one request, and waits. The server reads the request, does some work (querying a database, calling another service, computing the weather), and writes back one response. Then either side may close the connection, or the client may send another request on the same connection (this is called "keep-alive" — `requests.Session` does it for you automatically).

The client is the *active* party. A server cannot push data to a client that did not ask for it. (WebSockets and Server-Sent Events get around this, but they are layered on top of HTTP and out of scope this week.)

In Week 8, **you** are always the client. You write Python that opens connections to public servers and reads back JSON.

---

## 2. Anatomy of an HTTP request

Every HTTP request is just text. Here is exactly what flies over the wire when you `requests.get("https://httpbin.org/get?city=paris")`:

```http
GET /get?city=paris HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.31.0
Accept: */*
Accept-Encoding: gzip, deflate

```

Four parts to memorize:

1. **The request line** — `GET /get?city=paris HTTP/1.1`
   - **Method**: `GET`. Tells the server what kind of action.
   - **Path + query string**: `/get?city=paris`. What you want and any parameters.
   - **HTTP version**: `HTTP/1.1`. You almost never care.
2. **Headers** — one per line, `Name: Value`. Metadata about the request. The `Host` header is required; everything else (`User-Agent`, `Accept`, `Authorization`, …) is conventional.
3. **A blank line** separates headers from body.
4. **Body** (optional) — present on `POST`, `PUT`, `PATCH`. The actual payload (a JSON document, a form submission, a file upload). `GET` requests have no body.

You will never type this raw text in Python — `requests` builds it for you — but recognizing it makes the rest of the week click.

---

## 3. Anatomy of an HTTP response

The server replies with the same four-part structure:

```http
HTTP/1.1 200 OK
Date: Tue, 12 May 2026 14:23:01 GMT
Content-Type: application/json
Content-Length: 287

{
  "args": {"city": "paris"},
  "headers": {...},
  "origin": "203.0.113.42",
  "url": "https://httpbin.org/get?city=paris"
}
```

1. **The status line** — `HTTP/1.1 200 OK`
   - **Status code**: `200`. A three-digit number that tells you what happened.
   - **Reason phrase**: `OK`. Human-readable; ignore it.
2. **Headers** — metadata about the response (content type, length, caching info, rate-limit info).
3. **Blank line.**
4. **Body** — the actual payload (HTML, JSON, an image, anything).

In Python, every piece becomes an attribute on a `Response` object: `r.status_code`, `r.headers`, `r.text` or `r.content`, `r.json()`.

---

## 4. HTTP methods (verbs)

The method tells the server what kind of operation you want. There are nine in the spec; five are common, the other four are rare.

| Method | Purpose | Has body? | Safe? | Idempotent? |
|---|---|---|---|---|
| `GET` | **Read** a resource | No | Yes | Yes |
| `POST` | **Create** a new resource (or trigger an action) | Yes | No | No |
| `PUT` | **Replace** a resource entirely | Yes | No | Yes |
| `PATCH` | **Modify** part of a resource | Yes | No | No (usually) |
| `DELETE` | **Remove** a resource | No (usually) | No | Yes |

**Safe** means "does not change server state". `GET` should never delete your data — if it does, the API is broken.

**Idempotent** means "doing it twice gives the same result as doing it once". Calling `DELETE /users/42` twice is fine: after the first call the user is gone, after the second call they are still gone. Calling `POST /orders` twice is *not* fine: you just placed two orders. This distinction matters when your network drops a response and you want to know whether to retry.

A handy mnemonic: **C**reate=POST, **R**ead=GET, **U**pdate=PUT/PATCH, **D**elete=DELETE. CRUD.

---

## 5. Status codes

The first digit tells you everything. The remaining two add detail.

| Range | Family | Meaning | Examples |
|---|---|---|---|
| `1xx` | Informational | Rare; "I am still working" | `100 Continue`, `101 Switching Protocols` |
| `2xx` | Success | It worked | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirection | Look somewhere else | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | Client error | *You* did something wrong | `400 Bad Request`, `404 Not Found`, `429 Too Many Requests` |
| `5xx` | Server error | *They* did something wrong | `500 Internal Server Error`, `503 Service Unavailable` |

The five you will see most often in each family:

**2xx — Success**

| Code | Name | When you see it |
|---|---|---|
| `200` | OK | Normal successful `GET` or `PATCH`. Body has the data. |
| `201` | Created | After a successful `POST`. Usually includes a `Location` header pointing to the new resource. |
| `202` | Accepted | "I received it, I will work on it later." Common for async jobs. |
| `204` | No Content | Success, but the body is empty. Typical for `DELETE`. |
| `206` | Partial Content | Range requests (downloading half a video). |

**3xx — Redirection**

| Code | Name | When you see it |
|---|---|---|
| `301` | Moved Permanently | URL changed forever. Update your bookmark. |
| `302` | Found | Temporary redirect. Try this other URL for now. |
| `303` | See Other | After a `POST`, "go GET this other URL to see the result". |
| `304` | Not Modified | "Your cached copy is still good." Returned when you send `If-None-Match`. |
| `307` | Temporary Redirect | Like 302 but the method must not change. |

`requests` follows `3xx` redirects automatically. Pass `allow_redirects=False` to see them.

**4xx — Client error**

| Code | Name | When you see it |
|---|---|---|
| `400` | Bad Request | Your JSON was malformed or a required field is missing. |
| `401` | Unauthorized | You did not authenticate. Add a header. |
| `403` | Forbidden | You authenticated, but you are not allowed. |
| `404` | Not Found | The URL points to nothing. |
| `429` | Too Many Requests | You hit a rate limit. Slow down and check `Retry-After`. |

**5xx — Server error**

| Code | Name | When you see it |
|---|---|---|
| `500` | Internal Server Error | Their code crashed. File a bug. |
| `502` | Bad Gateway | A proxy in front of the server got a bad reply. |
| `503` | Service Unavailable | Server is overloaded or in maintenance. Retry later. |
| `504` | Gateway Timeout | A proxy waited too long for the upstream server. |
| `507` | Insufficient Storage | Disk full. Rare. |

In Python, `response.raise_for_status()` raises an `HTTPError` if the code is `>= 400`. We will lean on this constantly.

---

## 6. URLs decoded

A URL looks like one string but has up to six parts. Memorize them:

```
 https://api.example.com:443/v1/users/42?fields=name,email#section
 \___/   \______________/\_/\__________/\_______________/\_____/
   |            |         |       |            |             |
 scheme       host      port    path    query string    fragment
```

| Part | Example | Meaning |
|---|---|---|
| **scheme** | `https` | Protocol — almost always `http` or `https`. Use `https` everywhere. |
| **host** | `api.example.com` | The server's domain name. |
| **port** | `:443` | TCP port. Defaults to `80` for `http` and `443` for `https`; usually omitted. |
| **path** | `/v1/users/42` | Which resource on that server. |
| **query string** | `?fields=name,email` | Key-value pairs. Multiple keys joined by `&`. URL-encoded. |
| **fragment** | `#section` | Client-side only. Never sent to the server. |

The **query string** is where you put parameters that modify a `GET`. In `requests` you build it with the `params=` argument, never by string-concatenating. We will harp on this in lecture 2.

---

## 7. REST conventions

**REST** stands for **Representational State Transfer**. It is not a protocol or a library — it is a **set of conventions** for designing HTTP APIs that became dominant in the 2010s. An API is "RESTful" when it follows these conventions:

1. **Resources have URLs.** A resource is a noun: a user, a post, an order. Its URL identifies it.
   - `/users` — collection of users
   - `/users/42` — the user with id 42
   - `/users/42/posts` — the posts belonging to user 42
2. **Verbs are HTTP methods, not URLs.** The URL says *what*, the method says *how*.
   - `GET /users/42` — read user 42
   - `DELETE /users/42` — remove user 42
   - **Not** `GET /deleteUser?id=42`. (Yes, you will see that in the wild. It is bad REST.)
3. **State is transferred as a representation**, usually JSON. The server stores the canonical user, you receive a JSON copy.
4. **Statelessness.** Every request carries everything the server needs to handle it. The server keeps no session for you between requests (cookies and tokens are the workaround; they live in headers on every call).

This is why REST endpoints feel predictable. Once you see `GET /repos/{owner}/{repo}/issues` you can guess that `POST /repos/{owner}/{repo}/issues` creates an issue and `DELETE /repos/{owner}/{repo}/issues/3` closes one.

---

## 8. Idempotency in practice

Idempotency matters when networks fail. Imagine you call `POST /orders` and your Wi-Fi dies before the response arrives. Did the server place the order or not? You do not know. If you retry, you might double-order.

The fix is one of:

- **Use an idempotent method** when possible. `PUT /orders/abc-123` with a client-generated id is safe to retry — the second call overwrites the first with identical data.
- **Send an idempotency key** — a unique header like `Idempotency-Key: abc-123`. The server remembers it. Stripe, Square, and most payment APIs require this.
- **Check before retrying** — `GET /orders?clientRef=abc-123` to see if it already exists.

Frameworks like `requests` will retry idempotent methods automatically (when you configure a `Retry`) but refuse to retry `POST` by default. Now you know why.

---

## 9. REST vs GraphQL (a brief mention)

REST is not the only game in town. **GraphQL** is an alternative query language for APIs developed by Facebook. Instead of many endpoints each returning a fixed shape, GraphQL exposes **one** endpoint (`POST /graphql`) and lets the client ask for exactly the fields it wants:

```graphql
query {
  user(login: "octocat") {
    name
    repositories(first: 5) {
      nodes { name stargazerCount }
    }
  }
}
```

The server responds with JSON in the same shape as the query. One round-trip, no over-fetching, no under-fetching. GitHub, Shopify, and Contentful all expose GraphQL APIs alongside their REST ones.

When to consider GraphQL:

- Your client needs deeply nested data and you would otherwise make many REST calls.
- The shape of "what to fetch" varies a lot between screens.
- You control both the client and the server.

When to stick with REST:

- Simple CRUD on flat resources.
- You want HTTP caching at the URL level (GraphQL kills CDN caching).
- The API is consumed by many unknown clients.

That is all you need for this week. We will not write GraphQL queries in Week 8, but if you finish early, the stretch goals point you at GitHub's GraphQL API.

---

## 10. What to remember

If you forget everything else, remember this:

- HTTP is a **request/response text protocol**. Both sides have a status line, headers, blank line, body.
- The **method** says what kind of action. The **status code** says what happened. The **URL** says where.
- **2xx good, 4xx your fault, 5xx their fault.**
- A URL has parts: **scheme, host, path, query string**. Build query strings with `params=`, never with `+`.
- **REST** is a convention, not a library. Resources are nouns; methods are verbs.
- **Idempotency** is "safe to retry". `GET`, `PUT`, `DELETE` are idempotent; `POST` is not.

Next up — `02-using-requests.md` — we put this knowledge through Python's most-loved third-party library.
