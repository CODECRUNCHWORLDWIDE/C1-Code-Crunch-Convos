"""Distance and speed trip report.

Week 2 homework, problem 6, Code Crunch Convos. Converts a trip in
kilometers and hours into speed, miles, and miles per hour.

Questions go to the error stream and the report goes to the normal output
stream. When nobody is at the keyboard the script uses the example trip.
Save your own copy as ``homework-06-distance-speed.py``.
"""

import sys

KM_PER_MILE: float = 1.609344
LABEL_WIDTH: int = 9
INPUT_WIDTH: int = 6
RESULT_WIDTH: int = 7

SAMPLE_KILOMETERS: str = "250"
SAMPLE_HOURS: str = "3.5"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def print_report(kilometers: float, hours: float) -> None:
    """Print the trip report, or the error line when ``hours`` is not positive."""
    if hours <= 0:
        print("Error: time must be positive.")
        return

    kph: float = kilometers / hours
    miles: float = kilometers / KM_PER_MILE
    mph: float = miles / hours

    print("--- Trip Report ---")
    print(f"{'Distance':<{LABEL_WIDTH}}:{kilometers:>{INPUT_WIDTH}.1f} km")
    print(f"{'Time':<{LABEL_WIDTH}}:{hours:>{INPUT_WIDTH}.1f} hours")
    print(f"{'Speed':<{LABEL_WIDTH}}:{kph:>{RESULT_WIDTH}.2f} km/h")
    print(f"{'In miles':<{LABEL_WIDTH}}:{miles:>{RESULT_WIDTH}.2f} mi")
    print(f"{'At MPH':<{LABEL_WIDTH}}:{mph:>{RESULT_WIDTH}.2f} mph")


def main() -> None:
    """Read distance and time, then print the trip report."""
    kilometers: float = float(ask("Distance in kilometers: ", SAMPLE_KILOMETERS))
    hours: float = float(ask("Time in hours: ", SAMPLE_HOURS))
    print_report(kilometers, hours)


if __name__ == "__main__":
    main()
