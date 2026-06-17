"""Exercise 04 — Safe divide with logging.

Topic: try/except, narrow excepts, the logging module.
Reference: lecture-notes/03-exceptions-and-logging.md sections 2, 4, 9.

Task
----
Implement `safe_divide(a, b)` so that:

  * On success, returns `a / b` as a float.
  * On `ZeroDivisionError` (b is zero), logs a WARNING and returns None.
  * On `TypeError` (one of the args is not a number), logs a WARNING
    and returns None.
  * Any *other* exception propagates normally — we never want to hide
    unexpected bugs.

Use the `logging` module (already configured below), NOT print(), for
the warnings. The log messages should include the offending values so a
debugging human can tell what went wrong.

Expected output (the order matters because logging goes to stderr):

    10 / 2 = 5.0
    10 / 0 = None
    'ten' / 2 = None
    7 / 2 = 3.5

You will also see WARNING lines from the logger above/below the prints,
depending on your terminal. That is normal.
"""

from __future__ import annotations

import logging
from typing import Optional, Union

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger(__name__)

Number = Union[int, float]


def safe_divide(a: Number, b: Number) -> Optional[float]:
    """Return a / b, or None on ZeroDivisionError / TypeError."""
    try:
        return a / b
    except ZeroDivisionError:
        log.warning("division by zero: %r / %r", a, b)
        return None
    except TypeError:
        log.warning("non-numeric operands: %r / %r", a, b)
        return None


if __name__ == "__main__":
    cases: list[tuple[Number, Number]] = [
        (10, 2),
        (10, 0),
        ("ten", 2),     # type: ignore[arg-type]   — intentional bad input
        (7, 2),
    ]
    for a, b in cases:
        result = safe_divide(a, b)
        print(f"{a!r} / {b!r} = {result}")
