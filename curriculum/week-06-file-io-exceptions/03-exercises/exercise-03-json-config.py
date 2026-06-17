"""Exercise 03 — JSON config edit.

Topic: json.load / json.dump, pretty-printing.
Reference: lecture-notes/02-csv-and-json.md sections 5 and 6.

Task
----
Implement two functions:

  * `load_config(path)` — read a JSON file at `path` and return a dict.
    If the file does not exist, return a default config (see DEFAULT below).

  * `save_config(path, config)` — write the config dict to `path` as
    pretty-printed JSON (indent=2, keys sorted, utf-8).

Then in `__main__`, run a full round-trip:

  1. Save the DEFAULT config.
  2. Load it back.
  3. Toggle the `debug` flag.
  4. Save it again.
  5. Print the file contents so you can confirm `debug` was toggled.

Expected output (truncated):

    --- config.json ---
    {
      "database": {
        "host": "localhost",
        "port": 5432
      },
      "debug": true,
      "log_level": "INFO"
    }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT: dict[str, Any] = {
    "log_level": "INFO",
    "debug": False,
    "database": {
        "host": "localhost",
        "port": 5432,
    },
}


def load_config(path: Path) -> dict[str, Any]:
    """Load a JSON config file; return DEFAULT if it does not exist."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # First-run case — return a copy so callers can mutate it
        # without affecting DEFAULT itself.
        return dict(DEFAULT)


def save_config(path: Path, config: dict[str, Any]) -> None:
    """Save `config` to `path` as pretty-printed JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)
        f.write("\n")   # POSIX-friendly trailing newline


if __name__ == "__main__":
    here = Path(__file__).parent
    path = here / "config.json"

    # Step 1 — write the default config out.
    save_config(path, DEFAULT)

    # Step 2-4 — load, mutate, save.
    cfg = load_config(path)
    cfg["debug"] = not cfg["debug"]
    save_config(path, cfg)

    # Step 5 — show the result.
    print("--- config.json ---")
    print(path.read_text(encoding="utf-8"), end="")
