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
