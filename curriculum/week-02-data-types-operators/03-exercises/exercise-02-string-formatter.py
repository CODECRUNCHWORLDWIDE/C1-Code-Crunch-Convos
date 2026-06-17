"""Exercise 02 — String Formatter with Aligned f-strings.

Task
----
Build a small profile printer that takes three pieces of information —
a name (string), an age (int), and a test score as a percentage (float
between 0 and 1) — and prints them as an aligned, multi-line "card."

The card must look exactly like this (note the box drawing and the
alignment of the values on the right):

::

    +----------------------------+
    | Name        : Ada Lovelace |
    | Age         :           36 |
    | Score       :       92.50% |
    +----------------------------+

Requirements
------------
1. Inside ``main()``, define three variables:

   ::

       name = "Ada Lovelace"
       age = 36
       score = 0.925

2. Use a SINGLE multi-line f-string (triple-quoted) to build the card.
3. Inside the card:

   - The name is left-aligned but should sit on the line as shown.
   - The age and score are right-aligned to width ``12``.
   - The score is shown as a percentage with 2 decimals (``:.2%``).

4. ``print()`` the card.

Bonus
-----
Wrap the formatting logic in a function ``format_card(name: str, age:
int, score: float) -> str`` that returns the card as a string. Call it
from ``main()`` and ``print()`` the result.

Tips
----
- The ``:.2%`` format spec multiplies by 100 and appends ``%``. So
  ``f"{0.925:.2%}"`` prints ``"92.50%"``.
- Right-align with ``>``: ``f"{value:>12}"`` pads on the left to width 12.
- Combine: ``f"{score:>12.2%}"`` right-aligns a 2-decimal percentage in
  a field of width 12.

Expected Output
---------------
::

    +----------------------------+
    | Name        : Ada Lovelace |
    | Age         :           36 |
    | Score       :       92.50% |
    +----------------------------+
"""


def main() -> None:
    name: str = "Ada Lovelace"
    age: int = 36
    score: float = 0.925

    # TODO: Build the card as a multi-line f-string and print it.
    #
    # The card should match the "Expected Output" in the docstring above.
    # Hint: a triple-quoted f-string lets you write the box on multiple
    # lines exactly as it should appear.
    #
    # card = f"""..."""
    # print(card)

    # Variables are referenced here so linters don't warn about unused
    # names. Remove these lines once your TODO above is complete.
    _ = (name, age, score)


if __name__ == "__main__":
    main()
