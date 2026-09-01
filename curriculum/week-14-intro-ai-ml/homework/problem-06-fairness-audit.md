# Problem 6 — Fairness Audit: One Model, Three Scorecards

> **Topic:** Auditing a classifier group by group, and what an audit can and cannot tell you
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** this is the most important problem in the week, and it is the one to take slowest. Every other problem asks how well a model scores. This one asks *for whom*, finds out the answer is very different for two groups of the same test set, and then asks what you are supposed to do about it.

## The Brief

A pizza shop puts a sign in the window: **we get 9 out of 10 orders right**. It
is true. Now split the same orders in two. Walk-in orders: 99 right out of 100.
Delivery orders: 6 right out of 10. Nobody reading the sign would ever find that
out, and everyone being let down is in the same group. That is what an average
does — it is the exact operation that makes a difference between groups
disappear.

Your job here is to take the sign down and print the split.

The model is the Titanic survival classifier from
[Challenge 1](../challenges/challenge-01-titanic-survival.md): the same 500
generated passengers, the same preprocessing pipeline, the same split, the same
seed. This time the model is not the deliverable. **The audit is.** You will
score that one model three times — on all the test passengers, on the men only,
on the women only — and print precision, recall and accuracy for each.

Four things are worth understanding before you write a line of it.

**The labels are decisions, not facts.** The column the model predicts is
`survived`: who actually got off the ship. On the night of 14 April 1912 the
crew loaded women and children into the lifeboats first. So `survived` is not a
record of a law of nature. It is a record of a choice that people made. The model
cannot tell the two apart — it finds the pattern in the labels and repeats it.
This generalises, and it is the most important sentence on this page: **a model
trained on records of past decisions learns those decisions, including whatever
was unfair about them.** A résumé filter trained on who was hired before learns
who used to get hired. A lending model trained on approvals learns who used to be
approved. The arithmetic has no way to ask whether the old decision was a good
one, so it never does.

**One number hides the gap.** The model you are about to train gets 0.710
accuracy on the test set. Per group, accuracy is 0.68 for men and 0.79 for
women — close enough that most people would shrug and ship it. But recall — of
the passengers who really survived, how many did the model flag? — is **1.00 for
women and 0.09 for men**. Same model, same predictions, same afternoon. It
catches every surviving woman and almost no surviving man. No single overall
number showed that, and neither did per-group accuracy; it took *one rate,
computed separately for each group, and then compared*. That is why an audit is a
table and not a score. **You compare the same rate across groups instead of
averaging one rate over everybody.**

**A metric is a proxy that a person chose.** Precision, recall and accuracy are
not fairness. Each one is a number somebody picked to stand in for something they
cared about. Recall asks "of the people who really survived, how many did we
find?" — that is the one that matters if this list decides who gets a lifeboat
seat, because a miss means a person is left behind. Precision asks "when we say
survived, how often are we right?" — that is the one that matters when a wrong
yes costs the person something. Watch what the choice does here: judge this model
by accuracy and it looks roughly even-handed between men and women; judge it by
recall and it looks catastrophic for men. Same model, opposite verdicts.
**Choosing which error counts is a value judgement, not a technical one.** There
is no neutral metric waiting underneath to settle it. Decide before you look at
the results, write down who decided, and say what the number is standing in for.

**And passing an audit is evidence, not a certificate.** An audit checks the
groups you thought to name, in the data you happen to hold, with the metric you
happened to pick, on one day. It cannot tell you the labels were fair to begin
with. It cannot see a group that nobody wrote down. It says nothing about what
the model does next month, or about what people do with its output. A clean
table means *we looked here, this way, and found no gap we could measure*. It
never means the model is fair, and it must never be handed on as if it did.
Whether a system treats people fairly is decided by what it does to them, and
that goes on being decided long after your table is printed.

## Starter

Copy this into `problem-06-fairness-audit.py`. The passenger generator and the
column lists are given — they are Challenge 1's, unchanged, so your numbers line
up with that page. You build the pipeline and write the audit.

