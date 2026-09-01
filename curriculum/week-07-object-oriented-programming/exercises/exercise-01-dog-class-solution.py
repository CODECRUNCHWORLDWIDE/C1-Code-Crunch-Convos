"""exercise-01-dog-class-solution.py — one blueprint, many independent dogs.

Models the dogs on a route for Mesa Dog Walkers. The `-solution` in the name
keeps this file from colliding with the `exercise-01-dog-class.py` you write
yourself. Run it with::

    python exercise-01-dog-class-solution.py
"""


class Dog:
    """A single dog on the walking roster."""

    species: str = "Canis familiaris"

    def __init__(self, name: str, age: int) -> None:
        """Store this dog's name and age, and give it an empty trick list."""
        self.name = name
        self.age = age
        self.tricks: list[str] = []

    def bark(self) -> str:
        """Return this dog's greeting, e.g. `Biscuit says woof!`."""
        return f"{self.name} says woof!"

    def have_birthday(self) -> None:
        """Add one year to this dog's age. Returns nothing."""
        self.age += 1

    def learn(self, trick: str) -> None:
        """Append one trick to this dog's own trick list."""
        self.tricks.append(trick)

    def __repr__(self) -> str:
        """Developer form, e.g. `Dog(name='Biscuit', age=4)`."""
        return f"Dog(name={self.name!r}, age={self.age!r})"

    def __str__(self) -> str:
        """User form, e.g. `Biscuit, age 4, knows: sit, wait`."""
        known = ", ".join(self.tricks) if self.tricks else "no tricks yet"
        return f"{self.name}, age {self.age}, knows: {known}"


def main() -> None:
    """Run two dogs through a day and print what changed."""
    biscuit = Dog("Biscuit", 3)
    juniper = Dog("Juniper", 7)

    print(biscuit.bark())
    print(juniper.bark())

    biscuit.learn("sit")
    biscuit.learn("wait")
    biscuit.have_birthday()

    print(biscuit)
    print(juniper)
    print(repr(biscuit))
    print(Dog.species)


if __name__ == "__main__":
    main()
