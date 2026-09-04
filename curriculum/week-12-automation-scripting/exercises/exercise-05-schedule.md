# Exercise 5 — Schedule

> **Topic:** the `schedule` package, a `time.sleep` poll loop, and stopping cleanly
> **Lecture:** [03 — Scraping and Scheduling](../lecture-notes/03-scraping-and-scheduling.md)
> **Difficulty:** Easy
> **Target time:** 25 min
> **Why this one:** a script that runs forever is a script you have to be able to stop. Every long-running thing you write from here on — the website watcher in Challenge 1, the file organizer in the mini-project — needs an exit that leaves the terminal usable and the exit code honest. Ctrl-C handling is four lines. Learn them on a job that does nothing important.

## The Brief

Build a small recurring job runner. Every few seconds it wakes up, checks how
much free space is left on your disk, and prints a timestamped line. It stops
after a number of runs you choose, or the moment you press Ctrl-C.

The job itself is deliberately boring — `shutil.disk_usage` from Lecture 2,
one line of output. The exercise is the shell around it: scheduling the job,
letting it stop itself, and handling the interrupt. Keep the runs short, three
runs a couple of seconds apart, so the whole thing finishes in under ten
seconds. A scheduler you have to wait fifteen minutes to test is a scheduler
you will not test.

## Starter

```bash
pip install schedule
```

```python
"""exercise-05-schedule.py — run a small job on an interval and stop cleanly.

Reports free disk space every --every seconds, stopping after --runs runs
or on Ctrl-C.
"""

from __future__ import annotations

import argparse
import shutil
import time
from collections.abc import Callable
from datetime import datetime
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


def make_job(limit: int, state: dict[str, int]) -> Callable[[], object]:
    """Build the job callable.

    `state["runs"]` counts completed runs. When `limit` is greater than zero
    and that many runs have happened, the job returns schedule.CancelJob so
    the scheduler drops it and the main loop can end.
    """
    def job() -> object:
        # TODO: increment state["runs"]
        # TODO: print f"[{datetime.now():%H:%M:%S}] run {n}  free disk {gb:.1f} GB"
        # TODO: return schedule.CancelJob once the limit is reached
        raise NotImplementedError

    return job


def main(argv: list[str] | None = None) -> int:
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
    schedule.every(args.every).seconds.do(make_job(args.runs, state))

    tail = f"stopping after {args.runs} run(s)" if args.runs else "running until stopped"
    print(f"scheduler started: every {args.every}s, {tail}, Ctrl-C to stop")

    try:
        # TODO: while schedule.get_jobs(): schedule.run_pending(); sleep POLL_SECONDS
        ...
    except KeyboardInterrupt:
        print()
        print(f"stopped by user after {state['runs']} run(s)")
        return EXIT_INTERRUPTED

    print(f"all {state['runs']} run(s) complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. The banner prints immediately, before the first run, and names the interval
   and the stopping condition.
2. Each run prints `[HH:MM:SS] run N  free disk X.X GB` — two spaces before
   `free`, one decimal place on the gigabytes.
3. `--runs 3` stops after three runs, prints `all 3 run(s) complete`, and
   exits 0 without waiting for a fourth interval.
4. `--runs 0` runs until interrupted.
5. Ctrl-C at any moment prints `stopped by user after N run(s)` on its own
   line, with no traceback, and exits **130** — the conventional code for a
   process killed by an interrupt, from the table in Lecture 1 §8.
6. The interrupt is handled around the loop, not inside the job.

## Constraints

- **Poll once a second, whatever `--every` is.** `schedule.run_pending()` only
  fires jobs that are due, so the loop's own sleep decides how fast you notice
  two things: a job coming due, and a Ctrl-C. Sleeping the full interval
  instead means a `--every 300` script ignores your Ctrl-C for five minutes,
  and a terminal that will not quit teaches people to reach for the process
  killer.
- **Let the job stop itself by returning `schedule.CancelJob`.** The
  alternative — a counter checked by the loop — puts the stopping rule in two
  places. With no jobs left the loop has nothing to do, so
  `while schedule.get_jobs():` is both the loop condition and the exit.
- **Keep the run counter in a mutable object passed into the job, not a bare
  module-level `int`.** Rebinding a module-level name from a nested function
  needs a `global` declaration and makes the function untestable in isolation.
  A dict you hand in is explicit about what the job touches.
- **Catch `KeyboardInterrupt`, not bare `except:`.** A bare except also
  swallows `SystemExit` and every real bug, turning a crash into a silent,
  confident wrong answer.
- **Print a newline before the goodbye line.** Your terminal already echoed
  `^C` where the cursor was; without the newline your message lands beside it.

## Expected output

The shipped answer, [`exercise-05-schedule-solution.py`](./exercise-05-schedule-solution.py),
cannot wait for you to press Ctrl-C, and it cannot print a live clock or a live
disk reading and still match a recorded run. So it threads a clock and a disk
reading through as seams — they default to the real ones, so your own version
needs neither — injects a fixed clock and `128.0 GB`, runs one bounded schedule
that stops itself, and then drives the loop into a `KeyboardInterrupt` to prove
the handler. Real captured output:

```text
$ python exercise-05-schedule.py
Schedule — the interval scheduler, driven headless.

