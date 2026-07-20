# Week 13 — Exercises

Five short exercises that walk you through the muscle-memory moves of pandas
and matplotlib. Each one should take 10–30 minutes. Do them in order — they
build on each other.

## Setup

From the week-13 directory, create a virtual environment and install the
dependencies:

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .\.venv\Scripts\Activate.ps1     # Windows PowerShell

pip install numpy pandas matplotlib jupyter seaborn
```

## How to Run

- `.py` files: `python exercise-01-numpy-arrays.py`
- `.ipynb` files: `jupyter notebook` (or open it in VS Code) and run the
  cells top to bottom.

## Index

| # | File | What you'll practice |
|---|------|----------------------|
| 1 | [exercise-01-numpy-arrays.py](./exercise-01-numpy-arrays.py) | Creating arrays, vector math, broadcasting |
| 2 | [exercise-02-load-and-inspect.ipynb](./exercise-02-load-and-inspect.ipynb) | Loading a dataset in a notebook and inspecting it |
| 3 | [exercise-03-filter-and-sort.py](./exercise-03-filter-and-sort.py) | Filtering rows and sorting by a column |
| 4 | [exercise-04-groupby.py](./exercise-04-groupby.py) | `groupby` totals and averages |
| 5 | [exercise-05-plot.py](./exercise-05-plot.py) | Bar chart with matplotlib, save to PNG |

## Tips

- Read the docstring at the top of every file — it states the task and the
  expected output.
- Run the file once to see the starter output, then edit between the
  `# YOUR CODE HERE` markers.
- Compare your output against the `# Expected:` comments where present.
- If a numpy or pandas method is unfamiliar, look it up — that is part of
  the exercise.

## When You're Stuck

1. Read the error message all the way to the bottom. The actual problem is
   usually on the last line.
2. Print the shape and dtypes of any DataFrame you don't understand.
3. Check the pandas docs: <https://pandas.pydata.org/docs/>.
4. Ask in the Code Crunch Convos community channel.
