"""Exercise 02 — Iris classification with logistic regression.

Goals:
  * Load a built-in scikit-learn dataset.
  * Use train_test_split with stratification.
  * Train logistic regression and read its accuracy + per-class report.

Run:
    python exercise-02-iris-classifier.py
"""

from __future__ import annotations

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def main() -> None:
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target
    target_names = list(iris.target_names)

    print("Feature columns:", list(X.columns))
    print("Classes        :", target_names)
    print("Total samples  :", len(X))
    print()

    # Stratify so each split has the same class proportions.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # Logistic regression converges quickly on iris; bump max_iter just to
    # silence convergence warnings on any sklearn version.
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"Test-set accuracy: {acc:.4f}")
    print("\nPer-class report:")
    print(classification_report(y_test, preds, target_names=target_names))

    # Probabilities — useful when you care about confidence.
    print("First 5 test samples, predicted probabilities:")
    probs = clf.predict_proba(X_test.head())
    for actual, probs_row in zip(y_test.head(), probs):
        actual_name = target_names[int(actual)]
        formatted = ", ".join(
            f"{name}={p:.2f}" for name, p in zip(target_names, probs_row)
        )
        print(f"  actual={actual_name:12s}  {formatted}")

    print(
        "\nTry this next:\n"
        "  - Drop 'petal length (cm)' from X. Re-fit. Did accuracy change?\n"
        "  - Replace LogisticRegression with DecisionTreeClassifier(max_depth=2).\n"
        "  - Print clf.coef_ — what do the numbers mean for each class?\n"
    )


if __name__ == "__main__":
    main()
