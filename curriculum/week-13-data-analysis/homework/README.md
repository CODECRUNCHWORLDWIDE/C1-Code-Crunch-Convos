# Week 13 — Homework

Six problems, one page each. Every one of them is a task you will meet again
with a real deadline attached: convert a file somebody sent you, audit what is
missing from it, join it to a second table, pivot it into a shape a person can
read, chart it, and then say — carefully — what it does and does not show.

Each shipped answer runs **offline and unattended**. None of them opens a chart
window, waits for input, or calls a server. The plotting problems draw to a file
and print the name of the file they wrote, so `python <name>.py` finishes on its
own and prints the same thing on any machine.

## Setup

Work in the same virtual environment you used for the exercises:

```bash
pip install numpy pandas matplotlib openpyxl
```

`openpyxl` is what lets pandas read and write Excel files; Problem 1 mentions
them. Problem 6 also uses seaborn for its dataset — its page says so and gives
the install line.

## How to work a problem

1. Read The Brief and the Requirements. Before you write anything, say out loud
   what the table looks like going in and what it should look like coming out.
   Most of this week's bugs are answered by naming the shape first.
2. Copy the Starter into a file of your own — the page names it, and it is
   **not** the `-solution.py` file, which is the finished answer.
3. Fill in the `TODO` markers one at a time, running after each.
4. Compare your output with the Expected output block.
5. Only then read The Solution and Why it works.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [CSV to JSON converter](./problem-01-csv-to-json.md) | Reading a file you were handed and writing it back out in another shape | Beginner | 45 min |
| 2 | [Missing-data report](./problem-02-missing-data-report.md) | Finding the holes before they become wrong answers | Intermediate | 45 min |
| 3 | [Merge two DataFrames](./problem-03-merge-dataframes.md) | Joining on a key, and noticing the rows a join quietly drops | Intermediate | 1 hr |
| 4 | [Pivot table from raw rows](./problem-04-pivot-table.md) | Turning a long log into a table somebody can actually read | Intermediate | 45 min |
| 5 | [Multi-line chart](./problem-05-multi-line-chart.md) | One chart, several series, and a legend that explains itself | Intermediate | 45 min |
| 6 | [Find correlations](./problem-06-correlations.md) | Measuring how two columns move together — and what that does not prove | Advanced | 1 hr |

Total target time: about 5 hours. The [week schedule](../README.md) leaves more
room than that, and both numbers are honest — the figures here are how long a
problem takes when it goes well, and the schedule allows for getting stuck and
reading back over the lecture notes.

**Problem 6 carries the sentence that matters most in this whole week.** A
correlation says two columns move together. It does not say one causes the
other. Bigger bills come with bigger tips, and that is a real, measurable
relationship — but the number alone cannot tell you whether the bill drives the
tip, whether party size drives both, or whether something you never measured
drives all three. Read that part of the page slowly. It is the difference
between analysis and a confident mistake.

## What you hand in

Six programs of your own, one per problem, named as each page tells you — not
the `-solution.py` names, which belong to the published answers. Keep them
together in a folder called `homework/` inside your fork.

House rules, the same on every problem:

- **A docstring at the top of every file** stating which problem it answers and
  showing an example invocation.
- **Type hints on every signature** (`def load(path: str) -> pd.DataFrame:`).
- **No hard-coded paths** outside your own homework folder. Take the path as an
  argument.
- **Every chart has a title and labelled axes.** A chart nobody can read is a
  chart that says nothing.
- **It runs end-to-end** with `python <name>.py`, from a clean shell, with no
  edits.

## Checking your work

Every page ends with an acceptance checklist. Work down it before calling a
problem done. If your output differs from the page's Expected output, that
difference is the bug — read it rather than guessing. When a DataFrame surprises
you, print `df.shape`, `df.dtypes` and `df.head()` before you print anything
else; nearly every pandas confusion is one of those three not being what you
assumed.
