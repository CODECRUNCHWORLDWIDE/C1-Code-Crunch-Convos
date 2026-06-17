# Mini-project — SMS Spam Classifier

Build a complete, runnable spam classifier from raw text to a CLI that scores new messages. This is the capstone of Week 14 and the most realistic ML workflow we have done so far: text preprocessing, multiple algorithms, honest evaluation, model persistence, deployment as a CLI.

## What you will deliver

By the end of the project you should have:

1. `train.py` — trains and saves the best model.
2. `predict.py` — a command-line tool that loads the saved model and classifies a single message.
3. `model.joblib` — the saved pipeline (vectoriser + classifier in one file).
4. `report.md` — a short writeup of your results.

A working starter is in `starter.py`. Use it. Fill in the TODOs.

## Dataset

A small synthetic spam/ham CSV ships with this project: `sample-data.csv` (about 30 rows). It is enough to run the pipeline end-to-end without an internet connection.

For a more realistic experiment after you finish the basic version, download the **UCI SMS Spam Collection** dataset:
<https://archive.ics.uci.edu/dataset/228/sms+spam+collection>

It has 5,574 real SMS messages, professionally labelled. Drop it into the project as `sms-spam.csv` and re-run `train.py`. Your numbers will become much more meaningful.

## CSV format

Two columns:

```text
label,text
ham,"How are you doing today?"
spam,"WIN a FREE iPhone! Click http://bit.ly/abc now!"
```

`label` is `spam` or `ham`. `text` is the message. Everything else is up to you.

## Requirements (the spec)

You must:

1. **Preprocess text with `TfidfVectorizer`.** Set `lowercase=True` (the default) and `stop_words="english"`. Bigrams (`ngram_range=(1, 2)`) often help — try both with and without.
2. **Compare at least three classifiers:**
   - `LogisticRegression`
   - `MultinomialNB` (Naive Bayes — historically strong for text)
   - `DecisionTreeClassifier` *or* `RandomForestClassifier`
3. **Evaluate each model with precision, recall, F1, and a confusion matrix** on a stratified test split. Report all four numbers, not just accuracy.
4. **Pick the best model.** Justify your choice in `report.md`. "Highest F1 on the minority class" is a reasonable default — but if your stakeholder cares more about *not missing spam*, recall might dominate. State your criterion explicitly.
5. **Save the chosen pipeline with `joblib.dump`.** The saved file must include the vectoriser and the classifier — i.e., one `Pipeline`, one `joblib` file.
6. **Build a CLI** (`predict.py`) that:
   - Loads `model.joblib`.
   - Reads a message from `sys.argv[1]` (or stdin).
   - Prints `spam` or `ham` and the predicted probability of spam.

## Rubric

Self-assess out of 12 points. 9+ is a passing project.

| Area | 2 pts | 1 pt | 0 pts |
|---------------------|----------------------------------------|-------------------------------------|-------------------------|
| Preprocessing | TF-IDF inside a Pipeline, no leakage | TF-IDF separate from model | Bag of bugs |
| Algorithm comparison| 3+ models, fair comparison | 2 models | 1 model |
| Metrics | Precision/recall/F1 + confusion matrix | Accuracy only | None |
| Model persistence | Pipeline saved + loadable | Model only saved | None |
| CLI inference | Works on raw text input | Crashes on edge cases | None |
| Writeup | Clear, honest, includes ethics note | Numbers only | None |

## Example usage

```bash
python train.py sample-data.csv
# trains, prints metrics, writes model.joblib

python predict.py "Congratulations! You won a free cruise. Click here."
# spam (probability 0.92)

python predict.py "Are you home for dinner?"
# ham  (probability 0.04)
```

## Ethics note (required in your report)

In your `report.md`, include a section titled **"Limitations and risks"** of at least 150 words covering:

- What does the model do badly? (Inspect the false positives and false negatives.)
- What kinds of harm could a deployed spam filter cause? (Hint: blocking a legitimate but unusual message — a job offer, a doctor's appointment, an emergency alert — has different costs to different users.)
- What is the right human-recourse mechanism? (How does a user appeal a misclassification?)
- Could the model amplify any pattern in the training data that you would not want deployed at scale?

This section is not optional and not lip service. It is part of what makes you employable as an ML-aware engineer rather than a spreadsheet jockey with a `model.fit()` habit.

## Time budget

- Reading the spec and `starter.py`: 15 min
- Training pipeline: 60–90 min
- CLI: 30 min
- Writeup: 30 min

Aim for 2–3 focused hours. Don't perfect; ship.

## Stretch goals

- Replace the synthetic CSV with the real UCI SMS dataset.
- Add a `--top-features` flag to `train.py` that prints the words most associated with spam (use `model.named_steps['clf'].coef_`).
- Wrap `predict.py` in a tiny Flask endpoint (you learned Flask in Week 9). Now you have a real ML web service.
- Add a `tests/` folder with pytest tests for `train.py` and `predict.py`. You learned testing in Week 11.
- Track each training run's metrics in a CSV log so you can see your progress over iterations.
