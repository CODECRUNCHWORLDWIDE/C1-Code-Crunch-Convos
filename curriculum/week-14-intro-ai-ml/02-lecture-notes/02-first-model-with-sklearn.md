# Lecture 2 — Your first model with scikit-learn

## Read time

About 45 minutes (includes running the code).

You read Lecture 1, you nodded along, you are itching to write code. Good. This lecture is mostly code, with explanations between the snippets.

Run every snippet. Reading without running is reading; running is learning.

## The scikit-learn promise: one API for everything

scikit-learn (often `sklearn`) is the most important library in the Python ML ecosystem. Even when teams use PyTorch or TensorFlow for deep learning, they almost always reach for sklearn for preprocessing, splitting, and evaluation. Learning sklearn well buys you a lot.

The library's superpower is a tiny, consistent API. Almost everything in sklearn is one of two things:

- **An estimator.** Has a `.fit(X, y)` method. Produces predictions via `.predict(X)`. Examples: `LinearRegression`, `LogisticRegression`, `DecisionTreeClassifier`, `KMeans`.
- **A transformer.** Has a `.fit(X)` and `.transform(X)` method (or `.fit_transform(X)` as a shortcut). Examples: `StandardScaler`, `OneHotEncoder`, `TfidfVectorizer`.

That is the whole API surface for everyday use. When you see a new class, your first question is: estimator or transformer? Once you know, you know how to use it.

```python
# Estimators look like this:
model = SomeEstimator(hyperparameters)
model.fit(X_train, y_train)
preds = model.predict(X_test)

# Transformers look like this:
scaler = SomeTransformer()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)   # IMPORTANT: only fit on train.
```

A few classes are both (e.g., `PCA`). A few have extra methods (`predict_proba` on classifiers, for probability estimates). But this is the spine.

## Notation conventions

Throughout sklearn (and ML in general):

- **`X`** — capital X. The feature matrix. Shape `(n_samples, n_features)`. Rows are examples, columns are features.
- **`y`** — lowercase y. The target vector. Shape `(n_samples,)`. One value per row of X.
- **`X_train`, `X_test`, `y_train`, `y_test`** — what `train_test_split` returns.

If you ever see `model.fit(y, X)` somewhere, that code is wrong. `fit(X, y)`. Always.

## Hands-on 1: linear regression on a tiny dataset

Let's predict house price from square footage. We will use a hand-rolled toy dataset so the numbers are obvious.

```python
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# Tiny toy dataset: square feet -> price in thousands of dollars.
data = pd.DataFrame(
    {
        "sqft": [650, 800, 950, 1100, 1250, 1400, 1550, 1700, 1850, 2000,
                 2150, 2300, 2450, 2600, 2750, 2900, 3050, 3200, 3350, 3500],
        "price_k": [142, 168, 195, 218, 244, 266, 291, 311, 339, 360,
                    382, 410, 431, 460, 484, 512, 533, 561, 588, 613],
    }
)

X = data[["sqft"]]      # 2D
y = data["price_k"]     # 1D

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("slope:", float(model.coef_[0]))
print("intercept:", float(model.intercept_))
print("MAE:", mean_absolute_error(y_test, preds))
print("R^2:", r2_score(y_test, preds))
```

Things to notice:

- `X` is a **DataFrame** (2D). sklearn requires 2D for features. `data["sqft"]` would be 1D and would error. The double brackets `data[["sqft"]]` keep it 2D.
- `y` is a **Series** (1D). That's correct.
- `train_test_split` with `random_state=42` makes the split reproducible. Without a `random_state`, you'd get a different split every run, and your numbers would jitter.
- `model.coef_` and `model.intercept_` are the parameters the model learned. For a single feature, you can read them as "price per extra square foot" and "base price". Read them. They will make sense.
- MAE (mean absolute error) is in the same units as `y` (thousands of dollars). R² is a unitless goodness-of-fit score; 1.0 is perfect, 0.0 is "as good as predicting the mean", negative is "worse than predicting the mean". This tiny dataset should give you R² ≈ 0.99 because the relationship is basically linear by construction.

## What did fit actually do?

For linear regression with one feature, sklearn solved for the `(slope, intercept)` pair that minimises the sum of squared errors on the training set. The closed-form solution exists (normal equations), and sklearn just computes it.

For more complex models, "fit" is more involved (gradient descent, tree splits, etc.). But conceptually it's always the same: adjust parameters to reduce error on the training set.

## Hands-on 2: classification with the iris dataset

