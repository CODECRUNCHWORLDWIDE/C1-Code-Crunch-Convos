"""exercise-03-json-config-solution.py — load a JSON config, edit it, write it back.

Enables the comments feature, adds the Nairobi chapter, and raises the upload
cap. Re-running the script leaves the file byte-for-byte unchanged.

The file you write yourself keeps its sample config in a ``data/`` folder next
to the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact config the page gives
you, so the download runs on any machine with nothing set up beforehand. It
then applies the changes twice and hashes the file in between, because
"running it twice changes nothing" is the property this exercise is really
about. Everything from ``load_config`` to ``apply_changes`` is the exercise.

Run it with::

    python exercise-03-json-config-solution.py
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

NEW_MAX_UPLOAD_MB = 10

#: The config exactly as the exercise page gives it.
SAMPLE_CONFIG = """{
  "site_name": "Code Crunch Worldwide",
  "theme": "light",
  "features": {
    "newsletter": true,
    "comments": false
  },
  "chapters": ["Lagos", "Manila", "Bogota"],
  "max_upload_mb": 5
}
"""


def load_config(path: Path) -> dict:
    """Read the JSON file at *path* and return it as a dict."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def set_feature(config: dict, name: str, enabled: bool) -> bool:
    """Set config["features"][name] to *enabled*.

    Returns:
        True if the value changed, False if it was already correct.

    Raises:
        KeyError: if *name* is not an existing feature.
    """
    features = config["features"]
    if name not in features:
        raise KeyError(name)
    if features[name] == enabled:
        return False
    features[name] = enabled
    return True


def add_chapter(config: dict, name: str) -> bool:
    """Append *name* to config["chapters"] unless it is already listed.

    Returns:
        True if the chapter was added, False if it was already there.
    """
    chapters = config["chapters"]
    if name in chapters:
        return False
    chapters.append(name)
    return True


def save_config(config: dict, path: Path) -> None:
    """Write *config* back to *path* as sorted, indented JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)
        f.write("\n")


def apply_changes(path: Path) -> None:
    """Apply this month's config changes to the file at *path*, reporting each."""
    config = load_config(path)
    print(f"Loaded {len(config)} top-level keys from {path.name}")

    if set_feature(config, "comments", True):
        print("Enabled feature: comments")
    else:
        print("Feature already enabled: comments")

    for chapter in ("Nairobi", "Lagos"):
        if add_chapter(config, chapter):
            print(f"Added chapter: {chapter}")
        else:
            print(f"Chapter already listed: {chapter}")

    old_cap = config["max_upload_mb"]
    if old_cap < NEW_MAX_UPLOAD_MB:
        config["max_upload_mb"] = NEW_MAX_UPLOAD_MB
        print(f"Raised max_upload_mb from {old_cap} to {NEW_MAX_UPLOAD_MB}")
    else:
        print(f"max_upload_mb already at {old_cap}")

    save_config(config, path)
    print(f"Wrote {path.name}")


def digest(path: Path) -> str:
    """Return the SHA-256 of the raw bytes of *path*, as hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_sample(folder: Path) -> Path:
    """Write the sample site config into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "site-config.json"
    path.write_text(SAMPLE_CONFIG, encoding="utf-8")
    return path


def main() -> None:
    """Apply the changes twice and prove the second run changed nothing."""
    with tempfile.TemporaryDirectory() as workspace:
        config_path = build_sample(Path(workspace) / "data")

        print("--- first run ---")
        apply_changes(config_path)
        after_first = digest(config_path)

        print()
        print("--- second run ---")
        apply_changes(config_path)
        after_second = digest(config_path)

        print()
        print(f"byte-identical after the second run: {after_first == after_second}")

        print()
        print(f"--- {config_path.name} ---")
        print(config_path.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
