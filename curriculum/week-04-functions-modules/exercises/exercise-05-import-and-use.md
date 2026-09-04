# Exercise 5 — Import and Use

> **Topic:** Standard library: `math`, `random`, `statistics`
> **Lecture:** [04 — Modules and Imports](../lecture-notes/04-modules-and-imports.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** the standard library is the difference between a beginner who rewrites `mean` by hand and somebody who ships. This page also teaches you how to test code that gives a different answer every time you run it, which trips up people years into the job. Both challenges and the mini-project import from the standard library, so get the two import forms into your fingers here.

## The Brief

The community garden keeps a paper logbook: how much rain fell each day,
which round beds got compost, and which plots are in this week's seedling
trial. You are turning four pages of that logbook into four functions, and
the body of every one is a single call into something that already ships with
Python.

A **module** is a file full of ready-made code with a name on it. `import
math` does not copy anything into your file — it finds `math`, runs it once,
and gives you one name, `math`, to reach through with a dot. So `math.pi` is
"the thing called `pi` inside the box called `math`". Python comes with
hundreds of these boxes, and together they are called the **standard
library**, because you always have them and never install them.

Three boxes do all the work here.

**`math`** handles the geometry: `math.pi` for the round beds, `math.ceil`
for the compost, because you cannot buy 1.77 bags.

**`statistics`** handles the rainfall summary. `mean`, `median`, `mode` and
`stdev` are one call each. Writing them yourself is how you introduce a bug
you will not notice for weeks — `mean` is easy to get right, `median` needs a
sort and an even-length case, `mode` needs a tally, and `stdev` needs the
right denominator and a numerically careful sum.

**`random`** picks the trial plots, and that one changes how you test.

Think about that last part before you write any code. `pick_trial_plots`
returns something different every run, so there is nothing fixed to compare
it against. But three things are true of *every* correct run: it returned
three plots, the three are all different, and each one is a real plot from
the list. Those three facts are false of the common wrong implementations,
which is exactly what makes them a good test. **When you cannot assert on the
value, assert on the shape.**

## Starter

Create `exercise-05-import-and-use.py` in your practice repo.

```python
"""exercise-05-import-and-use.py — one afternoon at the community garden.

Three standard-library modules, four functions, no pip install.
"""

import math
import random
import statistics
from math import isclose

RAINFALL_MM = [12.4, 8.1, 15.0, 9.6, 11.2, 8.1, 20.3]
PLOTS = ["Plot A", "Plot B", "Plot C", "Plot D", "Plot E", "Plot F"]


def circle_bed_area(diameter_m: float) -> float:
    """Return the area of a round planting bed, in square meters.

    Args:
        diameter_m: The bed's diameter in meters.

    Returns:
        The area, rounded to two decimals.
    """
    # TODO: math.pi times the radius squared. The radius is half the diameter.
    raise NotImplementedError


def bags_of_compost(area_m2: float, coverage_m2: float = 4.0) -> int:
    """Return how many whole bags of compost it takes to cover `area_m2`."""
    # TODO: math.ceil -- a part-used bag is still a bag you had to buy
    raise NotImplementedError


def rainfall_summary(readings: list[float]) -> dict[str, float]:
    """Return mean, median, mode and sample stdev of `readings`, each to 2 dp.

    Args:
        readings: Daily rainfall in millimetres. At least two values.

    Returns:
        A dict with keys "mean", "median", "mode", "stdev".
    """
    # TODO: statistics.mean, .median, .mode, .stdev -- one call each
    raise NotImplementedError


def pick_trial_plots(plots: list[str], k: int) -> list[str]:
    """Return `k` distinct plots chosen at random for this week's trial."""
    # TODO: random.sample -- not random.choice in a loop
    raise NotImplementedError


if __name__ == "__main__":
    assert isclose(circle_bed_area(3.0), 7.07), circle_bed_area(3.0)
    assert isclose(circle_bed_area(1.0), 0.79), circle_bed_area(1.0)
    assert isclose(circle_bed_area(0.0), 0.0), circle_bed_area(0.0)

    assert bags_of_compost(7.07) == 2, bags_of_compost(7.07)
    assert bags_of_compost(8.0) == 2, bags_of_compost(8.0)
    assert bags_of_compost(8.01) == 3, bags_of_compost(8.01)
    assert bags_of_compost(0.0) == 0, bags_of_compost(0.0)
    assert bags_of_compost(10.0, coverage_m2=5.0) == 2

    summary = rainfall_summary(RAINFALL_MM)
    assert isclose(summary["mean"], 12.1), summary
    assert isclose(summary["median"], 11.2), summary
    assert isclose(summary["mode"], 8.1), summary
    assert isclose(summary["stdev"], 4.37), summary

    trial = pick_trial_plots(PLOTS, 3)
    assert len(trial) == 3, trial
    assert len(set(trial)) == 3, "a plot cannot be in the trial twice"
    assert set(trial) <= set(PLOTS), trial

    bed = circle_bed_area(3.0)
    print(f"Round bed, 3.0 m across: {bed} m2")
    print(f"Compost bags needed: {bags_of_compost(bed)}")
    print(
        f"Rainfall: mean {summary['mean']} mm, median {summary['median']} mm, "
        f"mode {summary['mode']} mm, stdev {summary['stdev']} mm"
    )
    print(f"Trial plots this week: {trial}")
    print("All checks passed.")
```

Four words you need before you start.

**Mean, median, mode.** The mean is the total divided by how many there are.
The median is the middle value once you sort them. The mode is the value that
shows up most often.

**Standard deviation.** One number saying how spread out the readings are. A
small one means every day was about the same; a big one means some days were
soaking and some were dry.

**Sample versus population.** If your seven readings are *all the data there
will ever be*, they are a population. If they are seven days out of a year,
they are a **sample** of something larger. The two need different arithmetic,
and `statistics` has a separate function for each. Seven days of rain are a
sample, so you want `stdev`.

**`set`.** A collection with no duplicates and no order. `len(set(trial)) ==
3` is how the starter asks "were all three different", and `set(trial) <=
set(PLOTS)` is how it asks "is every one of these a real plot". You meet sets
properly in Week 5.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/exercises/exercise-05-import-and-use.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `circle_bed_area` uses `math.pi`. Do not type `3.14159` — you get a
   different answer than the checks expect, and a hand-typed constant is
   untraceable six months later, when nobody can tell whether it was a
   rounding choice or a typo.
2. `circle_bed_area` rounds to two decimals and returns `0.0` for a diameter
   of `0.0`.
3. `bags_of_compost` uses `math.ceil` and returns an `int`, not a float.
4. `rainfall_summary` returns a dict with exactly the keys `"mean"`,
   `"median"`, `"mode"`, `"stdev"`, each rounded to two decimals.
5. `pick_trial_plots` uses `random.sample`, returns exactly `k` items, and
   never repeats a plot.
6. The imports stay at the top of the file, one module per line, standard
   library only.

## Constraints

- **Import `math`, `random` and `statistics` with plain `import`, and add
  exactly one `from math import isclose`.** Both forms appear on purpose. The
  plain form keeps `math.pi` labelled with where it came from, which is what
  you want for a name used once or twice. The `from` form is worth it for a
  name called four times in one block, where `math.isclose` four times is
  just noise.
- **Do not alias any of the three.** `import numpy as np` is a convention
  with decades of shared use behind it, so every reader already knows it.
  `import statistics as st` is a private code you invented, and the next
  reader has to scroll up to decode it.
  [Lecture 4, section 2](../lecture-notes/04-modules-and-imports.md) makes
  this comparison in full.
- **Use `isclose` in the checks, not `==`.** You are comparing floats that
  arrived by different arithmetic paths, and `==` asks a stricter question
  than you mean. Do not mistake `isclose` for a wide net, though — it is
  about one part in a billion, and it will not paper over a missing `round`:

  ```text
  isclose(7.0685834705770345, 7.07) = False
  ```

- **Use `math.ceil`, not `round` or `int()`.** All three disagree on exactly
  the numbers this exercise checks:

  ```text
  7.07 / 4 = 1.7675   ceil -> 2   int -> 1   round -> 2
  8.01 / 4 = 2.0025   ceil -> 3   int -> 2   round -> 2
  ```

  The real-world rule is "a part-used bag is still a bag you had to buy", and
  `ceil` is the only one of the three that says that. Choose the function
  whose definition matches the rule, not the one whose output happens to
  match your first test case.
- **Use `stdev`, not `pstdev`.** The difference is the denominator, and it is
  a statement about your data rather than a formatting choice. `pstdev`
  divides by `n` and is right when your readings *are* the whole population.
  `stdev` divides by `n - 1` and is right when they are a sample of
  something larger:

  ```text
  stdev  = 4.37
  pstdev = 4.05
  ```

  Getting it wrong produces a plausible number, which is why it is in Common
  bugs and not in a traceback.
- **Assert on properties of the random result, never on its value.** A check
  expecting `["Plot A", "Plot D", "Plot F"]` passes once and fails forever
  after. The length, the distinctness and the membership hold every run.
- **Do not call `random.seed()` inside `pick_trial_plots`.** Seeding is a
  global operation on the module's generator. A function that seeds on every
  call does not just make itself predictable — it makes every later use of
  `random` anywhere in the program predictable, which is a far worse bug than
  the one it was trying to solve. Seed once in `__main__`, where a reader can
  see it.

## Expected output

The published file seeds the generator so the download prints the same thing
every time. Real stdout, captured on CPython 3.13.2:

```text
$ python exercise-05-import-and-use.py
Round bed, 3.0 m across: 7.07 m2
Compost bags needed: 2
Rainfall: mean 12.1 mm, median 11.2 mm, mode 8.1 mm, stdev 4.37 mm
Trial plots this week: ['Plot A', 'Plot C', 'Plot F']
All checks passed.
```

**Your file has no seed, so your fourth line will differ, and that is the
whole point of the exercise.** Five real runs of the unseeded version:

```text
Trial plots this week: ['Plot D', 'Plot B', 'Plot C']
Trial plots this week: ['Plot F', 'Plot E', 'Plot C']
Trial plots this week: ['Plot A', 'Plot B', 'Plot F']
Trial plots this week: ['Plot C', 'Plot B', 'Plot A']
Trial plots this week: ['Plot F', 'Plot E', 'Plot A']
```

Five different lines, five passes. Notice the plots do not come out in the
order they appear in `PLOTS` — `random.sample` shuffles as well as selects,
which is exactly why the check is `set(trial) <= set(PLOTS)` and not a list
comparison.

## Steps

1. Create the file, paste the starter, run it. `NotImplementedError`, as
   expected.
2. Fill in `circle_bed_area`. Check the arithmetic by hand once: a 3-metre
   bed has a 1.5-metre radius, so the area is `pi * 2.25`, a bit over 7. Give
   the radius its own name rather than writing `math.pi * (diameter_m / 2) **
   2` — one named intermediate removes the question of whether `**` or `/`
   happens first, and the single most common wrong answer here is using the
   diameter as the radius, which is off by exactly a factor of four.
3. Fill in `bags_of_compost`. The `8.0` and `8.01` checks sit next to each
   other deliberately: exactly two bags' worth needs two bags, one hundredth
   more needs three.
4. Fill in `rainfall_summary`. Four one-line calls. If yours runs longer than
   six lines, you are rebuilding something the module already does.
5. Fill in `pick_trial_plots` and run the file five times. The last printed
   line should change. `All checks passed.` should not.
6. In a REPL, run `help(statistics.stdev)` and read the first paragraph, then
   `help(statistics.pstdev)` immediately after. The difference between those
   two paragraphs is the difference between `4.37` and `4.05`.

## The Solution

```python
"""exercise-05-import-and-use-solution.py — one afternoon at the community garden.

Four functions, and the body of every one is a single call into a module that
already ships with Python. No pip install, no hand-rolled formulas.

One line differs from the starter: `random.seed(2026)` at the top of the
__main__ block, so this published file prints the same trial plots every
time. Your own file has no seed and prints a different line each run, which
is what `random.sample` is for. Seeding lives in __main__ and never inside a
function -- the page explains why.
"""

import math
import random
import statistics
from math import isclose

RAINFALL_MM = [12.4, 8.1, 15.0, 9.6, 11.2, 8.1, 20.3]
PLOTS = ["Plot A", "Plot B", "Plot C", "Plot D", "Plot E", "Plot F"]


def circle_bed_area(diameter_m: float) -> float:
    """Return the area of a round planting bed, in square meters.

    Args:
        diameter_m: The bed's diameter in meters.

    Returns:
        The area, rounded to two decimals.
    """
    radius_m = diameter_m / 2
    return round(math.pi * radius_m**2, 2)


def bags_of_compost(area_m2: float, coverage_m2: float = 4.0) -> int:
    """Return how many whole bags of compost it takes to cover `area_m2`."""
    return math.ceil(area_m2 / coverage_m2)


def rainfall_summary(readings: list[float]) -> dict[str, float]:
    """Return mean, median, mode and sample stdev of `readings`, each to 2 dp.

    Args:
        readings: Daily rainfall in millimetres. At least two values.

    Returns:
        A dict with keys "mean", "median", "mode", "stdev".
    """
    return {
        "mean": round(statistics.mean(readings), 2),
        "median": round(statistics.median(readings), 2),
        "mode": round(statistics.mode(readings), 2),
        "stdev": round(statistics.stdev(readings), 2),
    }


def pick_trial_plots(plots: list[str], k: int) -> list[str]:
    """Return `k` distinct plots chosen at random for this week's trial."""
    return random.sample(plots, k)


if __name__ == "__main__":
    random.seed(2026)

    assert isclose(circle_bed_area(3.0), 7.07), circle_bed_area(3.0)
    assert isclose(circle_bed_area(1.0), 0.79), circle_bed_area(1.0)
    assert isclose(circle_bed_area(0.0), 0.0), circle_bed_area(0.0)

    assert bags_of_compost(7.07) == 2, bags_of_compost(7.07)
    assert bags_of_compost(8.0) == 2, bags_of_compost(8.0)
    assert bags_of_compost(8.01) == 3, bags_of_compost(8.01)
    assert bags_of_compost(0.0) == 0, bags_of_compost(0.0)
    assert bags_of_compost(10.0, coverage_m2=5.0) == 2

    summary = rainfall_summary(RAINFALL_MM)
    assert isclose(summary["mean"], 12.1), summary
    assert isclose(summary["median"], 11.2), summary
    assert isclose(summary["mode"], 8.1), summary
    assert isclose(summary["stdev"], 4.37), summary

    trial = pick_trial_plots(PLOTS, 3)
    assert len(trial) == 3, trial
    assert len(set(trial)) == 3, "a plot cannot be in the trial twice"
    assert set(trial) <= set(PLOTS), trial

    bed = circle_bed_area(3.0)
    print(f"Round bed, 3.0 m across: {bed} m2")
    print(f"Compost bags needed: {bags_of_compost(bed)}")
    print(
        f"Rainfall: mean {summary['mean']} mm, median {summary['median']} mm, "
        f"mode {summary['mode']} mm, stdev {summary['stdev']} mm"
    )
    print(f"Trial plots this week: {trial}")
    print("All checks passed.")
```

**The one line that is not in your version is `random.seed(2026)`.** Seeding
fixes the generator's starting point, so the same sequence of "random" numbers
comes out every time. That is not less random in any statistical sense — the
numbers are just as evenly spread — it only means the sequence is reproducible.
This published file needs that so its printed output can be checked. Your
file should not have it, because the exercise is about handling a result you
cannot predict. Where a seed belongs, when you want one, is right here in
`__main__`, visible, and never inside a library function.

**`math.pi`, never a typed-out `3.14159`.** `math.pi` carries the full
precision the machine can hold, and the `.pi` spelling is documentation: a
reader sees where the constant came from without leaving the line.

**`radius_m` gets its own name.** It removes a precedence question from the
line and it makes the halving mistake hard to commit by accident.

**`ceil` returns an `int`, so the annotation is honest without a cast.** In
Python 3, `math.ceil` hands back a whole number — `2`, not `2.0`.

**Four calls into `statistics`, and no hand-rolled formulas.** All four are
already written, tested and documented by people who care a great deal about
floating-point error. This is what the standard library is for.

**`random.sample`, not `random.choice` in a loop.** `sample` draws **without
replacement** — once a plot is picked it is out of the hat, so it cannot come
back twice by construction rather than by luck. `choice` draws **with
replacement**, so three `choice` calls will eventually hand you a duplicate.
With a seed of `7` it took two attempts:

```text
duplicate on draw 2: ['Plot F', 'Plot A', 'Plot A']
```

That is the shape of the worst kind of bug: correct on your machine, on the
day you wrote it, and wrong in the garden next Tuesday.

**Both import forms, on purpose.** `import math` for names used once or
twice, `from math import isclose` for the one name called four times in a
row. And no aliases, for the reason in the constraints.

## Run it

Copy the worked answer on this page into `exercise-05-import-and-use.py` and run it:

```bash
python exercise-05-import-and-use.py
```

It is the same program you are writing, plus the one seed line, under a name
that will not collide with your own `exercise-05-import-and-use.py`. Delete
the `random.seed(2026)` line and run it five times to watch the last line
start moving again.

## Common bugs to catch

- **`AssertionError: 7.0685834705770345` on the first check.** You skipped
  the rounding:

  ```text
  Traceback (most recent call last):
      assert isclose(circle_bed_area(3.0), 7.07), circle_bed_area(3.0)
             ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: 7.0685834705770345
  ```

  The number is right and the contract is not — the docstring promises two
  decimals. When a docstring and the code disagree, one of them is a bug, and
  it is usually not the docstring.

- **`AssertionError: 1` on the `bags_of_compost(7.07)` check.** You used
  `int()`, which truncates towards zero: `int(1.7675)` is `1`. Note the
  wording — "towards zero", not "down". `int(-1.5)` is `-1` while
  `math.floor(-1.5)` is `-2`, and that distinction will matter the first time
  you handle a negative number.

- **`AssertionError: 2` on the `bags_of_compost(8.01)` check.** You used
  `round()`. `bags_of_compost(8.01)` needs three bags, because two bags cover
  8.0 square metres and there is a hundredth left over. `round(2.0025)` is
  `2`.

- **`NameError: name 'pi' is not defined`.** You wrote `pi` after `import
  math`. The plain import binds one name, `math`, and nothing else. Either
  write `math.pi` or add `from math import pi`.

- **`TypeError: 'module' object is not callable`.** You wrote `math(...)`. A
  module is a box of names, not a function. Reach through it with a dot.

- **A bare `AssertionError` while the summary quietly reads `4.05`.** You used
  `statistics.pstdev`. The check that catches it carries no message, so there
  is nothing for Python to print. Print the summary dict and compare it
  against the expected line, key by key.

- **`AssertionError: a plot cannot be in the trial twice`.** You called
  `random.choice` three times in a loop instead of `random.sample` once. Run
  it again and it may well pass. That is the whole lesson: a test over a
  random function has to assert on properties that hold *every* time, because
  a test that asserts on values passes once and fails forever after.

- **`ValueError: Sample larger than population or is negative`.** You asked
  for more plots than exist:

  ```text
  Traceback (most recent call last):
      return random.sample(plots, 8)
             ~~~~~~~~~~~~~^^^^^^^^^^
    File "...\Lib\random.py", line 434, in sample
      raise ValueError("Sample larger than population or is negative")
  ValueError: Sample larger than population or is negative
  ```

  Should your function clamp `k` down to `len(plots)` instead? We say no. A
  caller who asks for eight plots out of six has a mistake in their
  reasoning, and quietly handing them six is how that mistake reaches the
  garden. Raising says so immediately. Whichever you choose, write the
  decision in the docstring — that is the actual deliverable.

- **Two errors that older tutorials predict and Python 3.13 does not
  produce.** Both are worth knowing, because both are cases where advice went
  stale and stayed in circulation.

  You may read that changing the rainfall data produces `StatisticsError: no
  unique mode; found 2 equally common values`. **Since Python 3.8 that is no
  longer true.** `statistics.mode` does not raise on a tie any more. It
  returns the first mode it came across, silently:

  ```text
  mode([8.1, 8.1, 20.3, 20.3]) = 8.1
  multimode([8.1, 8.1, 20.3, 20.3]) -> [8.1, 20.3]
  ```

  For your purposes that is *worse* than an exception, because a silent
  arbitrary choice is exactly the kind of thing you stop questioning. If ties
  are possible in your data, use `multimode` and decide explicitly what a tie
  means.

  You may also read `StatisticsError: variance requires at least two data
  points` for a one-element list. The real message names the function you
  actually called:

  ```text
    File "...\Lib\statistics.py", line 1207, in stdev
      raise StatisticsError('stdev requires at least two data points')
  statistics.StatisticsError: stdev requires at least two data points
  ```

  Same cause — sample standard deviation divides by `n - 1`, and `n = 1`
  makes that zero — different wording. Search for the string you actually
  saw, not the one somebody remembered.

## Under the hood

<details>
<summary>Under the hood — what import really does the first time, and what it skips the second</summary>

`import greeting` is not a copy-paste. It is four steps, and only the first
three ever happen twice.

**1. Check the cache.** Python keeps a dictionary of every module already
imported in this process, at `sys.modules`. If the name is in there, the
import is over — you get the existing module object and nothing else runs.
This is why the second import of anything is nearly free.

**2. Find the file.** If it is not cached, Python walks `sys.path`, a list of
directories, in order, and takes the first match. `sys.path[0]` is the folder
of the script you ran, which is why your own file can shadow a standard
library module — name a file `random.py` and `import random` finds yours.

**3. Run the file, top to bottom, once.** Every line at the top level
executes: every `def`, every constant, every stray `print`. The names that
result become the module's contents.

**4. Bind one name in your file.** `import math` binds `math`. That is all it
binds — which is why `pi` on its own is a `NameError`.

You can watch step 3 happen exactly once. Given a file `greeting.py`:

```python
"""greeting.py — a tiny module that announces when it is executed."""

print("greeting.py is running its top level")

MESSAGE = "hello from greeting"
```

```text
>>> import greeting
greeting.py is running its top level
>>> import greeting
>>> import sys
>>> sys.modules["greeting"]
<module 'greeting' from '...\greeting.py'>
>>> greeting.MESSAGE
'hello from greeting'
```

The second `import` printed nothing. The module was in `sys.modules`, so
Python handed back the object it already had. **Importing something twenty
times does not run it twenty times**, which is what makes it safe for ten
files in a project to all import the same helper.

A module is an ordinary object, by the way, with an ordinary type:

```text
>>> import math
>>> type(math)
<class 'module'>
>>> math.__name__
'math'
```

`math.pi` is just attribute access on an object, exactly like any other dot.

**Two things that follow directly.**

**Anything at a module's top level runs on import.** If your file prints a
report at the top level, importing it prints the report — probably in the
middle of somebody else's program. That is the entire reason for the
`if __name__ == "__main__":` guard. When you run a file directly, Python sets
its `__name__` to the string `"__main__"`; when it is imported, `__name__` is
the module's own name. One `if` tells the two apart.
[Lecture 4, section 6](../lecture-notes/04-modules-and-imports.md) has the
mechanism.

**The `__pycache__` folder is step 3 being skipped across runs.** The first
import compiles the source to bytecode and saves it as
`__pycache__/greeting.cpython-313.pyc`. Later runs reuse that file when the
source has not changed, which saves the parsing, not the executing — the top
level still runs once per process. It is a cache, it is safe to delete, and
it belongs in `.gitignore`.

</details>

<details>
<summary>Under the hood — what "random" means here, and why a seed is not cheating</summary>

`random` does not produce random numbers. It produces a fixed, extremely long
sequence of numbers that has no pattern anyone can detect, and it starts you
at an arbitrary point in that sequence. That is called a **pseudo-random
number generator**, and the algorithm underneath Python's is the Mersenne
Twister, whose sequence repeats after about 2 to the power of 19937 numbers —
a number with about 6,000 digits.

`random.seed(2026)` says "start at the point in that sequence identified by
2026". Same seed, same starting point, same numbers, forever:

```text
['Plot A', 'Plot C', 'Plot F']
['Plot A', 'Plot C', 'Plot F']
```

Two separate runs of the whole program, one answer. With no seed at all,
Python picks a starting point from the operating system's entropy source when
the module first loads, which is why your unseeded runs all differ.

Seeding is therefore not a way of faking randomness. It is how you make a
demo reproduce, and how you write a regression test over code that uses
random numbers. It is also exactly why `random.seed()` must never appear
inside a library function: seeding is a global reset of one shared generator,
so a function that seeds on each call silently makes every later `random`
call in the entire program predictable.

If you want randomness that does not touch the shared generator, make your
own:

```python
rng = random.Random(2026)
rng.sample(PLOTS, 3)
```

`random.Random` is an independent generator with its own state. Seed it as
much as you like and nothing else in the program notices. That is the shape
to reach for the moment two parts of a program both want reproducible
randomness.

**One warning that matters outside this garden.** The Mersenne Twister is
fast and statistically excellent and **completely unsuitable for anything
security-related**. Observe a few hundred of its outputs and you can
reconstruct its internal state and predict every number it will ever produce
again. For passwords, tokens, session keys or anything an attacker would like
to guess, use the `secrets` module, which draws from the operating system's
cryptographic source. `random` for simulations and shuffles and picking
plots; `secrets` for anything that guards something.

</details>

## Acceptance checklist

- [ ] `python exercise-05-import-and-use.py` prints four lines and `All checks passed.`
- [ ] All three modules are imported at the top, one per line, no aliases.
- [ ] `circle_bed_area` uses `math.pi`, not a typed-out constant.
- [ ] `bags_of_compost` returns an `int` and uses `math.ceil`.
- [ ] `rainfall_summary` is four calls into `statistics`, not four hand-rolled
      formulas.
- [ ] Running the file five times gives five different trial-plot lines and
      five passes.
- [ ] No `random.seed()` call inside any function.
- [ ] Committed to Git with a message like `Add Week 4 exercise 5: standard library imports`.

## Stretch

- Split the file in two. Move the four functions and the two constants into
  `garden.py`, give it a `_self_test` behind the `__main__` guard, and leave
  `main.py` holding nothing but the report:

  ```python
  """main.py — print the garden report. All the arithmetic lives in garden.py."""

  from garden import (
      PLOTS,
      RAINFALL_MM,
      bags_of_compost,
      circle_bed_area,
      pick_trial_plots,
      rainfall_summary,
  )


  def main() -> None:
      """Print one afternoon's garden report."""
      bed = circle_bed_area(3.0)
      summary = rainfall_summary(RAINFALL_MM)
      print(f"Round bed, 3.0 m across: {bed} m2")
      print(f"Compost bags needed: {bags_of_compost(bed)}")
      print(
          f"Rainfall: mean {summary['mean']} mm, median {summary['median']} mm, "
          f"mode {summary['mode']} mm, stdev {summary['stdev']} mm"
      )
      print(f"Trial plots this week: {pick_trial_plots(PLOTS, 3)}")


  if __name__ == "__main__":
      main()
  ```

  ```bash
  python garden.py
  ```

  ```text
  OK
  ```

  ```bash
  python main.py
  ```

  ```text
  Round bed, 3.0 m across: 7.07 m2
  Compost bags needed: 2
  Rainfall: mean 12.1 mm, median 11.2 mm, mode 8.1 mm, stdev 4.37 mm
  Trial plots this week: ['Plot B', 'Plot D', 'Plot F']
  ```

  The self-test fired when you ran `garden.py` directly and stayed silent
  when `main.py` imported it. That is the `__main__` guard earning its keep,
  and this two-file shape is exactly what Challenge 01 asks for.

- Put `random.seed(2026)` as the first line of your own `__main__` block and
  run the file three times. The trial plots stop moving. Then delete it and
  run three more times. Being able to switch reproducibility on and off at
  one line, in one visible place, is the point.

- Replace `statistics.mode` with `statistics.multimode` and decide what your
  function reports when two rainfall totals tie:

  ```text
  multimode, no tie : [8.1]
  multimode, tie    : [8.1, 20.3]
  mode, tie         : 8.1
  ```

  `multimode` always returns a list, even when there is a single winner,
  which changes that key's type from `float` to `list[float]`. There is no
  single right answer to what `rainfall_summary` should then report — the
  first mode, all of them, or `None` on a tie are all defensible. There is
  only the answer you wrote in the docstring, and the one you did not.

That is all five. Move on to the
[Week 4 challenges](../challenges/README.md), where you will split your first
program across two files.
