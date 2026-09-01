# Exercise 1 — Variable Swap

> **Topic:** Tuple unpacking and multiple assignment
> **Lecture:** [01 — Variables and Built-in Types](../lecture-notes/01-variables-and-types.md)
> **Difficulty:** Easy
> **Target time:** 15 minutes
> **Why this one:** you will type `=` more than any other character in this course, and most people arrive thinking it means "is equal to", the way it does in maths. In Python it means something else: *give this value that name*. Swapping two names is the smallest job that makes the difference show. Once you have watched `a, b = b, a` work and watched the two-line version fail, the rule sticks.

## The Brief

Your community coding lab runs two supervised shifts every evening, an
early one and a late one. One volunteer covers each. Tonight they want to
trade.

Then you do it again with three volunteers on Monday, Tuesday and
Wednesday. Everybody moves one day forward, and the person on the end
wraps around to the front.

Both jobs are one line of Python. Neither needs a spare box to hold a
value while you shuffle.

Here is why that is worth a whole exercise. The obvious two-step version
— copy the first into the second, then copy the second into the first —
throws one of your two volunteers away. It does not crash. It does not
warn you. It hands you the same name twice, and you find out an hour
later when the roster is wrong.

## Starter

Create `exercise-01-variable-swap.py` in your practice repo, paste this
in, then fill the two `TODO`s:

```python
"""exercise-01-variable-swap.py — trade and rotate shifts with no temporary.

Week 2, Exercise 1. Practises tuple unpacking and multiple assignment.
"""


def swap(first: str, second: str) -> tuple[str, str]:
    """Return the early and late volunteers in the opposite order."""
    # TODO: return the pair swapped, as a single tuple expression.
    #       No temporary variable, no list.
    ...


def rotate(a: str, b: str, c: str) -> tuple[str, str, str]:
    """Move Mon/Tue/Wed one day forward, wrapping the last to the front.

    rotate("Ada", "Grace", "Alan") returns ("Alan", "Ada", "Grace").
    """
    # TODO: one return statement, one tuple, no temporary variables.
    ...


def main() -> None:
    """Print the roster before and after a swap and a rotation."""
    early: str = "Ada"
    late: str = "Grace"
    print("Shift swap")
    print(f"  before: early={early}, late={late}")
    early, late = swap(early, late)
    print(f"  after : early={early}, late={late}")

    monday: str = "Ada"
    tuesday: str = "Grace"
    wednesday: str = "Alan"
    print("Weekly rotation")
    print(f"  before: {monday}, {tuesday}, {wednesday}")
    monday, tuesday, wednesday = rotate(monday, tuesday, wednesday)
    print(f"  after : {monday}, {tuesday}, {wednesday}")


if __name__ == "__main__":
    main()
```

A **tuple** is a row of values kept in a fixed order, written with commas:
`("Ada", "Grace")`. The word for reading a tuple back out into separate
names is **unpacking**, and `main()` already does it for you on the
`early, late = ...` line. You are writing the halves that build the rows;
the unpacking is handed to you finished.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/exercises/exercise-01-variable-swap.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `swap()` returns a `tuple[str, str]` holding its two arguments in the
   opposite order.
2. `rotate()` returns a `tuple[str, str, str]` where the third argument
   has moved to the front and the other two have each shifted one place
   later.
3. Neither function declares a temporary variable. Each one is a single
   `return` statement.
4. Do not change `main()`. It already unpacks the returned tuples back
   into the named variables, and that unpacking is half the lesson.
5. The output matches the Expected output section exactly, including the
   two-space indent and the space before the colon on the `after :`
   lines.
6. Both functions keep their type hints and their docstrings.

## Constraints

- **Return a tuple, not a list.** Both are rows of values and both would
  unpack correctly, so the program would still run. A tuple is the better
  fit because a tuple cannot be changed and cannot grow, which is exactly
  what "a pair of volunteers" is. A list says "this could get longer". It
  cannot. `mypy` — the type checker from Lecture 3 — also refuses a list
  where you promised a `tuple[str, str]`, which is the tool telling you
  the same thing in its own words.
- **No temporary variable.** A temporary works and is not a crime. It
  just hides the machinery you came here to see: Python works out the
  *whole* right-hand side of an `=` first, and only then hands out the
  names on the left. If you never write the version without a temporary,
  you never meet that rule head on.
- **Keep the return type hints even though Python ignores them at run
  time.** Lecture 3 explains what they are for. For now, read
  `-> tuple[str, str]` as the sentence "exactly two strings come back" —
  the one fact the function's name cannot carry on its own.

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-01-variable-swap.py
Shift swap
  before: early=Ada, late=Grace
  after : early=Grace, late=Ada
Weekly rotation
  before: Ada, Grace, Alan
  after : Alan, Ada, Grace
