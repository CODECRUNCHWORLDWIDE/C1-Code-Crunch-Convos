# Homework Problem 5 — Link Header Parser

> **Topic:** parsing one HTTP header whose punctuation can also appear inside its values
> **Lecture:** [02 — Using `requests`](../lecture-notes/02-using-requests.md) · [Exercise 4 — Walking Every Page](../exercises/exercise-04-pagination.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour 15 minutes
> **Why this one:** Exercise 4 ended with the friendliest pagination scheme — the server hands you the next URL in a `Link` header, and `requests` parses it into `response.links` for you. This problem takes the gift apart. You write that parser yourself, and in doing so you meet the oldest trap in text processing: the separator character that is also allowed inside the things it separates.

## The Brief

GitHub — and many other paginated APIs — put the page navigation in a header
instead of the body:

```text
Link: <https://api.github.com/repositories?page=2>; rel="next",
      <https://api.github.com/repositories?page=15>; rel="last"
```

Read it aloud and the format is friendly: each entry is a URL in angle
brackets, followed by `; name=value` parameters; entries are separated by
commas. The parameter that matters is `rel` — the *relationship*: what this
URL is to you. `next`, `prev`, `first`, `last`, or anything else the server
felt like saying.

You are writing:

```python
def parse_link_header(header: str | None) -> dict[str, str]: ...
```

which turns the header above into:

```python
{
    "next": "https://api.github.com/repositories?page=2",
    "last": "https://api.github.com/repositories?page=15",
}
```

The edge cases are the assignment:

- `None` or an empty string returns `{}` — a response with no `Link` header
  is normal, not an error.
- Whitespace and newlines between entries are legal and common — the example
  above has both.
- A `rel` value may be `"double-quoted"`, `'single-quoted'`, or bare, and a
  quoted one may contain spaces.
- Unknown rels are kept, not dropped. Your parser reports; the caller
  decides.
- And the trap: **a URL may contain commas and semicolons.**
  `https://api.example.com/search?q=a,b` is one URL, not two entries. This is
  why "split on comma" — everyone's first idea, including everyone who has
  written one of these before — is wrong, and why the brackets exist at all.

You may **not** use `requests`' own `response.links` to do the work — the
point is to build what it builds. Using it to *check* your output against a
real response is not only allowed but encouraged; it is the last step.

## Starter

Save this as `hw05_link_header.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it handles the empty cases and fails on
everything real:

```python
"""Parse an HTTP Link header into {rel: url}."""

from __future__ import annotations

import re

# TODO: one entry is <url> followed by any number of ;-parameters.
#       Match the URL as "everything up to the first >", so commas and
#       semicolons inside it cannot end the entry early.
ENTRY_PATTERN = re.compile(r"<([^>]*)>")

# TODO: one parameter is ; name = value, where value may be "quoted",
#       'quoted' or bare.
PARAM_PATTERN = re.compile(r";")


def unquote(value: str) -> str:
    """Strip one matching pair of surrounding quotes, if there is one."""
    value = value.strip()
    # TODO: if value starts and ends with the same quote character,
    #       return what is between them.
    return value


def parse_link_header(header: str | None) -> dict[str, str]:
    """Turn a Link header into a mapping of rel name to URL.

    Args:
        header: The raw header value, or None.

    Returns:
        A mapping of rel to URL. Empty when there is nothing to parse.
    """
    if not header:
        return {}
    links: dict[str, str] = {}
    # TODO: for each <url> and its parameter string, find the rel
    #       parameter, unquote its value, and record links[rel] = url.
    return links


if __name__ == "__main__":
    assert parse_link_header(None) == {}
    assert parse_link_header("") == {}

    header = (
        '<https://api.github.com/repositories?page=2>; rel="next",\n'
        '      <https://api.github.com/repositories?page=15>; rel="last"'
    )
    assert parse_link_header(header) == {
        "next": "https://api.github.com/repositories?page=2",
        "last": "https://api.github.com/repositories?page=15",
    }

    # The trap: one URL containing a comma, still one entry.
    tricky = '<https://api.example.com/search?q=a,b&page=2>; rel="next"'
    assert parse_link_header(tricky) == {
        "next": "https://api.example.com/search?q=a,b&page=2"
    }
    print("all checks passed")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-05-link-header-parser.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `parse_link_header(header: str | None) -> dict[str, str]`, type-hinted.
2. `None` and `""` return `{}`.
3. The two-entry GitHub example parses to exactly the dict in the brief,
   whitespace and newline included.
4. A comma inside a URL does not split the entry; a semicolon inside a URL
   does not end the URL.
5. `rel` values in double quotes, single quotes, and no quotes all work; a
   quoted rel may contain a space.
6. Entries with parameters besides `rel` (like `type="application/json"`)
   still parse; entries with no `rel` at all are skipped; unknown rel names
   are kept.
7. Five or more test cases run under `if __name__ == "__main__":`, including
   the comma-in-URL trap.

## Constraints

- **No `response.links` and no third-party parser.** The library's answer is
  your grading key, not your implementation.

- **Match the URL by the brackets, never by the separators.** The format
  wraps URLs in `< >` precisely *because* URLs can contain the separator
  characters. Any approach that starts with `header.split(",")` fights the
  format instead of using it — the brackets are load-bearing, so lean on
  them.

- **When the same rel appears twice, keep the first.** Any rule would do;
  this one matches what `requests` does, and matching the reference behaviour
  means a malformed header cannot make your program and everybody else's
  follow different pages.

- **Plain `str | None` in, plain `dict` out.** No classes, no clever return
  types. This function will sit inside a pagination loop like Exercise 4's;
  the simpler its contract, the easier that loop stays.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-05-link-header-parser-solution.py
a real Link header, captured from api.github.com:
  next   https://api.github.com/user/583231/repos?per_page=3&page=2
  last   https://api.github.com/user/583231/repos?per_page=3&page=3

ok  nothing at all: 0 link(s)
ok  an empty string: 0 link(s)
ok  the two-entry header from the brief: 2 link(s)
ok  a comma inside the URL: 1 link(s)
ok  a semicolon inside the URL: 1 link(s)
ok  single quotes, no quotes, and a rel with a space in it: 3 link(s)
ok  extra parameters beside rel: 1 link(s)
ok  an entry with no rel at all is skipped: 1 link(s)
ok  a repeated rel keeps the first: 1 link(s)

9 checks passed.
```

The header at the top is a real one — captured from `api.github.com` by
[Exercise 4](../exercises/exercise-04-pagination.md), pasted here as a
constant. Parsing it needs no network, which is the nature of this problem:
the hard part of HTTP is often not the transport, it is the text.

## Steps

1. Copy the starter into `hw05_link_header.py` and run it. The empty cases
   pass; the real ones fail.
2. Get entries out first. Write `ENTRY_PATTERN` to capture the URL between
   `<` and `>` **and** the parameter text after it, and test it with
   `.findall()` in a REPL on the brief's example before writing any more
   code. The shipped pattern is two groups: `<([^>]*)>\s*((?:;[^,<]*)*)`.
3. Read that URL group until it makes sense: `[^>]*` means "anything that is
   not a closing bracket", which is the whole trick — a comma is not a `>`,
   so a comma cannot end the URL.
4. Now parameters. Each one is `; name = value` where value is
   double-quoted, single-quoted, or bare. Three alternatives in one group:
   `"[^"]*"` or `'[^']*'` or `[^;,]*`.
