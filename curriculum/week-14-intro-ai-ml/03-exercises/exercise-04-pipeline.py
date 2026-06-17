"""Exercise 04 — Build a Pipeline: StandardScaler -> LogisticRegression.

Goals:
  * Wire preprocessing and a model into a single Pipeline.
  * See that the pipeline is itself an estimator (fit, predict, score).
  * Notice the leakage trap that pipelines prevent.

Run:
    python exercise-04-pipeline.py
"""

from __future__ import annotations

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def make_pipeline() -> Pipeline:
    """Build a fresh preprocessing + model pipeline."""
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )


def main() -> None:
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    pipe = make_pipeline()
    pipe.fit(X_train, y_train)

    print("Pipeline:")
    print(pipe)
    print()
    print(f"Train accuracy: {pipe.score(X_train, y_train):.4f}")
    print(f"Test  accuracy: {pipe.score(X_test, y_test):.4f}")

    # The pipeline behaves like a single estimator. Predicting on raw,
    # un-scaled data works because the scaler step runs first internally.
    sample = X_test.head(3)
    print("\nPredictions on three raw test samples:")
    for idx, pred in zip(sample.index, pipe.predict(sample)):
        actual = y_test.loc[idx]
        print(
            f"  row {idx}: predicted={iris.target_names[int(pred)]:12s}"
            f"  actual={iris.target_names[int(actual)]}"
        )

    # Use the pipeline inside cross_val_score. This is the *honest* way:
    # the scaler is re-fit on each training fold, not the whole dataset.
    cv = cross_val_score(make_pipeline(), X, y, cv=5, scoring="accuracy")
    print(f"\n5-fold CV accuracy: mean={cv.mean():.4f}, std={cv.std():.4f}")

    print(
        "\nKey takeaway:\n"
        "  - Without a pipeline, students often call scaler.fit_transform(X)\n"
        "    on the whole dataset before splitting. That leaks test-set info\n"
        "    into training. Reported accuracy will be optimistic.\n"
        "  - With a pipeline, the scaler only ever sees training data. Honest.\n"
        "\n"
        "Try this next:\n"
        "  - Swap LogisticRegression for KNeighborsClassifier. Compare scores\n"
        "    with and without the StandardScaler step. k-NN should benefit\n"
        "    much more from scaling than logistic regression does.\n"
    )


if __name__ == "__main__":
    main()
