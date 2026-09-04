# Exercise 1 — The Dog Class

> **Topic:** classes, `__init__`, `self`, methods, and giving every object its own stuff
> **Lecture:** [01 — Classes and Instances](../lecture-notes/01-classes-and-instances.md)
> **Difficulty:** Beginner
> **Target time:** 30 minutes
> **Why this one:** every class you write this week starts the same way — a `class` line, an `__init__`, and things hung off `self`. This exercise also walks you straight into one particular bug on purpose, because that bug is silent, it is common, and once you have watched two dogs share one trick list you will never write it again.

## The Brief

Mesa Dog Walkers keeps a list of the dogs on each route. Right now that list
is a pile of dictionaries and a stack of loose functions, and every new
feature means passing the same dictionary into one more function.

You are going to replace it with a `Dog` class.

A **class** is a form to fill in. It is not a dog. It says what shape a dog
has: a name, an age, a list of tricks. Filling the form in gives you an
**instance** — one actual dog, with one actual name. `Dog` is the form.
`Biscuit` is a dog.

Each dog knows its own name, its own age, and its own list of tricks, and it
carries the things that belong to it: barking, having a birthday, learning
something new. Those are **methods** — functions that live inside the class
and get handed the dog they were called on.

The interesting part is the trick list. Every dog needs one, and every dog
needs *its own*. Where you create that list decides whether the roster works
or quietly reports that a dog you have never trained knows how to sit.

## Starter

Create `exercise-01-dog-class.py` in your practice repo with this content,
then fill in the `TODO` markers:

```python
"""exercise-01-dog-class.py — one blueprint, many independent dogs.

Models the dogs on a route for Mesa Dog Walkers. Run it with:

    python exercise-01-dog-class.py
"""


class Dog:
    """A single dog on the walking roster."""

    species: str = "Canis familiaris"

    def __init__(self, name: str, age: int) -> None:
        """Store this dog's name and age, and give it an empty trick list."""
        # TODO: set self.name, self.age, and self.tricks (a brand-new list)

    def bark(self) -> str:
        """Return this dog's greeting, e.g. `Biscuit says woof!`."""
        # TODO: build the string from self.name
        raise NotImplementedError

    def have_birthday(self) -> None:
        """Add one year to this dog's age. Returns nothing."""
        # TODO: mutate self.age

    def learn(self, trick: str) -> None:
        """Append one trick to this dog's own trick list."""
        # TODO: append to self.tricks

    def __repr__(self) -> str:
        """Developer form, e.g. `Dog(name='Biscuit', age=4)`."""
        # TODO: use !r on both values
        raise NotImplementedError

    def __str__(self) -> str:
        """User form, e.g. `Biscuit, age 4, knows: sit, wait`."""
        # TODO
        raise NotImplementedError


def main() -> None:
    """Run two dogs through a day and print what changed."""
    biscuit = Dog("Biscuit", 3)
    juniper = Dog("Juniper", 7)

    print(biscuit.bark())
    print(juniper.bark())

    biscuit.learn("sit")
    biscuit.learn("wait")
    biscuit.have_birthday()

    print(biscuit)
    print(juniper)
    print(repr(biscuit))
    print(Dog.species)


if __name__ == "__main__":
    main()
```

Four words in that starter you need before you begin.

**`self`.** The first parameter of every method, and it is the dog the method
was called on. When you write `biscuit.bark()`, Python quietly passes
`biscuit` in as `self`. You never type it at the call site; you always type
it in the definition. `self.name` therefore means "this particular dog's
name", and it is how one piece of code works for every dog on the roster.

**`__init__`.** The method Python runs the moment you build a new dog. It is
where you hang things off `self` for the first time. It runs **once per dog**
— which is the single fact this whole exercise turns on.

**A class attribute.** A value written straight in the class body, outside any
method. `species` is one. The class body runs **once**, when Python first
reads the file, so a class attribute is one single object that every dog
looks at. That is right for `species`, because every dog on the roster is the
same species. It is very wrong for `tricks`.

