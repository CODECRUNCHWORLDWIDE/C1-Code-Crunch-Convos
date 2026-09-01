"""exercise-03-script-vs-repl-solution.py — one file, two ways to run it."""

SIGNUPS: list[str] = ["Ada", "Grace", "Katherine", "Dorothy", "Mary"]


def initials(names: list[str]) -> str:
    """Return each name's first letter, joined by single spaces."""
    return " ".join(name[0] for name in names)


def longest(names: list[str]) -> str:
    """Return the longest name. Ties go to the earliest one in the list."""
    if not names:
        return ""
    return max(names, key=len)


len(SIGNUPS)  # Value computed, then discarded; only the REPL echoes results.


if __name__ == "__main__":
    print(f"Signups: {len(SIGNUPS)}")
    print(f"Initials: {initials(SIGNUPS)}")
    print(f"Longest name: {longest(SIGNUPS)}")
    print(f"Running as: {__name__!r}")


# What survives a plain run?  Nothing. The interpreter exits when the last
# line finishes and every name in this file is freed with it.
# What survives a `python -i` run?  The whole module namespace: SIGNUPS,
# initials, longest, __name__ — Python drops you at >>> instead of exiting.
# Does a name appended at the >>> prompt show up in the next run?  No. The
# append changed the list object in memory, not the source file on disk,
# so a fresh run builds the same five-name list again.
