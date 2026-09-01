# Homework Problem 3 — Rate-Limit Decorator

> **Topic:** a decorator that spaces calls out in time, tested against a clock you control
> **Lecture:** [03 — Authentication and Secrets](../lecture-notes/03-authentication-and-secrets.md)
> **Difficulty:** Advanced
> **Target time:** 1 hour 15 minutes
> **Why this one:** every public API sets a speed limit, and Exercise 4's Under the hood showed you the headers that announce it. This problem builds the polite client's half of that bargain — and because "does it wait correctly?" is miserable to test by actually waiting, it also hands you the week's big idea one more time: put the thing you cannot control behind a seam. Last time it was the network. This time it is the clock.

## The Brief

An API that allows two requests per second is not asking you to count to two
and stop. It is asking for a **gap**: at two per second, at least half a
second between the start of one call and the start of the next.

You are writing `@rate_limited(calls_per_second)` — a decorator that wraps
any function and enforces that gap. The first call goes straight through.
Every call after it checks the time since the previous one and sleeps for
whatever is left of the gap, if anything is.

```python
@rate_limited(2.0)
def hello(name: str) -> None:
    print(f"hello {name}")

for n in ["a", "b", "c", "d"]:
    hello(n)          # four calls, three enforced gaps: ~1.5s total
```

A decorator is a function that takes a function and hands back a replacement.
Week 6's [retry decorator](../../week-06-file-io-exceptions/homework/problem-04-retry-on-error-decorator-preview-of-decorators.md)
was your first one; this one has the same three-layer shape plus one new
ingredient — the replacement has to *remember* something between calls (when
it last ran), which is what a **closure** is for.

And one requirement that sounds like a detail and is actually the whole
second half of the problem: the decorated function must still look like
itself. Its name, its docstring — `functools.wraps` preserves them, and the
brief requires it.

Your decorator only needs to be correct for a single-threaded program.
Document that limit in its docstring — knowing where the edge is counts as
much as the code.

## Starter

