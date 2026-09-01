# Week 8 — Homework

Six problems, one page each. Week 8 is about talking to the network, and the
homework is where the habits from the exercises become muscle: read a status
code before you trust a body, give every request a timeout, and never build a
URL by gluing strings together.

Each shipped answer runs **offline**. The real HTTP call sits behind a seam — a
small function you can swap — and the download feeds it a recorded response, so
the program runs the same on a plane as on a fast connection and its output
never drifts with someone else's live data. Each page shows the one-line change
that points it back at the real API.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what goes out on the wire
   and what you expect to come back.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [HTTP method matcher](./problem-01-http-method-matcher.md) | What each verb means and when a server should refuse one | Beginner | 45 min |
| 2 | [JSON path walker](./problem-02-json-path-walker.md) | Reaching into deeply nested JSON without crashing on a missing key | Intermediate | 1 hr |
| 3 | [Rate-limit decorator](./problem-03-rate-limit-decorator.md) | Slowing your own calls so a server does not have to refuse them | Advanced | 1 hr 15 min |
| 4 | [Mock API client](./problem-04-mock-api-client.md) | Testing network code without a network — the seam, on purpose | Intermediate | 1 hr |
| 5 | [Link header parser](./problem-05-link-header-parser.md) | Following pagination the way real APIs describe it | Intermediate | 1 hr 15 min |
| 6 | [Tiny URL-shortener client](./problem-06-tiny-url-shortener-client.md) | A small end-to-end client: send, read back, handle the error | Advanced | 1 hr |

Total target time: about 6 hours. The [week schedule](../README.md) leaves more
room than that, and both numbers are honest — the figures here are how long each
problem takes when it goes well, and the schedule allows for getting stuck and
reading back over the exercises.

## What you hand in

Six scripts of your own, one per problem, named as each page tells you — not the
`-solution.py` names, which belong to the published answers. Keep them together
in a folder called `homework/` inside your fork:

```text
homework/
    hw01_method_matcher.py
    hw02_json_walker.py
    hw03_rate_limit.py
    hw04_mock_client.py
    hw05_link_header.py
    hw06_url_shortener.py
```

Each one must run as `python <name>.py`, carry a module docstring with an
example invocation, and put type hints on every signature. Use narrow `except`
clauses and a custom exception where something can fail — never a bare
`except:`. If your cohort uses pull requests, open one; commit with
`feat(week-08): homework problems`.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference is the bug — read it rather than guessing.
