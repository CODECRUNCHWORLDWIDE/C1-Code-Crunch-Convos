# Homework Problem 4 — Recursive Sum

> **Topic:** a function that calls itself, the base case that stops it, and the same job written as a plain loop so the two can be checked against each other
> **Lecture:** [Lecture Note 3 — Recursion](../lecture-notes/03-recursion.md)
> **Difficulty:** Intermediate
> **Target time:** 45 minutes
> **Why this one:** recursion is not hard because the machinery is complicated. It is hard because you have to trust a function that has not finished running yet. Adding up a list is the smallest useful problem where that trust is required, and the smallest one where you can watch the trust pay off.

## The Brief

Here is a strange way to add up a list.

The total of `[1, 2, 3, 4]` is `1` plus the total of `[2, 3, 4]`.
The total of `[2, 3, 4]` is `2` plus the total of `[3, 4]`.
The total of `[3, 4]` is `3` plus the total of `[4]`.
The total of `[4]` is `4` plus the total of `[]`.
The total of `[]` is `0`.

Read those five lines again. Only the last one is an actual answer. The
other four are the same sentence with a shorter list each time, and each
one is waiting on the line below it. When the last line finally gives a
real number, all four waiting sums resolve back up: `4`, then `7`, then
`9`, then `10`.

That is **recursion** — a function that solves a problem by calling itself
on a smaller version of the same problem.

Write `sum_recursive(nums: list[int]) -> int`. It must not use `sum`, must
not use a loop, and must call itself.

Then write `sum_iterative(nums: list[int]) -> int` that does the same job
with an ordinary `for` loop. Both must give the same answer on the same
input, always.

Then write `_run_tests()` that checks both against these cases:

| Input | Total |
|-------|-------|
| `[]` | `0` |
| `[5]` | `5` |
| `[1, 2, 3, 4]` | `10` |
| `[-1, 1]` | `0` |

Two implementations that disagree tell you one of them is wrong. That is
more than one implementation can ever tell you, however carefully you read
it.

## Starter

Save this as `recursive_sum.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it just gets three of the four cases wrong:

```python
"""Sum a list of ints two ways: recursively and iteratively."""

CASES: list[tuple[list[int], int]] = [
    ([], 0),
    ([5], 5),
    ([1, 2, 3, 4], 10),
    ([-1, 1], 0),
]


def sum_recursive(nums: list[int]) -> int:
    """Return the sum of `nums` using recursion, without `sum` or a loop.

    Args:
        nums: A list of integers.

    Returns:
        The total.

    Example:
        >>> sum_recursive([1, 2, 3, 4])
        10
    """
    # TODO: base case first - an empty list totals 0
    # TODO: otherwise, the first item plus the total of everything after it
    return 0


def sum_iterative(nums: list[int]) -> int:
    """Return the sum of `nums` with a plain loop, for comparison."""
    # TODO: start a running total at 0, add each item, return it
    return 0


