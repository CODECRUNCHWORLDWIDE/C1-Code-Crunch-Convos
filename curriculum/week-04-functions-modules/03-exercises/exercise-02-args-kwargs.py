"""Exercise 02 - *args and **kwargs.

Goals:
    * Write a function that accepts any number of positional arguments.
    * Write a function that accepts any number of keyword arguments.
    * Practice unpacking with `*` and `**` at the call site.

How to run:
    $ python exercise-02-args-kwargs.py
"""


# ---------------------------------------------------------------------------
# TASK 1
#
# Write `summarize(*nums, label="Total")` that:
#   - Accepts any number of numbers (ints or floats) as positional arguments.
#   - Accepts a keyword-only `label` (default "Total").
#   - Returns a string of the form "<label>: <sum>".
#   - If no numbers are passed, the sum is 0.
#
# Examples:
#   summarize(1, 2, 3)              -> "Total: 6"
#   summarize(1.5, 2.5, label="X")  -> "X: 4.0"
#   summarize(label="Empty")        -> "Empty: 0"
# ---------------------------------------------------------------------------
def summarize(*nums: float, label: str = "Total") -> str:
    """Return a labelled sum of `nums`."""
    # TODO: compute the sum and return the formatted string.
    return f"{label}: {sum(nums)}"


# ---------------------------------------------------------------------------
# TASK 2
#
# Write `make_user(**fields)` that returns a dict containing exactly the
# keyword arguments that were passed in.
#
# Examples:
#   make_user(name="Amina")                     -> {"name": "Amina"}
#   make_user(name="Diego", age=31)             -> {"name": "Diego", "age": 31}
#   make_user()                                 -> {}
# ---------------------------------------------------------------------------
def make_user(**fields: object) -> dict[str, object]:
    """Return a dict built from the keyword arguments."""
    # TODO: return the fields as a regular dict.
    return dict(fields)


# ---------------------------------------------------------------------------
# TASK 3 (small bonus)
#
# Write `call_with_list(func, items)` that takes a callable and a list of
# numbers, and returns `func(*items)` (the items unpacked as positional
# arguments).
#
# Example:
#   call_with_list(summarize, [1, 2, 3]) -> "Total: 6"
# ---------------------------------------------------------------------------
def call_with_list(func, items: list) -> object:
    """Call `func` with `items` unpacked as positional arguments."""
    # TODO: return func(*items).
    return func(*items)


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    failures: list[str] = []

    # Task 1
    if summarize(1, 2, 3) != "Total: 6":
        failures.append("summarize(1, 2, 3) wrong")
    if summarize() != "Total: 0":
        failures.append("summarize() should report 0")
    if summarize(1.5, 2.5, label="X") != "X: 4.0":
        failures.append('summarize(1.5, 2.5, label="X") wrong')
    if summarize(label="Empty") != "Empty: 0":
        failures.append('summarize(label="Empty") wrong')

    # Unpacking at the call site
    nums = [10, 20, 30]
    if summarize(*nums) != "Total: 60":
        failures.append("summarize(*[10,20,30]) wrong")

    # Task 2
    if make_user() != {}:
        failures.append("make_user() should be empty dict")
    if make_user(name="Amina") != {"name": "Amina"}:
        failures.append('make_user(name="Amina") wrong')
    profile = {"name": "Diego", "age": 31}
    if make_user(**profile) != profile:
        failures.append("make_user(**profile) wrong")

    # Task 3
    if call_with_list(summarize, [1, 2, 3]) != "Total: 6":
        failures.append("call_with_list(summarize, [1,2,3]) wrong")

    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("All tests passed.")


if __name__ == "__main__":
    _run_tests()
