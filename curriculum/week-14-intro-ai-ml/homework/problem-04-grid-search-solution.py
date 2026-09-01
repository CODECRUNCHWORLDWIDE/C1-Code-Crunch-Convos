"""problem-04-grid-search.py — tune a k-NN with GridSearchCV, then check the estimate.

Grid-searches a StandardScaler -> KNeighborsClassifier pipeline over neighbours,
weighting and distance metric on the bundled digits dataset, with 5-fold
cross-validation. Then it scores the best estimator on a held-out test set the
search never touched, to see whether the CV estimate held up. Every seed is
pinned; the search itself is deterministic.

Run it with::

    python problem-04-grid-search-solution.py
"""

from __future__ import annotations

from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def build_search() -> GridSearchCV:
    """A scaler + k-NN pipeline wrapped in a 5-fold grid search."""
    pipe = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("knn", KNeighborsClassifier()),
        ]
    )
    param_grid = {
        "knn__n_neighbors": [1, 3, 5, 7, 9, 15, 21],
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan"],
    }
    return GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=1)


def main() -> None:
    """Split, grid-search on the training half, then test the winner."""
    digits = load_digits()
    x, y = digits.data, digits.target
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )
    print(f"images: {len(x)}   train: {len(x_train)}   test: {len(x_test)}")

    search = build_search()
    search.fit(x_train, y_train)

    print(f"combinations tried: {len(search.cv_results_['params'])}  (x 5 folds)")
    print("best parameters:")
    for name, value in sorted(search.best_params_.items()):
        print(f"  {name} = {value}")
    print(f"best 5-fold CV accuracy: {search.best_score_:.3f}")

    test_accuracy = search.score(x_test, y_test)
    print(f"held-out test accuracy : {test_accuracy:.3f}")
    print(f"test - CV gap: {test_accuracy - search.best_score_:+.3f}")


if __name__ == "__main__":
    main()
