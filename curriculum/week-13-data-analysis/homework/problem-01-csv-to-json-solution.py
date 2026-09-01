"""hw-01-csv-to-json.py — convert a delimited text file to JSON records.

Usage:
    python hw-01-csv-to-json.py data/sales.csv        # -> data/sales.json
    python hw-01-csv-to-json.py data/sales.tsv        # -> data/sales.json

Bonus behaviour: .tsv input is read with a tab separator, and every numeric
column is rounded to two decimals before writing.

Run with no argument (as the automated check does) it builds a sample sheet in a
throwaway temporary directory, converts it, prints the JSON, and cleans up — so
the download runs anywhere with nothing set up beforehand.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

SEPARATORS = {".csv": ",", ".tsv": "\t"}

#: A sample sheet with three-decimal prices, so the rounding bonus visibly fires.
SAMPLE_CSV = (
    "order_id,product,region,units,unit_price\n"
    "1001,Widget,North,3,9.995\n"
    "1002,Gadget,South,1,24.5\n"
    "1003,Widget,East,12,9.995\n"
    "1004,Doohickey,North,7,4.333\n"
)


def read_table(path: Path) -> pd.DataFrame:
    """Read a .csv or .tsv into a DataFrame, choosing the separator by suffix."""
    suffix = path.suffix.lower()
    if suffix not in SEPARATORS:
        raise ValueError(f"expected a .csv or .tsv file, got {path.suffix!r}")
    return pd.read_csv(path, sep=SEPARATORS[suffix])


def round_numeric(df: pd.DataFrame, places: int = 2) -> pd.DataFrame:
    """Return a copy with every float column rounded to `places` decimals."""
    return df.round({c: places for c in df.select_dtypes("float").columns})


def convert(src: Path) -> Path:
    """Write `src` out as JSON records next to it and return the new path."""
    df = round_numeric(read_table(src))
    dest = src.with_suffix(".json")
    df.to_json(dest, orient="records", indent=2)
    return dest


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        src = Path(argv[1])
        if not src.is_file():
            print(f"error: no such file: {src}", file=sys.stderr)
            return 1
        try:
            dest = convert(src)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(f"wrote {dest} ({dest.stat().st_size:,} bytes)")
        return 0

    # No argument: build the sample in a temp dir so the download runs anywhere.
    with tempfile.TemporaryDirectory() as workspace:
        src = Path(workspace) / "sales.csv"
        src.write_text(SAMPLE_CSV, encoding="utf-8")
        dest = convert(src)
        print(f"wrote {dest.name} from {src.name}")
        print(dest.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