def _run_tests() -> None:
    """Check both functions against CASES and against each other."""
    for nums, expected in CASES:
        rec = sum_recursive(nums)
        itr = sum_iterative(nums)
        if rec != expected or itr != expected:
            print(f"FAIL: {nums} -> recursive {rec}, iterative {itr}, expected {expected}")
            return
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
```

`_run_tests` is given to you complete this time, because you wrote one in
problem 3 and the shape is identical. `sum_iterative` is missing its
`Args:`, `Returns:` and `Example:` — writing those is part of the work.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-04-recursive-sum.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `sum_recursive` returns the total of the list and calls itself to do
   it.
2. `sum_recursive` contains no `for`, no `while`, no `sum`, and no
   comprehension.
3. `sum_iterative` returns the same total using a `for` loop.
4. Neither function changes the list it was given.
5. All four cases in `CASES` pass for both functions.
6. Type hints and a full docstring on all three functions.
7. Running the file runs the tests. Importing it prints nothing.

## Constraints

- **Write the base case first.** Before you write the line that calls
  itself, write the line that does not. Without it there is nothing to
  stop the recursion, and the failure is not the one you expect — it is an
  `IndexError`, because `[][0]` blows up before the call does.
- **Every recursive call must move strictly closer to the base case.**
  `nums[1:]` is exactly one item shorter than `nums`, every time. That is
  the property that guarantees a list of *n* items reaches `[]` after
  exactly *n* steps. Pass `nums` instead of `nums[1:]` and you have
  written an infinite loop with extra machinery.
- **No `sum`, no loop, no comprehension inside `sum_recursive`.** The
  constraint *is* the exercise. `return sum(nums)` passes every test in
  this file and teaches you nothing.
- **Do not mutate the input.** `nums.pop(0)` looks like a clever way to
  avoid copying. It gives the right total once and hands the caller back
  an empty list. Common bugs to catch shows exactly what that does to the
  second test run.
- **`sum_iterative` is not filler.** It is the second opinion. It is also
  the version you would actually ship, for reasons the Under the hood
  block on the recursion limit makes concrete.

## Expected output

```text
$ python problem-04-recursive-sum.py
All tests passed
```

Now watch the recursion work, and then watch it hit a wall. Nine hundred
numbers is fine:

```bash
python -c "from recursive_sum import sum_recursive as s; print(s(list(range(900))))"
```

```text
404550
```

Five thousand is not:

```bash
python -c "from recursive_sum import sum_recursive as s; s(list(range(5000)))"
```

The last four lines of a very long traceback:

```text
  File "...\homework\recursive_sum.py", line 36, in sum_recursive
    return nums[0] + sum_recursive(nums[1:])
                     ~~~~~~~~~~~~~^^^^^^^^^^
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

The same list through `sum_iterative` returns instantly. Nothing is
broken — you have found a real, hard limit of the technique, and the
Under the hood block below explains where the number 1000 comes from.

And the docstring examples are real tests:

```bash
python -m doctest recursive_sum.py -v
```

The last three lines:

```text
2 tests in 4 items.
2 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `recursive_sum.py`. Run it. It fails on `[5]`,
   because both functions return `0` for everything.
3. Write the base case of `sum_recursive` and nothing else:
   `if not nums: return 0`. Run it. The `[]` case now passes and `[5]`
   still fails, which is exactly right.
4. Add the recursive line: `return nums[0] + sum_recursive(nums[1:])`.
   Run it. `sum_recursive` is done.
5. Watch it work. Paste this into a scratch file and run it:

   ```python
   def traced(nums: list[int], depth: int = 0) -> int:
       """Sum a list recursively, printing each call as it is made."""
       print("  " * depth + f"traced({nums})")
       if not nums:
           return 0
       return nums[0] + traced(nums[1:], depth + 1)


   print(traced([1, 2, 3]))
   ```

   ```text
   traced([1, 2, 3])
     traced([2, 3])
       traced([3])
         traced([])
   6
   ```

   Four calls go down and one number comes back up. Nothing is added
   until the bottom is reached.
6. Write `sum_iterative`. Three lines: a total at `0`, a loop that adds,
   a return.
7. Run the file. `All tests passed`.
8. Finish `sum_iterative`'s docstring. Then run
   `python -m doctest recursive_sum.py -v`.
9. Find the wall. Run the 900 and the 5000 commands from **Expected
   output**. Read the last line of the traceback and believe it.
10. Compare against **The Solution**, tick the acceptance checklist, and
    commit: `git add homework/recursive_sum.py` then
    `git commit -m "Week 4 homework: recursive sum"`.

## The Solution

```python
"""Sum a list of ints two ways: recursively and iteratively.

Week 4 homework, problem 4, Code Crunch Convos.

Save your own copy as ``recursive_sum.py`` in your ``homework/`` folder.

Two functions answer the same question by different routes, and
``_run_tests`` checks both against the same expected totals. Two
implementations that disagree tell you one of them is wrong, which is more
than one implementation that merely looks right can ever tell you.
"""

