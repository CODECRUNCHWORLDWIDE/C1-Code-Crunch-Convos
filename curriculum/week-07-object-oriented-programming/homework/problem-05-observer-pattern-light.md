# Problem 5 — Observer pattern (light)

> **Topic:** a subject that calls whoever is listening — your first design pattern, built out of nothing but callables
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** it is the first *design pattern* in the course, and Python's version is startlingly small. In Java you would declare an `Observer` interface and every listener would implement it. Here the interface is "can be called with one argument", and a function, a bound method, a lambda and an object all qualify. Seeing how little code the pattern needs is the lesson — and so is seeing the one place where a careless loop makes an observer silently vanish.

## The Brief

Build a tiny **observer / event** system, then wire a temperature sensor to it.

An observer system is a doorbell with a list of people to ring. The `Subject`
is the door. Anyone can put their name on the list (`subscribe`), take it off
(`unsubscribe`), and when something happens the door rings everyone on the
list, in order (`notify`). The door does not know or care *who* is listening —
it only knows how to ring.

- `Subject` keeps a list of observer callables.
- `Subject.subscribe(callback) -> None` — adds a callable, refuses
  a non-callable with `TypeError`, and quietly ignores a repeat subscription.
- `Subject.unsubscribe(callback) -> None` — removes it, or raises
  `ValueError` naming the callable if it was never there.
- `Subject.notify(event: Any) -> None` — calls every subscriber with the
  event.

Then build a `TemperatureSensor(Subject)` whose `set_temperature(value)`
notifies subscribers **when the value changes** — not on every call. Wire up
two observers in `main()` — one that prints, one that records the last 5
values — and demonstrate them firing together.

**This is composition, not inheritance: subscribers are just callables.**
That closing line of the assignment is the design. There is no `Observer`
base class and no interface to implement. A module-level function, a bound
method like `recorder.record`, a `lambda`, and an instance with `__call__`
are all valid observers, because the only thing `notify` ever does to one is
call it with a single argument. The demo uses all four kinds on purpose.

One inheritance *is* in the picture, and it is the honest kind:
`TemperatureSensor` **is a** `Subject` — a sensor is a thing that can be
listened to, plus a reading. It subclasses, calls `super().__init__()` for
the observer list, and adds one field and one method. The listeners
themselves stay outside the hierarchy entirely.

## Starter

Save this as `events.py` and fill in the `TODO` markers. `LastValues` is
given nearly complete and `print_reading` entirely so, because the point of
the problem is `Subject` and the sensor — not the listeners.

```python
"""events.py — a light observer / event system.

    python events.py
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
        # TODO: create the empty observer list, self._observers

    def subscribe(self, callback: Observer) -> None:
        """Add `callback` to the list, ignoring a repeat subscription."""
        # TODO: raise TypeError if `callback` is not callable, naming its
        # type. Return early if it is already subscribed. Then append it.

    def unsubscribe(self, callback: Observer) -> None:
        """Remove `callback`, or say plainly that it was never there."""
        # TODO: self._observers.remove(callback), turning the ValueError a
        # miss raises into one that names the callable. Use __qualname__,
        # not repr() — a function's repr carries a memory address.

    def notify(self, event: Any) -> None:
        """Hand `event` to every subscriber, in subscription order."""
        # TODO: call every observer with `event`. Iterate over a COPY of
        # the list — an observer may unsubscribe itself mid-notification.

    def __len__(self) -> int:
        """How many observers are subscribed."""
        # TODO


class TemperatureSensor(Subject):
    """A Subject that has a reading. Notifies only when the value changes."""

    def __init__(self, celsius: float = 0.0) -> None:
        """Set the opening reading and initialise the Subject half."""
        # TODO: super().__init__() FIRST — it is the only place the
        # observer list is created — then store self._celsius.

    @property
    def temperature(self) -> float:
        """The current reading in degrees Celsius."""
        return self._celsius

    def set_temperature(self, value: float) -> None:
        """Store a new reading, notifying only if it actually changed."""
        # TODO: return early when nothing changed; otherwise store the
        # new value and notify with it.

    def __repr__(self) -> str:
        """Developer form, showing the reading and the observer count."""
        # TODO


class LastValues:
    """An observer with memory: keeps the most recent `size` readings.

    `deque(maxlen=...)` does the bounded-history bookkeeping for you —
    appending to a full deque drops the oldest item.
    """

    def __init__(self, size: int = 5) -> None:
        """Keep at most `size` readings."""
        self.values: deque[float] = deque(maxlen=size)

    def record(self, event: float) -> None:
        """Store one reading, evicting the oldest if the deque is full."""
        self.values.append(event)

    def __call__(self, event: float) -> None:
        """So the instance itself can be handed to `subscribe`."""
        # TODO: one line — hand the event to `record`.

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
```

