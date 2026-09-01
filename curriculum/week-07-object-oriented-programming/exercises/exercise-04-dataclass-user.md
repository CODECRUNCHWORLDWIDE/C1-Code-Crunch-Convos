# Exercise 4 — Dataclass User

> **Topic:** `@dataclass`, `field(default_factory=...)`, `__post_init__`, and the `__eq__` you get for free
> **Lecture:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** most classes in working Python are record types — a bundle of named values and not much else — and hand-writing `__init__`, `__repr__`, and `__eq__` for each one is how typos get into equality checks. `@dataclass` writes all three correctly from a four-line field list. This exercise also pins down what "equal" means for a record, which is the difference between `==` and `is` — a distinction that quietly breaks tests for people who never nailed it down.

## The Brief

The org's workshop signup sheet is a list of dictionaries with keys that are
spelled three different ways. You are replacing it with a `User` **record
type**: a username, an email, a list of topics the person wants to learn, and
a flag for whether the signup is still active.

You already know how to write that class by hand — Exercise 1 was the same
shape. The point of this one is that you should not have to. Python ships a
decorator, `@dataclass`, that reads a list of field names and writes
`__init__`, `__repr__` and `__eq__` for you, correctly, every time.

A **decorator** is a line starting with `@` above a class or a function. It
means "take this thing, hand it to that other thing, and use whatever comes
back". `@dataclass` takes your class, looks at the annotated names in its
body, and hands back the same class with three methods added.

Two things make this more than typing four lines.

First, the interests list has to be a *new* list per user — the same trap as
Biscuit's tricks in Exercise 1. Modern Python refuses to let you write it the
obviously wrong way at all, with an error message worth meeting on purpose.

Second, once the dataclass generates `__eq__`, two separately created users
with identical data compare equal. That is almost always what you want from a
record, and it is not what `is` tells you.

## Starter

Create `exercise-04-dataclass-user.py` and fill in the `TODO` markers:

```python
"""exercise-04-dataclass-user.py — a record type in four lines.

Models a workshop signup for the org's community sessions. Run it with:

    python exercise-04-dataclass-user.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    """One person signed up for a workshop."""

    # TODO: declare four fields, in this exact order:
    #   username : str
    #   email    : str
    #   interests: list[str], defaulting to a NEW empty list per user
    #   active   : bool, defaulting to True
    #
    # Every field needs a type annotation. A bare `name = value` line is
    # a plain class attribute and the dataclass will ignore it.

    def __post_init__(self) -> None:
        """Reject a signup whose email could not possibly be an email."""
        # TODO: if "@" is not in self.email, raise
        # ValueError(f"email must contain '@', got {self.email!r}")

    def add_interest(self, topic: str) -> None:
        """Record one topic. Adding the same topic twice changes nothing."""
        # TODO: append only when topic is not already in self.interests


def main() -> None:
    """Sign two people up, compare records, and reject one bad email."""
    rlopez = User("rlopez", "rlopez@example.org", ["python", "gis"])
    amina = User("amina", "amina@example.org")

    print(rlopez)
    print(amina)

    twin = User("rlopez", "rlopez@example.org", ["python", "gis"])
    print(f"equal: {rlopez == twin}   same object: {rlopez is twin}")

    rlopez.add_interest("mapping")
    rlopez.add_interest("python")
    print(f"rlopez interests: {rlopez.interests}")
    print(f"amina interests: {amina.interests}")

    try:
        User("dana", "not-an-email")
    except ValueError as exc:
        print(f"Rejected: {exc}")


if __name__ == "__main__":
    main()
```

Four terms before you begin.

**An annotation** is the `name: type` form, with a colon. `username: str` is
an annotation. `username = str` is an assignment, and the dataclass ignores
it completely. That is why the requirements insist on colons — the colon is
the entire signal.

**A field** is what an annotated name becomes once `@dataclass` has read it:
a parameter of the generated `__init__` and an entry in the generated
`__repr__` and `__eq__`.

**`field(default_factory=list)`** is how you say "give each user a brand-new
empty list". A *factory* is something you call to make a fresh one. `list` is
the callable; `list()` is one already-built empty list, which is the thing
you are trying not to share. There are no parentheses on purpose.

**`__post_init__`** is a method the generated `__init__` calls as its very
last line. It is where checks go, so that a `User` which exists is a `User`
whose email has an `@` in it.

## Requirements

1. `User` is decorated with `@dataclass` and declares exactly four annotated
   fields in the order given: `username`, `email`, `interests`, `active`.
