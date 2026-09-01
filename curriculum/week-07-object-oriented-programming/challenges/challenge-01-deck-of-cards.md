# Challenge 01 — A Deck of Cards

> **Topic:** dunder methods, iteration, sorting, and making your class behave like a built-in
> **Lecture:** [03 — Dataclasses, Dunder Methods, and Friends](../lecture-notes/03-dataclasses-and-magic-methods.md)
> **Difficulty:** Medium
> **Target time:** 90–120 minutes
> **Why this one:** it is the smallest problem where your own class earns the right to be used like a list. `len(deck)`, `for card in deck`, `sorted(hand)`, `card in a_set` — none of those are features you add. They are questions Python asks your object, and this is where you learn which method answers which question.

## The Brief

A standard deck has four **suits** — Clubs, Diamonds, Hearts, Spades — and
thirteen **ranks**: `2` through `10`, then `J`, `Q`, `K`, `A`. Each card is
one rank and one suit. Fifty-two cards, no repeats.

You are modelling both pieces: a `Card` and a `Deck`.

The interesting part is not the data. It is that Python already knows how to
ask a collection questions, and it asks them through **dunder methods** —
names with two underscores on each side, which you never call directly.
`len(deck)` calls `deck.__len__()`. `for card in deck` calls
`deck.__iter__()`. `sorted(hand)` calls `__lt__` on pairs of cards.
`{card1, card2}` calls `__hash__` and `__eq__`.

Write those methods and your class stops being a thing with a `size()` method
that everybody has to learn about, and starts being a thing that works the
way every other Python collection works.

Two traps are built into this on purpose.

**Sorting.** Ranks are strings, and strings sort alphabetically. `"10"` comes
before `"2"`, because `"1"` comes before `"2"` character by character. A deck
where a ten is the lowest card and an ace beats a king by alphabetical
accident will not raise a single error. You have to sort by *position in the
rank list*, not by the text.

**Hashing.** A card should be usable in a set — that is how you prove a deck
has no duplicates. But Python takes `__hash__` away from any class that
defines `__eq__`, for a reason Exercise 4's Under the hood block explains.
The fix here is one word: `frozen=True`.

## Starter

Create `deck.py` and fill in the `TODO` markers. The class shapes and the
demo are given; the methods are yours.

