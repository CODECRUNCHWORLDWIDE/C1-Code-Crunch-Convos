# Homework Problem 4 — Grade Letter Assigner (No `if`)

> **Topic:** `bool` as a kind of `int`, adding comparisons together, string indexing, and operator precedence
> **Lecture:** [01 — Variables and Built-in Types](../lecture-notes/01-variables-and-types.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** it is the first problem in the course with a genuine *idea* in it rather than a formula. Five outcomes, no branching, four lines of code. The trick only works because `True` really is `1` in Python, and once that clicks you have understood something about the language that most people carry around for years as a curiosity instead of a tool.

## The Brief

You are given a percentage score from 0 to 100 and you have to print the
letter grade:

| Score | Letter |
|-------|--------|
| 90–100 | A |
| 80–89.99 | B |
| 70–79.99 | C |
| 60–69.99 | D |
| below 60 | F |

```text
Grade: C
```

**You may not use `if` or `elif`.** Five outcomes and no branching. That
sounds impossible until you notice two things you already know.

**One: a comparison is a value.** Problem 2 established this. `score >= 60`
is `True` or `False` all by itself.

**Two: `True` is `1` and `False` is `0`.** Not "like" 1 and 0 — in Python a
boolean *is* a whole number wearing a different name. So you can add
comparisons together, and the sum tells you **how many of them were true**.

Put the two together. Count how many thresholds the score clears:

```python
index = (score >= 60) + (score >= 70) + (score >= 80) + (score >= 90)
```

A score of 41 clears none, so `index` is 0. A score of 75 clears two, so
`index` is 2. A score of 92 clears all four, so `index` is 4.

Now line the letters up so that the count picks the right one:

```python
letter = "FDCBA"[index]
```

Zero thresholds is `F`, at position 0. Four thresholds is `A`, at position
4. Do the walk for `score = 75` on paper before you go any further, and
convince yourself it prints `C`.

## Starter

Save this as `homework-04-grade-letter.py` and fill in the `TODO`s. It runs
as pasted and prints `Grade: F` for every score:

```python
"""TODO: one line saying what this file does."""

LETTERS: str = "FDCBA"


def main() -> None:
    """Read a percentage score and print its letter grade."""
    score: float = float(input("Enter your score: "))

    index: int = 0  # TODO: add the four comparisons, each in its own brackets
    letter: str = LETTERS[index]

    print(f"Grade: {letter}")


if __name__ == "__main__":
    main()
```

`LETTERS` is a constant rather than a literal in the middle of a line
because the *order of those five characters is the entire mapping*. It
deserves a name and, in real code, a comment explaining that it reads
low-to-high.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/homework/problem-04-grade-letter-assigner-no-if.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The program asks for a score and reads it as a float.
2. It prints one line, exactly `Grade: X`, where `X` is one of `A B C D F`.
3. The letter follows the table in The Brief, boundaries included.
4. There is no `if`, `elif`, `else`, or conditional expression anywhere in
   the part that works out the letter.
5. `main()` is annotated `-> None`, and every variable carries a type hint.

## Constraints

- **No branching in the answer.** No `if`, no `elif`, no
  `"A" if score >= 90 else ...`. (The downloadable file below has exactly
  one `if`, inside the helper that decides whether anybody is at the
  keyboard. It is plumbing so the file can run unattended, and it is not
  part of the answer. `grade_for()` has no branch in it at all.)
- **Put brackets around every comparison.** `(score >= 60) + (score >= 70)`
  and not `score >= 60 + score >= 70`. `+` binds tighter than `>=`, so
  without the brackets Python computes something completely different and
  does not complain. The exact wreckage is in Common bugs to catch.
- **Cast with `float()`, not `int()`.** The table has entries like
  `89.99`, and `int("89.5")` raises before you get anywhere near the
  comparisons.
- **Four comparisons, not five.** There is no threshold for `F`. Scoring
  below 60 clears nothing, which is what index 0 means.
- **`"FDCBA"`, in that order.** Writing the familiar `"ABCDF"` and indexing
  it the same way gives an `A` to somebody who scored 12.

## Expected output

The downloadable file below uses its built-in example score when nobody is
at the keyboard, so the run is the same every time:

```text
$ python problem-04-grade-letter-assigner-no-if.py
Grade: C
```

Run the same program in your own terminal and it has the conversation
instead. Three real sessions:

```text
Enter your score: 92
Grade: A
```

```text
Enter your score: 73
Grade: C
```

```text
Enter your score: 41
Grade: F
```

And the boundaries, which is where a wrong version gives itself away:

| Typed | Printed |
|-------|---------|
| `100` | `Grade: A` |
| `90` | `Grade: A` |
| `80` | `Grade: B` |
| `70` | `Grade: C` |
| `60` | `Grade: D` |
| `59.9` | `Grade: F` |
| `0` | `Grade: F` |

## Steps

1. Activate your Week 2 environment and `cd` into your `homework/` folder.
2. Save the Starter as `homework-04-grade-letter.py`.
3. Run it as pasted. Every score gives `Grade: F`, because `index` is stuck
   at 0.
4. Before you change anything, watch a boolean behave like a number:

   ```bash
   python -c "print(True + True + False, (75 >= 60) + (75 >= 70))"
   ```

   ```text
   2 2
   ```

5. Replace the `0` with the four bracketed comparisons.
6. Run it with `75`. You should get `C`.
7. Run it with all seven values from the boundary table above. Every one has
   to match. If `90` gives you `B`, one of your comparisons says `>` where
   it should say `>=`.
8. Deliberately break it: remove the brackets from the four comparisons and
   run it with `75` again. It prints `F`, and nothing warns you. Put them
   back, and remember what that failure looked like.
9. Commit: `git add homework-04-grade-letter.py` then
   `git commit -m "Add grade letter assigner without if"`.

## The Solution

```python
"""Grade-letter assigner with no ``if`` statement in the answer.

Week 2 homework, problem 4, Code Crunch Convos. Counts how many thresholds
the score clears and uses that count to index a string of letters.

The question goes to the error stream and the grade goes to the normal
output stream. When nobody is at the keyboard the script uses the example
score. Save your own copy as ``homework-04-grade-letter.py``.
"""

import sys

LETTERS: str = "FDCBA"

SAMPLE_SCORE: str = "73"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def grade_for(score: float) -> str:
    """Return the letter grade for ``score`` without branching."""
    index: int = (
        (score >= 60) + (score >= 70) + (score >= 80) + (score >= 90)
    )
    return LETTERS[index]


def main() -> None:
    """Read a percentage score and print its letter grade."""
    score: float = float(ask("Enter your score: ", SAMPLE_SCORE))
    print(f"Grade: {grade_for(score)}")


if __name__ == "__main__":
    main()
```

**Why it works.**

Walk `score = 75` one comparison at a time:

| Comparison | Value | As a number |
|------------|-------|------------:|
| `75 >= 60` | `True` | 1 |
| `75 >= 70` | `True` | 1 |
| `75 >= 80` | `False` | 0 |
| `75 >= 90` | `False` | 0 |
| **Sum** | | **2** |

`"FDCBA"[2]` is `"C"`. Correct.

**`bool` is a subclass of `int`.** That is not a trick, it is the language
definition. `True == 1`, `False == 0`, and `True + True` is `2`. Adding four
comparisons counts how many thresholds the score cleared, which is always a
number from 0 to 4 — exactly the range of valid positions in a five-letter
string.

**The letters are in ascending order for a reason.** `"FDCBA"` is indexed by
*how many thresholds you passed*. Zero passed is `F`, at position 0. All
four passed is `A`, at position 4. The order of the string *is* the mapping,
which is why it earns a constant name and, in a real program, a comment.

**The boundaries land exactly where the table says.** `score = 90` clears
all four thresholds, so index 4, so `A` — matching "90–100 → A".
`score = 60` clears exactly one, so index 1, so `D`. `score = 59.99` clears
none, so index 0, so `F`. Every band in the table is inclusive at the bottom
and `>=` is inclusive at the bottom, so they agree with no fiddling.

**`float()`, not `int()`.** The brief says the score is a float, and the
table has entries like `89.99`. `int("89.5")` raises; `float` accepts both
`92` and `89.5`.

**`grade_for()` is a separate function, and that is not decoration.** It
takes a number and returns a letter, and it neither asks a question nor
prints anything. That means all seven boundary cases can be checked in one
go instead of by typing at a prompt seven times:

```bash
python -c "
LETTERS = 'FDCBA'
def grade_for(score): return LETTERS[(score >= 60) + (score >= 70) + (score >= 80) + (score >= 90)]
print([grade_for(s) for s in (100, 90, 80, 70, 60, 59.9, 0)])
"
```

```text
['A', 'A', 'B', 'C', 'D', 'F', 'F']
```

A function that only computes is a function you can check. That habit starts
paying in Week 11 and never stops. (The function has to be pasted in here
because a filename with hyphens in it cannot be imported — Python module
names follow the same rules as variable names. Name a file `grades.py` if
you ever want to import from it.)

**`ask()` is the one piece the brief did not ask for.** It lets the
downloadable file run with nobody present. `sys.stdin.isatty()` asks whether
there is a real terminal with a person at it; when there is not, `ask()`
hands back the example score rather than hanging on an `input()` that will
never be answered. That single `if` is plumbing. The answer itself —
`grade_for` — has no branch in it.

## Download and run

Download [problem-04-grade-letter-assigner-no-if-solution.py](./problem-04-grade-letter-assigner-no-if-solution.py)
and run it:

```bash
python problem-04-grade-letter-assigner-no-if-solution.py
```

Run from a terminal, it asks you for a score. Run by a script or with its
input redirected, it grades the example score instead of hanging. Save your
own copy as `homework-04-grade-letter.py` in your homework folder, and
commit that.

## Common bugs to catch

- **You indexed with a single comparison.**

  ```python
  letter = "FDCBA"[score >= 60]     # score = 75
  ```

  prints `D`, with no error at all. `True` is `1`, so every passing score
  gets index 1 and every failing score gets index 0. It is a two-letter
  grading scale in a five-letter costume. You need the *sum* of four
  comparisons.
- **You dropped the brackets.**

  ```python
  index = score >= 60 + score >= 70 + score >= 80 + score >= 90
  ```

  `+` binds tighter than `>=`, so Python works out `60 + score` first and
  then chains the whole thing as one long comparison. For `score = 75` that
  ends up asking `75 >= 135`, which is `False`, and `"FDCBA"[False]` is
  `"F"`. Every score fails, and nothing raises. Bracket every comparison.
- **You cast with `int()`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(int("92.5"))
            ~~~^^^^^^^^
  ValueError: invalid literal for int() with base 10: '92.5'
  ```

  `int()` parses whole-number text only. `int(float("92.5"))` is the
  two-step version if you genuinely want truncation, but here you want the
  float.
- **You wrote the letters as `"ABCDF"`.** A score of 12 then prints `A`. The
  string has to run from the worst grade to the best, because the index
  counts upward from zero thresholds.
- **You used `>` instead of `>=`.** A score of exactly `90` then prints `B`.
  Boundaries are where grading disputes come from; test all four.
- **You assumed out-of-range input is handled.** `150` clears all four
  thresholds and prints `A`. `-20` prints `F`. Nothing crashes and nothing
  warns. If that bothers you, hold the thought — Week 3's `if` is the right
  tool, and coming back to rewrite this is a genuinely good exercise.
- **`IndexError: string index out of range`.** You added a fifth comparison,
  so the count can reach 5 and `"FDCBA"` only has positions 0 to 4. Four
  thresholds, five letters.

## Under the hood

<details>
<summary>Under the hood — why True really is 1, and where else that shows up</summary>

Python did not have a boolean type until version 2.3. Before that, truth was
just integers, and a great deal of existing code relied on `1` and `0`
behaving as true and false. When `bool` was finally added, PEP 285 chose to
make it a *subclass* of `int` so none of that code broke.

```bash
python -c "print(bool.__mro__)"
```

```text
(<class 'bool'>, <class 'int'>, <class 'object'>)
```

`bool` inherits from `int`, which inherits from `object`. A `True` is an
`int` in every way that matters; the only difference is `__str__` and
`__repr__`, which print `True` instead of `1`.

That inheritance is why all of this works:

```bash
python -c "print(True + True, True * 5, sum([True, False, True]), [10, 20][True])"
```

```text
2 5 2 20
```

The `sum()` one is the everyday version of this problem's trick: to count
how many items in a list satisfy a condition, sum the comparisons.

Two cautions:

- **`True is 1` is `False`.** `==` compares values; `is` compares identity,
  and they are different objects. Use `is` only for `None`, `True` and
  `False` themselves.
- **Do not go looking for places to use this.** The trick is right here
  because branching is banned and the mapping is genuinely a count. In a
  normal program with `if` available, `if`/`elif` is clearer, and clearer
  wins. The reason to learn the trick is to understand booleans, not to
  write clever code.

Python also treats many non-boolean values as true or false in a boolean
context: `0`, `0.0`, `""`, `[]`, `{}` and `None` are all falsy, and almost
everything else is truthy. That is a related idea and a separate one — those
values are *treated as* false, whereas `False` genuinely *is* zero.

</details>

<details>
<summary>Under the hood — precedence, and why the bracketless version fails silently</summary>

Python's operators have a fixed pecking order. From tighter to looser, the
part that matters here:

| Tightness | Operators |
|-----------|-----------|
| tightest | `**` |
| | unary `-` |
| | `*` `/` `//` `%` |
| | `+` `-` |
| | comparisons: `<` `<=` `>` `>=` `==` `!=` |
| | `not` |
| | `and` |
| loosest | `or` |

Arithmetic binds tighter than comparison. So in

```python
score >= 60 + score >= 70 + score >= 80 + score >= 90
```

Python first does all the addition, turning it into

```python
score >= (60 + score) >= (70 + score) >= (80 + score) >= 90
```

and *then* treats it as a chained comparison, which is `and`ed together
left to right. For `score = 75` the first link is `75 >= 135`, which is
`False`, so the chain short-circuits and the whole thing is `False`. Then
`"FDCBA"[False]` is `"FDCBA"[0]`, which is `"F"`.

Every score prints `F`. No exception, no warning, no clue. This is the
purest example in the whole week of why "it ran" is not the same as "it is
right".

You can watch Python's reading of it directly:

```bash
python -c "import ast; print(ast.dump(ast.parse('a >= 60 + a >= 70', mode='eval'), indent=1)[:120])"
```

The parse tree shows one `Compare` node with the additions already folded
into its operands. Brackets change the tree, which changes the answer.

</details>

## Acceptance checklist

- [ ] Running the file asks for a score and prints exactly one line.
- [ ] The line reads `Grade: X` with one of `A B C D F`.
- [ ] All seven values in the boundary table produce the letter shown.
- [ ] There is no `if`, `elif`, `else` or conditional expression in the part
      that works out the letter.
- [ ] Every comparison is in its own brackets.
- [ ] The score is cast with `float()`, and `89.5` is accepted.
- [ ] `LETTERS` is a named constant spelled `"FDCBA"`.
- [ ] `main()` is annotated `-> None` and every variable carries a type
      hint.
- [ ] Committed with a message like `Add grade letter assigner without if`.

## Stretch

- Add plus and minus grades — `B+`, `B`, `B-` — with the same technique.
  You will need more thresholds and a longer mapping, and you will discover
  the point at which the trick stops being clearer than a branch. Finding
  that point is the exercise.
- Print the grade point as well: `A` is 4.0, `B` is 3.0, down to `F` at
  0.0. Look at your `index` before you write any arithmetic — it is already
  the answer. Print it with `:.1f` and no conversion at all, and think about
  why the two scales happen to line up.
- Handle the out-of-range case without an `if`. `min(max(score, 0), 100)`
  clamps the score into the table's range before you grade it. Decide
  whether silently clamping is honest, or whether refusing is better, and
  write your reasoning in the commit message.
- Come back after Week 3 and rewrite it with `if`/`elif`. Put the two files
  side by side. The branch version is longer and almost everybody finds it
  easier to read, and understanding *why* is worth more than either version.
- Read PEP 285 at <https://peps.python.org/pep-0285/>, the proposal that
  added `bool` to Python. It is short, it is readable, and it explains the
  subclass decision that this whole problem rests on.

Next: [Homework Problem 5 — Compound Interest](./problem-05-compound-interest.md).