```python
"""problem-06-fairness-audit.py — one model, three scorecards: everyone, men, women."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
NUMERIC_COLS = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_COLS = ["sex", "embarked", "pclass"]


def make_titanic(seed: int = RANDOM_STATE, n: int = 500) -> pd.DataFrame:
    """Titanic-shaped passengers with the historical survival pattern."""
    rng = np.random.default_rng(seed)
    sex = rng.choice(["male", "female"], size=n, p=[0.64, 0.36])
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
    true_age = rng.normal(29.0, 14.0, n).clip(0.5, 80.0)
    sibsp = rng.integers(0, 4, n)
    parch = rng.integers(0, 3, n)
    base_fare = np.select([pclass == 1, pclass == 2, pclass == 3], [84.0, 21.0, 14.0])
    fare = (base_fare * rng.uniform(0.5, 1.8, n)).round(2)
    embarked = rng.choice(["S", "C", "Q"], size=n, p=[0.72, 0.19, 0.09])
    female = (sex == "female").astype(float)
    first = (pclass == 1).astype(float)
    third = (pclass == 3).astype(float)
    child = (true_age < 12).astype(float)
    logit = (-1.0 + 2.2 * female + 0.9 * first - 0.6 * third
             + 1.0 * child - 0.01 * (true_age - 29.0))
    survived = (rng.random(n) < 1.0 / (1.0 + np.exp(-logit))).astype(int)
    frame = pd.DataFrame({
        "survived": survived, "pclass": pclass, "sex": sex, "age": true_age,
        "sibsp": sibsp, "parch": parch, "fare": fare, "embarked": embarked,
    })
    frame.loc[rng.random(n) < 0.20, "age"] = np.nan
    frame.loc[rng.random(n) < 0.02, "embarked"] = np.nan
    return frame


def main() -> None:
    df = make_titanic()
    x = df.drop(columns=["survived"])
    y = df["survived"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    # TODO: build ONE pipeline: median-impute + scale the numeric columns,
    #       most-frequent-impute + one-hot the categorical ones, then
    #       LogisticRegression(max_iter=1000, random_state=RANDOM_STATE).
    # TODO: fit it on the training rows and predict on x_test.
    # TODO: print the overall test accuracy.
    # TODO: build boolean masks from x_test["sex"] for men and for women.
    # TODO: print one table row per group -- all, male, female -- with n,
    #       precision, recall and accuracy, using zero_division=0.
    # TODO: print one line naming the recall gap between the two groups.


if __name__ == "__main__":
    main()
```

## Requirements

1. Generate the passengers with `make_titanic(seed=42, n=500)` — the same
   generator as Challenge 1, so your table matches the one there.
2. Split with `test_size=0.20`, `random_state=42`, `stratify=y`.
3. Train **one** classifier: the leak-free pipeline from Lecture 3 — median
   impute plus `StandardScaler` on `age`, `sibsp`, `parch`, `fare`;
   most-frequent impute plus `OneHotEncoder(handle_unknown="ignore")` on `sex`,
   `embarked`, `pclass` — feeding
   `LogisticRegression(max_iter=1000, random_state=42)`.
4. Print the overall accuracy on the test set.
5. Print the audit table, positive class = survived, with a row for `all`, `male`
   and `female` and columns `n`, `precision`, `recall`, `accuracy`:

   ```text
   | group  |   n | precision | recall | accuracy |
   |--------|-----|-----------|--------|----------|
   | all    |     |           |        |          |
   | male   |     |           |        |          |
   | female |     |           |        |          |
   ```

6. Print one closing line that says the recall gap out loud, in words, with both
   numbers in it.
7. Write **200–300 words** in your `report.md` answering all three:
   - Are the group metrics meaningfully different, and why might that be?
   - Even if this model is "accurate overall", what could go wrong if it were
     used for a real decision — prioritising an evacuation, pricing insurance?
   - What would you want to know about how the data was collected before you
     recommended that anyone use this model?

## Constraints

- **One model, three scorecards. Never one model per group.** Fitting a separate
  classifier for men and another for women gives you three different systems and
  audits none of them. The thing you are measuring is the single model you would
  actually deploy, seen from three angles.
- **Audit on the test set only.** The model has effectively memorised part of the
  training rows, and memorised rows score well for everybody. A gap can hide
  completely in training scores.
- **`stratify=y` on the split.** The test set is only 100 passengers. Without
  stratification an unlucky draw can move a group's survival rate by several
  points, and you would be reading the split, not the model.
