# Homework Problem 5 — File Watcher (Poll-Based)

> **Topic:** a program that runs forever, notices a file changing, and stops politely when you press Ctrl-C
> **Lecture:** [Lecture 03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour
> **Why this one:** every program you have written so far started, did a thing, and stopped. This one never stops on its own. That changes what counts as correct: a loop that runs for a week has to survive the file vanishing, and it has to end without a traceback when a person decides it is finished.

## The Brief

You want to watch a file. Every time somebody saves it, you want to see
the new contents, straight away, without typing anything.

That is what `tail -f` does, and you are going to build a small version
of it.

The idea is simple enough to say in one sentence: **look at the file's
last-modified time once a second, and when it changes, print the file.**

```text
[2026-05-13 14:30:02] file modified
second version
```

Three things make it a real program rather than a `while` loop.

**The file might not be there.** Somebody is editing it; some editors
delete and recreate rather than overwrite. That must not crash the
watcher. Log a warning and keep watching — and log it **once**, not once
a second, or the message that matters scrolls away in a river of the
message that does not.

**It has to stop cleanly.** Ctrl-C is how a person ends a program that
never ends by itself. It must not answer with a traceback.

**Almost all of its time is spent asleep.** That fact decides where your
`try` goes, and it is the single detail this problem is really about.

Write a script called `watch.py` that takes one file path.

## Starter

Save this as `watch.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it polls forever, prints nothing, and
answers Ctrl-C with a traceback:

```python
"""Watch one file and reprint it whenever it changes."""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime
from pathlib import Path

log = logging.getLogger("watch")

POLL_SECONDS = 1.0


def current_mtime(path: Path) -> float | None:
    """Return the file's modification time, or None if it is not there.

    Args:
        path: The file to look at.

    Returns:
        The modification time in seconds since the epoch, or None.
    """
    # TODO: return path.stat().st_mtime, catching FileNotFoundError and
    #       returning None instead
    return path.stat().st_mtime


def show(path: Path, mtime: float) -> None:
    """Print the change banner and the file's current contents."""
    stamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] file modified")
    sys.stdout.write(path.read_text(encoding="utf-8"))
    sys.stdout.flush()


def watch(path: Path, interval: float = POLL_SECONDS) -> int:
    """Poll `path` forever. Returns 0 when interrupted with Ctrl-C."""
    last_mtime = current_mtime(path)
    log.info("watching %s (Ctrl-C to stop)", path)

    # TODO: put the whole `while` inside a try that catches KeyboardInterrupt,
    #       prints a newline, logs that it stopped, and returns 0
    while True:
        time.sleep(interval)
        mtime = current_mtime(path)
        # TODO: if mtime is None, warn once and carry on
        if mtime != last_mtime:
            last_mtime = mtime
            show(path, mtime)


