"""problem-03-rate-limit-decorator-solution.py — space calls out so you stay welcome.

A decorator that enforces a minimum gap between successive calls to the
function it wraps, sleeping when a call arrives too soon.

There is no network here, and there is no waiting either. The decorator takes
its clock and its sleep function as arguments, so the demo can hand it a fake
clock that jumps forward instantly. Real time is the default; fake time is what
makes the run below finish in no time at all and print the same numbers every
time.

Run it with::

    python problem-03-rate-limit-decorator-solution.py
"""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

#: A function that reports the time, in seconds, on some steady clock.
Clock = Callable[[], float]

#: A function that pauses for a number of seconds.
Sleep = Callable[[float], None]

F = TypeVar("F", bound=Callable[..., Any])


class FakeClock:
    """A clock that only moves when it is told to.

    Standing in for ``time.perf_counter`` and ``time.sleep`` together, so a
    test can watch a rate limiter work without waiting for it. ``now`` is the
    reading; ``sleep`` advances it and records how long it was asked for.
    """

    def __init__(self) -> None:
        """Start the clock at zero with nothing recorded."""
        self.reading = 0.0
        self.slept: list[float] = []

    def now(self) -> float:
        """Return the current reading.

        Returns:
            Seconds since this clock was created, on its own private timeline.
        """
        return self.reading

    def sleep(self, seconds: float) -> None:
        """Advance the clock instead of waiting.

        Args:
            seconds: How long the caller believes it is sleeping for.
        """
        self.slept.append(seconds)
        self.reading += seconds

    def tick(self, seconds: float) -> None:
        """Move the clock forward without anybody having slept.

        Args:
            seconds: How much time passed while other work happened.
        """
        self.reading += seconds


def rate_limited(
    calls_per_second: float,
    *,
    clock: Clock = time.perf_counter,
    sleep: Sleep = time.sleep,
) -> Callable[[F], F]:
    """Return a decorator allowing at most *calls_per_second* calls a second.

    The first call goes through immediately. Every call after it waits, if it
    has to, until a full interval has passed since the previous one started.

    This is safe for a single-threaded program and is **not** thread-safe: two
    threads can read the last-call time before either writes it back, and both
    then go through together. Making it safe needs a lock around the read, the
    sleep and the write, which is out of scope here and worth knowing about.

    Args:
        calls_per_second: The ceiling. Must be greater than zero.
        clock: How to read the time. Defaults to a real steady clock.
        sleep: How to wait. Defaults to really waiting.

    Returns:
        A decorator.

    Raises:
        ValueError: calls_per_second is not positive.
    """
    if calls_per_second <= 0:
        raise ValueError("calls_per_second must be greater than zero")
    interval = 1.0 / calls_per_second

    def decorate(function: F) -> F:
        last_call: list[float | None] = [None]

        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            previous = last_call[0]
            if previous is not None:
                wait = interval - (clock() - previous)
                if wait > 0:
                    sleep(wait)
            last_call[0] = clock()
            return function(*args, **kwargs)

        wrapper.interval = interval  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorate


def check() -> int:
    """Run every example and report.

    Returns:
        The number of checks that ran.
    """
    checks = 0

    # 1. Four calls at two per second means three gaps of half a second.
    fake = FakeClock()

    @rate_limited(2.0, clock=fake.now, sleep=fake.sleep)
    def greet(name: str) -> str:
        """Say hello to somebody."""
        return f"hello {name}"

    results = [greet(name) for name in ("a", "b", "c", "d")]
    assert results == ["hello a", "hello b", "hello c", "hello d"], results
    assert fake.slept == [0.5, 0.5, 0.5], fake.slept
    assert fake.now() == 1.5, fake.now()
    print(f"ok  four calls at 2/sec slept {fake.slept}, total {fake.now()}s")
    checks += 1

    # 2. The wrapper still looks like the function it wrapped.
    assert greet.__name__ == "greet", greet.__name__
    assert greet.__doc__ == "Say hello to somebody.", greet.__doc__
    print(f"ok  wrapper kept its name ({greet.__name__!r}) and its docstring")
    checks += 1

    # 3. A call that arrives late enough does not sleep at all.
    fake = FakeClock()

    @rate_limited(2.0, clock=fake.now, sleep=fake.sleep)
    def noop() -> None:
        """Do nothing, politely."""

    noop()
    fake.tick(3.0)
    noop()
    assert fake.slept == [], fake.slept
    print("ok  a call that arrives late enough does not sleep")
    checks += 1

    # 4. A slower limit means a longer gap.
    fake = FakeClock()

    @rate_limited(0.5, clock=fake.now, sleep=fake.sleep)
    def slow() -> None:
        """Do nothing, very politely."""

    slow()
    slow()
    assert fake.slept == [2.0], fake.slept
    print(f"ok  half a call per second waits {fake.slept[0]}s between calls")
    checks += 1

    # 5. Two decorated functions keep separate schedules.
    fake = FakeClock()
    limit = rate_limited(1.0, clock=fake.now, sleep=fake.sleep)
    first = limit(lambda: "first")
    second = limit(lambda: "second")
    first()
    second()
    assert fake.slept == [], fake.slept
    print("ok  two wrapped functions do not share a schedule")
    checks += 1

    # 6. A nonsense limit is refused at decoration time, not at call time.
    try:
        rate_limited(0)
    except ValueError as exc:
        print(f"ok  rate_limited(0) raised ValueError: {exc}")
        checks += 1
    else:  # pragma: no cover - only reached if the guard is removed
        raise AssertionError("rate_limited(0) should have raised")

    return checks


if __name__ == "__main__":
    total = check()
    print()
    print(f"{total} checks passed, and not one real second was spent waiting.")