**Dunder methods.** `__repr__` and `__str__` have two underscores on each
side, which is why people say "dunder". You never call them directly. Python
calls them for you: `print(dog)` reaches for `__str__`, and `repr(dog)`
reaches for `__repr__`. Two spellings of the same dog, for two different
readers.

## Requirements

1. `__init__` sets exactly three things on `self`: `self.name`, `self.age`,
   and `self.tricks`. `self.tricks` starts as an empty list.
2. `species` stays a **class attribute** with the value
   `Canis familiaris`. Do not move it into `__init__` — every dog on the
   roster shares it, and that is what class attributes are for.
3. `bark()` returns (does not print) the string
   `<name> says woof!` — for example `Biscuit says woof!`.
4. `have_birthday()` returns `None` and increases `self.age` by one.
5. `learn(trick)` returns `None` and appends `trick` to that dog's list.
6. `__repr__` returns `Dog(name='Biscuit', age=4)` — the quotes around the
   name come from `!r`, not from quotes you typed.
7. `__str__` returns `<name>, age <age>, knows: <tricks joined by ", ">`.
   When the dog knows nothing yet, the part after `knows: ` is exactly
   `no tricks yet`.
8. Do not edit `main()`. It is the test — if your class is right, the
   output below appears without you touching the demo.

## Constraints

- **Create the trick list inside `__init__`, not in the class body.** A
  class attribute is one object shared by every instance, so `tricks = []`
  at class level gives all dogs the same list, and teaching Biscuit to sit
  teaches Juniper too. `self.tricks = []` in `__init__` runs once per dog
  and produces one list per dog.

  Here is the part that makes the bug so hard to spot: nothing in the wrong
  version *looks* like sharing. `self.tricks.append("sit")` is not an
  assignment. It reaches into a list and changes it in place. Python only
  creates a new thing on `self` when you **assign** to it, so an `append`
  never gets the chance — it just finds the class's one list and edits it.
  Lecture 01, section 6 shows the failure in full.
- **`bark()` returns a string; it must not call `print()`.** A method that
  prints can only ever be used for printing. A method that returns can be
  printed, joined into a report, written to a log, or checked by a test. You
  will write `assert biscuit.bark() == "Biscuit says woof!"` in Week 11, and
  that line is only possible because `bark` hands the string back.
- **Use `!r` inside `__repr__`.** `f"name={self.name}"` gives
  `name=Biscuit`, which hides the fact that the value is a string.
  `f"name={self.name!r}"` gives `name='Biscuit'`, which you could paste back
  into the REPL to rebuild the dog. That is the whole job of `__repr__`.
- **No imports.** Everything here is core syntax. If you find yourself
  reaching for a module, you have taken a detour.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-dog-class.py
Biscuit says woof!
Juniper says woof!
Biscuit, age 4, knows: sit, wait
Juniper, age 7, knows: no tricks yet
Dog(name='Biscuit', age=4)
Canis familiaris
```

Line four is the one that matters. Juniper never learned anything, so
Juniper's list must still be empty. If line four mentions `sit, wait`, the
two dogs are sharing one list and you have the class-attribute bug.

Line five is the same dog as line three, spelled for a different reader.
Line three is what you would put on a roster; line five is what you would
want to see in a log at two in the morning.

## Steps

1. Create the file and run it before you write anything:
   `python exercise-01-dog-class.py`. It should fail. Failing on purpose,
   first, tells you the file is where you think it is.
2. Fill in `__init__`, then run again. You will get a `NotImplementedError`
   from `bark` — that is progress. It means building a dog worked.
3. Implement `bark`, run, and check the first two lines match.
4. Implement `have_birthday` and `learn`, then `__str__`. Run and compare
   lines three and four character by character.
5. Implement `__repr__` and check line five. Notice that `print(biscuit)`
   and `print(repr(biscuit))` now give different strings — that is the point
   of having both.
6. Prove the two dogs are independent. Add this to the bottom of `main()`,
   run, then delete it:
   `assert juniper.tricks == [], juniper.tricks`
7. Experiment: put `Dog.species = "Canis lupus"` on the line before
   `print(Dog.species)` and watch both dogs change species at once. Undo it
   before you commit.

## The Solution

```python
"""exercise-01-dog-class-solution.py — one blueprint, many independent dogs.

Models the dogs on a route for Mesa Dog Walkers. The `-solution` in the name
keeps this file from colliding with the `exercise-01-dog-class.py` you write
yourself. Run it with::

    python exercise-01-dog-class-solution.py
"""