2. `interests` defaults to a new empty list, created with
   `field(default_factory=list)`. Note that it is `list`, the callable — not
   `list()`, the result of calling it.
3. `active` defaults to `True`.
4. `__post_init__` raises `ValueError` with the message
   `email must contain '@', got 'not-an-email'` when the email has no `@`.
   The quotes around the value come from `!r`.
5. `add_interest` appends only when the topic is not already present, and
   returns `None`. The order of the existing entries never changes.
6. You write no `__init__`, no `__repr__`, and no `__eq__`. All three are
   generated. If you find yourself typing one, stop and re-read the
   requirement.
7. Do not edit `main()`.

## Constraints

- **`field(default_factory=list)`, never `interests: list[str] = []`.** The
  second form does not silently share one list the way Exercise 1's class
  attribute did — the `dataclasses` module checks for it and refuses to build
  the class at all. The factory is a zero-argument callable that the
  generated `__init__` calls once per instance, which is exactly the
  `self.interests = []` you would have written by hand.
- **Fields with defaults must come after fields without them.** Same rule as
  function parameters, same reason: the generated `__init__` is a real
  function signature, and `def __init__(self, interests=[], email)` is not
  valid Python. That is why the field order in the requirements is not
  negotiable.
- **Validate in `__post_init__`, not in a separate `validate()` you have to
  remember to call.** `__post_init__` runs at the end of the generated
  `__init__`, so an invalid `User` cannot be constructed. A validator
  somebody has to call by hand is a validator somebody will forget — and the
  object they forgot it on is the one that reaches production.
- **Use `==` to compare records and `is` only to compare identity.** `==`
  asks "do these hold the same data"; `is` asks "are these the same object in
  memory". The generated `__eq__` compares all four fields, which is why
  `rlopez == twin` is `True` while `rlopez is twin` is `False`. Reach for
  `is` only with `None`, `True`, and `False` — the three objects Python
  guarantees there is only one of.
- **Do not add `frozen=True` yet.** The demo changes `interests` after
  construction, and a frozen instance would still allow that (the list itself
  is not frozen) while blocking field assignment — a confusing half-measure.
  Immutability is the stretch goal, where you can do it properly.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-dataclass-user-solution.py