```python
"""deck.py — a 52-card deck built out of dunder methods.

    python deck.py
"""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from functools import total_ordering
from typing import ClassVar


class EmptyDeckError(IndexError):
    """Raised when you draw from an exhausted deck."""


@total_ordering
@dataclass(frozen=True)
class Card:
    """One playing card. Frozen, so it is immutable and hashable."""

    # ClassVar keeps these OFF the generated __init__ — they are constants
    # shared by every card, not per-card fields.
    RANKS: ClassVar[tuple[str, ...]] = (
        "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    )
    SUITS: ClassVar[tuple[str, ...]] = ("Clubs", "Diamonds", "Hearts", "Spades")

    rank: str
    suit: str

    def __post_init__(self) -> None:
        """Refuse a card that is not in the deck."""
        # TODO: raise ValueError when rank is not in RANKS, and again when
        # suit is not in SUITS. Message shape:
        #   invalid rank '1'; expected one of 2, 3, 4, ...

    @property
    def sort_key(self) -> tuple[int, int]:
        """Rank first, suit as the tie-breaker — both as positions, not text."""
        # TODO: return (RANKS.index(self.rank), SUITS.index(self.suit))
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        """Compare by rank, then by suit. NotImplemented for anything else."""
        # TODO: return NotImplemented when other is not a Card,
        # otherwise compare the two sort_keys
        raise NotImplementedError

    def __str__(self) -> str:
        """Player form, e.g. `A of Spades`."""
        # TODO
        raise NotImplementedError


class Deck:
    """A pile of cards you draw from the top."""

    def __init__(self, shuffled: bool = False) -> None:
        """Build a fresh 52-card deck, shuffled only if you ask."""
        self._cards: list[Card] = self._fresh_cards()
        if shuffled:
            self.shuffle()

    @staticmethod
    def _fresh_cards() -> list[Card]:
        """A brand-new 52-card deck, suit-major, low to high within each suit."""
        # TODO: one list comprehension, suits outer, ranks inner
        raise NotImplementedError

    def shuffle(self) -> None:
        """Shuffle the remaining cards in place."""
        # TODO: random.shuffle works in place and returns None

    def draw(self) -> Card:
        """Remove and return the top card."""
        # TODO: raise EmptyDeckError when there is nothing left

    def reset(self) -> None:
        """Refill back to a fresh, unshuffled 52 cards."""
        # TODO

    def __len__(self) -> int:
        """How many cards are left."""
        # TODO
        raise NotImplementedError

    def __iter__(self) -> Iterator[Card]:
        """Walk the remaining cards, top first."""
        # TODO: a reversed COPY, so drawing mid-loop cannot corrupt it
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, e.g. `Deck(remaining=42)`."""
        # TODO
        raise NotImplementedError


def main() -> None:
    """Deal from a seeded deck, then show what the two classes refuse."""
    random.seed(0)  # reproducible shuffle

    deck = Deck(shuffled=True)
    print(len(deck))
    print(repr(deck))

    card = deck.draw()
    print(card)
    print(repr(card))
    print(len(deck))

    print("next five:")
    for c in list(deck)[:5]:
        print(" ", c)

    a = Card("A", "Spades")
    b = Card("A", "Spades")
    assert a == b
    assert hash(a) == hash(b)
    assert len({a, b}) == 1

    hand = [Card("2", "Clubs"), Card("K", "Diamonds"), Card("5", "Hearts")]
    print(sorted(hand))
    print(max(hand), ">", min(hand))

    try:
        Card("1", "Spades")
    except ValueError as exc:
        print("ValueError:", exc)
    try:
        Card("A", "Swords")
    except ValueError as exc:
        print("ValueError:", exc)

    empty = Deck()
    for _ in range(52):
        empty.draw()
    print(repr(empty))
    try:
        empty.draw()
    except IndexError as exc:
        print(f"{type(exc).__name__}: {exc}")

    empty.reset()
    print("after reset:", repr(empty), "top:", empty.draw())


if __name__ == "__main__":
    main()
```

Two things in that starter are new since Exercise 4.

**`ClassVar[...]`** tells `@dataclass` "this annotated name is a shared
constant, not a per-card field". Without it, `RANKS` would become a field
with a default, and a defaulted field cannot sit above `rank` and `suit`,
which have none. It is the class-attribute-versus-instance-attribute
distinction from Exercise 1, said in dataclass syntax.

**`@total_ordering`** is a decorator that fills in `__le__`, `__gt__` and
`__ge__` from a `__lt__` and an `__eq__` you already have. Write one
comparison, get four.

## Requirements

### `Card`

1. Fields `rank: str` and `suit: str`, in that order.
2. Class constants `RANKS` (thirteen strings, low to high) and `SUITS` (four
   strings, in the order Clubs, Diamonds, Hearts, Spades). Neither may become
   a constructor argument.
3. `__post_init__` raises `ValueError` for an unknown rank or an unknown
   suit, naming the bad value and listing the valid ones.
4. `__repr__` gives `Card(rank='A', suit='Spades')`. You do not write this —
   `@dataclass` generates exactly that shape.
5. `__str__` gives `A of Spades`.
6. `__eq__` is true when rank and suit both match. You do not write this
   either.
7. `__lt__` compares by rank order, ties broken by suit order, and returns
   `NotImplemented` when handed something that is not a `Card`.
8. `__hash__` exists, so cards can live in sets. `frozen=True` gives it to
   you.

### `Deck`

1. `__init__(self, shuffled: bool = False)` builds a fresh 52-card deck and
   shuffles it only if asked.
2. `shuffle(self) -> None` shuffles the remaining cards in place.
3. `draw(self) -> Card` removes and returns the top card, and raises
   `EmptyDeckError` when there is nothing left.
4. `reset(self) -> None` refills to a fresh, unshuffled 52.
5. `__len__` returns how many cards remain.
6. `__iter__` walks the remaining cards, top card first.
7. `__repr__` gives `Deck(remaining=42)`.

## Constraints

