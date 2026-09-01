# Week 13 — Exercises

Five short exercises that walk you through the muscle-memory moves of pandas
and matplotlib. Each one should take 10–30 minutes. Do them in order — they
build on each other.

Every exercise is a page. Each page gives you the brief, a starter you copy
into your own `.py` file, the exact output your finished version should
produce, and a list of the errors you are most likely to hit along the way.
None of them download anything: each exercise builds its own small DataFrame
from a dictionary of lists, so they all run offline.

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

1. Open the exercise page and read it through before you type anything.
2. Create the matching `.py` file in your own practice repo — same slug, `.py`
   instead of `.md`. For Exercise 1 that is
   `exercise-01-numpy-arrays.py`.
3. Paste the starter from the page and fill in the `# TODO:` markers.
4. Run it from your terminal:

   ```bash
   python exercise-01-numpy-arrays.py
   ```

5. Compare what you got against the page's **Expected output** block, line by
   line, then work through the **Acceptance checklist**.

Exercise 2 is laid out as numbered notebook cells. You can paste those cells
into `exercise-02-load-and-inspect.ipynb` and run them top to bottom with
`jupyter notebook` (or in VS Code), or paste the same code into a `.py` file
and run it as a script. Every cell prints its result, so the output is the
same either way.

## Index

| # | Exercise | What you'll practice | Difficulty | Est. time |
|---|----------|----------------------|-----------:|----------:|
| 1 | [exercise-01-numpy-arrays.md](./exercise-01-numpy-arrays.md) | Creating arrays, vector math, broadcasting | Beginner | 20 min |
| 2 | [exercise-02-load-and-inspect.md](./exercise-02-load-and-inspect.md) | Building a DataFrame and inspecting it, as a notebook or a script | Beginner | 20 min |
| 3 | [exercise-03-filter-and-sort.md](./exercise-03-filter-and-sort.md) | Filtering rows and sorting by a column | Easy | 25 min |
| 4 | [exercise-04-groupby.md](./exercise-04-groupby.md) | `groupby` totals and averages | Medium | 25 min |
| 5 | [exercise-05-plot.md](./exercise-05-plot.md) | Bar chart with matplotlib, save to PNG | Medium | 30 min |

## Tips

- Read the whole page before you write code. The **Constraints** section
  explains *why* each rule is there, and those reasons are the part worth
  keeping.
- Fill in one `# TODO:` at a time and run the file after each one. Two correct
  lines beat six guesses.
- Compare your terminal output against the page's Expected output block
  character for character. If a number differs, the page is right and your
  code is wrong — every expected value in these pages was run before it was
  written down.
- When a numpy or pandas method is unfamiliar, look it up before you copy the
  starter. Reading the docs is part of the exercise, not a detour from it.

## When You're Stuck

1. Read the error message all the way to the bottom. The actual problem is
   usually on the last line.
2. Check the page's **Common bugs to catch** section — the exception you are
   staring at is probably listed there with its cause.
3. Print the shape and dtypes of any DataFrame you don't understand.
4. Check the pandas docs: <https://pandas.pydata.org/docs/>.
5. Ask in the Code Crunch Convos community channel.
