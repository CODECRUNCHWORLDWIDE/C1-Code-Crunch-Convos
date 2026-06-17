# Week 14 — Intro to AI/ML with scikit-learn

Welcome to the week where the buzzwords finally get unpacked. AI, ML, models, training, "the algorithm" — by Friday you will have written, trained, and evaluated your own machine learning models in Python, and you will be able to explain (in plain English) what is actually happening under the hood.

This week sits on top of everything you have learned so far. You already know how to load CSVs with pandas, write functions, manipulate lists and dicts, and reason about data. Machine learning is, mostly, those skills plus a handful of new library calls and a new way of thinking about problems.

## Why this week matters

Machine learning is now embedded in nearly every product you use: spam filters, recommendation systems, fraud detection, image search, autocomplete, navigation, voice assistants, medical screening tools, and the suggestion bar in your IDE. As a programmer in 2026, you do not need to be a research scientist — but you absolutely need to be able to:

- Tell when ML is the right tool for a job (and, just as important, when it is not).
- Read code that uses scikit-learn, PyTorch, or TensorFlow without panicking.
- Build a baseline model end-to-end and judge whether it is actually working.
- Spot common failure modes: leakage, overfitting, biased data, misleading metrics.
- Talk to data scientists and ML engineers as a competent peer.

This week is your on-ramp. Week 15 (Capstone) is where you put it all together with everything from Weeks 1 through 14.

## Learning objectives

By the end of the week you will be able to:

1. Define machine learning and distinguish supervised vs unsupervised, regression vs classification.
2. Walk through the standard ML workflow: data, features, split, train, evaluate, iterate.
3. Use the scikit-learn estimator API (`fit`, `predict`, `transform`) confidently.
4. Split data with `train_test_split` and explain why this matters.
5. Train and compare baseline models: linear regression, logistic regression, decision trees, k-NN, k-means.
6. Preprocess features: scale numeric columns, encode categoricals.
7. Combine preprocessing and modeling into a `Pipeline` with `ColumnTransformer`.
8. Compute and interpret accuracy, precision, recall, F1, MAE, MSE, and a confusion matrix.
9. Diagnose overfitting and underfitting from train vs validation scores.
10. Discuss bias and fairness in ML in a substantive, not performative, way.
11. Save a trained model with `joblib` and load it back for inference.

## Prerequisites

You should be comfortable with Weeks 1–13. Especially:

- **Week 4** — Functions and modules.
- **Week 5** — Lists, dicts, comprehensions.
- **Week 6** — File I/O.
- **Week 11** — Testing mindset (we will compare predictions to ground truth, a lot).
- **Week 13** — pandas, NumPy, basic plotting. This is non-negotiable for this week.

If `pd.read_csv`, `df.dropna()`, and `df.groupby("col").mean()` do not feel routine yet, take an hour to revisit Week 13 before starting the lectures.

## Topics covered

- What ML is and is not (pattern recognition vs intelligence)
- Supervised vs unsupervised learning
- Regression vs classification
- The full ML workflow
- `train_test_split` and why we hold data out
- Linear regression, logistic regression, decision trees, k-NN
- k-means clustering (unsupervised)
- Feature engineering basics
- Encoding categoricals (`OneHotEncoder`)
- Scaling numeric features (`StandardScaler`)
- scikit-learn API conventions: `fit`, `predict`, `transform`, `fit_transform`
- Evaluation: accuracy, precision, recall, F1, MAE, MSE, confusion matrix
- Cross-validation (`cross_val_score`)
- Overfitting vs underfitting
- `Pipeline` and `ColumnTransformer`
- Saving/loading models with `joblib`
- Bias, fairness, and the ethics of deploying models
- When NOT to use ML

## Schedule (~36 hours)

| Day | Focus | Approx. hours |
|-----|------------------------------------------------|---------------|
| Mon | Lecture 1: What is ML + first reading | 6 |
| Tue | Lecture 2: First model with sklearn + Ex 1–2 | 7 |
| Wed | Exercises 3–5 + start Challenge 1 | 6 |
| Thu | Lecture 3: Pipelines, evaluation, ethics | 6 |
| Fri | Mini-project: spam classifier | 7 |
| Weekend | Homework + Challenge 2 + quiz | 4 |

Total: about 36 hours. Adjust to your own pace; the lectures are dense.

## Folder navigation

```text
week-14-intro-ai-ml/
├── README.md                       <- you are here
├── resources.md                    <- curated reading + viewing list
├── quiz.md                         <- 10 MCQs, do at the end of the week
├── homework.md                     <- 6 problems, due before Week 15
├── lecture-notes/
│   ├── 01-what-is-ml.md
│   ├── 02-first-model-with-sklearn.md
│   └── 03-pipelines-evaluation-and-ethics.md
├── exercises/
│   ├── README.md
│   ├── exercise-01-linear-regression.py
│   ├── exercise-02-iris-classifier.py
│   ├── exercise-03-train-test-split.py
│   ├── exercise-04-pipeline.py
│   └── exercise-05-confusion-matrix.py
├── challenges/
│   ├── README.md
│   ├── challenge-01-titanic-survival.md
│   └── challenge-02-kmeans-clustering.md
└── mini-project/
    ├── README.md
    ├── starter.py
    └── sample-data.csv
```

## Environment setup

You will need:

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
```

Versions known to work with the code in this module: `scikit-learn>=1.4`, `pandas>=2.0`, `numpy>=1.24`, `joblib>=1.3`. Newer versions are fine.

Quick sanity check:

```python
import sklearn
import pandas as pd
print(sklearn.__version__, pd.__version__)
```

If that prints two version numbers without error, you are ready.

## Stretch goals

If you blast through the core material and want more, try these in order of increasing depth:

1. **Ensemble methods.** Replace the decision tree in Exercise 5 with `RandomForestClassifier` and `GradientBoostingClassifier`. Do they win? By how much? Why?
2. **Hyperparameter tuning.** Use `GridSearchCV` to tune the `C` parameter on logistic regression in the iris exercise. Plot training vs validation accuracy across the grid.
3. **Feature importance.** From a trained tree, print `model.feature_importances_` and sort. Which features actually drove decisions?
4. **Pipelines with text.** Add a `TfidfVectorizer` step to your spam classifier pipeline and save the whole thing with `joblib` — vectorizer included.
5. **Intro to deep learning.** Read about neural networks (3Blue1Brown playlist in `resources.md`), then try `MLPClassifier` from sklearn on iris. Same API. Compare to logistic regression.
6. **A fairness audit.** Pick any classifier you have built and split your test-set predictions by a sensitive attribute (e.g., sex on Titanic). Compare precision and recall per group. Write up what you find. This is what homework problem 6 is about — push it further.

## Up next

**Week 15 — Capstone.** You will design and ship one end-to-end project that uses skills from across the whole bootcamp: data ingestion, processing, persistence, an API or CLI, tests, docs — and, optionally, an ML model trained right here in Week 14. Bring receipts.

Let's get to it.
