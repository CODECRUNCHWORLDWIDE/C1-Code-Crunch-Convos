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
