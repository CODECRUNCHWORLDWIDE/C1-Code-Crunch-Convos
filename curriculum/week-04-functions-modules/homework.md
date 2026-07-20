# Week 4 — Homework

Six problems. Aim for about 5 hours total. Each problem asks for a function or a small module. Type hints and docstrings are mandatory.

When you finish, place your solutions in a folder called `homework/` next to this file. Suggested filenames are in each problem.

---

## Problem 1 — Temperature module

**File:** `homework/temperature.py`

Build a module with **three** functions:

- `c_to_f(celsius: float) -> float` — convert Celsius to Fahrenheit. Formula: `c * 9 / 5 + 32`.
- `f_to_c(fahrenheit: float) -> float` — convert Fahrenheit to Celsius. Formula: `(f - 32) * 5 / 9`.
- `c_to_k(celsius: float) -> float` — convert Celsius to Kelvin. Formula: `c + 273.15`.

Each function:

- Has a docstring including an `Example:` block.
- Has type hints.
- Raises `ValueError` from `c_to_k` if the temperature is below absolute zero (`-273.15`).

Under `if __name__ == "__main__":`, print a small table:

```text
   C       F        K
---------------------
   0    32.00   273.15
 100   212.00   373.15
 -40   -40.00   233.15
```

---

## Problem 2 — Password strength

**File:** `homework/password.py`

Write `password_strength(password: str) -> str` that returns one of `"weak"`, `"medium"`, or `"strong"` based on these rules:

| Rule | Counts toward score |
|------|---------------------|
| Length >= 8 | +1 |
| Has at least one lowercase letter | +1 |
| Has at least one uppercase letter | +1 |
| Has at least one digit | +1 |
| Has at least one non-alphanumeric character | +1 |

- Score 0–2 → `"weak"`
- Score 3–4 → `"medium"`
- Score 5 → `"strong"`

Type hints, docstring. Include a `_demo()` function that prints the strength of three sample passwords, called under `if __name__ == "__main__":`.

Hint: use methods like `str.islower()`, `str.isupper()`, `str.isdigit()`, `str.isalnum()` and `any(...)`.

---

## Problem 3 — Leap year function with tests

**File:** `homework/leap.py`

Write `is_leap_year(year: int) -> bool` using the Gregorian rules:

1. Year divisible by 400 → leap year.
2. Else year divisible by 100 → not a leap year.
3. Else year divisible by 4 → leap year.
4. Else → not a leap year.

Also write a `_run_tests()` function that exercises at least these cases and prints "All tests passed" if they all match:

| year | expected |
|------|----------|
| 2000 | True |
| 1900 | False |
| 2024 | True |
| 2023 | False |
| 2100 | False |
| 2400 | True |

Run `_run_tests()` from `if __name__ == "__main__":`.

---

## Problem 4 — Recursive sum

**File:** `homework/recursive_sum.py`

Write `sum_recursive(nums: list[int]) -> int` that returns the sum of a list **without using `sum`**, **without using a loop**, and **using recursion**.

Hint: the base case is the empty list (returns `0`). Otherwise return `nums[0] + sum_recursive(nums[1:])`.

Also include `sum_iterative(nums: list[int]) -> int` for comparison. Both must produce the same answer on the same input.

Self-test cases:

- `[]` → 0
- `[5]` → 5
- `[1, 2, 3, 4]` → 10
- `[-1, 1]` → 0

---

## Problem 5 — Dict builder

**File:** `homework/dict_builder.py`

Write `build_record(**fields)` that returns a dict containing only the keys whose values are not `None`. The function should be type-hinted and documented.

Examples:

```python
build_record(name="Amina", age=29, email=None)
# {"name": "Amina", "age": 29}

build_record()
# {}

build_record(a=None, b=None)
# {}
```

Also write `merge_records(*records: dict) -> dict` that takes any number of dicts and returns one merged dict (later records overwrite earlier ones on key collisions).

```python
merge_records({"a": 1}, {"b": 2}, {"a": 99})
# {"a": 99, "b": 2}
```

Hint: `result = {}` then loop and `result.update(r)`.

---

## Problem 6 — Importing from a custom module

**Files:** `homework/mymath.py` and `homework/use_mymath.py`

In `mymath.py`, define:

- `square(n: int) -> int`
- `cube(n: int) -> int`
- `is_prime(n: int) -> bool` — return `True` if `n` is prime (use trial division up to `int(n ** 0.5) + 1`).

In `use_mymath.py`, import all three functions and write a `main()` that:

1. Prints `square(7)` and `cube(7)`.
2. Lists the primes between 2 and 30 (inclusive) using `is_prime`.

Run `main()` from `if __name__ == "__main__":`.

You should be able to execute this from a terminal:

```bash
cd homework
python use_mymath.py
```

If the script crashes with `ModuleNotFoundError: No module named 'mymath'`, double-check that both files are in the same folder and that you ran `python use_mymath.py` from that folder.

---

## Submission

Your `homework/` folder should end up like this:

```text
homework/
    temperature.py
    password.py
    leap.py
    recursive_sum.py
    dict_builder.py
    mymath.py
    use_mymath.py
```

Commit with `feat(week-04): homework problems`. If you are in a cohort, open a PR.

## Grading guide (out of 60)

| Problem | Points |
|---------|--------|
| 1 | 10 |
| 2 | 10 |
| 3 | 10 |
| 4 | 10 |
| 5 | 10 |
| 6 | 10 |

You lose 1 point per missing docstring, 1 point per missing type hint, and 2 points for any function over 25 lines.
