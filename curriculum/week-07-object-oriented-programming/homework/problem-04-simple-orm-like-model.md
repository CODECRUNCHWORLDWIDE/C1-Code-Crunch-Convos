# Problem 4 — Simple ORM-like model

> **Topic:** reading a class's own annotations to build `__init__`, `to_dict`, `from_dict` and `__repr__` for every subclass at once
> **Lecture:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour 15 minutes
> **Why this one:** Exercise 4 used `@dataclass` and let it write the boilerplate. This is the same trick from the other side — you write the machine. Once you have built a small one, every framework you meet afterwards (Django models, SQLAlchemy, Pydantic, `@dataclass` itself) stops looking like magic and starts looking like a thing that reads `__annotations__`.

## The Brief

An **ORM** — object-relational mapper — is the layer that turns rows in a
database into objects and back. You are not building a database. You are
building the *shape*: a base class that subclasses can extend to get
`__init__`, `to_dict`, `from_dict` and `__repr__` for free, driven by nothing
but the field names they declare.

The whole idea in one picture. A subclass should be able to say only this:

```python
class User(Model):
    id: int
    name: str
    email: str
    joined: date
    active: bool = True
```

and then work:

```python
ada = User(id=1, name="Ada Lovelace", email="ada@example.com",
           joined=date(2026, 1, 15))
User.from_dict(json.loads(json.dumps(ada.to_dict()))) == ada   # True
```

Five annotated lines, and `Model` supplies everything else — including
turning the `date` into a string on the way out and back into a `date` on the
way in.

Write two subclasses, `User` and `Post`, and demonstrate a round trip through
`json.dumps` / `json.loads` via your `to_dict` / `from_dict`. Make `Post` hold
a `User`, so the round trip has to work recursively.

The brief gives you the hint: inspect `cls.__annotations__`, a dict of field
name to type, either in `__init_subclass__` or in `__init__`.

**This one is deliberately open-ended.** There is no single right answer.
What follows is one complete design; a grader is looking for the *mechanism*
— annotations read once, everything generated from them — not for these exact
choices. There is a note at the end of the Under the hood block about what
else counts as a good answer.

## Starter

Save this as `models.py` and fill in the `TODO` markers.