- **Pass `zero_division=0` to `precision_score` and `recall_score`.** If the
  model predicts "survived" for nobody in a group, precision is 0 divided by 0.
  scikit-learn warns and quietly returns 0.0; setting the parameter says you
  expected that case and keeps the warning out of the middle of your table.
- **Keep `sex` in the features and use it as the group key.** Deleting the
  sensitive column is the first fix everyone reaches for, and it is not an audit —
  it changes the model instead of measuring it. Measure first, then decide. (In
  real data, deleting the column rarely blinds a model anyway: other columns
  usually carry the same information.)
- **Print `n` next to every rate.** A precision computed over four people is
  noise wearing a decimal point. The counts are how a reader knows which rows
  carry weight — here 71 men and 29 women.

## Expected output

Every seed is pinned, so this run is identical on every machine, and the table
matches the audit at the bottom of Challenge 1 because it is the same model on
the same split.

```text
$ python problem-06-fairness-audit-solution.py
overall test accuracy: 0.710
fairness audit (positive class = survived):
| group  |   n | precision | recall | accuracy |
|--------|-----|-----------|--------|----------|
| all    | 100 |      0.76 |   0.54 |     0.71 |
| male   |  71 |      0.50 |   0.09 |     0.68 |
| female |  29 |      0.79 |   1.00 |     0.79 |
same model, but recall is 1.00 for women and 0.09 for men -- the overall accuracy hid that gap
```

Now read it properly, row by row.

**Overall, the model looks unremarkable.** 0.710 accuracy, precision 0.76,
recall 0.54. A middling classifier on a hard problem — nothing here would stop a
release.

**The men's row is where it falls apart.** Recall 0.09: of the men in the test
set who actually survived, the model flags about one in eleven. Precision 0.50
says that on the rare occasions it does call a man a survivor it is right half
the time — but it almost never calls one. If this list were used to decide
anything, the men who survived would be almost entirely invisible to it.

**The women's row is the same failure from the other side.** Recall 1.00 means it
flags *every* surviving woman — which sounds excellent until you notice precision
is 0.79, so it is also flagging women who did not survive. That combination is
the signature of a model that simply predicts "survived" for nearly every woman.

Put the two rows together and the model has learned essentially one rule:
**female ⇒ survived, male ⇒ died.** That rule scores 0.710 because in this data
78% of the women and 28% of the men survived (Challenge 1 prints those rates), so
following the base rate is rewarded. Accuracy is happy. The people the model is
wrong about are not distributed evenly, and one number could never have told you
so.

## Steps

1. Paste the starter and run it. Nothing prints yet — confirm it runs clean.
2. Build the pipeline (numeric branch, categorical branch, `ColumnTransformer`,
   classifier), fit on the training rows, predict on `x_test`, print the overall
   accuracy. Stop and look at it: this is the number that hides everything.
3. Pull `x_test["sex"]` out as a NumPy array and build two boolean masks from it.
   Keep everything positional — masks and labels as arrays, not Series — so
   pandas cannot quietly realign on index labels.
4. Write one small function that takes a name and a mask, slices the truth and
   the predictions with it, and prints one table row.
5. Call it three times: all (a mask of every `True`), male, female. Print the
   header rows above it so the output is a real markdown table.
6. Print the closing line with both recall numbers in it.
7. Write the 200–300 words. Start from the recall row, not the accuracy row.

## The Solution

