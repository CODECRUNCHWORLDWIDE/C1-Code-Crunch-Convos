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