Save this as `hw03_rate_limit.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — the wrapper passes calls through without
enforcing anything, so both asserts about timing fail until you write the
gap logic:

```python
"""A decorator that enforces a minimum gap between calls."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def rate_limited(calls_per_second: float) -> Callable[[F], F]:
    """Return a decorator allowing at most *calls_per_second* calls a second.

    Only safe for single-threaded programs: nothing guards the last-call
    time against two threads reading it at once.

    Args:
        calls_per_second: The ceiling. Must be greater than zero.

    Returns:
        A decorator.
    """
    # TODO: refuse calls_per_second <= 0 with a ValueError.
    interval = 1.0 / calls_per_second

    def decorate(function: F) -> F:
        # TODO: something here has to remember when the last call started.
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # TODO: if there was a previous call, work out how much of the
            #       interval is left and time.sleep() that much (never a
            #       negative amount).
            # TODO: record the current time as the last-call time.
            return function(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorate


if __name__ == "__main__":
    @rate_limited(2.0)
    def hello(name: str) -> str:
        """Say hello to somebody."""
        return f"hello {name}"

    t0 = time.perf_counter()
    for n in ["a", "b", "c", "d"]:
        hello(n)
    elapsed = time.perf_counter() - t0

    assert hello.__name__ == "hello", hello.__name__
    assert elapsed >= 1.4, f"4 calls at 2/sec should take ~1.5s, took {elapsed:.2f}s"
    print(f"4 calls took {elapsed:.2f}s -- all checks passed")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-08-apis-json/homework/problem-03-rate-limit-decorator.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `@rate_limited(2.0)` allows at most two calls per second: the first call
   is immediate, and each later call sleeps until a full interval has passed
   since the previous one started.
2. A call that arrives *after* the interval has already passed does not sleep
   at all — the limiter only ever adds the missing part of the gap.
3. The wrapper preserves the wrapped function's `__name__` and `__doc__`
   via `functools.wraps`.
4. Two separately decorated functions keep separate schedules — limiting
   `fetch_users` must not slow down `fetch_repos`.
5. `rate_limited(0)` and negative rates raise `ValueError` at decoration
   time, not at call time.
6. The docstring states the single-threaded limitation in your own words.
7. The wrapped function's arguments and return value pass through unchanged —
   any arguments, any return type.

## Constraints

- **`time.perf_counter()`, not `time.time()`.** `time.time()` is the wall
  clock, and the wall clock is allowed to jump — NTP adjustments, daylight
  saving, a user fixing their laptop's date. A backwards jump turns your
  arithmetic into a negative gap and a sleep of several minutes.
  `perf_counter` is a **monotonic** clock: it only moves forward, its zero
  point means nothing, and differences between readings are exactly what it
  is for.

- **Sleep only the remainder, never the whole interval.** If 0.3s of a 0.5s
  interval has already passed while your program did other work, the limiter
  owes 0.2s more, not 0.5s. Sleeping the full interval every time makes the
  limiter roughly twice as slow as the API allows, which is politeness
  curdled into waste.

- **Refuse a nonsense rate immediately.** `1.0 / 0` raises
  `ZeroDivisionError` deep inside your machinery, at decoration time, with a
  traceback that points at an arithmetic line instead of at the caller's
  mistake. Raise `ValueError` with a message that names the actual problem.
  Fail at the door, not in the kitchen.

- **The demo run must not actually wait.** The shipped answer's checks cover
  gaps that would take seconds of real sleeping — and take none, because the
  decorator accepts its clock and its sleep as parameters. Your own version
  can start with real `time.sleep` and real waiting; the solution shows what
  the parameters buy.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-rate-limit-decorator-solution.py
ok  four calls at 2/sec slept [0.5, 0.5, 0.5], total 1.5s
ok  wrapper kept its name ('greet') and its docstring
ok  a call that arrives late enough does not sleep
ok  half a call per second waits 2.0s between calls
ok  two wrapped functions do not share a schedule
ok  rate_limited(0) raised ValueError: calls_per_second must be greater than zero

6 checks passed, and not one real second was spent waiting.
```

The last line is not a joke; it is the point. Those checks include a
two-second gap and three half-second gaps, and the whole run finishes in
milliseconds, because the clock in the test is a fake that jumps instead of
waiting. Your own starter version, using real time, will genuinely take about
1.5 seconds — that is fine, and watching it wait once is worth it.

## Steps

1. Copy the starter into `hw03_rate_limit.py` and run it. The timing assert
   fails in well under 1.5 seconds — the wrapper is not waiting yet.
2. Write the guard: `calls_per_second <= 0` raises `ValueError`.
3. Give the closure its memory. The wrapper needs to read and update a
   last-call time that survives between calls — a one-element list, or a
   `nonlocal` variable. (Why a plain variable fails is bug two, below.)
4. Write the gap logic: `wait = interval - (now - previous)`; sleep only if
   `wait > 0`; record the new last-call time. Run it — the four calls should
   now take about 1.5 seconds.
5. Check requirement 3: print `hello.__name__`. If it says `wrapper`, you
   forgot `functools.wraps`.
6. Decorate a second function and interleave calls to both — the schedules
   must be independent (requirement 4). If limiting one slows the other, your
   last-call memory is in the wrong layer; see bug three.
7. Optional but worth it: add `clock=` and `sleep=` parameters like the
   shipped answer, hand in a fake, and watch your tests finish instantly.

## The Solution

```python
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
```

**Three layers, and each one exists for a reason.** `rate_limited(2.0)` runs
once and turns the rate into an interval — that is the factory.
`decorate(function)` runs once per decorated function and owns that
function's memory — that is the decorator. `wrapper(*args, **kwargs)` runs on
every call and does the actual waiting. The `@rate_limited(2.0)` syntax is
just those first two called in a row: Python evaluates `rate_limited(2.0)` to
get a decorator, then feeds `greet` to it.

**The memory lives in `decorate`, and that placement *is* requirement 4.**
`last_call` is created fresh each time `decorate` runs, so every decorated
function gets its own — which is why check 5 passes and limiting one function
does not slow another. Hoist it up into `rate_limited` and all functions
sharing one decorator share one schedule; push it into `wrapper` and it
resets on every call, remembering nothing. Where you put a closure variable
decides what it means.

**A one-element list, because closures can read but not rebind.** The wrapper
can *read* `last_call` from the enclosing scope freely, but plain assignment
(`last_call = ...`) would create a new local instead — Python decides
local-versus-enclosing at compile time, by looking for assignments. Mutating
the list (`last_call[0] = ...`) is not an assignment to the name, so it
works. The other spelling is `nonlocal last_call` with a plain
`float | None` variable — same meaning, and either is fine. What is *not*
fine is discovering this the hard way via `UnboundLocalError`; that is bug
two below.

**The gap arithmetic is one honest line.**
`wait = interval - (clock() - previous)` — how much of the interval remains
after subtracting what has already passed. If the answer is zero or negative,
the world already waited for you; sleep nothing. Note also *when* the clock
is read for the record: after the sleep, at the moment the call actually
goes through. Recording before the sleep would make the next call measure
from the wrong start and under-wait.

**`clock` and `sleep` are the network seam from Exercise 1, aimed at time.**
The decorator never says `time.sleep` in its body; it says *the sleep it was
given*, which defaults to the real one. So `FakeClock` can play both roles —
`now` reads a private timeline, `sleep` advances it and writes down how long
it was asked to wait — and the checks become exact: `fake.slept == [0.5,
0.5, 0.5]` is a statement no stopwatch could ever make. Testing against real
time gives you `elapsed >= 1.4` and a slow test; testing against a fake gives
you equality and an instant one.

**`functools.wraps` is one line that protects every tool downstream.**
Without it, `greet.__name__` is `'wrapper'`, `help(greet)` shows the
wrapper's docstring or nothing, and a traceback through the wrapper names a
function that appears nowhere in your code. `wraps` copies the wrapped
function's identity onto the wrapper — and tucks the original away as
`greet.__wrapped__`, which is how debuggers dig the real function back out.

## Download and run

Download
[problem-03-rate-limit-decorator-solution.py](./problem-03-rate-limit-decorator-solution.py)
and run it:

```bash
python problem-03-rate-limit-decorator-solution.py
```

It needs nothing installed, never touches the network, and finishes
instantly — the waiting in its checks happens on a fake clock. To feel the
real thing once, decorate a print with `@rate_limited(2.0)` (no `clock=`, no
`sleep=` — the defaults are real time) and call it four times; the run takes
about a second and a half of genuine waiting.

The `-solution` in the filename keeps it from colliding with your own
`hw03_rate_limit.py`.

## Common bugs to catch

- **`@rate_limited` without the parentheses.**

  ```text
  Traceback (most recent call last):
    File "hw03_rate_limit.py", line 41, in <module>
      hello("a")
  TypeError: decorate() takes 1 positional argument but 2 were given
  ```

  `@rate_limited` hands the *function* to the factory — `hello` lands in
  `calls_per_second` and the layers are off by one. A parameterised decorator
  is always applied with a call: `@rate_limited(2.0)`.

- **`UnboundLocalError` from assigning the closure variable.**

  ```text
  UnboundLocalError: cannot access local variable 'last_call' where it is not associated with a value
  ```

  You wrote `last_call = clock()` inside the wrapper with `last_call` as a
  plain variable in `decorate`. The assignment makes Python treat
  `last_call` as a *local* of the wrapper everywhere in the wrapper —
  including the read that happens before the assignment. Fix: `nonlocal
  last_call`, or make the memory a mutable container and assign to
  `last_call[0]` instead.

- **The memory in the wrong layer.** In `rate_limited`: all decorated
  functions share one schedule, and check 5's assert fails with `[1.0]` —
  the second function slept for the first one's call. In `wrapper`: nothing
  is ever remembered, no call ever sleeps, and the four-call test finishes
  suspiciously fast. The layer that runs once per function is the layer
  that owns per-function state.

- **Sleeping the full interval instead of the remainder.** Every call pays
  `interval` even when most of it already passed. Symptom in the fake-clock
  test: `fake.slept == [0.5, 0.5, 0.5]` fails because a `tick` between calls
  did not reduce the sleep. Requirement 2 exists to catch exactly this.

- **`functools.wraps` forgotten.** `hello.__name__` prints `'wrapper'`. One
  decorator line above the wrapper fixes it. If you have never seen why it
  matters: put two undecorated wrappers in a stack trace and try to work out
  which is which.

- **`time.time()` for the gap.** Works on every machine where nothing
  adjusts the clock — then a laptop wakes from sleep, NTP steps the time
  back four seconds, `clock() - previous` goes negative, and
  `interval - (negative)` sleeps for longer than both numbers put together.
  Monotonic clocks exist because the wall clock is allowed to lie.

## Under the hood

<details>
<summary>Under the hood — fixed gap versus token bucket, and what real APIs do</summary>

The limiter on this page enforces a **fixed gap**: at 2/sec, calls run at
0.0s, 0.5s, 1.0s — a metronome. Simple, predictable, and it never exceeds
the rate even briefly. But it also refuses harmless bursts: a client that
was idle for an hour still may not make two quick calls back to back.

Most real services use a **token bucket** instead. The bucket holds up to
`burst` tokens; tokens drip in at the allowed rate; each call spends one.
An idle client's bucket fills up, so short bursts go through at full speed,
and only *sustained* traffic gets slowed to the drip rate:

```python
def token_bucket(rate: float, burst: int, *, clock=time.perf_counter, sleep=time.sleep):
    tokens = float(burst)
    updated = clock()

    def acquire() -> None:
        nonlocal tokens, updated
        now = clock()
        tokens = min(burst, tokens + (now - updated) * rate)
        updated = now
        if tokens < 1.0:
            sleep((1.0 - tokens) / rate)
            tokens = 1.0
            updated = clock()
        tokens -= 1.0

    return acquire
```

Same seam — the clock and the sleep are parameters — so it tests the same
instant way.

The other half of real-world rate limiting is the server's, and you met it
in [Exercise 4's Under the hood](../exercises/exercise-04-pagination.md):
`X-RateLimit-Remaining` counts down your budget, and when you overdraw it,
`429 Too Many Requests` arrives with a `Retry-After` header saying how long
to back off. A production client uses *both* halves: a local limiter shaped
like this page's, so it rarely hits 429 — and the retry policy from
Exercise 5, which respects `Retry-After` (`respect_retry_after_header=True`
in that exercise's `make_session`) for the times it hits one anyway. The
local limiter is courtesy; handling 429 is correctness. Neither replaces
the other.

Why per-*start* gaps rather than per-finish, one subtlety worth having
seen: this limiter measures from when the previous call *began*, so a slow
function eats into its own gap — at 2/sec, a call that takes 0.4s only
waits 0.1s more. Measuring finish-to-start would be stricter than the API
asked for; servers meter *request arrivals*, and starts are when requests
arrive.

</details>

<details>
<summary>Under the hood — what a decorator with arguments actually desugars to</summary>

The `@` syntax is precisely two rewrites, and seeing both makes the layer
count stop feeling mystical.

A bare decorator is one call:

```python
@wraps_nothing
def f(): ...
# is exactly
def f(): ...
f = wraps_nothing(f)
```

A decorator *with arguments* is two:

```python
@rate_limited(2.0)
def greet(): ...
# is exactly
def greet(): ...
greet = rate_limited(2.0)(greet)
```

`rate_limited(2.0)` runs first and must *return a decorator* — that is the
factory layer, and it is why the guard raises at decoration time: the
factory runs when the `def` is executed, long before any call. Then that
returned decorator is applied to `greet`, and whatever *it* returns is
bound to the name `greet` forever after. Every call to `greet` from then on
is really a call to `wrapper`.

The closure is what keeps the layers alive after they return. `wrapper`
mentions `interval`, `clock`, `sleep`, `last_call` — names belonging to
enclosing functions that have already finished. Python keeps them alive in
`greet.__closure__`, one cell per captured name:

```text
>>> greet.__wrapped__          # the original, kept by functools.wraps
<function greet at 0x...>
>>> [c.cell_contents for c in greet.__closure__]
[<function greet at 0x...>, 0.5, <built-in function perf_counter>, ...]
```

That list is the decorator's entire "object state" — a closure is an
object whose fields are spelled variables. Week 7 built the same machinery
with a class and `__call__`; a closure is the lighter spelling for when
there is only one method.

One habit worth the extra line in real code:
`wrapper.interval = interval` exposes the derived number for tests and
debugging. Attributes on functions feel odd the first time; they are just a
dict (`greet.__dict__`), and `functools.wraps` copies them too, which is
why the shipped answer can hang the interval on the wrapper and trust it to
survive.

</details>

## Acceptance checklist

- [ ] Four calls at `@rate_limited(2.0)` take about 1.5 seconds with real
      time — or exactly `[0.5, 0.5, 0.5]` of fake sleep if you built the
      seam.
- [ ] A call arriving after the interval has already passed does not sleep.
- [ ] `hello.__name__` is `'hello'` and its docstring survives.
- [ ] Two decorated functions do not share a schedule.
- [ ] `rate_limited(0)` raises `ValueError` before any function is wrapped.
- [ ] Arguments and return values pass through unchanged.
- [ ] The docstring names the single-threaded limitation.
- [ ] Committed with a message like `Add Week 8 homework 3: rate limiter`.

## Stretch

- Build the token bucket from Under the hood with a `burst=` parameter, keep
  the `clock=`/`sleep=` seam, and write a fake-clock test proving a burst of
  three goes through instantly after an idle stretch while the fourth call
  waits.

- Add a `retries` companion: catch `429` in a wrapped `requests` call, read
  `Retry-After`, sleep that long, and try again — then compare what you wrote
  with what `Retry(respect_retry_after_header=True)` gave you for free in
  [Exercise 5](../exercises/exercise-05-handle-errors.md).

- Instrument it: make the wrapper count calls and total enforced sleep, and
  expose them as `wrapper.stats`. Run it over a loop of twenty calls and
  check the arithmetic against the rate by hand.

Once your limiter waits exactly as long as it should, move on to
[Homework Problem 4 — Mock API Client](./problem-04-mock-api-client.md).
