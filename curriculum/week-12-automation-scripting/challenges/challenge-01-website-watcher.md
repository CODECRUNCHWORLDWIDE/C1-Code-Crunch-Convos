# Challenge 01 — Website watcher

> **Topic:** `requests` + `hashlib` + `logging` — a daemon that reports when a page changes
> **Lecture:** [03 — Scraping and Scheduling](../lecture-notes/03-scraping-and-scheduling.md)
> **Difficulty:** Medium
> **Target time:** 1.5–3 hours
> **Why this one:** it stitches the week together — a polite HTTP client, a hash, a JSON state file, `logging`, and a Ctrl-C-able loop — into one small daemon. The pattern underneath is everywhere: alert me when a course opens for enrollment, when a PR description changes, when a homepage gets a new "What's new" entry. Build it once here and you own the shape.

## The Brief

Build a script that polls a URL on an interval, hashes the response body, and
prints a clear message whenever the content has changed since the previous
check. The last hash is remembered in a small JSON file, so a change is
detected across separate runs — which is what lets the same script run once from
`cron` or loop forever in a terminal.

The heart of it is three facts written to a state file: the URL, the hash of its
last body, and how many times you have checked. On each poll you fetch, hash,
compare against the stored hash, log `CHECK` or `CHANGE`, and write the new
state back. A server having a bad day (a 429 or a 5xx) is logged as a warning
and left alone — you do not want to record the hash of an error page and then
scream `CHANGE` the moment the real page comes back.

## Starter

Install `requests`; everything else is standard library.

```bash
pip install requests
```

```python
"""watcher.py — poll a URL and report when its content changes.

    python watcher.py URL [--interval SECONDS] [--state FILE] [--once] [--log FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests


def fetch_hash(url: str, session: requests.Session) -> tuple[str, int]:
    """Return (sha256 hex digest of the response body, HTTP status code)."""
    # TODO: session.get(url, timeout=10); hash resp.content, not resp.text
    ...


def load_state(path: Path) -> dict:
    """Read the state file. A missing or corrupt file means 'no history yet'."""
    ...


def save_state(path: Path, state: dict) -> None:
    """Write the state file, creating its parent directory if needed."""
    ...


def check_once(url: str, state_path: Path, session: requests.Session) -> bool:
    """Run a single check. Return True if the content changed."""
    # TODO: load state, fetch+hash, branch on status, log CHECK/CHANGE/WARN,
    # save the new state on success only
    ...


def main(argv: list[str] | None = None) -> int:
    """Parse args, then either check once or loop until Ctrl-C."""
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. **CLI** built with `argparse`: a positional `URL`, plus `--interval`
   (seconds, default 60), `--state` (JSON file, default `watcher_state.json`),
   `--once` (single check and exit), and `--log` (file path; stdout if
   omitted).
2. **Hash the body bytes** with `hashlib.sha256(resp.content).hexdigest()`.
   Hash `resp.content`, never `resp.text`.
3. **State file** is JSON holding `url`, `hash`, `checked_at`, and
   `checked_count`.
4. **Log lines carry a timestamp** and a fixed-width verb, e.g.
   `2026-05-13 10:00:00  CHECK   https://example.com -> sha256:abcd... (unchanged)`
   and `... CHANGE ... sha256:1234... (was abcd...)`.
5. **Polite HTTP**: a custom `User-Agent`, a 10-second timeout, and on a 429 or
   5xx, log a warning and continue rather than crash.
6. **Exit codes**: 0 on a normal stop (Ctrl-C, or `--once` succeeded), 1 if the
   URL is malformed or the state file cannot be written.
7. Use `logging`, not `print`; use `pathlib.Path`; make `main()` importable and
   `--once` take no `while True` loop.

## Constraints

- **Hash `resp.content`, not `resp.text`.** `.content` is the raw bytes off the
  socket; `.text` is those bytes decoded with a charset `requests` guesses.
  That guess can differ between two byte-identical responses, so hashing `.text`
  makes the digest a property of your HTTP library, not the page.
