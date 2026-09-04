# Homework Problem 2 — Password Strength

> **Topic:** turning a table of rules into a list of booleans, counting them with `sum`, and keeping the deciding separate from the printing
> **Lecture:** [Lecture Note 1 — Defining Functions](../lecture-notes/01-defining-functions.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** the rules are given to you as a table, and the tidiest code is the one that still *looks* like that table when somebody changes it next month. This problem is where you learn that a list of five true-or-false answers is a better shape than five `if` statements, and that `True` really is `1`.

## The Brief

Every website that asks you to pick a password has an opinion about it.
Too short. Needs a capital. Needs a number. You are writing the thing
that has the opinion.

The rules are worth one point each:

| Rule | Points |
|------|--------|
| At least 8 characters long | +1 |
| Contains at least one lowercase letter | +1 |
| Contains at least one uppercase letter | +1 |
| Contains at least one digit | +1 |
| Contains at least one character that is neither a letter nor a digit | +1 |

Add the points up and give the total a name:

| Score | Label |
|-------|-------|
| 0, 1 or 2 | `"weak"` |
| 3 or 4 | `"medium"` |
| 5 | `"strong"` |

Write `password_strength(password: str) -> str` that returns one of those
three words. Then write a second function, `_demo()`, that prints the
verdict for three sample passwords, and call it from the `__main__`
guard.

Two functions, not one, and the split matters. `password_strength`
*decides*. `_demo` *prints*. A function that only decides can be checked
by comparing what it hands back to what you expected. A function that
prints can only be watched.

Notice the fifth rule says "at least one". Not "how many". A password
with four digits scores the same single point as a password with one.

## Starter

Save this as `password.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it just calls everything weak:

```python
"""Score a password against five simple rules and label its strength."""

SAMPLES: list[str] = ["hunter2", "Hunter2024", "Hunter2024!"]


def password_strength(password: str) -> str:
    """Return "weak", "medium" or "strong" for `password`.

    One point per rule met: length >= 8, has a lowercase letter, has an
    uppercase letter, has a digit, has a non-alphanumeric character.
    A score of 0-2 is weak, 3-4 is medium, 5 is strong.

    Args:
        password: The candidate password.

    Returns:
        One of "weak", "medium", "strong".

    Example:
        >>> password_strength("Hunter2024!")
        'strong'
    """
    rules = [
        len(password) >= 8,
        # TODO: has at least one lowercase letter
        # TODO: has at least one uppercase letter
        # TODO: has at least one digit
        # TODO: has at least one non-alphanumeric character
    ]
    score = sum(rules)
    # TODO: return "weak", "medium" or "strong" based on score
    return "weak"


def _demo() -> None:
    """Print the strength of three sample passwords, one per band."""
    for sample in SAMPLES:
        print(f"{sample!r:>14} -> {password_strength(sample)}")


if __name__ == "__main__":
    _demo()
```

The first rule is filled in to show the shape: each entry in `rules` is
an expression that is either `True` or `False`, one line each, in the
brief's order.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-04-functions-modules/homework/problem-02-password-strength.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `password_strength` takes one string and returns exactly one of
   `"weak"`, `"medium"` or `"strong"`.
2. All five rules from the table are checked, and each contributes at
   most one point.
3. `password_strength` prints nothing.
4. `_demo` prints one line per sample and returns nothing.
5. Type hints and a docstring on both functions.
6. Running the file prints the three sample verdicts. Importing it prints
   nothing.

## Constraints

- **One list entry per rule, in the brief's order.** Somebody will change
  these rules. When they do, they should be able to lay the new table
  beside your `rules` list and tick them off line by line. Five separate
  `if score += 1` statements do the same arithmetic in five times the
  space, and nothing stops the fourth one from quietly adding `2`.
- **Use `any(...)` over the characters, not the string method on the
  whole string.** `"Hunter2024".islower()` asks "is every letter in this
  lowercase" and answers `False`. You need "is there at least one
  lowercase letter", which is a different question. Common bugs to catch
  shows what the wrong one costs.
- **Pick samples that land in three different bands.** A demo that prints
  `weak, weak, weak` has proved nothing. The starter's three samples
  score 2, 4 and 5 on purpose.
- **`password_strength` must not print.** It returns a word. `_demo`
  turns words into lines. Keeping those apart is the reason you can test
  the first one at all.

## Expected output

```text
$ python problem-02-password-strength.py
     'hunter2' -> weak
  'Hunter2024' -> medium
 'Hunter2024!' -> strong
```

The quotes around each password come from `!r` in the f-string, which
asks for the value's `repr` — the way Python would type it back to you.
It matters here because a password can end in a space, and
`'hunter2 '` shows that where `hunter2 ` does not.

Check the boundaries yourself. These four are the interesting ones:

```bash
python -c "from password import password_strength as p; print(p(''), p('abcdefgh'), p('Abcdefg1'), p('Abcdefg1!'))"
```

```text
weak weak medium strong
```

The second one is worth a pause. `'abcdefgh'` is eight characters, so it
takes the length point, and it is all lowercase, so it takes that point
too. Two points is still `"weak"`. Eight lowercase letters and nothing
else is a bad password, and the rules agree.

And the docstring example is a real test:

```bash
python -m doctest password.py -v
```

The last three lines:

```text
1 test in 3 items.
1 passed.
Test passed.
```

## Steps

1. Activate your Week 4 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `password.py`. Run it. All three samples come back
   `weak`, because the score is never more than 1 and the bands are not
   written yet.
3. Fill in the four remaining rules. Each is one line and each starts
   with `any(`.
4. Print the score while you work:
   `python -c "from password import password_strength as p; p('Hunter2024!')"`
   will not show you anything, so temporarily add `print(score)` above the
   bands. Take it out when the numbers are right.
5. Write the three bands as early returns: `weak` first, then `medium`,
   then `strong` as the fall-through.
6. Run the file. You want `weak`, `medium`, `strong`, in that order.
7. Run the four-boundary check from **Expected output**. Boundaries are
   where band bugs live; the middles never catch anything.
8. Run `python -m doctest password.py -v`.
9. Compare against **The Solution**, tick the acceptance checklist, and
   commit: `git add homework/password.py` then
   `git commit -m "Week 4 homework: password strength"`.

## The Solution

```python
"""Score a password against five simple rules and label its strength.

Week 4 homework, problem 2, Code Crunch Convos.

Save your own copy as ``password.py`` in your ``homework/`` folder.

``password_strength`` decides. ``_demo`` prints. Keeping those two jobs in
two functions is why the decision can be tested without capturing output.
"""

SAMPLES: list[str] = ["hunter2", "Hunter2024", "Hunter2024!"]


def password_strength(password: str) -> str:
    """Return "weak", "medium" or "strong" for `password`.

    One point per rule met: length >= 8, has a lowercase letter, has an
    uppercase letter, has a digit, has a non-alphanumeric character.
    A score of 0-2 is weak, 3-4 is medium, 5 is strong.

    Args:
        password: The candidate password.

    Returns:
        One of "weak", "medium", "strong".

    Example:
        >>> password_strength("Hunter2024!")
        'strong'
    """
    rules = [
        len(password) >= 8,
        any(char.islower() for char in password),
        any(char.isupper() for char in password),
        any(char.isdigit() for char in password),
        any(not char.isalnum() for char in password),
    ]
    score = sum(rules)
    if score <= 2:
        return "weak"
    if score <= 4:
        return "medium"
    return "strong"


def _demo() -> None:
    """Print the strength of three sample passwords, one per band."""
    for sample in SAMPLES:
        print(f"{sample!r:>14} -> {password_strength(sample)}")


if __name__ == "__main__":
    _demo()
```

**Why it works.**

**The `rules` list is the brief's table, in the brief's order, one row per
line.** That is the whole design. Reading the code and reading the
specification are the same activity, so a rule that changes is a line that
changes, and a rule that is missing is a line that is missing — which you
can see at a glance.

**`sum(rules)` works because in Python `bool` is a kind of `int`.** `True`
is `1` and `False` is `0`, not by conversion but literally:

```text
>>> True + True
2
>>> isinstance(True, int)
True
```

So adding up a list of five true-or-false answers counts how many are
true. This is one of the tidiest idioms in the language and you will
reach for it constantly once you have seen it.

**`any(char.islower() for char in password)` asks the right question.**
Compare the two:

| Expression | The question it asks | On `"Hunter2024"` |
|---|---|---|
| `password.islower()` | Are *all* the letters lowercase? | `False` |
| `any(char.islower() for char in password)` | Is there *at least one* lowercase letter? | `True` |

The rule says "contains at least one", so the second one is the match.
The piece inside the brackets, `char.islower() for char in password`, is a
**generator expression**: a recipe that produces one true-or-false answer
per character, on demand. `any` walks that recipe and stops the instant it
sees a `True`.

**"Neither a letter nor a digit" is `not char.isalnum()`, and a space
counts.** `" ".isalnum()` is `False`, so `"correct horse battery"` earns
its symbol point from the spaces. That is arguably right — a space is a
perfectly good password character — but know that it is what the rule as
written does.

**The bands cascade, so no `and` is needed.** After
`if score <= 2: return "weak"`, any line below already knows the score is
at least 3. So `if score <= 4` covers exactly the 3-and-4 band without
saying `if 3 <= score <= 4`. Each early return removes cases from the
lines beneath it, and the last line needs no condition at all.

**The three samples hit three different bands.**

| Sample | Length ≥ 8 | Lower | Upper | Digit | Symbol | Score | Band |
|---|---|---|---|---|---|---|---|
| `hunter2` | no (7) | yes | no | yes | no | 2 | weak |
| `Hunter2024` | yes | yes | yes | yes | no | 4 | medium |
| `Hunter2024!` | yes | yes | yes | yes | yes | 5 | strong |

Every branch you wrote gets exercised once. That is what a demo is for.

## Run it

Copy the worked answer on this page into `problem-02-password-strength.py` and run it:
and run it:

```bash
python problem-02-password-strength.py
```

Save your own copy as `password.py` in your homework folder, and commit
that one. The longer download name is there so it cannot overwrite your
work.

## Common bugs to catch

- **Calling the string method on the whole string.**

  ```python
  if password.islower():
      score += 1                       # WRONG
  ```

  Run it on a realistic password and watch two rules collapse at once:

  ```text
  >>> "Hunter2024".islower()
  False
  >>> "Hunter2024".isupper()
  False
  ```

  Both `False`, so a password that *has* both cases scores zero on both
  case rules. There is no exception and no warning. Just wrong answers.
- **Counting characters instead of counting rules.**

  ```python
  score = sum(1 for char in password if char.isdigit())   # WRONG
  ```

  `"Hunter2024"` now scores 4 on the digit rule alone. The table says
  `+1` per rule met, not per matching character. `any` is what collapses
  "one or more" down to a single point.
- **Bands with a gap in them.**

  ```python
  if score > 5:
      return "strong"
  elif score > 3:
      return "medium"
  elif score > 2:
      return "weak"                    # WRONG: score 5 and score 2 fall off the end
  ```

  A function that falls off the end returns `None`, and the caller prints
  `None` where a band should be. Test 2, 3, 4 and 5 — the values on the
  edges of the bands. The middles never catch anything.
- **Checking the bands from weakest first with the wrong operator.**
  `if score >= 2: return "weak"` claims 3, 4 and 5 as well, so nothing is
  ever medium or strong. When conditions overlap, the order of the tests
  *is* the logic. Either go smallest-first with `<=`, as the solution
  does, or largest-first with `>=`. Do not mix.
- **Annotating `_demo` as `-> str`.** It prints and returns nothing, so
  the honest hint is `-> None`. A type hint that lies is worse than no
  type hint, because the next reader believes it.

## Under the hood

<details>
<summary>Under the hood — why True is 1, and where that bites</summary>

`bool` is not a separate kind of thing in Python. It is a subclass of
`int`, which is a strong statement: every `True` *is* an integer, and its
value is `1`.

```text
>>> True == 1
True
>>> isinstance(True, int)
True
>>> True + True + False
2
>>> [10, 20][True]
20
```

The last line is the giveaway. `True` used as a list index picks item 1,
because it *is* 1.

This is a historical accident that turned out well. Python had no boolean
type at all until version 2.3 in 2003 — comparisons returned plain `1`
and `0`. When `bool` was added, making it a subclass of `int` kept every
existing program working, and `sum(list_of_bools)` came along for free.

Where it helps:

```python
score = sum(rules)                       # count how many rules passed
vowels = sum(c in "aeiou" for c in word) # count vowels without a counter
```

Where it bites:

- A function annotated `-> int` can return `True` and no type checker
  will complain at runtime. Mostly harmless, occasionally confusing when
  it prints as `True` in a total.
- `isinstance(x, int)` is `True` for `True`. If you are validating that
  somebody passed a real number, that check lets booleans through.
- `{1: "one", True: "yes"}` is a dict with **one** key. `True` and `1`
  hash the same and compare equal, so the second entry overwrites the
  first and the key stays `1`.

  ```text
  >>> {1: "one", True: "yes"}
  {1: 'yes'}
  ```

Worth knowing, rarely worth worrying about. For counting rules it is
exactly the behaviour you want.

</details>

<details>
<summary>Under the hood — how any() short-circuits, and why the generator has no brackets</summary>

Look at the shape again:

```python
any(char.islower() for char in password)
```

There is no list in there. `char.islower() for char in password` is a
**generator expression** — a description of a sequence, not the sequence
itself. It produces one value each time somebody asks for the next one,
and it never holds more than one at a time.

`any` asks for values one at a time and returns `True` the moment it gets
one. It never asks again. That is **short-circuiting**, and it is the
same behaviour `or` has.

You can watch it happen:

```python
def noisy(char: str) -> bool:
    """Report each character as it is tested."""
    print(f"testing {char!r}")
    return char.islower()


print(any(noisy(c) for c in "ABCdEF"))
```

```text
testing 'A'
testing 'B'
testing 'C'
testing 'd'
True
```

Four characters tested out of six. `'E'` and `'F'` were never looked at,
because the answer could not change.

Now the version with brackets:

```python
print(any([noisy(c) for c in "ABCdEF"]))
```

```text
testing 'A'
testing 'B'
testing 'C'
testing 'd'
testing 'E'
testing 'F'
True
```

All six. The square brackets build a **list comprehension**, and a list
has to be finished before it can be handed to `any`. Every character gets
tested whether it matters or not, and the whole list of results sits in
memory in the meantime.

For a password, the difference is a few microseconds and a few bytes.
For a file with a million lines, it is the difference between an answer
and a machine that has run out of memory. Same three characters of
difference in the source.

The sibling of `any` is `all`, which short-circuits the other way: it
stops at the first `False`. And the empty cases are worth memorising
because they surprise people once:

```text
>>> any([])
False
>>> all([])
True
```

"Is there at least one true thing in nothing" is no. "Is everything in
nothing true" is yes, vacuously — there is no counter-example to point
at.

</details>

## Acceptance checklist

- [ ] `python password.py` prints exactly three lines, one per sample.
- [ ] The three verdicts are `weak`, `medium`, `strong`, in that order.
- [ ] `password_strength('')` returns `"weak"`.
- [ ] `password_strength('abcdefgh')` returns `"weak"`, not `"medium"`.
- [ ] `password_strength('Abcdefg1')` returns `"medium"`.
- [ ] `password_strength('Abcdefg1!')` returns `"strong"`.
- [ ] `password_strength` contains no `print`.
- [ ] Both functions have type hints and a docstring; `_demo` is
      annotated `-> None`.
- [ ] `python -c "import password"` prints nothing.
- [ ] Committed with a message like
      `Week 4 homework: password strength`.

## Stretch

- **Return the score as well as the band.** Change the return type to
  `tuple[str, int]` and hand back `(band, score)`. The demo can then
  print `'hunter2' -> weak (2)`, which turns every run into an
  explanation instead of a verdict. Update the docstring's `Returns:` and
  its `Example:` — a doctest that no longer matches is a failing test,
  which is the system working.
- **Say which rules failed.** Build a parallel list of rule names, zip it
  with `rules`, and print the ones that came back `False`. This is what
  a real signup form does, and it is about five lines.
- **Make the rules data instead of code.** A list of
  `(name, function)` pairs, where each function takes the password and
  returns a bool. `rules = [ok for name, ok in checks]` then does the
  same job, and adding a rule never touches `password_strength` at all.
  This is the same table-driven move `CASES` makes in problem 3.
- **Add a rule that subtracts.** Dock a point for a password that appears
  in a small built-in list of common ones — `password`, `123456`,
  `qwerty`. Watch what `sum` does when one of the entries can be `-1`,
  and decide whether the bands still make sense or need their own
  rethink.
- **Check a longer password beats a complicated one.** Score
  `"correct horse battery staple"` and then `"P@ss1!"`. The rules as
  written prefer the second. Most modern password guidance prefers the
  first. Write two sentences in your journal about what the rules are
  actually measuring, and what they are not.

Next: [Homework Problem 3 — Leap Year Function With Tests](./problem-03-leap-year-function-with-tests.md).
