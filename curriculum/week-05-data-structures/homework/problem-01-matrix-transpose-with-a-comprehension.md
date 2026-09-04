# Homework Problem 1 — Matrix transpose (with a comprehension)

> **Topic:** nested list comprehensions, and reading one from the outside in
> **Lecture:** [03 — Comprehensions and Big-O](../lecture-notes/03-comprehensions-and-big-o.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** it is the only problem this week about the *shape* of your data rather than about looking something up, and it is where you find out whether you can actually read a comprehension that has two `for` clauses in it. Almost everybody writes this one backwards the first time, and almost everybody only finds out because somebody made them test a matrix that was not square.

## The Brief

A **matrix** is a grid of numbers. In Python you write one as a list of rows,
and each row is itself a list:

```python
[[1, 2, 3],
 [4, 5, 6]]
```

That grid is 2 rows tall and 3 columns wide. Its **transpose** is the same
numbers with the rows and the columns swapped over — 3 rows tall and 2 columns
wide:

```python
[[1, 4],
 [2, 5],
 [3, 6]]
```

Tip the grid onto its side and that is what you get. The number that was in row
0, column 2 is now in row 2, column 0. Nothing is added and nothing is lost;
every number keeps its two coordinates and they trade places.

Write one function.

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    ...
```

```python
transpose([[1, 2, 3], [4, 5, 6]])
# [[1, 4], [2, 5], [3, 6]]

transpose([[1]])
# [[1]]
```

The rows you are given are all the same length. A grid with rows of different
lengths is not a matrix, and this function is not asked to cope with one.

One rule sits over the whole problem: **build it with a list comprehension.**
Nested is fine — in fact nested is the answer. You could write it with two
`for` loops and an accumulator, and you would get the right answer, and you
would learn none of the thing this problem exists to teach.

## Starter

Save this in your `homework/` folder as part of `week-05-solutions.py` and fill
in the `TODO`. It runs as pasted — it just gives back an empty grid:

```python
"""Week 5 homework, problem 1: turn a matrix's rows into its columns."""


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return the transpose of a rectangular matrix, as a list comprehension.

    Args:
        matrix: A list of rows. Every row must be the same length.

    Returns:
        A new list of columns.

    Example:
        >>> transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    # TODO 1: give back [] when the matrix has no rows at all.
    # TODO 2: one nested comprehension. The outer clause walks the column
    #         numbers, `range(len(matrix[0]))`. The inner one walks the rows.
    return []


def _demo() -> None:
    """Print the brief's examples."""
    print(transpose([[1, 2, 3], [4, 5, 6]]))
    print(transpose([[1]]))


if __name__ == "__main__":
    _demo()
```

The `Example:` line in that docstring is a real test — see *Stretch*.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-05-data-structures/homework/problem-01-matrix-transpose-with-a-comprehension.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `transpose(matrix)` returns a new list of lists, with the rows and columns
   swapped.
2. An `r` by `c` matrix comes back as `c` lists of `r` numbers each.
3. `transpose([[1]])` returns `[[1]]`.
4. `transpose([])` returns `[]` and does not raise.
5. The input matrix is not changed.
6. Type hints on the signature and a docstring on the function.
7. These three asserts pass:

   ```python
   assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
   assert transpose([[1]]) == [[1]]
   assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
   ```

## Constraints

- **Build the answer with a list comprehension.** Nested is expected. A
  comprehension makes a brand-new inner list on every turn of the outer loop,
  which quietly avoids the aliasing trap in *Common bugs to catch* — that is
  part of why the brief insists on one.
- **Guard the empty matrix before you measure it.** `len(matrix[0])` on `[]`
  raises `IndexError`, so the guard has to come first. The transpose of a grid
  with no rows really is `[]`, so this is the right answer and not a dodge.
- **Test with a matrix that is not square.** A 2-by-2 matrix hides the single
  most common bug in this problem, because the buggy version gives the right
  answer on it. Use 2-by-3.
- **Do not sort, and do not reverse.** Every number keeps its place; only the
  two coordinates trade names.
- **`_demo` prints; `transpose` does not.** The function returns a grid and
  says nothing.

## Expected output

```text
$ python problem-01-matrix-transpose-with-a-comprehension.py
[[1, 4], [2, 5], [3, 6]]
[[1]]
[[1, 3, 5], [2, 4, 6]]
[]
All 5 asserts passed.
```

The first three lines are the brief's own examples and the required asserts. The
fourth is the empty matrix, which is the case the brief's hint cannot handle on
its own.

There is a second check worth running, and it is stronger than any of the
examples:

```bash
python -c "from week_05_solutions import transpose as t; m=[[1,2,3],[4,5,6]]; print(t(t(m)) == m)"
```

```text
True
```

Transposing twice gets you back where you started. That has to hold for *every*
rectangular matrix, not just the ones somebody thought to write down, which is
why it catches bugs the examples miss.

## Steps

1. Save the Starter into `week-05-solutions.py` and run it. Two empty lists.
2. Before you write anything, print the two numbers you are about to use:

   ```python
   matrix = [[1, 2, 3], [4, 5, 6]]
   print(len(matrix), len(matrix[0]))
   ```

   ```text
   2 3
   ```

   Two rows, three columns. Say out loud which of those two the answer needs
   as its *number of rows*. It is the 3.
3. Write the inner comprehension on its own first, for one fixed column:

   ```python
   i = 0
   print([row[i] for row in matrix])
   ```

   ```text
   [1, 4]
   ```

   That is one column of the input and one row of the answer.
4. Wrap it in the outer clause that walks `i` over
   `range(len(matrix[0]))`. That is the whole function.
5. Run it. The first line should be `[[1, 4], [2, 5], [3, 6]]`.
6. Add the empty guard, then run `transpose([])`. No traceback.
7. Add the three required asserts, plus `assert transpose([]) == []` and the
   round-trip assert from *Expected output*.
8. Compare with **The Solution**, tick the acceptance checklist, and commit:
   `git add homework/week-05-solutions.py` then
   `git commit -m "Week 5 homework: matrix transpose"`.

## The Solution

```python
"""Flip a matrix's rows and columns with one nested list comprehension.

Week 5 homework, problem 1, Code Crunch Convos.

Add ``transpose`` to your own ``week-05-solutions.py``. This file is the
published answer, and the longer name keeps it from landing on top of your work.

Read the comprehension from the outside in. The outer clause walks the column
numbers; the inner one walks the rows and picks out the number sitting in that
column. Each finished inner list is one column of the input, which is what a
transpose is.
"""


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return the transpose of a rectangular matrix, as a list comprehension.

    Args:
        matrix: A list of rows. Every row must be the same length.

    Returns:
        A new list of columns. An ``r`` by ``c`` matrix gives back ``c`` lists
        of ``r`` numbers each. An empty matrix gives back an empty list.

    Example:
        >>> transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    if not matrix:
        return []
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def _check() -> None:
    """Run the three asserts the brief requires, plus two it implies."""
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1]]) == [[1]]
    assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
    assert transpose([]) == []
    assert transpose(transpose([[1, 2, 3], [4, 5, 6]])) == [[1, 2, 3], [4, 5, 6]]