- **Do not call `raise_for_status()` and let it fly.** It is right for a
  one-shot scraper and wrong for a daemon: the first 503 kills your watcher.
  Branch on `response.status_code` instead, so a bad day for the server is a
  warning, not a death.
- **A failed check writes no state.** Return before `save_state` on any non-2xx
  or network error. Record the hash of an error page and the next healthy poll
  reports a `CHANGE` that never happened.
- **`--once` and the loop are two code paths.** The spec says "if `--once` is
  passed, no `while True` loop", so return before the loop exists rather than
  putting a flag inside it.
- **Catch `KeyboardInterrupt` around the loop and return 0.** Ctrl-C is how you
  stop a daemon; letting it escape prints a traceback and exits 130.

## Expected output

The shipped answer, [`challenge-01-website-watcher-solution.py`](./challenge-01-website-watcher-solution.py),
puts the HTTP call behind a one-line `fetch` seam and drives `check_once` with a
recorded sequence — a page that is new, then unchanged, then changed, then a
404 — so it runs offline and identically every time. Each real log line begins
with a live timestamp, which no recording can match, so the demo drops that one
prefix and prints the rest. Real captured output:

```text
$ python challenge-01-website-watcher-solution.py
Website Watcher — driven headless with recorded responses.
(each log line's live timestamp prefix is dropped here so the run matches)

CHECK   https://example.test/ -> sha256:a60033ba226b... (new)
CHECK   https://example.test/ -> sha256:a60033ba226b... (unchanged)
CHANGE  https://example.test/ sha256:453b410e0182... (was a60033ba226b...)
WARN    https://example.test/ HTTP 404 - nothing to compare
```

On a real run each of those lines is preceded by
`2026-05-13 10:00:00  ` — one seven-character left-justified verb column after a
timestamp. The 404 logs a warning and, crucially, writes no state, so the next
healthy poll does not report a phantom change.

## Steps

1. Build the parser and `main()` skeleton first. Get `--help` reading well
   before any HTTP happens.
2. Write `fetch_hash` and confirm two runs against a stable page
   (`https://example.com/`) log `(new)` then `(unchanged)`.
3. Add `load_state` / `save_state`, and check the JSON file grows a
   `checked_count`.
4. Serve a local page you can edit (`python -m http.server`), change it, and
   watch a run log `CHANGE`.
5. Point it at a 404 and a refused connection. Both must warn and exit 0 under
   `--once`, and leave the state file untouched.
6. Add the polling loop with `try/except KeyboardInterrupt`, and confirm Ctrl-C
   logs `STOP` and exits 0.

## The Solution

The shipped file is a complete watcher — `fetch_hash`, `load_state`,
`save_state`, `check_once`, the parser, `configure_logging`, `main` — with the
network call pulled into a `fetch` seam and a `demo()` that feeds it recorded
responses. Your own file has no seam and no demo; it calls `session.get`
directly and you stop it with Ctrl-C.

