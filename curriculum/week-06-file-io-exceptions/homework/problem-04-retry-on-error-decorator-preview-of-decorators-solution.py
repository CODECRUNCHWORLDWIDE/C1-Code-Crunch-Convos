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
