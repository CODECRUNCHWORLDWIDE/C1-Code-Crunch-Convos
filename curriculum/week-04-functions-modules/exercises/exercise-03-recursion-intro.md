# Exercise 3 — Recursion Intro

> **Topic:** The same problem solved with a loop and with a function that calls itself
> **Lecture:** [03 — Recursion](../lecture-notes/03-recursion.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** recursion falls out of something you already know — a function can call any function, including itself. What trips people up is the stopping condition and the pile of unfinished calls waiting underneath. Lecture 3 draws that pile frame by frame; this page is where you drive it. Trees, nested dictionaries and directory walks in later weeks are all recursive, and none of them make sense while the stopping condition is still a mystery.

## The Brief

The community cleanup day has a sign-in table with a fixed number of chairs
and more volunteers than chairs. Somebody asks how many different orders the
volunteers could sit in. That is a **factorial**, and factorials are the
standard first recursion because the rule is one line.

Here is the rule in plain words. To find `5!` — read it "five factorial" —
you multiply `5` by the answer to `4!`. To find `4!` you multiply `4` by the
answer to `3!`, and so on. When you get down to `0!`, the answer is `1` and
you stop. In symbols: `n! = n * (n - 1)!`, and `0! = 1`.

That is the shape of every recursive function you will ever write. Two
claims, and only two:

1. **One case you can answer with no help at all.** Here it is `0!`, and the
   answer is `1`. This is called the **base case**.
2. **A rule that turns every other case into a strictly smaller one.** Here
   it is `n * (n - 1)!`. Smaller matters — if the new problem is not closer
   to the base case, you never arrive.

Everything that goes wrong with recursion is one of those two claims being
false. [Lecture 3](../lecture-notes/03-recursion.md) draws exactly what the
computer is holding while all those unfinished multiplications wait, and it
is worth reading section 4 before you start.

You will write the factorial twice. `factorial_iterative` uses a loop and a
running product. `factorial_recursive` writes the rule out directly. Then
`arrangements` puts them to work: the number of ordered ways to seat `k`
people out of `n` is `n!` divided by `(n - k)!`.

Two versions of one function looks like busywork until you run the comparison
loop at the bottom of the starter, which checks that they agree for every `n`
from 0 to 15. That loop is a small **property test** — instead of checking a
handful of values you chose, it checks that two independently written pieces
of code reach the same answer sixteen times. When you cannot trace code in
your head, that is real evidence.

The base case is where this bites. Plenty of people write `if n == 1: return
1`, because `1! = 1` is obviously true. It is also obviously true that
`0! = 1`, and a function that stops at `1` never stops when handed `0` — it
goes to `-1`, then `-2`, and keeps going until Python gives up. The very
first self-check is `factorial(0)`, for exactly that reason.

## Starter

Create `exercise-03-recursion-intro.py` in your practice repo.

```python
"""exercise-03-recursion-intro.py — counting ways to seat volunteers.

Two factorials, one iterative and one recursive, plus one real use for them.
"""


def factorial_iterative(n: int) -> int:
    """Return n! computed with a loop.

    Args:
        n: A non-negative integer.

    Returns:
        The product 1 * 2 * ... * n, and 1 when n is 0.

    Raises:
        ValueError: If n is negative.
    """
    # TODO: reject negative n with ValueError("n must be non-negative")
    # TODO: start an accumulator at 1 and multiply up through n
    raise NotImplementedError


def factorial_recursive(n: int) -> int:
    """Return n! by calling itself. Same contract as factorial_iterative.

    Raises:
        ValueError: If n is negative.
    """
    # TODO: reject negative n with ValueError("n must be non-negative")
    # TODO: base case -- which value of n needs no further calls?
    # TODO: recursive step -- n * factorial_recursive(n - 1)
    raise NotImplementedError


def arrangements(n: int, k: int) -> int:
    """Return the number of ordered ways to seat k of n volunteers.

    Args:
        n: How many volunteers turned up.
        k: How many chairs there are.

    Returns:
        n! // (n - k)!

    Raises:
        ValueError: If n or k is negative, or if k is greater than n.
    """
    # TODO: validate, then use one of the factorials above
    raise NotImplementedError


if __name__ == "__main__":
    assert factorial_iterative(0) == 1, factorial_iterative(0)
    assert factorial_iterative(1) == 1, factorial_iterative(1)
    assert factorial_iterative(5) == 120, factorial_iterative(5)
    assert factorial_iterative(10) == 3_628_800, factorial_iterative(10)
    assert factorial_iterative(20) == 2_432_902_008_176_640_000

    for n in range(16):
        assert factorial_recursive(n) == factorial_iterative(n), n

    for fn in (factorial_iterative, factorial_recursive):
        try:
            fn(-1)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fn.__name__}(-1) should raise ValueError")

    assert arrangements(5, 0) == 1, arrangements(5, 0)
    assert arrangements(5, 2) == 20, arrangements(5, 2)
    assert arrangements(6, 3) == 120, arrangements(6, 3)
    assert arrangements(4, 4) == 24, arrangements(4, 4)

    try:
        arrangements(3, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("k greater than n should raise ValueError")

    print(f"0! = {factorial_iterative(0)}")
    print(f"5! = {factorial_recursive(5)}")
    print(f"20! = {factorial_iterative(20)}")
    print(f"Seating 2 of 5 volunteers: {arrangements(5, 2)} ways")
    print("Iterative and recursive agree for n = 0 through 15.")
    print("All checks passed.")
```

Three words you need before you start.

**Accumulator.** A variable that holds the answer so far while a loop builds
it up. `product = 1` before the loop, `product *= factor` inside it.

**Base case.** The input a recursive function can answer immediately, with no
call to itself. Write it first, every single time.

**`raise`.** `raise ValueError("...")` stops the function and reports a
problem to whoever called it. It is not a return value they can ignore. You
meet exceptions properly in Week 6; here you only need to throw one.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/exercises/exercise-03-recursion-intro.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Both factorial functions return `1` for `n = 0`. That is the definition,
   not an edge case bolted on afterwards.
2. Both raise `ValueError` with the message `n must be non-negative` for
   negative input. Returning `None` or `0` instead would let a bad value
   travel quietly into `arrangements`.
3. `factorial_recursive` must actually call itself. A loop wearing a
   recursive name is not the exercise.
4. `arrangements` raises `ValueError` when `k > n`, when `n < 0`, or when
   `k < 0`.
5. `arrangements` returns an `int`, and `arrangements(5, 0)` is `1` — there is
   exactly one way to seat nobody.
6. Every function keeps its type hints, its docstring, and its `Raises:`
   section.

## Constraints

- **Use `//` in `arrangements`, not `/`, and understand that nothing on this
  page will catch you if you do not.** Every assert in the starter passes
  with true division, because `20.0 == 20` is `True` and these results are
  small enough that a float holds them exactly:

  ```text
  arrangements(5, 2) with / : 20.0
  passes `== 20`? True
  arrangements(25, 3) with / : 13800.0
  ```

  Here is what actually goes wrong. A Python `int` has no size limit — it
  grows as large as your memory allows. A `float` has a fixed budget of about
  16 significant digits, and past `2 ** 53`, which is `9007199254740992`, it
  starts quietly rounding. Factorials cross that line fast. The first place
  the two answers genuinely differ is `n = 23`, `k = 19`:

  ```text
  exact (//) : 1077167364120207360000
  float  (/) : 1.0771673641202074e+21
  ```

  Those low digits are wrong and nothing warns you. Push a little further and
  Python stops pretending:

  ```text
  Traceback (most recent call last):
      fact(200) / fact(0)
      ~~~~~~~~~~^~~~~~~~~
  OverflowError: integer division result too large for a float
  ```

  So `//` is not a formatting preference. It is what keeps an exact count
  exact. That the self-checks do not enforce it is a useful thing to learn
  about self-checks.

- **Do not use `math.factorial`.** It exists, it is faster than anything you
  will write today, and you should reach for it in real code. The point right
  now is to build the thing, so that when you read someone else's recursive
  function you recognise the shape.
- **Keep the recursive body to one expression after the base case.** If your
  recursive function needs a loop, an accumulator and three temporary
  variables, you have written the iterative version with extra machinery. The
  whole reason to reach for recursion is that the rule reads like the
  mathematics.
- **Do not raise the recursion limit to make a big input work.** Python
  allows roughly 1000 nested calls by default. If you need `factorial(5000)`,
  the answer is the iterative version, not a bigger allowance. Lecture 3,
  section 5 explains what that limit is protecting.
- **Have `arrangements` guard `k > n` itself, before either factorial is
  called.** Without that guard, `arrangements(3, 5)` computes
  `factorial(3 - 5)`, which is `factorial(-2)`, which raises `ValueError: n
  must be non-negative` — a true statement about a number the caller never
  passed. Validate against the contract you published, in the words of the
  parameters you published.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-recursion-intro.py
0! = 1
5! = 120
20! = 2432902008176640000
Seating 2 of 5 volunteers: 20 ways
Iterative and recursive agree for n = 0 through 15.
All checks passed.
```

The fifth line is the one that earns its place. It is not a print statement
congratulating you; it is a report on the `for n in range(16)` loop above,
which compared two separately written functions sixteen times and found no
disagreement.

## Steps

1. Create the file, paste the starter, run it. `NotImplementedError`, as
   expected.
2. Write `factorial_iterative` first. It is the version you can check by
   hand: `5 * 4 * 3 * 2 * 1 = 120`. Get its asserts green before you touch
   recursion at all.
3. Write `factorial_recursive`. **Write the base case line before the
   recursive line, every time, for the rest of your career.** A recursive
   function with no base case is an infinite loop that also eats memory. The
   comparison loop over `range(16)` is your proof that the two agree.
4. Write `arrangements`. Sanity-check `arrangements(5, 2) = 20` by hand: five
   people could take the first chair, four are left for the second,
   `5 * 4 = 20`.
5. Open a REPL and run `factorial_recursive(2000)`. It stops:

   ```text
   Traceback (most recent call last):
       return n * factorial_recursive(n - 1)
                  ~~~~~~~~~~~~~~~~~~~^^^^^^^
     [Previous line repeated 994 more times]
   RecursionError: maximum recursion depth exceeded
   ```

   `sys.getrecursionlimit()` is `1000` on a stock install, and each call uses
   one slot, so a recursion needing 2001 of them stops well short. It stops a
   little before 1000 rather than exactly at it because the REPL itself is
   already a few calls deep.

   Now run `factorial_iterative(2000)`. It computes the answer without
   complaining. **Then try to print it, because this is where a lot of people
   decide their code is broken when it is not:**

   ```text
   Traceback (most recent call last):
       print(factorial_iterative(2000))
       ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
   ```

   Read that carefully. Nothing failed in your function, and there is no
   limit on how big a Python integer can be. `2000!` has 5,736 digits, and
   Python since 3.11 refuses to *convert* an integer that long into text
   unless you ask it to. Turning a huge number into decimal digits takes work
   that grows with the square of the length, so an unguarded conversion is an
   easy way to freeze a web server. `len(str(factorial_iterative(1000)))` is
   `2568`, comfortably under the cap, and works fine.

   Write one sentence in a comment explaining the difference between the two
   failures. The one worth writing: the recursive version's memory grows with
   `n`, because every waiting multiplication holds a frame open, and the
   iterative version's does not, because it keeps one number and overwrites
   it.

## The Solution

```python
"""exercise-03-recursion-intro-solution.py — counting ways to seat volunteers.

Two factorials that agree: one built from a loop, one built from the
recurrence n! = n * (n - 1)!. Then one real use for them.

The self-checks at the bottom are the starter's, unchanged. The loop over
range(16) is the important one: it proves the two implementations agree
sixteen times running.
"""


def factorial_iterative(n: int) -> int:
    """Return n! computed with a loop.

    Args:
        n: A non-negative integer.

    Returns:
        The product 1 * 2 * ... * n, and 1 when n is 0.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    product = 1
    for factor in range(2, n + 1):
        product *= factor
    return product


def factorial_recursive(n: int) -> int:
    """Return n! by calling itself. Same contract as factorial_iterative.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


def arrangements(n: int, k: int) -> int:
    """Return the number of ordered ways to seat k of n volunteers.

    Args:
        n: How many volunteers turned up.
        k: How many chairs there are.

    Returns:
        n! // (n - k)!

    Raises:
        ValueError: If n or k is negative, or if k is greater than n.
    """
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    if k > n:
        raise ValueError("k must not be greater than n")
    return factorial_iterative(n) // factorial_iterative(n - k)


if __name__ == "__main__":
    assert factorial_iterative(0) == 1, factorial_iterative(0)
    assert factorial_iterative(1) == 1, factorial_iterative(1)
    assert factorial_iterative(5) == 120, factorial_iterative(5)
    assert factorial_iterative(10) == 3_628_800, factorial_iterative(10)
    assert factorial_iterative(20) == 2_432_902_008_176_640_000

    for n in range(16):
        assert factorial_recursive(n) == factorial_iterative(n), n

    for fn in (factorial_iterative, factorial_recursive):
        try:
            fn(-1)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fn.__name__}(-1) should raise ValueError")

    assert arrangements(5, 0) == 1, arrangements(5, 0)
    assert arrangements(5, 2) == 20, arrangements(5, 2)
    assert arrangements(6, 3) == 120, arrangements(6, 3)
    assert arrangements(4, 4) == 24, arrangements(4, 4)

    try:
        arrangements(3, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("k greater than n should raise ValueError")

    print(f"0! = {factorial_iterative(0)}")
    print(f"5! = {factorial_recursive(5)}")
    print(f"20! = {factorial_iterative(20)}")
    print(f"Seating 2 of 5 volunteers: {arrangements(5, 2)} ways")
    print("Iterative and recursive agree for n = 0 through 15.")
    print("All checks passed.")
```

**The base case is `n == 0`, because the definition is `0! = 1`.** Writing
`if n == 1: return 1` looks equally true and is a trap:
`factorial_recursive(0)` then never meets a stopping condition and walks off
into `-1`, `-2`, `-3`. The first self-check in the file is `factorial(0)`
precisely so that this bug cannot survive your first run. When you choose a
base case, ask what the smallest **legal** input is, not what the smallest
input you happened to think of is.

**The negative guard sits above the base case, and it runs on every call.**
That is one extra comparison per call, and after the first call it can never
fire — `n - 1` from a non-negative `n` that was not `0` is still
non-negative. It buys something worth more than the comparison costs: the
function checks its own contract no matter who calls it, including itself.
The alternative is a public function that validates once and a private
`_factorial` that recurses without checking. That is the right shape for
code in a hot loop, and it is overbuilding here.

**The recursive branch has no `if` and no accumulator.**
`return n * factorial_recursive(n - 1)` is the rule `n! = n * (n - 1)!`
written in Python with the punctuation changed. That is the whole appeal.

**`n - 1` is what makes it stop.** Every recursive call has to make the
problem strictly smaller in a way that actually reaches the base case. `n -
1` on a non-negative whole number marches down to `0` and halts. `n`
unchanged, or `n - 0`, or `n // 1`, all recurse forever. Before you run a
recursive function, look at the argument in the recursive call and convince
yourself it shrinks.

**`arrangements` uses the iterative factorial.** Nothing in the brief demands
recursion here, and somebody who asks for `arrangements(5000, 3)` deserves an
answer rather than a `RecursionError`. Once both versions exist and agree,
you get to pick per call site. The recursive one is the one you read; the
iterative one is the one you ship.

**`arrangements(5, 0)` is `1`, and that is not a special case.** `5! // 5!`
is `1`, which the arithmetic produces without help. There is exactly one way
to seat nobody: the empty seating. An edge case that falls out of the formula
is a sign the formula is right.

## Download and run

Download
[exercise-03-recursion-intro-solution.py](./exercise-03-recursion-intro-solution.py)
and run it:

```bash
python exercise-03-recursion-intro-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-03-recursion-intro.py`.

## Common bugs to catch

- **`ValueError: n must be non-negative` from `factorial_recursive(0)`.** Your
  base case is `if n == 1`:

  ```text
  Traceback (most recent call last):
      return n * factorial_recursive(n - 1)
                 ~~~~~~~~~~~~~~~~~~~^^^^^^^
      raise ValueError("n must be non-negative")
  ValueError: n must be non-negative
  ```

  `0` sailed straight past the stop line and the next call arrived with `-1`,
  where the negative guard caught it. Without that guard the same mistake
  shows up as `RecursionError: maximum recursion depth exceeded` after a
  thousand calls. Both are one bug: a base case that a legal input can step
  over.

- **`RecursionError` on a perfectly ordinary input like `5`.** Your recursive
  call passes `n` instead of `n - 1`, so the argument never shrinks and every
  call is identical to the last. Look at the argument in the recursive call
  first, every time.

- **`AssertionError: 0` on the `factorial_iterative(5)` check.** You started
  the accumulator at `0`:

  ```text
  AssertionError: 0
  ```

  Anything times zero is zero. Products start at `1`; sums start at `0`. The
  starting value of an accumulator is always the value that changes nothing
  under the operation you are about to apply.

- **`AssertionError: 24` where you expected `120`.** Off by one in the loop
  bound:

  ```text
  AssertionError: 24
  ```

  `24` is `4!`, one step short. `range` stops *before* its second argument, so
  `range(1, 5)` gives you `1, 2, 3, 4` and never multiplies by `5`. You want
  `range(2, n + 1)`. Starting at `2` instead of `1` is a free saving —
  multiplying by one changes nothing — but the `n + 1` is not optional.

- **`TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'`.**
  Your base case has a bare `return`, or a branch with no `return` at all:

  ```text
  Traceback (most recent call last):
      return n * factorial_recursive(n - 1)
                 ~~~~~~~~~~~~~~~~~~~^^^^^^^
    [Previous line repeated 2 more times]
  TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
  ```

  A function that runs out of body hands back `None`, and `1 * None` is this
  error. Notice where it happened: the traceback shows the multiplication
  line repeated, because the failure is on the way back *up*. All the calls
  went down successfully; it broke when the deepest one tried to hand
  something back.

- **`arrangements(3, 5)` raises from inside a factorial rather than from your
  own guard.**

  ```text
  Traceback (most recent call last):
      return factorial_iterative(n) // factorial_iterative(n - k)
                                       ~~~~^^^^^^^
      raise ValueError("n must be non-negative")
  ValueError: n must be non-negative
  ```

  `n - k` is `-2`, which the factorial correctly rejects — but the message
  talks about `n`, and the caller passed two perfectly non-negative numbers.
  A true message about the wrong thing is worse than no message. Guard
  `k > n` yourself and name the real problem.

- **`arrangements` returns floats and every check still passes.** You used
  `/`. Nothing on this page will tell you. Go back and read the first
  constraint — the failure is real, it just starts at inputs bigger than the
  ones being tested.

## Under the hood

<details>
<summary>Under the hood — the call stack, and where the recursion limit comes from</summary>

Every time any function is called, Python builds a small workspace for that
one call: somewhere to keep the parameters and local variables, and a note
saying which line to come back to when it finishes. That workspace is a
**frame**, and frames pile up like a stack of plates — the newest one on top,
and only the top one running. When a call returns, its plate comes off and
the one underneath carries on from its note.

An ordinary program builds a handful of plates. A recursive one builds `n` of
them before a single multiplication happens:

```text
factorial_recursive(3)
  frame: n = 3   waiting on factorial_recursive(2)
    frame: n = 2   waiting on factorial_recursive(1)
      frame: n = 1   waiting on factorial_recursive(0)
        frame: n = 0   returns 1
      returns 1 * 1 = 1
    returns 2 * 1 = 2
  returns 3 * 2 = 6
```

Four frames go down, and the multiplying happens on the way back up.
[Lecture 3, section 4](../lecture-notes/03-recursion.md) draws this in more
detail; it is the same picture.

**Where the limit comes from.** Frames live in a region of memory called the
stack, and the operating system hands each thread a fixed amount of it —
commonly around 1 MB on Windows and 8 MB on Linux. Run past the end of it and
the operating system kills the process outright, with no traceback and no
Python-level error, because the machinery that would print the traceback also
needs stack space.

So CPython counts. It keeps its own ceiling, `sys.getrecursionlimit()`,
defaulting to `1000`, and raises a normal Python exception when you reach it:

```text
>>> import sys
>>> sys.getrecursionlimit()
1000
```

`RecursionError` is therefore a **kindness**, not a punishment. It converts
"your process vanished" into an exception you can read, catch and fix. The
limit is deliberately set below what the real stack could take, so the
guardrail fires before the cliff.

You can move it with `sys.setrecursionlimit()`, and you should treat that the
way you treat disabling a smoke alarm. It does not give you more stack; it
only raises the number at which Python stops counting. Set it high enough and
you go straight back to a hard crash. From module level, a stock 3.13 install
runs `factorial_recursive(997)` and fails at `998` — the few missing slots
are the frames Python itself is already using.

**One thing Python deliberately does not do.** Look at this shape:

```python
def factorial_tail(n: int, acc: int = 1) -> int:
    """Return n! in tail-recursive form. Python still builds every frame."""
    if n == 0:
        return acc
    return factorial_tail(n - 1, acc * n)
```

The recursive call is the last thing that happens — nothing is waiting on its
result, so in principle the current frame could be thrown away and reused.
That optimisation is called **tail-call elimination**, and Scheme and Scala
do it, which makes this shape run forever in constant memory there.

CPython does not, on purpose:

```text
factorial_tail(2000) -> RecursionError: maximum recursion depth exceeded
```

The reason is the traceback. Keeping every frame is exactly what lets an
error report the whole path that led to it, and Python's designers have
consistently judged that debuggability worth more than the optimisation. So
in Python, "make it tail recursive" is not a fix for stack depth. The fix for
stack depth is a loop.

</details>

<details>
<summary>Under the hood — why one recursive call is cheap and two are ruinous</summary>

`factorial(n)` makes `n` calls. That is linear: double `n`, double the work.

Now change one thing — let the body call itself *twice*:

```python
def fibonacci_recursive(n: int) -> int:
    """Return the nth Fibonacci number the naive way."""
    if n < 2:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
```

Same idea, same tidy two-claim shape, wildly different cost:

```text
fibonacci_recursive(30) = 832040 in 0.088 s
factorial_recursive(30) in 0.000003 s
```

Roughly thirty thousand times slower at the same `n`. Nothing is wrong with
the code. The difference is that each call now branches into two, so the
number of calls roughly multiplies by 1.6 every time `n` goes up by one
instead of adding one. Count them and `fib(30)` makes **2,692,537** calls to
produce a six-digit answer, because almost every one recomputes something
another branch already worked out:

```text
fib(30) = 832040   total calls = 2692537
  fib(20) computed 89 times
  fib(10) computed 10946 times
  fib(5) computed 121393 times
  fib(2) computed 514229 times
```

Two lessons come out of that.

**A recursive function's cost is set by how many times the body calls
itself.** One call is a chain. Two calls is a tree, and trees explode. Count
the calls in the body before you worry about anything else.

**Caching is worth exactly what the repeats are worth.** Python ships a
one-line cache, `functools.lru_cache`, which remembers what a function
returned for arguments it has seen before. On Fibonacci it is transformative,
because the repeats are the whole problem:

```text
fib(30) naive: 0.106 s   cached: 0.000018 s
calls saved: CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```

31 distinct subproblems instead of over a million calls. That technique has a
name, **memoization**, and this is its textbook case.

Now watch the same cache do nothing useful. Time the cached factorial in a
loop and it looks like a 250x win:

```text
plain recursive  x2000: 0.151 s
lru_cache        x2000: 0.0006 s
cache info: CacheInfo(hits=1999, misses=501, maxsize=None, currsize=501)
```

Read the cache info before you believe it. 501 misses — one for each of `0`
through `500` — then 1999 hits, because the benchmark loop asked for
`factorial(500)` two thousand times. The first call did all the work and the
other 1999 read a stored answer. That benchmark is measuring dictionary
lookups, not factorials. `lru_cache` on a function whose inputs never repeat
buys nothing at all and costs memory.

Before you believe any caching speedup, ask what the hit rate was.

</details>

## Acceptance checklist

- [ ] `python exercise-03-recursion-intro.py` prints five lines and `All checks passed.`
- [ ] `factorial_recursive` contains a call to itself, and `factorial_iterative` does not.
- [ ] Both return `1` for `0`.
- [ ] Both raise `ValueError` for negative input.
- [ ] `arrangements` uses `//` and checks `k > n` itself.
- [ ] You have run `factorial_recursive(2000)` and seen the `RecursionError`.
- [ ] You have run `print(factorial_iterative(2000))` and seen that the
      failure is about printing, not about computing.
- [ ] Committed to Git with a message like `Add Week 4 exercise 3: recursion intro`.

## Stretch

- Time both versions on `n = 500` with `time.perf_counter`, looped a couple
  of thousand times:

  ```text
  factorial_iterative(500) x2000: 0.090 s
  factorial_recursive(500) x2000: 0.155 s
  recursive / iterative = 1.73x
  ```

  Your numbers will differ; the ratio is the part worth keeping. A function
  call in Python is not free — it builds a frame, binds the parameters and
  unwinds on the way out — and the recursive version pays that 500 times per
  call where the loop pays it once. Write the number you measured in a
  comment.

- Write `fibonacci_recursive(n)` the naive way and time `n = 30`. Then add
  `functools.lru_cache` and time it again. Then add `lru_cache` to your
  *factorial* and time that, and explain why one of those two speedups is
  real and the other is an artefact of how you wrote the benchmark. The
  second Under the hood block above has the answer if you get stuck, but
  work it out first.

- Rewrite `factorial_recursive` in tail-recursive form, with an accumulator
  parameter, then confirm it still runs out of stack:

  ```python
  def factorial_tail(n: int, acc: int = 1) -> int:
      """Return n! in tail-recursive form. Python still builds every frame."""
      if n == 0:
          return acc
      return factorial_tail(n - 1, acc * n)
  ```

  ```text
  factorial_tail(2000) -> RecursionError: maximum recursion depth exceeded
  ```

  Knowing that Python does not eliminate tail calls, and why, saves you an
  afternoon someday.

Next: [Exercise 4 — Scope Mystery](./exercise-04-scope-mystery.md).
