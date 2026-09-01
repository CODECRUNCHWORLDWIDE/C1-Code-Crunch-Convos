"""exercise-01-list-operations-solution.py — the study-session leaderboard.

Four small reporting functions over a list of session records. One ranks,
one picks the longest, two slice the ranking down to a headline.

None of them rearranges the list the caller handed in.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import namedtuple

# ---- Given data ----
Session = namedtuple("Session", ["title", "city", "minutes", "attendees"])

SESSIONS: list[Session] = [
    Session("Intro to Loops", "Lagos", 90, 42),
    Session("Debugging Clinic", "Nairobi", 60, 17),
    Session("List Comprehensions", "Lagos", 120, 35),
    Session("Git Basics", "Accra", 45, 58),
    Session("Dict Patterns", "Nairobi", 75, 35),
    Session("Reading Tracebacks", "Accra", 30, 23),
]


# ---- Your task ----
def sort_by_attendees(sessions: list[Session]) -> list[Session]:
    """Return a NEW list ordered by attendance, highest first.

    Args:
        sessions: The session records to rank. This list is not modified.

    Returns:
        A new list, most attendees first, ties broken by title A to Z.
    """
    return sorted(sessions, key=lambda s: (-s.attendees, s.title))


def longest_session(sessions: list[Session]) -> Session:
    """Return the single session with the most minutes.

    Args:
        sessions: The session records to search.

    Returns:
        The whole record, not just its title or its minutes.
    """
    return max(sessions, key=lambda s: s.minutes)


def top_three_titles(sessions: list[Session]) -> list[str]:
    """Return the titles of the three best-attended sessions, in rank order.

    Args:
        sessions: The session records to rank.

    Returns:
        Three title strings, best attended first.
    """
    return [s.title for s in sort_by_attendees(sessions)[:3]]


def total_minutes_of_top(sessions: list[Session], n: int) -> int:
    """Return the combined minutes of the n best-attended sessions.

    Args:
        sessions: The session records to rank.
        n: How many of the top-ranked sessions to add up.

    Returns:
        The sum of those sessions' minutes.
    """
    return sum(s.minutes for s in sort_by_attendees(sessions)[:n])


# ---- Self-check ----
if __name__ == "__main__":
    ranked = sort_by_attendees(SESSIONS)
    for s in ranked:
        print(f"{s.attendees:3d}  {s.title} ({s.city})")

    assert [s.title for s in ranked[:3]] == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert ranked[-1].title == "Debugging Clinic"
    assert longest_session(SESSIONS).title == "List Comprehensions"
    assert longest_session(SESSIONS).minutes == 120
    assert top_three_titles(SESSIONS) == ["Git Basics", "Intro to Loops", "Dict Patterns"]
    assert total_minutes_of_top(SESSIONS, 3) == 210
    assert SESSIONS[0].title == "Intro to Loops"  # original list untouched
    print("All checks passed.")