5. Write `unquote` — strip the outer quotes only when they match each other.
   `'"hello'` (one lone quote) stays as it is.
6. Wire it together in `parse_link_header`: for each entry, find the `rel`
   parameter, lowercase the *name* when comparing (header parameter names
   are case-insensitive; values are not), unquote, keep the first of any
   duplicate.
7. Grow the harness to five-plus cases — the brief's list is the menu.
8. Grading key time: make one real call and compare —

   ```python
   import requests
   r = requests.get("https://api.github.com/users/octocat/repos",
                    params={"per_page": 3}, timeout=5)
   r.raise_for_status()
   assert parse_link_header(r.headers.get("Link")) == {
       rel: link["url"] for rel, link in r.links.items()
   }
   ```

## The Solution

```python
"""problem-05-link-header-parser-solution.py — read a paginated API's Link header.

GitHub and many other paginated APIs put the next, previous, first and last
page URLs in a header rather than in the body:

    Link: <https://api.github.com/repositories?page=2>; rel="next",
          <https://api.github.com/repositories?page=15>; rel="last"

This turns that string into ``{"next": "...", "last": "..."}``.

There is no network here. It is string work, and the interesting part is the
punctuation: commas separate entries, and commas also appear inside URLs, so
splitting naively is the bug this problem exists to make you meet.

Run it with::

    python problem-05-link-header-parser-solution.py
"""

from __future__ import annotations

import re

#: One entry: a URL in angle brackets, then any number of ; name=value pairs.
#: The URL group is non-greedy and stops at the first ">", so a comma or a
#: semicolon inside the URL cannot end the entry early.
ENTRY_PATTERN = re.compile(r"<([^>]*)>\s*((?:;[^,<]*)*)")

#: One parameter after a semicolon. The value may be bare, 'single quoted' or
#: "double quoted", and may contain spaces when it is quoted.
PARAM_PATTERN = re.compile(r";\s*([^=;\s]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^;,]*)")


def unquote(value: str) -> str:
    """Strip one matching pair of surrounding quotes, if there is one.

    Args:
        value: A parameter value, possibly quoted.

    Returns:
        The value with its outer quotes removed and its edges trimmed.
    """
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_link_header(header: str | None) -> dict[str, str]:
    """Turn a Link header into a mapping of rel name to URL.

    Every rel is kept, including ones nobody has heard of. When the same rel
    appears twice the first one wins, which matches how requests behaves and
    means a malformed header cannot silently change which page you follow.

    Args:
        header: The raw header value, or None.

    Returns:
        A mapping of rel to URL. Empty when there is nothing to parse.
    """
    if not header:
        return {}
    links: dict[str, str] = {}
    for url, params in ENTRY_PATTERN.findall(header):
        for name, value in PARAM_PATTERN.findall(params):
            if name.strip().lower() != "rel":
                continue
            rel = unquote(value)
            if rel and rel not in links:
                links[rel] = url.strip()
    return links


def check() -> int:
    """Run every example and report.

    Returns:
        The number of checks that ran.
    """
    cases: tuple[tuple[str, str | None, dict[str, str]], ...] = (
        ("nothing at all", None, {}),
        ("an empty string", "", {}),
        (
            "the two-entry header from the brief",
            '<https://api.github.com/repositories?page=2>; rel="next",\n'
            '      <https://api.github.com/repositories?page=15>; rel="last"',
            {
                "next": "https://api.github.com/repositories?page=2",
                "last": "https://api.github.com/repositories?page=15",
            },
        ),
        (
            "a comma inside the URL",
            '<https://api.example.com/search?q=a,b&page=2>; rel="next"',
            {"next": "https://api.example.com/search?q=a,b&page=2"},
        ),
        (
            "a semicolon inside the URL",
            "<https://api.example.com/x?filter=a;b>; rel=next",
            {"next": "https://api.example.com/x?filter=a;b"},
        ),
        (
            "single quotes, no quotes, and a rel with a space in it",
            "<https://a.example/1>; rel='first', "
            "<https://a.example/2>; rel=prev, "
            '<https://a.example/3>; rel="my odd rel"',
            {
                "first": "https://a.example/1",
                "prev": "https://a.example/2",
                "my odd rel": "https://a.example/3",
            },
        ),
        (
            "extra parameters beside rel",
            '<https://a.example/9>; rel="next"; type="application/json"; title="Page 9"',
            {"next": "https://a.example/9"},
        ),
        (
            "an entry with no rel at all is skipped",
            "<https://a.example/nope>; title=\"orphan\", "
            '<https://a.example/yes>; rel="next"',
            {"next": "https://a.example/yes"},
        ),
        (
            "a repeated rel keeps the first",
            '<https://a.example/1>; rel="next", <https://a.example/2>; rel="next"',
            {"next": "https://a.example/1"},
        ),
    )
    for label, header, expected in cases:
        actual = parse_link_header(header)
        assert actual == expected, f"{label}: expected {expected}, got {actual}"
        print(f"ok  {label}: {len(actual)} link(s)")
    return len(cases)


if __name__ == "__main__":
    real = (
        '<https://api.github.com/user/583231/repos?per_page=3&page=2>; rel="next", '
        '<https://api.github.com/user/583231/repos?per_page=3&page=3>; rel="last"'
    )
    print("a real Link header, captured from api.github.com:")
    for rel, url in parse_link_header(real).items():
        print(f"  {rel:<6} {url}")
    print()
    total = check()
    print()
    print(f"{total} checks passed.")
```

