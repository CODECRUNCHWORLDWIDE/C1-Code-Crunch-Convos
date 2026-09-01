"""exercise-05-custom-exception-solution.py — parse a check-in log, reject bad lines loudly.

Defines a CheckInError family so callers can catch every parse failure with one
except clause and still learn exactly which line failed and why. Accepted rows
go to stdout; rejections go to stderr through the logging module.

The file you write yourself keeps its sample data in a ``data/`` folder next to
the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact check-in log the page
gives you, so the download runs on any machine with nothing set up beforehand.

Every accepted row is printed with flush=True so that a combined
`python ... 2>&1` transcript interleaves the way the page shows it, instead of
holding the report in a buffer until the program ends.

Run it with::

    python exercise-05-custom-exception-solution.py
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

FIELD_COUNT = 3

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(message)s")
log = logging.getLogger(__name__)

#: The check-in log exactly as the exercise page gives it. Line 4 has nothing
#: between the two pipes and line 5 has only two fields.
SAMPLE_CHECKINS = (
    "lagos|ada.lovelace@example.org|3\n"
    "manila|grace.hopper@example.org|1\n"
    "bogota|katherine.johnson@example.org|zero\n"
    "nairobi||2\n"
    "quito|alan.turing@example.org\n"
    "osaka|mary.jackson@example.org|-4\n"
)


class CheckInError(Exception):
    """Base class for every failure while parsing a check-in line."""

    def __init__(self, line_number: int, raw: str, message: str) -> None:
        super().__init__(f"line {line_number}: {message}")
        self.line_number = line_number
        self.raw = raw


class MalformedLineError(CheckInError):
    """Raised when a line does not split into exactly FIELD_COUNT fields."""


class MissingFieldError(CheckInError):
    """Raised when a required field is present but empty."""


class InvalidCountError(CheckInError):
    """Raised when the check-in count is not a non-negative whole number."""


def parse_line(line_number: int, raw: str) -> tuple[str, str, int]:
    """Parse one pipe-delimited check-in line.

    Returns:
        A ``(chapter, email, count)`` triple.

    Raises:
        MalformedLineError: wrong number of fields.
        MissingFieldError: chapter or email is empty.
        InvalidCountError: count is not a whole number, or is negative.
    """
    line = raw.rstrip("\n")
    fields = line.split("|")
    if len(fields) != FIELD_COUNT:
        raise MalformedLineError(
            line_number,
            line,
            f"expected {FIELD_COUNT} fields, found {len(fields)}",
        )
    chapter, email, count_text = fields
    if not chapter:
        raise MissingFieldError(line_number, line, "chapter is empty")
    if not email:
        raise MissingFieldError(line_number, line, "email is empty")
    try:
        count = int(count_text)
    except ValueError as e:
        raise InvalidCountError(
            line_number,
            line,
            f"check-in count {count_text!r} is not a whole number",
        ) from e
    if count < 0:
        raise InvalidCountError(
            line_number, line, f"check-in count {count} is negative"
        )
    return chapter, email, count


def parse_file(source: Path) -> None:
    """Parse every line of *source*, print the good ones, log the bad ones."""
    accepted = 0
    total = 0
    with source.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, start=1):
            total += 1
            try:
                chapter, email, count = parse_line(line_number, raw)
            except CheckInError as e:
                log.warning("rejected %s: %s", type(e).__name__, e)
                continue
            accepted += 1
            print(f"{chapter:<8} {email:<32} {count:>3}", flush=True)
    print(f"{accepted} of {total} lines accepted; {total - accepted} rejected")


def build_sample(folder: Path) -> Path:
    """Write the sample check-in log into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "checkins.txt"
    path.write_text(SAMPLE_CHECKINS, encoding="utf-8")
    return path


def main() -> None:
    """Build the sample check-in log and parse it."""
    with tempfile.TemporaryDirectory() as workspace:
        parse_file(build_sample(Path(workspace) / "data"))


if __name__ == "__main__":
    main()
