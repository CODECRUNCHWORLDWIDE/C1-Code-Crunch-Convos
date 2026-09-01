"""Score a password against five simple rules and label its strength.

Week 4 homework, problem 2, Code Crunch Convos.

Save your own copy as ``password.py`` in your ``homework/`` folder.

``password_strength`` decides. ``_demo`` prints. Keeping those two jobs in
two functions is why the decision can be tested without capturing output.
"""

SAMPLES: list[str] = ["hunter2", "Hunter2024", "Hunter2024!"]


def password_strength(password: str) -> str:
    """Return "weak", "medium" or "strong" for `password`.

    One point per rule met: length >= 8, has a lowercase letter, has an
    uppercase letter, has a digit, has a non-alphanumeric character.
    A score of 0-2 is weak, 3-4 is medium, 5 is strong.

    Args:
        password: The candidate password.

    Returns:
        One of "weak", "medium", "strong".

    Example:
        >>> password_strength("Hunter2024!")
        'strong'
    """
    rules = [
        len(password) >= 8,
        any(char.islower() for char in password),
        any(char.isupper() for char in password),
        any(char.isdigit() for char in password),
        any(not char.isalnum() for char in password),
    ]
    score = sum(rules)
    if score <= 2:
        return "weak"
    if score <= 4:
        return "medium"
    return "strong"


def _demo() -> None:
    """Print the strength of three sample passwords, one per band."""
    for sample in SAMPLES:
        print(f"{sample!r:>14} -> {password_strength(sample)}")


if __name__ == "__main__":
    _demo()