**The entry pattern leans on the brackets, because the brackets are the
format's whole reason.** `<([^>]*)>` reads: an opening bracket, then *any
run of characters that are not a closing bracket*, then the closing bracket.
A comma inside the URL is not a `>`, so it is swallowed into the URL group
like any other character — requirement 4 falls straight out of the character
class, no special case needed. The second group, `((?:;[^,<]*)*)`, collects
the parameter tail: any number of runs that each start with `;` and stop
before a comma (the next entry's separator) or a `<` (the next entry
itself). The `(?:...)` is a **non-capturing group** — it groups for the `*`
to repeat without adding a capture that `findall` would have to return.

**The parameter pattern handles three spellings of one idea in one
alternation.** `(\"[^\"]*\"|'[^']*'|[^;,]*)` — a double-quoted run, or a
single-quoted run, or a bare run that stops at parameter or entry
punctuation. Order matters inside an alternation: the regex engine tries
alternatives left to right, so the quoted forms must come before the bare
form — the bare form would happily match `"my` and stop at the space.
Spaces inside quotes survive because the quoted alternatives are defined by
their quotes, not by whitespace.

**`unquote` refuses to guess.** It strips quotes only when the first and
last characters are the *same* quote character. `"next"` and `'next'` lose
their quotes; `next` is untouched; a mangled `"next` keeps its lone quote
and becomes visible garbage rather than invisible garbage — a small honesty
that pays off the day a proxy mangles a header.

