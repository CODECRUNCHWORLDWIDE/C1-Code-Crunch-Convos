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
