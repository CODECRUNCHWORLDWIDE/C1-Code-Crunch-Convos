# Week 4 — Exercises

Five short exercises. Do them in order. Each one is a page: a brief, a
starter you copy into your own `.py` file, and self-tests you run.

## How to work through these

1. Open the exercise page and read it top to bottom before you type anything.
   The Requirements and Constraints sections are the spec.
2. Create the matching `.py` file in your practice repo — the page names it
   for you, for example `exercise-01-function-basics.py`.
3. Copy the starter block into that file and replace each `# TODO:` with your
   own code.
4. Run the file: `python exercise-01-function-basics.py`.
5. If the self-checks pass, the script prints `All checks passed.` Move on.

Every starter ends with an `if __name__ == "__main__":` block full of
`assert` statements. That block is the grader. When one fails, Python names
the assertion and prints the value it actually got — read the error
carefully, because that is half the skill.

Exercise 4 is different: its starter is broken on purpose and your job is to
fix it. Paste it exactly as written.

## Index

| # | Exercise | Topic | Difficulty | Target solve time |
|---|----------|-------|------------|------------------|
| 1 | [Function basics](./exercise-01-function-basics.md) | `def`, parameters, defaults, type hints, docstrings | Beginner | 45 min |
| 2 | [`*args` and `**kwargs`](./exercise-02-args-kwargs.md) | Variable arguments, unpacking | Easy | 45 min |
| 3 | [Recursion intro](./exercise-03-recursion-intro.md) | Iterative vs. recursive factorial | Medium | 60 min |
| 4 | [Scope mystery](./exercise-04-scope-mystery.md) | Fix bugs caused by scope confusion | Medium | 45 min |
| 5 | [Import and use](./exercise-05-import-and-use.md) | Standard library: `math`, `random`, `statistics` | Easy | 45 min |

Total target solve time: about 4 hours.

The [week schedule](../README.md) budgets a longer block per exercise — 1.5 to
2 hours rather than 45 to 60 minutes. Both figures are real and they measure
different things. The number in this table is how long the exercise takes when
it goes well. The schedule's block is the whole sitting: getting stuck,
re-reading the lecture, working the stretch section, and committing. If you land
near the target here, you are on pace; if you need the full block, so does
almost everyone.

## Tips

- If you get stuck for more than 15 minutes, re-read the relevant lecture note
  section, then ask for help in `#week-04` on Discord.
- Use the Python REPL (`python` with no arguments) as a sandbox while you
  think. `python -i your_file.py` runs the file and then drops you into the
  REPL with everything already defined — the fastest way to poke at a
  function you just wrote.
- Type hints are required on every function you write this week, even when
  the spec does not say so explicitly.
- Every public function needs a one-line docstring per
  [PEP 257](https://peps.python.org/pep-0257/).
- Commit each exercise as you finish it. A commit per exercise gives you a
  point to go back to when the next one breaks something.

When all five exercises pass, move on to the
[challenges](../challenges/README.md).
