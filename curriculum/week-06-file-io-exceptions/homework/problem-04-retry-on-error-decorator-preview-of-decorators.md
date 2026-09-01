# Homework Problem 4 — Retry-On-Error Decorator (Preview Of Decorators)

> **Topic:** wrapping a function so it tries again, and knowing which failures deserve a second try
> **Lecture:** [Lecture 03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** you have not been taught decorators yet, and you are about to write one anyway. Copy the shape, then read what each layer is for. The real lesson underneath is that a blip and a bug are different things, and the `except` line is where you say which is which.

## The Brief

Some failures are worth trying again. The network hiccuped. The service
was restarting. Wait a second, ask again, and it works.

Some failures are not. You spelled a variable wrong. Asking again will
misspell it again, forever.

You are writing the thing that tells those two apart. It is a
**decorator** — a function that takes another function and gives back a
replacement with extra behaviour wrapped around it.

```python
@retry(FlakyServiceError, attempts=3)
def fetch_token() -> str:
    ...
```

Now `fetch_token` behaves like this:

- Call the real function.
- If it raises `FlakyServiceError`, log a WARNING and try again. Up to
  three tries in total.
- On the third failure, give up and let the exception out.
- If it raises **anything else**, do not retry at all. Let it out
  immediately.

Then show it working. Write a function that fails the first two times
and succeeds on the third, call it, and print the result.

You have not formally learned decorators. That is fine — copy the syntax
from the Starter and read the explanation after it works. The `@` line is
not magic; it is a function call whose result replaces your function.

## Starter

Save this as `retry.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — the decorator does nothing yet, so the first
failure escapes:

```python
"""Retry a function when it raises a particular exception."""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

log = logging.getLogger("retry")

F = TypeVar("F", bound=Callable[..., Any])


def retry(exc_type: type[Exception], attempts: int = 3) -> Callable[[F], F]:
    """Decorator: retry the wrapped function up to `attempts` times if `exc_type` is raised."""

    def decorate(func: F) -> F:
        """Wrap `func` in the retry loop, keeping its name and docstring."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Call the wrapped function, retrying on `exc_type`."""
            # TODO: loop `attempts` times
            # TODO:   try to return func(*args, **kwargs)
            # TODO:   on exc_type, re-raise if this was the last attempt,
            # TODO:   otherwise log a WARNING and go round again
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorate


class FlakyServiceError(Exception):
    """Stand-in for a transient network or service failure."""


_calls = 0


@retry(FlakyServiceError, attempts=3)
def fetch_token() -> str:
    """Fail the first two times it is called, then succeed."""
    global _calls
    _calls += 1
    if _calls < 3:
        raise FlakyServiceError(f"service unavailable (call {_calls})")
    return f"token-abc123 (after {_calls} calls)"


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")
    print(fetch_token())
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-04-retry-on-error-decorator-preview-of-decorators.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `retry(exc_type, attempts=3)` returns a decorator.
2. The wrapped function is called up to `attempts` times in total.
3. A failure that is an `exc_type` and is not the last attempt logs a
   WARNING and is followed by another try.
4. The last failure re-raises the exception to the caller.
5. Any exception that is not an `exc_type` propagates immediately, with
   no retry and no warning.
6. `functools.wraps` keeps the wrapped function's name and docstring.
7. A demonstration function fails twice and succeeds on the third call,
   and its result is printed.
8. Every function has type hints and a docstring.

## Constraints

- **`raise` on its own, never `raise e`.** Inside an `except` block a
  bare `raise` re-throws the exception currently being handled, with its
  original traceback intact. `raise e` re-throws the same object but
  resets the traceback to that line, so the report points at your
  decorator instead of the line inside the function that actually broke.
- **`except exc_type`, not `except Exception`.** Requirement 5 costs you
  zero lines if you catch the type you were given: an exception that is
  not an `exc_type` simply does not match the clause and flies straight
  out. Catch `Exception` and you have built a machine that retries your
  typos three times.
- **Re-raise on the last attempt, do not fall out of the loop.** A
  wrapper that runs out of attempts and reaches the end of its own body
  returns `None`. The caller gets something that looks like data. This
  is the single most common bug in this problem.
- **The warning goes before the next try, not after the last failure.**
  There is nothing to announce when nothing is being retried. Check for
  the last attempt at the *top* of the `except`, before you log.
- **`functools.wraps` is not decoration.** Without it every log line
  this decorator emits says `wrapper failed on attempt 1/3`, which
  defeats a decorator whose entire purpose is diagnostics.

## Expected output

This problem touches no files at all, so the shipped answer runs
anywhere as downloaded:

```bash
$ python problem-04-retry-on-error-decorator-preview-of-decorators-solution.py
```

```text
token-abc123 (after 3 calls)
gave up: FlakyServiceError: service is down for good
propagated immediately: ValueError: this is a bug, not a blip
fetch_token.__name__ is still 'fetch_token'
```

Those four lines are the four requirements, one each. The warnings that
went with them are not in that block because they went to stderr:

```console
WARNING  retry  fetch_token failed on attempt 1/3 (FlakyServiceError: service unavailable (call 1)); retrying
WARNING  retry  fetch_token failed on attempt 2/3 (FlakyServiceError: service unavailable (call 2)); retrying
WARNING  retry  always_broken failed on attempt 1/3 (FlakyServiceError: service is down for good); retrying
WARNING  retry  always_broken failed on attempt 2/3 (FlakyServiceError: service is down for good); retrying
```

Count them, because the counts are the proof:

- `fetch_token` warns **twice** and then returns. Three tries, two of
  them failures, so two "retrying" messages.
- `always_broken` also warns **twice** — not three times. The third
  failure is the re-raise, and it does not announce a retry that is not
  happening.
- `wrong_error` produces **no** warning at all. `ValueError` never
  matched the `except`.
- `fetch_token.__name__` is `'fetch_token'`, not `'wrapper'`.

To see the two streams interleaved in the order they really happened,
run it with `python -u`, which turns off the block buffering that
otherwise moves stdout lines around when the output is captured.

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `retry.py` and run it. It fails on the first call
   with `FlakyServiceError: service unavailable (call 1)`, because the
   wrapper is still a pass-through.
3. Replace the body of `wrapper` with a loop:

   ```python
   for attempt in range(1, attempts + 1):
       try:
           return func(*args, **kwargs)
       except exc_type as e:
           ...
   ```

   The `return` inside the `try` is what makes a success end the loop.
4. Inside the `except`, the first line is the one people get wrong.
   Write it first: `if attempt == attempts: raise`. Then, below it, the
   `log.warning` call.
5. Run it. You want two warnings and then `token-abc123 (after 3
   calls)`.
6. Add a second function that always fails, call it inside a
   `try` / `except FlakyServiceError`, and print what you caught. Two
   warnings, then your message.
7. Add a third that raises `ValueError`. Call it the same way. **No**
   warnings at all — that is requirement 5 proving itself.
8. Print `fetch_token.__name__` at the end. If it says `wrapper`, you
   left out `functools.wraps`.
9. Guard the argument: `if attempts < 1: raise ValueError(...)` at the
   top of `retry`. That makes `@retry(SomeError, attempts=0)` fail when
   the file is imported, rather than the first time that code path runs
   in front of a user.
10. Compare against **The Solution**, work down the acceptance
    checklist, and commit: `git add homework/retry.py` then
    `git commit -m "Week 6 homework: retry decorator"`.

## The Solution

```python
"""Homework 4 — retry-on-error decorator.

`retry(exc_type, attempts)` re-runs the wrapped function when it raises
`exc_type`, logging a WARNING between tries and re-raising on the last one.
Any other exception type propagates immediately.

    python retry.py

This one touches no files at all, so it runs anywhere as downloaded.

Save your own copy as ``retry.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

log = logging.getLogger("retry")

F = TypeVar("F", bound=Callable[..., Any])


def retry(exc_type: type[Exception], attempts: int = 3) -> Callable[[F], F]:
    """Decorator: retry the wrapped function up to `attempts` times if `exc_type` is raised.

    Args:
        exc_type: The exception type that counts as a retryable blip.
        attempts: How many tries in total, including the first.

    Returns:
        A decorator that wraps a function in the retry loop.

    Raises:
        ValueError: If *attempts* is less than 1.
    """
    if attempts < 1:
        raise ValueError(f"attempts must be at least 1, got {attempts}")

    def decorate(func: F) -> F:
        """Wrap *func* in the retry loop, keeping its name and docstring."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Call the wrapped function, retrying on *exc_type*."""
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exc_type as e:
                    if attempt == attempts:
                        raise
                    log.warning(
                        "%s failed on attempt %d/%d (%s: %s); retrying",
                        func.__name__,
                        attempt,
                        attempts,
                        type(e).__name__,
                        e,
                    )
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper  # type: ignore[return-value]

    return decorate


# --------------------------------------------------------------------------- #
# Demonstration
# --------------------------------------------------------------------------- #
class FlakyServiceError(Exception):
    """Stand-in for a transient network or service failure."""


_calls = 0


@retry(FlakyServiceError, attempts=3)
def fetch_token() -> str:
    """Fail the first two times it is called, then succeed."""
    global _calls
    _calls += 1
    if _calls < 3:
        raise FlakyServiceError(f"service unavailable (call {_calls})")
    return f"token-abc123 (after {_calls} calls)"


@retry(FlakyServiceError, attempts=3)
def always_broken() -> str:
    """Always fails, to show the final re-raise."""
    raise FlakyServiceError("service is down for good")


@retry(FlakyServiceError, attempts=3)
def wrong_error() -> str:
    """Raises something the decorator was not told about: no retry."""
    raise ValueError("this is a bug, not a blip")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-8s %(name)s  %(message)s")

    print(fetch_token())

    try:
        always_broken()
    except FlakyServiceError as e:
        print(f"gave up: {type(e).__name__}: {e}")

    try:
        wrong_error()
    except ValueError as e:
        print(f"propagated immediately: {type(e).__name__}: {e}")

    print(f"fetch_token.__name__ is still {fetch_token.__name__!r}")
```

**Why it works.**

**`return` inside the `try` is the loop's exit.** A successful call
returns straight out of `wrapper`, so the loop never sees a second
iteration. The loop only continues when the `except` catches, which is
exactly when another try is wanted.

**`if attempt == attempts: raise` sits at the top of the `except`, and
the order is the whole trick.** On the final failure it re-raises before
the warning is written, so nothing announces a retry that is not going to
happen. Getting this one line in the wrong order is the off-by-one that
makes this problem interesting.

**The bare `raise` keeps the traceback.** It re-throws the exception
being handled with its original stack, so the report points at the line
inside `fetch_token` that broke. `raise e` re-throws the same object
with a new traceback starting at your decorator, which is exactly the
information you did not need.

**`except exc_type` gives you requirement 5 for free.** There is no
`else`, no second check, no `isinstance`. A `ValueError` raised inside a
function decorated for `FlakyServiceError` simply does not match the
clause, so it leaves `wrapper` on the first call. That is the argument
for expressing intent in the *type* you catch rather than in logic
inside a broad handler.

**`functools.wraps` stops the function lying about itself.** It copies
`__name__`, `__doc__`, `__module__`, `__qualname__` and `__dict__`, and
sets `__wrapped__` so tools can find the original. Without it,
`fetch_token.__name__` is `"wrapper"`, `help(fetch_token)` shows the
wrapper's docstring, every warning this decorator emits names `wrapper`,
and a test runner reports the wrong test names. The last line of the
demonstration exists to prove it did its job.

**`raise AssertionError("unreachable")` after the loop.** The loop
cannot fall through — every path either returns or raises. A type
checker cannot see that, and without a final statement `wrapper` has an
implicit `return None` hiding at the bottom. The explicit raise writes
the invariant down and turns "impossible" into a loud failure if
somebody later edits the loop. The first entry under **Common bugs to
catch** is exactly that silent `None`.

**Checking `attempts` in `retry` itself, not in `wrapper`.** `retry`
runs once, when Python reads the `@` line. So
`@retry(SomeError, attempts=0)` fails at import, while you are still
looking at the file, instead of the first time that path runs in
production.

## Download and run

Download [problem-04-retry-on-error-decorator-preview-of-decorators-solution.py](./problem-04-retry-on-error-decorator-preview-of-decorators-solution.py)
and run it:

```bash
python problem-04-retry-on-error-decorator-preview-of-decorators-solution.py
```

It reads and writes no files, so it runs from anywhere with nothing set
up. Use `python -u` if you want the warnings and the results interleaved
in the order they really happened.

Save your own copy as `retry.py` in your homework folder, and commit that
one. The longer download name is there so it cannot overwrite your work.

## Common bugs to catch

- **Swallowing the final failure.** By far the most common version of
  this answer:

  ```python
  def wrapper(*a, **kw):
      for i in range(attempts):
          try:
              return func(*a, **kw)
          except exc_type as e:
              log.warning("attempt %d failed: %s", i + 1, e)
  ```

  ```text
  WARNING  retry  attempt 1 failed: service is down for good
  WARNING  retry  attempt 2 failed: service is down for good
  WARNING  retry  attempt 3 failed: service is down for good
  result is None
  ```

  Look at the last line. When every attempt fails the loop ends, the
  function falls off the bottom, and Python returns `None`. The caller
  gets a value that looks like data. Three warnings scrolled past on
  stderr and the program carried on with `None` in a variable that was
  supposed to hold a token — which surfaces fifty lines later as
  `TypeError: 'NoneType' object is not subscriptable` and takes an hour
  to trace back here.
- **Three warnings instead of two.** Logging first and checking for the
  last attempt afterwards. The count is always `attempts - 1`, because
  a warning means "going round again".
- **`except Exception:` instead of `except exc_type:`.** Retries the
  typo in your function three times before giving up, and breaks
  requirement 5 outright. A bug is not transient.
- **`raise e` instead of bare `raise`.** It works. The traceback now
  starts at your decorator, and the frames inside the function that
  failed — the ones that would have told you what broke — are gone.
- **Forgetting `functools.wraps`.**

  ```text
  >>> fetch_token.__name__
  'wrapper'
  ```

  Every diagnostic the decorator emits now names `wrapper`, and since
  the point of this decorator is diagnostics, the omission defeats it.
- **Only two levels of function.** Writing `def retry(func):` directly,
  because that is the shape of a decorator you have seen before. Then
  `attempts` has nowhere to live. A decorator that takes arguments needs
  three levels, and the Under the hood block below walks through why.

## Under the hood

<details>
<summary>Under the hood — the three levels of a decorator that takes arguments</summary>

The confusion here is almost always about **which level runs when**.

```text
retry(FlakyServiceError, attempts=3)   -> runs once, when Python reads the @ line.
                                          Captures exc_type and attempts.
   decorate(func)                      -> runs once, immediately after, with the
                                          function object. Returns the replacement.
      wrapper(*args, **kwargs)         -> runs on every call. Contains the loop.
```

Start with the version you have seen, which takes no arguments:

```python
def shout(func):
    def wrapper(*args, **kwargs):
        print("about to call", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@shout
def greet(name): ...
```

`@shout` means, precisely, `greet = shout(greet)`. Two levels: the
decorator, and the wrapper it returns.

Now look at what `@retry(FlakyServiceError, attempts=3)` means. There
are parentheses after `retry`, so that line is a **call**. It happens
first, and *its result* is used as the decorator:

```python
fetch_token = retry(FlakyServiceError, attempts=3)(fetch_token)
```

Read that right to left and the layers appear. `retry(...)` returns
`decorate`. `decorate(fetch_token)` returns `wrapper`. `wrapper` is
what the name `fetch_token` now points at.

So the third level exists to hold the arguments. `exc_type` and
`attempts` are ordinary local variables of `retry`, and the inner
functions can still see them long after `retry` has returned. That is a
**closure**: a function that remembers the variables of the place it was
defined, not just the ones passed to it.

```text
>>> fetch_token.__closure__ is not None
True
>>> fetch_token.__wrapped__.__name__      # functools.wraps left a way back
'fetch_token'
```

Three practical consequences:

**Decoration happens at import time.** Everything outside `wrapper` runs
once, when the module is read. That is why validating `attempts` in
`retry` catches a bad value immediately.

**`wrapper` must take `*args, **kwargs`.** It stands in for a function
whose signature it does not know. Anything narrower breaks the moment
somebody decorates a function that takes an argument.

**Stacking decorators applies them bottom-up.**

```python
@log_calls
@retry(FlakyServiceError)
def fetch(): ...
```

`retry` wraps `fetch` first, then `log_calls` wraps *that*. The one
nearest the `def` is the innermost.

</details>

<details>
<summary>Under the hood — why real retries wait, and what happens when they do not</summary>

This brief does not ask for a delay, and the answer does not have one.
Real retry code always does, and the reason is worth understanding
before you write one at work.

A service that is failing is usually failing because it is overloaded.
Three instant retries from your program mean three times the load, at
the worst possible moment. Multiply by a thousand clients all retrying
instantly and you have a **thundering herd** — the retries themselves
keep the service down.

The standard fix has two parts:

```python
import random
import time

delay = base * (2 ** (attempt - 1))     # exponential backoff
time.sleep(delay * random.uniform(0.5, 1.5))   # jitter
```

**Backoff** doubles the wait after each failure: 1 second, 2, 4, 8. A
service that needs thirty seconds to restart gets thirty seconds,
without you having to know that in advance.

**Jitter** — the random smear — is the part people leave out and should
not. Without it, a thousand clients that all failed at the same instant
all retry at the same instant, and the herd is still thundering, just on
a timer. Spreading each client's wait randomly around the target breaks
the synchronisation.

Two more rules that come from the same place:

**Do not retry something that is not safe to repeat.** Reading a value
twice is harmless. Charging a card twice is not. A request that can be
repeated without changing the result is called **idempotent**, and only
idempotent operations should be retried automatically. Everything else
needs the retry to carry an identifier so the far end can recognise the
repeat and ignore it.

**Cap the total, not just the count.** Three attempts with exponential
backoff can take a long time. Real clients also carry a deadline, and
give up when it passes even if attempts remain.

Adding backoff to your answer is a one-line change, and worth doing once
so the shape is in your hands:

```python
except exc_type as e:
    if attempt == attempts:
        raise
    log.warning(...)
    time.sleep(2 ** (attempt - 1))
```

</details>

## Acceptance checklist

- [ ] `python retry.py` prints the successful token after two warnings.
- [ ] A function that always fails produces `attempts - 1` warnings and
      then raises to the caller.
- [ ] A function that raises a different exception type produces zero
      warnings and raises immediately.
- [ ] The wrapper re-raises on the last attempt rather than returning
      `None`.
- [ ] The re-raise is a bare `raise`, not `raise e`.
- [ ] `functools.wraps` is applied, and `fetch_token.__name__` proves it.
- [ ] `attempts=0` raises a `ValueError` when the file is imported.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like `Week 6 homework: retry decorator`.

## Stretch

- **Add exponential backoff.** `time.sleep(2 ** (attempt - 1))` before
  the next try. Then add jitter, as the second Under the hood block
  describes, and write two sentences on why the random part matters.
- **Accept a tuple of exception types.** `except` already takes a tuple,
  so `retry((TimeoutError, ConnectionError))` needs no change at all
  except the type hint. Check that, then fix the hint.
- **Add an `on_retry` callback.** A function called with the attempt
  number and the exception, so the caller decides what a retry means —
  log it, count it, report it to a dashboard. This is how real libraries
  stay useful without knowing anything about your program.
- **Count the attempts on the wrapper.** Set `wrapper.attempts_used`
  after the loop so a caller can ask how much work that took. Notice you
  can attach attributes to a function object at all, which is a strange
  and useful fact.
- **Break it on purpose.** Take out `functools.wraps` and re-run.
  Compare the warning lines before and after. Then take out the
  `if attempt == attempts: raise` and print the result. Both failures
  are instructive precisely because neither one crashes.

Next: [Homework Problem 5 — File Watcher](./problem-05-file-watcher-poll-based.md).
