# Week 14 — Exercises

Five short, runnable scripts. Each one targets a specific concept from the lectures. Work through them in order; later ones reuse ideas from earlier ones.

## Setup

```bash
pip install scikit-learn pandas numpy matplotlib
```

Run any exercise with:

```bash
python exercises/exercise-01-linear-regression.py
```

Each script is fully self-contained — no external data required.

## The list

| # | File | Concept | Time |
|---|--------------------------------------|---------------------------------------|------|
| 1 | `exercise-01-linear-regression.py` | First model: predict price from sqft | 20m |
| 2 | `exercise-02-iris-classifier.py` | Logistic regression on iris | 20m |
| 3 | `exercise-03-train-test-split.py` | Why `random_state` matters | 25m |
| 4 | `exercise-04-pipeline.py` | StandardScaler + LogisticRegression | 25m |
| 5 | `exercise-05-confusion-matrix.py` | Reading the confusion matrix | 30m |

Total: about two hours of code + thinking. Slower if you experiment (and you should).

## How to work through these

1. **Read the script before running it.** Do not just execute. Predict the output.
2. **Run it.** Compare your prediction with reality.
3. **Break things.** Change `random_state`. Drop features. Use a different model. Notice what happens.
4. **Write down one observation per exercise.** Even if it's just "wow, accuracy jumped when I scaled".

The exercises don't have automated tests. The point is muscle memory for the sklearn API, not a leaderboard.

## Stuck?

- `ValueError: Expected 2D array` — you passed a Series where a DataFrame is needed. Use `df[["col"]]` not `df["col"]`.
- `ConvergenceWarning` — add `max_iter=1000` to your model.
- Imports failing — make sure your venv has `scikit-learn`, `pandas`, and `numpy` installed.

Up next: `challenges/` for harder problems on real datasets.
