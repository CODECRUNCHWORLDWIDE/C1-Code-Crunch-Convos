"""exercise-05-schedule-solution.py — the interval scheduler, proven headless.

The exercise part is the starter with its TODOs filled in: run a job every
--every seconds, let it stop itself after --runs runs by returning
schedule.CancelJob, and handle Ctrl-C around the loop so the process exits 130
with no traceback.

Your own exercise-05-schedule.py ends in ``raise SystemExit(main())`` and you
stop it yourself with Ctrl-C. A published answer cannot wait for a keypress,
and it cannot print live timestamps or a live disk reading and still match a
recorded run — those change every second. So this file threads a clock and a
disk reading through ``make_job`` and ``main`` as seams (they default to the
real ``datetime.now`` and ``shutil.disk_usage``, so your own version does not
need them), and the demo injects a fixed clock and a fixed reading. It runs one
bounded schedule (which stops itself) and then drives the loop into a
KeyboardInterrupt to prove the handler. The scheduler being tested is identical
either way.

Run it with::

    python exercise-05-schedule-solution.py
"""

from __future__ import annotations

import argparse
import shutil
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path

import schedule

POLL_SECONDS = 1.0
EXIT_INTERRUPTED = 130


def positive_int(value: str) -> int:
    """Parse a string as a whole number greater than zero."""
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError(f"must be a positive whole number, got {n}")
    return n


def free_gigabytes(where: Path) -> float:
    """Return the free space at `where` in gigabytes."""
    return shutil.disk_usage(where).free / 1e9


def make_job(limit: int, state: dict[str, int], *,
             clock: Callable[[], datetime] = datetime.now,
             disk: Callable[[Path], float] = free_gigabytes) -> Callable[[], object]:
    """Build the job callable.

    `state["runs"]` counts completed runs. When `limit` is greater than zero
    and that many runs have happened, the job returns schedule.CancelJob so
    the scheduler drops it and the main loop can end. `clock` and `disk` are
    seams the demo overrides; your own version can leave them at their defaults.
    """
    def job() -> object:
        state["runs"] += 1
        run_number = state["runs"]
        gigabytes = disk(Path.cwd())
        print(f"[{clock():%H:%M:%S}] run {run_number}  "
              f"free disk {gigabytes:.1f} GB")
        if limit and run_number >= limit:
            return schedule.CancelJob
        return None

    return job


def main(argv: list[str] | None = None, *,
         clock: Callable[[], datetime] = datetime.now,
         disk: Callable[[Path], float] = free_gigabytes) -> int:
    """Schedule the job, run until it finishes or is interrupted."""
    parser = argparse.ArgumentParser(
        prog="disk-watch",
        description="Report free disk space on an interval.",
    )
    parser.add_argument("--every", type=positive_int, default=2,
                        help="Seconds between runs (default: %(default)s)")
    parser.add_argument("--runs", type=int, default=3,
                        help="Stop after this many runs, 0 for no limit (default: %(default)s)")
    args = parser.parse_args(argv)

    state = {"runs": 0}
    schedule.every(args.every).seconds.do(make_job(args.runs, state, clock=clock, disk=disk))

    tail = f"stopping after {args.runs} run(s)" if args.runs else "running until stopped"
    print(f"scheduler started: every {args.every}s, {tail}, Ctrl-C to stop")

    try:
        while schedule.get_jobs():
            schedule.run_pending()
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print()
        print(f"stopped by user after {state['runs']} run(s)")
        return EXIT_INTERRUPTED

    print(f"all {state['runs']} run(s) complete")
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — a fixed clock and a fixed disk reading, a bounded run
# that stops itself, and a driven KeyboardInterrupt to prove the handler.
# Your own file has no demo; you run it from the shell and stop it with Ctrl-C.
# --------------------------------------------------------------------------- #

FIXED_DISK_GB = 128.0


def fixed_clock(start: datetime, step_seconds: int) -> Callable[[], datetime]:
    """A clock that returns *start*, then advances *step_seconds* each call."""
    state = {"t": start}

    def now() -> datetime:
        current = state["t"]
        state["t"] = current + timedelta(seconds=step_seconds)
        return current

    return now


def demo() -> None:
    """Run a bounded schedule, then interrupt one, both with fixed readings."""
    disk = lambda where: FIXED_DISK_GB  # noqa: E731 - a one-line stub for the demo
    base = datetime(2026, 1, 1, 7, 0, 0)

    print("Schedule — the interval scheduler, driven headless.")
    print()

    print("A bounded run that stops itself after --runs:")
    schedule.clear()
    code = main(["--every", "2", "--runs", "3"], clock=fixed_clock(base, 2), disk=disk)
    print(f"[exit {code}]")
    print()

    print("Ctrl-C is honoured around the loop — no traceback, exit 130:")
    schedule.clear()
    real_sleep = time.sleep
    calls = {"n": 0}

    def fake_sleep(seconds: float) -> None:
        # Let real time pass so two runs fire at the 2s interval, then interrupt
        # from inside the loop's own sleep, exactly where a real Ctrl-C lands.
        calls["n"] += 1
        if calls["n"] > 5:
            raise KeyboardInterrupt
        real_sleep(seconds)

    time.sleep = fake_sleep
    try:
        code = main(["--every", "2", "--runs", "0"], clock=fixed_clock(base, 2), disk=disk)
    finally:
        time.sleep = real_sleep
    print(f"[exit {code}]")


if __name__ == "__main__":
    demo()