def main(argv: list[str]) -> int:
    """Watch the file named in `argv`."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)-8s %(name)s  %(message)s"
    )
    if len(argv) != 1:
        print("usage: watch.py FILE", file=sys.stderr)
        return 2
    return watch(Path(argv[0]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Try it with two terminals. In the first:

```bash
python -c "from pathlib import Path; Path('notes.txt').write_text('first version\n', encoding='utf-8')"
python watch.py notes.txt
```

In the second:

```bash
echo "second version" > notes.txt
```

Then go back to the first and press Ctrl-C.

**You can open this one in the browser** — the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-05-file-watcher-poll-based.md) will run the starter and the finished answer. The two-terminal check above needs a real machine, because a browser tab has no second terminal and no Ctrl-C.

## Requirements

1. The script takes one file path.
2. It checks the file's modification time once per second, using
   `time.sleep(1)` and `Path.stat().st_mtime`.
3. When the modification time changes it prints
   `[YYYY-MM-DD HH:MM:SS] file modified` and then the file's current
   contents.
4. A missing file logs a WARNING and the loop carries on.
5. That warning appears once per disappearance, not once per poll.
6. Ctrl-C ends the program with no traceback and an exit code of 0.
7. Every function has type hints and a docstring.

## Constraints

- **The `try` goes outside the `while`, not inside it.** A poll loop
  spends essentially all of its time asleep, so that is where Ctrl-C
  will land. A `try` that only covers the body of the loop never sees
  it.
- **Catch `KeyboardInterrupt` by name.** It does not inherit from
  `Exception`, so `except Exception` does not catch it. That is
  deliberate — it is what stops a blanket handler in a long-running loop
  from making your program impossible to stop.
- **Stat and catch, do not ask first.** `if path.exists():` followed by
  `path.stat()` has a real gap between the two calls, and in a program
  whose whole job is watching a file other people are changing, that gap
  gets hit. `try: stat / except FileNotFoundError` is one system call and
  cannot race.
- **Log the transition, not the state.** A file that stays missing for
  an hour should produce one warning, not 3,600. Keep a flag for
  "already reported".
- **`sys.stdout.write` for the contents, not `print`.** The text you
  read already ends in a newline; `print` would add a second one, so
  every redisplay drifts another blank line down the screen.

## Expected output

The shipped answer runs a demo when you give it no arguments, so it
works from a clean checkout and finishes in well under a second. It
creates its own file in a scratch folder and hands `watch` a **scripted
clock** instead of a real one — a stand-in for `time.sleep` that, rather
than waiting, makes the next change and returns, and finally raises
`KeyboardInterrupt` exactly as a real Ctrl-C during a sleep would.

The script is: change the file, delete it, wait a beat with it still
gone, put it back, then interrupt.

```bash
$ python problem-05-file-watcher-poll-based-solution.py
```

```text
[2026-05-13 14:30:02] file modified
second version
[2026-05-13 14:30:04] file modified
third version

watch() returned 0
```

The banners are the same on every machine because the demo pins each
modification time with `os.utime`. Everything else went to stderr:

```console
INFO     watch  watching live.txt (Ctrl-C to stop)
WARNING  watch  live.txt went away; still watching
INFO     watch  stopped watching live.txt
```

That short transcript exercises all four requirements at once:

- The edit was detected and the new contents printed.
- The deletion warned **once**, not once per poll — the file was gone
  for two polls and there is one warning.
- The file coming back was reported as a modification, with no extra
  code to handle that case.
- The interrupt returned 0 with no traceback.

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `watch.py`. Make `notes.txt` and run it in one
   terminal. Press Ctrl-C. You get a traceback pointing at
   `time.sleep(1)` — that is the bug you are here to fix.
3. Move the `try` so it wraps the whole `while` loop, with
   `except KeyboardInterrupt` after it: `print()`, log that you stopped,
   `return 0`. Run and press Ctrl-C again. Clean exit.
4. Fill in `current_mtime`: `try: return path.stat().st_mtime` /
   `except FileNotFoundError: return None`.
5. Handle the `None` in the loop. Warn, set `last_mtime = None`, and
   `continue`. Delete the file from the other terminal and watch the
   warning arrive once a second. That is the noise problem.
6. Add the `missing_reported` flag: warn only when it is `False`, set it
   `True` after warning, and set it back to `False` on any poll where
   the file exists. Delete the file again — one warning now.
7. Recreate the file. Because `last_mtime` was set to `None`, the next
   real modification time is different from it, so the file reappearing
   is reported as a change with no extra branch.
8. Edit the file twice in quick succession and see whether both edits
   register. If they do not, you have met mtime granularity, which the
   Under the hood block below explains.
9. Compare against **The Solution**, work down the acceptance checklist,
   and commit: `git add homework/watch.py` then
   `git commit -m "Week 6 homework: file watcher"`.

## The Solution

```python
"""Homework 5 — poll-based file watcher.

Checks a file's modification time once per second and reprints the file
whenever it changes. A missing file is a WARNING, not a crash. Ctrl-C exits
quietly with no traceback.

    python watch.py notes.txt

Run it with no arguments and it watches a file it creates in a scratch folder,
driven by a scripted clock instead of a real one, so the download finishes in
under a second from a clean checkout with nothing set up.

Save your own copy as ``watch.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import logging
import os
import sys
import tempfile
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

log = logging.getLogger("watch")

POLL_SECONDS = 1.0

#: Anything that can be handed a number of seconds and come back later.
Sleeper = Callable[[float], None]


def current_mtime(path: Path) -> float | None:
    """Return the file's modification time, or None if it is not there.

    EAFP: stat and catch, rather than `if path.exists()`. Between an `exists()`
    check and the `stat()` the file can vanish, and then the check bought you
    nothing but a second syscall.

    Args:
        path: The file to look at.

    Returns:
        The modification time in seconds since the epoch, or None.
    """
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None


