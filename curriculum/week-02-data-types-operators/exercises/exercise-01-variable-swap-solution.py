"""exercise-01-variable-swap-solution.py — trade and rotate shifts with no temporary.

Week 2, Exercise 1. Practises tuple unpacking and multiple assignment.
"""


def swap(first: str, second: str) -> tuple[str, str]:
    """Return the early and late volunteers in the opposite order."""
    return second, first


def rotate(a: str, b: str, c: str) -> tuple[str, str, str]:
    """Move Mon/Tue/Wed one day forward, wrapping the last to the front.

    rotate("Ada", "Grace", "Alan") returns ("Alan", "Ada", "Grace").
    """
    return c, a, b


def main() -> None:
    """Print the roster before and after a swap and a rotation."""
    early: str = "Ada"
    late: str = "Grace"
    print("Shift swap")
    print(f"  before: early={early}, late={late}")
    early, late = swap(early, late)
    print(f"  after : early={early}, late={late}")

    monday: str = "Ada"
    tuesday: str = "Grace"
    wednesday: str = "Alan"
    print("Weekly rotation")
    print(f"  before: {monday}, {tuesday}, {wednesday}")
    monday, tuesday, wednesday = rotate(monday, tuesday, wednesday)
    print(f"  after : {monday}, {tuesday}, {wednesday}")


if __name__ == "__main__":
    main()