**Names compare case-insensitively; values do not.** `Rel="next"` is legal
header grammar, so the *name* is lowercased before comparing. But the value
is left alone: rel names are effectively lowercase in the wild, and
rewriting values you do not understand is how parsers corrupt data that was
fine.

**First-wins duplicate handling is borrowed deliberately.**
`if rel and rel not in links` — an already-seen rel is ignored. Not because
first is "right" (the RFC does not say), but because it is what `requests`
does, and two parsers in one program disagreeing about which page is "next"
is a debugging story nobody wants. When a reference implementation exists,
matching its tie-breaks is a feature.

**`findall` twice, loop, done.** No index arithmetic, no state machine, no
splitting. The two patterns each describe one *thing* (an entry, a
parameter), and the code reads as: for every entry, for every parameter,
keep the rels. When a format is regular enough for regular expressions,
letting the pattern do the walking keeps the Python nearly free of logic.

## Download and run

Download
[problem-05-link-header-parser-solution.py](./problem-05-link-header-parser-solution.py)
and run it:

```bash
python problem-05-link-header-parser-solution.py
```

It needs nothing installed and never touches the network — the one real
header in it was captured from `api.github.com` and pasted in as a constant.
The `-solution` in the filename keeps it from colliding with your own
`hw05_link_header.py`.

## Common bugs to catch

