# Challenge 1 — TDD FizzBuzz

**Goal:** experience the full red-green-refactor rhythm by building FizzBuzz one test at a time. No peeking at a finished implementation. Every line of production code must be motivated by a failing test.

**Approx. time:** 1 hour.

---

## The problem

For numbers 1 to N, return a list of strings:

- If the number is divisible by 3, the entry is `"Fizz"`.
- If the number is divisible by 5, the entry is `"Buzz"`.
- If the number is divisible by *both* 3 and 5, the entry is `"FizzBuzz"`.
- Otherwise, the entry is the number as a string (e.g. `"7"`).

So `fizzbuzz(15)` returns:

```python
["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
```

---

## Rules

1. You will write **tests first**. Every commit message starts with `RED`, `GREEN`, or `REFACTOR`.
2. You may only write enough production code to make the current failing test pass. No "while I'm here" fixes.
3. After each `GREEN`, look for a refactor opportunity. Commit it as `REFACTOR`.
4. The final test suite must run in under one second.
5. The final implementation must lint cleanly with `ruff` and format cleanly with `black`.

---

## Suggested test order

This is not a script — feel free to deviate — but the order below leads to a clean implementation:

1. `test_returns_a_list` — `fizzbuzz(1)` returns a list.
2. `test_length_matches_n` — `fizzbuzz(5)` returns a list of length 5.
3. `test_plain_numbers` — `fizzbuzz(2)` returns `["1", "2"]`.
4. `test_three_is_fizz` — entry at index 2 (the number 3) is `"Fizz"`.
5. `test_five_is_buzz` — entry at index 4 (the number 5) is `"Buzz"`.
6. `test_fifteen_is_fizzbuzz` — entry at index 14 (the number 15) is `"FizzBuzz"`.
7. `test_full_output_to_fifteen` — match the full 15-element list above.
8. `test_zero_returns_empty_list` — edge case.
9. `test_negative_raises_value_error` — negative `n` raises `ValueError`.

---

## Layout

```
challenge-01-tdd-fizzbuzz/
├── fizzbuzz.py
├── test_fizzbuzz.py
├── pyproject.toml
└── README.md           # describe how to run and your TDD log
```

Minimal `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-ra -q"
testpaths = ["."]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.black]
line-length = 100
target-version = ["py312"]
```

---

## Deliverables

1. The `fizzbuzz.py` and `test_fizzbuzz.py` files.
2. At least **9 commits** that follow the `RED` → `GREEN` → `REFACTOR` cadence.
3. A short `README.md` with:
   - How to run the tests.
   - A bullet list of your commits in order, showing the rhythm.
   - One paragraph reflecting on whether TDD felt natural or fought you.
4. `ruff check .` and `black --check .` both pass.
5. `pytest` shows all tests passing.

---

## Rubric

| Criterion                                   | Points |
|---------------------------------------------|--------|
| TDD commit rhythm visible in `git log`      | 4      |
| All 9+ tests pass                           | 3      |
| `ruff` and `black` clean                    | 2      |
| Reflection paragraph in README              | 1      |
| **Total**                                   | **10** |

---

## Hints

- The cleanest implementation is a list comprehension. Resist writing it until the simplest tests pass.
- `pytest -k fizz` runs only tests whose name contains "fizz" — useful while drilling on one rule.
- If you find yourself writing a test that already passes, **delete it** and write one that actually fails first. That is the discipline.