CASES: list[tuple[list[int], int]] = [
    ([], 0),
    ([5], 5),
    ([1, 2, 3, 4], 10),
    ([-1, 1], 0),
]


def sum_recursive(nums: list[int]) -> int:
    """Return the sum of `nums` using recursion, without `sum` or a loop.

    Args:
        nums: A list of integers.

    Returns:
        The total.

    Example:
        >>> sum_recursive([1, 2, 3, 4])
        10
    """
    if not nums:
        return 0
    return nums[0] + sum_recursive(nums[1:])


def sum_iterative(nums: list[int]) -> int:
    """Return the sum of `nums` with a plain loop, for comparison.

    Args:
        nums: A list of integers.

    Returns:
        The total.

    Example:
        >>> sum_iterative([1, 2, 3, 4])
        10
    """
    total = 0
    for num in nums:
        total += num
    return total


def _run_tests() -> None:
    """Check both functions against CASES and against each other."""
    for nums, expected in CASES:
        rec = sum_recursive(nums)
        itr = sum_iterative(nums)
        if rec != expected or itr != expected:
            print(f"FAIL: {nums} -> recursive {rec}, iterative {itr}, expected {expected}")
            return
    print("All tests passed")


if __name__ == "__main__":
    _run_tests()
```

**Why it works.**

**A recursive function needs exactly two things, and it needs both.** A
**base case** that returns an answer without calling itself, and a
**recursive case** that moves strictly closer to that base case. Here the
base case is `if not nums: return 0` and the recursive case is
`nums[0] + sum_recursive(nums[1:])`. `nums[1:]` is always one item
shorter, so a list of *n* items reaches `[]` in exactly *n* steps and
stops. Lose the "strictly closer" property and you have an infinite loop.
Lose the base case and there is nothing to stop at.

**Trace `sum_recursive([1, 2, 3])` by hand once. It is worth sixty
seconds:**

| Call | `nums` | Returns |
|------|--------|---------|
| 1 | `[1, 2, 3]` | `1 + <call 2>` |
| 2 | `[2, 3]` | `2 + <call 3>` |
| 3 | `[3]` | `3 + <call 4>` |
| 4 | `[]` | `0` |

Then the additions resolve back up: call 3 gives `3`, call 2 gives `5`,
call 1 gives `6`. Notice that nothing is added on the way down. All four
calls are sitting in memory, each holding a number and waiting, until the
base case finally returns something real. That waiting is not free, and
it is where the recursion limit comes from.

**`if not nums:` rather than `if len(nums) == 0:`.** An empty list is
falsy in Python, so `not nums` is `True` for `[]` and `False` for anything
with something in it. Same behaviour, less machinery, and it is the form
[PEP 8](https://peps.python.org/pep-0008/) prefers.

**`nums[1:]` is a fresh list, not a window onto the old one.** Slicing
copies. That is what makes `sum_recursive` safe — it never touches the
caller's list. It also means summing *n* items copies *n*, then *n-1*,
then *n-2* items and so on, which is a lot of copying for one addition.
`sum_iterative` copies nothing. For four numbers the difference is
invisible; the point is that "elegant" and "efficient" are two different
axes and you should know which one you traded away.

**`sum_iterative` is the second opinion.** `_run_tests` compares both
against the expected value on every case, so a case can fail three
different ways — recursive wrong, iterative wrong, or both wrong in
different directions — and the FAIL line names all three numbers so you
can tell which.

## Download and run

Download [problem-04-recursive-sum-solution.py](./problem-04-recursive-sum-solution.py)
and run it:

```bash
python problem-04-recursive-sum-solution.py
```

Save your own copy as `recursive_sum.py` in your homework folder, and
commit that one. The longer download name keeps it from landing on top of
your work.

## Common bugs to catch

- **No base case, or the base case written after the recursive call.**

  ```python
  def sum_recursive(nums: list[int]) -> int:
      """BUGGY: nothing stops this."""
      return nums[0] + sum_recursive(nums[1:])
  ```

  The failure is not the `RecursionError` you might expect. It is this,
  after only a few calls:

  ```text
  IndexError: list index out of range
  ```

  `[][0]` fails before the recursive call gets a chance to. People often
  "fix" it by wrapping the line in `try`, which buries the real problem.
  Write the base case first, always.
- **Recursing on the same list.**

  ```python
  return nums[0] + sum_recursive(nums)     # WRONG: nums never shrinks
  ```

  Now the argument never gets closer to `[]`, so this really does run
  until the stack is full: `RecursionError: maximum recursion depth
  exceeded`. Every recursive call must make the problem smaller.
- **Mutating the caller's list to avoid the copy.**

  ```python
  def sum_recursive(nums: list[int]) -> int:
      if not nums:
          return 0
      first = nums.pop(0)      # WRONG: this empties the caller's list
      return first + sum_recursive(nums)
  ```

  It gives the right total exactly once:

  ```text
  10
  []
  0
  ```

  That is the same list summed, printed, and summed again. The first
  answer is right, the list is now empty, and the second answer is `0`. A
  function that returns a value should not also gut its argument.
- **Using `sum` and calling it done.**

  ```python
  def sum_recursive(nums: list[int]) -> int:
      return sum(nums)         # WRONG: passes every test, learns nothing
  ```
- **Treating `RecursionError` as a bug in your code.** It is not. On a
  list of 5000 your function is correct and the technique is out of room.
  The fix is not a cleverer recursion; it is `sum_iterative`.
- **`total += num` outside the loop.** In `sum_iterative`, one space of
  indentation decides whether you add every item or only the last one.
  `sum_iterative([1, 2, 3])` returning `3` is this bug.

## Under the hood

<details>
<summary>Under the hood — why the base case is not optional, and where 1000 comes from</summary>

Every time a Python function is called, the interpreter builds a small
record called a **stack frame**. It holds that call's local variables, its
arguments, and the place to jump back to when the call finishes. Frames
are stacked: the newest sits on top, and when a call returns its frame is
thrown away.

`sum_recursive([1, 2, 3])` builds four frames before any of them returns.
Frame 1 cannot finish until frame 2 hands it a number, frame 2 is waiting
on frame 3, and so on. All four exist at once.

That stack is real memory, and it is not unlimited. CPython caps the depth
on purpose:

```bash
python -c "import sys; print(sys.getrecursionlimit())"
```

```text
1000
```

Go past it and you get an exception rather than a crash:

```text
RecursionError: maximum recursion depth exceeded
```

The limit exists to catch runaway recursion *before* the real machine
stack runs out. If Python let you keep going, you would eventually get a
segmentation fault — the operating system killing the process with no
traceback and no message. `RecursionError` is a catchable Python
exception with a stack trace attached, which is enormously more useful.

You can raise the ceiling:

```python
import sys