```

Six lines, and nothing in them changes from machine to machine. Every
name in this program is typed into the file, so your run and this run are
the same run.

## Steps

1. Turn on your Week 2 virtual environment. Your prompt should show
   `(.venv)` or something like it.
2. Create `exercise-01-variable-swap.py` and paste the starter in.
3. Fill in `swap()` first. Run it: `python exercise-01-variable-swap.py`.
   You will get a `TypeError` from the `rotate()` line, and that is
   expected at this stage — read the five lines that print before the
   error, confirm the swap worked, then carry on.
4. Fill in `rotate()`. Run again. All six lines should print.
5. Before you move on, prove the failure mode to yourself. Open the REPL
   by typing `python` on its own and enter these four lines:

   ```python
   >>> early, late = "Ada", "Grace"
   >>> early = late
   >>> late = early
   >>> early, late
   ('Grace', 'Grace')
   ```

   Ada is gone. There was no error. That is the bug this exercise exists
   to vaccinate you against.
6. If you installed `mypy`, run `mypy exercise-01-variable-swap.py` and
   aim for `Success: no issues found in 1 source file`.

## The Solution

```python
"""exercise-01-variable-swap-solution.py — trade and rotate shifts with no temporary.

Week 2, Exercise 1. Practises tuple unpacking and multiple assignment.
"""


def swap(first: str, second: str) -> tuple[str, str]:
    """Return the early and late volunteers in the opposite order."""
    return second, first


def rotate(a: str, b: str, c: str) -> tuple[str, str, str]:
    """Move Mon/Tue/Wed one day forward, wrapping the last to the front.

    rotate("Ada", "Grace", "Alan") returns ("Alan", "Ada", "Grace").
    """
    return c, a, b


def main() -> None:
    """Print the roster before and after a swap and a rotation."""
    early: str = "Ada"
    late: str = "Grace"
    print("Shift swap")
    print(f"  before: early={early}, late={late}")
    early, late = swap(early, late)
    print(f"  after : early={early}, late={late}")

    monday: str = "Ada"
    tuesday: str = "Grace"
    wednesday: str = "Alan"
    print("Weekly rotation")
    print(f"  before: {monday}, {tuesday}, {wednesday}")
    monday, tuesday, wednesday = rotate(monday, tuesday, wednesday)
    print(f"  after : {monday}, {tuesday}, {wednesday}")


if __name__ == "__main__":
    main()
```

Two lines of work. That is the correct amount, and it is the point.

**The comma makes the tuple. The brackets do not.** `return second, first`
and `return (second, first)` are the same instruction. Python sees the
comma and packs the values into a row; the brackets in the second version
are ordinary grouping brackets that happen to look like tuple syntax.
Knowing this is what lets you read `early, late = swap(early, late)`
correctly. There is a row of two on the right and a row of two names on
the left, and neither of them needs brackets to be a row.

**Python finishes the right-hand side before it touches the left.** This
is the whole exercise in one sentence. When `swap()` runs
`return second, first`, Python builds the finished pair
`("Grace", "Ada")` as one value. Only after that does the caller's
`early, late = ...` open it up and hand out the two names. Nothing on the
left can disturb anything on the right, because the right is already
done.

The two-step version fails for exactly the opposite reason. `early = late`
finishes completely, and in finishing it wipes out the only label pointing
at `"Ada"`. The second line then copies Grace onto herself. There was
never a moment where both values had somewhere to live.

**`rotate()` is the same rule with three slots.** `return c, a, b` builds
`("Alan", "Ada", "Grace")`. Read it as a seating plan, not as a shuffle:
whoever should be on Monday goes in slot one, and that is Wednesday's
volunteer, `c`. Write down where people *land*, not how they *move*.
People who think "everyone shifts forward one" tend to type `b, c, a`,
which is the rotation running backwards.

**A tuple rather than a list, on purpose.** `return [second, first]` would
run, and would unpack correctly, because unpacking works on any row of
values. The type hint is what rejects it. `tuple[str, str]` promises a
pair of exactly two strings; `list[str]` promises zero or more. `mypy`
will not let you swap one for the other. The hint is carrying a fact the
function's name cannot — how many things come back — and a list throws
that fact away.

**Nothing here needs an `if`.** Worth noticing while you have the chance.
Week 2 has no `if` in its lecture material and this exercise does not miss
it, because rearranging values is pure assignment. Week 3 hands you
branching, and from then on it is tempting to reach for `if` in places
where a plain expression would have done the job.

## Download and run

Download [exercise-01-variable-swap-solution.py](./exercise-01-variable-swap-solution.py) and run it:

```bash
python exercise-01-variable-swap-solution.py
```

## Common bugs to catch

- **`TypeError: cannot unpack non-iterable NoneType object`.** You left
  the `...` in a function body, or you worked out the tuple and forgot to
  `return` it. A function that returns nothing gives back `None`, and
  `None` cannot be spread across two names:

  ```text
  Traceback (most recent call last):
    File "<string>", line 5, in <module>
      early, late = swap("Ada", "Grace")
      ^^^^^^^^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  The little arrows point at the *left* side of the `=`, which is a
  useful hint: the unpacking is where it broke, so the thing to fix is
  what the function handed back.

