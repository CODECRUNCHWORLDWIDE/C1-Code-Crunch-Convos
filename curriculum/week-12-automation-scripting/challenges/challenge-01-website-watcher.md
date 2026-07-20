# Challenge 01 — Website watcher

Build a daemon-style Python script that polls a URL on an interval, hashes the response body, and prints (or logs) a clear message whenever the content has changed since the previous check.

This pattern is the foundation of all kinds of useful automation: alerting you when a course opens for enrollment, when a PR description changes, when a homepage gets a new "What's new" entry, etc.

---

## Requirements

### Functional

1. **CLI** built with `argparse`. At minimum:

   ```text
   python watcher.py URL [--interval SECONDS] [--state FILE] [--once] [--log FILE]
   ```

   - `URL` (positional): the URL to watch.
   - `--interval`: seconds between checks. Default 60.
   - `--state`: path to a JSON file used to persist the last hash. Default `./watcher_state.json`.
   - `--once`: run a single check and exit (great for cron).
   - `--log`: file path for the log. If omitted, log to stdout.

2. **Hashing**: SHA-256 of the response body (`hashlib.sha256(resp.content).hexdigest()`).

3. **State file** (JSON):

   ```json
   {
     "url": "https://example.com",
     "hash": "abcdef...",
     "checked_at": "2026-05-13T10:00:00",
     "checked_count": 12
   }
   ```

4. **Output / log lines** must include a timestamp:

   ```text
   2026-05-13 10:00:00  CHECK   https://example.com -> sha256:abcd... (unchanged)
   2026-05-13 10:01:00  CHANGE  https://example.com sha256:1234... (was abcd...)
   ```

5. **Polite HTTP**:
   - Custom `User-Agent` (e.g. `WebsiteWatcher/0.1 (+your-email)`).
   - 10-second timeout.
   - On `429`/`5xx`, log a warning and continue (do not crash).

6. **Exit codes**: 0 on normal stop (Ctrl-C or `--once` succeeded), 1 if the URL is malformed or the state file is unwritable.

### Non-functional

- Use the `logging` module, not `print`.
- Use `pathlib.Path` for the state and log files.
- If `--once` is passed, no `while True` loop.
- Make the script importable: only call `main()` under `if __name__ == "__main__":`.

---

## Suggested implementation outline

```python
import argparse, hashlib, json, logging, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests


def fetch_hash(url: str) -> tuple[str, int]:
    ...


def load_state(path: Path) -> dict:
    ...


def save_state(path: Path, state: dict) -> None:
    ...


def check_once(url: str, state_path: Path) -> bool:
    """Return True if the content changed."""
    ...


def main(argv=None) -> int:
    ...
```

---

## Stretch goals

1. **Diff preview**: when content changes, store the previous body and print a `difflib.unified_diff` summary.
2. **Multiple URLs**: accept a list of URLs (from a file) and watch all of them.
3. **Notifications**: on change, send a desktop notification (use `osascript` on macOS, `notify-send` on Linux, `winotify` on Windows) or an email via `smtplib`.
4. **Backoff**: on repeated 5xx, double the interval up to a cap.

---

## Manual test plan

1. Run with a stable page (e.g. `https://example.com/`). First run logs `CHECK ... (new)`. Second run logs `CHECK ... (unchanged)`.
2. Modify the state file's `hash` to a fake value. Next run should log `CHANGE`.
3. Run with `--once` — script should exit immediately after one check.
4. Point it at a 404 URL — should log a WARNING and continue (or exit gracefully if `--once`).

---

## Rubric (10 pts)

| Category                           | Pts |
|------------------------------------|-----|
| Correctly detects changes          | 3   |
| CLI surface matches spec           | 2   |
| Polite HTTP (UA, timeout, errors)  | 2   |
| State persistence works            | 1   |
| Code uses `logging` + `pathlib`    | 1   |
| README / docstring clear           | 1   |