```python
"""problem-06-fairness-audit.py — one model, three scorecards: everyone, men, women.

Trains a single survival classifier on the offline Titanic-shaped data from
Challenge 1, then scores it three times: on all test passengers, on men only, and
on women only. A model can be "accurate overall" and still behave completely
differently for two groups, and the only way to see that is to measure each group
on its own. Every seed is pinned.

Run it with::

    python problem-06-fairness-audit-solution.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
NUMERIC_COLS = ["age", "sibsp", "parch", "fare"]
CATEGORICAL_COLS = ["sex", "embarked", "pclass"]


def make_titanic(seed: int = RANDOM_STATE, n: int = 500) -> pd.DataFrame:
    """Titanic-shaped passengers with the historical survival pattern."""
    rng = np.random.default_rng(seed)
    sex = rng.choice(["male", "female"], size=n, p=[0.64, 0.36])
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
    true_age = rng.normal(29.0, 14.0, n).clip(0.5, 80.0)
    sibsp = rng.integers(0, 4, n)
    parch = rng.integers(0, 3, n)
    base_fare = np.select([pclass == 1, pclass == 2, pclass == 3], [84.0, 21.0, 14.0])
    fare = (base_fare * rng.uniform(0.5, 1.8, n)).round(2)
    embarked = rng.choice(["S", "C", "Q"], size=n, p=[0.72, 0.19, 0.09])

    female = (sex == "female").astype(float)
    first = (pclass == 1).astype(float)
    third = (pclass == 3).astype(float)
    child = (true_age < 12).astype(float)
    logit = (-1.0 + 2.2 * female + 0.9 * first - 0.6 * third
             + 1.0 * child - 0.01 * (true_age - 29.0))
    survived = (rng.random(n) < 1.0 / (1.0 + np.exp(-logit))).astype(int)

    frame = pd.DataFrame(
        {
            "survived": survived, "pclass": pclass, "sex": sex, "age": true_age,
            "sibsp": sibsp, "parch": parch, "fare": fare, "embarked": embarked,
        }
    )
    frame.loc[rng.random(n) < 0.20, "age"] = np.nan
    frame.loc[rng.random(n) < 0.02, "embarked"] = np.nan
    return frame


def build_pipeline() -> Pipeline:
    """A leak-free preprocessing + logistic-regression pipeline."""
    numeric = Pipeline(
        steps=[("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    categorical = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocess = ColumnTransformer(
        transformers=[("num", numeric, NUMERIC_COLS), ("cat", categorical, CATEGORICAL_COLS)]
    )
    return Pipeline(
        steps=[
            ("prep", preprocess),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )


def score_group(name: str, mask: np.ndarray, y_true: pd.Series, y_pred: np.ndarray) -> None:
    """Print one row of the fairness table for the passengers in *mask*."""
    truth = y_true.to_numpy()[mask]
    guess = y_pred[mask]
    precision = precision_score(truth, guess, zero_division=0)
    recall = recall_score(truth, guess, zero_division=0)
    accuracy = accuracy_score(truth, guess)
    print(f"| {name:<6} | {mask.sum():>3} | {precision:>9.2f} | {recall:>6.2f} | {accuracy:>8.2f} |")


def main() -> None:
    """Train one classifier and score it for everyone, men, and women."""
    df = make_titanic()
    x = df.drop(columns=["survived"])
    y = df["survived"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(x_train, y_train)
    predictions = pipe.predict(x_test)
    print(f"overall test accuracy: {accuracy_score(y_test, predictions):.3f}")

    sex = x_test["sex"].to_numpy()
    print("fairness audit (positive class = survived):")
    print("| group  |   n | precision | recall | accuracy |")
    print("|--------|-----|-----------|--------|----------|")
    score_group("all", np.ones(len(sex), dtype=bool), y_test, predictions)
    score_group("male", sex == "male", y_test, predictions)
    score_group("female", sex == "female", y_test, predictions)

    male_recall = recall_score(y_test.to_numpy()[sex == "male"], predictions[sex == "male"], zero_division=0)
    female_recall = recall_score(y_test.to_numpy()[sex == "female"], predictions[sex == "female"], zero_division=0)
    print(
        f"same model, but recall is {female_recall:.2f} for women and {male_recall:.2f} "
        f"for men -- the overall accuracy hid that gap"
    )


if __name__ == "__main__":
    main()
```

**One model, sliced three ways.** Look at what `main` does after `fit`: it calls
`predict` exactly once, and then every row of the table is a different *view* of
that same prediction array. `score_group` takes a boolean mask, uses it to pick
out the passengers in that group, and computes the three metrics on just those
rows. The model never learns that groups exist. The audit is entirely something
that happens afterwards, with masks — which is precisely why it can be run on a
model somebody else trained.

**Why `.to_numpy()` before the mask.** `y_test` is a pandas Series and it kept
the original row labels from the 500-row frame, so its index is a scattered set
of numbers, not 0–99. The mask is positional — it came from `x_test["sex"]` in
row order. Mixing the two is the classic way to silently score the wrong
passengers. Converting both sides to plain arrays makes the slicing positional on
both, so row 7 of the mask lines up with row 7 of the labels.