- **`header.split(",")` as the first move.** The comma-in-URL case shatters:

  ```text
  AssertionError: a comma inside the URL: expected
  {'next': 'https://api.example.com/search?q=a,b&page=2'}, got
  {'next': 'https://api.example.com/search?q=a'}
  ```

  Half a URL is worse than no URL — it may still *fetch* something, and then
  you are debugging a 404 (or someone else's page) three functions away from
  the split that caused it. Parse by the brackets.

- **A greedy URL group.** `<(.*)>` with two entries on one line matches from
  the first `<` to the *last* `>` — one giant "URL" containing both entries,
  because `*` is greedy and `.` will happily match `>` on its way there.
  `[^>]*` cannot overrun the first close bracket; that is what character
  classes are for. (`(.*?)` also works; the class says the intent better.)

- **Forgetting `re.escape` habits and testing only pretty input.** The
  brief's example has a newline and leading spaces before the second entry.
  If your parameter pattern anchors on `; ` with a literal space, `;rel=next`
  (no space — legal) silently yields nothing and the entry is "skipped".
  `;\s*` is the spelling that means what the grammar means.

- **Splitting parameters with `params.split(";")` then `split("=")`.**
  Works until a quoted value contains either character —
  `title="a;b=c"` is one parameter. If you go the splitting route rather
  than the pattern route, every quoted value is a landmine; the pattern
  route defuses them by defining values quote-first.

- **Dropping unknown rels.** Filtering to
  `("next", "prev", "first", "last")` passes the brief's example and fails
  requirement 6 — and real APIs do send others (`hub`, `alternate`,
  `canonical`). Your parser reports; the *caller* filters. Tools that
  discard what they do not recognise lose exactly the data you need on the
  weird day.

- **Testing with `in` instead of `==`.** `assert "next" in links` passes
  even when the URL attached to it is half a URL. Assert whole dicts —
  every failure message above came from an equality assert that could name
  the difference.

## Under the hood

<details>
<summary>Under the hood — RFC 8288, and what the full grammar allows that this parser skips</summary>

The `Link` header is specified in **RFC 8288, "Web Linking"** — it defines
the syntax and keeps a public registry of rel names (`next`, `prev`,
`canonical`, `alternate`, and a couple hundred more). GitHub's usage is the
registry's `next`/`prev`/`first`/`last` quartet, unchanged.

A few things the full grammar allows that this page's parser deliberately
does not chase:

- **`rel` can hold several names in one value**: `rel="next prefetch"`
  means the link is both. A full parser splits the value on spaces and
  registers the URL under each name. Ours would store it under the literal
  key `"next prefetch"` — visible, harmless for the APIs this week uses,
  and easy to add if you meet it. (This is also why "a rel with a space in
  it" appears in the tests: the behaviour is pinned down, not accidental.)
- **Parameters can be `*`-suffixed** (`title*=UTF-8''caf%C3%A9`) — an
  encoding scheme (RFC 8187) for non-ASCII text in headers. Rarely seen on
  `Link`, fiddly to decode, ignored here.
- **A URI-Reference may be relative** — `</page/2>; rel="next"` is legal,
  and resolving it needs the request's own URL as a base
  (`urllib.parse.urljoin`). GitHub always sends absolute URLs; not all APIs
  do. This is the first extension worth adding in real code.

Where the reference implementations sit, so you can read them: `requests`
parses `Link` in `requests.utils.parse_header_links` — about thirty lines,
split-based, with a `replace_chars = " '\""` strip loop — and exposes the
result as `response.links`. Its split-based approach handles the common
cases and quietly mis-parses a comma inside a URL... in the *rare* place
GitHub never produces one. The regex approach on this page trades a little
pattern-reading for correctness on that case. Both are defensible
engineering; knowing *which* corner each cuts is the skill.

And one habit worth keeping from this problem: when a format gives you
delimiters that can appear inside values, the format almost always also
gives you a **quoting or bracketing mechanism** — and the parser should be
built on the brackets, never on the delimiters. CSV solved the same problem
with double quotes (Week 6, where `csv.reader` saved you from writing
this); `Link` solved it with `< >`. Same disease, same cure.

</details>

<details>
<summary>Under the hood — reading the two patterns one atom at a time</summary>

Regular expressions reward being read slowly, once, atom by atom. The entry
pattern:

```text
<([^>]*)>\s*((?:;[^,<]*)*)
```

| Atom | Meaning |
|---|---|
| `<` | a literal opening angle bracket |
| `([^>]*)` | group 1: zero or more of anything except `>` — the URL |
| `>` | the literal close |
| `\s*` | optional whitespace (GitHub puts a space here) |
| `(?: ... )` | a group that repeats but does not capture |
| `;[^,<]*` | a `;`, then anything up to the next entry's `,` or `<` |
| `( ... )*` | group 2: all the parameter runs, concatenated |

`findall` with two groups returns `(url, params)` tuples — which is why
`parse_link_header` can unpack them directly in its `for`.

The parameter pattern:

```text
;\s*([^=;\s]+)\s*=\s*("[^"]*"|'[^']*'|[^;,]*)
```

| Atom | Meaning |
|---|---|
| `;\s*` | each parameter starts at a semicolon |
| `([^=;\s]+)` | group 1: the name — no `=`, `;` or spaces in names |
| `\s*=\s*` | the equals sign, whitespace forgiven on both sides |
| `"[^"]*"` | a double-quoted value (may contain `;`, `,`, spaces) |
| `'[^']*'` | or a single-quoted one |
| `[^;,]*` | or a bare one, stopping before parameter/entry punctuation |

Two ideas carry both patterns. **Negated character classes** (`[^>]`,
`[^;,]`) are how you say "up to the next structural character" without
letting the engine run past it — they are the disciplined cousin of `.*`,
which respects nothing. And **alternation order** matters because the
engine is eager: it commits to the first alternative that can match at the
current position, so specific, delimited forms (the quoted values) must be
listed before the loose catch-all (the bare value).

What these patterns do *not* need is also worth noticing: no lookahead, no
backreferences, no flags. The format was designed to be parseable by
exactly this much machinery. When you find yourself reaching for the
exotic corners of `re`, it is usually the format telling you it wants a
real parser instead — JSON, for instance, cannot be parsed with regular
expressions at all, because nesting is not a regular language. Week 8 hands
that job to `.json()`; the `Link` header is flat, and flat is what regexes
are for.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] `None` and `""` return `{}`.
- [ ] The brief's two-entry example — newline, spaces and all — parses to
      exactly its dict.
- [ ] A URL containing a comma survives whole; so does one containing a
      semicolon.
- [ ] Double-quoted, single-quoted and bare rels all parse; a quoted rel
      with a space parses.
- [ ] An entry with no `rel` is skipped; unknown rels are kept; a repeated
      rel keeps the first.
- [ ] Five or more asserts on exact dict equality.
- [ ] Checked once against `response.links` on a real GitHub response
      (Steps, item 8).
- [ ] Committed with a message like `Add Week 8 homework 5: Link parser`.

## Stretch

- Handle relative URLs: give `parse_link_header` an optional
  `base: str | None = None` and resolve each URL with
  `urllib.parse.urljoin(base, url)` when a base is supplied. One test:
  `</page/2>; rel="next"` against `base="https://api.example.com/page/1"`.

- Split multi-name rels: make `rel="next prefetch"` register the URL under
  both keys, per RFC 8288, and keep the first-wins rule working per key.

- Rebuild Exercise 4's GitHub walk using *your* parser instead of
  `response.links` — the loop condition becomes
  `while "next" in parse_link_header(r.headers.get("Link"))`. If the two
  parsers ever walk a different set of pages, one of you has a bug worth
  finding.

- Read `requests.utils.parse_header_links` (it is short) and write one
  sentence on where its behaviour and yours differ, and which input would
  expose it.

Once your parser survives every quoting style, move on to
[Homework Problem 6 — Tiny URL-Shortener Client](./problem-06-tiny-url-shortener-client.md).