```python
"""models.py — a tiny ORM-shaped base class driven by annotations.

    python models.py

NOTE: no `from __future__ import annotations` in this file, on purpose. With
that import every annotation becomes a plain string, and the decoder below
needs real type objects. `typing.get_type_hints` turns strings back into
objects, which is why it is used instead of reading `cls.__annotations__`
directly.
"""

import copy
import json
from datetime import date, datetime
from typing import Any, ClassVar, get_args, get_origin, get_type_hints

MISSING = object()          # sentinel: "this field has no default"


class Model:
    """Subclasses declare their fields as annotated class attributes."""

    _fields: ClassVar[dict[str, Any]]      # {name: resolved type} per subclass
    _defaults: ClassVar[dict[str, Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Read this subclass's annotations once, when the class is created."""
        super().__init_subclass__(**kwargs)
        # TODO: hints = get_type_hints(cls)
        # TODO: cls._fields = every hint whose name does not start with "_"
        #       and whose get_origin(...) is not ClassVar
        # TODO: cls._defaults = {name: getattr(cls, name, MISSING) ...}

    def __init__(self, **kwargs: Any) -> None:
        """Build one record, filling in defaults and refusing unknown names."""
        # TODO: raise TypeError naming any kwarg that is not a field
        # TODO: for each field, use the kwarg if given, else the default
        # TODO: raise TypeError when a field has no value and no default
        # TODO: copy.deepcopy the default, so a mutable one is not shared

    def to_dict(self) -> dict[str, Any]:
        """This record as a JSON-safe dict."""
        # TODO: _encode each field value
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Model":
        """`cls`, not `Model` — a subclass calling this gets its own type back."""
        # TODO: _decode each present field, guided by its annotation,
        # then return cls(**kwargs)
        raise NotImplementedError

    def to_json(self, **dumps_kwargs: Any) -> str:
        """This record as a JSON string."""
        return json.dumps(self.to_dict(), **dumps_kwargs)

    @classmethod
    def from_json(cls, text: str) -> "Model":
        """Rebuild a record of this class from a JSON string."""
        return cls.from_dict(json.loads(text))

    def __repr__(self) -> str:
        """Developer form listing every field in declaration order."""
        # TODO
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Same exact class and same values in every field."""
        # TODO: NotImplemented when the types differ exactly
        raise NotImplementedError


def _encode(value: Any) -> Any:
    """Python value -> JSON-safe value."""
    # TODO: a Model becomes its to_dict()
    # TODO: a datetime becomes isoformat() -- CHECK THIS BEFORE date
    # TODO: a date becomes isoformat()
    # TODO: a list or tuple becomes a list of encoded items
    # TODO: a dict becomes a dict of encoded values
    # TODO: anything else passes through
    raise NotImplementedError


def _decode(value: Any, hint: Any) -> Any:
    """JSON-safe value -> Python value, guided by the field's annotation."""
    # TODO: None stays None
    # TODO: a list[...] hint decodes each item with the inner hint
    # TODO: a Model subclass hint calls hint.from_dict(value)
    # TODO: datetime and date parse with fromisoformat
    # TODO: anything else passes through
    raise NotImplementedError


class User(Model):
    """One person, with the date they joined."""

    id: int
    name: str
    email: str
    joined: date
    active: bool = True


class Post(Model):
    """One post, written by a nested `User`."""

    id: int
    author: User                  # a nested model, round-tripped too
    title: str
    body: str
    tags: list[str] = []          # safe: __init__ deepcopies defaults
    published_on: date = None     # type: ignore[assignment]


def main() -> None:
    """Build two records, round-trip them through JSON, then break them."""
    ada = User(id=1, name="Ada Lovelace", email="ada@example.com",
               joined=date(2026, 1, 15))
    print(ada)
    print("fields:", list(User._fields))

    post = Post(
        id=10,
        author=ada,
        title="Why OOP",
        body="State and behaviour, together at last.",
        tags=["python", "oop"],
        published_on=date(2026, 3, 1),
    )
    print(post)

    text = post.to_json(indent=2)
    print(text)
    restored = Post.from_json(text)
    print("restored:", restored)
    print("equal after round trip:", restored == post)
    print("nested type survived:", type(restored.author).__name__,
          "| joined is a date:", type(restored.author.joined).__name__)

    raw = json.loads(json.dumps(ada.to_dict()))
    print("user round trip:", User.from_dict(raw) == ada)

    a = Post(id=1, author=ada, title="a", body="")
    b = Post(id=2, author=ada, title="b", body="")
    a.tags.append("mutated")
    print("a.tags:", a.tags, "| b.tags:", b.tags)

    for label, thunk in [
        ("missing", lambda: User(id=2, name="Bob")),
        ("unknown", lambda: User(id=2, name="Bob", email="b@x.com",
                                 joined=date(2026, 1, 1), nickname="Bobby")),
    ]:
        try:
            thunk()
        except TypeError as exc:
            print(f"TypeError ({label}):", exc)

    class Admin(User):
        """A user with a permission list of their own."""

        permissions: list[str] = []

    root = Admin(id=0, name="root", email="root@example.com",
                 joined=date(2026, 1, 1), permissions=["all"])
    print("admin:", root)
    print("admin fields:", list(Admin._fields))
    print("admin round trip:", Admin.from_dict(root.to_dict()) == root)


if __name__ == "__main__":
    main()
```

Four names in that starter are new. They are all from `typing`, and they are
all about reading annotations at runtime.

**`__init_subclass__`** is a method Python calls on the **parent** every time
somebody creates a subclass. Not per object — per class, once, at
class-definition time. It is where a base class gets to look at what its
children declared. (You do not write `@classmethod` on it; Python makes it
one for you.)

**`get_type_hints(cls)`** returns the annotations of `cls` **and all its
parents**, with any string annotations turned back into real objects. Plain
`cls.__annotations__` gives you neither of those things reliably, which is
the second Under the hood block.

**`get_origin` and `get_args`** take apart a compound hint. For
`list[str]`, `get_origin` is `list` and `get_args` is `(str,)`. That is how
`_decode` knows to walk into a list and what to decode each item as.

**`MISSING = object()`** is a **sentinel** — a unique object that can never
collide with real data. You need it because `None` is a legitimate default
here (`published_on: date = None` means "not published yet"). If "no default"
were also spelled `None`, the two would be indistinguishable.

## Requirements

1. `Model.__init_subclass__` reads each subclass's annotations **once**, at
   class-definition time, and stores the field list and the defaults on the
   class.
