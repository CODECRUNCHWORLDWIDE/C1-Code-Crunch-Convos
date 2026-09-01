# Week 2 — Exercises

Four short, focused exercises. Each takes 10 to 30 minutes. Do them in
order; later exercises assume techniques from earlier ones.

## How to Use These

Each exercise below is a page, not a file you download. The page holds
the brief, a starter you copy, the requirements, the exact output your
program should produce, and a list of the bugs that catch people on that
particular task. You create the `.py` file yourself, in your own practice
repository. Typing the starter out is part of the exercise.

1. Open the exercise page and read it all the way through before you
   write anything, including the **Common bugs to catch** section. It is
   quicker to recognise a bug you have already read about than to
   diagnose it cold.
2. Create the matching file in your `exercises/` folder — for Exercise 1
   that is `exercise-01-variable-swap.py` — and copy the **Starter file**
   block into it.
3. Fill in the `TODO` markers. Leave the docstrings and type hints in
   place; they are part of the spec, not decoration.
4. Run the file from your terminal:

   ```bash
   python exercises/exercise-01-variable-swap.py
   ```

5. Compare what you got to the **Expected output** section on the page,
   character for character. Columns and spacing count.
6. Work through the **Acceptance checklist** at the bottom before you
   move on.
7. If you installed `mypy`, run it on your finished file:

   ```bash
   mypy exercises/exercise-01-variable-swap.py
   ```

   Aim for `Success: no issues found`.

## The Exercises

| # | Exercise | Topic | Difficulty | Est. time |
|---|----------|-------|------------|----------:|
| 1 | [exercise-01-variable-swap.md](./exercise-01-variable-swap.md) | Tuple unpacking, multiple assignment | Easy | 15 min |
| 2 | [exercise-02-string-formatter.md](./exercise-02-string-formatter.md) | f-strings, alignment, format specs | Easy | 25 min |
| 3 | [exercise-03-temperature-converter.md](./exercise-03-temperature-converter.md) | Functions, type hints, arithmetic | Medium | 30 min |
| 4 | [exercise-04-input-parsing.md](./exercise-04-input-parsing.md) | `input()`, casting, error handling | Medium | 30 min |

Exercises 3 and 4 feed directly into Friday's
[mini-project](../mini-project/README.md): the three conversion functions
and the `read_int()` helper are reused there without changes. Getting
them right this week is work you do not repeat.

## A Note on Style

Every exercise expects you to:

- Use `snake_case` for variables and functions.
- Add a docstring to each function you write.
- Use type hints on function parameters and return values.
- Avoid magic numbers — name constants with `UPPER_SNAKE_CASE`.

If you finish all four and want more practice, move on to the
[challenges](../challenges/README.md).
