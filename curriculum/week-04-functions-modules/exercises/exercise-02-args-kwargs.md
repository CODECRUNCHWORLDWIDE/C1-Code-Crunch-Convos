# Exercise 2 — `*args` and `**kwargs`

> **Topic:** Variable-length argument lists and unpacking at the call site
> **Lecture:** [02 — `*args`, `**kwargs`, and Scope](../lecture-notes/02-args-kwargs-and-scope.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** `*` and `**` turn up in every Python library you will ever read, and they mean two opposite things depending on which side of the call they sit on. Get that mirror straight now and decorators, dict merging and `functools.partial` all feel obvious later. Get it wrong and you will spend an hour wondering why your list of three numbers arrived as one thing.

## The Brief

The Saturday farmers market runs on paper. Stalls weigh what a customer
picked, scribble a total, and hand over a receipt. You are writing the three
functions that would replace the scribbling.

Here is the idea the whole page turns on, in one sentence: **a star in a
`def` line collects loose values into one container, and a star at a call
site does the opposite — it takes one container and spreads it back into
loose values.** Same symbol, opposite directions, and which one you get
depends entirely on where you wrote it.

A picture for the collecting half. Imagine a function that says "hand me as
many weights as you like". Python sweeps whatever arrives into a bag and
gives you the bag under one name. One star means a bag of loose values in
order, called a **tuple**. Two stars means a bag of labelled values, called a
**dict**.

Each function hits one part of the story.

**`total_pounds` collects loose numbers.** A basket has however many items it
has, so the signature says "however many".

**`build_stall` collects labelled details.** A greens stall and an orchard
stall do not describe themselves with the same fields, so the signature
refuses to guess which fields exist.

**`receipt_line` puts a parameter *behind* the star.** Anything after a
`*items` can only ever be passed by name. That is what stops `"CAD"` from
being sold as a vegetable.

The spreading half matters just as much, because the market keeps baskets as
lists and stall configs as dicts, and both have to reach these functions. A
list handed straight to `total_pounds` does not become three arguments. It
becomes one argument that happens to be a list. The self-checks cover that
on purpose.

## Starter

Create `exercise-02-args-kwargs.py` in your practice repo.

```python
"""exercise-02-args-kwargs.py — receipts for the Saturday farmers market.

Fill in every TODO, then run the file.
"""


def total_pounds(*weights: float) -> float:
    """Return the combined weight of everything in one basket, in pounds.

    Args:
        *weights: Zero or more individual item weights.

    Returns:
        The total, rounded to two decimals. 0.0 when nothing was passed.
    """
    # TODO
    raise NotImplementedError


def build_stall(name: str, **details: object) -> dict[str, object]:
    """Return a stall record with "name" first, then every keyword detail."""
    # TODO: build a NEW dict. Do not mutate `details`.
    raise NotImplementedError


def receipt_line(stall_name: str, *items: str, currency: str = "USD") -> str:
    """Return one receipt line for a stall.

    Args:
        stall_name: The stall's display name.
        *items: Zero or more item names, in the order they were weighed.
        currency: Three-letter currency code. Keyword-only.

    Returns:
        A line like `Sunrise Greens: kale, chard [USD]`.
    """
    # TODO: join the items with ", "
    # TODO: with no items at all, the item list reads "(nothing)"
    raise NotImplementedError


if __name__ == "__main__":
    assert total_pounds() == 0.0, total_pounds()
    assert total_pounds(1.5) == 1.5, total_pounds(1.5)
    assert total_pounds(1.5, 2.25, 0.75) == 4.5, total_pounds(1.5, 2.25, 0.75)

    basket = [1.5, 2.25, 0.75]
    assert total_pounds(*basket) == 4.5, "did you unpack the list with *?"

    sunrise = build_stall("Sunrise Greens", produce="kale", price_per_pound=3.5)
    assert sunrise == {
        "name": "Sunrise Greens",
        "produce": "kale",
        "price_per_pound": 3.5,
    }, sunrise
    assert list(sunrise)[0] == "name", "name must be the first key"

    config = {"produce": "figs", "price_per_pound": 6.0}
    orchard = build_stall("Hilltop Orchard", **config)
    assert orchard["name"] == "Hilltop Orchard", orchard
    assert orchard["produce"] == "figs", orchard
    assert config == {"produce": "figs", "price_per_pound": 6.0}, "config was mutated"

    line = receipt_line("Sunrise Greens", "kale", "chard", "spinach")
    assert line == "Sunrise Greens: kale, chard, spinach [USD]", line
    assert receipt_line("Hilltop Orchard", "figs", currency="CAD") == (
        "Hilltop Orchard: figs [CAD]"
    )
    assert receipt_line("Empty Stall") == "Empty Stall: (nothing) [USD]"

    print(line)
    print(receipt_line("Hilltop Orchard", "figs", currency="CAD"))
    print(f"Basket weight: {total_pounds(*basket)} lb")
    print("All checks passed.")
```

Before you fill anything in, spend two minutes watching the collecting half
work. Paste this into a REPL:

```python
def probe(*args, **kwargs):
    print("args =", args, " kwargs =", kwargs)
```

```text
>>> probe(1.5, 2.25, 0.75)
args = (1.5, 2.25, 0.75)  kwargs = {}
>>> probe([1.5, 2.25, 0.75])
args = ([1.5, 2.25, 0.75],)  kwargs = {}
>>> probe(*[1.5, 2.25, 0.75])
args = (1.5, 2.25, 0.75)  kwargs = {}
>>> probe(produce="kale", price_per_pound=3.5)
args = ()  kwargs = {'produce': 'kale', 'price_per_pound': 3.5}
```

Compare the second line to the third. Without the star, the list went in
whole and `args` is a one-item tuple whose single item is a list — look for
the comma before the closing bracket. With the star, the list was spread out
first and `args` holds three numbers. That one comma is the entire bug in the
first entry of Common bugs, and now you have seen it before it bites you.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/exercises/exercise-02-args-kwargs.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `total_pounds` accepts any number of positional floats, including none,
   and returns `0.0` when called with no arguments.
2. `total_pounds` rounds its result to two decimals.
3. `build_stall` returns a dict whose **first** key is `"name"`, followed by
   the keyword details in the order they were passed. Dicts remember the
   order things were put in, and the self-check relies on it.
4. `build_stall` must not modify the dict Python handed it as `details`, and
   must not modify a caller's dict that was spread in with `**`.
5. `receipt_line` returns exactly `"{stall_name}: {items} [{currency}]"`,
   where `{items}` is the item names joined by `", "`, or the literal
   `(nothing)` when no items were passed.
6. `currency` stays keyword-only. Because it sits after `*items`, Python
   already enforces this — do not move it in front.

## Constraints

- **Use the built-in `sum(weights, 0.0)` inside `total_pounds`, not a hand-
  written loop.** `weights` is an ordinary tuple, and the point of this
  exercise is that a star in the `def` line hands you an ordinary sequence
  you can give to ordinary tools. A hand-rolled accumulator hides that. The
  second argument to `sum` is the starting value, and starting at `0.0`
  rather than `0` is what makes an empty basket return `0.0` instead of the
  integer `0`.
- **Build a new dict with `{"name": name, **details}`.** Do not write
  `details["name"] = name`. Assignment puts `name` *last*, which fails the
  ordering check, and it changes a dict instead of making one. The `**`
  inside a dict literal is the same operator you already use at a call site,
  and seeing it in both places is the point.
- **Do not add `**kwargs` to `receipt_line`.** A narrow signature is a
  spell-checker. `receipt_line("A", "b", currancy="CAD")` raises a `TypeError`
  straight away and shows you the typo. A function that accepts any keyword
  would swallow it and quietly print `[USD]`. Accept arbitrary keywords only
  when you genuinely intend to pass them on somewhere.
- **Leave `currency` after `*items`.** Moving it in front does not raise. It
  silently succeeds and is wrong in two places at once — see Common bugs. The
  star is what makes the language enforce your intent instead of you hoping.
- **Never name a parameter `args` or `kwargs` when a real name exists.** The
  asterisks do the work, not the names. `*weights` and `*items` tell a reader
  what is in the bag. `*args` tells them nothing.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-args-kwargs.py
Sunrise Greens: kale, chard, spinach [USD]
Hilltop Orchard: figs [CAD]
Basket weight: 4.5 lb
All checks passed.
```

The third line is `total_pounds(*basket)` — a list spread back into three
separate arguments — which is the only reason it says `4.5` and not
something worse.

## Steps

1. Create the file, paste the starter, run it. First failure is
   `NotImplementedError` from `total_pounds`.
2. Implement `total_pounds`. Before you move on, open a REPL and run both
   `total_pounds(basket)` and `total_pounds(*basket)` with
   `basket = [1.5, 2.25, 0.75]`. Read the exception the first one raises
   carefully — it tells you exactly what shape `weights` ended up as.
3. Implement `build_stall`. Check the key order with `list(sunrise)`, which
   gives you the keys in order and nothing else.
4. Implement `receipt_line`. Do the no-items case last; it is the one people
   forget. Run until `All checks passed.` appears.
5. Add one experiment at the bottom, run it, then delete it:

   ```text
   >>> receipt_line("Test", "kale", "CAD")
   'Test: kale, CAD [USD]'
   ```

   `CAD` was sold as a vegetable. Your signature is correct — `currency` is
   keyword-only and therefore *could not* absorb that third loose argument —
   so `"CAD"` went where every extra loose argument goes, into `items`.
   Keyword-only parameters do not stop you passing rubbish. They stop rubbish
   from silently landing in the wrong parameter.

## The Solution

```python
"""exercise-02-args-kwargs-solution.py — receipts for the Saturday farmers market.

Three functions, one for each side of the star story. `total_pounds` packs
however many weights arrive. `build_stall` packs however many details arrive.
`receipt_line` puts a keyword-only parameter behind a `*` so a currency code
can never be sold as a vegetable.

The self-checks at the bottom are the starter's, unchanged.
"""


def total_pounds(*weights: float) -> float:
    """Return the combined weight of everything in one basket, in pounds.

    Args:
        *weights: Zero or more individual item weights.

    Returns:
        The total, rounded to two decimals. 0.0 when nothing was passed.
    """
    return round(sum(weights, 0.0), 2)


def build_stall(name: str, **details: object) -> dict[str, object]:
    """Return a stall record with "name" first, then every keyword detail."""
    return {"name": name, **details}


def receipt_line(stall_name: str, *items: str, currency: str = "USD") -> str:
    """Return one receipt line for a stall.

    Args:
        stall_name: The stall's display name.
        *items: Zero or more item names, in the order they were weighed.
        currency: Three-letter currency code. Keyword-only.

    Returns:
        A line like `Sunrise Greens: kale, chard [USD]`.
    """
    listed = ", ".join(items) if items else "(nothing)"
    return f"{stall_name}: {listed} [{currency}]"


if __name__ == "__main__":
    assert total_pounds() == 0.0, total_pounds()
    assert total_pounds(1.5) == 1.5, total_pounds(1.5)
    assert total_pounds(1.5, 2.25, 0.75) == 4.5, total_pounds(1.5, 2.25, 0.75)

    basket = [1.5, 2.25, 0.75]
    assert total_pounds(*basket) == 4.5, "did you unpack the list with *?"

    sunrise = build_stall("Sunrise Greens", produce="kale", price_per_pound=3.5)
    assert sunrise == {
        "name": "Sunrise Greens",
        "produce": "kale",
        "price_per_pound": 3.5,
    }, sunrise
    assert list(sunrise)[0] == "name", "name must be the first key"

    config = {"produce": "figs", "price_per_pound": 6.0}
    orchard = build_stall("Hilltop Orchard", **config)
    assert orchard["name"] == "Hilltop Orchard", orchard
    assert orchard["produce"] == "figs", orchard
    assert config == {"produce": "figs", "price_per_pound": 6.0}, "config was mutated"

    line = receipt_line("Sunrise Greens", "kale", "chard", "spinach")
    assert line == "Sunrise Greens: kale, chard, spinach [USD]", line
    assert receipt_line("Hilltop Orchard", "figs", currency="CAD") == (
        "Hilltop Orchard: figs [CAD]"
    )
    assert receipt_line("Empty Stall") == "Empty Stall: (nothing) [USD]"

    print(line)
    print(receipt_line("Hilltop Orchard", "figs", currency="CAD"))
    print(f"Basket weight: {total_pounds(*basket)} lb")
    print("All checks passed.")
```

**Inside the function, `weights` is an ordinary tuple, and that is the entire
point.** There is nothing star-shaped left in the body. The `*` in the
signature was an instruction about how arguments get collected on the way in;
what lands in the body is a plain sequence you can hand to `sum`, `len`,
`max` or a `for` loop. Once you believe that, `*args` stops being a special
feature and becomes a way of writing "however many".

**`sum(weights, 0.0)` rather than `sum(weights)`.** With no weights at all,
`sum(())` returns the integer `0`, and this function promises a float — the
docstring says so and so does the `-> float`. The assert passes either way,
because `0 == 0.0` is true. The *type* does not, and a caller who formats the
result with `:.1f` would see the difference. Starting at `0.0` makes the
return type honest for free.

**The rounding is on the total, not on each weight.** Round early and you
collect seven small errors instead of one. Do the arithmetic at full
precision, round once, at the point where the number becomes an answer.

**`{"name": name, **details}` gets the contents and the order right in one
expression.** A dict literal is built left to right, and dicts remember the
order things were put in, so `"name"` goes in first and every detail follows
in the order it was passed. The `**details` inside the literal is a
**spread**: it copies the pairs out of `details` into the new dict. Nothing
is modified, so a caller's config survives the call intact — which is
requirement 4, and it comes free from choosing an expression over a
statement.

**`details` is already a fresh dict, and it still is not yours to keep.**
Python builds a brand new dict for `**details` on every call, so changing it
would not corrupt the caller's data today. The habit is what matters. The
moment someone rewrites `build_stall` to take a plain `dict` parameter
instead, a body that modifies its argument starts writing to the caller's
object, and nothing in the signature warns them. Build new things and return
them.

**`currency` sits after `*items`, so Python enforces keyword-only for you.**
There is no way to sneak a loose argument past a `*args` — every extra loose
argument lands in `items`. That is not a convention you are politely
following. It is a rule the language applies.
[Lecture 1, section 9](../lecture-notes/01-defining-functions.md) has the
full ordering rule.

**The empty case is a conditional expression, not a separate branch.**
`", ".join(())` is the empty string, so without the guard you get
`Empty Stall:  [USD]` with two spaces where the items should be. That is the
classic "empty container formats to nothing" bug, and it shows up anywhere
you join a collection you did not check first.

## Download and run

Download
[exercise-02-args-kwargs-solution.py](./exercise-02-args-kwargs-solution.py)
and run it:

```bash
python exercise-02-args-kwargs-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-02-args-kwargs.py`.

## Common bugs to catch

- **`TypeError: unsupported operand type(s) for +: 'float' and 'list'`.** You
  forgot the star at the call site:

  ```text
  Traceback (most recent call last):
      assert total_pounds(basket) == 4.5
      return round(sum(weights, 0.0), 2)
                   ~~~^^^^^^^^^^^^^^
  TypeError: unsupported operand type(s) for +: 'float' and 'list'
  ```

  Read the two type names in that message and you can rebuild exactly what
  happened. `weights` is `([1.5, 2.25, 0.75],)` — a one-item tuple whose one
  item is a list — and `sum` tried to compute `0.0 + [1.5, 2.25, 0.75]`. Add
  the star. If you wrote plain `sum(weights)`, the same bug reports `'int'
  and 'list'` instead, because the default starting value is the integer `0`.
  Same bug, different first operand.

- **`AssertionError: name must be the first key`.** You wrote
  `details["name"] = name` and returned `details`:

  ```text
  Traceback (most recent call last):
      assert list(sunrise)[0] == "name", "name must be the first key"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError: name must be the first key
  ```

  The record comes out as
  `{'produce': 'kale', 'price_per_pound': 3.5, 'name': 'Sunrise Greens'}` —
  right contents, wrong order, because assignment adds a new key at the end.
  Order is not cosmetic here: this dict becomes a receipt, and a receipt names
  the stall first.

- **Everything passes and the order is still wrong.** You wrote
  `{**details, "name": name}` — the spread before the fixed key. This is the
  near-miss version of the bug above and it deserves its own entry, because
  the equality check is perfectly happy:

  ```text
  stall: {'produce': 'kale', 'price_per_pound': 3.5, 'name': 'Sunrise Greens'}
  equal to expected dict? True
  ```

  Dict equality ignores order, so `assert sunrise == {...}` passes. Only
  `list(sunrise)[0] == "name"` catches it. Fixed key first, spread after.

- **`TypeError: build_stall() got multiple values for argument 'name'`.** Your
  config dict has a `name` key and you spread it with `**` while also passing
  `name` separately:

  ```python
  config = {"name": "Hilltop Orchard", "produce": "figs"}
  build_stall("Hilltop Orchard", **config)   # WRONG
  ```

  The spread turned into `name="Hilltop Orchard"`, and you had already filled
  `name` positionally. Python will not fill one parameter twice. Either drop
  `name` from the dict or stop passing it separately. Notice this is the same
  error you would get from typing `build_stall("A", name="B")` by hand.

- **A bare `AssertionError` on the Empty Stall check.** You joined without
  checking for empty, so the function returned `'Empty Stall:  [USD]'` with a
  doubled space. That assert carries no message, so all Python prints is:

  ```text
  AssertionError
  ```

  Call the function yourself and look at the `repr` — the extra space is
  invisible until you do:

  ```text
  >>> receipt_line("Empty Stall")
  'Empty Stall:  [USD]'
  ```

- **You moved `currency` in front of `*items` and nothing raised.** This is
  the worst outcome on the page, because it succeeds:

  ```python
  def receipt_line(stall_name: str, currency: str = "USD", *items: str) -> str:   # WRONG
      ...
  ```

  ```text
  >>> receipt_line("Sunrise Greens", "kale", "chard")
  'Sunrise Greens: chard [kale]'
  ```

  `"kale"` was sold as the currency and vanished from the item list. No
  exception, a receipt that is wrong in two places, and a customer who finds
  out before you do. You only get a `TypeError` here if you drop `*items`
  altogether, and its real text names the range of arguments the function will
  take:

  ```text
  TypeError: receipt_line() takes from 1 to 2 positional arguments but 3 were given
  ```

  Both have the same fix — put `currency` after the star — but a silent wrong
  answer is the one that reaches a customer.

- **`SyntaxError: positional argument follows keyword argument`.** You named
  an argument and then went back to unnamed ones:

  ```text
    File "<stdin>", line 1
      receipt_line(stall_name="Sunrise Greens", "kale")
                                                      ^
  SyntaxError: positional argument follows keyword argument
  ```

  This one is caught before your program runs at all — it is a parse error,
  not a call error. Once you start naming arguments at a call site,
  everything after must be named.

## Under the hood

<details>
<summary>Under the hood — how packing and unpacking actually work, and what keyword-only really means</summary>

**Packing, on the `def` side.** When Python calls a function it walks the
arguments in order and fills the named parameters first. Whatever loose
arguments are left over go into the `*name` parameter as a **tuple**, and
whatever named arguments have no matching parameter go into the `**name`
parameter as a **dict**. Both containers are built fresh for that one call.
If nothing is left over you get an empty tuple and an empty dict, never
`None`:

```text
>>> probe()
args = ()  kwargs = {}
```

That is why `total_pounds()` can return `0.0` without a special case:
`sum((), 0.0)` is `0.0`.

The tuple is a *copy* of the loose arguments, so rebinding `weights` inside
the function cannot affect the caller. The dict is a fresh dict too, which is
why `build_stall` cannot damage the caller's `config` even by accident. What
those containers *hold* is not copied — the objects inside are the caller's
objects — which is the same rule as everywhere else in Python.

**Unpacking, on the call side.** `f(*seq)` says "take every item of `seq` and
pass them as separate loose arguments". `f(**mapping)` says "take every
key/value pair and pass them as separate named arguments". The keys must be
strings, or you get `TypeError: keywords must be strings`.

Both work with any sequence and any mapping, not just lists and dicts, and
you can use several at once — `f(*a, *b, **c, **d)` is legal, and duplicate
keys across `**c` and `**d` are an error rather than a silent overwrite.

**The full parameter order.** Every Python signature is some subset of this,
always in this order:

```text
def f(a, b=2, *rest, c, d=4, **extra): ...
```

- `a` — required, can be given loose or by name
- `b=2` — optional, can be given loose or by name
- `*rest` — everything else loose
- `c` — **keyword-only and required**, because it is after the star
- `d=4` — keyword-only and optional
- `**extra` — everything else named

`inspect.signature` shows it back to you exactly as written:

```text
>>> import inspect
>>> inspect.signature(f)
<Signature (a, b=2, *rest, c, d=4, **extra)>
```

**Keyword-only is a position, not a keyword.** There is no `keyword_only=True`
flag anywhere. A parameter is keyword-only because it appears *after* a star,
and the reason is arithmetic rather than policy: `*rest` will absorb every
remaining loose argument, so no loose argument can ever get past it. Nothing
is checking your intent; there is simply no path for the value to arrive the
wrong way.

That is also why you can write a bare `*` with no name after it:

```python
def late_fee(days_late, daily_rate=0.25, *, waive=False): ...
```

The bare star collects nothing. It exists only to mark the boundary, so
`waive` must be named. You used this in Exercise 1's stretch.

**The mirror in one line.** `def f(*args)` collects; `f(*seq)` spreads. The
symbol is the same because the relationship is the same, read in opposite
directions — and this is exactly why every decorator you will ever read is
`def wrapper(*args, **kwargs)` on one line and `func(*args, **kwargs)` on the
next. Collect whatever arrives, spread it back out untouched.

</details>

<details>
<summary>Under the hood — why dicts remember their order, and when you are allowed to rely on it</summary>

Requirement 3 says `"name"` must come out first. That only means anything
because a Python dict gives its keys back in the order they were first
inserted.

This was not always true, and the way it became true is worth knowing.
Through Python 3.5, dict order was genuinely arbitrary — it fell out of where
each key landed in a hash table, so it could change between runs. In CPython
3.6 the dict was rebuilt to use a compact layout: a small array of indices
plus a dense array of entries stored in insertion order. Ordered iteration
came out of that redesign as a side effect, and it was documented as an
implementation detail nobody should depend on.

In **Python 3.7** the language specification adopted it. Insertion order is
now a guarantee every conforming Python must provide, which is what makes
`{"name": name, **details}` a correct way to control key order rather than a
trick that happens to work today.

Two things it does *not* mean.

**Equality still ignores order.** Two dicts with the same pairs in different
orders are equal, which is why the near-miss bug above passes the equality
check and only the explicit `list(sunrise)[0]` catches it.

**Sets are not ordered.** Sets got no such guarantee, and their iteration
order really can move between runs when strings are involved, because string
hashing is randomised per process for security reasons. If you need an
ordered collection of unique things, a dict with `None` values or
`dict.fromkeys(items)` is the standard move.

</details>

## Acceptance checklist

- [ ] `python exercise-02-args-kwargs.py` prints three lines and `All checks passed.`
- [ ] `total_pounds()` with no arguments returns `0.0`, not an error.
- [ ] `build_stall` returns a new dict and leaves the caller's config untouched.
- [ ] `"name"` is the first key of every stall record.
- [ ] `currency` cannot be passed without naming it.
- [ ] You have run `receipt_line("Test", "kale", "CAD")` and seen where `CAD` went.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 4 exercise 2: args and kwargs`.

## Stretch

- Write `merge_stalls(*stalls: dict[str, object]) -> dict[str, object]` that
  folds several stall records into one, with later records winning where two
  disagree.

  Try the obvious thing first, so you meet the wall on purpose:

  ```text
    File "<stdin>", line 1
      {**s for s in stalls}
       ^^
  SyntaxError: dict unpacking cannot be used in dict comprehension
  ```

  `{**a, **b}` works because the compiler can count the spreads while it is
  reading your source. `*stalls` holds an unknown number of dicts until the
  program actually runs, so there is nothing to count. Loop over the pairs
  instead:

  ```python
  def merge_stalls(*stalls: dict[str, object]) -> dict[str, object]:
      """Fold several stall records into one; later records win on conflicts."""
      return {key: value for stall in stalls for key, value in stall.items()}
  ```

  ```text
  >>> merge_stalls(
  ...     {"name": "Sunrise Greens", "produce": "kale"},
  ...     {"produce": "chard", "stall_number": 4},
  ... )
  {'name': 'Sunrise Greens', 'produce': 'chard', 'stall_number': 4}
  ```

  "Later wins" is not a rule you wrote. It falls out of assigning the same key
  twice, in order. Read the double `for` carefully: the outer loop is written
  first, exactly as it would be in nested `for` statements.

  Then write it a second way with the dict union operator and decide which one
  you would rather read six months from now:

  ```python
  import functools
  import operator

  def merge_stalls(*stalls: dict[str, object]) -> dict[str, object]:
      """Fold several stall records into one; later records win on conflicts."""
      return functools.reduce(operator.or_, stalls, {})
  ```

  ```text
  {'name': 'Sunrise Greens', 'produce': 'chard', 'stall_number': 4}
  ```

- Give `total_pounds` a keyword-only `unit` that converts to kilograms:

  ```python
  def total_pounds(*weights: float, unit: str = "lb") -> float:
      """Return the basket total in `unit` ("lb" or "kg"), to two decimals."""
      total = sum(weights, 0.0)
      if unit == "kg":
          total *= 0.45359237
      elif unit != "lb":
          raise ValueError(f"unknown unit {unit!r}")
      return round(total, 2)
  ```

  ```text
  total_pounds(1.5, 2.25, 0.75) = 4.5
  total_pounds(1.5, 2.25, 0.75, unit="kg") = 2.04
  ```

  There was never a choice about keyword-only here — nothing can follow
  `*weights` loosely. The `elif unit != "lb"` matters more than it looks:
  without it, `unit="kilograms"` silently hands back pounds.

- Write `trace_call(func_name: str, *args: object, **kwargs: object) -> str`
  that reconstructs a call as a printable string:

  ```python
  def trace_call(func_name: str, *args: object, **kwargs: object) -> str:
      """Return a printable reconstruction of a call."""
      shown = [repr(a) for a in args]
      shown += [f"{name}={value!r}" for name, value in kwargs.items()]
      return f"{func_name}({', '.join(shown)})"
  ```

  ```text
  >>> trace_call("receipt_line", "Sunrise Greens", "kale", currency="CAD")
  "receipt_line('Sunrise Greens', 'kale', currency='CAD')"
  ```

  `repr` rather than `str` is deliberate: you want the quotes, so that `'3'`
  and `3` look different in the trace. And `(*args, **kwargs)` in the
  signature with `(*args, **kwargs)` at a forwarding call site is the exact
  shape every decorator you will ever read uses to pass arguments through
  untouched.

Next: [Exercise 3 — Recursion Intro](./exercise-03-recursion-intro.md).
