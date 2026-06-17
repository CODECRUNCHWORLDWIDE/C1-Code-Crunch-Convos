# Challenge 01 — A Deck of Cards

> **Estimated time:** 90–120 minutes. **Difficulty:** medium.

A classic OOP exercise. Done well, it is a perfect playground for **dunder
methods** — your deck will support `len(deck)`, `for card in deck`, sorting,
and equality, just like a built-in collection.

---

## Background

A standard 52-card deck has four **suits** (`♣`, `♦`, `♥`, `♠`) and 13
**ranks** (`2`–`10`, `J`, `Q`, `K`, `A`). Each card is one suit + one rank.
You will model both pieces and put them together.

---

## Requirements

Create a single file `deck.py` with two classes.

### `Card`

- Fields: `rank: str`, `suit: str`.
- A class attribute `RANKS` holding `("2", "3", ..., "10", "J", "Q", "K", "A")`
  — exactly 13 strings in order.
- A class attribute `SUITS` holding `("Clubs", "Diamonds", "Hearts", "Spades")`.
- Validation: `__init__` (or `__post_init__` if you use a dataclass) must
  reject invalid ranks or suits with `ValueError`.
- `__repr__` returning something like `Card(rank='A', suit='Spades')`.
- `__str__` returning something like `"A of Spades"`.
- Implements `__eq__` (two cards are equal iff rank and suit match) and
  `__lt__` (compare by rank order, ties broken by suit order). Optional:
  use `@functools.total_ordering` so all comparisons work.
- `__hash__` so cards can live in `set`s. (A frozen dataclass gives this
  for free.)

### `Deck`

- `__init__(self, shuffled: bool = False)` builds a fresh 52-card deck. If
  `shuffled=True`, shuffle it (use `random.shuffle`).
- `shuffle(self) -> None` — shuffles the remaining cards in place.
- `draw(self) -> Card` — removes and returns the **top** card (your choice
  of which end of the list is "the top" — be consistent). Raise
  `IndexError` (or a custom `EmptyDeckError`) if empty.
- `__len__(self) -> int` — number of cards remaining.
- `__iter__(self)` — iterate over remaining cards in current order.
- `__repr__` showing `Deck(remaining=42)` or similar.
- Optional: a `reset(self) -> None` method that refills the deck back to 52
  cards.

---

## Example session

Your finished `deck.py` should support something like this:

```python
from deck import Card, Deck
import random

random.seed(0)              # reproducible shuffle

deck = Deck(shuffled=True)
print(len(deck))            # 52
print(repr(deck))           # Deck(remaining=52)

card = deck.draw()
print(card)                 # e.g. "7 of Hearts"
print(repr(card))           # Card(rank='7', suit='Hearts')
print(len(deck))            # 51

# iterate — peek at the next 5 cards without drawing them
for c in list(deck)[:5]:
    print(c)

# equality
a = Card("A", "Spades")
b = Card("A", "Spades")
assert a == b

# sorting
hand = [Card("2", "Clubs"), Card("K", "Diamonds"), Card("5", "Hearts")]
print(sorted(hand))
```

---

## Acceptance criteria

- [ ] `Card` validates rank and suit in `__init__`.
- [ ] `Card` has working `__repr__`, `__str__`, `__eq__`, `__lt__`,
      `__hash__`.
- [ ] `len(deck)` returns the number of remaining cards.
- [ ] `for c in deck:` works.
- [ ] `deck.draw()` removes and returns the top card; raises a clear error
      on an empty deck.
- [ ] `deck.shuffle()` randomizes order; passing the same seed before
      shuffling gives the same order (so it is testable).
- [ ] All your code is **type-hinted**.
- [ ] You include a small `if __name__ == "__main__":` demo at the bottom
      of the file that runs cleanly with `python deck.py`.

---

## Stretch goals

- Use `enum.IntEnum` for `Rank` and `Suit` instead of strings.
- Make `Card` a `@dataclass(frozen=True, order=True)` and let the dataclass
  generate the comparisons.
- Add a `Hand` class that contains cards and implements `__contains__`,
  `__len__`, and a `value()` method (e.g. for Blackjack).
- Write 3–5 small `pytest` tests for `Card` and `Deck`.
