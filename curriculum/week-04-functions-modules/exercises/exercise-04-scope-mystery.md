# Exercise 4 — Scope Mystery

> **Topic:** Finding and fixing five bugs caused by scope confusion
> **Lecture:** [02 — `*args`, `**kwargs`, and Scope](../lecture-notes/02-args-kwargs-and-scope.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** the other exercises ask you to write code. This one asks you to read somebody else's, which is what you will spend far more of your life doing. Scope bugs produce either a baffling error message or, worse, a quietly wrong number. Two of the five here throw nothing at all — the self-checks are the only reason you ever find them. Learning to distrust a program that appears to work is the whole point.

## The Brief

**Scope** is the answer to one question: when Python sees a name, where does
it go looking for it?

Think of a set of nested boxes. Inside a function, Python looks in that
function's own box first. If the name is not there it looks in the box around
it, then the box around that, and finally in the outermost box of built-in
names like `sum` and `print`. The first box that has the name wins, and the
search stops there. That order has a nickname, **LEGB** — Local, Enclosing,
Global, Builtins — and every bug on this page is that search going somewhere
you did not expect.

The starter below is a real-ish module: the neighborhood cleanup day sign-in
sheet. Somebody wrote it in a hurry and it has **five** bugs, every one of
them about scope in some way. Nothing else is wrong with the file. The
arithmetic is correct, the data is correct, and the self-checks at the bottom
are correct. Only the five bugs stand between you and a clean run.

This is a debugging exercise, not a rewrite. Run the file. Read the first
error. Fix exactly one thing. Run it again. That loop is the job, and it is
the job for the rest of your career.

Two of the five bugs raise `UnboundLocalError`, one raises `TypeError`, and
two raise nothing whatsoever — they just produce wrong answers that only the
asserts catch. When you finish, write one sentence per bug at the top of your
file naming which rule it broke. If you cannot name the rule, you patched the
symptom.

## Starter

Create `exercise-04-scope-mystery.py` in your practice repo and paste this in
**exactly as written**. It is broken on purpose.

```python
"""exercise-04-scope-mystery.py — five scope bugs. Fix them all.

BROKEN ON PURPOSE. Run the file, read the first traceback, fix one bug,
run it again. Repeat until the self-checks print "All checks passed."

Do not rewrite the file from scratch. Find the five bugs that are in it.
"""

VOLUNTEERS_SIGNED_UP = 0
BAGS_PER_VOLUNTEER = 3
METERS_PER_VOLUNTEER = 40

# Someone left a running total up here months ago and never took it out.
sum = 0


def sign_up(name: str, roster: list[str] = []) -> list[str]:
    """Add `name` to `roster` and return the roster."""
    roster.append(name)
    VOLUNTEERS_SIGNED_UP = VOLUNTEERS_SIGNED_UP + 1
    return roster


def bags_for_crew(crew_size: int) -> int:
    """Return how many trash bags a crew of `crew_size` needs."""
    per_person = [BAGS_PER_VOLUNTEER] * crew_size
    return sum(per_person)


def street_totals(counts: dict[str, int]) -> dict[str, int]:
    """Return a running total of bags collected, street by street."""
    running = 0

    def add(bags: int) -> int:
        """Add `bags` to the running total and return the new total."""
        running += bags
        return running

    return {street: add(bags) for street, bags in counts.items()}


def crew_capacity(crew_size: int) -> int:
    """Return how many meters of curb a crew of `crew_size` can clear."""
    return METERS_PER_VOLUNTEER * VOLUNTEERS_SIGNED_UP


if __name__ == "__main__":
    first = sign_up("Rosa")
    second = sign_up("Ken")
    assert first == ["Rosa"], first
    assert second == ["Ken"], second
    assert VOLUNTEERS_SIGNED_UP == 2, VOLUNTEERS_SIGNED_UP

    assert bags_for_crew(4) == 12, bags_for_crew(4)
    assert bags_for_crew(0) == 0, bags_for_crew(0)

    totals = street_totals({"Cedar Street": 5, "Mill Road": 3, "Front Street": 2})
    assert totals == {"Cedar Street": 5, "Mill Road": 8, "Front Street": 10}, totals

    assert crew_capacity(3) == 120, crew_capacity(3)
    assert crew_capacity(0) == 0, crew_capacity(0)

    print(f"{VOLUNTEERS_SIGNED_UP} volunteers signed up.")
    print(f"Bags for a crew of 4: {bags_for_crew(4)}")
    print(f"Street totals: {totals}")
    print(f"A crew of 3 clears {crew_capacity(3)} m of curb.")
    print("All checks passed.")
```

Four words you need before you start.

**Local.** A name that belongs to one call of one function and disappears
when that call ends.

**Global.** In Python this means "at the top level of this file", not
"everywhere in the universe". `VOLUNTEERS_SIGNED_UP` is a global.

**Shadowing.** Using a name that already means something else, so your
version hides the original for as long as yours is in scope. That is what
`sum = 0` does to the built-in `sum`.

**Closure.** A function defined inside another function, which can see the
outer function's variables. `add` inside `street_totals` is one.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/exercises/exercise-04-scope-mystery.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Do not change the `if __name__ == "__main__":` block. It is the
   specification. If a check fails, the function is wrong, not the check.
2. Do not change the constants `BAGS_PER_VOLUNTEER` or
   `METERS_PER_VOLUNTEER`, and do not change what any docstring promises.
3. `sign_up` must return a **fresh** list on every call that does not pass a
   roster, and must leave `VOLUNTEERS_SIGNED_UP` at `2` after two calls.
4. `bags_for_crew(4)` must return `12` and `bags_for_crew(0)` must return `0`.
5. `street_totals` must return a running cumulative total per street, in the
   order the input dict gave them.
6. `crew_capacity(3)` must return `120` and `crew_capacity(0)` must return
   `0`. It must depend on its parameter, not on module state.
7. At the top of your fixed file, add a comment block with one line per bug:
   what the symptom was, and which rule caused it.

## Constraints

- **Fix `sign_up`'s counter with an explicit `global VOLUNTEERS_SIGNED_UP`,
  not by renaming.** Lecture 2 calls `global` a code smell and it is one, but
  the checks read that module-level name. Assigning to a fresh local instead
  would make the error message disappear and leave the counter at `0`, which
  the third check catches. Making an error message go away is not the same as
  fixing the error. The Stretch section asks you to design the smell away
  properly.
- **Fix the shadowing bug by deleting the offending line, not by renaming the
  call.** Writing `builtins.sum(per_person)` works and is horrible — it
  leaves the landmine in place for the next person who writes `sum(...)` in
  this file, and now there is a working `builtins.sum` nearby to make them
  doubt themselves. Remove the cause, not the symptom.
- **Fix the closure with `nonlocal`, not with a `global`.** `running` lives
  in the enclosing *function*, not at the top of the file. `global running`
  reaches past the place the variable actually lives, and the damage it does
  is invisible on a single run — see Common bugs.
- **Fix `crew_capacity` by using its parameter.** Do not add a `global`. A
  function that takes an argument and ignores it is lying in its signature,
  and this is exactly the "pure function" argument from
  [Lecture 2, section 9](../lecture-notes/02-args-kwargs-and-scope.md).

## Expected output

Once all five bugs are fixed. Real stdout, captured on CPython 3.13.2:

```text
$ python exercise-04-scope-mystery.py
2 volunteers signed up.
Bags for a crew of 4: 12
Street totals: {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
A crew of 3 clears 120 m of curb.
All checks passed.
```

Read the third line closely. Cedar Street collected 5, Mill Road collected 3,
Front Street collected 2 — and the output shows `5`, `8`, `10`. Those are
running totals, each one adding to the last. If your output repeats the input
numbers back at you, `add` is not accumulating anything.

## Steps

1. Create the file, paste the starter exactly, and run it:
   `python exercise-04-scope-mystery.py`.
2. Read the first traceback. The last four lines are the ones that matter:

   ```text
     File "exercise-04-scope-mystery.py", line 20, in sign_up
       VOLUNTEERS_SIGNED_UP = VOLUNTEERS_SIGNED_UP + 1
                              ^^^^^^^^^^^^^^^^^^^^
   UnboundLocalError: cannot access local variable 'VOLUNTEERS_SIGNED_UP' where it is not associated with a value
   ```

   Look at where the caret is pointing: at the **read**, on the right-hand
   side. And that name has a perfectly good value on line 9 of the same file.
   Before you touch anything, say out loud why.
   [Lecture 2, section 5](../lecture-notes/02-args-kwargs-and-scope.md),
   "Reads vs. writes", has the answer.
3. Fix one bug. Run again. You get a different failure. Keep going. Do not
   fix two at once — the order the file fails in is itself the lesson.
4. When you hit the assert about `first`, stop and look at it properly. The
   check on the *first* roster fails, even though `first` was completely
   correct the moment it was created. Something changed it afterwards. Print
   the identities to confirm what you suspect:

   ```text
   first : ['Rosa', 'Ken'] id: 2541604543168
   second: ['Rosa', 'Ken'] id: 2541604543168
   same object? True
   the default itself: (['Rosa', 'Ken'],)
   ```

   `id()` gives you a number that is unique to one object while it exists. Two
   names, one number, one list. That last line is `sign_up.__defaults__` — the
   default value stored on the function object, which has been growing.
5. When you reach the `crew_capacity` failure, notice that it never raised
   anything. It returned a number, for two whole runs, and only the assert
   caught it. Add your five-line comment block and run one final time.

## The Solution

```python
"""exercise-04-scope-mystery-solution.py — five scope bugs, all five fixed.

Bug 1 (sign_up counter): UnboundLocalError. Assigning to VOLUNTEERS_SIGNED_UP
    anywhere in the body made it local for the whole function, so the read on
    the right-hand side had nothing to read. Rule: assignment decides scope,
    and it decides it for the entire function. Fixed with `global`.
Bug 2 (sign_up roster): no exception, wrong answer. `roster: list[str] = []`
    is evaluated once, at def time, so every call that omitted a roster shared
    one list. Rule: default values are bound at definition, not at call.
    Fixed with the None sentinel.
Bug 3 (module-level `sum = 0`): TypeError, 'int' object is not callable. A
    module-level name hid the built-in for the whole file. Rule: LEGB looks in
    Global before Builtins. Fixed by deleting the line.
Bug 4 (add's running total): UnboundLocalError. `running += bags` is an
    assignment, so `running` was local to `add` and the enclosing function's
    variable was invisible for writing. Rule: `nonlocal` reaches the enclosing
    function scope; `global` would reach past it to the module.
Bug 5 (crew_capacity): no exception, wrong answer. The function read module
    state instead of its own parameter. Rule: a name in the signature is a
    promise; a function that ignores it is not pure and not honest.
"""

VOLUNTEERS_SIGNED_UP = 0
BAGS_PER_VOLUNTEER = 3
METERS_PER_VOLUNTEER = 40


def sign_up(name: str, roster: list[str] | None = None) -> list[str]:
    """Add `name` to `roster` and return the roster."""
    global VOLUNTEERS_SIGNED_UP
    if roster is None:
        roster = []
    roster.append(name)
    VOLUNTEERS_SIGNED_UP = VOLUNTEERS_SIGNED_UP + 1
    return roster


def bags_for_crew(crew_size: int) -> int:
    """Return how many trash bags a crew of `crew_size` needs."""
    per_person = [BAGS_PER_VOLUNTEER] * crew_size
    return sum(per_person)


def street_totals(counts: dict[str, int]) -> dict[str, int]:
    """Return a running total of bags collected, street by street."""
    running = 0

    def add(bags: int) -> int:
        """Add `bags` to the running total and return the new total."""
        nonlocal running
        running += bags
        return running

    return {street: add(bags) for street, bags in counts.items()}


def crew_capacity(crew_size: int) -> int:
    """Return how many meters of curb a crew of `crew_size` can clear."""
    return METERS_PER_VOLUNTEER * crew_size


if __name__ == "__main__":
    first = sign_up("Rosa")
    second = sign_up("Ken")
    assert first == ["Rosa"], first
    assert second == ["Ken"], second
    assert VOLUNTEERS_SIGNED_UP == 2, VOLUNTEERS_SIGNED_UP

    assert bags_for_crew(4) == 12, bags_for_crew(4)
    assert bags_for_crew(0) == 0, bags_for_crew(0)

    totals = street_totals({"Cedar Street": 5, "Mill Road": 3, "Front Street": 2})
    assert totals == {"Cedar Street": 5, "Mill Road": 8, "Front Street": 10}, totals

    assert crew_capacity(3) == 120, crew_capacity(3)
    assert crew_capacity(0) == 0, crew_capacity(0)

    print(f"{VOLUNTEERS_SIGNED_UP} volunteers signed up.")
    print(f"Bags for a crew of 4: {bags_for_crew(4)}")
    print(f"Street totals: {totals}")
    print(f"A crew of 3 clears {crew_capacity(3)} m of curb.")
    print("All checks passed.")
```

Five changes, and they are small. One added `global` line. One changed
default plus its two-line sentinel. One deleted line, along with the stale
comment above it. One added `nonlocal` line. One changed expression. The
`__main__` block is byte-for-byte the starter's.

**Bug 1 — `global VOLUNTEERS_SIGNED_UP`.** Python decides which names in a
function are local when it *compiles* the function, before a single line
runs, and the rule is blunt: **if a name is assigned anywhere in the body, it
is local for the whole body** — including lines that come before the
assignment. `VOLUNTEERS_SIGNED_UP` appears on the left of an `=`, so it is
local, so the read on the right is a read of a local nobody has filled in
yet. `global VOLUNTEERS_SIGNED_UP` on the first line of the body overrides
that decision: reads and writes both go to the module-level name.

**Bug 2 — the `None` sentinel.** `def` is a statement that runs once. The
`[]` in the signature is evaluated at that moment and stored on the function
object, where you saw it in step 4. Every call that omits `roster` gets that
same list, still holding whatever the last caller put in it. The sentinel
works because `None` is immutable — there is nothing to accumulate in — and
because `if roster is None: roster = []` moves the list-making into the body,
which runs once per call. Same fix, same reason, as Exercise 1's `record_fee`.

**Bug 3 — delete the shadow.** `sum` is resolved through LEGB, and the
module-level `sum = 0` sits in **G**, one step before **B**. Python finds the
integer first and never reaches the built-in, so `sum(per_person)` is an
attempt to call the number zero:

```text
module-level sum: 0 <class 'int'>
builtins.sum: <built-in function sum>
```

Both names exist. Only one of them is found.

**Bug 4 — `nonlocal running`.** Exactly the same rule as bug 1, one box
inward. `running += bags` is an assignment, so `running` is local to `add`,
so the read that `+=` implies has nothing to read. But `running` does not
live at module level — it lives in `street_totals`, the enclosing *function*.
That is the **E** in LEGB, and `nonlocal` is the keyword that binds to it.
[Lecture 2, section 7](../lecture-notes/02-args-kwargs-and-scope.md) is the
reference.

**Bug 5 — read the parameter.** Nothing raises. The function returns a
number, for two whole runs, and only the assert catches it. Two volunteers
times forty meters is eighty, which looks like a perfectly plausible number
of meters. `crew_capacity` accepted `crew_size` and then read module state
instead — a signature that lies. The fix is `METERS_PER_VOLUNTEER *
crew_size`, and the deeper point is
[Lecture 2, section 9](../lecture-notes/02-args-kwargs-and-scope.md): a
function whose output depends only on its inputs can be tested, reasoned
about and moved somewhere else. A function that reads module state gives a
different answer depending on what ran before it.

Notice what fixing bug 5 does to the rest of the file. `crew_capacity` no
longer touches `VOLUNTEERS_SIGNED_UP` at all, which is what makes the
stretch — getting rid of `global` entirely — reachable.

## Download and run

Download
[exercise-04-scope-mystery-solution.py](./exercise-04-scope-mystery-solution.py)
and run it:

```bash
python exercise-04-scope-mystery-solution.py
```

It is the fixed version of the file you are debugging, under a name that will
not collide with your own `exercise-04-scope-mystery.py`. Open both side by
side once you are done and diff them by eye.

## Common bugs to catch

These are in the order the file fails. Fixing one reveals the next.

- **First run — `UnboundLocalError` on `VOLUNTEERS_SIGNED_UP`.**

  ```text
  Traceback (most recent call last):
    File "exercise-04-scope-mystery.py", line 48, in <module>
      first = sign_up("Rosa")
    File "exercise-04-scope-mystery.py", line 20, in sign_up
      VOLUNTEERS_SIGNED_UP = VOLUNTEERS_SIGNED_UP + 1
                             ^^^^^^^^^^^^^^^^^^^^
  UnboundLocalError: cannot access local variable 'VOLUNTEERS_SIGNED_UP' where it is not associated with a value
  ```

  Assignment anywhere in a body makes the name local for the entire body.
  Declare `global VOLUNTEERS_SIGNED_UP` on the first line.

  **The tempting wrong fix:** rename the local to `count`. The traceback does
  vanish, and then the third check fails instead, because the module-level
  counter never moved:

  ```text
  ex4 renaming instead of global leaves the counter at 0
  returned: 0
  ```

  A silenced error message is not a fixed error.

- **Second run — `AssertionError: ['Rosa', 'Ken']` on the check for
  `first`.**

  ```text
  Traceback (most recent call last):
      assert first == ["Rosa"], first
             ^^^^^^^^^^^^^^^^^
  AssertionError: ['Rosa', 'Ken']
  ```

  `roster: list[str] = []` evaluated that `[]` once, at `def` time. Both calls
  appended to the same list, so `first` and `second` are two names for one
  object. Switch to `roster: list[str] | None = None` and make the list in
  the body. Step 4 above shows the `id()` proof.

- **Third run — `TypeError: 'int' object is not callable` from
  `bags_for_crew`.**

  ```text
  Traceback (most recent call last):
      assert bags_for_crew(4) == 12, bags_for_crew(4)
             ~~~~~~~~~~~~~^^^
      return sum(per_person)
  TypeError: 'int' object is not callable
  ```

  The module-level `sum = 0` hides the built-in `sum` for the whole file.
  Python found the global before it got to the built-in box — the **G** in
  LEGB comes before the **B**. Delete the line and its stale comment.

  **The tempting wrong fix:** `import builtins` and call
  `builtins.sum(per_person)`. It returns the right answer, which is what
  makes it tempting:

  ```text
  returned: (12, 0)
  ```

  It also leaves `sum = 0` sitting in the module for the next person.

- **Fourth run — `UnboundLocalError` on `running`, raised from `add`.**

  ```text
  Traceback (most recent call last):
      totals = street_totals({"Cedar Street": 5, ...})
      return {street: add(bags) for street, bags in counts.items()}
                      ~~~^^^^^^
      running += bags
      ^^^^^^^
  UnboundLocalError: cannot access local variable 'running' where it is not associated with a value
  ```

  Same rule as the first bug, one box in. `nonlocal running` points it at the
  enclosing function's variable.

  **The tempting wrong fix, part one:** swap in `global running`. On its own
  that does not even get off the ground, because no module-level `running`
  exists:

  ```text
  NameError: name 'running' is not defined
  ```

  **The tempting wrong fix, part two:** satisfy that by hoisting `running =
  0` up to module level. Now it runs, and now it is genuinely worse than the
  bug you started with:

  ```text
  call 1: {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
  call 2: {'Cedar Street': 15, 'Mill Road': 18, 'Front Street': 20}
  ```

  The first call is right and every call after it is wrong, because a
  module-level `running` survives between calls while a function-local one is
  created fresh each time. A single-run test suite never sees this. Test your
  fix by calling the function twice. With `nonlocal`, you get:

  ```text
  {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
  {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
  ```

  **The other tempting wrong fix:** make the `UnboundLocalError` go away by
  not storing anything.

  ```python
      def add(bags: int) -> int:
          return running + bags   # WRONG: nothing accumulates
  ```

  ```text
  AssertionError: {'Cedar Street': 5, 'Mill Road': 3, 'Front Street': 2}
  ```

  The error is gone because there is no longer an assignment, and every
  street now reports its own count instead of a running total. Compare that
  dict against the input dict — they are identical, which is the tell.

- **Fifth run — `AssertionError: 80` on `crew_capacity(3)`.**

  ```text
  Traceback (most recent call last):
      assert crew_capacity(3) == 120, crew_capacity(3)
             ^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: 80
  ```

  No exception, just a wrong number: the function multiplies by the
  module-level volunteer count instead of the `crew_size` it was handed. Two
  volunteers times forty meters is eighty. This bug would have shipped.

- **Editing the `__main__` block.** Whatever the symptom, do not do this. If a
  check fails, the function is wrong. The checks are the specification, which
  is exactly the relationship you will have with a test suite for the rest of
  your career.

## Under the hood

<details>
<summary>Under the hood — LEGB in full, and why assignment decides scope before the code runs</summary>

When Python meets a bare name, it searches four places in a fixed order and
takes the first hit:

| Letter | Scope | What is in it |
| --- | --- | --- |
| **L** | Local | names assigned in the running function |
| **E** | Enclosing | locals of any function this one is nested inside |
| **G** | Global | names at the top level of this module |
| **B** | Builtins | `sum`, `len`, `print`, `int`, and the rest |

Bug 3 is that table, read literally. `sum = 0` at module level sits in **G**,
one step before **B**, so it wins.

**The decision is made at compile time, not while running.** This is the part
that surprises people, and it is what both `UnboundLocalError`s on this page
come from. When Python compiles a function body it scans for assignments and
writes down, once and for all, which names are local. It does not matter
*where* in the body the assignment sits:

```python
x = "module level"

def show():
    print(x)      # <- fails
    x = "local"   # <- because of this line, below it
```

```text
UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
```

The `print(x)` is on the line before the assignment and still fails, because
`x` was classified local for the whole function before either line ran. You
can see the classification in the compiled code:

```text
>>> show.__code__.co_varnames
('x',)
```

`x` is listed as a local variable of `show`, and locals live in a numbered
slot rather than a dictionary lookup — which is *why* the rule exists. Fixed
slots are much faster than searching scopes on every access, and fixed slots
require knowing the list of locals up front.

**`global` and `nonlocal` are compile-time instructions too.** They are not
statements that run. They are notes to the compiler that change which box a
name is filed under for that whole function:

- `global name` — file it in **G**, the module's top level.
- `nonlocal name` — file it in **E**, the nearest enclosing function that
  already has it. If no enclosing function has it, that is a `SyntaxError` at
  compile time, not a runtime error, which is a genuinely useful difference:
  `nonlocal` cannot create a variable out of nothing, so it cannot typo its
  way into a new one.

**Reading is free; writing is what needs a declaration.** `bags_for_crew`
reads `BAGS_PER_VOLUNTEER` from **G** with no ceremony at all, and that is
normal and fine. You only need `global` or `nonlocal` when you want to
*rebind* an outer name — point it at a different object. Note the word
rebind. This works with no declaration whatsoever:

```python
def add_one(roster: list[str]) -> None:
    """Change the list the caller passed. No `global` required."""
    roster.append("Ken")
```

Changing an object's contents is not assignment. Assignment is `name = ...`,
which points a name at a different object, and that is the only thing scope
declarations are about.

**Why `global` is a smell and `nonlocal` is not, quite.** A `global` write
means any function anywhere in the file might have changed that value, so to
predict what a function returns you have to know what ran before it. A
`nonlocal` write is confined to one enclosing function's lifetime — smaller
blast radius, still shared state. Both are tools, and both are worth
replacing with a return value when the replacement is cheap. The stretch
below is that replacement.

</details>

<details>
<summary>Under the hood — comprehensions have their own scope, and that matters here</summary>

`street_totals` ends in a dict comprehension:

```python
return {street: add(bags) for street, bags in counts.items()}
```

That comprehension is not just tidy syntax. Since Python 3, a comprehension
compiles into its own hidden function, with its own local scope. You can
prove it in one line:

```text
>>> [i for i in range(3)]
[0, 1, 2]
>>> i
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'i' is not defined
```

The loop variable never escapes. In Python 2 it did, and it would happily
overwrite a variable you were using — one of the tidier things Python 3 fixed.

Two consequences land directly on this exercise.

**The comprehension is a third scope in the chain.** Inside it, `add` is
found by looking outward into `street_totals`, exactly the way `add` finds
`running`. Nested scopes chain as deep as you nest them; **E** is not one box
but as many as there are enclosing functions.

**Order is guaranteed, so the running total means something.**
`counts.items()` yields pairs in insertion order and the comprehension
consumes them in that order, so `add` is called on Cedar Street, then Mill
Road, then Front Street. If dicts were unordered, "a running total, street by
street" would not even be a well-defined thing to ask for.

One genuine trap, since you now know comprehensions have a scope: `nonlocal`
and `global` inside a comprehension refer to the *comprehension's* enclosing
chain, which usually does what you want but is worth knowing about before you
try to be clever inside one. The plainest advice is the best advice — if a
comprehension needs a scope declaration, write a `for` loop instead.

</details>

## Acceptance checklist

- [ ] `python exercise-04-scope-mystery.py` prints four lines and `All checks passed.`
- [ ] The `__main__` block is byte-for-byte unchanged.
- [ ] `sign_up` returns a fresh list when no roster is passed.
- [ ] No module-level name shadows a built-in anywhere in the file.
- [ ] `street_totals` uses `nonlocal`, not `global`.
- [ ] Calling `street_totals` twice with the same input gives the same answer
      twice.
- [ ] `crew_capacity` reads `crew_size` and nothing else.
- [ ] A comment block at the top names all five bugs and the rule each broke.
- [ ] Committed to Git with a message like `Fix Week 4 exercise 4: five scope bugs`.

To check the last two properly, import the module and call things twice in
one session — a single run of the file cannot show you either:

```bash
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', 'exercise-04-scope-mystery.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
counts = {'Cedar Street': 5, 'Mill Road': 3, 'Front Street': 2}
print(m.street_totals(counts))
print(m.street_totals(counts))
print(m.sign_up('Rosa'), m.sign_up('Ken'), m.VOLUNTEERS_SIGNED_UP)
"
```

```text
{'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
{'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
['Rosa'] ['Ken'] 2
```

Two identical dicts means no state leaked between calls. Two separate
one-name rosters means the default is not shared. The counter at `2` means
`global` is doing its job.

## Stretch

- Remove `global` entirely. Have `sign_up` hand back both values and let the
  caller do the rebinding:

  ```python
  def sign_up_pure(name: str, roster: list[str] | None = None,
                   count: int = 0) -> tuple[list[str], int]:
      """Return a roster with `name` added and the new signed-up count."""
      if roster is None:
          roster = []
      return [*roster, name], count + 1
  ```

  ```text
  roster: ['Rosa', 'Ken'] count: 2
  ```

  Is it better? Genuinely yes, and not for style reasons. The function no
  longer changes its argument either — `[*roster, name]` builds a new list —
  so it has no effect on the world beyond what it returns, and you can call
  it a hundred times in a test without resetting anything first. The cost is
  real too: every call site now handles two values, and
  `roster, count = sign_up_pure(...)` is noisier than `sign_up(...)`. That
  trade is the one behind functional programming, and the honest answer is
  that it starts paying as soon as more than one thing calls the function.
  Write down which way you land.

- Rewrite `street_totals` with `itertools.accumulate` and no nested function
  at all:

  ```python
  def street_totals(counts: dict[str, int]) -> dict[str, int]:
      """Return a running cumulative total per street, with no closure."""
      return dict(zip(counts, itertools.accumulate(counts.values())))
  ```

  ```text
  accumulate once : {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
  accumulate twice: {'Cedar Street': 5, 'Mill Road': 8, 'Front Street': 10}
  ```

  The nested function is gone, and with it the entire class of bug: there is
  no `running`, so there is nothing to declare `nonlocal`, so there is
  nothing to get wrong. Looping over a dict gives you its keys and
  `counts.values()` gives the values in matching order, so `zip` lines them
  up. This is not a smaller version of the original — it is a different idea,
  "running totals" as a named operation rather than a loop with a memory.

- Add a sixth bug of your own to a copy of the file, hand it to someone else
  in the org, and see how long it takes them to find it. Writing a bug that
  is hard to find teaches you more than fixing five easy ones.

- Install `ruff` and run `ruff check` on the original broken file. Predict
  first, then look. The mutable default and the shadowed built-in are both
  single-line, purely syntactic patterns, and linters spot them instantly.
  The missing `global`, the missing `nonlocal` and the ignored parameter are
  much harder — the first two are legal code that means something else, and
  the third needs somebody to know what the function was *supposed* to
  compute. A linter reads syntax. Only you read intent.

Next: [Exercise 5 — Import and Use](./exercise-05-import-and-use.md).
