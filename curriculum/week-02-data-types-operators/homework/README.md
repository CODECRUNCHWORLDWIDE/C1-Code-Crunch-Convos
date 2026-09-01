# Week 2 Homework

Six problems that take you from "I can print a number" to "I can print a
number where I want it, in the format I want, having checked it was a number
in the first place". The whole set takes about **6 hours**. Unlike Week 1's
homework these are independent — each one is its own small program — so you
can work them in any order. Working them in the order given is still easier,
because the later ones lean on the formatting you learned in the earlier
ones.

## How to Work a Problem

Each problem below is a page, not a program. The page gives you the brief, a
starter to copy, the exact output to expect, the full worked answer, and the
mistakes that catch people on that particular task. You do the typing.

1. Open a terminal and activate your Week 2 virtual environment.
2. Read the whole page before you type anything, including **Common bugs to
   catch**. The Constraints section is short and it is where the traps are
   named.
3. Create the file in your own `homework/` folder, using the name the page
   gives you — `homework-01-simple-interest.py`, `homework-02-bmi.py`, and
   so on — and copy the **Starter** into it. Every starter runs as pasted
   and does part of the job.
4. Fill in the `TODO` markers. Leave the docstrings, type hints and
   constants in place; they are part of the spec, not decoration.
5. Run it and compare against **Expected output**, character for character.
   Columns and spacing count this week more than any other.
6. Compare your answer against **The Solution**, then tick every box in the
   acceptance checklist honestly.
7. If you installed `mypy`, run it on your finished file and aim for
   `Success: no issues found`.
8. Commit. Every problem should leave at least one commit behind in your
   Week 2 repository.

All six problems end in a real script, and each ships the finished `.py`
beside its page under **Download and run**. Those files ask their questions
when you run them from a terminal and fall back to a built-in example when
nobody is at the keyboard, so they can be run and checked automatically. The
file you hand in is your own copy, under the name the page gives you.

## Index

| # | Problem | What you'll practice | Difficulty | Est. time |
|---|---------|----------------------|-----------:|----------:|
| 1 | [problem-01-simple-interest-calculator.md](./problem-01-simple-interest-calculator.md) | Format specs, field widths, thousands separators, casting input | Beginner | 1 h |
| 2 | [problem-02-bmi-calculator.md](./problem-02-bmi-calculator.md) | Comparison operators, chained comparisons, booleans as values | Beginner | 45 min |
| 3 | [problem-03-word-and-character-counter.md](./problem-03-word-and-character-counter.md) | `len()`, `.replace()`, `.split()`, `.upper()`, immutable strings | Beginner | 45 min |
| 4 | [problem-04-grade-letter-assigner-no-if.md](./problem-04-grade-letter-assigner-no-if.md) | `bool` as `int`, summing comparisons, string indexing, precedence | Intermediate | 1 h |
| 5 | [problem-05-compound-interest.md](./problem-05-compound-interest.md) | `**`, precedence, load-bearing parentheses, float rounding | Beginner | 45 min |
| 6 | [problem-06-distance-and-speed-report.md](./problem-06-distance-and-speed-report.md) | Named constants, unit conversion, a guard clause, two-width reports | Intermediate | 1 h 45 min |

**Total: about 6 hours.**

Problems 2 and 4 forbid `if`, which is a Week 3 topic. That is deliberate:
doing without it is what makes you notice that a comparison is already a
value. Problem 6 then hands `if` back for one guard clause, because
refusing bad input is a decision that genuinely cannot be a calculation.

Problem 6 is also the warm-up for Friday's
[mini-project](../mini-project/README.md): the named conversion constant,
the guard clause and the aligned report all reappear there without changes.

## Checking Your Work

There is no automated grader. For each problem, satisfy yourself that:

- The program ran without an error you had to ignore.
- Your output matches the page's **Expected output** section character for
  character, columns included.
- Every box in the page's acceptance checklist is honestly ticked.
- `mypy` is clean, if you have it installed.
- The work is committed and pushed.

When all six are done, finish
[the Week 2 mini-project](../mini-project/README.md) and take
[the quiz](../quiz.md).