class Dog:
    """A single dog on the walking roster."""

    species: str = "Canis familiaris"

    def __init__(self, name: str, age: int) -> None:
        """Store this dog's name and age, and give it an empty trick list."""
        self.name = name
        self.age = age
        self.tricks: list[str] = []

    def bark(self) -> str:
        """Return this dog's greeting, e.g. `Biscuit says woof!`."""
        return f"{self.name} says woof!"

    def have_birthday(self) -> None:
        """Add one year to this dog's age. Returns nothing."""
        self.age += 1

    def learn(self, trick: str) -> None:
        """Append one trick to this dog's own trick list."""
        self.tricks.append(trick)

    def __repr__(self) -> str:
        """Developer form, e.g. `Dog(name='Biscuit', age=4)`."""
        return f"Dog(name={self.name!r}, age={self.age!r})"

    def __str__(self) -> str:
        """User form, e.g. `Biscuit, age 4, knows: sit, wait`."""
        known = ", ".join(self.tricks) if self.tricks else "no tricks yet"
        return f"{self.name}, age {self.age}, knows: {known}"


def main() -> None:
    """Run two dogs through a day and print what changed."""
    biscuit = Dog("Biscuit", 3)
    juniper = Dog("Juniper", 7)

    print(biscuit.bark())
    print(juniper.bark())

    biscuit.learn("sit")
    biscuit.learn("wait")
    biscuit.have_birthday()

    print(biscuit)
    print(juniper)
    print(repr(biscuit))
    print(Dog.species)


if __name__ == "__main__":
    main()
```

**`species` and `tricks` are both "a thing every dog has", and they belong in
opposite places.** The difference is not what they hold. It is who owns the
value. Every dog on the roster is the same species, and if the scientists
rename it you want one edit to change every dog at once — so `species` is one
object, stored on `Dog` itself. Every dog also has a trick list, but
Biscuit's tricks are not Juniper's tricks, and teaching one dog must never
teach the other — so `tricks` has to be built inside `__init__`, which is the
code that runs once per dog.

**`bark` returns instead of printing, and that is a design decision, not a
style preference.** A method that prints has exactly one use. A method that
returns can be printed, put in an f-string, joined into a report, written to
a log, or compared against an expected value in a test. `print(biscuit.bark())`
costs you four extra characters at the call site and buys you all of that.

**`__repr__` and `__str__` answer questions from two different people.**
`__str__` is for whoever is reading the roster, so it reads like a sentence.
`__repr__` is for whoever is reading a log, so it reads like the line of code
that would rebuild the dog. `!r` is what makes the second one true: it asks
the value for *its* repr, so a string comes back with quotes on it.
`Dog(name='Biscuit', age=4)` tells you the name is a string.
`Dog(name=Biscuit, age=4)` looks like it might be a variable — and when a
name has a stray space on the end, only the quoted form shows you.

**`__str__` handles the empty list explicitly rather than letting `join` do
it.** `", ".join([])` returns the empty string, so a dog with no tricks would
print `Juniper, age 7, knows: ` with a trailing space and nothing after it.
The requirement asks for `no tricks yet`, and the conditional expression is
the smallest honest way to say it. This is a small case of a large habit: the
empty case is a case, and if you do not name it, the output names it for you
badly.

## Run it

Copy the worked answer on this page into `exercise-01-dog-class.py` and run it:

```bash
python exercise-01-dog-class.py
```

It needs no setup and imports nothing. The `-solution` in the name keeps it
from colliding with your own `exercise-01-dog-class.py`, so you can keep both
in the same folder and diff them.

## Common bugs to catch

- **Juniper knows Biscuit's tricks.**

  ```text
  Biscuit, age 3, knows: sit, wait
  Juniper, age 7, knows: sit, wait
  ```

  No traceback, no warning. Juniper knows two tricks nobody taught her. You
  wrote `tricks = []` in the class body, so the class holds one list and both
  dogs are looking at it. Move the line into `__init__` as
  `self.tricks = []` and line two becomes `no tricks yet`.

- **`AttributeError: 'Dog' object has no attribute 'tricks'`.** You wrote
  `tricks = []` inside a method other than `__init__`, or you assigned to a
  bare local `tricks` instead of `self.tricks`. Without the `self.` prefix
  you created an ordinary variable that vanished when the method returned.

- **`TypeError: Dog.bark() takes 0 positional arguments but 1 was given`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 9, in <module>
      Dog("Biscuit", 3).bark()
      ~~~~~~~~~~~~~~~~~~~~~~^^
  TypeError: Dog.bark() takes 0 positional arguments but 1 was given
  ```

  The message reads backwards the first time you see it. You called `bark()`
  with no arguments, and Python says you passed one. That one argument is the
  dog. `biscuit.bark()` is shorthand for `Dog.bark(biscuit)`, so every method
  needs a parameter waiting to catch it. You wrote `def bark():` and left out
  `self`.