2. Names starting with `_` and anything annotated `ClassVar[...]` are not
   fields.
3. `Model.__init__` takes keyword arguments only. It raises `TypeError`
   naming any unknown field, and `TypeError` naming any required field with
   no value.
4. A mutable default is deep-copied per instance, so two records never share
   one list.
5. `to_dict` produces JSON-safe values: nested models become dicts, dates
   become ISO strings, lists and dicts are walked.
6. `from_dict` is a `@classmethod` using `cls`, so `Admin.from_dict(...)`
   returns an `Admin`.
7. `from_dict` uses each field's annotation to rebuild the right type — a
   nested `User`, a real `date`.
8. `__repr__` lists every field in declaration order. `__eq__` compares
   exact type and every field, and returns `NotImplemented` for a foreign
   type.
9. `main()` demonstrates a round trip through `json.dumps` / `json.loads`,
   as the brief asks.

## Constraints

- **No `from __future__ import annotations` in this file.** With that import
  every annotation is a string, so `hint is date` becomes `"date" is date`,
  which is `False`, and every type-driven decision silently falls through.
  Your dates would stay strings and nothing would raise.
- **Use `get_type_hints(cls)`, not `cls.__annotations__`.** Two independent
  reasons, both in the Under the hood block: `__annotations__` breaks under
  string annotations, and it only holds the names written in *that* class
  body, so inherited fields go missing.
- **`_encode` must check `datetime` before `date`.** `datetime` is a
  *subclass* of `date`, so `isinstance(some_datetime, date)` is `True`. Check
  `date` first and every timestamp silently loses its time component. This
  ordering bug is subtle, permanent, and extremely common in serialisation
  code.
- **Deep-copy defaults.** `setattr(self, name, default)` without the copy
  gives two `Post` objects one shared `tags` list. Same bug as Exercise 1's
  `tricks = []`, one layer of abstraction up, so it is harder to spot.
- **`from_dict` is a `@classmethod` and uses `cls`.** A `@staticmethod`
  returning `Model(...)` gives you a `Model`, not a `User`, and every
  subclass would need its own copy of the method.
- **Read the annotations once per class, not once per object.**
  `get_type_hints` evaluates annotations and walks the MRO. Doing that in
  `__init__` works and costs you the same reflection on every single object
  you build.
- **`__eq__` compares `type(other) is not type(self)`, not `isinstance`.**
  With `isinstance`, an `Admin` could compare equal to a `User` with the same
  five fields — and it would be asymmetric, since `User.__eq__(admin)` and
  `Admin.__eq__(user)` would disagree.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-04-simple-orm-like-model.py
