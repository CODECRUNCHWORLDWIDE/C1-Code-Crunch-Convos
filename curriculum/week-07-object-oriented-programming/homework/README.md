# Week 7 — Homework

Six problems, one page each. This is the week your programs stop being
loose collections of functions and start being **objects** — things that
own their state, guard it, and answer for it. Every problem here hands
you a small design decision that no syntax rule can make for you.

Each page carries the brief, a starter you can paste and run, the answer
with an explanation, and a file you can download to compare against.
Read the answer *after* you have written something and run it — the gap
between "this should work" and "why does it print that" is where the
learning happens, and reading first closes it for free.

Do **at least four** of the six. All six are answered, so whichever four
you pick, you can check your work — but the two you skip are the two you
should read anyway, because each one carries a design move the others do
not.

## The one move behind all six

The six look unrelated. They are the same move, six times: **put each
fact in exactly one place, and derive everything else from it.**

| # | The fact, stored once | What is derived from it |
|---|---|---|
| 1 | the balance, moved only through `deposit` | the history, the validation, and interest as just another credit |
| 2 | the promise (`area`, `perimeter`), declared once in the ABC | every shape kept honest before it can even be built |
| 3 | the list, hidden inside the `Stack` | an API that can only push and pop — no `sort()`, no `insert(0, x)` |
| 4 | the field names, written once as annotations | `__init__`, `to_dict`, `from_dict` and `__repr__`, for every subclass |
| 5 | the observer list, owned by `Subject` | anything callable can listen, and nothing has to inherit |
| 6 | one number, `_meters` | four other units that can never disagree with it |

When a design decision in any of these feels arbitrary, ask which option
leaves one copy of the fact. That question answers it more often than
any rule about inheritance.

## How to work a problem

1. Read The Brief and the Requirements. Say out loud what the class owns
   and what it promises before you type anything.
2. Copy the Starter into a file of your own. The page names it — for
   problem 1 that is `savings_account.py`, not the `-solution.py` file,
   which is the finished answer.
3. Fill in the `TODO` markers one at a time. Run it after each one.
4. Compare your output with the Expected output block, character for
   character.
5. Only then read The Solution and the why-it-works notes under it.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [`BankAccount` with interest](./problem-01-bankaccount-with-interest.md) | Subclassing a class that guards its own state, and rounding money on purpose | Beginner | 45 min |
| 2 | [Polygon hierarchy](./problem-02-polygon-hierarchy.md) | Abstract base classes — making "you must implement this" a real rule | Intermediate | 1 hr |
| 3 | [`Stack` built on a list](./problem-03-stack-built-on-a-list.md) | Composition over inheritance, then putting the stack to work | Intermediate | 50 min |
| 4 | [Simple ORM-like model](./problem-04-simple-orm-like-model.md) | Reading annotations to write the boilerplate machine yourself | Advanced | 1 hr 15 min |
| 5 | [Observer pattern (light)](./problem-05-observer-pattern-light.md) | A subject that calls whoever is listening — your first design pattern | Intermediate | 1 hr |
| 6 | [Unit-conversion class](./problem-06-unit-conversion-class.md) | Property pairs over one stored fact, and operators that refuse politely | Intermediate | 1 hr |

Total target time: about 5 hours 50 minutes for all six, and the
[week schedule](../README.md) budgets a shorter block because it expects
four. Both numbers are honest — the figures here are how long each
problem takes when it goes well, and several of these are the kind where
the first attempt teaches you what the second attempt should have been.

## What you hand in

Your own `homework/` folder should end up holding the files you wrote —
at least four of:

```text
homework/
    savings_account.py
    polygons.py
    stack.py
    models.py
    events.py
    length.py
```

Those are *your* files. The `-solution.py` files on the problem pages
are the published answers, and they are named differently on purpose so
that the two never land on top of each other.

Each one must be runnable as `python <name>.py` and must carry a module
docstring saying what it does, with an example invocation. Type hints on
every signature. No global state apart from the demo in `main()`.

Each problem is graded on three things, in this order:

1. **Correctness** — runs without errors; output matches the page's
   Expected output exactly.
2. **Design** — sensible attribute and method choices; facts stored
   once; good naming.
3. **Style** — type hints, docstrings, PEP 8. Your editor's
   auto-formatter (`black` or similar) is your friend.

Due before you start Week 8. Commit with
`feat(week-07): homework problems`. If you are working in a cohort, open
a pull request.

## Checking your work

Every problem page ends with an acceptance checklist. Work down it
before you call a problem done. If your output differs from the page's
Expected output, the difference is the bug — read it rather than
guessing.

Two habits are worth carrying out of this week, and you can check both
by looking rather than running: **not one of these six answers reaches
into another object's underscore attribute from outside its class, and
not one of them stores a fact it could derive.** Neither was a rule
imposed from outside. Both fell out of asking, at each design decision,
which option leaves one copy of the fact.

Then it is on to the [mini-project](../mini-project/README.md), which
uses all of it at once.