- **Sort by position, never by the rank string.** `RANKS.index(self.rank)`
  turns `"10"` into `8` and `"A"` into `12`, and comparing those integers is
  the order you actually want. Deriving the order from the one place it is
  written down means the deck and the sort can never disagree.
- **Compare tuples, not two separate `if` statements.** Python compares
  tuples left to right and only looks at the second element when the first
  ties. `(rank_pos, suit_pos) < (rank_pos, suit_pos)` *is* "rank first, suit
  as tie-breaker", with no branching.
- **`__lt__` returns `NotImplemented` for a non-`Card`, not `False`.**
  Returning `False` would claim that a card is not less than the string
  `"hello"`, which is a statement you have no standing to make.
  `NotImplemented` says "I do not know", and Python then asks the other
  operand and, if that also declines, raises a proper `TypeError`.
- **Pick one end of the list as the top and stay consistent.** This answer
  uses the **end**, so `draw()` is a plain `list.pop()`. Popping from the
  front works too, and costs a shift of every remaining card. At 52 cards
  nobody will notice; the habit is the thing you are building.
- **`__iter__` must yield a snapshot, not a live view.** Return
  `iter(self._cards[::-1])` — the slice makes a copy. A `for` loop that draws
  a card mid-iteration then cannot go strange underneath itself.
- **Validate in `__post_init__`.** A frozen dataclass has no `__init__` of
  yours to put a check in. `__post_init__` runs as the last statement of the
  generated one, which is exactly the boundary: after that line, every `Card`
  in the program is valid.
- **`random.shuffle` returns `None`.** It shuffles in place. Writing
  `self._cards = random.shuffle(self._cards)` leaves you holding `None`, and
  the failure shows up much later in `__len__`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-deck-of-cards-solution.py
52
Deck(remaining=52)
K of Diamonds
Card(rank='K', suit='Diamonds')
51
next five:
  J of Spades
  2 of Hearts
  4 of Clubs
  5 of Diamonds
  8 of Hearts
[Card(rank='2', suit='Clubs'), Card(rank='5', suit='Hearts'), Card(rank='K', suit='Diamonds')]
K of Diamonds > 2 of Clubs
ValueError: invalid rank '1'; expected one of 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A
ValueError: invalid suit 'Swords'; expected one of Clubs, Diamonds, Hearts, Spades
Deck(remaining=0)
EmptyDeckError: cannot draw from an empty deck
after reset: Deck(remaining=52) top: A of Spades
```

**Which card comes out depends on three things**, so read this before you
worry that yours differs: the seed (`0`), the order the deck is built in
(suit-major, Clubs through Spades, `2` through `A` within each), and which
end you call the top. Change any one of them and `K of Diamonds` becomes a
different card. That is not a bug.

What you *can* compare against, whatever build order you chose, is the
structure: `52`, then `51` after one draw, five peeked cards that are not the
one you drew, a sorted hand in rank order, two `ValueError`s that name the
bad value, an empty-deck error at the end, and `52` again after `reset()`.

The sorted line is the one to check hardest. `2 of Clubs`, then `5 of
Hearts`, then `K of Diamonds`. If a `10` sorts before a `2`, you compared
strings.

## Steps

1. Write `Card` first and stop when `Card("A", "Spades")` reprs correctly.
   You should have written no `__init__` and no `__repr__`.
2. Add `__post_init__` and check both refusals in the REPL.
3. Add `sort_key` and print it for `Card("10", "Clubs")` and
   `Card("2", "Clubs")`. You want `(8, 0)` and `(0, 0)` — the ten is higher.
   If you skip this step you will debug the sort instead.
4. Add `__lt__`, then `sorted(hand)`, `max(hand)` and `min(hand)`. The last
   two work with no extra code because `@total_ordering` filled them in.
5. Check hashing: `len({Card("A", "Spades"), Card("A", "Spades")})` is `1`.
   If it raises `TypeError: unhashable type`, you dropped `frozen=True`.
6. Now `Deck`. Build `_fresh_cards` and assert `len(set(deck)) == 52` — the
   set proves there are no duplicates, and it only works because step 5
   passed.
7. Add `draw`, `__len__`, `__iter__`, `__repr__`, then `reset`. Drain a deck
   in a loop and confirm the 53rd draw raises.
8. Prove the shuffle is reproducible: seed, build, list; seed again, build
   again, list again; the two lists must be equal. Then confirm the shuffled
   list differs from an unshuffled one, or your `shuffle` might be doing
   nothing.

## The Solution

```python
"""challenge-01-deck-of-cards-solution.py — a 52-card deck built out of dunder methods.

The `-solution` in the name keeps this file from colliding with the `deck.py`
you write yourself. Run it with::

    python challenge-01-deck-of-cards-solution.py
"""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from functools import total_ordering
from typing import ClassVar


