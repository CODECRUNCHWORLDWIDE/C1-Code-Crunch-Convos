"""problem-05-learning-curve.py — does this model want more data, or a bigger brain?

A learning curve plots training and validation accuracy as the training set grows.
The real deliverable is a PNG; this course runs headless and compares text, so the
curve is printed as a table instead. Reading it: if the two lines meet low, more
data will not help (the model is too simple — underfitting); if they meet high with
a gap, more data closes the gap. Every seed is pinned.

Run it with::

    python problem-05-learning-curve-solution.py
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve

RANDOM_STATE = 42
# 5-fold CV trains on 4/5 of the 1,797 images = 1,437, so the sizes stay under that.
TRAIN_SIZES = [50, 100, 250, 500, 900, 1400]


def main() -> None:
    """Compute train and validation accuracy at growing training sizes."""
    digits = load_digits()
    x, y = digits.data, digits.target

    model = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    sizes, train_scores, val_scores = learning_curve(
        model,
        x,
        y,
        train_sizes=TRAIN_SIZES,
        cv=5,
        scoring="accuracy",
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    print("learning curve (mean accuracy across 5 folds):")
    print(f"  {'train_size':>10}  {'train_acc':>9}  {'val_acc':>7}  {'gap':>6}")
    train_mean = train_scores.mean(axis=1)
    val_mean = val_scores.mean(axis=1)
    for size, train_acc, val_acc in zip(sizes, train_mean, val_mean):
        print(f"  {size:>10}  {train_acc:>9.3f}  {val_acc:>7.3f}  {train_acc - val_acc:>6.3f}")

    print(f"validation accuracy went from {val_mean[0]:.3f} at {sizes[0]} rows "
          f"to {val_mean[-1]:.3f} at {sizes[-1]} rows")
    verdict = (
        "still rising — more data would likely help"
        if val_mean[-1] - val_mean[-2] > 0.005
        else "flattening — the curve has mostly levelled off"
    )
    print(f"the validation line is {verdict}")


if __name__ == "__main__":
    main()
