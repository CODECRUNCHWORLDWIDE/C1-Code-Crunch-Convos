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
