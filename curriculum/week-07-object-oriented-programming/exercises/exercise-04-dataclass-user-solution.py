"""exercise-04-dataclass-user-solution.py — a record type in four lines.

Models a workshop signup for the org's community sessions. The `-solution` in
the name keeps this file from colliding with the
`exercise-04-dataclass-user.py` you write yourself. Run it with::

    python exercise-04-dataclass-user-solution.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    """One person signed up for a workshop."""

    username: str
    email: str
    interests: list[str] = field(default_factory=list)
    active: bool = True

    def __post_init__(self) -> None:
        """Reject a signup whose email could not possibly be an email."""
        if "@" not in self.email:
            raise ValueError(f"email must contain '@', got {self.email!r}")

    def add_interest(self, topic: str) -> None:
        """Record one topic. Adding the same topic twice changes nothing."""
        if topic not in self.interests:
            self.interests.append(topic)


def main() -> None:
    """Sign two people up, compare records, and reject one bad email."""
    rlopez = User("rlopez", "rlopez@example.org", ["python", "gis"])
    amina = User("amina", "amina@example.org")

    print(rlopez)
    print(amina)

    twin = User("rlopez", "rlopez@example.org", ["python", "gis"])
    print(f"equal: {rlopez == twin}   same object: {rlopez is twin}")

    rlopez.add_interest("mapping")
    rlopez.add_interest("python")
    print(f"rlopez interests: {rlopez.interests}")
    print(f"amina interests: {amina.interests}")

    try:
        User("dana", "not-an-email")
    except ValueError as exc:
        print(f"Rejected: {exc}")


if __name__ == "__main__":
    main()
