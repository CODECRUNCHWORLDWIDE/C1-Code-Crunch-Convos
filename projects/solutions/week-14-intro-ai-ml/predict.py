"""Score a single SMS message with the saved spam pipeline.

Usage:
    python predict.py "Congratulations! You won a free cruise. Click here."
    echo "Are you home for dinner?" | python predict.py
    python predict.py --model model.joblib --threshold 0.3 "text here"

Exit codes: 0 = classified, 1 = bad input or missing model, 2 = argparse error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib

LABELS = {0: "ham", 1: "spam"}


def read_message(argv_text: str | None) -> str:
    """argv[1] if given, otherwise stdin. Empty input is an error, not a crash."""
    if argv_text is not None:
        message = argv_text
    elif not sys.stdin.isatty():
        message = sys.stdin.read()
    else:
        raise ValueError("no message given — pass one as an argument or pipe it on stdin")

    message = message.strip()
    if not message:
        raise ValueError("empty message")
    return message


def classify(pipe, message: str, threshold: float) -> tuple[str, float]:
    """Return (label, P(spam)). Falls back to a hard label if the model has no probabilities."""
    if hasattr(pipe, "predict_proba"):
        spam_index = list(pipe.classes_).index(1)
        proba = float(pipe.predict_proba([message])[0][spam_index])
        return LABELS[int(proba >= threshold)], proba

    hard = int(pipe.predict([message])[0])
    return LABELS[hard], float(hard)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Classify one SMS message as spam or ham.")
    parser.add_argument("message", nargs="?", help="the message; omit to read stdin")
    parser.add_argument("--model", type=Path, default=Path("model.joblib"))
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="P(spam) at or above this is called spam (default 0.5)")
    parser.add_argument("--quiet", action="store_true", help="print only the label")
    args = parser.parse_args(argv)

    if not args.model.exists():
        print(f"error: {args.model} not found — run train.py first", file=sys.stderr)
        return 1

    try:
        message = read_message(args.message)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    pipe = joblib.load(args.model)
    label, proba = classify(pipe, message, args.threshold)

    if args.quiet:
        print(label)
    else:
        print(f"{label:<4} (probability {proba:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
