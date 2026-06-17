"""Exercise 05 — Confusion matrix: read the off-diagonals.

Goals:
  * Train a classifier on a multi-class dataset.
  * Print and interpret a confusion matrix.
  * Compare classification_report with raw accuracy.

Run:
    python exercise-05-confusion-matrix.py
"""

from __future__ import annotations

from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def pretty_print_confusion(cm, class_labels: list[str]) -> None:
    """Print a confusion matrix with row/column headers."""
    header = "actual\\pred  " + " ".join(f"{c:>4s}" for c in class_labels)
    print(header)
    for row_label, row in zip(class_labels, cm):
        formatted_row = " ".join(f"{int(v):>4d}" for v in row)
        print(f"{row_label:>11s}  {formatted_row}")


def main() -> None:
    # The digits dataset: 8x8 grayscale images of handwritten digits 0-9,
    # flattened to 64 features. 1,797 samples, 10 classes.
    digits = load_digits(as_frame=True)
    X, y = digits.data, digits.target
    class_labels = [str(c) for c in sorted(y.unique())]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipe = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000)),
        ]
    )
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)

    print(f"Accuracy on test: {accuracy_score(y_test, preds):.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, preds, target_names=class_labels))

    cm = confusion_matrix(y_test, preds)
    print("Confusion matrix (rows = actual, columns = predicted):")
    pretty_print_confusion(cm, class_labels)

    # Find the worst off-diagonal: which true class gets confused the most
    # with which predicted class?
    worst = (0, 0, -1)  # (actual, predicted, count)
    for actual in range(len(class_labels)):
        for predicted in range(len(class_labels)):
            if actual == predicted:
                continue
            count = int(cm[actual, predicted])
            if count > worst[2]:
                worst = (actual, predicted, count)

    print(
        f"\nMost-common mistake: digit {class_labels[worst[0]]} predicted as "
        f"digit {class_labels[worst[1]]} ({worst[2]} times)."
    )
    print(
        "\nInterpretation tips:\n"
        "  - The diagonal is your friend. Big numbers there = correct predictions.\n"
        "  - Off-diagonal cells tell you *which* classes the model confuses.\n"
        "  - Some confusions are intuitive (4 vs 9, 3 vs 8 in handwriting).\n"
        "    Those are usually fine. Others might reveal a feature problem.\n"
        "\n"
        "Try this next:\n"
        "  - Replace LogisticRegression with KNeighborsClassifier(n_neighbors=3).\n"
        "    Where does its confusion matrix differ?\n"
        "  - Print precision and recall *per class* and identify the weakest one.\n"
    )


if __name__ == "__main__":
    main()
