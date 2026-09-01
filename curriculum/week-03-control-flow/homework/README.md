# Week 3 — Homework

Six practice problems that take you from "I can write an `if`" to "I can
keep a loop running safely while somebody types things at it". Each one
is a page: the brief, a starter you copy into your own `.py` file, the
exact output to aim for, the full worked answer, and the mistakes that
catch people on that particular task. You do the typing.

The problems are independent — each is its own small program — so you can
work them in any order. Working them in the order given is easier,
because 3 and 4 are the same loop with one operator changed, and 6 leans
on every guard clause you wrote in 1 through 5.

## How to Work a Problem

1. Open a terminal and activate your Week 3 environment.
2. Read the whole page before you type anything, including **Common bugs
   to catch**. The Constraints section is short and it is where the traps
   are named.
3. Create the file in your own `homework/` folder, using the name the
   page gives you — `homework-01-leap-year.py`,
   `homework-02-count-vowels.py`, and so on — and copy the **Starter**
   into it. Every starter runs as pasted and does part of the job.
4. Fill in the `TODO` markers. Leave the docstring and the constants in
   place; they are part of the spec, not decoration.
5. Run it and compare against **Expected output**, character for
   character.
6. Compare your answer against **The Solution**, then tick every box in
   the acceptance checklist honestly.
7. Commit. Every problem should leave at least one commit behind in your
   Week 3 repository.

## The Problems

| # | Problem | What you will practise | Difficulty | Est. time |
|---|---------|------------------------|-----------:|----------:|
| 1 | [problem-01-leap-year-checker.md](./problem-01-leap-year-checker.md) | Ordered `if`/`elif`/`else`, `%`, validating before converting | Beginner | 45 min |
| 2 | [problem-02-count-vowels-in-a-string.md](./problem-02-count-vowels-in-a-string.md) | The counting pattern, iterating a string, `in` as membership | Beginner | 30 min |
| 3 | [problem-03-reverse-a-number.md](./problem-03-reverse-a-number.md) | `while` + accumulator, `% 10` and `// 10`, a free empty case | Beginner | 45 min |
| 4 | [problem-04-sum-of-digits.md](./problem-04-sum-of-digits.md) | The same traversal, a different accumulator | Beginner | 30 min |
| 5 | [problem-05-fibonacci-numbers-up-to-n.md](./problem-05-fibonacci-numbers-up-to-n.md) | A loop of unknown length, tuple assignment, boundaries | Beginner | 30 min |
| 6 | [problem-06-simple-atm-menu.md](./problem-06-simple-atm-menu.md) | `while True`, `break` vs `continue`, guard clauses, refusing safely | Intermediate | 1 h 30 min |

**About four and a half hours of focused work.** The week's schedule
allows six; the difference is the extensions under each page's
**Stretch**, which are where most of the fun is.

## Two rules that shape all six

- **No functions.** `def` is Week 4. Everything sits at the top level of
  your file, in the order it runs. Where a function would obviously help,
  the page says so and shows what Week 4 will let you write instead.
- **No `try` / `except`.** Exceptions are Week 6. Input is validated
  *before* it is converted, using string membership and guard clauses —
  the tools [Lecture 1](../lecture-notes/01-conditionals.md) and
  [Lecture 2](../lecture-notes/02-loops.md) actually gave you.

You will notice the same six-line validation block at the top of most of
these answers. That repetition is deliberate and it is the point: by
problem 4 it should be annoying you, and that annoyance is exactly the
feeling Week 4 exists to fix.

## About the downloadable answers

All six problems end in a real script, and each ships the finished `.py`
beside its page under **Download and run** as
`problem-NN-<name>-solution.py`. Those files ask their questions when you
run them from a terminal and fall back to a built-in example when nobody
is at the keyboard, so they can be run and checked automatically.

Each of them contains exactly one `def` — a small helper called `ask` —
and it is **not part of the answer**. It is there so the download can run
without a keyboard, and each page says so where it appears. The file you
hand in is your own copy, under the name the page gives you, with a plain
`input(...)` in place of `ask(...)`.

The other thing `ask` does is worth stealing even before you learn `def`:
it sends the *question* to the error stream and the *answer* to the
normal output stream. That is why
`python homework-05-fibonacci.py > fib.txt` saves ten clean numbers
instead of ten numbers with a prompt stuck to the front of them.

## Checking Your Work

There is no automated grader. For each problem, satisfy yourself that:

- The program ran without an error you had to ignore.
- Your output matches the page's **Expected output** section character
  for character.
- Every box in the page's acceptance checklist is honestly ticked.
- The work is committed and pushed.

## How to submit

If you are tracking your work in Git — highly recommended, see Week 1 —
commit each problem as you finish it:

```bash
git add homework/homework-01-leap-year.py
git commit -m "Week 3 homework: leap year checker"
```

Each homework file should start with a short docstring saying what it
does, just like the exercise starters. Good docstrings now become muscle
memory for Week 4.

When all six are done, finish
[the Week 3 mini-project](../mini-project/README.md) and take
[the quiz](../quiz.md).
