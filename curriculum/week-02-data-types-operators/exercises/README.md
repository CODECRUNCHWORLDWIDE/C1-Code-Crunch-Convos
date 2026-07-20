# Week 2 — Exercises

Four short, focused exercises. Each takes 10 to 30 minutes. Do them in
order; later exercises assume techniques from earlier ones.

## How to Use These

1. Open the exercise file in your editor.
2. Read the docstring at the top — it describes the task, inputs,
   outputs, and any constraints.
3. Implement the solution where indicated.
4. Run the file from your terminal:

   ```bash
   python exercises/exercise-01-variable-swap.py
   ```

5. Compare your output to the **Expected Output** section in the
   docstring.
6. If you installed `mypy`, run it on your finished file:

   ```bash
   mypy exercises/exercise-01-variable-swap.py
   ```

   Aim for `Success: no issues found`.

## The Exercises

| # | File | Topic | Difficulty |
|---|------|-------|------------|
| 1 | [exercise-01-variable-swap.py](./exercise-01-variable-swap.py) | Tuple unpacking, multiple assignment | Easy |
| 2 | [exercise-02-string-formatter.py](./exercise-02-string-formatter.py) | f-strings, alignment, format specs | Easy |
| 3 | [exercise-03-temperature-converter.py](./exercise-03-temperature-converter.py) | Functions, type hints, arithmetic | Medium |
| 4 | [exercise-04-input-parsing.py](./exercise-04-input-parsing.py) | `input()`, casting, error handling | Medium |

## A Note on Style

Every exercise file expects you to:

- Use `snake_case` for variables and functions.
- Add a docstring to each function you write.
- Use type hints on function parameters and return values.
- Avoid magic numbers — name constants with `UPPER_SNAKE_CASE`.

If you finish all four and want more practice, move on to the
[challenges](../challenges/README.md).
