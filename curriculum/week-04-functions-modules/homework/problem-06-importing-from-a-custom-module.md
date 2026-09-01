# Homework Problem 6 — Importing From a Custom Module

> **Topic:** splitting one program across two files, importing your own module by filename, and the `__main__` guard that stops an import from making noise
> **Lecture:** [Lecture Note 4 — Modules and Imports](../lecture-notes/04-modules-and-imports.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** every program you have written so far has been one file. Real programs are folders of files that call each other, and the joint between two of them is where beginners lose an afternoon. This is that joint, at the smallest size it comes in: two files, one import line, and every mistake you are going to make later already visible.

## The Brief

Up to now, one program has meant one file. That stops here.

You are writing **two** files that live side by side in your `homework/`
folder:

```text
homework/
├── mymath.py        ← the library. Defines things. Runs nothing.
└── use_mymath.py    ← the program. Imports things. Does the work.
```

`mymath.py` holds three functions and nothing else:

- `square(n: int) -> int` — `n` times itself.
- `cube(n: int) -> int` — `n` times itself twice.
- `is_prime(n: int) -> bool` — `True` when `n` has no divisors except
  1 and itself.

A **prime** is a whole number with exactly two divisors: 1 and itself. 7
is prime. 9 is not, because 3 divides it. 1 is not, because it only has
one divisor. The way to check is **trial division** — try every possible
divisor and see if any of them go in evenly. You do not have to try all of
them, only up to the square root of `n`, and the "Why it works" section
explains why that is enough rather than just asserting it.

`use_mymath.py` imports all three and has a `main()` that:

1. Prints `square(7)` and `cube(7)`.
2. Lists every prime from 2 to 30, inclusive.

Then you run it from a terminal:

```bash
cd homework
python use_mymath.py
```

If you get `ModuleNotFoundError: No module named 'mymath'`, the two files
are not in the same folder, or you are not standing in that folder. That
error has a whole section further down, because it is the one everybody
hits.

## Starter

Two files. Save both in your `homework/` folder.

`mymath.py`:

```python
"""A few small integer helpers, written to be imported by other files."""


def square(n: int) -> int:
    """Return `n` squared.

    Args:
        n: Any integer.

    Returns:
        n * n.

    Example:
        >>> square(7)
        49
    """
    return 0  # TODO: n * n


def cube(n: int) -> int:
    """Return `n` cubed."""
    return 0  # TODO: n * n * n


def is_prime(n: int) -> bool:
    """Return True if `n` is prime, using trial division."""
    # TODO: anything below 2 is not prime
    # TODO: try every divisor from 2 up to int(n ** 0.5) + 1
    return True


def _demo() -> None:
    """Self-test the three helpers when the module is run directly."""
    print(square(7), cube(7), is_prime(29), is_prime(1))


if __name__ == "__main__":
    _demo()
```

`use_mymath.py`:

```python
"""Demo script for the sibling `mymath` module."""

from mymath import cube, is_prime, square


def primes_between(low: int, high: int) -> list[int]:
    """Return every prime in the inclusive range low..high.

    Args:
        low: Lower bound, inclusive.
        high: Upper bound, inclusive.

    Returns:
        A sorted list of primes.

    Example:
        >>> primes_between(2, 10)
        [2, 3, 5, 7]
    """
    return []  # TODO: every n in range(low, high + 1) where is_prime(n)


def main() -> None:
    """Print the squares, cubes and primes the homework asks for."""
    print(f"square(7) = {square(7)}")
    print(f"cube(7)   = {cube(7)}")
    print(f"primes 2..30: {primes_between(2, 30)}")


if __name__ == "__main__":
    main()
```

Both run as pasted. `python use_mymath.py` prints zeroes and an empty
list, which is wrong in a way you can see, and — more importantly — proves
the import line already works before you have written a single useful
line.

`cube` and `is_prime` are missing most of their docstrings. Writing those
is part of the work.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-06-importing-from-a-custom-module.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `mymath.py` defines `square`, `cube` and `is_prime`, all with type
   hints and full docstrings.
2. `is_prime` returns `False` for every number below 2.
3. `is_prime` uses trial division up to `int(n ** 0.5) + 1`.
4. `use_mymath.py` imports the three functions from `mymath` and defines
   `primes_between` and `main`.
5. `python use_mymath.py`, run from the folder holding both files, prints
   the three lines in **Expected output**.
6. `python mymath.py` on its own prints its demo line.
7. `python -c "import mymath"` prints nothing.

## Constraints

- **Both files get a `__main__` guard.** Without one on `mymath.py`,
  every run of `use_mymath.py` prints `49 343 True False` before its own
  first line, as a side effect of the import. That guard is the entire
  reason a module can also be a script.
- **`is_prime` guards `n < 2` before it loops.** Not decoration — it is
  the correctness of the function. The loop for `n = 0` and `n = 1` is
  empty, so without the guard both fall through to `return True` and the
  function cheerfully declares 0 and 1 prime.
- **The `+ 1` in `range(2, int(n ** 0.5) + 1)` is load-bearing.** `range`
  excludes its endpoint, and the square root itself has to be tested.
  Common bugs to catch shows the wreckage when it is missing.
- **Do not name your module after something in the standard library.**
  `mymath.py` is the name for a reason. A file called `random.py` or
  `json.py` in your folder shadows the real one for every file beside it,
  and the failure looks nothing like what you did.
- **`primes_between` lives in `use_mymath.py`, not in `mymath.py`.** The
  module holds general-purpose pieces. The script holds what this
  particular program wants. Deciding which side of the line a function
  belongs on is the actual skill this problem is teaching.
- **`main()` prints; `primes_between` returns.** Same split as every
  other problem this week, and it is why `primes_between` has a doctest
  and `main` cannot.

## Expected output

Run from inside the folder holding both files:

```bash
cd homework
python use_mymath.py
```

```text
square(7) = 49
cube(7)   = 343
primes 2..30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

Ten primes. Count them.

The module works standalone too, which is what its own guard is for:

```bash
python mymath.py
```

```text
49 343 True False
```

That last `False` is `is_prime(1)` — the `n < 2` guard doing its job.

And importing it makes no noise at all:

```bash
python -c "import mymath; print('nothing printed above this line')"
```

```text
nothing printed above this line
```

If the demo line appears above that sentence, your `__main__` guard is
missing or mis-indented.

Both files' docstring examples are real tests:

```bash
python -m doctest mymath.py use_mymath.py
```

Silence means every example passed. For the count:

```bash
python -m doctest mymath.py -v
```

The last three lines:

```text
3 tests in 5 items.
3 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save both Starters, as `mymath.py` and `use_mymath.py`, in that same
   folder.
3. Run `python use_mymath.py` **before writing anything**. You should get
   `square(7) = 0`, `cube(7) = 0` and an empty list. The numbers are
   wrong and the import is right, which is the order you want to find
   things out in.
4. Fill in `square` and `cube`. Run again. Two lines are now correct.
5. Fill in `is_prime`, guard first, loop second. Check it directly:
   `python -c "from mymath import is_prime; print([n for n in range(0, 12) if is_prime(n)])"`
   should print `[2, 3, 5, 7, 11]`. If `0` and `1` are in that list, the
   guard is missing.
6. Fill in `primes_between`. Run `python use_mymath.py`. All three lines
   correct.
7. Break the import on purpose, once, so you recognise it later. Move up
   one folder and run `python -c "import use_mymath"`. Read the
   `ModuleNotFoundError`. Then `cd` back.
8. Prove the guard works: `python -c "import mymath"` must print nothing.
9. Finish the two thin docstrings, then run
   `python -m doctest mymath.py use_mymath.py`.
10. Compare against **The Solution**, tick the acceptance checklist, and
    commit both files:
    `git add homework/mymath.py homework/use_mymath.py` then
    `git commit -m "Week 4 homework: importing from a custom module"`.

## The Solution

The downloadable answer is **one** file, because a page here ships exactly
one runnable file and `use_mymath.py` on its own is not runnable — without
`mymath.py` beside it, it stops on line 3. So the download stacks the two
halves in one file, with a comment marking the seam. It is the same code,
in the same order, with the import line removed because both halves are
now in the same place.

```python
"""Small integer helpers, and the script that uses them, in one file.

Week 4 homework, problem 6, Code Crunch Convos.

The brief asks for **two** files - ``mymath.py`` with the helpers, and
``use_mymath.py`` that imports them - and two files is what you should
write. This download is one file for a plain reason: every page here ships
exactly one runnable answer, and a lone ``use_mymath.py`` is not runnable.
On its own it stops on line 3 with ``ModuleNotFoundError: No module named
'mymath'``, because the thing it imports is not there.

So this file is the two halves stacked. ``square``, ``cube`` and
``is_prime`` are the ``mymath.py`` half. ``primes_between`` and ``main``
are the ``use_mymath.py`` half. To get the two files the brief wants, cut
between them and put ``from mymath import cube, is_prime, square`` at the
top of the second half. The page shows both files written out in full.
"""


def square(n: int) -> int:
    """Return `n` squared.

    Args:
        n: Any integer.

    Returns:
        n * n.

    Example:
        >>> square(7)
        49
    """
    return n * n


def cube(n: int) -> int:
    """Return `n` cubed.

    Args:
        n: Any integer.

    Returns:
        n * n * n.

    Example:
        >>> cube(7)
        343
    """
    return n * n * n


def is_prime(n: int) -> bool:
    """Return True if `n` is prime, using trial division.

    Args:
        n: Any integer. Values below 2 are never prime.

    Returns:
        True if n has no divisor other than 1 and itself.

    Example:
        >>> is_prime(29)
        True
    """
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


# Everything below this line is the `use_mymath.py` half.


def primes_between(low: int, high: int) -> list[int]:
    """Return every prime in the inclusive range low..high.

    Args:
        low: Lower bound, inclusive.
        high: Upper bound, inclusive.

    Returns:
        A sorted list of primes.

    Example:
        >>> primes_between(2, 10)
        [2, 3, 5, 7]
    """
    return [n for n in range(low, high + 1) if is_prime(n)]


def main() -> None:
    """Print the squares, cubes and primes the homework asks for."""
    print(f"square(7) = {square(7)}")
    print(f"cube(7)   = {cube(7)}")
    print(f"primes 2..30: {primes_between(2, 30)}")


if __name__ == "__main__":
    main()
```

**The two files, which is what you hand in.**

`homework/mymath.py`:

```python
"""A few small integer helpers, written to be imported by other files."""


def square(n: int) -> int:
    """Return `n` squared.

    Args:
        n: Any integer.

    Returns:
        n * n.

    Example:
        >>> square(7)
        49
    """
    return n * n


def cube(n: int) -> int:
    """Return `n` cubed.

    Args:
        n: Any integer.

    Returns:
        n * n * n.

    Example:
        >>> cube(7)
        343
    """
    return n * n * n


def is_prime(n: int) -> bool:
    """Return True if `n` is prime, using trial division.

    Args:
        n: Any integer. Values below 2 are never prime.

    Returns:
        True if n has no divisor other than 1 and itself.

    Example:
        >>> is_prime(29)
        True
    """
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def _demo() -> None:
    """Self-test the three helpers when the module is run directly."""
    print(square(7), cube(7), is_prime(29), is_prime(1))


if __name__ == "__main__":
    _demo()
```

`homework/use_mymath.py`:

```python
"""Demo script for the sibling `mymath` module."""

from mymath import cube, is_prime, square


def primes_between(low: int, high: int) -> list[int]:
    """Return every prime in the inclusive range low..high.

    Args:
        low: Lower bound, inclusive.
        high: Upper bound, inclusive.

    Returns:
        A sorted list of primes.

    Example:
        >>> primes_between(2, 10)
        [2, 3, 5, 7]
    """
    return [n for n in range(low, high + 1) if is_prime(n)]


def main() -> None:
    """Print the squares, cubes and primes the homework asks for."""
    print(f"square(7) = {square(7)}")
    print(f"cube(7)   = {cube(7)}")
    print(f"primes 2..30: {primes_between(2, 30)}")


if __name__ == "__main__":
    main()
```

Run the pair and you get the same three lines the one-file download
prints:

```bash
cd homework
python use_mymath.py
```

```text
square(7) = 49
cube(7)   = 343
primes 2..30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

**Why it works.**

**`from mymath import cube, is_prime, square` names exactly what it uses.**
The word `mymath` is the *filename* with the `.py` taken off. Python goes
looking for a file called `mymath.py` in the folder the running script came
from, finds it, runs it, and pulls those three names out. Nothing is
registered anywhere and nothing is installed. The filename is the module
name.

Three names in a twenty-line script is squarely `from` territory. The other
form, `import mymath`, would mean writing `mymath.square(7)` at every call
site, which is more typing but makes the origin of every name obvious.
[Lecture Note 4 §2](../lecture-notes/04-modules-and-imports.md) lays out
the trade-off properly. The three names are listed alphabetically because
that is what `isort` and most formatters produce, and it keeps a long list
scannable.

**`if n < 2: return False` is the correctness of `is_prime`, not a
politeness.** Trial division loops over `range(2, int(n ** 0.5) + 1)`. For
`n = 0` that is `range(2, 2)`, which is empty. For `n = 1` it is
`range(2, 2)` as well. An empty loop body never runs, so the function falls
straight through to `return True`. Here is what the version without the
guard reports for 0 through 9:

```text
[0, 1, 2, 3, 5, 7]
```

Two wrong entries at the front. One `if` fixes both.

**Why stop at the square root?** Because divisors come in pairs. If `d`
divides `n`, then so does `n / d`, and one of that pair is always at or
below the square root. `36 = 2 × 18 = 3 × 12 = 4 × 9 = 6 × 6`. Read the
left-hand column: 2, 3, 4, 6 — every one at or under 6, which is
`sqrt(36)`. So if there is a divisor at all, you will meet the smaller half
of the pair before you pass the square root, and everything above it is
wasted work.

**And why the `+ 1`?** Because `range` stops *before* its endpoint, and the
square root itself is a divisor you must test. For `n = 49`,
`int(49 ** 0.5)` is `7`, and `range(2, 8)` includes 7, which correctly
finds that 49 is 7 times 7.

**`primes_between` is its own function, not a loop inside `main`.** The
brief asks `main()` to "list the primes between 2 and 30". Pulling the
list-building out into a named, hinted function means the printing stays in
`main` and the computing can be tested by comparing a return value — which
is exactly what its doctest does. `main` has no doctest because you cannot
compare printed output that way.

**`range(low, high + 1)` is what makes the range inclusive.** The brief
says "between 2 and 30 (inclusive)", and `range` is half-open. 30 is not
prime, so this particular `+ 1` does not change the printed answer — which
is exactly why it is easy to get wrong and never find out. Try `2..29` and
`2..31` and watch the boundary move.

**Both files have a `__main__` guard, and they do different jobs with it.**
`use_mymath.py`'s guard runs the program. `mymath.py`'s guard lets the
module double as its own smoke test: `python mymath.py` prints
`49 343 True False`, while `from mymath import square` prints nothing.
Without that guard on `mymath.py`, the demo line would appear above every
run of `use_mymath.py`, because importing a module runs it.

## Download and run

Download [problem-06-importing-from-a-custom-module-solution.py](./problem-06-importing-from-a-custom-module-solution.py)
and run it:

```bash
python problem-06-importing-from-a-custom-module-solution.py
```

**Read this before you use it.** That download is one file, and the
homework is two. It is one file because every page in this course ships a
single runnable answer, and `use_mymath.py` alone is not one — with no
`mymath.py` beside it, it stops on line 3 with `ModuleNotFoundError`. A
download that cannot run is worth nothing to you.

So the file stacks both halves, with a comment on the seam. To get the two
files you hand in: cut at that comment, save the top half as `mymath.py`
and the bottom half as `use_mymath.py`, and put
`from mymath import cube, is_prime, square` at the top of the second one.
Both files are written out in full above, under **The Solution**, so you
can copy them directly instead.

## Common bugs to catch

- **`ModuleNotFoundError: No module named 'mymath'`.** The single most
  common failure in this problem, and worth understanding rather than
  memorising. When you run a script, Python puts **the folder that script
  lives in** at the front of its search path — not the folder you happen
  to be standing in. So `import mymath` looks beside `use_mymath.py`.

  ```text
  Traceback (most recent call last):
    File "...\homework\use_mymath.py", line 3, in <module>
      from mymath import square
  ModuleNotFoundError: No module named 'mymath'
  ```

  Two things fix it. `cd homework` first, or run
  `python homework/use_mymath.py` from the parent — the second works from
  anywhere, because Python still puts `homework/` on the path. What does
  *not* work is `python -c "import use_mymath"` from the parent folder,
  because then the search starts where you are standing and `mymath` is a
  folder down.
- **Naming your module after a standard library one.** Call a file
  `random.py` and every file beside it that says `import random` gets
  yours instead:

  ```text
  AttributeError: module 'random' has no attribute 'randint' (consider renaming '...\random.py' since it has the same name as the standard library module named 'random' and prevents importing that standard library module)
  ```

  Python 3.13 spells out the cause, which is kind of it — older versions
  gave you only the first half of that sentence and left you to work out
  the rest. The same trap is waiting under `json.py`, `email.py`,
  `socket.py` and `test.py`. `mymath.py` is safe.

  A footnote, because it will confuse you otherwise: `math.py` does
  **not** shadow anything. `math` is compiled into the interpreter rather
  than being a `.py` file on the search path, and built-in modules are
  found before the path is consulted at all.
  `python -c "import sys; print('math' in sys.builtin_module_names)"`
  prints `True`. Do not use the name anyway — the rule "never name a file
  after a standard library module" is easier to follow than the list of
  exceptions.
- **Missing the `n < 2` guard.** Covered above. The tell is `0` and `1`
  appearing in a list of primes. You will not see it with
  `primes_between(2, 30)`, which is a good argument for testing outside
  the range the brief hands you.
- **Dropping the `+ 1` from the range.** This is much worse than it
  looks. Here is `primes_between(2, 50)` with `range(2, int(n ** 0.5))`:

  ```text
  [2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49]
  ```

  4, 6, 8, 9, 15, 25, 35 and 49 are all in there. Without the `+ 1`, any
  number whose smallest divisor is at or above its square root is never
  tested at all, and the loop for small numbers is empty entirely.
- **`import mymath` and then calling `square(7)` bare.**

  ```python
  import mymath

  print(square(7))     # WRONG
  ```

  ```text
  NameError: name 'square' is not defined
  ```

  `import mymath` binds exactly one name: `mymath`. The functions live
  inside it, and you reach them as `mymath.square`. Pick one import form
  per file and stay with it.
- **`from mymath import *`.** It works here, and it is what the week's
  quiz marks as poor style. You cannot tell where `is_prime` came from by
  reading the file, and if `mymath` later grows a name that collides with
  one of yours, the collision is silent and the wrong function wins.
- **No `__main__` guard on `mymath.py`.** Then `python use_mymath.py`
  prints `49 343 True False` before its own first line. Beginners spend
  real time hunting for a `print` in `use_mymath.py` that does not exist.
- **Editing `mymath.py` and seeing no change.** Check that you saved it,
  and check that you are running the file you think you are. Python does
  cache the *compiled* form of a module in `__pycache__/`, but it
  re-checks the source timestamp on every run, so a saved change always
  takes effect. A `__pycache__` folder is normal and can be deleted at
  any time.

## Under the hood

<details>
<summary>Under the hood — a module runs once, and sys.modules is why</summary>

Here is the thing nobody tells you about `import`: it **runs the file**.

Not "reads the definitions out of it". Runs it, top to bottom, exactly as
if you had typed it at a prompt. Every line at the top level executes. A
`def` line executes by creating a function. A `print` at the top level
executes by printing.

Watch it. Put this in `noisy.py`:

```python
"""A module that says so out loud when it is set up."""

print("noisy is being set up")

VALUE = 42
```

Now import it twice in the same program:

```bash
python -c "import noisy; import noisy; print(noisy.VALUE)"
```

```text
noisy is being set up
42
```

Two `import` statements. One setup. The second `import` did not run the
file again — it did almost nothing at all.

**The cache is `sys.modules`,** a plain dict mapping module names to
module objects. Every `import` follows the same three steps:

1. Look the name up in `sys.modules`. If it is there, bind it and stop.
2. Otherwise find the file, create an empty module object, and — this is
   the important ordering — **put it in `sys.modules` before running it**.
3. Run the file top to bottom, filling that module object as it goes.

You can see the cache directly:

```bash
python -c "import sys, noisy; print('noisy' in sys.modules)"
```

```text
noisy is being set up
True
```

Step 2's ordering is what makes circular imports survivable: if `a`
imports `b` and `b` imports `a`, the half-built `a` is already in the
cache when `b` asks for it, so nothing loops forever. It may well be
missing names that were defined further down, which is why circular
imports produce baffling `ImportError`s rather than hangs.

**Why this matters for real programs.** Say `alpha.py` and `beta.py` both
import `noisy`, and `run_both.py` imports both:

```bash
python run_both.py
```

```text
noisy is being set up
alpha is ready
beta is ready
run_both is ready
```

One setup line, from two importers. If a module opens a file, reads
configuration or connects to something at its top level, that work happens
**once per program**, not once per importer — and every importer shares
the same module object. A module-level variable is genuinely global across
your whole program.

That shared-once behaviour is a feature when you want it and a trap when
you do not. It is also why the `__main__` guard exists: since importing
runs the file, anything at the top level that *does* something rather than
*defines* something becomes a side effect of somebody else's import. The
guard is the fence between the two.

**How Python decides which of the two it is.** Every module gets a
variable called `__name__`. When a file is run directly, Python sets its
`__name__` to the string `"__main__"`. When a file is imported,
`__name__` is the module's own name — `"mymath"`. That is all the guard
checks:

```python
if __name__ == "__main__":
    _demo()
```

Run directly, the condition is true and the demo runs. Imported, it is
false and the demo does not.

**Reloading, and why you almost never want to.** The cache means editing a
module during a long-running session has no effect. `importlib.reload`
forces a re-run:

```bash
python -c "import importlib, noisy; importlib.reload(noisy); print('reloaded')"
```

```text
noisy is being set up
noisy is being set up
reloaded
```

Two setups now. It exists, and it is a mess: objects created before the
reload still point at the old functions, so you end up with two versions
of the same class in memory at once. Restarting the program is almost
always the better answer.

</details>

<details>
<summary>Under the hood — where Python looks for mymath, in order</summary>

`import mymath` does not search your disk. It walks a short, ordered list
and stops at the first hit.

**First, built-in modules.** These are compiled into the interpreter
itself, not stored as `.py` files anywhere. `sys`, `math`, `time` and
about thirty others.

```bash
python -c "import sys; print('math' in sys.builtin_module_names, 'random' in sys.builtin_module_names)"
```

```text
True False
```

This is why a file called `math.py` cannot shadow the standard library's
`math` but a file called `random.py` can shadow its `random`. Do not rely
on the distinction. Just do not name files after standard library
modules.

**Second, `sys.modules`** — the cache from the previous block.

**Third, every folder in `sys.path`, in order.** That list is built when
Python starts:

- **`sys.path[0]`** is the folder containing the script you ran. Not your
  current directory. The script's folder. This is the single most
  important line in this block, and it is why `python homework/use_mymath.py`
  works from anywhere while `cd .. && python -c "import use_mymath"` does
  not.
- Then anything in the `PYTHONPATH` environment variable.
- Then the standard library's own folders.
- Then `site-packages`, where `pip install` puts things.

You can print the list from inside a script:

```python
"""Print the first folder Python searches for imports."""

import sys

print(sys.path[0])
```

Run that from anywhere and it names the folder the script is sitting in.

Two consequences worth carrying:

**Your own folder wins over `site-packages`.** A file named `requests.py`
in your project shadows the installed `requests` library for every file
beside it. Same trap as the standard library, one shelf further down.

**`python -c` and the interactive prompt behave differently.** With no
script file, `sys.path[0]` is the current directory instead. That is why
`python -c "import mymath"` works when you are standing in `homework/`
and fails when you are not, while `python homework/use_mymath.py` works
either way.

When an import fails, the fastest diagnosis is to print the path and look:

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

If the folder your module is in is not in that list, no amount of
rereading the import line will help.

</details>

## Acceptance checklist

- [ ] `mymath.py` and `use_mymath.py` are both in your `homework/`
      folder.
- [ ] `python use_mymath.py`, run from that folder, prints the three
      lines from **Expected output**.
- [ ] The prime list has exactly ten entries and starts at 2.
- [ ] `python mymath.py` prints `49 343 True False`.
- [ ] `python -c "import mymath"` prints nothing.
- [ ] `is_prime(0)` and `is_prime(1)` are both `False`.
- [ ] `is_prime(49)` is `False` — the `+ 1` in the range is present.
- [ ] `primes_between` lives in `use_mymath.py`, not in `mymath.py`.
- [ ] Both files have a `__main__` guard.
- [ ] Every function in both files has type hints and a docstring.
- [ ] `python -m doctest mymath.py use_mymath.py` prints nothing.
- [ ] You have seen `ModuleNotFoundError` once, on purpose, and know
      which folder caused it.
- [ ] Both files committed, with a message like
      `Week 4 homework: importing from a custom module`.

## Stretch

- **Add `factors(n: int) -> list[int]`** to `mymath.py`, returning every
  divisor of `n` including 1 and `n` itself. Then rewrite `is_prime` as
  `len(factors(n)) == 2`. It is a lovely one-liner and it is much slower,
  because it looks at every number up to `n` instead of stopping at the
  square root. Time both on 999983, which is prime, and you will feel the
  difference without needing a stopwatch.
- **Turn the two files into a package.** Make a folder called `mymathpkg`
  with an empty `__init__.py` and move `mymath.py` inside it. The import
  becomes `from mymathpkg.mymath import square`.
  [Lecture Note 4 §8](../lecture-notes/04-modules-and-imports.md) covers
  what `__init__.py` is for and what you can put in it to shorten that
  line back down.
- **Add `__all__` to `mymath.py`.** Set it to
  `["square", "cube", "is_prime"]` and then try `from mymath import *` in
  a scratch file. `_demo` no longer comes across. `__all__` is how a
  module states its public interface out loud instead of leaving people
  to guess from the underscores.
- **Sieve of Eratosthenes.** Trial division tests each number on its own.
  The sieve crosses out multiples instead, and finds every prime below a
  million in about the time trial division takes for ten thousand. Write
  `primes_up_to(limit: int) -> list[int]` using a list of booleans, and
  check its answer against `primes_between(2, limit)` for `limit = 1000`.
  Two implementations, one expected answer — the same move as problem 4.
- **Give `use_mymath.py` a command line.** Read the bounds from
  `sys.argv` so `python use_mymath.py 2 100` lists the primes in that
  range, falling back to 2 and 30 when no arguments are given. The week
  README's stretch goal 6 points at `argparse` for the grown-up version.

That is all six. Back to [the homework index](./README.md), then finish
[the Week 4 mini-project](../mini-project/README.md) and take
[the quiz](../quiz.md).
