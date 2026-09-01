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