Iris is the "Hello, world!" of classification. 150 flowers, 4 measurements each (sepal length, sepal width, petal length, petal width), 3 species labels. The dataset comes with sklearn.

```python
from __future__ import annotations
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


iris = load_iris(as_frame=True)
X, y = iris.data, iris.target
print(X.head())
print("classes:", list(iris.target_names))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print("accuracy:", accuracy_score(y_test, preds))
```

You should see accuracy in the high 0.9s. Iris is an easy dataset — the species are well-separated in feature space.

A couple of new things:

- `stratify=y` tells `train_test_split` to keep the class proportions the same in train and test. With three classes of 50 each, stratifying matters less, but on imbalanced data (think 99% ham / 1% spam) it matters a lot. Default to using it for classification.
- `max_iter=1000` raises the iteration limit. Logistic regression is fit by an iterative optimiser; the default 100 is sometimes too few, and sklearn warns you. Raising it removes the warning.
- `accuracy_score(y_test, preds)` is `correct / total`. Simple and intuitive. Misleading on imbalanced data, as we will see.

`clf.predict_proba(X_test)` gives you per-class probabilities — useful when you want a confidence score, not just a hard label.

## Decision trees: easy to read, easy to overfit

A decision tree is a flowchart the model learns from data. "Is petal length > 2.45? If yes, ask the next question; if no, predict setosa."

```python
from sklearn.tree import DecisionTreeClassifier, export_text


tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

print("accuracy:", tree.score(X_test, y_test))
print(export_text(tree, feature_names=list(X.columns)))
```

`export_text` prints the tree as a human-readable flow:

```text
|--- petal length (cm) <= 2.45
|   |--- class: 0
|--- petal length (cm) >  2.45
|   |--- petal width (cm) <= 1.75
|   |   |--- ...
```

The big appeal of trees: you can *read them*. Loan officer asks why an applicant got rejected — you can show them the path. Big risk of trees: they will memorise the training set if you let them. `max_depth=3` is a guardrail; without it, the tree will keep splitting until each leaf is a single example, which is textbook overfitting (covered in Lecture 3).

## k-Nearest Neighbours: no training, just memory

k-NN is the simplest "model" you will ever meet. To predict a new point's label: find the `k` most similar training points and let them vote.

```python
from sklearn.neighbors import KNeighborsClassifier


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
print("accuracy:", knn.score(X_test, y_test))
```

Notice `.fit()` here just memorises the training data. All the work happens at `.predict()`, when sklearn computes distances to every training point and picks the closest k.

Implications:

- **Training is fast, prediction is slow.** Opposite of most models.
- **Distances depend on units.** A feature measured in millimetres will dwarf one measured in meters. You must scale features before using k-NN. We will introduce `StandardScaler` in Lecture 3.
- **k matters.** Small k overfits (one weird neighbour decides everything). Large k underfits (everything looks average). Try a few.

## A quick comparison

Same iris data, three baselines, three lines each:

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


for name, model in [
    ("logreg", LogisticRegression(max_iter=1000)),
    ("tree", DecisionTreeClassifier(max_depth=3, random_state=42)),
    ("knn", KNeighborsClassifier(n_neighbors=5)),
]:
    model.fit(X_train, y_train)
    print(f"{name:7s} -> {model.score(X_test, y_test):.3f}")
```

On iris you will get three numbers around 0.95. None of these is "the right algorithm" in some absolute sense. They are all reasonable baselines. **Pick the simplest one that meets the requirement** and move on. Beginners agonise over algorithm choice and ignore data quality; senior practitioners do the opposite.

## Choosing a baseline

Whenever you start an ML project, ask:

1. What is the **dumbest model** that would partially solve this?
2. Is its score acceptable? If yes, ship it. If no, what does the error pattern look like?
3. Pick the **next-simplest** model and try it. Compare.
4. Stop the moment you have enough.

Concretely, my default playbook:

- Regression: `LinearRegression` first. Then `Ridge`. Then trees / `GradientBoostingRegressor`.
- Classification: `LogisticRegression` first. Then `DecisionTreeClassifier`. Then `RandomForestClassifier` or `GradientBoostingClassifier`.
- High-dimensional sparse text data: `LogisticRegression` or `MultinomialNB`.
- Tabular with mixed numeric / categorical: tree ensembles tend to win.

Note what is NOT in my default list: neural networks. They are amazing for images, audio, and text — but for tabular data they are usually overkill, slower to train, harder to debug, and rarely beat a tuned gradient boosting model. Use the right tool.

## Reading sklearn errors

Two errors you will hit repeatedly. Recognise them now and save hours later.

**`ValueError: Found input variables with inconsistent numbers of samples`.**
You passed `X` and `y` with different numbers of rows. Print `X.shape` and `y.shape` and find the mismatch.

**`ValueError: Expected 2D array, got 1D array instead.`**
You passed a Series where sklearn wanted a DataFrame, or a flat array where it wanted 2D. Use `data[["col"]]` not `data["col"]`. Or `.reshape(-1, 1)` for NumPy arrays.

**`ConvergenceWarning: lbfgs failed to converge`.**
Your model didn't finish optimising. Add `max_iter=1000` or scale your features.

## A complete first-model template

Burn this into muscle memory. Almost every supervised ML script starts here:

```python
from __future__ import annotations
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def main() -> None:
    df = pd.read_csv("data.csv")
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))