User(id=1, name='Ada Lovelace', email='ada@example.com', joined=datetime.date(2026, 1, 15), active=True)
fields: ['id', 'name', 'email', 'joined', 'active']
Post(id=10, author=User(id=1, name='Ada Lovelace', email='ada@example.com', joined=datetime.date(2026, 1, 15), active=True), title='Why OOP', body='State and behaviour, together at last.', tags=['python', 'oop'], published_on=datetime.date(2026, 3, 1))
{
  "id": 10,
  "author": {
    "id": 1,
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "joined": "2026-01-15",
    "active": true
  },
  "title": "Why OOP",
  "body": "State and behaviour, together at last.",
  "tags": [
    "python",
    "oop"
  ],
  "published_on": "2026-03-01"
}
restored: Post(id=10, author=User(id=1, name='Ada Lovelace', email='ada@example.com', joined=datetime.date(2026, 1, 15), active=True), title='Why OOP', body='State and behaviour, together at last.', tags=['python', 'oop'], published_on=datetime.date(2026, 3, 1))
equal after round trip: True
nested type survived: User | joined is a date: date
user round trip: True
a.tags: ['mutated'] | b.tags: []
TypeError (missing): User: missing field 'email'
TypeError (unknown): User: unknown field(s) nickname
admin: Admin(id=0, name='root', email='root@example.com', joined=datetime.date(2026, 1, 1), active=True, permissions=['all'])
admin fields: ['id', 'name', 'email', 'joined', 'active', 'permissions']
admin round trip: True
```

Four lines prove the design, and they are the four to check first:

- **`equal after round trip: True`** — the object survived JSON intact.
- **`joined is a date: date`** — not the string `'2026-01-15'`. The decoder
  used the annotation.
- **`b.tags: []`** — defaults are not shared, even though `Post` declares
  `tags: list[str] = []`.
- **`admin fields:` lists six names** — inheritance merged the parent's five
  with the child's one, in the right order, with no work from you.

Note `true` in the JSON, lowercase. That is JSON's spelling of `True`, and
`json.loads` turns it back.

## Steps

1. Save the starter and run it. It fails immediately, in
   `__init_subclass__`, when `User` is defined — before `main` runs at all.
   That is the hook firing.
2. Fill in `__init_subclass__` and check what it found:

   ```bash
   python -c "import models; print(models.User._fields); print(models.User._defaults)"
   ```

   You want five fields, and `_defaults` holding `MISSING` for four of them.
3. Fill in `__init__` and `__repr__`. The first line should now print.
4. Fill in `_encode` and `to_dict`, and print `ada.to_dict()`. Look at
   `joined` — it must be the string `'2026-01-15'`, not a `date` object, or
   `json.dumps` will raise
   `TypeError: Object of type date is not JSON serializable`.
5. Fill in `_decode` and `from_dict`. Check `joined` comes back as a `date`.
6. Add `__eq__` and confirm `equal after round trip: True`.
7. Test the nesting: `Post.from_json(post.to_json())`. The author must come
   back as a `User`, not a dict.
8. Test the deep copy: two `Post` objects, append to one's `tags`, confirm
   the other is still empty. Then delete the `copy.deepcopy` and watch them
   share.
9. Define `Admin(User)` and confirm it inherits all five fields plus its own.
   This is the step that proves `get_type_hints` was the right call.

## The Solution

```python
"""problem-04-simple-orm-like-model-solution.py — a tiny ORM-shaped base class.

The `-solution` in the name keeps this file from colliding with the `models.py`
you write yourself. Run it with::

    python problem-04-simple-orm-like-model-solution.py

No database. The point is the *shape*: declare fields once as annotations, get
`__init__`, `to_dict`, `from_dict`, `__repr__` and `__eq__` for free.

NOTE: this file deliberately does NOT use `from __future__ import annotations`.
With that import every annotation becomes a plain string, so `hint is date`
would be `hint == "date"` and the decoder could not do its job. `typing.
get_type_hints` resolves strings back into objects, which is why it is used
below instead of reading `cls.__annotations__` directly.
"""

import copy
import json
from datetime import date, datetime
from typing import Any, ClassVar, get_args, get_origin, get_type_hints

MISSING = object()          # sentinel: "this field has no default"