```python
"""challenge-01-website-watcher-solution.py — the watcher, proven offline.

The challenge answer is a daemon that polls a URL, hashes the body, and logs
CHECK / CHANGE / WARN as the content moves. Your own watcher.py ends in
``raise SystemExit(main())`` and hits real URLs on a real interval; you stop it
with Ctrl-C.

A published answer must run the same way on every machine with no network and
no waiting, so this file puts the HTTP call behind a one-line ``fetch`` seam and
the demo feeds it recorded responses — a page that is new, then unchanged, then
changed, then a 404. Every log line carries a live timestamp, which cannot match
a recording, so the demo drops that one volatile prefix and prints the rest. The
change-detection being tested is identical either way; the CLI, the state file,
and the polite-HTTP branches are exactly what runs live.

Run it with::

    python challenge-01-website-watcher-solution.py
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import logging
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

__version__ = "1.0.0"

USER_AGENT = "WebsiteWatcher/0.1 (+you@example.com)"
TIMEOUT = 10.0
HASH_PREFIX = 12

LOG_FORMAT = "%(asctime)s  %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGER = logging.getLogger("watcher")


class StateError(RuntimeError):
    """The state file cannot be read or written."""


def short(digest: str) -> str:
    """The first HASH_PREFIX hex characters of a digest, for human-sized logs."""
    return digest[:HASH_PREFIX]


def is_valid_url(url: str) -> bool:
    """True only for absolute http(s) URLs with a host."""
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fetch(session: requests.Session, url: str) -> tuple[bytes, int]:
    """Return (response body bytes, HTTP status). The seam the demo overrides.

    Everything downstream hashes the bytes and branches on the status, so a
    recorded (bytes, status) pair stands in for a live fetch with no change to
    the logic being tested.
    """
    response = session.get(url, timeout=TIMEOUT)
    return response.content, response.status_code


def fetch_hash(url: str, session: requests.Session) -> tuple[str, int]:
    """Return (sha256 hex digest of the response body, HTTP status code).

    Hashes the raw bytes, not decoded text: decoding would make the digest
    depend on the charset guess, so two identical responses could hash
    differently.
    """
    content, status = fetch(session, url)
    return hashlib.sha256(content).hexdigest(), status


def load_state(path: Path) -> dict:
    """Read the state file. A missing or corrupt file means 'no history yet'."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        LOGGER.warning("%-7s state file %s is not valid JSON; starting fresh",
                       "WARN", path)
        return {}
    except OSError as exc:
        raise StateError(f"cannot read state file {path}: {exc}") from exc


def save_state(path: Path, state: dict) -> None:
    """Write the state file, creating its parent directory if needed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise StateError(f"cannot write state file {path}: {exc}") from exc


def check_once(url: str, state_path: Path, session: requests.Session) -> bool:
    """Run a single check. Return True if the content changed."""
    state = load_state(state_path)

    try:
        digest, status = fetch_hash(url, session)
    except requests.RequestException as exc:
        LOGGER.warning("%-7s %s %s: %s", "WARN", url, type(exc).__name__, exc)
        return False

    if status == 429 or status >= 500:
        LOGGER.warning("%-7s %s HTTP %d - server is unhappy, state untouched",
                       "WARN", url, status)
        return False
    if status >= 400:
        LOGGER.warning("%-7s %s HTTP %d - nothing to compare", "WARN", url, status)
        return False

    same_target = state.get("url") == url
    previous = state.get("hash") if same_target else None
    changed = previous is not None and previous != digest

    if previous is None:
        LOGGER.info("%-7s %s -> sha256:%s... (new)", "CHECK", url, short(digest))
    elif changed:
        LOGGER.info("%-7s %s sha256:%s... (was %s...)",
                    "CHANGE", url, short(digest), short(previous))
    else:
        LOGGER.info("%-7s %s -> sha256:%s... (unchanged)", "CHECK", url, short(digest))

    count = int(state.get("checked_count", 0)) if same_target else 0
    save_state(state_path, {
        "url": url,
        "hash": digest,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checked_count": count + 1,
    })
    return changed


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0, got {number}")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="watcher",
        description="Poll a URL and report when its content changes.",
    )
    parser.add_argument("url", metavar="URL", help="The URL to watch.")
    parser.add_argument("--interval", type=positive_float, default=60.0,
                        metavar="SECONDS",
                        help="Seconds between checks (default: %(default)s)")
    parser.add_argument("--state", type=Path, default=Path("watcher_state.json"),
                        metavar="FILE",
                        help="JSON file holding the last hash (default: %(default)s)")
    parser.add_argument("--once", action="store_true",
                        help="Run a single check and exit (great for cron).")
    parser.add_argument("--log", type=Path, default=None, metavar="FILE",
                        help="Log to this file instead of stdout.")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    return parser


def configure_logging(log_path: Path | None) -> None:
    """One handler: the log file if asked for, otherwise stdout."""
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False

    if log_path is None:
        handler: logging.Handler = logging.StreamHandler(stream=sys.stdout)
    else:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    LOGGER.addHandler(handler)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not is_valid_url(args.url):
        print(f"error: {args.url!r} is not an absolute http(s) URL", file=sys.stderr)
        return 1

    try:
        configure_logging(args.log)
    except OSError as exc:
        print(f"error: cannot open log file {args.log}: {exc}", file=sys.stderr)
        return 1

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    try:
        if args.once:
            check_once(args.url, args.state, session)
            return 0

        LOGGER.info("%-7s %s every %gs (Ctrl-C to stop)",
                    "START", args.url, args.interval)
        while True:
            check_once(args.url, args.state, session)
            time.sleep(args.interval)
    except StateError as exc:
        LOGGER.error("%-7s %s", "ERROR", exc)
        return 1
    except KeyboardInterrupt:
        LOGGER.info("%-7s stopped by user", "STOP")
        return 0
    finally:
        session.close()


# --------------------------------------------------------------------------- #
# The headless demo — recorded responses through the fetch seam, the log's
# volatile timestamp prefix dropped so the run matches every time. Your own
# file has no demo; it polls real URLs and you stop it with Ctrl-C.
# --------------------------------------------------------------------------- #

TS_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}  ")


def demo() -> None:
    """Feed the watcher a new / unchanged / changed / 404 sequence."""
    global fetch
    print("Website Watcher — driven headless with recorded responses.")
    print("(each log line's live timestamp prefix is dropped here so the run matches)")
    print()

    url = "https://example.test/"
    version_one = b"<h1>version one</h1>\n"
    version_two = b"<h1>version two</h1>\n"
    script = [
        (version_one, 200),  # first ever check     -> (new)
        (version_one, 200),  # same bytes           -> (unchanged)
        (version_two, 200),  # different bytes       -> CHANGE
        (b"", 404),          # gone                  -> WARN, state untouched
    ]
    responses = iter(script)

    def recorded_fetch(session: requests.Session, target: str) -> tuple[bytes, int]:
        return next(responses)

    buffer = io.StringIO()
    for handler in list(LOGGER.handlers):
        LOGGER.removeHandler(handler)
        handler.close()
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    LOGGER.addHandler(handler)

    original_fetch = fetch
    fetch = recorded_fetch
    try:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            session = requests.Session()
            for _ in script:
                check_once(url, state_path, session)
            session.close()
    finally:
        fetch = original_fetch

    for line in buffer.getvalue().splitlines():
        print(TS_PREFIX.sub("", line))


if __name__ == "__main__":
    demo()
```