User(username='rlopez', email='rlopez@example.org', interests=['python', 'gis'], active=True)
User(username='amina', email='amina@example.org', interests=[], active=True)
equal: True   same object: False
rlopez interests: ['python', 'gis', 'mapping']
amina interests: []
Rejected: email must contain '@', got 'not-an-email'
```

Line five is the one that proves the factory worked: amina's list is still
empty after rlopez picked up a third interest. Line four proves
`add_interest` ignored the duplicate `python` — three entries, not four.

Both of the first two lines end in `active=True`, which is how you know all
four fields were declared. A three-field class produces no error at all here,
just a repr that quietly does not match.

## Steps

1. Create the file and run it. Before you declare any fields you get
   `TypeError: User.__init__() takes 1 positional argument but 4 were given`
   — a dataclass with no annotated fields generates an `__init__` that
   accepts nothing but `self`.
2. Add `username` and `email` with annotations and no defaults. Run — `amina`
   will now fail, because the demo relies on the two defaulted fields.
3. Add `interests` with `field(default_factory=list)` and
   `active: bool = True`. Run again. The first three lines should now be
   correct with no `__repr__` written by you.
4. On purpose, change the interests line to `interests: list[str] = []` and
   run. Read the error in full — it names the field and it names the fix.
   Change it back.
5. Implement `add_interest`, then confirm lines four and five.
6. Implement `__post_init__` and confirm the last line.
7. In the REPL, import your `User` and try `{User("a", "a@b.c")}` — building
   a set of one user. Read the `TypeError`, then read the last Under the hood
   block on this page.

## The Solution

```python
"""exercise-04-dataclass-user-solution.py — a record type in four lines.

Models a workshop signup for the org's community sessions. The `-solution` in
the name keeps this file from colliding with the
`exercise-04-dataclass-user.py` you write yourself. Run it with::

    python exercise-04-dataclass-user-solution.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    """One person signed up for a workshop."""

    username: str
    email: str
    interests: list[str] = field(default_factory=list)
    active: bool = True

    def __post_init__(self) -> None:
        """Reject a signup whose email could not possibly be an email."""
        if "@" not in self.email:
            raise ValueError(f"email must contain '@', got {self.email!r}")

    def add_interest(self, topic: str) -> None:
        """Record one topic. Adding the same topic twice changes nothing."""
        if topic not in self.interests:
            self.interests.append(topic)


def main() -> None:
    """Sign two people up, compare records, and reject one bad email."""
    rlopez = User("rlopez", "rlopez@example.org", ["python", "gis"])
    amina = User("amina", "amina@example.org")

    print(rlopez)
    print(amina)

    twin = User("rlopez", "rlopez@example.org", ["python", "gis"])
    print(f"equal: {rlopez == twin}   same object: {rlopez is twin}")

    rlopez.add_interest("mapping")
    rlopez.add_interest("python")
    print(f"rlopez interests: {rlopez.interests}")
    print(f"amina interests: {amina.interests}")

    try:
        User("dana", "not-an-email")
    except ValueError as exc:
        print(f"Rejected: {exc}")


if __name__ == "__main__":
    main()
```

**Four annotated lines generate `__init__`, `__repr__` and `__eq__`, and all
three are the versions you would have written on your best day.** The
generated `__repr__` is
`User(username='rlopez', email='rlopez@example.org', interests=['python', 'gis'], active=True)`
— every field, in declaration order, each one repr'd — which is exactly the
shape Exercise 1 asked you to type by hand. The generated `__eq__` compares
all four fields at once. Hand-writing that is where typos live: you compare
three fields and forget the fourth, and now two users who differ in `active`
compare equal, and the bug shows up in a test six weeks later as an assertion
that passes when it should not.

The word doing the work is *annotated*. `username: str` is an annotation and
becomes a field. `username = str` assigns the type object to a plain class
attribute, and the dataclass ignores it completely.

**`field(default_factory=list)` passes the function, not a list.** A default
*value* is worked out once, when the class is created, so
`interests: list[str] = []` would mean one list for the entire program — the
Biscuit-and-Juniper bug in dataclass clothing. A default *factory* is a
zero-argument callable that the generated `__init__` calls once per instance,
so each user gets a fresh list. It is precisely the `self.interests = []` you
would have written by hand, said declaratively.

`dataclasses` also refuses the mutable-default version outright rather than
letting it fail silently. That refusal is a genuine kindness — the equivalent
bug in Exercise 1 costs an afternoon, and here it costs one error message at
import time.

**Defaulted fields must come last, because the generated `__init__` is a real
function signature.** `def __init__(self, username, email, interests=..., active=True)`
is legal Python; put `interests` before `email` and you get
`def __init__(self, username, interests=..., email, active=True)`, which is
not. Same rule you already know about function parameters, now applied to
code you did not type — which is why it is worth knowing the code exists.

**`__post_init__` runs as the last statement of the generated `__init__`, so
checking happens at the boundary.** Same property Exercise 2 got from
validating in the setter: a `User` that exists is a `User` whose email has an
`@` in it, everywhere in the program, with no downstream check needed. The
two underscores on each side matter — Python looks up that exact name, and a
method called `post_init` is a method nothing ever calls.

**`equal: True   same object: False` is the line worth pausing on.** `rlopez`
and `twin` are two distinct objects at two distinct addresses, so `is` is
`False` and always will be. They hold identical data, so the generated
`__eq__` says `True`. Almost every time you want to compare records, `==` is
the question you meant.

**`add_interest` checks membership before appending, so calling it twice does
nothing the second time.** For a list this short, `topic not in self.interests`
is a linear scan and completely fine. If the list grew to thousands, a `set`
would be the right structure, at the cost of the ordering the requirement
asks for. Choosing the structure that fits the requirement rather than the
fastest one is the correct move here.

## Download and run

Download
[exercise-04-dataclass-user-solution.py](./exercise-04-dataclass-user-solution.py)
and run it:

```bash
python exercise-04-dataclass-user-solution.py
```

It imports only `dataclasses` from the standard library and needs no setup.
The `-solution` in the name keeps it from colliding with your own
`exercise-04-dataclass-user.py`.

## Common bugs to catch

- **`ValueError: mutable default <class 'list'> for field interests is not
  allowed: use default_factory`.** You wrote `= []` or `field(default=[])`.
  This fires when the class is *defined*, before any instance exists — the
  module checked for the trap and refused to build the class. The message
  names the field and names the fix.

- **`TypeError: 'list' object is not callable`.** You wrote
  `field(default_factory=list())` with parentheses.

  ```text
  Traceback (most recent call last):
    File "wrong.py", line 11, in <module>
      print(User("amina", "amina@example.org"))
            ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<string>", line 5, in __init__
  TypeError: 'list' object is not callable
  ```

  Read where it happened. The class definition **succeeded** — `field` never
  checks that its argument is callable — and the failure waited until the
  first `User` was built, when the generated `__init__` tried to call `[]`.

  So this mistake does not give you one shared list. It gives you no users at
  all. The two mistakes look similar and fail completely differently: `= []`
  is caught at class-definition time, and `default_factory=list()` is caught
  at the first construction. Neither one can produce the "amina has rlopez's
  interests" symptom, because neither one ever produces a working `User`.

  The odd `File "<string>", line 5, in __init__` frame with no source line
  under it is the generated `__init__`. It was compiled from a string that
  `dataclasses` built, so there is no file for the traceback to quote.

- **`TypeError: non-default argument 'email' follows default argument 'interests'`.**
  You put a defaulted field above a plain one. Also raised at
  class-definition time. Reorder so every defaulted field sits at the bottom.
  (On Python 3.13 the message names both fields, which is a recent
  improvement — older versions named only the non-default one and left you
  guessing which default was above it.)

- **`TypeError: User.__init__() takes 1 positional argument but 4 were given`.**
  The decorator is there but the dataclass found no fields. Your field lines
  use `=` where they need `:`. Compare with the same demo on a class that has
  no decorator at all, which gives `TypeError: User() takes no arguments`.
  Two different messages for two different mistakes: "the decorator found no
  fields" versus "there is no decorator". The first mentions `__init__`
  because one was generated; the second does not, because none was.

- **The first two lines print but have no `active=True` on the end.** You
  declared only three fields. Nothing raises, because the demo never passes a
  fourth argument — the only symptom is a repr that does not match. This is
  why the expected output is compared line for line.

- **`equal: False`.** You hand-wrote an `__eq__` that compares with `is`, or
  you added `eq=False` to the decorator. Delete your version and let the
  dataclass generate it.

- **The last line never prints.** `__post_init__` is misspelled — it needs two
  underscores on each side. A method named `post_init` or `__post_init` is
  never called by anything, so the bad email sails through and no exception
  reaches the `except`.

- **`TypeError: unhashable type: 'User'`.** You tried to put users in a set or
  use one as a dict key. That is not a bug; the last Under the hood block
  explains why, and `frozen=True` is the fix.

## Under the hood

<details>
<summary>Under the hood — what @dataclass actually generates, and how to read it</summary>

`@dataclass` is not compiler magic. It is an ordinary function that receives
your class, reads `__annotations__`, builds the source text of three methods
as strings, `exec`s them, and attaches the results. You can see the field
list it built:

```text
>>> from dataclasses import fields
>>> [(f.name, f.type) for f in fields(User)]
[('username', <class 'str'>), ('email', <class 'str'>), ('interests', list[str]), ('active', <class 'bool'>)]
```

And you can see the `__init__` signature it wrote:

```text
>>> import inspect
>>> print(inspect.signature(User.__init__))
(self, username: str, email: str, interests: list[str] = <factory>, active: bool = True) -> None
```

`<factory>` is the placeholder `dataclasses` prints for a `default_factory`,
because there is no single default value to show. The generated code calls
that factory once per construction — roughly
`self.interests = _dflt_interests() if interests is _HAS_DEFAULT_FACTORY else interests`.

There is no source file to read for that method, which is why the traceback
in the bugs list above shows `File "<string>", line 5, in __init__` with no
code under it. The generated text was compiled from a string and thrown away.

Two consequences of this being generated *code* rather than runtime
behaviour. First, the field order is fixed at class-definition time, so
reordering fields is a breaking change for anyone calling positionally.
Second, the decorator arguments switch generation on and off:

| argument | default | what it generates |
|---|---|---|
| `init` | `True` | `__init__` |
| `repr` | `True` | `__repr__` |
| `eq` | `True` | `__eq__` |
| `order` | `False` | `__lt__`, `__le__`, `__gt__`, `__ge__` |
| `frozen` | `False` | `__setattr__`/`__delattr__` that raise |
| `slots` | `False` | rebuilds the class with `__slots__` |
| `kw_only` | `False` | makes every field keyword-only |

`order=True` is worth one warning. It compares the fields **as a tuple, in
declaration order**, using each field's own `<`. For `User` that means it
sorts by username first, which is probably fine. Challenge 01 has a case
where it is quietly disastrous: comparing card ranks as strings puts `"10"`
before `"2"`.

`kw_only=True` is the one that makes dataclass inheritance bearable, and
Challenge 02's stretch goals show why: without it, a defaulted field in a
parent forces every field in every child to have a default too.

</details>

<details>
<summary>Under the hood — why generating __eq__ takes __hash__ away, and what frozen=True gives back</summary>

Try to put a user in a set and Python refuses:

```text
>>> {User("a", "a@b.c")}
TypeError: unhashable type: 'User'
```

That is deliberate, and the reasoning is worth following because it is the
same reasoning behind `frozen=True`.

A **hash** is a number a container uses to decide which bucket to look in.
Sets and dicts find things fast because they hash the key, go straight to one
bucket, and only compare against what is in it. For that to work at all,
Python requires one rule:

> If `a == b`, then `hash(a)` must equal `hash(b)`.

Break the rule and the container looks in the wrong bucket, finds nothing,
and tells you an item you just added is not there. Not an exception — a wrong
answer.

The default `__hash__` inherited from `object` is based on the object's
identity, which is consistent with the default `__eq__` — also identity. Two
distinct objects are unequal and hash differently, and the rule holds.

Now you add a value-based `__eq__`. Suddenly `rlopez == twin` is `True`, but
their identity hashes differ, so the rule is broken. Python's answer is to
refuse rather than to guess: **any class that defines `__eq__` gets
`__hash__ = None` unless it says otherwise**, and `@dataclass` follows the
same rule.

Could `dataclasses` just generate a matching hash from the fields? Only if
the fields never change. They do:

```text
>>> u = User("rlopez", "r@example.org")
>>> h = hash(u)          # if this were allowed...
>>> u.add_interest("gis")
>>> hash(u) == h         # ...it would now be a different number
```

A user sitting in a set, hashed under its old value, is now filed in a bucket
that no longer matches. It is lost, and nothing raised.

`frozen=True` removes the mutation, which restores the promise:

```text
>>> from dataclasses import dataclass
>>> @dataclass(frozen=True)
... class Workshop:
...     title: str
...     date: str
...
>>> w = Workshop("OOP", "2026-03-01")
>>> hash(w) == hash(Workshop("OOP", "2026-03-01"))
True
>>> w.title = "Other"
dataclasses.FrozenInstanceError: cannot assign to field 'title'
```

Frozen is not enforced by making the object read-only at the machine level.
`dataclasses` generates a `__setattr__` that raises, and `__init__` sidesteps
it with `object.__setattr__`. That is why a frozen dataclass with a `list`
field is only *half* immutable — the field cannot be reassigned, but the list
it points at can still be appended to, and the hash would still drift. Freeze
records whose fields are themselves immutable: strings, numbers, tuples,
dates, other frozen dataclasses.

There is a third option, `unsafe_hash=True`, and the name is the warning. It
generates the hash anyway and trusts you never to change a field that feeds
it. Nothing checks.

The table, in short:

| decorator | `__eq__` | `__hash__` | usable in a set |
|---|---|---|---|
| no decorator | identity | identity | yes |
| `@dataclass` | by field | `None` | no |
| `@dataclass(frozen=True)` | by field | by field | yes |
| `@dataclass(eq=False)` | identity | identity | yes, but `==` is identity |
| `@dataclass(unsafe_hash=True)` | by field | by field | yes, and you are on your own |

</details>

## Acceptance checklist

- [ ] `python exercise-04-dataclass-user.py` runs with no traceback.
- [ ] All six output lines match exactly.
- [ ] The file contains no hand-written `__init__`, `__repr__`, or `__eq__`.
- [ ] `interests` uses `field(default_factory=list)`.
- [ ] Two users built from identical data are `==` but not `is`.
- [ ] `User("dana", "not-an-email")` raises `ValueError` at construction.
- [ ] Committed to Git with a message like
      `Add Week 7 exercise 4: User dataclass`.

## Stretch

- Add a `@classmethod` alternative constructor
  `from_row(cls, row: str) -> "User"` that parses
  `"rlopez,rlopez@example.org,python|gis"` into a `User`. Lecture 03,
  section 4 covers why `cls` beats naming `User` directly inside it.
- Make a second, frozen dataclass — `@dataclass(frozen=True)` — for a
  `Workshop` with `title` and `date` fields, and build a
  `dict[Workshop, list[User]]`. Frozen records are hashable, so they work as
  keys. Try the same thing with a non-frozen `Workshop` and read the error.
- Add `order=True` to `User` and sort a list of them. Then read the generated
  behaviour carefully: it compares the fields as a tuple, in declaration
  order, so it sorts by username first. Decide whether that is what a reader
  of your code would expect, and write one sentence saying why you kept or
  dropped it.
- Add `slots=True` and confirm the demo still passes. Then try setting an
  attribute that does not exist, such as `rlopez.emial = "x"`, and note that
  the typo now raises `AttributeError` instead of silently creating a new
  attribute.

When your record type behaves, move on to
[Exercise 5 — Bank Account](./exercise-05-bank-account.md).