def show(path: Path, mtime: float) -> None:
    """Print the change banner and the file's current contents.

    Args:
        path: The file that changed.
        mtime: The modification time to stamp the banner with.
    """
    stamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] file modified")
    try:
        sys.stdout.write(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        log.warning("%s disappeared before it could be read", path)
    except UnicodeDecodeError as e:
        log.warning("%s is not valid UTF-8 (%s)", path, e.reason)
    sys.stdout.flush()


def watch(
    path: Path, interval: float = POLL_SECONDS, sleep: Sleeper = time.sleep
) -> int:
    """Poll *path* forever. Returns 0 when interrupted with Ctrl-C.

    Args:
        path: The file to watch.
        interval: Seconds between polls.
        sleep: How to wait. Handing the waiting in as an argument is what lets
            the demo drive this loop with a scripted clock instead of a real
            one, without changing a line of the logic below.

    Returns:
        0, once someone presses Ctrl-C.
    """
    last_mtime = current_mtime(path)
    if last_mtime is None:
        log.warning("%s does not exist yet; waiting for it", path)
    else:
        log.info("watching %s (Ctrl-C to stop)", path)

    missing_reported = last_mtime is None
    try:
        while True:
            sleep(interval)
            mtime = current_mtime(path)
            if mtime is None:
                if not missing_reported:
                    log.warning("%s went away; still watching", path)
                    missing_reported = True
                last_mtime = None
                continue
            missing_reported = False
            if mtime != last_mtime:
                last_mtime = mtime
                show(path, mtime)
    except KeyboardInterrupt:
        print()
        log.info("stopped watching %s", path)
        return 0


def _stamp(text: str) -> float:
    """Turn ``"2026-05-13 14:30:01"`` into a timestamp for `os.utime`.

    Reading it back with `datetime.fromtimestamp` gives the same wall-clock
    string in any time zone, because both conversions use the local one. That
    is what makes the demo's banners identical on every machine.

    Args:
        text: A local date and time, ``YYYY-MM-DD HH:MM:SS``.

    Returns:
        Seconds since the epoch.
    """
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").timestamp()


def _demo() -> int:
    """Watch a scratch file whose changes are scripted, then interrupt it.

    The scripted clock edits the file in place of really waiting, and finally
    raises `KeyboardInterrupt` — which is exactly what a real Ctrl-C during
    `time.sleep` does. Every modification time is pinned, so the banners come
    out the same on every machine.

    Returns:
        Always 0. The demo ends the same way every time.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="watch_") as scratch:
        try:
            os.chdir(scratch)
            target = Path("live.txt")
            target.write_text("first version\n", encoding="utf-8")
            os.utime(target, (_stamp("2026-05-13 14:30:01"),) * 2)

            def rewrite(text: str, when: str) -> None:
                """Replace the file's contents and pin its modification time."""
                target.write_text(text, encoding="utf-8")
                os.utime(target, (_stamp(when),) * 2)

            steps: list[Callable[[], None]] = [
                lambda: rewrite("second version\n", "2026-05-13 14:30:02"),
                target.unlink,
                lambda: None,
                lambda: rewrite("third version\n", "2026-05-13 14:30:04"),
            ]
            script = iter(steps)

            def scripted_sleep(_seconds: float) -> None:
                """Run the next scripted change, or interrupt when they run out."""
                try:
                    next(script)()
                except StopIteration:
                    raise KeyboardInterrupt from None

            code = watch(target, interval=0.0, sleep=scripted_sleep)
            print(f"watch() returned {code}")
        finally:
            os.chdir(home)
    return 0


def main(argv: list[str]) -> int:
    """Watch the file named in *argv*, or run the scripted demo when empty.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)-8s %(name)s  %(message)s"
    )
    if not argv:
        return _demo()
    if len(argv) != 1:
        print("usage: watch.py FILE", file=sys.stderr)
        return 2
    return watch(Path(argv[0]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**Why it works.**

**The `try` wraps the whole loop, including the sleep.** This is the one
detail that decides whether the program exits cleanly. Checking a file's
modification time takes microseconds; sleeping takes a second. So more
than 99.9% of the program's life is spent inside `sleep`, and that is
where Ctrl-C almost certainly lands. A `try` that starts inside the loop
misses it entirely.

**`float | None` is a better state than a separate "exists" flag.**
`None` means "not there right now", and it takes part in the same
comparison as any other value. When the file comes back,
`mtime != last_mtime` compares a float with `None`, which is `True`, so
the reappearance is reported as a modification without a single extra
branch. Pick a placeholder that participates in the logic instead of one
you have to work around.

**`missing_reported` logs the transition, not the state.** Without it, a
file that stays missing produces one warning every second forever, and
the event you care about — the file coming back — scrolls off the top of
the screen. A message that repeats every tick is noise, and noise is how
people learn to ignore logs.

**The banner shows the file's modification time, not the current time.**
There are two defensible times to print: when the file changed, or when
you noticed. With a one-second poll those can differ by nearly a full
second. The modification time is a fact about the event; "now" is a fact
about your polling interval. If you choose `datetime.now()` instead,
that is fine — say so in your docstring, so a reader knows you saw the
choice.

**`show` catches `FileNotFoundError` again, one layer down.** Between the
`stat` that reported a new modification time and the `read_text` that
follows it, the file can be deleted. It is the same race, and catching
it turns a crash into a warning.

**The `sleep` parameter is what makes the answer testable.** `watch`
does not reach out and grab `time.sleep`; it is handed something to wait
with, and defaults to the real one. The demo passes a stand-in that
makes the next scripted change instead of waiting, and raises
`KeyboardInterrupt` when the script runs out. Not one line of the loop's
logic changes. Handing a dependency in rather than reaching for it is
the move that makes long-running code possible to check, and you will
meet it again in Week 11.

## Download and run

Download [problem-05-file-watcher-poll-based-solution.py](./problem-05-file-watcher-poll-based-solution.py)
and run it:

```bash
python problem-05-file-watcher-poll-based-solution.py
```

With no arguments it creates its own file in a temporary folder and
drives the watcher with a scripted clock, so it runs anywhere, needs
nothing set up, and finishes immediately. Give it a real path and it
watches that file for real, once a second, until you press Ctrl-C:

```bash
python problem-05-file-watcher-poll-based-solution.py notes.txt
```

Save your own copy as `watch.py` in your homework folder, and commit that
one. The longer download name is there so it cannot overwrite your work.

## Common bugs to catch

- **`except KeyboardInterrupt` inside the loop.**

  ```python
  while True:
      time.sleep(1)
      try:
          mtime = path.stat().st_mtime
          if mtime != last:
              last = mtime
              print("file modified")
      except KeyboardInterrupt:       # never fires: the sleep is outside the try
          print("bye")
          break
  ```

  Press Ctrl-C and you get exactly what the brief forbids:

  ```text
  Traceback (most recent call last):
    File "wrong5.py", line 7, in <module>
      time.sleep(1)
      ~~~~~~~~~~^^^
  KeyboardInterrupt
  ```

  The traceback names `time.sleep(1)` — the line above the `try`. Move
  the `try` outside the `while`.
- **`except Exception:` to catch the interrupt.** It does not catch it.
  `KeyboardInterrupt` inherits from `BaseException`, not from
  `Exception`, and that is on purpose: it is what keeps a blanket
  handler in a long-running loop from making your program
  un-interruptible.

  ```text
  BaseException
   ├── SystemExit
   ├── KeyboardInterrupt
   └── Exception
  ```

- **`if path.exists()` before every stat.** Works nearly always. Races
  occasionally. The occasional failure is a crash in a program that is
  meant to run for days, and it will happen at three in the morning.
- **Warning on every poll while the file is missing.** One line a second
  for as long as it takes somebody to notice. The flag is three lines
  and it is the difference between a log you read and a log you skip.
- **Forgetting to update `last_mtime` after a change.** The file's
  contents get reprinted once a second forever. It looks like it works
  for the first second.
- **`print(path.read_text())`.** Double newlines, one extra per
  redisplay. Cosmetic, until you try to diff the output.

## Under the hood

<details>
<summary>Under the hood — how logging levels differ from print, and why that matters here</summary>

`print` has exactly one behaviour: put this on stdout, now, always.
`logging` gives every message a **level**, and levels are what let you
change your mind later without editing the code.

```text
DEBUG     10   the detail you want when something is wrong
INFO      20   normal progress: started, finished, connected
WARNING   30   something odd, but the program carries on
ERROR     40   this operation failed
CRITICAL  50   the program cannot continue
```

The logger compares each message's level against a threshold and drops
anything below it. One line changes what you see:

```python
logging.basicConfig(level=logging.INFO)    # DEBUG hidden
logging.basicConfig(level=logging.DEBUG)   # everything shown
logging.basicConfig(level=logging.WARNING) # only problems
```

That is the first difference: **the messages stay in the code and the
decision moves out of it.** Delete a `print` and it is gone; you write
it again next time you have the same bug. Turn a `log.debug` off and it
is still there when you need it.

Four more differences, each of which matters in this program:

**Destination.** `logging` writes to stderr by default. So
`python watch.py notes.txt > captured.txt` puts the file's contents in
`captured.txt` and leaves the "watching…" and "went away" lines on your
screen where you can see them. With `print` the diagnostics would be
mixed into the captured file.

**Formatting arguments are not joined until they are needed.**

```python
log.debug("record %d of %d: %s", i, total, record)
```

If DEBUG is switched off, that `%s` never runs and `record` is never
converted to a string. `log.debug(f"record {i}: {record}")` builds the
string first, every time, even when nobody will read it. In a loop over
a million records that is a real cost.

**Every message carries where it came from.** `logging.getLogger("watch")`
names this module's logger, and the format string `%(name)s` prints it.
In a program with five modules you can see which one is complaining —
and you can turn one of them down without touching the others:

```python
logging.getLogger("watch").setLevel(logging.WARNING)
```

**The output can be redirected without changing any call site.** A
handler decides where records go: the screen, a file, a rotating set of
files, the system log, a network service. `log.warning(...)` does not
know or care, so you can add file logging to a finished program by
adding one handler at startup.

The honest counter-case: for a program's actual *result* — the table in
problem 1, the file contents here — `print` is right and `logging` is
wrong. The rule that sorts them is not "logging is more professional".
It is **results go to stdout with `print`, everything about how the run
went goes to `logging`.**

</details>

<details>
<summary>Under the hood — what polling misses, and how the real tools do it</summary>

The brief calls this "a preview of why people use libraries like
`watchdog` for the real thing". Here is what "the real thing" fixes.

**Modification-time granularity.** Two saves inside the same filesystem
timestamp tick look like one save. Modern Linux filesystems store
nanoseconds; older ones, and some network mounts, store whole seconds.
An editor that writes twice in quick succession can lose an event
entirely. That is why the demo in this answer pins each modification
time explicitly — without distinct times, two of its edits would be
invisible.

**Latency.** You find out up to a whole second late. Halving the
interval halves the delay and doubles the system calls, forever, whether
anything is happening or not.

**Same-size, same-time rewrites are invisible.** Comparing
`(st_mtime, st_size)` catches more changes than `st_mtime` alone. A
content hash catches everything, at the cost of reading the whole file
on every single poll.

**Partial reads.** If the writer is halfway through when you look, you
print half a file. Nothing in a poll loop can prevent that. Problem 6's
atomic write is what fixes it — from the *writer's* side, which is
exactly why the two problems sit next to each other in this homework.

`watchdog` and tools like it do not poll at all. They ask the operating
system to tell them:

| Platform | Mechanism |
|---|---|
| Linux | `inotify` |
| macOS | `FSEvents` |
| Windows | `ReadDirectoryChangesW` |

The kernel already knows the instant a file is written, because it did
the writing. These interfaces let a program register interest and then
block until something actually happens — no polling, no interval, no
missed events between ticks.

Polling is still worth knowing, and it is still occasionally the right
answer: it works over network filesystems where notifications do not, it
works the same on every platform, and it is twenty lines with no
dependencies. Just know what you gave up.

</details>

## Acceptance checklist

- [ ] `python watch.py notes.txt` prints the banner and contents when
      the file is saved from another terminal.
- [ ] Ctrl-C exits with no traceback and an exit code of 0.
- [ ] Deleting the watched file logs exactly one WARNING, not one per
      second.
- [ ] Recreating it is reported as a modification.
- [ ] `current_mtime` uses `try` / `except FileNotFoundError`, not
      `path.exists()`.
- [ ] The `try` that catches `KeyboardInterrupt` is outside the `while`.
- [ ] The contents are written with `sys.stdout.write`, so there are no
      doubled blank lines.
- [ ] The docstring says whether the banner shows the modification time
      or the current time.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like `Week 6 homework: file watcher`.

## Stretch

- **Compare `(st_mtime, st_size)` instead of the modification time
  alone.** A one-line change that catches a whole class of edits the
  timestamp misses.
- **Print only the new lines, like `tail -f` really does.** Remember how
  many bytes you have already shown, `seek` to that offset, and read
  from there. Then think about what should happen when the file gets
  *shorter*, which is what log rotation looks like from the inside.
- **Watch a whole folder.** `path.glob("*.txt")` on each poll, and keep
  a dict of path to modification time. Now you can report files that
  appeared and files that vanished, not just files that changed.
- **Make the interval a flag.** `--interval 0.25`. Then measure the
  system calls per minute at 1 second and at 0.25, and decide out loud
  what you bought.
- **Use `watchdog` for comparison.** `pip install watchdog` in your
  Week 6 environment, write the same tool with it in about fifteen
  lines, and note two things it does that your version cannot. Do this
  after yours works, not before — the point is the comparison.

Next: [Homework Problem 6 — Atomic-Save Helper](./problem-06-atomic-save-helper.md).