class EmptyDeckError(IndexError):
    """Raised when you draw from an exhausted deck.

    Subclassing IndexError means `except IndexError` still catches it, so the
    spec's "IndexError (or a custom EmptyDeckError)" is satisfied both ways.
    """


@total_ordering
@dataclass(frozen=True)
class Card:
    """One playing card. Frozen, so it is immutable and hashable."""

    # ClassVar keeps these OFF the generated __init__ — they are constants
    # shared by every card, not per-card fields.
    RANKS: ClassVar[tuple[str, ...]] = (
        "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    )
    SUITS: ClassVar[tuple[str, ...]] = ("Clubs", "Diamonds", "Hearts", "Spades")

    rank: str
    suit: str

    def __post_init__(self) -> None:
        """Refuse a card that is not in the deck."""
        if self.rank not in self.RANKS:
            raise ValueError(
                f"invalid rank {self.rank!r}; expected one of {', '.join(self.RANKS)}"
            )
        if self.suit not in self.SUITS:
            raise ValueError(
                f"invalid suit {self.suit!r}; expected one of {', '.join(self.SUITS)}"
            )

    # --- ordering ---------------------------------------------------------

    @property
    def sort_key(self) -> tuple[int, int]:
        """Rank first, suit as the tie-breaker — both as positions, not text."""
        return (self.RANKS.index(self.rank), self.SUITS.index(self.suit))

    def __lt__(self, other: object) -> bool:
        """Compare by rank, then by suit. NotImplemented for anything else."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.sort_key < other.sort_key

    # __eq__ and __hash__ come from @dataclass(frozen=True).
    # @total_ordering fills in __le__, __gt__ and __ge__ from __lt__ + __eq__.

    # --- display ----------------------------------------------------------

    def __str__(self) -> str:
        """Player form, e.g. `A of Spades`."""
        return f"{self.rank} of {self.suit}"


class Deck:
    """A pile of cards you draw from the top.

    The top of the deck is the **end** of the internal list, so `draw()` is a
    plain `list.pop()` — O(1), no shifting. Iteration yields draw order (top
    card first), which is the order a player cares about.
    """

    def __init__(self, shuffled: bool = False) -> None:
        """Build a fresh 52-card deck, shuffled only if you ask."""
        self._cards: list[Card] = self._fresh_cards()
        if shuffled:
            self.shuffle()

    @staticmethod
    def _fresh_cards() -> list[Card]:
        """A brand-new 52-card deck, suit-major, low to high within each suit."""
        return [
            Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS
        ]

    # --- operations -------------------------------------------------------

    def shuffle(self) -> None:
        """Shuffle the remaining cards in place."""
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """Remove and return the top card."""
        if not self._cards:
            raise EmptyDeckError("cannot draw from an empty deck")
        return self._cards.pop()

    def reset(self) -> None:
        """Refill back to a fresh, unshuffled 52 cards."""
        self._cards = self._fresh_cards()

    # --- protocols --------------------------------------------------------

    def __len__(self) -> int:
        """How many cards are left."""
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
        """Walk the remaining cards, top first."""
        # Reversed COPY: top card first, and a snapshot so drawing mid-loop
        # cannot corrupt the iteration.
        return iter(self._cards[::-1])

    def __repr__(self) -> str:
        """Developer form, e.g. `Deck(remaining=42)`."""
        return f"Deck(remaining={len(self._cards)})"


def main() -> None:
    """Deal from a seeded deck, then show what the two classes refuse."""
    random.seed(0)  # reproducible shuffle

    deck = Deck(shuffled=True)
    print(len(deck))            # 52
    print(repr(deck))           # Deck(remaining=52)

    card = deck.draw()
    print(card)
    print(repr(card))
    print(len(deck))            # 51

    print("next five:")
    for c in list(deck)[:5]:
        print(" ", c)

    a = Card("A", "Spades")
    b = Card("A", "Spades")
    assert a == b
    assert hash(a) == hash(b)
    assert len({a, b}) == 1

    hand = [Card("2", "Clubs"), Card("K", "Diamonds"), Card("5", "Hearts")]
    print(sorted(hand))
    print(max(hand), ">", min(hand))

    try:
        Card("1", "Spades")
    except ValueError as exc:
        print("ValueError:", exc)
    try:
        Card("A", "Swords")
    except ValueError as exc:
        print("ValueError:", exc)

    empty = Deck()
    for _ in range(52):
        empty.draw()
    print(repr(empty))
    try:
        empty.draw()
    except IndexError as exc:      # EmptyDeckError IS an IndexError
        print(f"{type(exc).__name__}: {exc}")

    empty.reset()
    print("after reset:", repr(empty), "top:", empty.draw())


if __name__ == "__main__":
    main()
```

**`Card` is a frozen dataclass, and that one decision pays for four
requirements at once.** `@dataclass(frozen=True)` generates `__init__`,
`__repr__` — already the exact `Card(rank='A', suit='Spades')` shape the
requirements ask for — `__eq__` comparing both fields, and, because the card
cannot change, `__hash__`. Frozen is not decoration. Python's rule is that a
class defining `__eq__` loses `__hash__` unless it says otherwise, because
two objects that compare equal must hash equal and a changeable object cannot
promise that. Freezing the card removes the change, so the promise holds and
Python restores the hash.

**`ClassVar` is what keeps `RANKS` and `SUITS` out of the constructor.** A
dataclass turns *every annotated name in the class body* into a field.
`RANKS: tuple[str, ...] = (...)` would become a field with a default, sitting
in the generated `__init__` ahead of `rank` and `suit`, which have none — and
that is not a legal signature.

**Ordering is computed from positions, never from the strings.** `sort_key`
returns `(RANKS.index(self.rank), SUITS.index(self.suit))`, and `__lt__`
compares those two tuples. Tuple comparison is left to right: it compares the
first elements, and only if they tie does it look at the second — which is
precisely "compare by rank order, ties broken by suit order" with no `if`
statement anywhere.

**`@total_ordering` turns two methods into six.** You write `__lt__`; the
dataclass writes `__eq__`; `total_ordering` reads those and fills in
`__le__`, `__gt__` and `__ge__`. That is why `max(hand)` and `min(hand)` work
in the demo without another line of code. The decorator order matters:
decorators apply bottom-up, so `@dataclass` runs first and installs `__eq__`,
and then `@total_ordering` — which looks for an existing `__lt__` and
`__eq__` — finds both. Flip the two lines and `total_ordering` runs before
`__eq__` exists.

**The deck's "top" is the end of the list, on purpose.** `list.pop()` with no
index removes the last element and moves nothing. `list.pop(0)` removes the
first and shifts every remaining card down one slot. The cost of that choice
is that the list's natural order is now *bottom* to top, so `__iter__`
returns `iter(self._cards[::-1])`: a reversed **copy**, so iteration yields
draw order and a snapshot that cannot be corrupted if something draws a card
mid-loop. `list(deck)[:5]` then really is the next five cards.

**`EmptyDeckError(IndexError)` gives you both options at once.** A caller
writing `except IndexError` catches it, a caller writing
`except EmptyDeckError` catches it, and the traceback names the specific
problem instead of a generic index failure. Same design as `InsufficientFunds`
in Exercise 5, and the same reason the standard library makes `KeyError` and
`IndexError` both subclasses of `LookupError`.

## Download and run

Download
[challenge-01-deck-of-cards-solution.py](./challenge-01-deck-of-cards-solution.py)
and run it:

```bash
python challenge-01-deck-of-cards-solution.py
```

It imports only from the standard library and seeds `random` itself, so two
runs on the same machine give identical output. Save your own version as
`deck.py`, which is the name the brief asks for and cannot collide with this
download.

## Common bugs to catch

- **A ten sorts below a two.**

  ```text
  ['10', '2', 'A', 'K']
  ```

  No exception, no warning — just a deck where a `10` is the lowest card and
  an ace beats a king by alphabetical accident. You compared the rank
  strings. This is the single most dangerous mistake in the challenge because
  it fails silently. It happens most often by reaching for
  `@dataclass(frozen=True, order=True)`, which compares the fields as a tuple
  using each field's own `<` — and `str.__lt__` is character by character.
  Compare `RANKS.index(...)` instead.

- **`TypeError: non-default argument 'rank' follows default argument 'RANKS'`.**
  You annotated `RANKS` as a normal field:

  ```python
  @dataclass(frozen=True)
  class Card:
      RANKS: tuple[str, ...] = ("2", "3", "A")
      rank: str
      suit: str
  ```

  The message names `rank`, not `RANKS`, which sends people off editing the
  wrong line. `RANKS` became a field with a default, and a defaulted field
  cannot be followed by one without a default. Fix it with
  `RANKS: ClassVar[tuple[str, ...]] = (...)`, or drop the annotation
  entirely — an unannotated class-body assignment is never a dataclass field.

- **`TypeError: unhashable type: 'Card'`.** You dropped `frozen=True`.
  `@dataclass` with the default `eq=True` sets `__hash__` to `None`,
  deliberately. Your options are `frozen=True` (best — a card is a value, not
  a thing that changes), `eq=False` (loses `==`, useless here), or
  `unsafe_hash=True` (the name is the warning: you are promising never to
  change a field that feeds the hash, and nothing enforces it).

- **`TypeError: object of type 'NoneType' has no len()`.** You wrote
  `self._cards = random.shuffle(self._cards)`. `random.shuffle` shuffles in
  place and returns `None`, so you replaced the deck with nothing. The
  failure surfaces in `__len__`, several calls from the mistake.

- **`ValueError: tuple.index(x): x not in tuple`.** `sort_key` called
  `.index()` on a rank that is not in `RANKS`. That means a bad card got
  built, which means `__post_init__` is not doing its job — check its
  spelling, two underscores each side.

- **Drawing mid-loop skips cards.** You returned `iter(self._cards)` or
  `reversed(self._cards)` from `__iter__` instead of a slice. Both are live
  views. Removing an element while iterating a live list makes the loop skip
  the next one, silently. `self._cards[::-1]` makes a copy.

- **`len(set(deck))` is less than 52.** Your `_fresh_cards` has a loop bug —
  usually the two `for` clauses in the comprehension are the wrong way round,
  or one of them iterates `Card.RANKS` twice.

## Under the hood

<details>
<summary>Under the hood — the protocols a collection implements, and what each one buys</summary>

`Deck` never inherits from `list` and never registers itself anywhere. It
works with `len()`, `for`, `list()` and `in` because Python asks objects for
specific method names and uses whatever it finds. That is **duck typing**,
and each of these name-and-behaviour pairs is called a **protocol**.

The ones this challenge touches:

| you write | Python calls | protocol |
|---|---|---|
| `len(deck)` | `deck.__len__()` | sized |
| `for c in deck` | `deck.__iter__()` | iterable |
| `list(deck)`, `sorted(deck)`, `max(deck)` | `deck.__iter__()` | iterable |
| `card in deck` | `deck.__contains__` or falls back to `__iter__` | container |
| `if deck:` | `deck.__bool__`, or falls back to `__len__` | truthiness |
| `sorted(hand)` | `__lt__` on pairs | ordered |
| `{card}` | `card.__hash__()` then `__eq__` | hashable |

Two of those fallbacks are worth knowing.

**`in` falls back to iteration.** You did not write `__contains__`, and yet:

```text
>>> deck = Deck()
>>> Card("A", "Spades") in deck
True
```

Python could not find `__contains__`, so it iterated and compared each item
with `==`. That is O(n), where a set would be O(1) — but it is correct, and
it means `__contains__` is an optimisation you add when you have measured a
reason, not a method you must write.

**`if deck:` falls back to `__len__`.** With no `__bool__`, an object is
truthy unless its length is zero. So a drained deck is falsy for free, and
`while deck: deck.draw()` terminates:

```text
>>> empty = Deck()
>>> for _ in range(52):
...     empty.draw()
...
>>> bool(empty)
False
```

That fallback is also a trap in the other direction. Any class with a
`__len__` that can return `0` is falsy sometimes, whether or not you meant it
to be. If "empty" and "false" are not the same idea for your class, write
`__bool__` and say so.

Now `sorted`. It does not need `__gt__`, `__le__` or `__eq__`. It needs
`__lt__` and nothing else — every comparison it makes is `a < b`. `min` and
`max` are the same. So a class with only `__lt__` sorts perfectly, and
`@total_ordering` is there for the *other* call sites, the ones that write
`card_a >= card_b` directly.

`total_ordering` is not free. It builds the missing methods out of your
`__lt__` and `__eq__`, so `a >= b` becomes `not (a < b)` plus an equality
check — two calls where a hand-written `__ge__` would be one. Nobody cares
for 52 cards. For a sort inside a tight loop over a million records, write
the four by hand or store a `sort_key` and use `sorted(items, key=...)`,
which calls the key function once per item instead of once per comparison.

Finally, `NotImplemented`. It is a singleton object, not an exception, and it
is not the same thing as `NotImplementedError`:

```text
>>> Card("A", "Spades").__lt__("hello")
NotImplemented
>>> Card("A", "Spades") < "hello"
TypeError: '<' not supported between instances of 'Card' and 'str'
```

Returning it says "I do not handle this operand". Python then tries the
reflected operation — here `"hello".__gt__(card)` — and only when that also
declines does it raise the `TypeError` you see. That message is better than
anything you would write by hand, it names both types, and it is the same
message every other Python type produces for the same mistake. Homework
problem 6 uses the identical move for `Length + 5`.

</details>

## Acceptance checklist

- [ ] `python deck.py` runs a demo with no traceback.
- [ ] `Card` validates rank and suit at construction.
- [ ] `Card` has working `__repr__`, `__str__`, `__eq__`, `__lt__` and
      `__hash__`.
- [ ] `sorted([Card("10","Clubs"), Card("2","Clubs"), Card("A","Clubs")])`
      gives ranks in the order `2`, `10`, `A`.
- [ ] `len(deck)` returns the number of remaining cards, and
      `len(set(Deck())) == 52`.
- [ ] `for c in deck:` works and yields the top card first.
- [ ] `deck.draw()` removes and returns the top card, and raises a clear
      error on an empty deck.
- [ ] Seeding `random` before two shuffles gives the same order twice.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 challenge 1: deck of cards`.

## Stretch

- Replace the string ranks and suits with `enum.IntEnum` members. Once a rank
  *is* an integer, `@dataclass(frozen=True, order=True)` produces exactly the
  ordering this challenge specifies, and you can delete `__lt__`, `sort_key`
  and `@total_ordering` outright. Note what you give up: `Card(Rank.ACE,
  Suit.SPADES)` is wordier than `Card("A", "Spades")` at every call site.
  That is the usual enum trade — safety at construction, verbosity in use.
- Add a `Hand` class holding cards, with `__contains__`, `__len__`,
  `__iter__` and a `value()` method for Blackjack. The interesting part is
  aces: a hand of `A A` is 12, not 22, because one ace drops from 11 to 1.
  Write `value()` as a method rather than a property so the demotion loop has
  somewhere to live.
- Write four or five `pytest` tests for `Card` and `Deck`. The one that pays
  for `__hash__` is `len(set(Deck())) == 52` — it proves there are no
  duplicates and it only runs at all because cards are hashable. The one that
  pays for the seed is "same seed, same order", and make it assert the
  negative too: a `shuffle()` that did nothing would pass the first half
  perfectly.
- Add `__contains__` to `Deck` backed by a `set`, then measure it against the
  iteration fallback with `timeit`. Write one sentence saying whether the
  extra state was worth it at 52 cards.

When your deck deals cleanly, move on to
[Challenge 02 — Employee Hierarchy and Payroll](./challenge-02-employee-hierarchy.md).
