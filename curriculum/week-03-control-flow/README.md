# Week 3 — Control Flow: Conditionals & Loops

Welcome back to **Code Crunch Convos**. So far you have installed Python,
written tiny scripts, and learned how variables, types, and operators work.
This week we add the missing ingredient that turns those linear scripts into
*real programs*: **control flow**. Control flow is how your code decides what
to do next — whether to run a block, skip it, or repeat it. You will learn
the two pillars of control flow in Python: **conditionals** (`if`, `elif`,
`else`) and **loops** (`while`, `for`). By Sunday night you will have built a
classic number-guessing game from scratch, complete with a replay loop and an
attempt counter. We will keep the tone friendly and the examples concrete, so
don't worry if a few ideas take a moment to click — that is normal, and the
exercises are designed to drill them in.

## Learning Objectives

By the end of this week, you will be able to:

- **Write** `if`, `elif`, and `else` chains that branch on any boolean
  expression.
- **Predict** the *truthiness* of any Python value (numbers, strings, lists,
  `None`) without running the code.
- **Combine** comparison operators (`<`, `<=`, `==`, `!=`, `>=`, `>`) and
  logical operators (`and`, `or`, `not`) into clear conditions.
- **Use** chained comparisons such as `0 < x < 10` and conditional
  expressions (the ternary `x if cond else y`).
- **Write** `while` loops with a clear termination condition and avoid
  accidental infinite loops.
- **Iterate** with `for` loops over strings, lists, and `range(...)` objects.
- **Apply** `enumerate()` and `zip()` to iterate with indices or in parallel.
- **Control** loops with `break`, `continue`, and the often-missed `else`
  clause on `for` and `while`.
- **Recognize** and write the common loop patterns: counting, accumulating,
  searching, filtering, and max/min finding.
- **Refactor** nested `if` statements into early-return / guard-clause style
  for readability.
- **Build** a complete interactive command-line program — a number-guessing
  game — using everything above.

## Prerequisites

You should have completed **Week 1** (Python installed, terminal basics, Git)
and **Week 2** (variables, numeric and string types, operators, `input()`,
`print()`, `type()`, type conversion with `int()`, `float()`, `str()`). If
any of those feel shaky, revisit the relevant lecture notes before you
start — control flow assumes you can already store a value in a variable and
compare it to another.

## Topics Covered

- `if`, `elif`, and `else` statements and their indentation rules
- Truthiness: which values are falsy (`0`, `0.0`, `""`, `[]`, `{}`, `None`,
  `False`) and which are truthy (everything else, basically)
- Review of comparison operators and the logical operators `and`, `or`, `not`
- Chained comparisons (`0 < x < 100`) and short-circuit evaluation
- Conditional expressions: the ternary `value_if_true if cond else
  value_if_false`
- `while` loops and the dreaded accidental infinite loop
- `for` loops, `range(start, stop, step)` semantics, and iterating over
  strings, lists, and other iterables
- Iteration helpers: `enumerate()` for index + value, `zip()` for parallel
  iteration (preview — we go deeper in Week 5)
- `break` to exit a loop early and `continue` to skip to the next iteration
- The `else` clause on loops (runs only if the loop was *not* broken out of)
- Nested loops and how their iteration counts multiply
- Common loop patterns: counting, accumulating, max/min, filtering,
  searching with `break`
- Early-return and guard-clause patterns to flatten deeply nested code

## Weekly Schedule

The schedule below adds up to approximately **36 hours**. Treat it as a
target, not a contract — some sections will click faster, others slower.

