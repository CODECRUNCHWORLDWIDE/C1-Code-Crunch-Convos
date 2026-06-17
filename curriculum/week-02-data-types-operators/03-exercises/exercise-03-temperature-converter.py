"""Exercise 03 — Celsius to Fahrenheit Converter.

Task
----
Write a function ``c_to_f(celsius: float) -> float`` that converts a
temperature in Celsius to Fahrenheit using the formula:

    F = C * 9 / 5 + 32

Then write a small ``main()`` that demonstrates your function on a
known set of inputs and prints a table.

Requirements
------------
1. Implement ``c_to_f`` with full type hints and a docstring describing
   what it does, the parameter, and the return value.

2. In ``main()``, define a list of test temperatures (provided below)
   and print one row per temperature in this exact format:

   ::

       C     ->   F
       ----------------
         -40.0  ->   -40.00
           0.0  ->    32.00
          20.0  ->    68.00
         100.0  ->   212.00

3. The Celsius value should be right-aligned in a width-6 field with
   one decimal place. The Fahrenheit value should be right-aligned in
   a width-8 field with two decimals.

Bonus 1
-------
Also implement the inverse: ``f_to_c(fahrenheit: float) -> float``.

Bonus 2
-------
Implement ``c_to_k(celsius: float) -> float`` to convert Celsius to
Kelvin. The conversion is ``K = C + 273.15``. Add a column to your
table.

Sanity Check
------------
- ``c_to_f(0)`` must return ``32.0``.
- ``c_to_f(100)`` must return ``212.0``.
- ``c_to_f(-40)`` must return ``-40.0`` (the famous crossover point).

If ``mypy`` is installed, this file should pass with no errors.
"""


def c_to_f(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Parameters
    ----------
    celsius:
        Temperature in degrees Celsius.

    Returns
    -------
    float
        The same temperature expressed in degrees Fahrenheit.
    """
    # TODO: implement the conversion: F = C * 9 / 5 + 32
    raise NotImplementedError("Replace this with your implementation.")


def main() -> None:
    test_temperatures: list[float] = [-40.0, 0.0, 20.0, 100.0]

    print(f"{'C':>6}  ->  {'F':>8}")
    print("-" * 22)
    for c in test_temperatures:
        f = c_to_f(c)
        print(f"{c:>6.1f}  ->  {f:>8.2f}")


if __name__ == "__main__":
    main()