**What the three metrics are actually counting.** For one group: precision is
`TP / (TP + FP)`, the share of that group's "survived" predictions that were
right. Recall is `TP / (TP + FN)`, the share of that group's real survivors the
model found. Accuracy is every correct call over everybody in the group. Precision
and recall answer different questions and can move in opposite directions — the
women's row, precision 0.79 with recall 1.00, is exactly that: catch everyone, at
the cost of also flagging people you should not have.

**What this program does not do, on purpose.** It does not fix anything, and it
does not print a verdict. It prints rates per group and one honest sentence about
the gap. Deciding whether a 0.09-versus-1.00 recall gap is acceptable needs
somebody who knows what the model is for, who would be affected by a miss, and
what happens to a person the model gets wrong — and that decision is not a
`sklearn` call. The audit's job is to make the gap impossible to miss. What to do
next is a human's job, and it stays a human's job.

## Download and run

Download
[problem-06-fairness-audit-solution.py](./problem-06-fairness-audit-solution.py)
and run it:

```bash
python problem-06-fairness-audit-solution.py
```

If scikit-learn and pandas are not installed yet:

```bash
python -m pip install scikit-learn pandas
```

The passengers are generated from a fixed seed inside the file, so there is
nothing to download and the table is identical everywhere. The `-solution` suffix
keeps it clear of your own `problem-06-fairness-audit.py`.

## Common bugs to catch

- **`IndexError: boolean index did not match indexed array along axis 0; size of
  axis is 500 but size of corresponding boolean axis is 100`.** You built the
  mask from the 100-row test set and applied it to the full 500-row column. Mask
  the test set with a test-set mask.
- **UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to
  no predicted samples. Use `zero_division` parameter to control this behavior.**
  A group got no positive predictions at all. Pass `zero_division=0` — and notice
  what the warning is telling you: for that group, the model says no to everyone.
- **The male and female rows have the same numbers as the `all` row.** Your masks
  are not doing anything. Print `mask.sum()` for each; they should be 71 and 29
  and add up to 100.
- **The rows do not add up to 100.** You masked a Series with an index-aligned
  filter instead of a positional one, so pandas matched on labels. Call
  `.to_numpy()` on the labels and the predictions first.
- **"Recall 1.00 must be a bug."** It is not. It means the model predicted
  "survived" for every woman who really survived — and, given precision 0.79, for
  several who did not. A perfect recall with imperfect precision is a model
  saying yes very freely, not a model that is perfect.
- **You trained a model per group.** Then you have audited three systems, and the
  one you would ship is none of them. Fit once.
- **You looked at per-group accuracy, saw 0.68 and 0.79, and stopped.** That is
  the whole trap this problem is built around. The gap lives in recall.
- **You dropped `sex` from the features and called the audit passed.** You changed
  the model rather than measuring it — and `sex` has to stay in `x_test` regardless,
  because it is what you group by.

## Under the hood

<details>
<summary>Under the hood — the 2×2 table hiding behind every row</summary>

Every rate in that audit comes from four counts, computed over one group's
passengers only:

```text
                    predicted died   predicted survived
actually died            TN                  FP
actually survived        FN                  TP
```

- precision = `TP / (TP + FP)` — of the ones we said survived, how many did.
- recall = `TP / (TP + FN)` — of the ones who did survive, how many we said so.
- accuracy = `(TP + TN) / everybody`.

Run `confusion_matrix(y_test.to_numpy()[mask], predictions[mask])` for the men and
you can watch the recall come apart: a large `FN` cell and a tiny `TP` cell is
what 0.09 looks like in whole people. This is why Lecture 3 calls the confusion
matrix the single most useful diagnostic in classification — a rate tells you how
often, the matrix tells you which way.

Notice that accuracy has `TN` in its numerator and the other two do not. In a
group where most people died, a model that says "died" to everyone banks a huge
pile of true negatives and posts a respectable accuracy while its recall sits near
zero. That is the whole mechanism of the men's row, in one line of arithmetic.

</details>

<details>
<summary>Under the hood — the fairness definitions, and why you cannot have them all</summary>

Researchers have written down many precise definitions of what it would mean for
a classifier to treat groups equally. Three you will meet constantly:

