# Lecture 3 — Pipelines, evaluation, and ethics

## Read time

About 50 minutes. The ethics section is half the value of the lecture; do not skim it.

In Lecture 2 you trained models. In this lecture you make them robust, evaluate them honestly, and confront the responsibility that comes with shipping decisions that affect people.

## Why pipelines

Here is the problem. Real datasets need preprocessing:

- Numeric features have different scales. Age is 0–100; income is 0–1,000,000. Many models care.
- Categorical features need to be encoded into numbers.
- Missing values must be handled.
- Sometimes you do feature selection or dimensionality reduction.

The naïve approach:

```python
# Don't do this.
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_encoded = encoder.fit_transform(X_train_scaled)
X_test_encoded = encoder.transform(X_test_scaled)
model.fit(X_train_encoded, y_train)
preds = model.predict(X_test_encoded)
```

Four problems:

1. **Verbose.** You have to remember to apply every step in the same order to test data, deployment data, and any new input you ever feed the model.
2. **Easy to leak.** A common mistake is to call `scaler.fit(X)` on the whole dataset before splitting. That leaks information from the test set into the training set, and your reported accuracy is inflated.
3. **Hard to deploy.** When you save the model with `joblib`, you also need to save the scaler, the encoder, and remember their order. Three artefacts to keep in sync.
4. **Hard to cross-validate.** If you scale before cross-validation, every fold leaks.

**`Pipeline`** fixes all of this. It is one of the most important sklearn idioms.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


pipe = Pipeline(
    steps=[
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ]
)

pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)
```

The pipeline is a single estimator. It has `.fit`, `.predict`, `.score`. The preprocessing happens automatically and correctly — `StandardScaler` is fit only on the training fold, then applied to whatever you predict on.

`joblib.dump(pipe, "model.joblib")` saves everything in one file: scaler, model, and the order. You can ship that one file and call `.predict` on raw data.

## ColumnTransformer: different preprocessing per column

Real datasets have a mix of numeric and categorical columns. You want to scale the numeric ones and one-hot encode the categorical ones. `ColumnTransformer` lets you wire that up:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


numeric_cols = ["age", "fare"]
categorical_cols = ["sex", "embarked", "pclass"]

preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ]
)

pipe = Pipeline(
    steps=[
        ("prep", preprocess),
        ("clf", LogisticRegression(max_iter=1000)),
    ]
)
pipe.fit(X_train, y_train)
```

A few notes:

- `handle_unknown="ignore"` on `OneHotEncoder` makes the encoder robust to categories seen only at prediction time. Without it, your production deploy will crash the first time a new value shows up.
- The order of columns in `numeric_cols` and `categorical_cols` does not have to match the DataFrame.
- Pandas DataFrames are first-class citizens here. You can refer to columns by name, not just index.

The pipeline can now be cross-validated, pickled, deployed — as a single object.

## StandardScaler: what it actually does

`StandardScaler` subtracts the mean and divides by the standard deviation, column by column. Each output column has mean 0 and standard deviation 1. This is called **standardisation**. It matters for:

- Models that compute distances (k-NN, k-means, SVMs).
- Linear models with regularisation (which is most modern linear models).
- Anything involving gradient descent on raw features.

It does NOT matter for tree-based models (decision trees, random forests, gradient boosting). Trees split on thresholds; the scale doesn't affect which threshold wins. You can include the scaler in a pipeline for a tree and the model will still work — it just doesn't help.

## OneHotEncoder: encoding categories

`OneHotEncoder` turns one categorical column into several binary columns, one per category. If `sex` has values `male`/`female`, the encoder produces `sex_male` and `sex_female`, each 0 or 1.

Why not just map `male → 0, female → 1` with a single column? Because for non-binary categories (say, `embarked` with values `S`/`C`/`Q`), assigning 0/1/2 implies that `Q > S` in a way that has numeric meaning. The model will believe you. One-hot encoding avoids that.

A related family: **ordinal encoding** (use `OrdinalEncoder`) is appropriate when the categories have a real order, e.g. `low/medium/high`. Use the right tool for the semantics.

## Cross-validation: don't trust one split

`train_test_split` gives you one train/test partition. That partition might be lucky, or unlucky. You don't know.

**Cross-validation** splits the data into K folds, trains K times (each time holding out a different fold as validation), and reports the mean score across folds. The most common variant is **5-fold cross-validation**.

```python
from sklearn.model_selection import cross_val_score


scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
print("scores:", scores)
print("mean:", scores.mean(), "std:", scores.std())
```

That gives you five numbers and tells you not just "how good is this model" but also "how stable is the answer". A model with mean 0.85 ± 0.01 is very different from one with mean 0.85 ± 0.15 — even though they look identical from a single split.