def _demo() -> None:
    """Print the brief's three examples, then the empty matrix."""
    print(transpose([[1, 2, 3], [4, 5, 6]]))
    print(transpose([[1]]))
    print(transpose([[1, 2], [3, 4], [5, 6]]))
    print(transpose([]))
    print("All 5 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
```

**Why it works.**

**Read the nested comprehension from the outside in, not from left to right.**
That is the single reading habit this problem is teaching. The outer clause is
the one at the end:

```python
[[row[i] for row in matrix] for i in range(len(matrix[0]))]
#                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ outer: walks columns
# ^^^^^^^^^^^^^^^^^^^^^^^^^ inner: walks rows, plucks one column
```

`matrix[0]` is the first row, so `len(matrix[0])` is the number of **columns**.
`i` therefore walks the column numbers. For each `i`, the inner comprehension
walks every row and takes the number in column `i`. One column of the input
becomes one row of the answer, which is exactly what a transpose is.

Traced out for the brief's example:

```text
matrix = [[1, 2, 3],        i = 0  ->  [row[0] for row in matrix] = [1, 4]
          [4, 5, 6]]        i = 1  ->  [row[1] for row in matrix] = [2, 5]
                            i = 2  ->  [row[2] for row in matrix] = [3, 6]
```

The shape flips as a consequence rather than as a step: three columns in, three
lists out, each holding the two numbers that used to be stacked above each
other.

**Notice that the two dimensions swap roles in the code as well.**
`range(len(matrix[0]))` — the columns — drives the *outer* loop, and `matrix` —
the rows — drives the *inner* one. When a transpose comes out wrong, this is
almost always what is backwards.

**The `if not matrix: return []` guard is the correct answer, not a patch.**
`len(matrix[0])` reaches for the first row, and an empty matrix has not got one.
The transpose of a grid with zero rows genuinely is a grid with zero columns, so
`[]` is right. There is another way to write the whole function that handles
this for free —
`list(map(list, zip(*matrix)))` — but the brief asks for a comprehension, so the
guard is the honest way to satisfy both.

**The round-trip assert is a different kind of test.**

```python
assert transpose(transpose([[1, 2, 3], [4, 5, 6]])) == [[1, 2, 3], [4, 5, 6]]
```

The other four asserts check hand-picked examples. This one checks a **property**
— something that has to be true for every rectangular matrix there is. Properties
catch whole families of bugs at once, including the swapped-index bug below,
which survives happily on square matrices and dies instantly here.

## Run it

Copy the worked answer on this page into `problem-01-matrix-transpose-with-a-comprehension.py` and run it:
and run it:

```bash
python problem-01-matrix-transpose-with-a-comprehension.py
```

Your own copy of `transpose` belongs in `week-05-solutions.py`, and that is the
file you commit. The longer download name keeps the published answer from
landing on top of your work.

## Common bugs to catch

- **Swapping the two index roles.** The bug this problem exists to catch:

  ```python
  [[matrix[i][j] for i in range(len(matrix[0]))] for j in range(len(matrix))]
  ```

  ```text
  Traceback (most recent call last):
    File "week-05-solutions.py", line 2, in <module>
      bad = [[matrix[i][j] for i in range(len(matrix[0]))] for j in range(len(matrix))]
              ~~~~~~^^^
  IndexError: list index out of range
  ```

  Read where the squiggle points: it is under `matrix[i]`, so `i` is being used
  as a **row** number — but `i` was built from `len(matrix[0])`, which counts
  columns. The two letters have swapped jobs. The cruel part is that on a square
  matrix this version returns the right answer and never says a word. Test with
  a 2-by-3.
- **Building the rows by repeating one list.**

  ```python
  rows, cols = len(matrix), len(matrix[0])
  out = [[0] * rows] * cols          # every row is the SAME list
  for i in range(rows):
      for j in range(cols):
          out[j][i] = matrix[i][j]
  ```

  ```text
  [[3, 6], [3, 6], [3, 6]]
  ```

  No exception — just three identical rows, each showing only the last column
  that was written. `[x] * n` repeats the **reference**, so `out` is one list
  stored three times. This is the aliasing rule from
  [lecture 01](../lecture-notes/01-lists-and-tuples.md#aliasing--the-gotcha).
  `[[0] * rows for _ in range(cols)]` builds a fresh list each time and does not
  have the problem, which is one more reason the brief asks for a comprehension.
- **Measuring before guarding.**

  ```text
      return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
                                                            ~~~~~~^^^
  IndexError: list index out of range
  ```

  The squiggle is under `matrix[0]`, which tells you the failure is in working
  out the bounds, not in reading an element. Python 3.11 and later point at the
  exact sub-expression that failed; learning to read that mark saves you
  minutes every time.
- **Assuming ragged rows work.** `transpose([[1, 2, 3], [4, 5]])` raises
  `IndexError` when it reaches `row[2]`. The brief says "rows of equal length",
  so this is out of scope — but say so in a comment rather than letting a reader
  believe you handled it.
- **Returning tuples instead of lists.** `list(zip(*matrix))` gives
  `[(1, 4), (2, 5), (3, 6)]`, and `[(1, 4), ...] != [[1, 4], ...]`, so the
  assert fails on a result that looks right when printed. If you go the `zip`
  route you need the inner `list` call too.

## Under the hood

<details>
<summary>Under the hood — what the two for clauses of a nested comprehension really do</summary>

A comprehension with two `for` clauses is not two nested comprehensions. It is
one loop inside another, written in the same order you would write the loops —
and that order is the opposite of the order you *read* the expression, which is
why people get it wrong.

The mechanical translation is exact. This:

```python
[[row[i] for row in matrix] for i in range(len(matrix[0]))]
```

is this:

```python
out = []
for i in range(len(matrix[0])):        # the LAST clause is the OUTER loop
    column = []
    for row in matrix:                 # the earlier clause is the inner loop
        column.append(row[i])
    out.append(column)
```

Two rules fall out of that translation, and both matter here.

**Clauses run left to right, outermost first.** In
`[x for a in outer for x in a]`, `a` comes from `outer` and then `x` comes from
`a`. So a later clause can use a name a earlier one introduced, but not the
other way round. In our function the inner comprehension uses `i`, which the
outer clause created — that works. Swap them and `i` does not exist yet.

**The expression at the front runs last**, once per innermost turn. It sees
every name every clause has bound. That is why the thing you read first is the
thing that happens last, and why reading outside-in is the habit that makes
these legible.

Now the part that is genuinely different from ordinary loops. **A comprehension
gets its own scope.** The loop variable does not leak:

```python
squares = [n * n for n in range(3)]
print(n)
```

```text
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'n' is not defined
```

Write the same thing as a `for` loop and `n` is still sitting there afterwards,
holding `2`. Python 3 gave comprehensions their own scope precisely so that
writing one could not quietly overwrite a variable of yours that happened to
share a name. Python 2 did leak, and it caused exactly the bug you are
imagining.

One consequence worth knowing: an assignment inside the comprehension cannot
touch the enclosing function's names either, unless you use the walrus operator
`:=`, which is deliberately awkward to type.

</details>

<details>
<summary>Under the hood — zip(*matrix), the one-liner this problem is not asking for</summary>

There is a transpose that fits on half a line:

```python
>>> matrix = [[1, 2, 3], [4, 5, 6]]
>>> list(zip(*matrix))
[(1, 4), (2, 5), (3, 6)]
```

Two separate pieces of machinery are doing the work.

**The `*` at the call site unpacks.** `zip(*matrix)` means
`zip([1, 2, 3], [4, 5, 6])` — the rows are handed over as separate arguments,
not as one list of rows. The number of arguments is decided at run time by how
many rows there are.

**`zip` walks several sequences in step**, handing back one tuple per position:
the first item of each, then the second item of each, and so on. Take "one item
from each row, at the same position" and you have described a column. So
transposing is what `zip` does when you point it at rows.

It also stops at the shortest input, which is a real difference in behaviour:

```python
>>> list(zip(*[[1, 2, 3], [4, 5]]))
[(1, 4), (2, 5)]
```

The comprehension version raises `IndexError` on that ragged input. `zip`
silently drops the 3. Neither is more correct — the brief says the rows are the
same length, so both are answering a question that was never asked — but
silently dropping data is the more dangerous of the two failure modes, and
`zip(*rows, strict=True)` on Python 3.10 and later turns it back into an error.

Two more things `zip` gives you for free: the empty matrix works
(`list(zip(*[])) == []`), and the result is tuples, so
`list(map(list, zip(*matrix)))` is the full equivalent of our function.

Why write the comprehension at all, then? Because `zip(*rows)` is a trick you
have to *recognise*, and the comprehension is a thing you can *derive*. Once you
can read the nested form, `zip(*rows)` is a shortcut you have earned. Learn it
the other way round and you have one memorised incantation and no way to handle
the next problem, which will not have one.

</details>

## Acceptance checklist

- [ ] `transpose([[1, 2, 3], [4, 5, 6]])` gives `[[1, 4], [2, 5], [3, 6]]`.
- [ ] `transpose([[1]])` gives `[[1]]`.
- [ ] `transpose([[1, 2], [3, 4], [5, 6]])` gives `[[1, 3, 5], [2, 4, 6]]`.
- [ ] `transpose([])` gives `[]` and does not raise.
- [ ] `transpose(transpose(m)) == m` for a matrix that is **not** square.
- [ ] The body is a list comprehension, not a pair of `for` loops.
- [ ] The matrix you passed in is unchanged afterwards.
- [ ] The signature has type hints and the function has a docstring.
- [ ] Committed with a message like `Week 5 homework: matrix transpose`.

## Stretch

- **Make the docstring example a real test.** Run
  `python -m doctest week-05-solutions.py -v` and watch the `>>>` line in the
  docstring get executed and compared. A docstring that is checked by a machine
  cannot quietly go out of date, which is the whole argument for writing
  examples in that format.
- **Handle ragged rows deliberately.** Write `transpose_ragged` that pads short
  rows with `None` up to the longest row, so
  `[[1, 2, 3], [4, 5]]` becomes `[[1, 4], [2, 5], [3, None]]`. Then decide
  whether padding or raising is the better contract, and write one sentence in
  the docstring saying which you chose and why. `itertools.zip_longest` does the
  padding for you.
- **Transpose in place for a square matrix.** For an `n` by `n` grid you can
  swap `matrix[i][j]` with `matrix[j][i]` for every `j > i` and never build a
  second list. Write it, then check that your loop bounds really are `j > i` —
  running over the whole grid swaps everything twice and gives you the original
  back, which is a wonderfully confusing bug.
- **Rotate instead of transpose.** A 90-degree clockwise rotation is a transpose
  followed by reversing each row: `[list(reversed(r)) for r in transpose(m)]`.
  Work out on paper why that is the same thing, then check whether reversing
  *first* and transposing second rotates the other way.
- **Time it against `zip`.** Use `timeit` on a 200-by-200 grid to compare the
  comprehension with `list(map(list, zip(*matrix)))`. Both are linear in the
  number of elements, so the difference is a constant factor rather than a
  different curve — which is a useful thing to see with your own eyes.

Next: [Homework Problem 2 — Invert a dictionary](./problem-02-invert-a-dictionary.md).
