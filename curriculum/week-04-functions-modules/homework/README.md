# Week 4 — Homework

Six problems, one page each. This is the week functions stop being something you
read about and start being the thing you build with, so every problem here asks
you to write one, name it well, and hand it something to do.

Each page carries the brief, a starter you can paste and run, the answer with an
explanation, and a file you can download to compare against. Read the answer
*after* you have written something and run it — the gap between "this should
work" and "why does it print that" is where the learning happens, and reading
first closes it for free.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the function takes and
   what it gives back before you type anything.
2. Copy the Starter into a file of your own. The page names it — for problem 1
   that is `temperature.py`. Copy the Starter, not the worked answer on the
   page, which is the finished version.
3. Fill in the `TODO` markers one at a time. Run it after each one.
4. Compare your output with the Expected output block, character for character.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Temperature module](./problem-01-temperature-module.md) | Writing a module of related functions, then importing it | Easy | 45 min |
| 2 | [Password strength](./problem-02-password-strength.md) | Returning a verdict rather than printing one | Easy | 40 min |
| 3 | [Leap year function with tests](./problem-03-leap-year-function-with-tests.md) | A function plus the asserts that prove it | Easy | 40 min |
| 4 | [Recursive sum](./problem-04-recursive-sum.md) | A base case and a step that shrinks the problem | Medium | 45 min |
| 5 | [Dict builder](./problem-05-dict-builder.md) | Building and returning a dictionary from arguments | Medium | 45 min |
| 6 | [Importing from a custom module](./problem-06-importing-from-a-custom-module.md) | Two files, one importing the other | Medium | 1 hr |

Total target time: about 4 hours 15 minutes. The [week schedule](../README.md)
budgets a longer block, and both numbers are honest — the figures here are how
long each problem takes when it goes well, and the schedule leaves room for
getting stuck, reading back over the lecture, and committing your work.

## What you hand in

Your own `homework/` folder should end up holding the seven files you wrote:

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

Those are *your* files. The published answers stay on the problem pages
themselves, so nothing you write can be overwritten by an answer and nothing
you hand in can be mistaken for one.

Commit with `feat(week-04): homework problems`. If you are working in a cohort,
open a pull request.

## Grading guide (out of 60)

| Problem | Points |
|---------|-------:|
| 1 | 10 |
| 2 | 10 |
| 3 | 10 |
| 4 | 10 |
| 5 | 10 |
| 6 | 10 |

You lose 1 point per missing docstring, 1 point per missing type hint, and 2
points for any function longer than 25 lines. That last one is not a style
preference — a function you cannot see all of at once is a function you cannot
reason about, and Week 4 is where that habit is cheapest to build.

## Checking your work

Every problem page ends with an acceptance checklist. Work down it before you
call a problem done. If your output differs from the page's Expected output,
the difference is the bug — read it rather than guessing.
