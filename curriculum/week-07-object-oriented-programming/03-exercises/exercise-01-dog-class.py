"""Exercise 01 — A first class: Dog.

Goal
----
Define a `Dog` class with:

* an `__init__` that takes a `name` (str) and an `age` (int),
* a method `bark()` that returns the string ``"<name> says woof!"``,
* a method `describe()` that returns a single-line description such as
  ``"Fido is 3 years old."``.

Then in `main()`, create two dogs and print the result of both methods on
each.

Expected output
---------------
    Fido says woof!
    Fido is 3 years old.
    Rex says woof!
    Rex is 5 years old.

Run with:

    python exercise-01-dog-class.py
"""

from __future__ import annotations


class Dog:
    """A very small dog model."""

    def __init__(self, name: str, age: int) -> None:
        # TODO: store name and age as instance attributes on self.
        self.name = name
        self.age = age

    def bark(self) -> str:
        # TODO: return "<name> says woof!"
        return f"{self.name} says woof!"

    def describe(self) -> str:
        # TODO: return "<name> is <age> years old."
        return f"{self.name} is {self.age} years old."


def main() -> None:
    fido = Dog("Fido", 3)
    rex = Dog("Rex", 5)

    for dog in (fido, rex):
        print(dog.bark())
        print(dog.describe())


if __name__ == "__main__":
    main()
