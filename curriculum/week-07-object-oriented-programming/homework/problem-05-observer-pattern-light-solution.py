"""problem-05-observer-pattern-light-solution.py — a light observer / event system.

The `-solution` in the name keeps this file from colliding with the `events.py`
you write yourself. Run it with::

    python problem-05-observer-pattern-light-solution.py

Subscribers are plain callables. No Observer base class, no interface to
implement: this is composition, and it is why a function, a bound method, a
lambda and an instance with `__call__` are all valid observers here.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import Any

Observer = Callable[[Any], None]


class Subject:
    """Keeps a list of callables and hands each of them every event."""

    def __init__(self) -> None:
        """Start with nobody listening."""
        self._observers: list[Observer] = []

    def subscribe(self, callback: Observer) -> None:
        """Add `callback` to the list, ignoring a repeat subscription."""
        if not callable(callback):
            raise TypeError(f"observer must be callable, got {type(callback).__name__}")
        if callback in self._observers:
            return                       # subscribing twice would fire twice
        self._observers.append(callback)

    def unsubscribe(self, callback: Observer) -> None:
        """Remove `callback`, or say plainly that it was never there."""
        try:
            self._observers.remove(callback)
        except ValueError:
            # __qualname__ instead of repr(): a function's repr carries a memory
            # address, which makes the message different on every run.
            name = getattr(callback, "__qualname__", repr(callback))
            raise ValueError(f"{name} is not subscribed") from None

    def notify(self, event: Any) -> None:
        """Hand `event` to every subscriber, in subscription order."""
        # Iterate over a COPY: an observer is allowed to unsubscribe itself
        # while being notified, and mutating a list mid-iteration silently
        # skips the next element.
        for callback in list(self._observers):
            callback(event)

    def __len__(self) -> int:
        """How many observers are subscribed."""
        return len(self._observers)


class TemperatureSensor(Subject):
    """A Subject that has a reading. Notifies only when the value changes."""

    def __init__(self, celsius: float = 0.0) -> None:
        """Set the opening reading and initialise the Subject half."""
        super().__init__()               # the Subject half must be initialised
        self._celsius = float(celsius)

    @property
    def temperature(self) -> float:
        """The current reading in degrees Celsius."""
        return self._celsius

    def set_temperature(self, value: float) -> None:
        """Store a new reading, notifying only if it actually changed."""
        if value == self._celsius:
            return                       # no change, no event
        self._celsius = float(value)
        self.notify(self._celsius)

    def __repr__(self) -> str:
        """Developer form, showing the reading and the observer count."""
        return f"TemperatureSensor(celsius={self._celsius!r}, observers={len(self)})"


class LastValues:
    """An observer with memory: keeps the most recent `size` readings.

    `deque(maxlen=...)` does the bounded-history bookkeeping for you — appending
    to a full deque drops the oldest item.
    """

    def __init__(self, size: int = 5) -> None:
        """Keep at most `size` readings."""
        self.values: deque[float] = deque(maxlen=size)

    def record(self, event: float) -> None:
        """Store one reading, evicting the oldest if the deque is full."""
        self.values.append(event)

    def __call__(self, event: float) -> None:
        """So the instance itself can be handed to `subscribe`."""
        self.record(event)

    def __repr__(self) -> str:
        """Developer form, showing the readings oldest first."""
        return f"LastValues({list(self.values)!r})"


def print_reading(event: float) -> None:
    """A module-level function used as an observer."""
    print(f"  [printer] temperature is now {event:.1f} C")


def main() -> None:
    """Wire two observers to a sensor, then add two more of different kinds."""
    sensor = TemperatureSensor(celsius=20.0)
    recorder = LastValues(size=5)

    sensor.subscribe(print_reading)
    sensor.subscribe(recorder.record)     # a bound method is a callable
    print(repr(sensor))

    for reading in [21.0, 21.0, 22.5, 19.0, 25.5, 30.0, 31.5]:
        print(f"set_temperature({reading})")
        sensor.set_temperature(reading)

    print("recorded:", recorder)          # 21.0 was only fired once
    print("recorder kept", len(recorder.values), "of 6 changes")

    # --- unsubscribe -----------------------------------------------------
    sensor.unsubscribe(print_reading)
    sensor.set_temperature(12.0)          # recorder still fires, printer does not
    print("after unsubscribe:", recorder, "| observers:", len(sensor))

    try:
        sensor.unsubscribe(print_reading)
    except ValueError as exc:
        print("ValueError:", exc)

    try:
        sensor.subscribe("not a function")   # type: ignore[arg-type]
    except TypeError as exc:
        print("TypeError:", exc)

    # --- any callable works ---------------------------------------------
    alarms: list[str] = []
    sensor.subscribe(lambda t: alarms.append(f"ALARM at {t} C") if t > 30 else None)
    sensor.subscribe(LastValues(size=2))      # instance with __call__
    sensor.set_temperature(35.0)
    sensor.set_temperature(10.0)
    print("alarms:", alarms)
    print("final:", repr(sensor), "| history:", recorder)


if __name__ == "__main__":
    main()
