"""Download and cache the pinned OWID CO2 dataset used by analysis.ipynb.

The notebook is the narrative; this module is the plumbing. Keeping the
download here means the notebook's Load section is three lines instead of
thirty, and it means the data-integrity check lives in one place.

Two things make this reproducible rather than merely convenient:

1. The URL points at a **commit SHA**, not at `master`. OWID rebuilds
   `owid-co2-data.csv` every few months; a `master` URL would silently change
   every number in this analysis. A commit URL never changes.
2. The download is checked against a SHA-256 digest. If the bytes are not the
   bytes this analysis was written against, you get an exception instead of
   quietly different results.

Run it directly to warm the cache before opening the notebook:

    python fetch_data.py
"""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

import pandas as pd

# OWID co2-data, commit 382ee6c (2026-06-02, "Update EIA data ...").
# Browse the repo at https://github.com/owid/co2-data
COMMIT = "382ee6c662b0ece26e111f263b44c029afad7787"
URL = f"https://raw.githubusercontent.com/owid/co2-data/{COMMIT}/owid-co2-data.csv"

EXPECTED_SHA256 = "7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6"
EXPECTED_BYTES = 14_377_942

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "owid-co2-data.csv"


def _sha256(path: Path) -> str:
    """SHA-256 of a file, read in 1 MiB chunks so a big file never blows up RAM."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(force: bool = False) -> Path:
    """Ensure the pinned CSV is on disk and has the expected contents.

    Returns the path to the cached file. Downloads only if the file is
    missing, the wrong size, or `force=True`.
    """
    DATA_DIR.mkdir(exist_ok=True)

    needs_download = force or not CSV_PATH.exists()
    if not needs_download and CSV_PATH.stat().st_size != EXPECTED_BYTES:
        print(f"Cached file is {CSV_PATH.stat().st_size} bytes, expected "
              f"{EXPECTED_BYTES}. Re-downloading.")
        needs_download = True

    if needs_download:
        print(f"Downloading {EXPECTED_BYTES / 1e6:.1f} MB from {URL} ...")
        urllib.request.urlretrieve(URL, CSV_PATH)

    actual = _sha256(CSV_PATH)
    if actual != EXPECTED_SHA256:
        raise RuntimeError(
            "Checksum mismatch for the OWID CO2 dataset.\n"
            f"  expected {EXPECTED_SHA256}\n"
            f"  got      {actual}\n"
            "Delete data/owid-co2-data.csv and try again. If it still fails, "
            "the pinned commit no longer resolves and the numbers in "
            "findings.md may not reproduce."
        )
    return CSV_PATH


def load_raw() -> pd.DataFrame:
    """Return the full, untouched OWID CO2 table (50,411 rows x 79 columns)."""
    return pd.read_csv(download())


if __name__ == "__main__":
    path = download(force="--force" in sys.argv)
    print(f"OK  {path}")
    print(f"    {path.stat().st_size:,} bytes")
    print(f"    sha256 {EXPECTED_SHA256}")