- **Demographic parity** — each group is predicted positive at the same *rate*.
- **Equal opportunity** — each group gets the same *recall*. (Of the people who
  truly qualify, the same share is found in every group.)
- **Predictive parity** — each group gets the same *precision*. (A "yes" means
  the same thing whoever receives it.)

Each is reasonable. Each is what somebody sincerely means by "fair". And there is
a well-known impossibility result — Kleinberg, Mullainathan and Raghavan (2016)
and Chouldechova (2017) — showing that when two groups have genuinely different
base rates, no classifier can satisfy all of them at once except in degenerate
cases. Not "no one has managed it yet": it cannot be done, as a matter of
arithmetic.

This is not a reason to give up on the question. It is the reason the choice has
to be made explicitly, by named people, before the results are in — because there
is no configuration of the model that quietly satisfies everyone, and a team that
never chooses has still chosen, by default, whatever their metric happened to be.
This is also exactly why the fairness table on this page reports precision *and*
recall *and* accuracy per group rather than a single "fairness score". A single
score would be one of these definitions in disguise, with the choice hidden.

</details>

<details>
<summary>Under the hood — what you can actually do when the gap is real</summary>

The audit found a gap. Ordered roughly from best to worst:

1. **Fix the data.** If a group is thin in the training set, collect more of it.
   Most gaps are representation problems first and modelling problems second
   (Lecture 3's Gender Shades example is the canonical case).
2. **Question the label.** If the target column encodes a past decision you would
   not defend out loud, no modelling technique repairs it. Sometimes the honest
   conclusion is that the prediction problem was the wrong problem.
3. **Change what you optimise.** Class weights, resampling, or scoring the model
   on the metric you actually care about (`scoring="recall"` in cross-validation)
   shift where the errors fall.
4. **Move the decision threshold.** `predict_proba` gives a probability;
   `predict` just cuts it at 0.5. Lowering the cut raises recall and lowers
   precision. Using a *different* cut per group directly equalises recall — and
   is a policy that treats people differently by group on purpose, which in many
   places is unlawful and in all places needs to be argued in public, not slipped
   into a notebook.
5. **Do not deploy.** Lecture 3 lists the red flags, and "the error modes hit a
   vulnerable group and there is no realistic mitigation" is on that list. Taking
   the system down is a legitimate engineering decision.

Whichever you pick, write it in a model card: what the model predicts, which
groups it was measured on, where it fails, who is accountable, and when it should
be switched off. The audit is the measurement. The card is what makes the
measurement someone's responsibility.

</details>

## Acceptance checklist

- [ ] One model is trained, once, on the training split, and every row of the
      table comes from that one model's predictions.
- [ ] The overall test accuracy prints (0.710).
- [ ] The table has rows for `all`, `male` and `female` with `n`, precision,
      recall and accuracy, positive class = survived.
- [ ] `n` prints for each group and the two groups add up to the 100 test
      passengers.
- [ ] `random_state=42` is on the generator, the split and the classifier, and
      two runs print identical numbers.
- [ ] A closing line names both recall numbers.
- [ ] Your `report.md` has 200–300 words answering all three questions, and it
      talks about recall, not only accuracy.
- [ ] You can say in one sentence what your audit does **not** prove.

## Stretch

- **Audit a different grouping.** Rerun the table split by `pclass` (1, 2, 3)
  instead of sex. Class was the other strong signal in 1912. Does the model treat
  third-class passengers the way it treats men?
- **Cross the two.** Audit women in third class. Watch `n` collapse to a handful —
  and notice that this is where real audits run out of data first, which is
  exactly where harm is easiest to miss.
- **Try the fix everyone suggests.** Drop `sex` from the feature lists (keep the
  column in `x_test`, you still need it to group by) and rerun the audit. Does the
  gap close? What happens to overall accuracy? Then answer the real question: is
  "the model cannot see it" ever the same thing as "the model is not doing it"?
- **Move the threshold.** Use `predict_proba` and cut at 0.3 instead of 0.5. Watch
  recall rise and precision fall for both groups, and decide which trade you would
  defend for an evacuation list.
- **Write the model card.** Ten lines: what it predicts, what it was trained on,
  the per-group table, the known failure mode, who is accountable for a wrong
  call, and the conditions under which it should be retired. Lecture 3 explains
  why this is the deliverable that outlives the code.
