"""Exercise 05 — Schedule.

Two implementations of the same idea: print "tick N" every 5 seconds.

Implementation A (default, stdlib only): a sleep loop with a counter.
Implementation B (--use-schedule): the `schedule` package.

Run:
    python exercise-05-schedule.py                 # uses stdlib loop
    pip install schedule
    python exercise-05-schedule.py --use-schedule  # uses schedule package

Press Ctrl-C to stop.

Stretch:
  1. Add a --count N option that stops after N ticks.
  2. Add a --interval SECONDS option (float).
  3. Replace `print` with the `logging` module and add a timestamp.
"""
from __future__ import annotations

import argparse
import sys
import time
from itertools import count


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Print 'tick N' every 5 seconds.")
    p.add_argument("--use-schedule", action="store_true",
                   help="Use the `schedule` package instead of a sleep loop")
    p.add_argument("--interval", type=float, default=5.0,
                   help="Seconds between ticks (default: 5)")
    p.add_argument("--count", type=int, default=0,
                   help="Stop after N ticks (default: 0 = run forever)")
    return p


def run_stdlib_loop(interval: float, max_ticks: int) -> None:
    """Plain sleep loop. Easy to reason about; no dependencies."""
    counter = count(1)
    while True:
        n = next(counter)
        print(f"tick {n}")
        if max_ticks and n >= max_ticks:
            break
        time.sleep(interval)


def run_schedule_loop(interval: float, max_ticks: int) -> None:
    """Use the `schedule` package."""
    try:
        import schedule  # type: ignore[import-not-found]
    except ImportError:
        print("schedule package not installed. Run: pip install schedule",
              file=sys.stderr)
        sys.exit(1)

    counter = count(1)
    state = {"done": 0}

    def tick() -> None:
        n = next(counter)
        print(f"tick {n}")
        state["done"] = n
        if max_ticks and n >= max_ticks:
            schedule.clear()

    schedule.every(interval).seconds.do(tick)

    # Run an immediate tick, then loop until cleared.
    tick()
    while schedule.jobs:
        schedule.run_pending()
        time.sleep(0.5)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.use_schedule:
            run_schedule_loop(args.interval, args.count)
        else:
            run_stdlib_loop(args.interval, args.count)
    except KeyboardInterrupt:
        print("\nstopped.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