**The log format is `%-7s` and nothing else.** Count the spaces the spec asks
for: three after `CHECK`, two after `CHANGE`. That is not two hand-typed
strings, it is one seven-character left-justified column followed by a single
space, so `"%-7s %s"` produces both and they can never drift apart. The
timestamp is `logging`'s own `%(asctime)s` with a `datefmt` that drops the
milliseconds the default includes.

**Hash the bytes, not the text.** `resp.content` is `bytes` exactly as they came
off the socket. `resp.text` decodes them with a charset `requests` guesses, and
on a page with no declared charset that guess can differ across `requests`
versions — so two byte-identical responses could hash differently. Hashing
`.content` makes the digest a property of the page; hashing `.text` makes it a
property of the page *and* your HTTP library.

**Errors do not touch the state.** A 503 returns early, before `save_state`.
This matters more than it looks: record the hash of an error page and the next
successful poll reports a `CHANGE` the site never made. So `checked_count`
counts *successful* checks — the number you actually want when you ask "has
this been stable for a week?".

**`same_target` is why the URL is in the state file.** Without it, pointing an
existing state file at a different URL would compare this page's hash against
that page's hash and scream `CHANGE` on the first poll. Storing the URL and
comparing it turns that into a clean `(new)` and resets the count.

**`raise_for_status()` is the wrong tool here.** It is the right habit for a
one-shot scraper and a death sentence for a daemon: the first 503 raises
`HTTPError` and your watcher exits. Branching on `response.status_code` keeps
the two failure classes — server unhappy (429/5xx) and nothing-to-compare
(4xx) — as warnings that leave the loop running.