sys.setrecursionlimit(10000)
```

With that in place, `sum_recursive(list(range(5000)))` returns
`12497500`. But raising the limit is trading one failure mode for a worse
one — the C stack underneath has its own hard size, and going past *that*
is the segmentation fault the limit was protecting you from. Treat
`sys.setrecursionlimit` as a tool for a known-depth problem, not as a way
to make a design decision go away.

**So what is recursion actually for?** Problems whose *shape* is
recursive, and whose depth grows slowly:

- Trees and nested data. A folder holds files and folders. A JSON object
  holds values and objects. Walking one is naturally recursive, and the
  depth is the nesting depth — rarely more than a few dozen.
- Divide and conquer. Merge sort splits a list in half, then halves
  again. A million items is only about 20 levels deep, because each level
  halves the problem instead of shaving one item off it.

`sum_recursive` is neither. It shaves one item per level, so its depth is
the length of the list, which is the worst possible ratio. It is a
teaching example, and it teaches honestly by falling over at a size you
can actually reach.

**One thing Python deliberately does not do.** Some languages spot that
`sum_recursive`'s last action is a call and quietly reuse the current
frame instead of stacking a new one. That is **tail-call elimination**,
and it makes deep recursion free. Python does not do it and
[has decided not to](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit),
because losing the frames means losing the traceback, and Python's
designers consider a readable traceback worth more than deep recursion.
That is a real trade-off, honestly made, and it is why recursion in
Python is a modelling tool rather than a looping one.

[Lecture Note 3](../lecture-notes/03-recursion.md) walks through the call
stack in more detail, including the three properties every correct
recursive function has.

</details>

<details>
<summary>Under the hood — the hidden cost of nums[1:]</summary>

`nums[1:]` reads like "the rest of the list". What it actually does is
build a brand new list and copy every remaining item into it.

Count the copying for a list of *n* items:

| Call | List length copied |
|------|--------------------|
| 1 | *n* − 1 |
| 2 | *n* − 2 |
| 3 | *n* − 3 |
| … | … |
| *n* | 0 |

Add those up and you get roughly *n²/2* item-copies. For 900 numbers
that is about 400,000 copies to perform 900 additions. `sum_iterative`
does 900 additions and copies nothing.

This is the difference between **quadratic** and **linear** work. Double
the input and the loop takes twice as long, while the recursion takes
four times as long. At small sizes nobody notices. At large sizes it is
the whole story.

The recursive shape can be fixed without giving up recursion, by passing
an index instead of a slice:

```python
def sum_from(nums: list[int], start: int = 0) -> int:
    """Return the total of nums[start:] without copying anything."""
    if start >= len(nums):
        return 0
    return nums[start] + sum_from(nums, start + 1)