Look at what `main()` subscribes, because it is a deliberate parade: a
module-level function, a **bound method** (`recorder.record`), a `lambda`,
and a whole **instance** (`LastValues(size=2)`, callable because it defines
`__call__`). Four different kinds of thing, one list, and `notify` treats
them identically. That is duck typing doing the job an interface would do
elsewhere.

## Requirements

1. `Subject` stores its observers in a list, in subscription order.
2. `subscribe` raises `TypeError` for a non-callable, naming the actual
   type, and silently ignores a callable that is already subscribed.
3. `unsubscribe` removes the callable, or raises `ValueError` whose message
   names it by `__qualname__`.
4. `notify(event)` calls every subscriber with `event`, iterating over a
   **copy** of the list.
5. `__len__` reports how many observers are subscribed.
6. `TemperatureSensor` subclasses `Subject` and calls `super().__init__()`
   as its first statement.
7. `set_temperature` notifies only when the value actually changed. Setting
   the same value twice fires once.
8. `LastValues` keeps the most recent `size` readings and its instances are
   themselves valid observers.
9. Do not edit `main()`.

## Constraints

- **No `Observer` base class.** The whole point. The coupling between
  `Subject` and its listeners is one call signature wide — "callable with one
  argument" — and every kind of callable in `main()` must work unmodified.
- **`notify` iterates over a copy.** An observer is entirely within its
  rights to unsubscribe itself while being notified. Mutate the list you are
  looping over and the loop silently skips the next observer — no exception,
  no warning, just a handler that sometimes does not fire.
- **Notify on change, not on set.** A sensor polling every second would
  otherwise flood its observers with identical readings. The demo sets
  `21.0` twice so you can see the guard working.
- **The error message uses `__qualname__`, never `repr()`.** A function's
  repr is `<function print_reading at 0x000001DC80211440>` — the address
  changes on every run, which makes the output impossible to compare
  against, including by this page.
- **`super().__init__()` comes first.** `Subject.__init__` is the only place
  `self._observers` is created. Skip it and the crash surfaces from
  `subscribe`, several lines away from the actual mistake.
- **`deque(maxlen=...)`, not a hand-trimmed list.** Appending to a full
  deque evicts the oldest item in O(1). The hand-rolled
  `if len(values) > 5: values.pop(0)` is three extra lines and an O(n)
  shift for the same behaviour.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-05-observer-pattern-light.py
TemperatureSensor(celsius=20.0, observers=2)
set_temperature(21.0)
  [printer] temperature is now 21.0 C
set_temperature(21.0)
set_temperature(22.5)
  [printer] temperature is now 22.5 C
set_temperature(19.0)
  [printer] temperature is now 19.0 C
set_temperature(25.5)
  [printer] temperature is now 25.5 C
set_temperature(30.0)
  [printer] temperature is now 30.0 C
set_temperature(31.5)
  [printer] temperature is now 31.5 C
