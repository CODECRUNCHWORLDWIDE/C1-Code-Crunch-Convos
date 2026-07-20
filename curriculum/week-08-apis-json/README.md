# Week 8 — APIs, JSON & HTTP

Welcome to Week 8 of **Code Crunch Convos**, our open-source Python bootcamp. Until now your programs read local files and computed local answers. This week your programs reach across the internet, ask remote servers for data, and send data back. You will leave this week able to call any modern REST API, parse the JSON it returns, handle errors and rate limits, and ship a small CLI that turns a city name into a weather forecast.

Every API we use is **free** and most need **no key at all** — you can start coding immediately, no signup, no credit card, no waiting for approvals.

---

## Learning objectives

By the end of Week 8 you will be able to:

1. Explain the HTTP **request/response** cycle and identify the parts of a URL.
2. Choose the correct **HTTP method** (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) for a task.
3. Read and reason about **status codes** in the `2xx`, `3xx`, `4xx`, and `5xx` families.
4. Install and use the **`requests`** library to make HTTP calls.
5. Pass **query parameters** with `params=` and **JSON bodies** with `json=`.
6. Set custom **headers** (`User-Agent`, `Accept`, `Content-Type`, `Authorization`).
7. Inspect a `Response` object — `.status_code`, `.headers`, `.text`, `.json()`.
8. Handle network failure with **`timeout=`**, **`raise_for_status()`**, and `try`/`except`.
9. Authenticate with **API keys**, **Bearer tokens**, and **HTTP Basic Auth**.
10. Implement **pagination** strategies — page-number, offset/limit, cursor, and `Link` header.
11. Respect **rate limits** with `time.sleep` and exponential **backoff** with retries.
12. Keep secrets out of source control with **`.env`** files and `python-dotenv`.
13. Recognize when **GraphQL** might be a better fit than REST (high level).
14. Build a small, well-structured **CLI tool** that wraps an external API.

---

## Prerequisites

You should be comfortable with everything from Weeks 1–7:

- **Week 1** — running `.py` files from the terminal.
- **Week 2** — strings, f-strings, basic types.
- **Week 3** — `if`/`for`/`while` control flow.
- **Week 4** — defining functions, modules, type hints, `argparse` basics.
- **Week 5** — lists and dicts (you will navigate deeply nested JSON).
- **Week 6** — `try`/`except`, `json.load`/`dump`, `pathlib.Path` for saving history.
- **Week 7** — classes (we will sketch a tiny API client class in homework).

If JSON parsing or dict navigation feels shaky, re-read `week-06-file-io-exceptions/lecture-notes/02-csv-and-json.md` before you start.

---

## Topics

| # | Topic | Where |
|---|---|---|
| 1 | Client–server model, HTTP request anatomy | `lecture-notes/01-http-and-rest.md` |
| 2 | HTTP methods (`GET`/`POST`/`PUT`/`PATCH`/`DELETE`) | `lecture-notes/01-http-and-rest.md` |
| 3 | Status codes (2xx/3xx/4xx/5xx) | `lecture-notes/01-http-and-rest.md` |
| 4 | URLs — scheme, host, path, query string | `lecture-notes/01-http-and-rest.md` |
| 5 | REST conventions and idempotency | `lecture-notes/01-http-and-rest.md` |
| 6 | Installing and using `requests` | `lecture-notes/02-using-requests.md` |
| 7 | Query params, headers, JSON bodies | `lecture-notes/02-using-requests.md` |
| 8 | The `Response` object and `.json()` | `lecture-notes/02-using-requests.md` |
| 9 | Timeouts, sessions, retries with `HTTPAdapter` | `lecture-notes/02-using-requests.md` |
| 10 | API keys, Bearer tokens, Basic auth | `lecture-notes/03-authentication-and-secrets.md` |
| 11 | `.env` files with `python-dotenv` | `lecture-notes/03-authentication-and-secrets.md` |
| 12 | Rate limits and exponential backoff | `lecture-notes/03-authentication-and-secrets.md` |
| 13 | Pagination patterns | `exercises/exercise-04-pagination.py` |
| 14 | REST vs GraphQL (brief mention) | `lecture-notes/01-http-and-rest.md` |

