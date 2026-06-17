"""
Exercise 03 — Password Checker
==============================

Keep asking the user to enter a password until they enter one that
satisfies ALL of the following rules:

1. At least 8 characters long.
2. Contains at least one digit (`0-9`).
3. Contains at least one letter (a-z or A-Z).

When they finally enter a valid password, print:

    Password accepted.

If they enter a bad one, print which rules failed (one per failed rule),
then ask again.

Example session
---------------
    Enter a password: hi
    - Must be at least 8 characters.
    - Must contain at least one digit.
    Enter a password: abcdefgh
    - Must contain at least one digit.
    Enter a password: abcd1234
    Password accepted.

Skills practised
----------------
- `while True:` paired with `break`
- Building a list of error messages (filtering pattern)
- The `any(...)` built-in with a generator expression
- `str.isdigit()`, `str.isalpha()` (works per-character)

Hints
-----
- `any(c.isdigit() for c in pw)` is True if at least one character of
  `pw` is a digit. The same trick with `c.isalpha()` checks letters.
- Collect failure messages in a list. If the list is empty after
  checking, the password is valid -> `break`.
- DO NOT print real passwords in a real app. This is a teaching example.

Run me
------
    python exercise-03-password-checker.py
"""


def main() -> None:
    while True:
        pw = input("Enter a password: ")

        problems: list[str] = []

        # TODO: Append a message to `problems` for each rule that fails.
        # Rule 1: length >= 8
        # Rule 2: contains at least one digit
        # Rule 3: contains at least one letter

        if not problems:
            print("Password accepted.")
            break

        for message in problems:
            print(f"- {message}")


if __name__ == "__main__":
    main()