- **`ValueError: too many values to unpack (expected 2)`.** Your `swap()`
  returned three items, usually because you pasted the `rotate()` body
  into it:

  ```text
  Traceback (most recent call last):
    File "<string>", line 5, in <module>
      early, late = swap("Ada", "Grace")
      ^^^^^^^^^^^
  ValueError: too many values to unpack (expected 2)
  ```

- **`ValueError: not enough values to unpack (expected 3, got 2)`.** The
  same mistake in a mirror, inside `rotate()`:

  ```text
  Traceback (most recent call last):
    File "<string>", line 6, in <module>
      monday, tuesday, wednesday = rotate("Ada", "Grace", "Alan")
      ^^^^^^^^^^^^^^^^^^^^^^^^^^
  ValueError: not enough values to unpack (expected 3, got 2)
  ```

  Count the commas in your `return`. The number of items on the right and
  the number of names on the left have to agree exactly. Python does not
  pad the short side and does not trim the long one.

- **Both names print the same volunteer, and nothing complains.** This is
  the dangerous one, because it makes wrong data quietly. You wrote the
  two-step version inside `swap()` and returned the two locals:

  ```text
  Shift swap
    before: early=Ada, late=Grace
    after : early=Grace, late=Grace
  Weekly rotation
    before: Ada, Grace, Alan
    after : Grace, Alan, Ada
  ```

  Ada is off the roster and nothing raised. That same run also shows the
  rotation going backwards, which is the other silent failure here.

- **The swap prints the same order twice.** You called
  `swap(early, late)` on a line by itself and let the answer fall on the
  floor:

  ```text
  Shift swap
    before: early=Ada, late=Grace
    after : early=Ada, late=Grace
  ```

  Python cannot reach back through a parameter name and rebind the
  caller's variable. A function that returns a value does nothing at all
  unless you assign what it returns.

- **The rotation goes the wrong way.** You returned `b, c, a` instead of
  `c, a, b`. Test it against the docstring example: Wednesday's
  volunteer, Alan, has to end up on Monday.

- **`SyntaxError: invalid syntax` on the return line.** You wrote
  `return second first` and dropped the comma. The comma is what builds
  the tuple.

- **`mypy` reports both likely static mistakes at once:**

  ```text
  exercise-01-variable-swap.py:7: error: Missing return statement  [empty-body]
  exercise-01-variable-swap.py:17: error: Incompatible return value type (got "list[str]", expected "tuple[str, str, str]")  [return-value]
  Found 2 errors in 1 file (checked 1 source file)
  ```

  `[empty-body]` is the `...` you forgot to replace. `[return-value]` is
  the list you used instead of a tuple. Neither would have raised at run
  time. That is the argument for a type checker, in one screenshot.

## Under the hood

<details>
<summary>Under the hood — why the swap needs no temporary, and what the bytecode does</summary>

Before Python runs your file it translates it into **bytecode**: a list of
very small instructions for a machine that only knows how to push values
onto a stack and pop them off again. A stack is a pile of plates. You add
to the top and you take from the top.

The `dis` module shows you that list. Here is the plain two-name swap on
CPython 3.13.2:

```python
>>> import dis
>>> def f(a, b):
...     a, b = b, a
...
>>> dis.dis(f)
  1           RESUME                   0

  2           LOAD_FAST_LOAD_FAST     16 (b, a)
              STORE_FAST_STORE_FAST   16 (b, a)
              RETURN_CONST             0 (None)
```

Two instructions of actual work. `LOAD_FAST_LOAD_FAST` pushes the current
values of `b` and `a` onto the stack, in that order.
`STORE_FAST_STORE_FAST` pops them straight back off into `a` and `b`. No
temporary variable, and — this may surprise you — no tuple either. The
values sit on the stack for the length of one instruction. CPython
recognises the shape `a, b = b, a` and skips building a tuple it would
only take apart again.

Compare the version with a temporary:

```text
  LOAD_FAST                0 (a)
  STORE_FAST               2 (tmp)
  LOAD_FAST                1 (b)
  STORE_FAST               0 (a)
  LOAD_FAST                2 (tmp)
  STORE_FAST               1 (b)
```

Six instructions, one extra name, and a third slot reserved in the
function's frame for `tmp`. It is not slower in any way you could
measure, and it is more to read.

