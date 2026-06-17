# Week 14 — Quiz

Ten multiple-choice questions. Cover the page below the answer key with your hand and try without peeking. Aim for 8/10 before moving on to Week 15.

---

## Question 1 — Supervised vs unsupervised

A team has 50,000 customer transactions and wants to group customers into similar segments. They have no group labels. Which family of ML applies?

A. Supervised regression
B. Supervised classification
C. Unsupervised clustering
D. Reinforcement learning

---

## Question 2 — Regression vs classification

You want to predict tomorrow's temperature in Celsius from today's weather data. The output is a continuous number. This is:

A. Classification
B. Regression
C. Clustering
D. Dimensionality reduction

---

## Question 3 — train_test_split

Why do we hold out a test set when training a model?

A. To make the training loop faster
B. To estimate how the model will perform on data it has never seen
C. To save memory during training
D. To increase the size of the training set

---

## Question 4 — The estimator API

Which two methods are common to almost every scikit-learn estimator?

A. `train` and `evaluate`
B. `learn` and `infer`
C. `fit` and `predict`
D. `compile` and `forward`

---

## Question 5 — Overfitting

A model gets 99% accuracy on the training set and 62% accuracy on the test set. The most likely diagnosis is:

A. Underfitting — the model is too simple
B. The model is correctly trained but the test set is too small
C. Overfitting — the model has memorised the training data
D. The optimiser failed to converge

---

## Question 6 — Metrics on imbalanced data

You build a fraud detector. Only 1% of transactions are fraud. Your model predicts "not fraud" for every transaction and achieves 99% accuracy. What is the right next step?

A. Ship it — 99% is great
B. Stop using ML; the problem is too hard
C. Switch metrics to precision/recall on the fraud class and re-evaluate
D. Add more "not fraud" examples to balance the dataset

---

## Question 7 — Pipelines

You scale your features with `StandardScaler` and then train `LogisticRegression`. Why is a `Pipeline` preferable to running the scaler and the model separately?

A. Pipelines run faster than separate calls
B. Pipelines prevent leakage during cross-validation by re-fitting preprocessing on each fold's training data only
C. Pipelines automatically tune hyperparameters
D. Pipelines convert pandas DataFrames into NumPy arrays for you

---

## Question 8 — Confusion matrix

In a binary confusion matrix laid out as:

```
                Predicted 0    Predicted 1
Actual 0        a              b
Actual 1        c              d
```

Which cell represents *false negatives* (positives the model missed)?

A. `a`
B. `b`
C. `c`
D. `d`

---

## Question 9 — Bias and ethics

A facial recognition model is reported to perform significantly worse for darker-skinned women than for lighter-skinned men. The single most likely cause is:

A. The algorithm is racist by design
B. Darker faces are inherently harder to classify
C. The training data underrepresented darker-skinned women, so the model's performance for that group is worse
D. The choice of learning rate

---

## Question 10 — When NOT to use ML

For which of the following problems is machine learning **least** appropriate?

A. Filtering spam from email
B. Translating a fixed table of currency codes to country names
C. Predicting customer churn from usage data
D. Detecting tumours in chest X-rays

---

## Answer key

(Read after you've answered all ten.)

1. **C.** No labels + grouping = unsupervised clustering. k-means is the canonical method.
2. **B.** Continuous numerical output is regression by definition.
3. **B.** The test set is your honest estimate of generalisation. Touching it during model selection invalidates it.
4. **C.** `fit` (train) and `predict` (produce outputs) are the sklearn API spine.
5. **C.** Large gap between train and test scores is the classic overfitting signature.
6. **C.** Accuracy is a trap on imbalanced classes. Move to precision/recall on the minority class — that's what you actually care about.
7. **B.** Pipelines correctly re-fit preprocessing on each cross-validation fold, preventing leakage. They also simplify deployment.
8. **C.** `c` is the bottom-left cell: actual class 1 (positive), predicted class 0 (negative) = false negative.
9. **C.** Representation in training data is the dominant driver of subgroup performance gaps in modern ML systems. This was documented at scale in the "Gender Shades" research and is now widely replicated.
10. **B.** Translating a fixed table is a deterministic lookup. Write a dictionary. ML is overkill, slower, and adds error.

## Scoring

- **9–10:** Excellent. Move on to Week 15.
- **7–8:** Good. Re-read the lecture sections you missed.
- **5–6:** OK. Redo the exercises you skipped.
- **Below 5:** Re-read the lectures slowly with a code editor open. Then retake.