recorded: LastValues([22.5, 19.0, 25.5, 30.0, 31.5])
recorder kept 5 of 6 changes
after unsubscribe: LastValues([19.0, 25.5, 30.0, 31.5, 12.0]) | observers: 1
ValueError: print_reading is not subscribed
TypeError: observer must be callable, got str
alarms: ['ALARM at 35.0 C']
final: TemperatureSensor(celsius=10.0, observers=3) | history: LastValues([30.0, 31.5, 12.0, 35.0, 10.0])
```

Three things to check. The second `set_temperature(21.0)` prints nothing —
the change guard works. `recorded:` starts at 22.5, not 21.0, because the
deque evicted the oldest of six values. And after `unsubscribe(print_reading)`,
`set_temperature(12.0)` produces no printer line but 12.0 does appear in the
recorder's history — the two observers really are independent.

## Steps

1. Save the starter and run it. It fails with
   `TypeError: __repr__ returned non-string (type NoneType)` — the sensor's
   `__repr__` is still only a comment, and a method whose body is only a
   comment returns `None`.
2. Write `TemperatureSensor.__init__` — `super().__init__()` first — and
   `__repr__`. Run again. The first line now prints, but says `observers=0`
   even though `main()` subscribed two. Nothing raised: `subscribe` is still
   a comment, so it silently did nothing. Sit with that for a second — a
   stub that *returns* `None` is invisible in a way a stub that *raises*
   is not.
3. Write `Subject.__init__`, `subscribe` and `__len__`. The first line
   should now say `observers=2`.
4. Write `notify` and `set_temperature`. The printer lines appear. Check the
   two `set_temperature(21.0)` calls produce exactly one printer line.
5. Fill in `LastValues.__call__` and confirm the `recorded:` line — it must
   start at 22.5, because six changes went into a five-slot deque.
6. Write `unsubscribe` and check all three refusal lines: the printer goes
   quiet, the second removal raises with the function's *name*, and
   subscribing a string is refused up front.
7. Now break it on purpose. Change `notify` to iterate `self._observers`
   directly — no copy — and add this above `main()`'s final prints:

   ```python
   def once(t: float) -> None:
       print("  [once] fired, now leaving")
       sensor.unsubscribe(once)
   sensor.subscribe(once)
   ```

   Watch an observer *after* `once` in the list silently miss an event.
   No traceback. Put the copy back and the snippet becomes harmless.

## The Solution

```python
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
```

**Observers are callables, so there is nothing to implement.** The brief's
closing line — "this is composition, not inheritance: subscribers are just
callables" — is the design. In Java you would define an `Observer` interface
and every subscriber would implement it. In Python the interface is "can be
called with one argument", and a module-level function, a bound method
(`recorder.record`), a `lambda`, and an instance with `__call__` all satisfy
it. The demo uses all four deliberately. This is lecture 02's duck typing at
its most useful: the coupling between `Subject` and its observers is one call
signature wide.

**`notify` iterates over `list(self._observers)`, a copy.** An observer is
entirely within its rights to call `unsubscribe` on itself — a one-shot
handler, say. If `notify` iterated the live list, removing an element during
iteration would shift the remaining elements down and the loop's index would
skip the next observer, silently. A copy costs one small allocation per
notification and removes an entire class of heisenbug.

**`set_temperature` only fires on an actual change**, which is what the brief
asks for ("notifies subscribers when the value changes"). The demo sets 21.0
twice and you can see exactly one printer line and one recorded value.
Without the guard, a sensor polling every second would flood its observers
with identical readings.

**`super().__init__()` in `TemperatureSensor.__init__` is mandatory, not
optional.** `Subject.__init__` is the only place `self._observers` is
created. Skip the `super()` call and:

```text
AttributeError: 'TemperatureSensor' object has no attribute '_observers'
```

surfacing from `subscribe`, not from the constructor.

**`deque(maxlen=5)` is the right tool for "last N".** Appending to a full
`deque` evicts from the other end automatically, in O(1). The hand-rolled
version — `self.values.append(x)` then `if len(self.values) > 5:
self.values.pop(0)` — is correct but is three lines and an O(n) shift where
the standard library gives you zero lines and O(1). The demo shows the
eviction: six changes, five values kept.

**`subscribe` refuses duplicates.** Subscribing the same callable twice would
deliver each event twice, and then a single `unsubscribe` would remove only
one copy, leaving the observer half-attached. Silently ignoring the
re-subscribe keeps the list a set-like collection while preserving order.

**`unsubscribe` on an absent callback raises rather than passing silently.**
If you thought you were subscribed and you were not, you want to hear about
it. The message uses `__qualname__` rather than `repr()` because a function's
repr contains its memory address —
`<function print_reading at 0x000001DC80211440>` — which changes on every run
and makes the output impossible to test against.

Two details about identity: `recorder.record` creates a **new** bound-method
object every time you write it, but bound methods compare equal when the
underlying function and instance are the same, so `list.remove` finds it.
Lambdas are the exception — every `lambda` expression is a distinct object
with no equal twin, so you *cannot* unsubscribe a lambda you did not keep a
reference to. Bind it to a name first if you will need to remove it.

## Run it

Copy the worked answer on this page into `problem-05-observer-pattern-light.py` and run it:

```bash
python problem-05-observer-pattern-light.py
```

It imports nothing outside the standard library and needs no setup. Save your
own version as `events.py`; the longer download name is there so it cannot
overwrite your work.

## Common bugs to catch

- **`AttributeError: 'TemperatureSensor' object has no attribute '_observers'`.**
  The single most common failure in this problem, because
  `TemperatureSensor.__init__` looks complete on its own:

  ```python
  class TemperatureSensor(Subject):
      def __init__(self, celsius: float = 0.0) -> None:
          self._celsius = float(celsius)   # and no super().__init__()
  ```

  The traceback points at `subscribe`, several calls away from the actual
  mistake, because nothing reads `_observers` until then.

- **One observer mysteriously does not fire — and only sometimes.** You
  iterated the live list in `notify`:

  ```python
  def notify(self, event):
      for callback in self._observers:      # live list
          callback(event)
  ```

  An observer that unsubscribes itself makes the loop skip the next
  observer. No exception, no warning, just one handler that quietly misses
  an event. Iterate `list(self._observers)`.

- **The printer says 21.0 twice.** You notified on every *set* instead of
  every *change*, and the sensor became a firehose. Compare the two
  `set_temperature(21.0)` lines in the transcript — the second prints
  nothing.

- **`TypeError: 'str' object is not callable`, raised from `notify`.** You
  skipped the callable check in `subscribe`, so the bad observer was
  accepted quietly and only exploded when the first event tried to call it —
  far from the line that caused it. The check in `subscribe` moves the error
  to where the mistake was made.

- **`ValueError: <lambda> is not subscribed`.**
  `s.subscribe(lambda t: print(t))` then `s.unsubscribe(lambda t: print(t))`
  fails — the two lambdas are different objects that happen to share source
  text. Keep a reference to any lambda you will need to remove.

- **Writing `class Observer(ABC)` with an abstract `update()`.** It works,
  and it means you can no longer pass a plain function, so every trivial
  handler needs a class. That is the Java shape of this pattern, and the
  brief is specifically pointing at the alternative.

## Under the hood

<details>
<summary>Under the hood — bound methods, lambdas, and what "callable" actually means</summary>

`callable(x)` asks one question: does `type(x)` define `__call__`? Everything
`main()` subscribes answers yes, for four different reasons:

- **A function** — functions are objects of type `function`, which defines
  `__call__`. That is all "calling a function" is.
- **A bound method** — `recorder.record` is not a function; it is a
  *method object* wrapping two things, the underlying function
  (`LastValues.record`) and the instance it is bound to (`recorder`).
- **A lambda** — exactly a function with no name and one expression.
- **An instance with `__call__`** — `LastValues(size=2)` is callable because
  its class says so. This is how objects impersonate functions, and it is
  the trick behind decorators-with-state and `functools.partial`.

The bound-method detail hides a genuine subtlety. Every time you write
`recorder.record`, Python builds a **fresh** method object:

```text
>>> recorder.record is recorder.record
False
>>> recorder.record == recorder.record
True
```

Two different objects, yet equal — method objects compare equal when their
underlying function and their instance are both the same. That equality is
the only reason `unsubscribe(recorder.record)` works: `list.remove` searches
by `==`, finds the equal method object made at subscribe time, and removes
it. Lambdas have no such equality — two lambdas with identical source text
are just two functions — which is why the page warns you cannot unsubscribe
a lambda you did not keep.

Two things real event systems add, and why this one leaves them out:

**Error isolation.** Here, an observer that raises kills the whole `notify`
loop — the observers after it never hear the event. For six lines of
homework that is honest; in a GUI toolkit or a message bus, one broken
plugin must not silence the rest, so real systems wrap each call and collect
the failures (Python 3.11's `ExceptionGroup` is built for exactly this).

**Weak references.** `self._observers` holds *strong* references. Subscribe
a method of some window object, close the window, and the sensor still
keeps the whole window alive — a memory leak shaped exactly like
"I forgot to unsubscribe". `weakref.WeakMethod` stores a reference that
does not prevent collection and hands back `None` once the object is gone,
at the price of checking for `None` on every notify. The standard library's
own observer systems (`logging` handlers, `atexit`) choose strong
references and documented unsubscribe, which is also what this solution
does.

</details>

## Acceptance checklist

- [ ] `python events.py` runs with no traceback.
- [ ] Every output line matches the transcript exactly.
- [ ] `TemperatureSensor.__init__` calls `super().__init__()` first.
- [ ] `notify` iterates over a copy of the observer list.
- [ ] The second `set_temperature(21.0)` produces no output at all.
- [ ] `recorded:` starts at 22.5 — the deque evicted the oldest of six.
- [ ] After the unsubscribe, 12.0 reaches the recorder but not the printer.
- [ ] Unsubscribing twice raises `ValueError: print_reading is not subscribed`.
- [ ] Subscribing a string raises `TypeError` naming `str`.
- [ ] Every signature is type-hinted.
- [ ] Committed to Git with a message like
      `Add Week 7 homework 5: observer pattern`.

## Stretch

- Add `subscribe_once(callback)` — a subscription that removes itself after
  its first event. Write it *without* touching `notify`, as a small wrapper
  callable that unsubscribes itself. Notice that it only works because
  `notify` iterates a copy — write one sentence saying why.
- Add named events: `notify("temperature", value)` and
  `subscribe("temperature", callback)`, with a dict of lists inside
  `Subject`. Decide what `unsubscribe` means when a callable is subscribed
  to two names, and write the decision down in the docstring.
- Make one observer raise, on purpose, and watch it silence every observer
  after it in the list. Then change `notify` to call every observer no
  matter what, collecting the failures, and re-raise them at the end as an
  `ExceptionGroup` (Python 3.11+).
- Subscribe a bound method of a short-lived object, delete the object, and
  show with `len(sensor)` that the sensor is keeping it alive. Then rebuild
  the observer list with `weakref.WeakMethod` so a dead observer drops out
  on the next notify. Note what got more complicated.

Next: [Problem 6 — Unit-conversion class](./problem-06-unit-conversion-class.md).
