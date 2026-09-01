"""exercise-05-comprehensions-solution.py — six loops, six one-liners.

The six `_loop` functions are the starter's, unedited. They already work, and
they are the tests: each of the six comprehensions below has to produce the
identical result.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
TITLES: list[str] = [
    "Intro to Loops", "Debugging Clinic", "List Comprehensions",
    "Git Basics", "Dict Patterns",
]

MINUTES: list[int] = [90, 60, 120, 45, 75]

SCORES: dict[str, int] = {
    "ada": 88, "grace": 54, "linus": 71, "margaret": 59, "guido": 95,
}

ROSTERS: list[list[str]] = [["ada", "grace"], ["linus"], ["margaret", "guido", "ada"]]


# ---- Reference loops (do not edit) ----
def slugs_loop(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens, the long way."""
    out = []
    for title in titles:
        out.append(title.lower().replace(" ", "-"))
    return out


def long_sessions_loop(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes, the long way."""
    out = []
    for title, mins in zip(titles, minutes):
        if mins > 60:
            out.append(title)
    return out


def labels_loop(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise, the long way."""
    out = []
    for score in scores.values():
        if score >= 60:
            out.append("pass")
        else:
            out.append("retry")
    return out


def title_to_minutes_loop(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes, the long way."""
    out = {}
    for title, mins in zip(titles, minutes):
        out[title] = mins
    return out


def initials_loop(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, the long way."""
    out = set()
    for name in names:
        out.add(name[0].upper())
    return out


def flatten_loop(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, the long way."""
    out = []
    for roster in rosters:
        for name in roster:
            out.append(name)
    return out


# ---- Your task: one comprehension per function ----
def slugs(titles: list[str]) -> list[str]:
    """Lowercase each title and replace spaces with hyphens.

    Args:
        titles: The session titles.

    Returns:
        One slug per title, in the same order.
    """
    return [title.lower().replace(" ", "-") for title in titles]


def long_sessions(titles: list[str], minutes: list[int]) -> list[str]:
    """Return the titles of sessions longer than 60 minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        The titles that run over an hour.
    """
    return [title for title, mins in zip(titles, minutes) if mins > 60]


def labels(scores: dict[str, int]) -> list[str]:
    """Return "pass" for scores of 60 or more, "retry" otherwise.

    Args:
        scores: A name-to-score mapping.

    Returns:
        One label per score, in the dict's own order.
    """
    return ["pass" if score >= 60 else "retry" for score in scores.values()]


def title_to_minutes(titles: list[str], minutes: list[int]) -> dict[str, int]:
    """Map each title to its length in minutes.

    Args:
        titles: The session titles.
        minutes: Each session's length, in the same order as `titles`.

    Returns:
        A dict from title to minutes.
    """
    return {title: mins for title, mins in zip(titles, minutes)}


def initials(names: dict[str, int]) -> set[str]:
    """Return the uppercase first letters of the names, deduplicated.

    Args:
        names: A mapping whose keys are the names.

    Returns:
        A set of single uppercase letters.
    """
    return {name[0].upper() for name in names}


def flatten(rosters: list[list[str]]) -> list[str]:
    """Return every name from every roster, in order, duplicates kept.

    Args:
        rosters: One list of names per study circle.

    Returns:
        A single flat list of names.
    """
    return [name for roster in rosters for name in roster]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"slugs:     {slugs(TITLES)[0]}")
    print(f"long:      {', '.join(long_sessions(TITLES, MINUTES))}")
    print(f"labels:    {' '.join(labels(SCORES))}")
    print(f"lookup:    Git Basics -> {title_to_minutes(TITLES, MINUTES)['Git Basics']}")
    print(f"initials:  {', '.join(sorted(initials(SCORES)))}")
    print(f"flattened: {len(flatten(ROSTERS))} names, {len(set(flatten(ROSTERS)))} unique")

    assert slugs(TITLES) == slugs_loop(TITLES)
    assert long_sessions(TITLES, MINUTES) == long_sessions_loop(TITLES, MINUTES)
    assert long_sessions(TITLES, MINUTES) == ["Intro to Loops", "List Comprehensions", "Dict Patterns"]
    assert labels(SCORES) == labels_loop(SCORES) == ["pass", "retry", "pass", "retry", "pass"]
    assert title_to_minutes(TITLES, MINUTES) == title_to_minutes_loop(TITLES, MINUTES)
    assert initials(SCORES) == initials_loop(SCORES) == {"A", "G", "L", "M"}
    assert flatten(ROSTERS) == flatten_loop(ROSTERS)
    assert flatten(ROSTERS) == ["ada", "grace", "linus", "margaret", "guido", "ada"]
    print("All checks passed.")