```

No copying now — the same list is passed down and only a number changes.
The work is linear. The stack depth is unchanged, so it still stops at
1000, but one of the two costs is gone.

The general lesson is bigger than this function. **Slicing always
copies**, in loops as well as in recursion. A loop that does
`rest = rest[1:]` on every pass has the same quadratic problem, and it is
much harder to spot there because nothing about the code looks recursive.
When you find yourself slicing inside something that repeats, ask whether
an index would do.

</details>

## Acceptance checklist

- [ ] `python recursive_sum.py` prints exactly `All tests passed`.
- [ ] `sum_recursive` calls itself and contains no `for`, `while`, `sum`
      or comprehension.
- [ ] `sum_recursive([])` returns `0`.
- [ ] `sum_recursive([5])` returns `5`.
- [ ] `sum_recursive([1, 2, 3, 4])` returns `10`.
- [ ] Summing the same list twice gives the same answer both times — the
      input is not mutated.
- [ ] `sum_iterative` returns the same totals for all four cases.
- [ ] You have seen `RecursionError` at least once, on purpose.
- [ ] All three functions have type hints and a docstring.
- [ ] `python -m doctest recursive_sum.py -v` ends with `Test passed.`
- [ ] Committed with a message like `Week 4 homework: recursive sum`.

## Stretch

- **Write `max_recursive(nums: list[int]) -> int`.** Same shape, different
  combining step: the largest of the list is the larger of the first item
  and the largest of the rest. Decide what the base case is when the list
  is empty — there is no sensible maximum of nothing, so raising
  `ValueError` is the honest answer, and it is the same guard-before-you-
  compute move as problem 1's absolute zero.
- **Write `count_down(n: int) -> None`.** Print `n`, then call yourself
  with `n - 1`, stopping at zero. Then move the `print` to *after* the
  recursive call and run it again. The numbers come out backwards, and
  the reason why is the whole call stack made visible.
- **Add the index version.** Put `sum_from` from the second Under the
  hood block in your file and check it against the other two in
  `_run_tests`. Three implementations, one expected answer.
- **Time all three.** Use `time.perf_counter` around each on a list of
  900 numbers, and print the three durations. Then try 2000 with the
  limit raised and watch which one still finishes in the time you are
  willing to wait.
- **Find your own recursion limit.** Write a function that calls itself
  and counts, catching nothing, and see what depth it reaches before
  `RecursionError`. It will be a little under 1000, because the frames
  your own program already had on the stack count too.

Next: [Homework Problem 5 — Dict Builder](./problem-05-dict-builder.md).