| Day       | Focus                                       | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----------|---------------------------------------------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday    | `if`/`elif`/`else` & truthiness             |   2h     |    2h     |    0h      |    0.5h   |   1h     |     0h       |    0.5h    |    6h       |
| Tuesday   | `while` loops & guard clauses               |   2h     |    2h     |    0h      |    0.5h   |   1h     |     0h       |    0.5h    |    6h       |
| Wednesday | `for` loops, `range`, `enumerate`, `zip`    |   2h     |    2h     |    1h      |    0.5h   |   1h     |     0h       |    0h      |    6.5h     |
| Thursday  | Loop patterns & `break`/`continue`/`else`   |   1h     |    1h     |    1h      |    0.5h   |   1h     |     1h       |    0.5h    |    6h       |
| Friday    | Nested loops & refactoring                  |   1h     |    1h     |    1h      |    0.5h   |   1h     |     1h       |    0.5h    |    6h       |
| Saturday  | Mini-project deep work                      |   0h     |    0h     |    0h      |    0h     |   0h     |     3h       |    0.5h    |    3.5h     |
| Sunday    | Quiz, review, polish                        |   0h     |    0h     |    0h      |    1h     |   1h     |     0h       |    0h      |    2h       |
| **Total** |                                             | **8h**   | **8h**    |   **3h**   |   **3.5h**|  **6h**  |    **5h**    |   **2.5h** |  **36h**    |

## How to Navigate This Week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview (you are here) |
| [resources.md](./resources.md) | Curated readings, docs links, and articles |
| [lecture-notes/01-conditionals.md](./lecture-notes/01-conditionals.md) | `if`/`elif`/`else`, truthiness, ternary, guard clauses |
| [lecture-notes/02-loops.md](./lecture-notes/02-loops.md) | `while`, `for`, `range`, `enumerate`, `zip`, `break`/`continue`/`else` |
| [lecture-notes/03-loop-patterns.md](./lecture-notes/03-loop-patterns.md) | Counting, accumulating, searching, performance hints |
| [exercises/README.md](./exercises/README.md) | Index of short coding exercises |
| [exercises/exercise-01-fizzbuzz.py](./exercises/exercise-01-fizzbuzz.py) | Classic FizzBuzz from 1 to 100 |
| [exercises/exercise-02-sum-evens.py](./exercises/exercise-02-sum-evens.py) | Sum even numbers from 1 to N |
| [exercises/exercise-03-password-checker.py](./exercises/exercise-03-password-checker.py) | Loop until the password meets the rules |
| [exercises/exercise-04-multiplication-table.py](./exercises/exercise-04-multiplication-table.py) | Print an N×N multiplication table |
| [exercises/exercise-05-find-prime.py](./exercises/exercise-05-find-prime.py) | Decide whether a number is prime |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-caesar-cipher.md](./challenges/challenge-01-caesar-cipher.md) | Build a Caesar shift cipher |
| [challenges/challenge-02-rps.md](./challenges/challenge-02-rps.md) | Rock-paper-scissors with score tracking |
| [quiz.md](./quiz.md) | 10 multiple-choice questions |
| [homework.md](./homework.md) | Six practice problems for the week |
| [mini-project/README.md](./mini-project/README.md) | Full spec for the number-guessing game |
| [mini-project/starter.py](./mini-project/starter.py) | Starter file for the mini-project |

## Stretch Goals

If you finish early and want to push further, try any of the following:

- **FizzBuzz with twists**: extend the classic FizzBuzz to also print
  `"Bang"` for multiples of 7 and `"FizzBuzzBang"` for multiples of 3, 5,
  and 7. Then make the divisors and labels configurable at the top of the
  file.
- **Caesar cipher upgrade**: after finishing
  [challenge-01-caesar-cipher.md](./challenges/challenge-01-caesar-cipher.md),
  add support for *any* shift (including negative), preserve case, and leave
  punctuation untouched.
- **Multi-round number-guessing**: add a "best score" tracker that persists
  across replays within a single run, and a hint system ("you're getting
  warmer/colder").
- Read the official Python tutorial section on control flow end-to-end at
  <https://docs.python.org/3/tutorial/controlflow.html> and try every
  example in the REPL.

## Up Next

When the number-guessing game runs cleanly and your homework is committed,
continue to [Week 4 — Functions & Modules](../week-04-functions-modules/README.md).
Functions are how we package the control flow you just learned into reusable
named blocks — they are the next big jump in expressive power.