Now the two halves of this exercise, which are a little different because
a function call sits in the middle. `return second, first` really does
build a tuple, because a function can only hand back one value:

```text
  LOAD_FAST_LOAD_FAST     16 (second, first)
  BUILD_TUPLE              2
  RETURN_VALUE
```

And the caller takes it apart again:

```text
  LOAD_FAST                2 (swap)
  PUSH_NULL
  LOAD_FAST_LOAD_FAST      1 (a, b)
  CALL                     2
  UNPACK_SEQUENCE          2
  STORE_FAST_STORE_FAST    1 (a, b)
```

`UNPACK_SEQUENCE 2` is the instruction that raises `ValueError` when the
count is wrong, and `TypeError: cannot unpack non-iterable NoneType
object` when the thing on the stack is `None`. Both of those messages in
Common bugs to catch come from this one instruction, which is why the
carets in the traceback underline the left side of the `=`.

The thing worth carrying away is not the instruction names. It is that
`BUILD_TUPLE` always comes before `STORE`. The right-hand side is
finished and sitting on the stack before a single name on the left is
touched.

</details>

<details>
<summary>Under the hood — a name is a label, not a box</summary>

School maths teaches you to picture a variable as a box with a value in
it, and `a = b` as copying the contents of one box into the other. Python
does not work that way, and the box picture is what makes the two-step
swap look reasonable.

In Python, values float in memory and names are sticky labels pointing at
them. `early = "Ada"` writes a label and sticks it on the string `"Ada"`.
`early = late` does not copy anything. It peels the `early` label off and
sticks it on whatever `late` is pointing at. Now two labels point at one
string, and the string that `early` used to point at has nothing pointing
at it at all.

That is why the value disappears. Not because it was overwritten, but
because the last label pointing at it moved away. You can watch it happen
with `id()`, which gives you the address a value lives at:

```text
>>> early, late = "Ada", "Grace"
>>> id(early), id(late)
(1504415578608, 1504415578272)
>>> early = late
>>> id(early), id(late)
(1504415578272, 1504415578272)
```

The two numbers you get will differ from these — addresses change every
run — but the shape will not. After `early = late` there is one address,
listed twice. `"Ada"` is still out there for a moment, with no label,
waiting to be cleaned up.

`x = y = "Ada"` is the same fact from another angle. Both labels go on
one string. Then `x = "Grace"` moves only the `x` label, and `y` still
says `"Ada"`. Rebinding a name never reaches through to any other name —
which is exactly why a swap has to move both labels in the same step.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] All six lines print, matching the Expected output character for character.
- [ ] `swap()` and `rotate()` each contain exactly one `return` and no temporary variable.
- [ ] Both functions return tuples, not lists.
- [ ] You reproduced the two-step failure in the REPL and can explain in one sentence why it loses a value.
- [ ] `mypy` reports no issues, if you have it installed.
- [ ] The file is committed to Git with a message like `Add Week 2 exercise 1: variable swap`.

## Stretch

- Extend the idea to a fourth volunteer for Thursday. Write
  `rotate4(a, b, c, d) -> tuple[str, str, str, str]` and notice that you
  now have four names on the left of the assignment too:

  ```text
  four-day : Katherine, Ada, Grace, Alan
  ```

  Four is where this stops scaling. A fifth volunteer wants a fifth
  parameter and a sixth line of the same idea. The signature is now
  carrying data that belongs in a list, and Week 5 gives you
  `names[-1:] + names[:-1]`, which is one expression for any number of
  people. Writing `rotate4()` by hand is worth doing exactly once, so
  that the list version later lands as a relief rather than as a rule.

- Write `rotate_back()`, which moves everybody one day *earlier*. It is
  `rotate()` read the other way: forward puts each name one position
  later, so backward puts each one earlier, `b` lands first and `a` wraps
  to the end. Confirm it undoes the forward rotation:

  ```text
  undone   : ('Ada', 'Grace', 'Alan')
  ```

  Write that check as `rotate_back(*rotate("Ada", "Grace", "Alan"))`. The
  `*` spreads the returned three-tuple into three separate arguments.
  Without it you are handing one tuple to a function that wants three
  strings, and you get
  `TypeError: rotate_back() missing 2 required positional arguments: 'b' and 'c'`.

- Try chained assignment in the REPL: `x = y = "Ada"`, then `x = "Grace"`.
  Predict what `y` is before you press Enter.

  ```text
  chained  : x=Grace, y=Ada
  ```

  Chaining is not a swap. It puts both labels on one value, and moving one
  label afterwards leaves the other exactly where it was.

When your roster reorders correctly, move on to
[Exercise 2 — String Formatter](./exercise-02-string-formatter.md).
