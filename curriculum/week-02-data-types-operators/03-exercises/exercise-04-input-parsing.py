"""Exercise 04 — Input Parsing with Arithmetic.

Task
----
Read two numbers from the user, then print the four basic arithmetic
results: sum, difference, product, and quotient. Handle bad input
gracefully — if the user types something that isn't a number, the
program must print a helpful error message and exit cleanly (not with
a traceback).

Requirements
------------
1. Prompt the user with ``"First number: "`` and read a line.
2. Prompt with ``"Second number: "`` and read a second line.
3. Try to convert both inputs to ``float``. If either conversion fails,
   print:

   ::

       Error: please enter valid numbers.

   and return from ``main()`` immediately.

4. Compute:

   - ``a + b``  (sum)
   - ``a - b``  (difference)
   - ``a * b``  (product)
   - ``a / b``  (quotient)

5. If ``b`` is zero, print:

   ::

       Error: cannot divide by zero.

   instead of attempting the division. (Print the sum, difference, and
   product first; only suppress the quotient line.)

6. Print results in this format, each value rounded to 2 decimals and
   right-aligned in a width-10 field:

   ::

       Sum       :     12.50
       Difference:      2.50
       Product   :     35.00
       Quotient  :      1.40

Bonus
-----
Also print ``a ** b`` (power) and ``a % b`` (remainder), with the same
formatting. Skip the remainder line if ``b`` is zero.

Tips
----
- Use ``try / except ValueError`` around the casts.
- Check ``if b == 0:`` before the division. Note: for floats this is
  usually fine, but be aware that very small floats can also produce
  ``inf`` if you divide by them.
- Use the ``:>10.2f`` format spec for the numeric columns.

Sample Session
--------------
::

    $ python exercise-04-input-parsing.py
    First number: 7.5
    Second number: 5
    Sum       :     12.50
    Difference:      2.50
    Product   :     37.50
    Quotient  :      1.50

    $ python exercise-04-input-parsing.py
    First number: hello
    Second number: 5
    Error: please enter valid numbers.
"""


def main() -> None:
    raw_a: str = input("First number: ")
    raw_b: str = input("Second number: ")

    # TODO: convert raw_a and raw_b to floats inside a try/except.
    #       If either fails, print the error message from the docstring
    #       and return.

    # TODO: compute and print the four results.
    #       Use the format ``"Sum       : {value:>10.2f}"`` etc.
    #       Skip the quotient line (with its own error message) if b == 0.

    _ = (raw_a, raw_b)  # remove this once your TODOs are done


if __name__ == "__main__":
    main()
