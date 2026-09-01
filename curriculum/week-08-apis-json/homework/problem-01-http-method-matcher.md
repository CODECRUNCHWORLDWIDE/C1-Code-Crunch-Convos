# Homework Problem 1 — HTTP Method Matcher

> **Topic:** picking the right HTTP verb from what a sentence means
> **Lecture:** [01 — HTTP and REST](../lecture-notes/01-http-and-rest.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** the five HTTP methods are the week's vocabulary, and vocabulary does not stick from reading a table. It sticks from making a hundred small decisions with it. This problem makes you encode the whole table as code, which means you cannot finish it while any row of it is still fuzzy.

## The Brief

An HTTP method is the **tone of voice** a request uses. The words after it say
*what* you are talking about; the method says what kind of sentence it is.
`GET` is a question. `POST` hands over something new. `PUT` says "replace what
is at this address with this". `PATCH` says "change these fields, leave the
rest". `DELETE` says what it says.

People do not think in verbs, though. They think in intents: "add a new user",
"remove the old branch", "read the catalog". You are writing the translator —
a function that takes one of those sentences and answers with the method that
expresses it.

The mapping, in priority order:

| Intent (lowercased) contains | Method |
|---|---|
| `"create"` or `"add"` or `"submit"` | `POST` |
| `"replace"` or `"overwrite"` | `PUT` |
| `"update"` or `"modify"` or `"edit"` | `PATCH` |
| `"remove"` or `"delete"` | `DELETE` |
| `"fetch"` or `"read"` or `"get"` or `"list"` | `GET` |
| anything else | `GET` (the default) |

**Order matters.** If a sentence contains both `"add"` and `"update"`, the
first row that matches wins, so "add or update the row" is `POST`. That makes
the order of the rules part of the specification, not a detail — and how you
store the rules has to protect that order.

There is no network in this problem at all. That is the point: most of what
people call "API code" is ordinary Python making careful decisions, and this
is the first of five problems this week that prove it.

## Starter

Save this as `hw01_method_matcher.py` in your `homework/` folder and fill in
the `TODO`s. It runs as pasted — every intent comes back `GET` until you write
the rules:

```python
"""Pick the HTTP method that expresses an intent sentence."""

from __future__ import annotations

DEFAULT_METHOD = "GET"

# TODO: the rules from the brief, in priority order. A tuple of
# (method, words-that-select-it) pairs, so the order cannot be lost.
RULES: tuple[tuple[str, tuple[str, ...]], ...] = ()


def recommend_method(intent: str) -> str:
    """Return the HTTP method that best expresses *intent*.

    Args:
        intent: A sentence describing what the caller wants to do.

    Returns:
        One of POST, PUT, PATCH, DELETE or GET.
    """
    # TODO: lowercase the intent once.
    # TODO: walk RULES in order; return the first method whose words match.
    # TODO: return DEFAULT_METHOD when nothing matched.
    return DEFAULT_METHOD


if __name__ == "__main__":
    assert recommend_method("add a new user") == "POST"
    assert recommend_method("delete order 42") == "DELETE"
    assert recommend_method("read the catalog") == "GET"
    assert recommend_method("modify the title") == "PATCH"
    assert recommend_method("") == "GET"
    # Order matters: "add" outranks "update".
    assert recommend_method("add or update the row") == "POST"
    print("all checks passed")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-01-http-method-matcher.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `recommend_method(intent: str) -> str` implements the table exactly, with
   type hints.
2. Matching ignores case: `"DELETE EVERYTHING"` is `DELETE`.
3. Order matters: when two rows both match, the earlier row wins, and at least
   one of your tests proves it.
4. Anything that matches no row returns `"GET"`, including the empty string.
5. At least six `assert` tests run inside `if __name__ == "__main__":` — one
   per method, one for the empty string, one for the priority rule.
6. A docstring explains why `"submit"` maps to `POST` and not `PUT`, in your
   own words. (The answer is about what happens when the same request is sent
   twice — the lecture calls it **idempotency**.)

## Constraints

- **No network, no imports beyond the standard library.** The problem is the
  meaning of five words. Adding `requests` to it would be dressing up a
  dictionary lookup as an API call.

- **The rules live in one data structure, in priority order — not in a chain
  of `if`s.** A chain of `if`s hides the table inside control flow, where you
  cannot read it at a glance, test it row by row, or add a row without
  touching logic. Data you can see is data you can check against the brief.

- **Not a plain `dict` keyed by word.** A dict maps one word to one method,
  which loses the grouping ("create", "add", "submit" are one rule, not
  three) — and nothing about a dict *says* its order is load-bearing, so a
  future editor can reorder it and change behaviour without a single test
  telling them. A tuple of tuples cannot be "harmlessly" reordered.

- **Lowercase the intent once, at the top.** Lowercasing inside the loop does
  the same work per row for no reason, and lowercasing the rule words at
  runtime hides the fact that the table is already lowercase by design.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-http-method-matcher-solution.py
POST    <- 'add a new user'
POST    <- 'create an invoice'
POST    <- 'submit the form'
PUT     <- 'replace the avatar'
PUT     <- 'overwrite the config file'
PATCH   <- 'modify the title'
PATCH   <- 'edit my profile'
DELETE  <- 'delete order 42'
DELETE  <- 'remove the old branch'
GET     <- 'read the catalog'
GET     <- 'list every repository'
GET     <- ''
GET     <- 'stare wistfully at the ocean'
POST    <- 'add or update the row'
DELETE  <- 'DELETE EVERYTHING'

15 checks passed.
```

Your own `hw01_method_matcher.py` prints whatever your test harness prints —
the line format is yours. What must agree is every left-hand answer.

## Steps

1. Copy the starter into `hw01_method_matcher.py` and run it. It fails on the
   first assert, because everything is `GET` so far.
2. Write `RULES` straight from the table in the brief, top row first.
3. Make `recommend_method` walk the rules: lowercase once, then for each
   `(method, words)` pair, return `method` if any of its words appears in the
   sentence.
4. Run it after each change. The asserts are your progress bar.
5. Add your own tests until you have six or more, including one that proves
   the priority rule and one with capital letters.
6. Write the `"submit"` docstring last, after the code works — explaining a
   decision is easier once you have made it.

## The Solution

```python
"""problem-01-http-method-matcher-solution.py — pick the HTTP verb for an intent.

Turns a sentence describing what somebody wants to do -- "add a new user",
"delete order 42" -- into the HTTP method that expresses it.

There is no network here at all. This problem is about the meaning of the five
verbs, and the meaning is what you have to have straight before any of the rest
of the week is safe.

Run it with::

    python problem-01-http-method-matcher-solution.py
"""

from __future__ import annotations

DEFAULT_METHOD = "GET"

#: The rules, in priority order. The first rule whose words appear in the
#: intent wins, so the order of this list is part of the specification and not
#: a detail. A tuple of tuples rather than a dict, because a dict would invite
#: somebody to reorder it harmlessly, and reordering it is not harmless.
RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("POST", ("create", "add", "submit")),
    ("PUT", ("replace", "overwrite")),
    ("PATCH", ("update", "modify", "edit")),
    ("DELETE", ("remove", "delete")),
    ("GET", ("fetch", "read", "get", "list")),
)


def recommend_method(intent: str) -> str:
    """Return the HTTP method that best expresses *intent*.

    "submit" is POST rather than PUT because a submission asks the server to
    create something new and to choose where it goes. PUT means "put this
    exact thing at this exact address, replacing whatever was there" -- the
    caller names the address, and sending it twice leaves the same result. A
    submission sent twice makes two records, which is precisely the difference.

    Args:
        intent: A sentence describing what the caller wants to do. Case does
            not matter.

    Returns:
        One of POST, PUT, PATCH, DELETE or GET. Anything unrecognised gets
        GET, because reading is the one verb that cannot damage anything.
    """
    lowered = intent.lower()
    for method, words in RULES:
        if any(word in lowered for word in words):
            return method
    return DEFAULT_METHOD


def check() -> int:
    """Run every example and report.

    Returns:
        The number of checks that ran.
    """
    cases: tuple[tuple[str, str], ...] = (
        ("add a new user", "POST"),
        ("create an invoice", "POST"),
        ("submit the form", "POST"),
        ("replace the avatar", "PUT"),
        ("overwrite the config file", "PUT"),
        ("modify the title", "PATCH"),
        ("edit my profile", "PATCH"),
        ("delete order 42", "DELETE"),
        ("remove the old branch", "DELETE"),
        ("read the catalog", "GET"),
        ("list every repository", "GET"),
        ("", "GET"),
        ("stare wistfully at the ocean", "GET"),
        # "add" comes before "update" in RULES, so POST wins. Order matters.
        ("add or update the row", "POST"),
        # Capitals do not matter; the intent is lowercased first.
        ("DELETE EVERYTHING", "DELETE"),
    )
    for intent, expected in cases:
        actual = recommend_method(intent)
        assert actual == expected, f"{intent!r}: expected {expected}, got {actual}"
        print(f"{actual:<7} <- {intent!r}")
    return len(cases)


if __name__ == "__main__":
    total = check()
    print()
    print(f"{total} checks passed.")
```

**The table is data, and the function is four lines.** Everything the brief
specifies lives in `RULES`, where you can read it row by row against the
table and see that they match. `recommend_method` only knows the *shape* of a
rule — a method and some words — not any particular rule. Add a row for
`HEAD` tomorrow and the function does not change.

**A tuple of tuples, and the comment says why.** Python dicts do keep their
insertion order, so a dict would *work* today. The problem is what it says to
the next person: nothing about a dict warns that its order is load-bearing,
and "alphabetise this for tidiness" is a one-line edit that would silently
turn "add or update the row" from `POST` into `PATCH`. A tuple of pairs makes
the order look deliberate, because it is. When an ordering is part of your
specification, pick the container that shows it.

**`any(word in lowered for word in words)` is the whole matcher.** `in` on
strings is a substring test, `any` stops at the first hit, and the generator
inside means no list is ever built. Read it aloud and it is the rule itself:
"any of these words in the sentence".

**The docstring answers the brief's bonus question.** Send `PUT /users/42`
twice and the second one changes nothing — the same thing is at the same
address. That property is called **idempotent**: doing it twice is the same
as doing it once. Send a submission twice and you have two records. So
"submit" is `POST`, the one verb that is *expected* to create something new
every time it is used. The full safe/idempotent table is in Under the hood.

**The default is `GET` because reading cannot damage anything.** When the
translator is not sure, it must pick the verb whose worst case is a wasted
read — never one that writes or deletes on a guess.

**`check()` prints every case as it passes.** Fifteen silent asserts tell you
nothing until one fails. Fifteen printed lines are a table you can read back
against the brief — the output *is* the specification, demonstrated.

## Download and run

Download
[problem-01-http-method-matcher-solution.py](./problem-01-http-method-matcher-solution.py)
and run it:

```bash
python problem-01-http-method-matcher-solution.py
```

It needs nothing installed and never touches the network. The `-solution` in
the filename keeps it from colliding with your own `hw01_method_matcher.py`.

## Common bugs to catch

- **A chain of `elif`s with the priority upside down.** Written as
  `if "update" in ... elif "add" in ...`, the sentence "add or update the
  row" comes back `PATCH`. No exception, no warning — just the wrong verb,
  which for a real API is the difference between editing a record and
  creating a duplicate. This is why requirement 3 demands a test for it.

- **Forgetting `.lower()`.** `"DELETE EVERYTHING"` matches no lowercase word
  and falls through to `GET`. The failure is quiet and the default hides it —
  which is the general price of having a default at all.

- **`intent.lower()` computed but not kept.**

  ```python
  intent.lower()
  for method, words in RULES:
      if any(word in intent for word in words):
  ```

  Strings are immutable; `.lower()` returns a new string and changes nothing
  in place. Calling it without assigning the result does nothing at all.
  `lowered = intent.lower()` is the line you wanted.

- **Testing `word == intent` instead of `word in intent`.** Every sentence
  longer than one word matches nothing and everything becomes `GET`. The
  brief says *contains*.

- **`assert recommend_method("add") == "POST", "..."` written with the
  parentheses wrong.** `assert (condition, "message")` — with one pair of
  parentheses around both — asserts a two-element tuple, which is always
  truthy, so the test can never fail. Python 3.13 warns about this
  (`SyntaxWarning: assertion is always true`); read your warnings.

- **Substring matches you did not order.** `"read"` hides inside
  `"readd the file"` — and so does `"add"`. Both rules match, so the
  priority order decides: `POST`, because the POST row comes first. If that
  bothers you, it should — see the Stretch for the word-boundary fix. What
  matters here is that the behaviour is *defined*, by the order, rather than
  accidental.

## Under the hood

<details>
<summary>Under the hood — safe, idempotent, and why the table is what it is</summary>

The five methods differ on two promises, and the whole table falls out of
them.

**Safe** means the request changes nothing on the server. It is a read.

**Idempotent** means sending the request twice leaves the server in the same
state as sending it once. Deleting the same record twice: the second call
finds nothing to delete, state unchanged. Replacing a record with the same
content twice: same. Creating a record twice: **two records** — not
idempotent.

| Method | Safe | Idempotent | Sentence |
|---|---|---|---|
| `GET` | yes | yes | "show me" |
| `PUT` | no | yes | "put exactly this at exactly this address" |
| `DELETE` | no | yes | "make this address empty" |
| `PATCH` | no | not promised | "change these fields" |
| `POST` | no | **no** | "here is something new; you pick the address" |

Why anyone cares: **retries.** Networks fail after a request is sent but
before the answer arrives, and the only cure is sending it again. A retry of
an idempotent request is always harmless. A retry of a `POST` might charge a
card twice — which is why Exercise 5's retry policy listed only `GET` and
`HEAD` in `allowed_methods`, and why real payment APIs make you send an
"idempotency key" so their server can spot the duplicate for you.

That is also the honest answer to the docstring question. "Submit" implies
the server assigns the identity of the new thing — a new order number, a new
user id. The caller cannot name the address, so it cannot be `PUT`, whose
meaning *is* the address.

And one more corner worth knowing: idempotent does not mean the *response*
repeats. The first `DELETE` may answer `204 No Content` and the second
`404 Not Found` — the server state is identical after each, which is all
idempotency promises.

</details>

<details>
<summary>Under the hood — substring matching versus word boundaries</summary>

`"get" in "forget the milk"` is `True`. The matcher in this problem is a
substring matcher, and substrings do not respect word edges — `"forget"`
contains `get`, `"caddy"` contains `add`, `"breading"` contains `read`.

For this brief that is fine, because the brief says *contains* and the
priority order makes every outcome defined. For a real intent classifier it
would not be fine, and the fix is one regular expression feature: `\b`, the
**word boundary**. It matches the empty position between a word character and
a non-word character — no text, just a place.

```python
import re

def matches(word: str, sentence: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", sentence) is not None
```

`matches("get", "forget the milk")` is `False`, because the position before
`get` inside `forget` has letters on both sides — no boundary.
`re.escape` matters even here: the day a rule word contains a `.` or a `+`,
an unescaped pattern stops meaning what it says.

The deeper lesson is about failure modes. The substring matcher never
crashes; it just occasionally gives a defensible-but-surprising answer. Bugs
that produce *plausible wrong answers* are the expensive kind — nothing in
your logs will ever point at them. When you choose a cheap approximation, do
what this page does: write down where its edges are, and put the case that
proves the edge in your tests.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback and prints its checks.
- [ ] All five methods appear in your tests, plus the empty string.
- [ ] `"add or update the row"` returns `POST`, and a test proves it.
- [ ] `"DELETE EVERYTHING"` returns `DELETE`, and a test proves it.
- [ ] The rules are one visible data structure, in the brief's order.
- [ ] The docstring explains "submit is POST" using the idea of sending the
      same request twice.
- [ ] Type hints on `recommend_method`, and on `RULES`.
- [ ] Committed with a message like `Add Week 8 homework 1: method matcher`.

## Stretch

- Add word-boundary matching from Under the hood, and a test where the
  substring matcher and the boundary matcher disagree — `"forget the milk"`
  is a good start.

- Add a second function `expected_status(method: str) -> tuple[int, ...]`
  returning the status codes each verb usually succeeds with — `POST` earns
  `(200, 201)`, `DELETE` earns `(200, 204)`. Exercise 1's Under the hood has
  the table.

- Return a **confidence** alongside the method: `("POST", "matched 'add'")`.
  When the default fires, say so: `("GET", "no rule matched")`. Programs that
  explain their answers are easier to trust and far easier to debug.

Once your matcher answers cleanly, move on to
[Homework Problem 2 — JSON Path Walker](./problem-02-json-path-walker.md).
