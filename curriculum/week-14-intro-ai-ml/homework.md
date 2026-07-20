# Week 14 — Homework

Six problems. Due before Week 15 begins. Each problem references concepts from one or more of the lectures, exercises, or challenges. Submit your work as Python scripts and a short `report.md` summarising your findings.

Time estimate: 4–6 hours total. Budget accordingly.

## Problem 1 — Housing regression

Use the California housing dataset from scikit-learn:

```python
from sklearn.datasets import fetch_california_housing
data = fetch_california_housing(as_frame=True)
X, y = data.data, data.target  # y is median house value in $100,000s
```

Tasks:

1. Train a `LinearRegression` baseline. Report MAE, RMSE, and R² on a held-out test set.
2. Train a `GradientBoostingRegressor`. Same metrics.
3. Which is better, and by how much? Speculate on why.

Hand-in: `hw01_housing.py` plus a paragraph in `report.md` summarising the numbers and your reasoning.

## Problem 2 — Churn classification

Build a synthetic-but-realistic churn dataset in code, then train a classifier on it.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification


def make_churn(seed: int = 42, n: int = 5000) -> pd.DataFrame:
    X, y = make_classification(
        n_samples=n,
        n_features=8,
        n_informative=4,
        n_redundant=2,
        weights=[0.85, 0.15],   # imbalanced: ~15% churn
        random_state=seed,
    )
    cols = [f"signal_{i}" for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=cols)
    df["churned"] = y
    return df
```

Tasks:

1. Train `LogisticRegression` and `RandomForestClassifier`. Compare on accuracy AND precision/recall/F1 for the *churn* class.
2. Which model would you pick if false negatives (missed churners) cost the business more than false positives? Justify.
3. Show the confusion matrix for both models.

Hand-in: `hw02_churn.py` plus a short discussion in `report.md`.

## Problem 3 — Feature importance from a tree

Train a `RandomForestClassifier` on the iris dataset. Then:

1. Print `model.feature_importances_` as a sorted list of (feature, importance) pairs.
2. Drop the *least* important feature and retrain. Did accuracy change much?
3. Drop the *most* important feature and retrain. Discuss what happens.

Hand-in: `hw03_importance.py` plus a few sentences in `report.md` reflecting on what "feature importance" actually means here (and what it does NOT mean — hint: causality).

## Problem 4 — Hyperparameter tuning with GridSearchCV

Using the digits dataset (`load_digits`), tune a `KNeighborsClassifier`:

```python
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

param_grid = {
    "n_neighbors": [1, 3, 5, 7, 9, 15, 21],
    "weights": ["uniform", "distance"],
    "metric": ["euclidean", "manhattan"],
}
```

Tasks:

1. Wrap the k-NN inside a `Pipeline` with `StandardScaler`. Grid-search over the parameter grid using 5-fold CV.
2. Report the best parameters and the best CV score.
3. Evaluate the best estimator on a held-out test set. Did it match the CV estimate?

Hand-in: `hw04_grid_search.py` plus a paragraph in `report.md` describing what changed and what didn't.

## Problem 5 — Plot a learning curve

A learning curve shows training and validation score as a function of training-set size. It tells you whether your model would benefit from more data.

Using the digits dataset and `LogisticRegression`:

```python
from sklearn.model_selection import learning_curve
import numpy as np
import matplotlib.pyplot as plt
```

Tasks:

1. Compute training and validation scores at training sizes [50, 100, 250, 500, 1000, 1500].
2. Plot two lines: train score vs size, val score vs size.
3. Interpret: is your model bottlenecked by data, or by capacity?

Hand-in: `hw05_learning_curve.py` and the resulting plot saved as `learning_curve.png`. One paragraph of interpretation in `report.md`.

## Problem 6 — Fairness audit

Pick the Titanic dataset from Challenge 01 (or the model you saved there). Perform a fairness audit:

1. After training a single binary classifier on the survival prediction task, compute on the **test set**:
   - Precision and recall for **all passengers**.
   - Precision and recall for **men only**.
   - Precision and recall for **women only**.
2. Build a small results table:

   ```text
   | group  | n | precision | recall | accuracy |
   |--------|---|-----------|--------|----------|
   | all    |   |           |        |          |
   | male   |   |           |        |          |
   | female |   |           |        |          |
   ```

3. Write 200–300 words discussing:
   - Are the group metrics meaningfully different? Why might that be?
   - Even if a model is "accurate overall", what could be problematic about deploying it for a real-world decision (e.g., evacuation prioritisation, insurance pricing)?
   - What would you want to know about the data-collection process before recommending the model be used?

Hand-in: `hw06_fairness.py` and the discussion in `report.md`. **This is the most important homework problem. Take it seriously.**

## Submission checklist

- [ ] Six Python scripts: `hw01_housing.py` ... `hw06_fairness.py`.
- [ ] One `report.md` with sections for each problem.
- [ ] `learning_curve.png` from Problem 5.
- [ ] All scripts run end-to-end with no manual edits required.
- [ ] You set `random_state` everywhere reproducibility matters.

Good luck. See you in Week 15.