- **`TypeError: __init__() should return None, not 'Dog'`.** You added
  `return self` at the end of `__init__`. Initialisers set the object up and
  return nothing; Python hands the dog back for you.

- **`None` prints where a bark should be.**

  ```text
  Biscuit says woof!
  None
  ```

  Two lines where one was expected. `bark` ends with `print(...)` instead of
  `return ...`, so it printed the bark and then returned `None` — every
  function with no `return` returns `None` — and the outer `print` dutifully
  printed that too. Whenever a stray `None` shows up in your output, look for
  a method that prints where it should return.

- **`Dog(name=Biscuit, age=4)` with no quotes.** You forgot `!r` on the name.
  Nothing raises; the repr is simply less useful, because you can no longer
  paste it back into a REPL and get the same dog.

- **`TypeError: sequence item 0: expected str instance, int found`.** You
  passed something that is not a string into `learn()` and then hit
  `", ".join(...)`. `join` only joins strings.

## Under the hood

<details>
<summary>Under the hood — what self really is, and why a method is not just a function</summary>

`self` is not magic and it is not a keyword. You could rename it `dog` and
everything would still work. It is simply the first parameter, and Python
fills it in for you. Here is the mechanism, one step at a time.

Look up a method on the **class** and you get a plain function:

```text
>>> Dog.bark
<function Dog.bark at 0x0000023E0A5B1DA0>
>>> type(Dog.bark)
<class 'function'>
```

Look up the same name on an **instance** and you get something else:

```text
>>> biscuit = Dog("Biscuit", 3)
>>> biscuit.bark
<bound method Dog.bark of Dog(name='Biscuit', age=3)>
>>> type(biscuit.bark)
<class 'method'>
```

A **bound method** is a small object holding two things: the function, and
the instance it was fetched from. You can see both:

```text
>>> biscuit.bark.__func__ is Dog.bark
True
>>> biscuit.bark.__self__ is biscuit
True
```

Calling it inserts `__self__` as the first argument and then calls
`__func__`. So these two lines do exactly the same work:

```text
>>> biscuit.bark()
'Biscuit says woof!'
>>> Dog.bark(biscuit)
'Biscuit says woof!'
```

That second form is what the `TypeError` in the bugs list above is really
complaining about. `def bark():` accepts nothing, and Python handed it a dog.