Use cross-validation **on the training set** during model selection. Keep the held-out test set untouched until you have committed to a final model. That last test-set score is your honest estimate of generalisation performance.

## Classification metrics, properly

`accuracy = correct / total`. Easy and intuitive. Useless when classes are imbalanced.

Example: you build a fraud detector. 1% of transactions are fraud. A model that predicts "not fraud" for every transaction gets 99% accuracy. It is also catastrophically useless. Accuracy alone is a trap.

You need:

- **Precision** = `TP / (TP + FP)`. Of the things the model said are positive, how many are? "When the model cries fraud, how often is it right?"
- **Recall** = `TP / (TP + FN)`. Of the actual positives, how many did we catch? "Of all real fraud, how much did we flag?"
- **F1** = harmonic mean of precision and recall. A single number that balances both.

Where `TP` = true positives, `FP` = false positives, `FN` = false negatives.

When to optimise for which:

- **Precision matters more** when false positives are costly. Don't accuse innocents of fraud. Don't tell healthy people they have cancer.
- **Recall matters more** when false negatives are costly. Don't miss real fraud. Don't miss tumours.
- **F1** when you want a balance and don't have strong priors. Default choice for reporting.

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, preds, target_names=["ham", "spam"]))
```

That one call gives you precision, recall, F1, and support (sample count) per class, plus a macro and weighted average. **Get into the habit of printing this instead of plain accuracy.**

## The confusion matrix

A confusion matrix is a `K x K` table for `K` classes. Rows are actual classes, columns are predicted classes. The cell `(i, j)` counts how many examples of true class `i` were predicted as class `j`.

```python
from sklearn.metrics import confusion_matrix

print(confusion_matrix(y_test, preds))
# [[TN, FP],
#  [FN, TP]]   for binary classification
```

For binary classification with labels `[0, 1]`:

```text
                Predicted 0    Predicted 1
Actual 0        TN             FP
Actual 1        FN             TP
```

Read the off-diagonals: they tell you *where* the model is wrong, not just *how often*. If FN is much bigger than FP, your model is missing positives. If FP is bigger, it is over-flagging.

For multi-class problems, the matrix shows which classes get confused for which others. On iris, you will often see versicolor and virginica confused for each other (they are similar) while setosa is perfectly classified.

The confusion matrix is the single most useful diagnostic tool in classification. Always look at it.

## Overfitting and underfitting

Two failure modes you will see constantly.

- **Overfitting.** The model memorises the training set instead of learning patterns. Training score: very high. Test score: poor. Diagnosis: the model is too flexible for the amount of data. Fixes: more data, simpler model, regularisation, fewer features, more `max_depth` constraints on trees.
- **Underfitting.** The model is too simple to capture the patterns. Training score: low. Test score: also low. Fixes: more flexible model, more features, less regularisation.

A canonical demo:

```python
from sklearn.tree import DecisionTreeClassifier

for depth in [1, 2, 3, 5, 10, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42)
    t.fit(X_train, y_train)
    print(f"depth={str(depth):4s}  train={t.score(X_train, y_train):.3f}  test={t.score(X_test, y_test):.3f}")