class Model:
    """Subclasses declare their fields as annotated class attributes.

    An annotation with a value is an optional field with that default; an
    annotation without a value is required. The base class reads the
    annotations once, when the subclass is created, and builds everything else
    from that list.
    """

    _fields: ClassVar[dict[str, Any]]      # {name: resolved type} per subclass
    _defaults: ClassVar[dict[str, Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Read this subclass's annotations once, when the class is created."""
        super().__init_subclass__(**kwargs)
        # get_type_hints walks the MRO, so a subclass of a subclass inherits
        # its parent's fields automatically.
        hints = get_type_hints(cls)
        cls._fields = {
            name: hint
            for name, hint in hints.items()
            if not name.startswith("_") and get_origin(hint) is not ClassVar
        }
        cls._defaults = {
            name: getattr(cls, name, MISSING) for name in cls._fields
        }

    def __init__(self, **kwargs: Any) -> None:
        """Build one record, filling in defaults and refusing unknown names."""
        unknown = set(kwargs) - set(self._fields)
        if unknown:
            raise TypeError(
                f"{type(self).__name__}: unknown field(s) "
                f"{', '.join(sorted(unknown))}"
            )
        for name in self._fields:
            if name in kwargs:
                setattr(self, name, kwargs[name])
                continue
            default = self._defaults[name]
            if default is MISSING:
                raise TypeError(f"{type(self).__name__}: missing field {name!r}")
            # deepcopy so a mutable class-level default (`tags: list[str] = []`)
            # cannot be shared between instances — the lecture-01 footgun,
            # solved once, here, for every subclass.
            setattr(self, name, copy.deepcopy(default))

    # --- serialization ----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """This record as a JSON-safe dict."""
        return {name: _encode(getattr(self, name)) for name in self._fields}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Model":
        """`cls`, not `Model` — a subclass calling this gets its own type back."""
        kwargs = {
            name: _decode(data[name], hint)
            for name, hint in cls._fields.items()
            if name in data
        }
        return cls(**kwargs)

    def to_json(self, **dumps_kwargs: Any) -> str:
        """This record as a JSON string."""
        return json.dumps(self.to_dict(), **dumps_kwargs)

    @classmethod
    def from_json(cls, text: str) -> "Model":
        """Rebuild a record of this class from a JSON string."""
        return cls.from_dict(json.loads(text))

    # --- niceties ---------------------------------------------------------

    def __repr__(self) -> str:
        """Developer form listing every field in declaration order."""
        inner = ", ".join(f"{n}={getattr(self, n)!r}" for n in self._fields)
        return f"{type(self).__name__}({inner})"

    def __eq__(self, other: object) -> bool:
        """Same exact class and same values in every field."""
        if type(other) is not type(self):
            return NotImplemented
        return all(
            getattr(self, n) == getattr(other, n) for n in self._fields
        )


def _encode(value: Any) -> Any:
    """Python value -> JSON-safe value."""
    if isinstance(value, Model):
        return value.to_dict()
    if isinstance(value, datetime):        # check before date: datetime IS a date
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def _decode(value: Any, hint: Any) -> Any:
    """JSON-safe value -> Python value, guided by the field's annotation."""
    if value is None:
        return None
    origin = get_origin(hint)
    if origin in (list, tuple):
        args = get_args(hint)
        inner = args[0] if args else Any
        return [_decode(item, inner) for item in value]
    if isinstance(hint, type):
        if issubclass(hint, Model):
            return hint.from_dict(value)
        if hint is datetime:
            return datetime.fromisoformat(value)
        if hint is date:
            return date.fromisoformat(value)
    return value


# --- two models -----------------------------------------------------------


class User(Model):
    """One person, with the date they joined."""

    id: int
    name: str
    email: str
    joined: date
    active: bool = True


class Post(Model):
    """One post, written by a nested `User`."""

    id: int
    author: User                  # a nested model, round-tripped too
    title: str
    body: str
    tags: list[str] = []          # safe: __init__ deepcopies defaults
    published_on: date = None     # type: ignore[assignment]


def main() -> None:
    """Build two records, round-trip them through JSON, then break them."""
    ada = User(id=1, name="Ada Lovelace", email="ada@example.com",
               joined=date(2026, 1, 15))
    print(ada)
    print("fields:", list(User._fields))

    post = Post(
        id=10,
        author=ada,
        title="Why OOP",
        body="State and behaviour, together at last.",
        tags=["python", "oop"],
        published_on=date(2026, 3, 1),
    )
    print(post)

    # --- round trip ------------------------------------------------------
    text = post.to_json(indent=2)
    print(text)
    restored = Post.from_json(text)
    print("restored:", restored)
    print("equal after round trip:", restored == post)
    print("nested type survived:", type(restored.author).__name__,
          "| joined is a date:", type(restored.author.joined).__name__)

    # The long way, exactly as the brief words it.
    raw = json.loads(json.dumps(ada.to_dict()))
    print("user round trip:", User.from_dict(raw) == ada)

    # --- defaults are not shared ----------------------------------------
    a = Post(id=1, author=ada, title="a", body="")
    b = Post(id=2, author=ada, title="b", body="")
    a.tags.append("mutated")
    print("a.tags:", a.tags, "| b.tags:", b.tags)

    # --- errors ----------------------------------------------------------
    for label, thunk in [
        ("missing", lambda: User(id=2, name="Bob")),
        ("unknown", lambda: User(id=2, name="Bob", email="b@x.com",
                                 joined=date(2026, 1, 1), nickname="Bobby")),
    ]:
        try:
            thunk()
        except TypeError as exc:
            print(f"TypeError ({label}):", exc)

    # --- inheritance between models -------------------------------------
    class Admin(User):
        """A user with a permission list of their own."""

        permissions: list[str] = []

    root = Admin(id=0, name="root", email="root@example.com",
                 joined=date(2026, 1, 1), permissions=["all"])
    print("admin:", root)
    print("admin fields:", list(Admin._fields))
    print("admin round trip:", Admin.from_dict(root.to_dict()) == root)


if __name__ == "__main__":
    main()
```

**`__init_subclass__` is the hook that makes this feel like a framework.** It
is called on the *parent* every time a subclass is created — at
class-definition time, once, not per instance. So the field list is computed
exactly once for `User`, once for `Post`, and never again. The alternative the
brief offers, inspecting annotations inside `__init__`, works but re-does the
same reflection on every single object you create.

**`typing.get_type_hints(cls)` instead of `cls.__annotations__`, for two
independent reasons**, both spelled out in the second Under the hood block:
string annotations, and inheritance.

**`_fields` and `_defaults` are `ClassVar`, and the filter skips them.** The
comprehension drops any name starting with `_` and any hint whose origin is
`ClassVar`, so the bookkeeping attributes never become fields of themselves.
Without that filter, `Model`'s own `_fields` annotation would try to become a
field on every subclass.

**`copy.deepcopy(default)` fixes the mutable-default problem for every
subclass at once.** `tags: list[str] = []` is exactly the footgun from
Exercise 1 — one list object living on the class, shared by every instance.
Rather than forbidding it, the way `dataclasses` does, this base class *makes
it safe*: each instance gets its own deep copy of whatever the default is.
The demo proves it: appending to `a.tags` leaves `b.tags` empty.

**`from_dict` is a `@classmethod` using `cls`, and that is what makes nesting
work.** `Post.from_dict` calls `_decode` on the `author` value, which sees the
annotation `User`, notices `issubclass(User, Model)`, and calls
`User.from_dict(...)` — recursively. Because each `from_dict` builds
`cls(...)`, `Admin.from_dict` returns an `Admin`, not a `User`.

**`_encode` checks `datetime` before `date`, and the order is load-bearing.**
`datetime` is a subclass of `date`, so `isinstance(some_datetime, date)` is
`True`. Check `date` first and every timestamp silently loses its time.

**`__eq__` uses `type(other) is not type(self)`.** Exact-type comparison keeps
`==` symmetric. Returning `NotImplemented` for a foreign type is the same
rule as everywhere else.

**The `MISSING` sentinel exists because `None` is a legitimate default.**
`Post.published_on = None` means "no publication date", which is real data.
A unique `object()` can never collide with a user value.

## Run it

Copy the worked answer on this page into `problem-04-simple-orm-like-model.py` and run it:

```bash
python problem-04-simple-orm-like-model.py
```

It imports only `copy`, `json`, `datetime` and `typing`, all from the
standard library, and touches no files. Save your own version as `models.py`.

## Common bugs to catch

- **`TypeError: Object of type date is not JSON serializable`.** Your
  `to_dict` handed the `date` object straight through. `json` knows about
  strings, numbers, booleans, `None`, lists and dicts, and nothing else.
  `_encode` is what turns everything else into one of those six.

- **`joined` comes back as the string `'2026-01-15'`.** The round trip
  "worked" and the object is now wrong. Your `_decode` never looked at the
  hint, or the hint was a string rather than a type — see the next bug.

- **Every type-driven branch silently does nothing.** You added
  `from __future__ import annotations` at the top. Now every annotation is a
  string:

  ```text
  >>> User.__annotations__
  {'id': 'int', 'name': 'str', 'email': 'str', 'joined': 'date', 'active': 'bool'}
  >>> User.__annotations__["joined"] is date
  False
  ```

  `hint is date` is `False`, `issubclass(hint, Model)` raises
  `TypeError: issubclass() arg 1 must be a class`, and your dates stay
  strings. `get_type_hints` evaluates those strings against the defining
  module's namespace and hands back real objects.

- **`Admin` has only one field.** You read `cls.__annotations__` instead of
  `get_type_hints(cls)`. A class body's `__annotations__` holds only what
  that body declared:

  ```text
  >>> Admin.__annotations__
  {'permissions': list[str]}
  ```

  `get_type_hints` walks the MRO and merges, which is why the shipped version
  gets six.

- **Two `Post` objects share one `tags` list.** You did
  `setattr(self, name, default)` without the deep copy. Appending to one
  changes the other, and nothing raises.

- **Every timestamp comes back at midnight.** You checked `date` before
  `datetime` in `_encode`. Silent truncation, no error, and nobody notices
  until somebody asks why the times are all zero.

- **`User.from_dict(...)` returns a `Model`.** You wrote `from_dict` as a
  `@staticmethod` returning `Model(...)`. `@classmethod` with `cls` is the
  whole reason Lecture 03 introduces it.

- **`RecursionError` on `to_dict`.** You gave a model a field pointing back at
  something that points at it — a `User` with a `posts` list whose posts each
  hold that user. `_encode` follows the cycle forever. Real ORMs solve this
  with lazy loading or an explicit depth limit; the smallest fix here is to
  serialise the reference as an id rather than as the whole object.

## Under the hood

<details>
<summary>Under the hood — the four hooks that fire when a class is created</summary>

Classes are objects, and building one is a process you can step into at four
points. This problem uses the second. Knowing all four is what makes
frameworks legible.

**1. The class body runs.** It is ordinary code executing in a fresh
namespace, top to bottom. Assignments become entries in that namespace;
annotations become entries in `__annotations__`. This is why
`species = "Canis familiaris"` in Exercise 1 runs exactly once.

**2. `__init_subclass__` on the parent.** After the body has run and the
class object exists, Python calls this on the nearest ancestor that defines
it, passing the brand-new class as `cls`. It is the cheapest way for a base
class to inspect or register its children, and it is implicitly a
classmethod.

```text
>>> class Base:
...     def __init_subclass__(cls, **kwargs):
...         super().__init_subclass__(**kwargs)
...         print("registering", cls.__name__)
...
>>> class Child(Base): pass
registering Child
```

Notice it printed at `class Child(Base): pass`, not at any construction.

**3. `__set_name__` on each descriptor in the body.** If a value in the class
body defines `__set_name__`, Python calls it with the owning class and the
name it was bound to. That is how a field object learns what it is called —
the mechanism behind `Column("id")` in SQLAlchemy not needing you to repeat
the name.

**4. The metaclass.** `type(SomeClass)` is what actually builds it, and a
custom metaclass can rewrite the class before anybody sees it. `ABCMeta` from
homework problem 2 is one. This is the heaviest hammer and almost never the
right one — the Python docs' own guidance is that `__init_subclass__` and
`__set_name__` cover most of what metaclasses used to be needed for.

`@dataclass` is a fifth option that is not a hook at all: an ordinary
decorator, running after everything above, that reads the finished class and
attaches methods. That is a useful mental model for this whole problem —
there is no magic anywhere, only code reading `__annotations__` at four
different moments.

Which to reach for:

- **A decorator** when the behaviour is opt-in per class. `@dataclass`.
- **`__init_subclass__`** when every subclass should get it automatically,
  and you only need to *read* the class. This problem.
- **`__set_name__`** when individual attributes need to know their own name.
- **A metaclass** when you need to change how the class itself is
  constructed. Rarely.

</details>

<details>
<summary>Under the hood — why get_type_hints and not __annotations__</summary>

Two independent failures, and each one is enough on its own.

**The first is string annotations.** Python lets you write a type that does
not exist yet, as a quoted forward reference — and `from __future__ import
annotations` makes *every* annotation a string automatically:

```text
>>> from __future__ import annotations
>>> from datetime import date
>>> class User:
...     id: int
...     joined: date
...
>>> User.__annotations__
{'id': 'int', 'joined': 'date'}
>>> User.__annotations__["joined"] is date
False
```

Every type-driven decision in `_decode` would fall through silently and your
dates would stay strings. `get_type_hints` evaluates those strings against
the defining module's globals and hands back the real objects:

```text
>>> from typing import get_type_hints
>>> get_type_hints(User)["joined"] is date
True
```

That is also why the shipped file says, in a comment at the top, that it
deliberately does *not* use the `__future__` import. A single line added by a
well-meaning teammate would break the decoder with no error message.

**The second is inheritance.** `cls.__annotations__` is only the annotations
written in *that* class body:

```text
>>> Admin.__annotations__
{'permissions': list[str]}
>>> list(get_type_hints(Admin))
['_fields', '_defaults', 'id', 'name', 'email', 'joined', 'active', 'permissions']
```

`get_type_hints` walks the MRO and merges, parents first, which is exactly
the order you want the fields in.

Look at what came back first, though: `_fields` and `_defaults`, which are
`Model`'s own bookkeeping annotations. Merging the whole MRO means merging
*everything*, including the base class's private ones. That is precisely why
the comprehension in `__init_subclass__` filters out names starting with `_`
and anything whose origin is `ClassVar` — without it, `Model` would try to
make fields out of its own machinery on every subclass you ever wrote.

There is a historical trap worth knowing about, because it broke a generation
of hand-rolled ORMs. **Before Python 3.10, a class with no annotations of its
own did not get an empty `__annotations__` — it got its parent's**, because
attribute lookup fell through to the base class. So a subclass that declared
nothing appeared to declare all of its parent's fields, and one that declared
one field appeared to declare only that one. Both wrong, in opposite
directions, silently. Python 3.10 gave every class its own dict, and 3.14
went further with `annotationlib` and lazy evaluation. `get_type_hints` has
been the correct answer throughout.

One caveat, since you should know the cost: `get_type_hints` *evaluates* the
annotations, which means it can raise `NameError` on a forward reference to
something that genuinely does not exist yet, and it is not free. Calling it
once per class in `__init_subclass__` — rather than once per object in
`__init__` — is what keeps that cost invisible.

</details>

<details>
<summary>Under the hood — what a grader is looking for in an open-ended problem</summary>

The brief says this problem is intentionally open-ended, so a wide range of
designs is acceptable. What should be present in any of them:

- **Fields come from annotations, read once.** Whether via
  `__init_subclass__`, a metaclass, or a decorator does not matter.
  Hard-coding a `FIELDS = [...]` list in each subclass misses the point of
  the problem.
- **`to_dict` and `from_dict` are mirror images**, and the round trip is
  actually demonstrated through `json.dumps` / `json.loads` — the brief asks
  for that specific demonstration.
- **`from_dict` is a `@classmethod`.** A `@staticmethod` cannot produce the
  right subclass.
- **Non-JSON types are handled somewhere.** A `date` field is the obvious
  case. A solution that only supports `str` and `int` is simpler and still
  passes, but should say so rather than crash on
  `TypeError: Object of type date is not JSON serializable`.
- **Missing and unknown fields fail loudly**, with a message naming the
  field.

Also perfectly acceptable, and arguably better engineering: **"this is what
`@dataclass` already does, so here is the version that uses it"**, with a
written comparison. Saying "the standard library solved this" and showing you
know how is a fine answer to an open-ended problem — as long as you also show
you understand the mechanism underneath, which is what the
annotation-reading version demonstrates.

And it is worth naming what a real ORM adds on top of this shape, so you know
what you have and have not built: lazy loading, so a nested object is not
fetched until you touch it; identity mapping, so two queries for row 7 give
you the same object; change tracking, so `save()` knows which columns moved;
migrations; and a query language. Every one of those is a large problem. The
part you built — declare once, generate the rest — is the part they all
start from.

</details>

## Acceptance checklist

- [ ] `python models.py` runs with no traceback.
- [ ] The JSON round trip is demonstrated through `json.dumps` and
      `json.loads`, and the restored object is `==` to the original.
- [ ] `joined` comes back as a `date`, not a string.
- [ ] A nested `User` inside a `Post` survives the round trip as a `User`.
- [ ] Two records with the same mutable default do not share it.
- [ ] `Admin(User)` inherits all of `User`'s fields plus its own, in order.
- [ ] `Admin.from_dict(...)` returns an `Admin`.
- [ ] A missing field and an unknown field each raise `TypeError` naming the
      field.
- [ ] No `from __future__ import annotations` in the file.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 4: annotation-driven model`.

## Stretch

- Add per-field validation. Give `Model` an optional
  `_validators: ClassVar[dict[str, Callable]]` and run them in `__init__`.
  Then decide whether that belongs on the base class or on a `Field` object
  in the class body, and say why. (If you pick the second, you have just
  discovered `__set_name__`.)
- Add type checking at construction: raise `TypeError` when a value does not
  match its annotation. Discover how quickly that gets hard —
  `list[str]` cannot be handed to `isinstance` — and write down where you
  drew the line.
- Write the same two models with `@dataclass` and a pair of module-level
  `to_dict` / `from_dict` functions. Compare the two files on length,
  readability and what happens when you add a seventh field. Say which one
  you would ship.
- Add `Model.from_rows(cls, rows: list[dict]) -> list[Model]` and use it to
  load a small JSON file of users. Then time it against building them one at
  a time, and confirm that reading annotations once per class rather than
  once per object was worth the `__init_subclass__`.

Next: [Problem 5 — Observer pattern (light)](./problem-05-observer-pattern-light.md).
