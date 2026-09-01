# Week 5 — Homework

Six problems, one page each, to consolidate everything this week taught you
about lists, sets, dicts and comprehensions. Five of the six are the same move
in a different costume: **something you would otherwise go looking for becomes a
key you can look up.** Problem 1 is the exception, and it is about the shape of
your data rather than about finding things in it.

Each page carries the brief, a starter you can paste and run, the answer with an
explanation, and a file you can download to compare against. Read the answer
*after* you have written something and run it. The gap between "this should
work" and "why does it print that" is where the learning happens, and reading
first closes it for free.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the function takes and
   what it gives back before you type anything.
2. Copy the Starter into your own `homework/week-05-solutions.py`. That one file
   holds all six functions — see *What you hand in* below. The `-solution.py`
   file beside each page is the published answer, and it is named differently on
   purpose so the two never land on top of each other.
3. Fill in the `TODO` markers one at a time. Run the file after each one.
4. Compare your output with the Expected output block, character for character.
5. Only then read The Solution and *Why it works*.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [Matrix transpose (with a comprehension)](./problem-01-matrix-transpose-with-a-comprehension.md) | Reading a nested comprehension from the outside in | Easy | 30 min |
| 2 | [Invert a dictionary](./problem-02-invert-a-dictionary.md) | A dict comprehension, and what "hashable and unique" is protecting you from | Easy | 25 min |
| 3 | [Two-Sum (classic)](./problem-03-two-sum-classic.md) | Replacing a loop inside a loop with one dict lookup | Medium | 45 min |
| 4 | [Find duplicates](./problem-04-find-duplicates.md) | Counting with a dict, and spotting a scan hidden inside a loop | Easy | 30 min |
| 5 | [Group by first letter](./problem-05-group-by-first-letter.md) | `setdefault`, a dict of lists, and aliasing used on purpose | Medium | 35 min |
| 6 | [Intersect dictionaries](./problem-06-intersect-dictionaries.md) | Membership tests on keys, and the set algebra inside `.keys()` | Medium | 35 min |

Total target time: about 3 hours 20 minutes. The
[week schedule](../README.md#suggested-schedule-36-hours) budgets a shorter
block for homework, and both numbers are honest — the figures here are how long
each problem takes when it goes well, and the schedule assumes you have already
done the exercises and challenges, which cover a lot of the same ground.

## What you hand in

One file: `homework/week-05-solutions.py` in your fork, holding all six
functions.

```text
homework/
    week-05-solutions.py
```

That is different from Week 4, where each problem got its own file. Here the six
functions are small, none of them imports another, and keeping them together
means one command runs every assert you have written:

```bash
python homework/week-05-solutions.py
```

Silence, or your own summary line, means every assert passed. `assert` says
nothing when it is happy.

The `-solution.py` files beside the problem pages are the published answers.
They are named after their page rather than after your file so the two can never
collide, and so a download says what it is.

Commit with `feat(week-05): homework problems`. If you are working in a cohort,
open a pull request.

## Submission checklist

From the original assignment, and still exactly what a reviewer looks for:

- [ ] All six functions implemented and runnable.
- [ ] All required asserts pass — at least three per problem.
- [ ] Type hints on every function signature.
- [ ] A docstring on every function.
- [ ] No bare `except:` blocks.
- [ ] No global state — pure functions only.
- [ ] The file runs without errors: `python homework/week-05-solutions.py`.

One nuance on "pure". `group_by_first_letter` in Problem 5 mutates a list, and
so does the stretch version of `invert` in Problem 2 — but only objects they
built themselves, and never their arguments. That is still pure from the
caller's point of view, which is the property the checklist is really asking
about. Contrast it with the mini-project's operation functions, which change the
caller's list on purpose; there, the mutation *is* the contract.

## Checking your work

Every problem page ends with an acceptance checklist. Work down it before you
call a problem done. If your output differs from the page's Expected output, the
difference is the bug — read it rather than guessing.

Three habits worth building while the problems are this small:

- **Test with something that is not symmetrical.** Problem 1's classic bug gives
  the right answer on every square matrix. Problem 3's gives the right answer on
  every list whose answer does not involve position `0`. Both hide from a
  careless test and neither hides from a deliberate one.
- **Write down the behaviour you did not want.** `invert({"a": 1, "b": 1})`
  loses a pair. Asserting that it does turns a surprise into a decision.
- **Read the squiggle in a traceback.** Python 3.11 and later underline the
  exact sub-expression that failed, which usually tells you which of two
  similar-looking things was the problem.

When all seven boxes above are ticked you are ready for the week's capstone, the
[Contact Book Manager](../mini-project/README.md), and after that for
**Week 6 — File I/O & Exceptions**.