**`KeyboardInterrupt` is caught around the loop, and returns 0.** Ctrl-C is how
you are *supposed* to stop a daemon. Catching it, logging `STOP`, and returning
0 is the difference between a tool and a script — and it is caught outside the
`while`, so an interrupt during `time.sleep` and one during `session.get` are
handled the same way.

## Download and run

Download
[challenge-01-website-watcher-solution.py](./challenge-01-website-watcher-solution.py)
and run it:

```bash
pip install requests
python challenge-01-website-watcher-solution.py
```

The demo runs entirely against recorded responses, so it needs no network. To
watch a real page, run it as `python challenge-01-website-watcher-solution.py
https://example.com/ --once`; the docstring lists every flag.

## Common bugs to catch

- **The watcher dies on the first 503.** You called `raise_for_status()` and let
  the `HTTPError` fly. A daemon must survive a server's bad day — branch on the
  status code and log a warning instead.
- **It reports `CHANGE` on every single poll.** The page has a rotating ad slot,
  a CSRF token, or a "generated in 0.048s" footer, so it genuinely is different
  every time. Nothing is wrong with your hashing. Hash the *part you care
  about* — parse the HTML and hash one CSS selector's text — or accept that some
  pages cannot be watched by whole-body hash.
- **`session.get(url)` with no `timeout` hangs forever.** Not thirty seconds,
  forever, if the server accepts the connection and then never sends a byte.
  Under cron you get a new stuck process every minute. `TIMEOUT = 10.0`.
- **The state file holds a truncated hash.** Logging `sha256:ff67a9d764d6...` is
  friendly; *storing* only those twelve characters throws the digest away and
  makes collisions cheap. Store the full 64 hex characters; shorten only when
  logging.
- **A phantom `CHANGE` after an outage.** You saved state on an error response.
  The next healthy poll then differs from the error-page hash. Return before
  `save_state` on any non-2xx.

## Under the hood

<details>
<summary>Under the hood — signed state, atomic writes, and why a corrupt file should not be fatal</summary>

`save_state` rewrites the whole file every time rather than appending, so the
file on disk is always either the previous complete JSON or the new complete
JSON — never half of each. On most filesystems a `write_text` of a small file is
effectively atomic from a reader's point of view, but the truly careful version
writes to a temp file next to the target and `os.replace`s it into place, which
*is* atomic on every platform: a reader either sees the old file or the new one,
because `replace` swaps the directory entry in one step.

`load_state` treats a corrupt or missing file as "no history yet" instead of
crashing. That is a deliberate reliability choice: a watcher that dies
permanently because one write got interrupted is worse than one that reports a
single spurious `(new)` and carries on. The general rule for anything that runs
unattended is that the recoverable failure should recover — log it, assume the
safe default, keep going — and only the truly unrecoverable one (the state
directory is unwritable) should stop the process. That is exactly the split
between the `json.JSONDecodeError` branch, which starts fresh, and the `OSError`
branch, which raises `StateError` and exits 1.

</details>

## Acceptance checklist

- [ ] First run of a stable page logs `(new)`, the second logs `(unchanged)`.
- [ ] Editing a served page makes the next run log `CHANGE (was ...)`.
- [ ] A 404 and a refused connection both warn and exit 0 under `--once`, and
      write no state.
- [ ] A malformed URL prints to stderr and exits 1.
- [ ] Ctrl-C out of the loop logs `STOP` and exits 0.
- [ ] The code uses `logging` and `pathlib`, and `main(argv)` is importable.
- [ ] Committed to Git with a message like
      `Add Week 12 challenge 1: website watcher`.

## Stretch

- **Diff preview**: when content changes, keep the previous body and log a
  `difflib.unified_diff` of it against the new one.
- **Multiple URLs**: accept several URLs (or a file of them) and one state file
  that tracks all of them.
- **Notifications**: on change, fire a desktop notification (`osascript`,
  `notify-send`, or `winotify`) or an email via `smtplib`.
- **Backoff**: on repeated 5xx, double the interval up to a cap, and reset it on
  the first clean round.

When your watcher survives a 503 and stops cleanly on Ctrl-C, move on to
[Challenge 02 — PDF renamer](./challenge-02-pdf-renamer.md).
