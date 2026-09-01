"""Generate a larger offline SMS spam corpus so the metrics mean something.

`sample-data.csv` has 36 rows. That is enough to prove the pipeline runs, and
far too little to evaluate anything: a stratified 20% test split leaves seven
messages, and one flipped prediction moves F1 by 0.15.

This script builds a deterministic synthetic corpus with the same shape as the
UCI SMS Spam Collection (about 13% spam) so you can look at precision and
recall without pretending seven messages told you something.

    python make_dataset.py --out sms-spam-synthetic.csv --n 1200

Real data is still better. When you have an internet connection, download the
UCI SMS Spam Collection and train on that instead:
https://archive.ics.uci.edu/dataset/228/sms+spam+collection
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

SPAM_TEMPLATES = [
    "WIN a {prize}! Text {word} to {short} now",
    "URGENT! You have won a {prize}. Call {phone} to claim",
    "Congratulations, you have been selected for a FREE {prize}. Reply {word}",
    "FREE entry into our {money} weekly draw! Just text {word} to {short}",
    "You have 1 unclaimed voucher worth {money}. Claim now: {url}",
    "Winner!! As a valued customer you have been selected to receive {money}",
    "Your account has been suspended. Verify immediately at {url}",
    "Final notice: your parcel is held. Pay a small fee at {url}",
    "Get CHEAP loans approved instantly, no credit check. Call {phone}",
    "Claim your FREE {prize} now! Reply STOP to opt out, std rates apply",
    "HOT singles in your area waiting to chat! Text {word} to {short}",
    "Limited offer, {pct} OFF today only, shop here {url}",
    "Double your money in 30 days. Guaranteed returns. Message {word} now",
    "You have WON {money}! Reply {word} within 24 hours or it expires",
    "Your mobile number has won {money} in the draw. Call {phone} to collect",
    "FREE 3 month subscription, no catch. Text {word} to {short} to activate",
    "Exclusive: {prize} reserved in your name. Confirm at {url}",
    "Bank alert: unusual login detected. Secure your account at {url}",
]

HAM_TEMPLATES = [
    "Are you home for {meal}?",
    "Can you pick up {item} on the way back please",
    "Meeting moved to {time}, room {room}. See you there",
    "I'll be about {mins} minutes late, {reason}",
    "Did the {item} arrive yet? Tracking says delivered",
    "Sure, {time} works. I'll book the table",
    "Sorry I missed your call, I was on the train. Ring me back?",
    "The tests all pass now, pushing the branch in a sec",
    "Can you send me the {thing} before the standup tomorrow",
    "Running late for the {event}, save me a seat",
    "Thanks so much for helping out yesterday, really appreciated it",
    "What time does the {event} start?",
    "I left the keys under the mat, let yourself in",
    "See you at the {place} after work",
    "Mum says {meal} is at hers on Sunday, can you make it",
    "lol that video was hilarious, send me the link again",
    "Just landed. Grabbing my bag then heading to the {place}",
    "Do you still need a lift to the {event} on Saturday?",
    "Reminder: {thing} is due Friday. Shout if you are stuck",
    "Coffee at {time}? I need to talk through the {thing}",
]

# Ham messages that deliberately contain spam-ish vocabulary. These are what
# create the false positives you will inspect in the writeup.
HARD_HAM_TEMPLATES = [
    "Your free trial of the gym ends Friday, thought you should know",
    "Congratulations on the promotion!! Drinks on you then",
    "The prize giving at school is at {time}, are you coming",
    "I won the raffle at work, {money} in vouchers, unreal",
    "Call the bank about the account, they left a message",
    "Click the link Sarah sent, the photos are on there {url}",
    "URGENT can you grab {item} before the shop shuts",
    "Free tickets going for the {event}, want one?",
    "Text me when you get the offer through from HR",
    "Winner of the pub quiz again, obviously",
]

# Spam messages written to look ordinary. These create the false negatives.
HARD_SPAM_TEMPLATES = [
    "Hi, are you free to talk about a work opportunity? {url}",
    "Hey it's me, I changed number. Can you send {money} quickly, I'll explain",
    "Your delivery could not be completed. Reschedule: {url}",
    "Following up on my last message about the {item} order, see {url}",
    "Quick question about your car insurance renewal, call {phone}",
    "Photo of you? {url}",
]

SLOTS = {
    "prize": ["FREE iPhone", "cruise for two", "1 week FREE membership", "shopping spree",
              "designer watch", "holiday to Spain", "ringtone", "gift card"],
    "money": ["£1000", "$500", "£900", "£2000", "250,000", "$1,000,000", "£100"],
    "word": ["WIN", "CLAIM", "PRIZE", "YES", "CHAT", "FREE", "NOW", "STOP"],
    "short": ["80086", "87121", "69696", "88877", "83355", "61200"],
    "phone": ["09061701461", "0800900900", "08000930705", "09058094597"],
    "url": ["http://bit.ly/abc9", "http://secure-login.example.co", "http://parcel-fee.example",
            "http://pp-verify.example", "http://watch-deal.example", "http://tinyurl.example/x1"],
    "pct": ["90%", "75%", "80%", "70%"],
    "meal": ["dinner", "lunch", "breakfast", "tea"],
    "item": ["milk", "bread", "the package", "the parcel", "coffee", "the charger"],
    "time": ["3pm", "7pm", "9.30", "half six", "midday", "8am"],
    "room": ["204", "1A", "the annexe", "the small one upstairs"],
    "mins": ["5", "10", "15", "20"],
    "reason": ["traffic on the bridge", "the train is delayed", "parking is a nightmare",
               "the bus never came"],
    "thing": ["slides", "report", "invoice", "notes", "PR", "budget"],
    "event": ["film", "match", "gig", "appointment", "class", "talk"],
    "place": ["gym", "pub", "office", "station", "cafe"],
}

TYPO_MAP = {"you": "u", "are": "r", "to": "2", "for": "4", "your": "ur",
            "please": "pls", "tomorrow": "tmrw", "and": "&"}


def fill(template: str, rng: np.random.Generator) -> str:
    out = template
    for slot, options in SLOTS.items():
        token = "{" + slot + "}"
        while token in out:
            out = out.replace(token, str(rng.choice(options)), 1)
    return out


def roughen(text: str, rng: np.random.Generator) -> str:
    """Apply the kind of noise real SMS has: txt-speak, caps, trailing junk."""
    words = text.split()
    if rng.random() < 0.35:
        words = [TYPO_MAP.get(w.lower(), w) for w in words]
    text = " ".join(words)
    if rng.random() < 0.12:
        text = text.upper()
    if rng.random() < 0.15:
        text = text + rng.choice(["", " x", " :)", "!!", "...", " thanks"])
    return text.strip()


def build(n: int, spam_rate: float, seed: int) -> list[tuple[str, str]]:
    rng = np.random.default_rng(seed)
    n_spam = int(round(n * spam_rate))
    n_ham = n - n_spam

    rows: list[tuple[str, str]] = []
    for _ in range(n_spam):
        pool = HARD_SPAM_TEMPLATES if rng.random() < 0.18 else SPAM_TEMPLATES
        rows.append(("spam", roughen(fill(str(rng.choice(pool)), rng), rng)))
    for _ in range(n_ham):
        pool = HARD_HAM_TEMPLATES if rng.random() < 0.12 else HAM_TEMPLATES
        rows.append(("ham", roughen(fill(str(rng.choice(pool)), rng), rng)))

    order = rng.permutation(len(rows))
    return [rows[i] for i in order]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=Path("sms-spam-synthetic.csv"))
    parser.add_argument("--n", type=int, default=1200)
    parser.add_argument("--spam-rate", type=float, default=0.134)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = build(args.n, args.spam_rate, args.seed)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label", "text"])
        writer.writerows(rows)

    n_spam = sum(1 for label, _ in rows if label == "spam")
    print(f"wrote {args.out} - {len(rows)} rows, {n_spam} spam "
          f"({n_spam / len(rows):.1%}), {len(rows) - n_spam} ham")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
