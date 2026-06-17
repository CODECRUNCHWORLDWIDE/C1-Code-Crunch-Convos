"""Mini-project starter — SMS Spam Classifier.

This file gives you the skeleton of a training script. Fill in the TODOs.

Usage:
    python starter.py sample-data.csv

After training, write a separate predict.py CLI that:
    1. Loads model.joblib.
    2. Reads a message from argv or stdin.
    3. Prints "spam" or "ham" and the predicted probability of spam.

Requirements (from README.md):
    - Compare >= 3 classifiers.
    - Report precision, recall, F1, and a confusion matrix.
    - Save the best pipeline with joblib.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


MODEL_PATH = Path("model.joblib")


def load_data(csv_path: str | Path) -> tuple[pd.Series, pd.Series]:
    """Load the CSV and return (texts, labels).

    Expected columns: `label` (spam/ham) and `text`.

    TODO:
        - Read the CSV with pandas.
        - Return df["text"] and df["label"].
        - Optionally: lower-case the labels, drop rows with missing text.
    """
    df = pd.read_csv(csv_path)
    # TODO: validate columns and clean as needed.
    return df["text"], df["label"]


def build_pipeline(classifier: Any) -> Pipeline:
    """Build a TfidfVectorizer + classifier pipeline.

    TODO:
        - Configure TfidfVectorizer (lowercase, stop_words, ngram_range, etc.).
        - Return a Pipeline with two steps: ("tfidf", vectorizer), ("clf", classifier).
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
    )
    return Pipeline(steps=[("tfidf", vectorizer), ("clf", classifier)])


def evaluate(name: str, pipe: Pipeline, X_test, y_test) -> float:
    """Print classification report + confusion matrix. Return F1 for spam class."""
    preds = pipe.predict(X_test)
    print(f"\n=== {name} ===")
    print(classification_report(y_test, preds, digits=3))
    print("Confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_test, preds, labels=["ham", "spam"]))
    # F1 with respect to the "spam" class.
    return float(f1_score(y_test, preds, pos_label="spam"))


def train_and_select_best(csv_path: str | Path) -> Pipeline:
    """Train multiple classifiers and return the best pipeline."""
    X, y = load_data(csv_path)
    print(f"Loaded {len(X)} messages.")
    print(f"Label distribution:\n{y.value_counts()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    candidates: dict[str, Any] = {
        "logreg": LogisticRegression(max_iter=1000),
        "naive_bayes": MultinomialNB(),
        "decision_tree": DecisionTreeClassifier(max_depth=10, random_state=42),
    }

    best_pipe: Pipeline | None = None
    best_name: str = ""
    best_f1: float = -1.0

    for name, classifier in candidates.items():
        pipe = build_pipeline(classifier)
        pipe.fit(X_train, y_train)
        f1 = evaluate(name, pipe, X_test, y_test)
        if f1 > best_f1:
            best_f1 = f1
            best_pipe = pipe
            best_name = name

    assert best_pipe is not None
    print(f"\nBest model: {best_name} with spam F1 = {best_f1:.3f}")
    return best_pipe


def save_model(pipe: Pipeline, path: Path = MODEL_PATH) -> None:
    """Persist the pipeline (vectorizer + classifier) to disk."""
    joblib.dump(pipe, path)
    print(f"Saved model to {path.resolve()}")


def predict_single(message: str, path: Path = MODEL_PATH) -> tuple[str, float]:
    """Load the saved pipeline and classify a single message.

    Returns:
        (label, probability_of_spam)
    """
    pipe: Pipeline = joblib.load(path)
    label = pipe.predict([message])[0]
    # predict_proba columns are aligned with pipe.classes_
    classes = list(pipe.classes_)
    spam_idx = classes.index("spam")
    proba = float(pipe.predict_proba([message])[0][spam_idx])
    return str(label), proba


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python starter.py path/to/data.csv", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]
    best = train_and_select_best(csv_path)
    save_model(best)

    # Smoke-test the saved model.
    sample = "Congratulations! You have won a free iPhone. Click http://x.y/z"
    label, proba = predict_single(sample)
    print(f"\nSmoke test: {sample!r}")
    print(f"  -> {label} (P(spam)={proba:.3f})")


if __name__ == "__main__":
    main()
