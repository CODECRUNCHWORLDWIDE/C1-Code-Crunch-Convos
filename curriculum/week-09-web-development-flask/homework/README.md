# Week 9 — Homework

Six problems, one page each. They are not six unrelated exercises. Each one is a
piece of the blog you build in the [mini-project](../mini-project/README.md),
and problems 2, 4, 5, and 6 stack directly on top of one another — a base
template to inherit from, then tags, then search, then a login that guards the
page where posts are written. Work them in order and the blog assembles itself.

Each shipped answer runs **offline and unattended**. A Flask app normally waits
for a browser; these do not. Every answer drives its own routes with Flask's
test client and prints what came back, so `python <name>.py` finishes on its own
and prints the same thing on any machine. The weather problem goes further and
puts the network call behind a small function you can swap, so the page's output
never drifts with somebody else's live forecast. Each page shows the one-line
change that points it back at a real browser or a real API.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the route receives and
   what it should send back.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Custom 404 page](./problem-01-custom-404-page.md) | Turning a framework's default error into a page of your own | Beginner | 45 min |
| 2 | [Base template](./problem-02-base-template.md) | Writing the header and footer once, so a new page is one small file | Beginner | 45 min |
| 3 | [Weather route](./problem-03-weather-route.md) | Wrapping last week's network code in a route that never shows a traceback | Intermediate | 1 hr 15 min |
| 4 | [Post tags](./problem-04-post-tags.md) | Cleaning typed input once, at the boundary, instead of everywhere after | Intermediate | 1 hr 15 min |
| 5 | [Search filter](./problem-05-search-filter.md) | A GET form that filters a list and hands the query back to the user | Intermediate | 1 hr |
| 6 | [Session auth (demo only)](./problem-06-session-auth-demo.md) | How a session remembers who you are — and why this is not real security | Advanced | 1 hr 15 min |

Total target time: about 6 hours. The [week schedule](../README.md) leaves more
room than that, and both numbers are honest — the figures here are how long a
problem takes when it goes well, and the schedule allows for getting stuck and
reading back over the lecture notes.

**Problem 6 carries a security warning, and it is not decoration.** That problem
shows how Flask sessions work. It is not how to build a login. The password sits
in the source, there is no hashing, and nothing defends against someone guessing
in a loop. Read the warning on the page before you copy any of it anywhere.

## What you hand in

Six scripts of your own, one per problem, named as each page tells you — not the
`-solution.py` names, which belong to the published answers. Keep them together
in a folder called `homework/` inside your fork:

```text
homework/
    problem-01-custom-404-page.py
    problem-02-base-template.py
    problem-03-weather-route.py
    problem-04-post-tags.py
    problem-05-search-filter.py
    problem-06-session-auth-demo.py
```

Each one must run as `python <name>.py`, carry a module docstring with an
example invocation, and put type hints on every signature. Use narrow `except`
clauses and a custom exception where something can fail — never a bare
`except:`. Read your API key from `os.environ`; never type a key into a file you
commit. If your cohort uses pull requests, open one; commit with
`feat(week-09): homework problems`.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference is the bug — read it rather than guessing.