```

As `max_depth` increases, training accuracy climbs toward 1.0. Test accuracy will climb for a while, then plateau or fall. The sweet spot is where the test score peaks and the gap to train score is small. This pattern — known as the **bias-variance tradeoff** — shows up in every ML problem you will work on.

Two important reflexes:

1. **Always report both train and test scores.** A single number is suspicious.
2. **If train and test scores match and both are bad, you are underfitting.** Make the model bigger.
3. **If train is great and test is bad, you are overfitting.** Make the model smaller, or get more data.

## Ethics, fairness, and accountability — substantively

We could end the lecture there. Lots of ML courses do. They will tell you "be ethical" in a half-paragraph and move on. We are not going to do that, because the half-paragraph approach is exactly how the field arrived at the present mess.

The technical work you just learned — `fit`, `predict`, `score` — is genuinely powerful. Power without accountability becomes harm. Let's get specific.

### Representation in training data

A model learns the distribution of its training data. If a group is underrepresented in the data, the model will be worse at making predictions about that group, full stop.

- Facial recognition systems have historically performed dramatically worse on darker-skinned faces because they were trained on datasets dominated by lighter-skinned subjects. The 2018 "Gender Shades" study by Joy Buolamwini and Timnit Gebru documented error rates over 30% for darker-skinned women on commercial systems, versus under 1% for lighter-skinned men.
- A medical diagnostic model trained mostly on data from one country will be worse at diagnosing patients from another, where disease presentation, baseline rates, and even what "normal" looks like in lab results differ.
- A loan-approval model trained on historical lending data will reproduce — and often amplify — historical discrimination, because the labels themselves reflect biased human decisions.

The technical lesson: **the test set being good is not enough**. You must audit performance per subgroup. Compute precision and recall separately for each sensitive group (race, sex, age band, geography — whatever applies). If the gap is unacceptable, your model is unfit to deploy, no matter what your headline accuracy says.

Homework problem 6 has you do this. Take it seriously.

### Feedback loops

Many deployed ML systems shape the data they are subsequently trained on. This creates feedback loops that can amplify small initial biases into large ones over time.

- **Predictive policing.** A model predicts where crime will occur; police are dispatched there; they find more crime there (because they're there); the new data confirms the model's prediction; next iteration sends more police there. Neighbourhoods that were over-policed historically get more over-policed by the model. Cathy O'Neil's *Weapons of Math Destruction* dissects exactly this in detail.
- **Recommendation systems.** A platform shows you what its model thinks you'll engage with; you engage with what it shows you; the model "learns" your preferences from your engagement. But your engagement was constrained by its showings. The model now has a self-fulfilling theory of who you are.
- **Hiring filters.** A resume screener trained on past hires will favour candidates who look like past hires. Future hires will look more like past hires. The filter is "validated" by its own outputs.

The technical lesson: **monitor your live model the way you would monitor a sick patient**. Track its decisions over time. Track who its decisions affect. If you can, randomly bypass the model for a small fraction of cases to keep a clean counterfactual stream.

### Opacity and explainability

A linear regression with a dozen features is explainable: each weight tells you the contribution of one variable. A 175-billion-parameter language model is, for practical purposes, a black box. Most ML in between is closer to the black-box end.

Why this matters:

- **Legal.** GDPR Article 22 grants subjects the right to meaningful information about automated decisions affecting them. "The model said so" is not meaningful information.
- **Operational.** When a model misbehaves, you need to know why so you can fix it. An opaque model that misbehaves in production is much harder to debug.
- **Trust.** Domain experts (doctors, judges, loan officers) will only use a model they can sanity-check. An opaque "trust me" pipeline gets bypassed or worse, blindly followed.

Tools exist (SHAP, LIME, surrogate models) and they help. But the cleanest answer to "is this model explainable?" is often to choose an explainable model — logistic regression, a shallow tree, GAMs — even when a more complex one would score slightly higher.

### Accountability

When an algorithm denies someone insurance, who is accountable?

- The data scientist who trained the model?
- The product manager who scoped the project?
- The company that deployed it?
- The customer-service rep on the phone who can't explain?
- "The algorithm"?

If your answer is "the algorithm", you are part of the problem. Algorithms are not moral agents. They cannot be held accountable. People can.

A useful principle from the FAccT (Fairness, Accountability, Transparency) research community: **a model is a policy**. If you wouldn't be comfortable with a person reading the policy out loud and applying it ("we deny loans to anyone whose ZIP code historically had high default rates"), you should not deploy the model that encodes it.

Concretely:

- **Document your model.** Datasheets for datasets and model cards (Google's "Model Cards for Model Reporting", 2019) are well-established templates. Use them. Make them public.
- **Have a human-in-the-loop for high-stakes decisions.** Healthcare, employment, criminal justice, education, housing, finance — all of these need humans who can override the model and absorb accountability.
- **Provide recourse.** People affected by a model's decision must be able to dispute and correct it.
- **Sunset bad models.** Sometimes the right answer is to take the system down. That is a valid engineering decision.

### When NOT to deploy a model

Even when a model technically works, sometimes you should not ship it. Red flags:

- The model encodes decisions that should be **value judgments**, not predictions. (Should this person get parole? That is a value question disguised as a prediction question.)
- The training labels reflect **biased historical decisions** that you don't want to perpetuate.
- The error modes affect **vulnerable populations** disproportionately and there is no realistic mitigation.
- There is **no plan for monitoring or recourse**.
- The product team is using the model as a **rhetorical shield** ("the algorithm decided") rather than a tool.

This is not academic hand-wringing. Real systems have caused real harm: the COMPAS recidivism tool, the Robodebt automated benefits-clawback system in Australia, the Dutch childcare-benefits scandal, multiple resume-screening tools that systematically discriminated. Engineers built every one of these. Engineers chose to stay silent.

You will, in your career, be asked to build something you should refuse to build. Have an answer ready.

## Recap

- Pipelines are not optional. They prevent leakage, simplify deployment, make cross-validation honest.
- `ColumnTransformer` handles mixed numeric/categorical data cleanly.
- Cross-validation, not a single split, tells you the truth.
- Accuracy is one number in a constellation; print `classification_report` and `confusion_matrix`.
- Overfitting and underfitting have a diagnostic shape; learn to spot it.
- Ethics is engineering, not PR. Audit by subgroup. Choose explainable models when stakes are high. Insist on human accountability. Refuse to build what should not be built.

Now go do the exercises. They reinforce every concept here.
