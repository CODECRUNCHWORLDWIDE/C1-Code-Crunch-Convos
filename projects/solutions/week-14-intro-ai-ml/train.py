"""Train, compare, and persist an SMS spam classifier.

Usage:
    python train.py sample-data.csv
    python train.py sms-spam-synthetic.csv --top-features 15
    python train.py sms-spam-synthetic.csv --criterion recall --out model.joblib

Every candidate is a single `Pipeline` (TfidfVectorizer -> classifier), so the
vectoriser is fit on the training fold only. There is no way to leak test
vocabulary into training without deleting a line of this file on purpose.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42
POSITIVE = "spam"


@dataclass(frozen=True)
class Result:
    name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    cv_f1_mean: float
    cv_f1_std: float
    confusion: tuple[int, int, int, int]  # tn, fp, fn, tp


def load_data(path: Path) -> pd.DataFrame:
    """Read the two-column CSV and fail loudly on anything malformed."""
    df = pd.read_csv(path)
    missing = {"label", "text"} - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing column(s) {sorted(missing)}; expected label,text")

    df = df.dropna(subset=["label", "text"]).copy()
    df["label"] = df["label"].str.strip().str.lower()
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"] != ""]

    bad = set(df["label"]) - {"spam", "ham"}
    if bad:
        raise ValueError(f"{path}: unexpected label(s) {sorted(bad)}; expected only spam/ham")
    if df["label"].nunique() < 2:
        raise ValueError(f"{path}: needs both spam and ham rows to train a classifier")
    return df.reset_index(drop=True)


def build_candidates(bigrams: bool) -> dict[str, Pipeline]:
    """One Pipeline per candidate. Same vectoriser settings across all of them."""
    ngram_range = (1, 2) if bigrams else (1, 1)

    def vectoriser() -> TfidfVectorizer:
        # A fresh instance per pipeline: sharing one transformer object between
        # estimators means the second fit silently overwrites the first.
        return TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=ngram_range,
            sublinear_tf=True,
        )

    return {
        "logreg": Pipeline([
            ("tfidf", vectoriser()),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced",
                                       random_state=RANDOM_STATE)),
        ]),
        "naive_bayes": Pipeline([
            ("tfidf", vectoriser()),
            ("clf", MultinomialNB(alpha=0.1)),
        ]),
        "random_forest": Pipeline([
            ("tfidf", vectoriser()),
            ("clf", RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE,
                                           class_weight="balanced_subsample")),
        ]),
    }


def evaluate(name: str, pipe: Pipeline, X_train, X_test, y_train, y_test,
             cv_splits: int) -> Result:
    cv_mean = cv_std = float("nan")
    if cv_splits >= 2:
        cv = cross_val_score(
            pipe, X_train, y_train,
            cv=StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=RANDOM_STATE),
            scoring="f1",
        )
        cv_mean, cv_std = float(cv.mean()), float(cv.std())

    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, preds, labels=[0, 1]).ravel()

    return Result(
        name=name,
        accuracy=float(accuracy_score(y_test, preds)),
        precision=float(precision_score(y_test, preds, zero_division=0)),
        recall=float(recall_score(y_test, preds, zero_division=0)),
        f1=float(f1_score(y_test, preds, zero_division=0)),
        cv_f1_mean=cv_mean,
        cv_f1_std=cv_std,
        confusion=(int(tn), int(fp), int(fn), int(tp)),
    )


def print_report(result: Result, y_test, preds) -> None:
    tn, fp, fn, tp = result.confusion
    print("\n" + "=" * 64)
    print(f"MODEL: {result.name}")
    print("=" * 64)
    print(classification_report(y_test, preds, target_names=["ham", "spam"],
                                digits=3, zero_division=0))
    print("Confusion matrix (rows = actual ham/spam, cols = predicted):")
    print(f"  [[{tn:4d} {fp:4d}]     TN={tn}  FP={fp}  (ham wrongly binned)")
    print(f"   [{fn:4d} {tp:4d}]]    FN={fn}  TP={tp}  (spam that got through)")
    if result.cv_f1_mean == result.cv_f1_mean:  # not NaN
        print(f"5-fold CV F1 on train: {result.cv_f1_mean:.3f} +/- {result.cv_f1_std:.3f}")


def top_features(pipe: Pipeline, k: int) -> None:
    """Print the tokens most associated with each class, if the model exposes them."""
    clf = pipe.named_steps["clf"]
    names = pipe.named_steps["tfidf"].get_feature_names_out()

    if hasattr(clf, "coef_"):
        weights = clf.coef_[0]
        label = "logistic-regression coefficient"
    elif hasattr(clf, "feature_log_prob_"):
        weights = clf.feature_log_prob_[1] - clf.feature_log_prob_[0]
        label = "naive-Bayes log-odds"
    elif hasattr(clf, "feature_importances_"):
        weights = clf.feature_importances_
        label = "impurity importance (unsigned)"
    else:
        print("this classifier exposes no per-token weights")
        return

    order = weights.argsort()
    print(f"\n=== top {k} spam-leaning tokens ({label}) ===")
    for i in order[::-1][:k]:
        print(f"  {names[i]:<24} {weights[i]:+.3f}")
    if label != "impurity importance (unsigned)":
        print(f"\n=== top {k} ham-leaning tokens ===")
        for i in order[:k]:
            print(f"  {names[i]:<24} {weights[i]:+.3f}")


def log_run(path: Path, data_path: Path, result: Result, criterion: str, bigrams: bool) -> None:
    """Append one row per training run so you can watch your own progress."""
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new:
            writer.writerow(["timestamp", "data", "model", "criterion", "bigrams",
                             "accuracy", "precision", "recall", "f1"])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            data_path.name, result.name, criterion, bigrams,
            f"{result.accuracy:.4f}", f"{result.precision:.4f}",
            f"{result.recall:.4f}", f"{result.f1:.4f}",
        ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train an SMS spam classifier.")
    parser.add_argument("data", type=Path, help="CSV with label,text columns")
    parser.add_argument("--out", type=Path, default=Path("model.joblib"))
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--criterion", choices=["f1", "recall", "precision"], default="f1",
                        help="which test-set metric on the spam class picks the winner")
    parser.add_argument("--no-bigrams", action="store_true",
                        help="unigrams only; default is ngram_range=(1, 2)")
    parser.add_argument("--top-features", type=int, metavar="K", default=0,
                        help="print the K most spam- and ham-leaning tokens")
    parser.add_argument("--log", type=Path, default=Path("runs.csv"))
    args = parser.parse_args(argv)

    if not args.data.exists():
        print(f"error: {args.data} not found", file=sys.stderr)
        return 1

    try:
        df = load_data(args.data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    X = df["text"]
    y = (df["label"] == POSITIVE).astype(int)  # spam = 1, ham = 0

    print(f"loaded {len(df)} messages from {args.data}")
    print(f"  ham : {int((y == 0).sum())}")
    print(f"  spam: {int((y == 1).sum())} ({y.mean():.1%})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=RANDOM_STATE, stratify=y
    )
    print(f"train: {len(X_train)}  test: {len(X_test)} "
          f"({int(y_test.sum())} spam in test)")

    # Never ask for more folds than the rarest class has training examples.
    cv_splits = min(5, int(y_train.value_counts().min()))
    if cv_splits < 5:
        print(f"note: only {cv_splits} usable CV folds — the minority class is tiny here")

    results: list[Result] = []
    fitted: dict[str, Pipeline] = {}
    for name, pipe in build_candidates(bigrams=not args.no_bigrams).items():
        result = evaluate(name, pipe, X_train, X_test, y_train, y_test, cv_splits)
        print_report(result, y_test, pipe.predict(X_test))
        results.append(result)
        fitted[name] = pipe

    table = pd.DataFrame([{
        "model": r.name, "accuracy": r.accuracy, "precision": r.precision,
        "recall": r.recall, "f1": r.f1, "cv_f1": r.cv_f1_mean,
        "FP": r.confusion[1], "FN": r.confusion[2],
    } for r in results]).set_index("model").round(3)
    print("\n=== comparison (spam = positive class) ===")
    print(table.to_string())

    best = max(results, key=lambda r: getattr(r, args.criterion))
    print(f"\nselection criterion: highest {args.criterion} on the spam class")
    print(f"winner: {best.name} "
          f"(precision {best.precision:.3f}, recall {best.recall:.3f}, F1 {best.f1:.3f})")

    if args.top_features:
        top_features(fitted[best.name], args.top_features)

    print("\n=== misclassified test messages ===")
    preds = fitted[best.name].predict(X_test)
    wrong = X_test[preds != y_test]
    if wrong.empty:
        print("  none")
    for idx, text in wrong.items():
        kind = "FALSE POSITIVE (ham -> spam)" if y.loc[idx] == 0 else "FALSE NEGATIVE (spam -> ham)"
        print(f"  {kind}: {text[:88]}")

    joblib.dump(fitted[best.name], args.out)
    print(f"\nwrote {args.out}")

    reloaded = joblib.load(args.out)
    identical = bool((reloaded.predict(X_test) == preds).all())
    print(f"reload check: predictions identical -> {identical}")
    if not identical:
        print("error: the reloaded pipeline disagrees with the in-memory one", file=sys.stderr)
        return 1

    log_run(args.log, args.data, best, args.criterion, not args.no_bigrams)
    print(f"appended one row to {args.log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
