"""Exercise 01 — Variable Swap Without a Temporary.

Task
----
In most programming languages, swapping two variables requires a temporary:

    temp = a
    a = b
    b = temp

Python has a much cleaner way using *tuple unpacking*. Your task is to:

1. Create two variables ``a`` and ``b``. ``a`` should hold the integer 1
   and ``b`` should hold the integer 2.
2. Print them in the form ``"Before: a=1, b=2"``.
3. Swap their values in a SINGLE line of code, without using a third
   variable.
4. Print them again in the form ``"After:  a=2, b=1"``.

You should be able to do the swap with this exact pattern:

    a, b = b, a

The right side ``(b, a)`` is built as a tuple first, then unpacked into
the names on the left.

Bonus
-----
After you complete the basic task, do the same with three variables
``x``, ``y``, ``z`` initially holding ``"red"``, ``"green"``, ``"blue"``
respectively. Rotate them so ``x`` ends up with ``"green"``, ``y`` with
``"blue"``, and ``z`` with ``"red"`` — in one line.

Expected Output
---------------
::

    Before: a=1, b=2
    After:  a=2, b=1
    Before: x=red, y=green, z=blue
    After:  x=green, y=blue, z=red

Hints
-----
- Use an f-string for the prints.
- The "Before" and "After" labels are seven characters wide so the
  outputs line up. Use ``:>2`` width specs on the values if you want
  them perfectly aligned with multi-digit numbers.
"""


def main() -> None:
    # --- Part 1: swap two integers ---
    a: int = 1
    b: int = 2

    print(f"Before: a={a}, b={b}")

    # TODO: swap a and b on a single line using tuple unpacking.
    # a, b = ...

    print(f"After:  a={a}, b={b}")

    # --- Part 2 (bonus): rotate three strings ---
    x: str = "red"
    y: str = "green"
    z: str = "blue"

    print(f"Before: x={x}, y={y}, z={z}")

    # TODO: rotate so x="green", y="blue", z="red" — in one line.
    # x, y, z = ...

    print(f"After:  x={x}, y={y}, z={z}")


if __name__ == "__main__":
    main()
