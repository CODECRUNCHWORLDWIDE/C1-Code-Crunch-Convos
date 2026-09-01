# Mini-Project — SMS Spam Classifier

> **Topic:** the whole week in one tool — TF-IDF, three classifiers inside a pipeline, honest metrics, a group-by-group audit, `joblib`, and a CLI
> **Lecture:** [02 — Your First Model With scikit-learn](../lecture-notes/02-first-model-with-sklearn.md) · [03 — Pipelines, Evaluation and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 2–3 hours
> **Why this one:** it is the first thing you will build that makes a decision about a person and then hides it. Everything the week drilled — a pipeline so nothing leaks, four numbers instead of one, a confusion matrix, a subgroup audit — is here because of what happens when a filter quietly eats somebody's appointment reminder.

## The Brief

Build a spam filter, end to end. It reads a pile of text messages that somebody
has already labelled `spam` or `ham` — "ham" is the old email word for a message
you actually wanted — learns what the two kinds look like, and then judges
messages it has never seen.

Think of the filter as a bouncer on a door who cannot hear a word anybody says.
All the bouncer gets is the sign each guest is holding. After a few hundred
guests the bouncer notices that signs saying **free**, **win** and **claim**
usually belong to trouble, and signs saying **dinner** and **sorry** usually do
not. That is the whole trick. There is no understanding in it. There is counting.

And here is the part that makes this a real project rather than a toy. The
bouncer keeps turning away the courier. A delivery firm writes "URGENT",
"track it here", "before Friday" — the exact words a scam writes. A clinic
writes "confirm your appointment at this link". A shop writes "free delivery".
Every one of those is a message somebody wanted, wearing a scam's clothes, and a
filter that is right 93 times out of 100 can still be wrong about the clinic
one time in five.

You will deliver four things:

1. `train.py` — trains the models, compares them, and saves the best one.
2. `predict.py` — a command-line tool that loads the saved model and scores one
   message.
3. `model.joblib` — the saved pipeline, vectoriser and classifier in one file.
4. `report.md` — a short writeup of what you found, including what the filter
   gets wrong and who that hurts.

## Starter

Three files to paste. All three run as pasted — badly, on purpose, which is the
point of running them first. Make a folder, put the three in it, and install
what they need:

```bash
mkdir week-14-spam
cd week-14-spam
python -m pip install scikit-learn pandas joblib
```

### `sample-data.csv`

Thirty labelled messages so the pipeline runs before you have downloaded
anything. Three columns: `label` is `spam` or `ham`, `group` says what kind of
message it is, and `text` is the message. The `group` column is not a feature —
the model never sees it — it exists so you can score each kind of message
separately at the end.

```text
label,group,text
spam,spam,"WIN a free iPhone! Click http://bit.ly/x7q now."
spam,spam,"URGENT. You have won 1000 pounds in the prize draw. Claim at http://bit.ly/x7q."
spam,spam,"Cheap watches online up to 90% off. Limited stock so order today."
spam,spam,"You are pre-approved for a 2500 pounds loan. No credit check needed."
spam,spam,"Free entry to the draw. Text WIN to 80086. Offer ends Friday."
spam,spam,"Final notice. Claim your 500 pounds refund at http://tinyurl.com/9kd."
spam,spam,"Exclusive offer just for you. Unbeatable deal on a laptop. Act now."
spam,spam,"Double your money in 30 days. Risk free trial. Verify at http://claim-now.co."
spam,spam,"You have been selected for a free cruise. Reply now before it expires."
spam,spam,"Your PayPal account is suspended. Verify at http://claim-now.co within 24 hours."
ham,ham-personal,"Are you home for dinner?"
ham,ham-personal,"Running ten minutes late sorry."
ham,ham-personal,"Can you grab milk on the way back."
ham,ham-personal,"Happy birthday! Hope you have a lovely Saturday."
ham,ham-personal,"Did you find my keys anywhere?"
ham,ham-personal,"Mum says dinner is at seven."
ham,ham-personal,"Call me when you get out of class."
ham,ham-personal,"The spare key is under the plant pot."
ham,ham-personal,"Want to walk the dog before it rains?"
ham,ham-personal,"That film was better than I expected."
ham,ham-personal,"Shall we get pizza tonight?"
ham,ham-personal,"Bring a jumper it is freezing."
ham,ham-business,"Your Argos order A4192 has shipped. Track it at http://bit.ly/x7q."
ham,ham-business,"Your appointment at Oakfield Surgery is on Friday. Reply STOP to opt out."
ham,ham-business,"URGENT. Your prescription is ready to collect. Confirm at http://tinyurl.com/9kd."
ham,ham-business,"Your Barclays statement is ready. Manage it online at http://claim-now.co."
ham,ham-business,"Free flu jab clinic at the eye clinic this Tuesday. Book at http://bit.ly/x7q."
ham,ham-business,"We would like to offer you an interview on Monday. Confirm at http://bit.ly/x7q."
ham,ham-business,"Your loyalty points expire Sunday. Act now and spend them free in store."
ham,ham-business,"Your delivery arrives Monday. Quote reference B7730."
```

### `train.py`

The plumbing, plus one working model so you can see the shape of the output.
Four TODOs turn it into the project.

```python
"""train.py — Week 14 mini-project. Trains a spam filter and saves it."""

from __future__ import annotations

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42


def load(path: str = "sample-data.csv") -> pd.DataFrame:
    """Read the CSV and turn the spam/ham column into 1s and 0s."""
    messages = pd.read_csv(path)
    messages["label"] = (messages["label"] == "spam").astype(int)
    return messages


def main() -> None:
    messages = load()
    print(f"messages: {len(messages)}   spam: {int(messages['label'].sum())}")

    train, test = train_test_split(
        messages,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=messages["label"],
    )

    baseline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )
    baseline.fit(train["text"], train["label"])
    predictions = baseline.predict(test["text"])

    print(
        classification_report(
            test["label"], predictions, target_names=["ham", "spam"], zero_division=0
        )
    )
    print(confusion_matrix(test["label"], predictions))

    # TODO 1: add MultinomialNB and RandomForestClassifier(random_state=42) as
    #         two more pipelines, built the same way, and score all three.
    # TODO 2: pick the winner on cross_val_score(..., cv=5, scoring="f1") over
    #         the training half, not on the test score.
    # TODO 3: print accuracy and the count of real messages wrongly blocked for
    #         each value in the "group" column, one row per group.
    # TODO 4: joblib.dump(winner, "model.joblib") — the whole Pipeline, one file.


if __name__ == "__main__":
    main()
```

Run it now, before you change anything:

```bash
python train.py
```

It works, and it calls every single test message ham — `precision 0.00` and
`recall 0.00` on the spam row. That is not a bug you have to fix. Thirty
messages leave twenty-two to train on, and twenty-two examples is not enough to
learn anything about language. Growing the pile is the first real step, and it
is why the finished answer writes itself six hundred messages instead.

### `predict.py`

```python
"""predict.py — Week 14 mini-project. Scores one message with the saved model."""

from __future__ import annotations

import sys

import joblib


def main() -> None:
    if len(sys.argv) < 2:
        print('usage: python predict.py "your message here"', file=sys.stderr)
        raise SystemExit(2)

    model = joblib.load("model.joblib")
    probability = model.predict_proba([sys.argv[1]])[0][1]
    label = "spam" if probability >= 0.5 else "ham"
    print(f"{label} (probability {probability:.2f})")


if __name__ == "__main__":
    main()
```

It needs `model.joblib`, so it only works after TODO 4. The CLI you are aiming
for:

```bash
python train.py
# compares the models, prints the metrics, writes model.joblib

python predict.py "Congratulations! You won a free cruise. Click here."
# spam (probability 0.92)

python predict.py "Are you home for dinner?"
# ham (probability 0.04)
```

## Requirements

1. **Preprocess the text with `TfidfVectorizer`, inside a `Pipeline`.** Set
   `lowercase=True` (the default) and `stop_words="english"`. Use
   `ngram_range=(1, 2)` so the model sees word pairs as well as single words —
   try it both ways and keep the better one.
2. **Compare at least three classifiers**, each in its own pipeline with the
   same vectoriser settings:
   - `LogisticRegression`
   - `MultinomialNB` — Naive Bayes, historically the spam-filter classic
   - `RandomForestClassifier` *or* `DecisionTreeClassifier`
3. **Pin `random_state=42` everywhere it is accepted** — the `train_test_split`,
   the `LogisticRegression`, the forest, and the seed of any generator you write.
   Forty-two is the number the output on this page was produced with. Change it
   and your numbers will move, which is fine as long as you change it on purpose.
4. **Split with `stratify`.** `train_test_split(..., test_size=0.25,
   random_state=42, stratify=y)` so the test set has the same spam share as the
   whole pile.
5. **Report precision, recall, F1 and a confusion matrix** on the held-out test
   set. All four, not just accuracy. `classification_report` prints the first
   three per class in one call.
6. **Choose the winner by cross-validation on the training half, not by the test
   score.** `cross_val_score(pipeline, x_train, y_train, cv=5, scoring="f1")`.
   Look at the test set once, after you have committed.
7. **Audit the winner group by group.** Print accuracy and the number of real
   messages wrongly blocked for each value of the `group` column separately. One
   row per group.
8. **Say why you picked the model you picked**, in `report.md`. "Highest F1 on
   spam" is a reasonable default — but if the person you are building for cares
   more about never missing a scam, recall dominates, and if they care more about
   never losing a real message, precision does. State your criterion out loud.
9. **Save the chosen pipeline with `joblib.dump`.** One `Pipeline`, one file. The
   vectoriser and the classifier go in together or the saved model is useless.
10. **Build the `predict.py` CLI.** It loads `model.joblib`, reads a message from
    `sys.argv[1]`, and prints `spam` or `ham` plus the predicted probability of
    spam.
11. **Write `report.md`**, including a section titled **"Limitations and risks"**
    of at least 150 words that answers four questions:
    - What does the model do badly? Read your own false positives and false
      negatives and quote two of them.
    - What harm could a deployed filter cause? A blocked job offer, a blocked
      appointment reminder and a blocked emergency alert cost different people
      very different amounts.
    - How does somebody appeal a decision? Name the mechanism.
    - Does the model amplify anything in your training data you would not want
      amplified at scale?

    This section is not lip service. It is the difference between an ML engineer
    and somebody with a `model.fit()` habit.

## Constraints

- **The vectoriser goes inside the `Pipeline`, never beside it.** Fit a
  `TfidfVectorizer` on all the messages before you split and it learns its
  vocabulary and its word weights from the test messages too. That is
  **leakage**: the score comes back higher than the model deserves, and you have
  no way to tell by looking. Inside a pipeline, `fit` only ever sees the training
  fold, and every later `predict` reuses what that fold learned.
- **Never tune against the test set.** Every time you look at the test score and
  change something, a little of that test set leaks into your choice. Use
  cross-validation on the training half for every decision, and spend the test
  set once at the end. A test score you have optimised against is not an
  estimate any more; it is a target you hit.
- **Stratify the split.** Spam is the smaller class. An unstratified split can
  hand you a test set with barely any spam in it, and a spam recall computed on
  four messages is noise wearing a decimal point.
- **Accuracy alone is banned in your report.** If 1 message in 100 were spam, a
  filter that says "ham" to everything scores 99% and catches nothing.
  Precision, recall and F1 are the numbers that can tell the difference; accuracy
  cannot.
- **Save one file, not three.** `joblib.dump(pipeline, "model.joblib")` writes
  the vectoriser, the classifier and the order they run in. Save the classifier
  alone and `predict.py` has no way to turn text into numbers the same way
  training did — and a *nearly* right vectoriser is worse than none, because it
  fails silently.
- **`predict.py` must survive junk input.** An empty string, an emoji, a
  thousand characters of nothing. A CLI that throws a traceback at a user is a
  CLI that gets uninstalled.
- **Pin every seed.** Without `random_state` the split moves, the forest moves,
  and two runs of your own project disagree. You cannot debug a program whose
  output changes when nothing changed.

## Expected output

This is the finished project, run end to end. The messages are generated from a
pinned seed inside the file, so this run is the same on every machine.

```text
$ python sms-spam-classifier.py
SMS Spam Classifier - the Week 14 mini-project, end to end.

1. The messages
messages: 600   spam: 200   ham: 400
group
spam            200
ham-personal    250
ham-business    150
train rows: 450   test rows: 150

2. Compare three models
model                cv F1 (train)    precision   recall       F1
LogisticRegression   0.869 +/- 0.050      0.917    0.880    0.898
MultinomialNB        0.893 +/- 0.032      0.868    0.920    0.893
RandomForest         0.842 +/- 0.046      0.887    0.940    0.913
chosen on cross-validated F1: MultinomialNB (0.893)

3. The winner on the held-out test set: MultinomialNB
              precision    recall  f1-score   support

         ham       0.96      0.93      0.94       100
        spam       0.87      0.92      0.89        50

    accuracy                           0.93       150
   macro avg       0.91      0.93      0.92       150
weighted avg       0.93      0.93      0.93       150

confusion matrix (rows actual, columns predicted)
             pred ham   pred spam
actual ham         93           7
actual spam         4          46

4. The same model, group by group
group            messages   accuracy   real messages blocked
spam                   50      0.920   n/a - no real messages in this group
ham-personal           67      1.000   0 of 67 (0.0%)
ham-business           33      0.788   7 of 33 (21.2%)

5. Save the whole pipeline, load it back, classify new messages
saved model.joblib (63 KB)
spam (probability 0.83)  Congratulations! You won a free cruise. Click http:/
ham  (probability 0.03)  Are you home for dinner?
ham  (probability 0.02)  Your appointment at Oakfield Surgery is on Friday. R
ham  (probability 0.21)  URGENT. Your prescription is ready to collect. Confi
```

### What that 0.93 means, and what it does not

The headline number is **93% accuracy**, and there are four honest things to say
about it before you put it in a report.

**It is an estimate, not a measurement.** It comes from 150 messages the model
had not seen. Score a different 150 and you get a different number. That is what
the `+/- 0.032` beside the cross-validated F1 is telling you: five different
splits of the same training data disagreed with each other by about three
points. Any single split — including this one — could be a lucky one or an
unlucky one, and a score quoted to two decimal places from one split is quoted
with more confidence than it has earned.

**It moves when the split moves.** Change `random_state=42` to `random_state=7`
and every number on this page changes. Nothing about the model got better or
worse. This is exactly why the seed is pinned and why the comparison between the
three models is done on five folds instead of one.

**A model can score well and still be wrong in ways the score cannot see.** The
number counts mistakes. It does not know *which* mistakes, or who pays for them.
Losing a scam text costs you nothing. Losing a message from your doctor might
cost you a great deal, and both show up in that 0.93 as one unit of wrong.

**And an equal-looking overall number can hide very different error rates
between groups.** That is what section 4 is for, and it is the most important
block of output on the page:

| group | accuracy | real messages wrongly blocked |
|-------|----------|-------------------------------|
| `ham-personal` | 1.000 | 0 of 67 (0.0%) |
| `ham-business` | 0.788 | 7 of 33 (21.2%) |

Both groups are inside the same 93%. Split them and the filter turns out to be
**perfect on messages from your friends and wrong about one business message in
five.** Every message it blocked was a real one — a delivery notice, a
prescription, an interview invitation — and it blocked them because a courier
and a scam use the same words: *urgent*, *confirm*, *free*, and a link.

Nobody would ever see that from the headline number. This is the whole reason
[Lecture 3](../lecture-notes/03-pipelines-evaluation-and-ethics.md) tells you to
compute precision and recall separately for every group you can name, and the
reason Homework Problem 6 makes you do it again. **The test set being good is not
enough.** If the gap between groups is unacceptable, the model is unfit to ship,
whatever the headline says.

Look at the last line of the run too. The clinic's real message — "URGENT. Your
prescription is ready to collect. Confirm at …" — comes back `ham`, but at
probability 0.21, seven times closer to the line than "Are you home for dinner?"
at 0.03. It survives. The next one like it might not.

## Steps

Four TODOs, worked top to bottom. Run `train.py` after each one.

1. **Grow the data first.** Thirty messages cannot teach a model language. Either
   write a generator like the one in the answer below, or skip ahead and download
   the real UCI SMS Spam Collection (see Stretch). Everything after this step is
   more informative with a few hundred messages behind it.
2. **TODO 1 — the other two models.** Build `MultinomialNB` and
   `RandomForestClassifier(random_state=42)` as two more pipelines with the same
   `TfidfVectorizer` settings, so the only thing that differs between the three
   is the classifier. Print precision, recall and F1 for each on the test set.
3. **TODO 2 — choose honestly.** `cross_val_score(pipeline, x_train, y_train,
   cv=5, scoring="f1")` gives you five numbers per model. Take the mean to
   choose and the standard deviation to know how much to trust the choice. The
   winner is decided here, on the training half, before the test set is read.
4. **TODO 3 — the group audit.** Filter the test rows by the `group` column, run
   `model.predict` on each group on its own, and print accuracy plus how many
   real messages that group lost. This is four lines of pandas and it is the most
   valuable output your project produces.
5. **TODO 4 — save and reload.** `joblib.dump(winner, "model.joblib")`, then
   `joblib.load` it in `predict.py` and score a message from the command line.
   Reloading in a *different process* is the only thing that proves the save
   worked.
6. **Write `report.md` last**, from your own numbers. Quote two messages the
   model got wrong, by hand, out of your own test set. The "Limitations and
   risks" section is easy to write once you have read the mistakes and
   impossible to fake if you have not.

## The Solution

```python
"""sms-spam-classifier.py — the finished answer to the Week 14 mini-project.

Everything the project asks for, in one file that runs on its own: build the
message table, split it, train three classifiers inside pipelines, score them
honestly, pick a winner, audit it group by group, save it with joblib, load it
back, and classify new messages the way ``predict.py`` will.

Your own deliverable is four things — ``train.py``, ``predict.py``,
``model.joblib`` and ``report.md``. Four files cannot be started by one
``python`` command, so the reference answer folds them into this one script:
``build_corpus`` and ``compare_models`` are ``train.py``, ``classify`` is
``predict.py``, and ``audit_by_group`` is the evidence your report's
"Limitations and risks" section is built on.

No text corpus ships with scikit-learn, and the real UCI SMS Spam Collection
needs a download, so the 600 messages here are written on the spot out of shared
phrase pools. Every seed in the file is ``RANDOM_STATE = 42``: the message
generator, the train/test split, the logistic solver and the forest. That is why
the numbers printed below are the same on every machine, and it is the only
reason this page can promise you an output block at all.

The saved model goes into a throwaway temporary directory that Python deletes on
the way out, so the download leaves nothing behind. Yours writes a real
``model.joblib`` beside ``train.py``.

Run it with::

    python sms-spam-classifier.py
"""

from __future__ import annotations

import random
import tempfile
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42

# Five pools of phrases, with blanks to fill in. A message is a few of them
# stuck together. "sell" is a scam trying to sell you something and "chat" is
# somebody you know, but "alarm" and "link" belong to nobody: a scam shouts a
# deadline and sends a link, and so does the courier, the clinic and the bank.
# That shared middle is not decoration. It is the whole point of this project.
POOLS = {
    "sell": [
        "win a free {prize}",
        "you have won {money} in the prize draw",
        "claim your prize",
        "cheap {product} online up to 90% off",
        "you are pre-approved for a {money} loan",
        "text WIN to 80086",
        "exclusive offer just for you",
        "no credit check needed",
        "double your money in 30 days",
        "free entry to the draw",
        "limited stock so order today",
        "risk free trial of {product}",
        "unbeatable deal on a {prize}",
        "get {money} cashback instantly",
        "you have been selected for a free {prize}",
    ],
    "alarm": [
        "URGENT",
        "act now",
        "final notice",
        "within 24 hours",
        "before it expires",
        "last chance",
        "immediate action required",
        "do not ignore this message",
        "offer ends {day}",
        "reply now",
    ],
    "link": [
        "click {link}",
        "verify at {link}",
        "details at {link}",
        "book at {link}",
        "track it at {link}",
        "confirm at {link}",
        "manage it online at {link}",
    ],
    "admin": [
        "your {shop} order {code} has shipped",
        "your appointment at {clinic} is on {day}",
        "your {bank} statement is ready",
        "your prescription is ready to collect",
        "your delivery arrives {day}",
        "your payment of {money} was received",
        "we would like to offer you an interview on {day}",
        "your loyalty points expire {day}",
        "quote reference {code}",
        "your {bank} balance has changed",
        "flu jab clinic at {clinic} this {day}",
        "reply STOP to opt out",
    ],
    "chat": [
        "are you home for dinner",
        "running ten minutes late sorry",
        "can you grab {product} on the way back",
        "happy birthday hope you have a lovely {day}",
        "did you find my keys",
        "mum says dinner is at seven",
        "that film was better than I expected",
        "call me when you get out of class",
        "the spare key is under the plant pot",
        "want to walk the dog before it rains",
        "see you {day} then",
        "I am on the bus",
        "how did the exam go",
        "sorry I missed your call",
        "shall we get pizza",
        "the cat was sick on the rug again",
        "bring a jumper it is freezing",
        "I will be at the usual place",
        "loved the photos you sent",
        "tell your mum I said hi",
    ],
}

# How much each kind of message draws from each pool. Read the columns, not the
# rows: "alarm" and "link" belong to spam and to real businesses alike, which is
# exactly why a filter trained on this will hurt the clinic and the courier more
# than it hurts your friends. That is what the group audit at the end measures.
MIXTURES = {
    "spam": {"sell": 0.55, "alarm": 0.20, "link": 0.20, "admin": 0.05},
    "ham-business": {"admin": 0.45, "link": 0.25, "alarm": 0.22, "sell": 0.08},
    "ham-personal": {"chat": 0.92, "admin": 0.05, "alarm": 0.03},
}

FILLERS = {
    "prize": ["iPhone", "cruise", "holiday", "laptop", "gift card"],
    "link": ["http://bit.ly/x7q", "http://tinyurl.com/9kd", "http://claim-now.co"],
    "bank": ["Halifax", "Barclays", "PayPal", "Natwest"],
    "money": ["1000 pounds", "500 pounds", "2500 pounds", "150 pounds"],
    "day": ["Monday", "Tuesday", "Friday", "Saturday", "Sunday"],
    "product": ["milk", "trainers", "watches", "coffee", "bread"],
    "shop": ["Argos", "Tesco", "Royal Mail", "Evri"],
    "clinic": ["Oakfield Surgery", "the dental practice", "the eye clinic"],
    "code": ["A4192", "B7730", "C2085", "D6641"],
}

GROUPS = ["spam", "ham-personal", "ham-business"]

NEW_MESSAGES = [
    "Congratulations! You won a free cruise. Click http://bit.ly/x7q now.",
    "Are you home for dinner?",
    "Your appointment at Oakfield Surgery is on Friday. Reply STOP to opt out.",
    "URGENT. Your prescription is ready to collect. Confirm at http://bit.ly/x7q.",
]


def fill(phrase: str, rng: random.Random) -> str:
    """Fill one phrase's blanks from FILLERS, one random choice each."""
    filled = phrase
    for slot, options in FILLERS.items():
        token = "{" + slot + "}"
        while token in filled:
            filled = filled.replace(token, rng.choice(options), 1)
    return filled


def compose(group: str, rng: random.Random) -> str:
    """Write one message: two to four phrases drawn from the group's mixture."""
    pools = list(MIXTURES[group])
    weights = [MIXTURES[group][pool] for pool in pools]
    phrases = [
        fill(rng.choice(POOLS[rng.choices(pools, weights)[0]]), rng)
        for _ in range(rng.randint(2, 4))
    ]
    return ". ".join(phrases) + "."


def build_corpus(seed: int = RANDOM_STATE) -> pd.DataFrame:
    """The 600 labelled messages, dealt out from a pinned seed.

    Three columns come back: ``text``, ``label`` (1 for spam, 0 for ham) and
    ``group``, which the headline metrics ignore and the audit does not.

    Nothing here is copied from a template list, because a corpus whose classes
    never overlap trains a model that scores a perfect 1.00 and teaches you
    nothing. Every message is a handful of phrases pulled from shared pools, and
    the only thing that separates a scam from a delivery notice is *how often*
    each pool gets picked. Spam mostly sells; a business mostly informs; both
    shout deadlines and both send links.
    """
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    plan = [("spam", 1, 200), ("ham-personal", 0, 250), ("ham-business", 0, 150)]

    for group, label, count in plan:
        for _ in range(count):
            rows.append({"text": compose(group, rng), "label": label, "group": group})

    rng.shuffle(rows)
    return pd.DataFrame(rows)


def make_pipeline(classifier) -> Pipeline:
    """TF-IDF and a classifier welded into one estimator.

    The vectoriser lives *inside* the pipeline on purpose. Fit it outside and it
    learns its vocabulary and its word weights from the test messages too, which
    is leakage: the score comes back flattering and false.
    """
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("clf", classifier),
        ]
    )


def candidates() -> dict[str, Pipeline]:
    """The three models the project asks you to compare."""
    return {
        "LogisticRegression": make_pipeline(
            LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
        ),
        "MultinomialNB": make_pipeline(MultinomialNB()),
        "RandomForest": make_pipeline(
            RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
        ),
    }


def compare_models(x_train, y_train, x_test, y_test) -> tuple[str, Pipeline]:
    """Cross-validate every candidate on the training half, then score the test.

    The winner is chosen on cross-validated F1 over the training messages, never
    on the test score. The test set gets looked at once, after the decision, so
    it stays an honest estimate rather than a thing we shopped for.
    """
    print("model                cv F1 (train)    precision   recall       F1")
    best_name, best_score = "", -1.0
    fitted: dict[str, Pipeline] = {}

    for name, pipeline in candidates().items():
        folds = cross_val_score(pipeline, x_train, y_train, cv=5, scoring="f1")
        pipeline.fit(x_train, y_train)
        fitted[name] = pipeline

        predictions = pipeline.predict(x_test)
        matrix = confusion_matrix(y_test, predictions)
        true_negative, false_positive, false_negative, true_positive = matrix.ravel()
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        test_f1 = f1_score(y_test, predictions)

        print(
            f"{name:<21}{folds.mean():.3f} +/- {folds.std():.3f}"
            f"      {precision:.3f}    {recall:.3f}    {test_f1:.3f}"
        )
        if folds.mean() > best_score:
            best_name, best_score = name, folds.mean()

    print(f"chosen on cross-validated F1: {best_name} ({best_score:.3f})")
    return best_name, fitted[best_name]


def report(model: Pipeline, x_test, y_test) -> None:
    """The four numbers per class, plus the table that says where it went wrong."""
    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions, target_names=["ham", "spam"]))
    matrix = confusion_matrix(y_test, predictions)
    true_negative, false_positive, false_negative, true_positive = matrix.ravel()
    print("confusion matrix (rows actual, columns predicted)")
    print("             pred ham   pred spam")
    print(f"actual ham   {true_negative:>8}   {false_positive:>9}")
    print(f"actual spam  {false_negative:>8}   {true_positive:>9}")


def audit_by_group(model: Pipeline, test: pd.DataFrame) -> None:
    """Score the winner separately for each group of messages.

    This is the part a headline accuracy cannot show you. Every one of these
    messages is in the same test set and the same overall number; split them and
    the model turns out to be far rougher on legitimate business texts than on
    messages from a friend.
    """
    print("group            messages   accuracy   real messages blocked")
    for group in GROUPS:
        rows = test[test["group"] == group]
        predictions = model.predict(rows["text"])
        accuracy = (predictions == rows["label"]).sum() / len(rows)
        if group == "spam":
            blocked = "n/a - no real messages in this group"
        else:
            wrong = int(((predictions == 1) & (rows["label"] == 0)).sum())
            blocked = f"{wrong} of {len(rows)} ({wrong / len(rows):.1%})"
        print(f"{group:<17}{len(rows):>8}      {accuracy:.3f}   {blocked}")


def classify(model_path: Path, messages: list[str]) -> None:
    """What ``predict.py`` does: load the one saved file and score raw text."""
    model = joblib.load(model_path)
    for message in messages:
        probability = model.predict_proba([message])[0][1]
        label = "spam" if probability >= 0.5 else "ham "
        print(f"{label} (probability {probability:.2f})  {message[:52]}")


def main() -> None:
    """Train, compare, audit, save, reload, predict."""
    print("SMS Spam Classifier - the Week 14 mini-project, end to end.")

    print()
    print("1. The messages")
    corpus = build_corpus()
    print(f"messages: {len(corpus)}   spam: {int(corpus['label'].sum())}   "
          f"ham: {int((corpus['label'] == 0).sum())}")
    print(corpus["group"].value_counts().reindex(GROUPS).to_string())

    train, test = train_test_split(
        corpus,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=corpus["label"],
    )
    print(f"train rows: {len(train)}   test rows: {len(test)}")

    x_train, y_train = train["text"], train["label"]
    x_test, y_test = test["text"], test["label"]

    print()
    print("2. Compare three models")
    best_name, model = compare_models(x_train, y_train, x_test, y_test)

    print()
    print(f"3. The winner on the held-out test set: {best_name}")
    report(model, x_test, y_test)

    print()
    print("4. The same model, group by group")
    audit_by_group(model, test)

    print()
    print("5. Save the whole pipeline, load it back, classify new messages")
    with tempfile.TemporaryDirectory() as workspace:
        model_path = Path(workspace) / "model.joblib"
        joblib.dump(model, model_path)
        print(f"saved model.joblib ({model_path.stat().st_size // 1024} KB)")
        classify(model_path, NEW_MESSAGES)


if __name__ == "__main__":
    main()
```

**Why it works.** The four files you deliver are folded into one script, in the
order the project asks for them. `build_corpus` and `compare_models` are
`train.py`, `classify` is `predict.py`, `audit_by_group` is the evidence
`report.md` is built on, and `main()` runs them one after another with a
numbered heading before each. Read it top to bottom and you are reading the
finished project.

**The messages are written, not downloaded.** No text dataset ships with
scikit-learn and the real UCI collection needs a network connection, so the
corpus is built from five pools of phrases: `sell`, `alarm`, `link`, `admin` and
`chat`. A message is two to four of those phrases stuck together. What makes a
message spam is not any single phrase — it is *how often each pool gets picked*.
Spam mostly sells, a business mostly informs, and both shout deadlines and both
send links. That shared middle is deliberate. Delete it and every model scores a
perfect 1.00 and you learn nothing, which is exactly what happened the first time
this project was written with tidy one-line templates.

**`Pipeline` is what makes the score believable.** `make_pipeline` welds the
`TfidfVectorizer` to the classifier so they are one object with one `fit` and
one `predict`. When `cross_val_score` splits the training data five ways, the
vectoriser is rebuilt from scratch inside each fold, on that fold's training
rows only. Do it by hand and the vectoriser sees every message before the split,
the vocabulary and the word weights are contaminated, and the score comes back
flattering and false — with no error message anywhere.

**The winner is chosen before the test set is read.** `compare_models` picks on
the mean of five cross-validated F1 scores over the training half. The test
numbers are printed in the same table, but they are not what decides. That
ordering is the whole difference between "here is my estimate of how this will
do" and "here is the best of the numbers I kept looking at". Note that the
choice and the test set disagree here: the forest has the best test F1 (0.913)
and still loses, because cross-validation says its five folds were the least
consistent (0.842). The rule survives being inconvenient, or it is not a rule.

**One `joblib` file, reloaded in the same run.** `joblib.dump` writes the
vectoriser, the classifier and the order they run in. `classify` then calls
`joblib.load` and predicts from the loaded object, not from the one still in
memory — that round trip is the only thing that proves the save is complete. A
pipeline saved without its vectoriser loads without complaint and predicts
nonsense forever.

**`predict_proba` gives a number, not a verdict.** The model reports how spammy
it thinks a message is, between 0 and 1, and the `>= 0.5` on the next line turns
that into a decision. The threshold is a **policy choice**, not a fact about the
model. Raise it to 0.8 and the filter blocks fewer real messages and misses more
scams; drop it to 0.3 and the opposite. Whoever is harmed by the mistakes should
be who sets that number.

## Download and run

<!-- no-runnable-file: what you hand in is four files - train.py, predict.py, model.joblib and report.md - and four files cannot be started by one python command, so there is nothing this page could name README-solution.py without lying about the shape of the project. The runnable answer ships beside this page as sms-spam-classifier.py, all four folded into one script, and is linked from Download and run. -->

Download [sms-spam-classifier.py](./sms-spam-classifier.py) and run it:

```bash
python -m pip install scikit-learn pandas joblib
python sms-spam-classifier.py
```

It prints the run above, exactly. There is nothing to download and no network
call: the six hundred messages are written by the file itself from
`RANDOM_STATE = 42`, and every other seed in it is the same 42, so the split,
the logistic solver and the forest all land in the same place on every machine.
The saved `model.joblib` goes into a throwaway temporary directory that Python
deletes on the way out, so the download leaves nothing behind. Yours writes a
real `model.joblib` beside `train.py`, which is what `predict.py` needs.

The file is named after the project, not after this page, so it can never be
confused with the `train.py` and `predict.py` you are supposed to write.

## Common bugs to catch

- **`FileNotFoundError: [Errno 2] No such file or directory: 'sample-data.csv'`.**
  You are running `train.py` from a different folder than the CSV. `pd.read_csv`
  resolves relative paths against the working directory, not the script.
- **Every test message comes back `ham`, and the spam row of the report is all
  zeros.** With thirty messages, that is the starter behaving as described — you
  have twenty-two training rows. With six hundred it means something is wrong:
  check that `label` really is 1s and 0s and not the strings `"spam"` and
  `"ham"`.
- **`UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in
  labels with no predicted samples`.** The model predicted spam for nothing at
  all, so precision is a division by zero. `zero_division=0` silences the
  warning; it does not fix the model.
- **`ValueError: The least populated class in y has only 1 member, which is too
  few. The minimum number of groups for any class cannot be less than 2.`** You
  passed `stratify=` a column with a class that appears once. Check
  `df["label"].value_counts()`.
- **The scores are suspiciously perfect — 1.00 everywhere.** Two usual causes.
  Either you fit the vectoriser outside the pipeline, on all the data, and leaked
  the test set into training; or your messages are so templated that the test
  rows are literal duplicates of training rows. Both make a model that looks
  brilliant and helps nobody.
- **`AttributeError: 'MultinomialNB' object has no attribute 'predict_proba'`
  after loading.** You saved the classifier instead of the pipeline, so what
  loaded is not what you trained. `joblib.dump(pipeline, ...)`, never
  `joblib.dump(pipeline.named_steps["clf"], ...)`.
- **`ValueError: X has 412 features, but MultinomialNB is expecting 1841
  features as input`.** Same cause, seen from the other end: a classifier saved
  alone is being fed text vectorised by a *different* vectoriser. The pipeline
  exists so this cannot happen.
- **`predict.py` crashes on `model.predict_proba("some text")`.** The pipeline
  expects a list of messages, not one string. Pass `[message]`. Give it a bare
  string and the vectoriser treats each character as a document.
- **Two runs print different numbers.** A `random_state` is missing somewhere —
  most often on the forest, which is easy to forget because the split has one.
- **`InconsistentVersionWarning: Trying to unpickle estimator … from version
  1.4.2 when using version 1.6.1`.** The `model.joblib` was written by a
  different scikit-learn. Retrain rather than trusting it; a pickle is not a
  portable format.

## Under the hood

<details>
<summary>Under the hood — what TF-IDF actually computes</summary>

TF-IDF turns a message into a row of numbers, one column per word the vectoriser
saw during training. The name is two ideas multiplied together.

**TF, term frequency.** How often this word appears in *this* message. Say
"free" three times and the number goes up.

**IDF, inverse document frequency.** How rare this word is across *all* the
messages. A word in nearly every message — "the", "your", "at" — gets a tiny
weight. A word in one message out of fifty gets a large one. The formula
scikit-learn uses is roughly `log(number of messages / number containing the
word)`, plus some smoothing so a word seen everywhere never divides by zero.

Multiply them and you get "words this message uses a lot, that most messages do
not use". That is a decent mechanical definition of what a text is *about*, and
it is why a plain word count is a worse feature: a count is dominated by the
most common words, which are the least informative ones.

`stop_words="english"` throws out a list of the very commonest words before any
of this happens. `ngram_range=(1, 2)` adds every adjacent pair as its own column,
so "not free" can be distinguished from "free" — bag-of-words has no idea what
order anything came in, and pairs buy back a sliver of that.

The result is very wide and almost entirely zeros: a few thousand columns, of
which a given message uses maybe twenty. scikit-learn stores it as a **sparse
matrix**, keeping only the non-zero entries and their positions. A dense array
of 600 × 3000 floats would be 14 MB of mostly nothing.

</details>

<details>
<summary>Under the hood — why Naive Bayes is "naive", and why it wins anyway</summary>

Naive Bayes asks a question in reverse. You want "given these words, how likely
is spam?" It is far easier to count "given spam, how likely are these words?" —
you just tally the training messages. **Bayes' theorem** is the piece of
arithmetic that flips one into the other.

The naive part is what it assumes to make the flip cheap: that every word is
independent of every other word, given the label. It assumes that knowing a
message contains "free" tells you nothing about whether it also contains "prize".
That is plainly false. "Free" and "prize" travel together constantly.

And it works anyway, which is one of the genuinely strange results in machine
learning. The reason is that the assumption wrecks the *probabilities* while
usually preserving the *ranking*. Naive Bayes will tell you a message is 99.98%
spam when the honest answer is 80% — it double-counts evidence from correlated
words. But it still puts the spammy messages above the non-spammy ones, and a
classifier only has to get the order right on either side of the threshold.

`MultinomialNB` is the variant for counts, which is why it pairs with a
bag-of-words. It has no `random_state` because there is nothing random in it: it
counts, and counting gives the same answer twice. It also trains in a single pass
over the data, which is why spam filters ran on it for twenty years on hardware
that could not have afforded anything else.

</details>

<details>
<summary>Under the hood — precision, recall, and why one number cannot serve</summary>

Every prediction lands in one of four boxes. The message is spam or it is not;
the filter said spam or it did not.

|  | filter said ham | filter said spam |
|--|-----------------|------------------|
| **really ham** | true negative | **false positive** — a real message blocked |
| **really spam** | **false negative** — a scam let through | true positive |

**Precision** is `TP / (TP + FP)`: when the filter cries spam, how often is it
right? Low precision means real messages are being eaten.

**Recall** is `TP / (TP + FN)`: of all the real spam, how much did we catch? Low
recall means scams are getting through.

They trade against each other, and the thing that moves them is the threshold.
Block anything over 0.9 and precision goes up and recall goes down. Block
anything over 0.1 and the reverse. **F1** is the harmonic mean of the two, which
is a fancy way of saying it is a single number that stays low if *either* is low
— you cannot buy a good F1 by maxing one and abandoning the other.

Which one matters is never a technical question. A spam filter on a personal
phone should probably favour precision: missing a scam is annoying, losing a
message from the school is not. A fraud detector on a bank's card network favours
recall, because a flagged transaction gets a phone call and a missed one gets a
stolen account. Same maths, opposite settings, and the difference is decided by
who gets hurt — which means it is not yours to decide alone.

</details>

<details>
<summary>Under the hood — joblib, pickle, and why you should never load a model you did not make</summary>

`joblib.dump` is `pickle` with a large-array optimisation. Pickle is Python's own
serialisation format: it writes out enough to rebuild an object later, and for
NumPy arrays joblib stores the raw buffers instead of pickling them element by
element, which is why it is the recommended way to save a scikit-learn model.

Two things follow, and both matter.

**A pickle is not a data format, it is a program.** Loading one runs
instructions that construct objects, and a maliciously crafted pickle can run
whatever it likes on your machine while `joblib.load` is still returning. Treat a
`.joblib` from the internet exactly as you would treat a downloaded `.exe`. This
is a real supply-chain attack surface on model hubs, not a hypothetical.

**A pickle is bound to the code that made it.** It stores which classes to
rebuild, not their source, so loading it needs the same library available — and
a version mismatch gives you `InconsistentVersionWarning` at best and silently
different behaviour at worst. That is why a saved model should always travel with
a pinned `requirements.txt`, and why "just retrain it" beats "just load it" the
moment anything in the stack moves. For sharing models across languages or across
years, look at **ONNX**, which serialises the computation rather than the Python
objects.

</details>

## Acceptance checklist

Self-assess out of 12 points. Nine or more is a passing project.

| Area | 2 pts | 1 pt | 0 pts |
|---------------------|----------------------------------------|-------------------------------------|-------------------------|
| Preprocessing | TF-IDF inside a Pipeline, no leakage | TF-IDF separate from model | Bag of bugs |
| Algorithm comparison| 3+ models, fair comparison | 2 models | 1 model |
| Metrics | Precision/recall/F1 + confusion matrix | Accuracy only | None |
| Model persistence | Pipeline saved + loadable | Model only saved | None |
| CLI inference | Works on raw text input | Crashes on edge cases | None |
| Writeup | Clear, honest, includes ethics note | Numbers only | None |

The same six criteria, phrased as things you can check off:

- [ ] The `TfidfVectorizer` is a step inside the `Pipeline`, and nothing is ever
      fit on the full dataset before the split.
- [ ] Three classifiers are compared with identical vectoriser settings.
- [ ] The winner is chosen on cross-validated F1 over the training half, not on
      the test score.
- [ ] Precision, recall, F1 and a confusion matrix print for the winner on the
      held-out test set.
- [ ] The group audit prints one row per `group`, with accuracy and the count of
      real messages wrongly blocked.
- [ ] `random_state=42` is on the split, the logistic model, the forest and any
      generator you wrote — and two runs print identical numbers.
- [ ] `joblib.dump` saved the whole `Pipeline`, and `predict.py` loads it in a
      fresh process and scores a message.
- [ ] `predict.py` handles a missing argument and an empty string without a
      traceback.
- [ ] `report.md` names the criterion you chose the model by, in one sentence.
- [ ] `report.md` has a "Limitations and risks" section of at least 150 words
      that quotes two real mistakes from your own test set and names an appeal
      mechanism.
- [ ] Committed and pushed:

      ```bash
      git add train.py predict.py model.joblib report.md
      git commit -m "feat(week-14): sms spam classifier mini-project"
      git push
      ```

## Stretch

- **Use the real data.** Download the
  [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
  — 5,574 real, professionally labelled messages. Save it as `sms-spam.csv`,
  point `load()` at it, and rerun. Every number you have becomes meaningful, and
  most of them get worse. Real language is messier than any generator.
- **Print the words the model leans on.** Add a `--top-features` flag that prints
  the terms most associated with spam. For the linear model:
  `sorted(zip(pipe.named_steps["tfidf"].get_feature_names_out(),
  pipe.named_steps["clf"].coef_[0]))`. Read the top twenty and ask whether any of
  them is something you would be uncomfortable seeing in a rule written out in
  plain English.
- **Move the threshold on purpose.** Instead of `>= 0.5`, sweep it from 0.1 to
  0.9 and plot precision and recall against it. Then pick the value that blocks
  the fewest real business messages while still catching most spam, and say in
  `report.md` who you optimised for.
- **A tiny web service.** Wrap `predict.py` in a Flask endpoint — you learned
  Flask in [Week 9](../../week-09-web-development-flask/README.md). Now you have
  a real ML service instead of a script.
- **Tests.** Add a `tests/` folder with pytest tests for `load`, the pipeline
  and the CLI, the way you learned in
  [Week 11](../../week-11-testing-debugging/README.md). Assert that a known
  scam scores above 0.8 and a known personal message below 0.2.
- **Keep a log.** Append each training run's metrics to a CSV with a timestamp,
  so you can see whether your changes are actually helping across a whole
  afternoon of them.

That is Week 14, and it is the last mini-project of the course. Everything from
here — better models, bigger data, deeper networks — is a variation on what you
just built: split honestly, measure four ways, look at who the mistakes land on,
and be able to say out loud what your model is doing.