A bounded run that stops itself after --runs:
scheduler started: every 2s, stopping after 3 run(s), Ctrl-C to stop
[07:00:00] run 1  free disk 128.0 GB
[07:00:02] run 2  free disk 128.0 GB
[07:00:04] run 3  free disk 128.0 GB
all 3 run(s) complete
[exit 0]

Ctrl-C is honoured around the loop — no traceback, exit 130:
scheduler started: every 2s, running until stopped, Ctrl-C to stop
[07:00:00] run 1  free disk 128.0 GB
[07:00:02] run 2  free disk 128.0 GB

stopped by user after 2 run(s)
[exit 130]
```

Two things to notice on the bounded run. Nothing fires the instant it starts —
`schedule` runs a job one interval *after* you register it. And the script ends
on its own after the third run, without waiting out a fourth interval.

## Steps

1. `pip install schedule` inside your virtual environment, then paste the
   starter.
2. Implement `make_job` without the cancel logic first. Run
   `--every 1 --runs 0` and confirm lines appear once a second. Stop it with
   Ctrl-C — at this stage you get a traceback, which is the point.
3. Add the `try`/`except KeyboardInterrupt` around the loop, run it again, and
   press Ctrl-C. Now you should see your goodbye line and no traceback. Check
   the exit code with `echo $?` on macOS or Linux, `echo $LASTEXITCODE` in
   PowerShell. You want 130.
4. Add the `schedule.CancelJob` return. Run `--every 2 --runs 3` and confirm
   the script ends on its own without waiting out a fourth interval.
5. Run `--every 30 --runs 0` and press Ctrl-C after a couple of seconds. It
   should quit within about a second. If it hangs for thirty, your loop is
   sleeping for the interval instead of the poll period.
6. Read Lecture 3 §4.3 and write the cron line that would run this script
   every morning at 07:00. Put it in a comment at the bottom of your file. You
   do not have to install it.

## The Solution

The shipped file is your answer with two additions for the demo only: `make_job`
and `main` take an optional `clock` and `disk` (both defaulting to the real
`datetime.now` and `shutil.disk_usage`, so your own `make_job(args.runs, state)`
needs neither), and a `demo()` runs a bounded schedule and a driven interrupt
with fixed readings. The scheduler itself is unchanged.

```python
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
```

**`POLL_SECONDS` and `--every` are different numbers on purpose.**
`schedule.run_pending()` does not block; it looks at the clock, fires anything
due, and returns immediately. So the loop's own `time.sleep` is the only thing
that ever blocks, and it decides two separate latencies: how late a job can
fire, and how long a Ctrl-C sits unnoticed. Sleeping `args.every` instead would
make both equal to the interval, so `--every 300` gives you a script that
ignores your interrupt for five minutes. People do not wait five minutes; they
learn to reach for the process killer, and after that they never trust a
long-running script of yours again.

**`while schedule.get_jobs():` is the loop condition *and* the exit.** Returning
`schedule.CancelJob` from the job removes it from the scheduler, the next test
of the condition finds an empty list, and the loop ends. There is one rule about
stopping and it lives in one place. `get_jobs()` is a function call, not a
captured list, so it is asked fresh every pass — which is what lets the job's
own return value change the answer.

**`if limit and run_number >= limit`.** `--runs 0` means "no limit", and `0` is
falsy, so the guard reads as English: if there is a limit, and we have reached
it, stop. No separate `if limit == 0` branch anywhere. The job returns `None`
explicitly on the other path, which says the fall-through was a decision, not an
oversight.

**The counter lives in a dict that is passed in.** `job` is a closure, so it can
*read* an enclosing name but rebinding one needs `nonlocal` or `global`.
Mutating a dict needs neither, because you are changing the object the name
points at, not the binding. And because the dict is handed in from `main()`, the
count is readable from outside the job — which is what makes
`stopped by user after {state['runs']} run(s)` possible in the handler.

**The handler returns 130 itself.** Falling out of the `except` and reaching the
normal `return 0` at the bottom would print your goodbye line and then report
success, which is a lie a shell script downstream will believe. 130 is the
convention for a process ended by an interrupt — 128 plus the signal number —
and it is in the exit-code table in Lecture 1 §8.

**`except KeyboardInterrupt`, never a bare `except`.** A bare `except` also
catches `SystemExit`, `MemoryError`, and every genuine bug in your job, and
reports all of them as "stopped by user". A crash misreported as a clean exit
is the worst outcome available, because it is the one nobody investigates.

## Run it

Copy the worked answer on this page into `exercise-05-schedule.py` and run it:

```bash
pip install schedule
python exercise-05-schedule.py
```

The bounded run takes about seven seconds of real time, because `schedule` fires
on the real clock; the interrupt demo drives the loop's own `sleep` and finishes
quickly. The `-solution` in the name keeps it from colliding with your own
`exercise-05-schedule.py`.

## Common bugs to catch

- **`KeyboardInterrupt` traceback ending in
  `File "exercise-05-schedule.py", line 62, in main / time.sleep(POLL_SECONDS)`.**
  The interrupt arrived while you were sleeping and nothing caught it. That is
  exactly what the `try` block is for.
- **Ctrl-C prints the goodbye line but the exit code is 0.** You handled the
  interrupt and then fell through to the normal `return 0`. The handler has to
  return 130 itself.
- **The script ignores Ctrl-C for the whole interval.** Your loop is
  `time.sleep(args.every)` instead of `time.sleep(POLL_SECONDS)`.
- **One bad run kills the whole scheduler.** `schedule` does not catch
  exceptions raised inside your job — they travel straight out of
  `run_pending()` and end the loop. If the job can fail (a network call, a
  missing path), wrap the body in its own `try`/`except`, log the failure, and
  let the next run try again.
- **The job runs forever even with `--runs 3`.** Returning `schedule.CancelJob`
  is what removes the job — returning `True`, `False`, or the string
  `"cancel"` does nothing. It must be the sentinel object itself.
- **`free disk 128449298432.0 GB`.** You printed the raw byte count.
  `shutil.disk_usage` returns bytes; divide by `1e9` for gigabytes as the
  disk vendor counts them, or by `1024 ** 3` for the gibibytes your operating
  system probably shows. Pick one and label it honestly.
- **`AttributeError: module 'schedule' has no attribute 'every'`.** You have a
  file called `schedule.py` in the same folder and Python imported yours
  instead of the package. Rename your file. The same trap waits with
  `json.py`, `random.py`, and `email.py`.

## Under the hood

<details>
<summary>Under the hood — why the poll loop is separate from the schedule at all</summary>

`schedule` is deliberately not a background service. It does not spawn a thread
or ask the operating system to wake it; it is a plain list of jobs and their
next-due times, and `run_pending()` is a single pass that fires whichever ones
are due right now and returns. Nothing happens between your calls to it. That is
why *you* own the loop: the library decides *what* is due, and your
`while ... time.sleep()` decides *how often to ask*.

Pulling those apart is what buys you a responsive Ctrl-C on a slow schedule. The
process is only ever blocked inside `time.sleep(POLL_SECONDS)`, never inside
`schedule`, so the longest an interrupt can sit unnoticed is one poll — a
second — no matter whether the job runs every two seconds or every two hours.
It is also why the design scales: register a second job on a different interval
and the same one-second loop services both, firing each when it comes due,
because the loop's job was never to *be* the schedule, only to keep asking it.

</details>

## Acceptance checklist

- [ ] `--every 2 --runs 3` finishes in about seven seconds and exits 0.
- [ ] The banner prints before the first run, not after it.
- [ ] Ctrl-C produces the goodbye line, no traceback, and exit code 130.
- [ ] Ctrl-C is honored within about a second even with `--every 30`.
- [ ] `--every 0` is rejected by the parser with exit code 2.
- [ ] A cron line for a 07:00 daily run is written in a comment at the bottom
      of the file.
- [ ] The file is committed to Git with a message like
      `Add Week 12 exercise 5: interval scheduler with clean shutdown`.

## Stretch

- Rewrite it with a plain `time.sleep` loop and no `schedule` dependency:
  track the next-due time yourself against `time.monotonic()`. Then decide
  which version you would rather maintain.
- Add `--warn-below GB` that warns when free space drops under a threshold and
  exits non-zero if it ever tripped. That turns the script into something cron
  can alert on.
- Swap `print` for `logging` with `--log FILE`, so the runs land somewhere you
  can read tomorrow. A scheduled script nobody watches needs a log or it may
  as well not run.
- Register a second job on a different interval and watch how `schedule`
  interleaves them. Then make one slow and watch the other run late.

That is the whole exercise set for Week 12. Next come the longer, combined
problems: [Week 12 Challenges](../challenges/README.md).