---

## Suggested schedule (~36 hours)

This is a self-paced suggestion. Most learners spend **30–40 hours** on this week.

| Block | Hours | Activity |
|---|---|---|
| Day 1 | 4 | Read `01-http-and-rest.md`, draw the request/response diagram |
| Day 1 | 2 | Exercise 01 — first GET against httpbin |
| Day 2 | 4 | Read `02-using-requests.md`, type along with every snippet |
| Day 2 | 3 | Exercises 02–03 (PokeAPI, POST echo) |
| Day 3 | 3 | Read `03-authentication-and-secrets.md`, set up your `.env` |
| Day 3 | 3 | Exercise 04 (GitHub pagination) |
| Day 4 | 3 | Exercise 05 (robust fetcher with retries) |
| Day 4 | 3 | Challenge 01 (currency converter) |
| Day 5 | 3 | Challenge 02 (GitHub user stats) |
| Day 5 | 5 | Mini-project: weather dashboard |
| Day 6 | 2 | Homework problems |
| Day 6 | 1 | Quiz + reflection |

Total: **~36 hours**.

---

## Navigation

- **Lecture notes** — `lecture-notes/01-http-and-rest.md` → `02-using-requests.md` → `03-authentication-and-secrets.md`
- **Exercises** — `exercises/README.md` (five short, focused tasks)
- **Challenges** — `challenges/README.md` (two open-ended write-ups)
- **Quiz** — `quiz.md` (10 multiple-choice questions, self-graded)
- **Homework** — `homework.md` (6 problems, due before Week 9)
- **Mini-project** — `mini-project/README.md` (weather dashboard CLI)
- **Resources** — `resources.md` (official docs and recommended reading)

---

## Stretch goals

If you finish early and want to push further:

1. **`httpx` port** — rewrite Exercise 02 using [`httpx`](https://www.python-httpx.org/). Notice that the API is nearly identical to `requests`, then enable async with `httpx.AsyncClient` and fetch ten Pokémon in parallel.
2. **Caching with `requests-cache`** — install [`requests-cache`](https://requests-cache.readthedocs.io/) and add a 1-hour cache to the weather mini-project so repeated lookups for the same city do not re-hit Open-Meteo.
3. **GraphQL** — read the [GitHub GraphQL API docs](https://docs.github.com/en/graphql) and re-implement Challenge 02 as a single GraphQL query.
4. **Wireshark / Charles** — run a tiny request through a packet inspector and look at the actual TCP bytes. Seeing the raw `GET /get HTTP/1.1\r\n...` is a moment most developers never have.
5. **OpenAPI spec** — read the [OpenAPI 3.1 spec](https://spec.openapis.org/oas/v3.1.0) for any one API you used this week, then generate a typed Python client with [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client).

---

## Up next

Once you finish this week, head to **[Week 9 — Web Development with Flask](../week-09-web-development-flask/)**. There you switch sides: instead of *calling* HTTP APIs you will *build* one. Everything you learned this week about methods, status codes, JSON bodies, and headers applies in reverse.

---

## Submission checklist

Before marking this week complete:

- [ ] Read all three lecture notes
- [ ] Completed exercises 01–05 (working code, runs without error)
- [ ] Attempted both challenges (markdown write-up plus working code)
- [ ] Passed the quiz (8/10 or higher; retake until you do)
- [ ] Submitted homework problems
- [ ] Mini-project runs end-to-end and prints current + 3-day forecast for any city
- [ ] `.env` file is in your `.gitignore` (verify with `git status`)
- [ ] Pushed everything to your fork of the bootcamp repo

Happy crunching!