if __name__ == "__main__":
    main()
```

Twenty lines for a complete, evaluable, reproducible classifier. The library is doing the heavy lifting — your job is to think carefully about the problem.

## What about regression metrics?

For regression, swap the imports:

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ... fit ...
preds = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, preds))
print("MSE:", mean_squared_error(y_test, preds))
print("RMSE:", mean_squared_error(y_test, preds) ** 0.5)
print("R^2:", r2_score(y_test, preds))
```

- **MAE** is in the same units as the target. Easy to explain to non-technical stakeholders. ("Our predictions are off by $12k on average.")
- **MSE / RMSE** penalises large errors more heavily. Useful when big misses are particularly bad.
- **R²** is unitless. Roughly: fraction of variance the model explains. Useful for comparing models on the same dataset.

Pick the metric that matches what the business actually cares about. Do not just print three numbers and look at the biggest.

## Recap

You can now, in fewer than 20 lines:

- Load a dataset.
- Split it into train and test.
- Fit a model.
- Evaluate it with the right metric.
- Compare a few algorithms.

That is more than 90% of "doing ML" at the entry level. Lecture 3 turns it into something production-shaped: preprocessing in pipelines, cross-validation, confusion matrices, and a deep dive on the ethics you cannot duck.

## A note on `random_state`

You will see `random_state=42` everywhere in this curriculum. It is not magic. It is a seed for the random number generator that controls things like which rows go into the train split, the initial weights in some models, and which examples a tree considers at each node.

The numbers do not matter; consistency does. Three rules of thumb:

- Use a `random_state` whenever you split, sample, or initialise. Otherwise your numbers will jitter between runs and you will not be able to tell whether a code change actually improved the model.
- Pick one number for the file and stick with it. `42` is conventional. `0` works too. The number is arbitrary.
- When comparing two models, use the *same* `random_state` for both. Otherwise you are partly comparing the models and partly comparing the splits.

In production you typically *do not* fix the seed — you want each retrained model to see fresh random state — but in tutorials, debugging, and CI you almost always do.

## Saving and loading models

Once you have a trained model, you do not want to retrain it every time you call your program. `joblib` (a library that ships with the scientific Python stack) handles the persistence:

```python
import joblib

joblib.dump(model, "iris_model.joblib")          # save
loaded = joblib.load("iris_model.joblib")        # later: load
preds = loaded.predict(X_new)
```

Why `joblib` instead of plain `pickle`? `joblib` is optimised for the large NumPy arrays that scikit-learn models contain, and the file format is the de-facto standard in the sklearn world. Files end in `.joblib` by convention.

Two things to remember:

1. **Versioning.** A model saved with scikit-learn 1.4 may not load cleanly under 1.7. If you persist a model, persist a `requirements.txt` or `pyproject.toml` with it.
2. **Pipelines.** If your model has preprocessing steps (scaling, encoding, etc.), save the whole `Pipeline` — not just the final classifier. Otherwise you have to manually replay the preprocessing every time you load, and you will eventually get it wrong.

This is exactly what the mini-project asks you to do.

## Practice prompts

Try these in a REPL before moving on:

1. Re-run the iris classifier with `random_state=0` and `random_state=1`. Are the scores identical? Why or why not?
2. Drop `petal length (cm)` from `X`. Does accuracy fall? By how much?
3. Replace `LogisticRegression` with `KNeighborsClassifier(n_neighbors=1)`. Score on train set. Score on test set. Notice anything?
4. For the house-price example, predict the price of a 2200 sqft house. Does the answer feel right?
5. Save the iris logistic regression to `iris.joblib`. Open a new Python shell. Load it. Predict on a row of `X_test`. Confirm you get the same answer.

You will rerun versions of this code dozens of times this week. Keep a scratch script open.
