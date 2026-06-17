"""Exercise 04 — @dataclass for a User.

Goal
----
Use the ``@dataclass`` decorator to build a `User` class with these fields:

* ``username: str``
* ``email: str``
* ``is_active: bool = True``

Then in `main()`:

1. Create two ``User`` instances with the same ``username`` and ``email``.
2. Print one of them — note that ``@dataclass`` generated a nice ``__repr__``.
3. Compare them with ``==`` — they are equal, because ``@dataclass`` also
   generated ``__eq__``.
4. Create a third user with a different email and confirm it is *not* equal
   to the first two.

Expected output (approximately)
-------------------------------
    User(username='ada', email='ada@example.com', is_active=True)
    a == b  -> True
    a == c  -> False

Run with:

    python exercise-04-dataclass-user.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    username: str
    email: str
    is_active: bool = True


def main() -> None:
    a = User(username="ada", email="ada@example.com")
    b = User(username="ada", email="ada@example.com")
    c = User(username="ada", email="other@example.com")

    print(a)                # auto-generated __repr__
    print(f"a == b  -> {a == b}")   # auto-generated __eq__: True
    print(f"a == c  -> {a == c}")   # different email: False


if __name__ == "__main__":
    main()