The binding happens on **attribute access**, not at definition time. That is
why you can pull a bound method out and pass it around, and it keeps its dog:

```text
>>> greet = biscuit.bark
>>> greet()
'Biscuit says woof!'
```

`greet` is not a function that will look up a dog later. It is a function
that already has one. Homework problem 5 leans on exactly this: you subscribe
`recorder.record` to a sensor, and the sensor never needs to know which
recorder it belongs to, because the bound method already does.

One consequence worth knowing. Two bound methods fetched from the same
instance are different *objects* but compare equal:

```text
>>> biscuit.bark is biscuit.bark
False
>>> biscuit.bark == biscuit.bark
True
```

Each attribute access builds a fresh binding, which is why `is` says no. They
compare equal because their function and their instance match, which is why
`list.remove(recorder.record)` finds the one you subscribed even though it is
a different object.

</details>

<details>
<summary>Under the hood — where Python actually looks when you write biscuit.name</summary>

Every instance carries a dictionary of its own, and you can read it:

```text
>>> biscuit = Dog("Biscuit", 3)
>>> biscuit.learn("sit")
>>> biscuit.__dict__
{'name': 'Biscuit', 'age': 3, 'tricks': ['sit']}
```

`species` is not in there. It never will be, because nothing in `__init__`
assigns it. And yet:

```text
>>> biscuit.species
'Canis familiaris'
```

The rule is: **instance first, then the class.** Python checks
`biscuit.__dict__`, finds nothing called `species`, and falls through to
`Dog.__dict__`, where it is waiting. (The full rule also walks the class's
parents, which is Exercise 3's Under the hood block.)

That fall-through is the whole class-attribute bug in one sentence. With
`tricks = []` in the class body, `self.tricks` finds nothing on the instance,
falls through to the class, and returns the class's one list — for every dog.
`append` then edits that one list, and because `append` is not an assignment,
the instance dictionary stays empty forever.

Assignment works the other way. It never falls through — it always writes to
the instance:

```text
>>> juniper = Dog("Juniper", 7)
>>> juniper.species = "Canis lupus"
>>> juniper.__dict__
{'name': 'Juniper', 'age': 7, 'tricks': [], 'species': 'Canis lupus'}
>>> biscuit.species
'Canis familiaris'
>>> Dog.species
'Canis familiaris'
```

Juniper now has her own `species` that shadows the class's. Biscuit and the
class are untouched. This is also the answer to the first stretch goal:
`self.count += 1` reads the class's counter, adds one, and then *assigns* the
result to the instance — so every dog quietly gets a private counter stuck at
1 and the shared one never moves. `Dog.count += 1` writes to the class, which
is what you meant.

</details>

## Acceptance checklist

- [ ] `python exercise-01-dog-class.py` runs with no traceback.
- [ ] All six output lines match the expected output exactly.
- [ ] `species` is defined once, in the class body, not in `__init__`.
- [ ] `juniper.tricks` is still `[]` after Biscuit learns two tricks.
- [ ] `bark()` returns its string instead of printing it.
- [ ] `repr(biscuit)` and `str(biscuit)` produce different strings.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 1: Dog class`.

## Stretch

- Add a class attribute `count` that tracks how many dogs have been created,
  and increment it inside `__init__` with `Dog.count += 1`. Then try
  `self.count += 1` instead and explain, in a comment, why that silently
  gives every dog a private counter and stops the shared one working. The
  second Under the hood block above has the answer if you get stuck.
- Add `is_senior()` returning `True` when `age >= 7`, then print a roster
  line for each dog that flags the senior dogs. Juniper qualifies.
- Print `biscuit.__dict__` and `Dog.__dict__.keys()` side by side. Find
  `species` in one and `name`, `age`, `tricks` in the other. That is the
  lookup order, made visible.

When your roster prints cleanly, move on to
[Exercise 2 — Rectangle](./exercise-02-rectangle.md).
