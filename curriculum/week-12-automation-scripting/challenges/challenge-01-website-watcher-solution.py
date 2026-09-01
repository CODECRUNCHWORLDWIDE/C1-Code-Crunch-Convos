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
