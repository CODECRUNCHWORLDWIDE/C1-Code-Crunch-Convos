# Exercise 4 — Multiplication Table

> **Topic:** Nested `for` loops and `print` formatting
> **Lecture:** [02 — Loops: Doing Things Repeatedly](../lecture-notes/02-loops.md)
> **Difficulty:** Easy
> **Target time:** 20 minutes
> **Why this one:** a nested loop is the first program where you have to hold two moving parts in your head at once, and where a `print()` one indentation level off produces output that is wrong in a way you can actually see. Grids, calendars, board games and every table you ever draw are this shape. The column alignment is not decoration either: lining numbers up is what turns a wall of digits into something a person can read down a column.

## The Brief

Print a times-table card for the Code Crunch tutoring sessions. Twelve rows
by twelve columns, with a header row across the top, a header column down
the left, and a rule separating the headers from the body. Every cell sits
in a fixed-width column with the digits pushed to the right, so the ones,
tens and hundreds stack up neatly.

Two loops. The outer one walks the rows. The inner one walks the columns
and builds up one row's worth of text.

The row is printed once, *after* the inner loop has finished. Where that
`print()` goes is the whole exercise. Put it inside the inner loop and you
get 144 lines with one number on each. Put it outside the outer loop and
you get one row.

And you build the row as a string rather than printing pieces as you go.
That is deliberate. A string is a value your program is holding. You can
check it, compare it, hand it to something else, write it to a file. Text
that has already gone to the screen is gone.

## Starter

Create `exercise-04-multiplication-table.py` in your practice repo, paste
this in, then fill in the four `TODO`s:

```python
"""exercise-04-multiplication-table.py — nested loops and aligned columns.

Prints an aligned N-by-N multiplication table with header row, header
column, and a separator rule.
"""

TABLE_SIZE = 12
CELL_WIDTH = 4


def build_row(row: int, size: int) -> str:
    """Return one body row of the table, header cell included.

    Example for row 3 of a 5-wide table:
    "   3 |   3   6   9  12  15"
    """
    line = f"{row:>{CELL_WIDTH}} |"
    # TODO: append one right-aligned cell per column, 1 through size.
    return line


def build_header(size: int) -> str:
    """Return the header row: an 'x' corner cell then 1 through size."""
    line = f"{'x':>{CELL_WIDTH}} |"
    # TODO: append the column numbers, formatted exactly like the cells
    # in build_row so the columns line up.
    return line


def build_rule(size: int) -> str:
    """Return the separator rule that sits under the header."""
    # TODO: CELL_WIDTH + 1 dashes, then a "+", then CELL_WIDTH * size
    # dashes. The "+" must land directly under the "|".
    return ""


def main() -> None:
    """Print the header, the rule, and every body row."""
    print(build_header(TABLE_SIZE))
    print(build_rule(TABLE_SIZE))
    # TODO: print one body row per row number, 1 through TABLE_SIZE.


if __name__ == "__main__":
    main()
```

Two things to read before you start.

**`f"{value:>4}"` means "print this in a four-character space, pushed
right".** The `>` is an arrow pointing at the side the text gets shoved
towards. `f"{7:>4}"` is three spaces and a `7`. `f"{144:>4}"` is one space
and `144`. Everything comes out four characters wide, which is what makes a
column a column.

**`f"{value:>{CELL_WIDTH}}"` is the same thing with the width looked up
instead of typed.** The inner `{CELL_WIDTH}` is filled in first, and then
the result is used as the width. That is what lets one edit at the top of
the file re-align the entire table.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-03-control-flow/exercises/exercise-04-multiplication-table.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The table is 12 by 12, driven by `TABLE_SIZE`. Setting it to 5 must
   produce a correct 5 by 5 table with no other edit.
2. Every cell is right-aligned in a space of `CELL_WIDTH` characters, using
   `f"{value:>{CELL_WIDTH}}"`.
3. The header row starts with `x` in the corner cell, aligned like
   everything else, followed by ` |`.
4. The rule is `CELL_WIDTH + 1` dashes, then a single `+`, then
   `CELL_WIDTH * size` dashes. For the default 12 by 12 that is 5 dashes, a
   `+`, and 48 dashes.
5. Body rows print in order, 1 through 12, one `print()` call each.
6. No line ends in a space. Because every cell is right-aligned, the last
   character of every row is a digit, which is exactly what you want.

## Constraints

- **Build the row string, then print it once.** Printing with `end=" "`
  inside the inner loop ([Lecture 2 §11](../lecture-notes/02-loops.md))
  draws the same grid on screen, but the row only ever exists as pixels. It
  is not something your program can hold, check or reuse. Returning a
  string means `build_row(3, 5)` can be compared against the example in its
  own docstring.
- **`CELL_WIDTH` is 4 because the largest cell is 144.** Three digits, plus
  one character of gap. Set it to 3 and row 12 runs its numbers together;
  set it to 6 and the table is wider than it needs to be. Pick your width
  from the widest value you have to print, not by nudging a number until it
  looks right on your screen with your font.
- **Use the format spec, not hand-made spaces.** Computing
  `" " * (CELL_WIDTH - len(str(value)))` works right up until a value is
  wider than the space you left it. Then the repeat count goes negative,
  `" " * -1` is an empty string, and the table skews with no error at all.
  A format spec cannot produce that surprise; it just overflows the field
  and stays honest about it.
- **The `+` in the rule must land exactly under the `|`.** That is why the
  rule uses `CELL_WIDTH + 1`: four characters for the corner cell, plus the
  space before the pipe. Working it out from `CELL_WIDTH` rather than
  typing five dashes means the rule follows along when you change the
  width.
- **Loop over `range(1, size + 1)`, not `range(size)`.** A times table has
  no zero row and no zero column. `range(size)` would give you a row of
  zeros at the top *and* leave you one column short on the right — two bugs
  from one missing argument.
- **`def` is Week 4, and these five exercises are the deliberate exception:
  the starter hands you the function headers already written, so you are
  filling in a body someone else declared rather than deciding what a
  function should be.**

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-04-multiplication-table.py
   x |   1   2   3   4   5   6   7   8   9  10  11  12
-----+------------------------------------------------
   1 |   1   2   3   4   5   6   7   8   9  10  11  12
   2 |   2   4   6   8  10  12  14  16  18  20  22  24
   3 |   3   6   9  12  15  18  21  24  27  30  33  36
   4 |   4   8  12  16  20  24  28  32  36  40  44  48
   5 |   5  10  15  20  25  30  35  40  45  50  55  60
   6 |   6  12  18  24  30  36  42  48  54  60  66  72
   7 |   7  14  21  28  35  42  49  56  63  70  77  84
   8 |   8  16  24  32  40  48  56  64  72  80  88  96
   9 |   9  18  27  36  45  54  63  72  81  90  99 108
  10 |  10  20  30  40  50  60  70  80  90 100 110 120
  11 |  11  22  33  44  55  66  77  88  99 110 121 132
  12 |  12  24  36  48  60  72  84  96 108 120 132 144
```

Rows 9 and 12 are the ones that punish a width you guessed at. `108`,
`120`, `132` and `144` are the three-digit values, and with `CELL_WIDTH`
set to 3 they touch the number in front of them.

Row 10 is the one that punishes a hard-coded corner. The row header goes
from one digit to two, and if you built the left column with `f"{row} |"`
instead of a width, every row from 10 down shifts and the whole grid skews.

With `TABLE_SIZE = 5` the same code must produce this, rule included:

```text
   x |   1   2   3   4   5
-----+--------------------
   1 |   1   2   3   4   5
   2 |   2   4   6   8  10
   3 |   3   6   9  12  15
   4 |   4   8  12  16  20
   5 |   5  10  15  20  25
```

## Steps

1. Create `exercise-04-multiplication-table.py` and paste the starter in.
2. Fill in `build_row()` first. One `for` over the columns, with
   `line += f"{row * column:>{CELL_WIDTH}}"` inside it.
3. Check it on its own before you check the table. Run
   `python -i exercise-04-multiplication-table.py`, then:

   ```text
   >>> build_row(3, 5)
   '   3 |   3   6   9  12  15'
   ```

   That is the exact string from the docstring. Count the characters if you
   have to — it is worth doing once.
4. Fill in `build_header()`. It is the same loop with `column` where
   `row * column` was, which is a hint that a smarter version of this file
   has one function and not two.
5. Fill in `build_rule()`, then the loop in `main()`.
6. Run it and compare against the 12 by 12 block above, especially rows 9
   through 12. Then check the other two helpers:

   ```text
   >>> build_header(5)
   '   x |   1   2   3   4   5'
   >>> build_rule(5)
   '-----+--------------------'
   ```

   `build_rule(5)` is five dashes, a `+`, and twenty dashes: 5 + 1 + 20.
7. Change `TABLE_SIZE` to 5, run again, and confirm you get the small table
   exactly — rule length included. If the rule stayed 48 dashes wide,
   something in `build_rule` is reading a constant where it should be
   reading `size`. Then set it back to 12.

## The Solution

```python
"""exercise-04-multiplication-table-solution.py — nested loops and aligned columns.

Prints an aligned N-by-N multiplication table with header row, header
column, and a separator rule.
"""

TABLE_SIZE = 12
CELL_WIDTH = 4


def build_row(row: int, size: int) -> str:
    """Return one body row of the table, header cell included.

    Example for row 3 of a 5-wide table:
    "   3 |   3   6   9  12  15"
    """
    line = f"{row:>{CELL_WIDTH}} |"
    for column in range(1, size + 1):
        line += f"{row * column:>{CELL_WIDTH}}"
    return line


def build_header(size: int) -> str:
    """Return the header row: an 'x' corner cell then 1 through size."""
    line = f"{'x':>{CELL_WIDTH}} |"
    for column in range(1, size + 1):
        line += f"{column:>{CELL_WIDTH}}"
    return line


def build_rule(size: int) -> str:
    """Return the separator rule that sits under the header."""
    return "-" * (CELL_WIDTH + 1) + "+" + "-" * (CELL_WIDTH * size)


def main() -> None:
    """Print the header, the rule, and every body row."""
    print(build_header(TABLE_SIZE))
    print(build_rule(TABLE_SIZE))
    for row in range(1, TABLE_SIZE + 1):
        print(build_row(row, TABLE_SIZE))


if __name__ == "__main__":
    main()
```

**The nesting is real. It is just spread across two places.** `main()`
loops over rows; `build_row` loops over columns. The inner body runs
`TABLE_SIZE * TABLE_SIZE` times — 144 for the default — exactly as it would
if both `for` statements sat in the same function
([Lecture 2 §11](../lecture-notes/02-loops.md)). Splitting them does not
change the arithmetic. It changes what you can inspect. `build_row(3, 5)`
is a value you can print, compare or paste into a test. A nested loop that
prints as it goes leaves nothing behind at all.

**One `print` per row, and it is outside the inner loop.** This is the
whole exercise in one sentence. The inner loop *adds* to `line`. The row
leaves the function as a finished string. `main()` prints it once. Move the
printing inside the inner loop and you get 144 lines of one number each,
which you can diagnose from the shape of the output without reading a line
of your code.

**`f"{value:>{CELL_WIDTH}}"` is a slot inside a slot.** The outer `{}` is
the value. The inner `{}` is the *width*, looked up from the constant while
the program runs. That is what makes one edit at the top of the file
re-align every cell in the table at once.

**Width 4 comes from the data, not from nudging.** The largest cell in a 12
by 12 table is 144 — three characters — plus one for separation. Choosing a
width from the widest thing you have to print is a habit worth forming now,
because the alternative is a number you tuned until it happened to look
right. The stretch below makes it explicit: `len(str(size * size)) + 1`.

**The rule is worked out, not counted.** `CELL_WIDTH + 1` dashes, a `+`,
then `CELL_WIDTH * size` dashes. The `+ 1` is the space between the corner
cell and the `|`: the corner cell takes four characters, the space is the
fifth, so the pipe is the sixth character of the line, and the `+` has to
be the sixth character of the rule. Typing five dashes would work today and
break the moment `CELL_WIDTH` changes. Anything you can work out from a
constant, work out from the constant.

**`range(1, size + 1)`, both times.** A times table starts at one, in both
directions.

**No trailing whitespace, for free.** Because every cell is right-aligned,
the last character of every row is a digit. Requirement 6 is satisfied by
the alignment rule rather than by anything extra:

```text
>>> any(build_row(r, 12).endswith(" ") for r in range(1, 13))
False
```

**What a function would still buy you here.** `build_header` and
`build_row` are the same loop with `column` where `row * column` should be.
Two functions that differ by one expression are one function waiting to be
written, and Week 4 is where you will have the tools to write it on purpose
— something like `build_line(label, values)`, called twice with different
values. Notice the duplication now so that the tidy-up has an obvious
target when you get there.

## Run it

Copy the worked answer on this page into `exercise-04-multiplication-table.py` and run it:

```bash
python exercise-04-multiplication-table.py
```

It is the same program as the one you are writing, under a name that will
not collide with your own `exercise-04-multiplication-table.py`.

## Common bugs to catch

- **144 lines with one number on each.** Your `print()` is inside the inner
  loop instead of after it. In the starter's shape, that means you called
  `print()` inside `build_row()` rather than adding to `line`.

- **Only one row prints, and it is the last one.** The
  `print(build_row(...))` call sits outside the loop in `main()`, so it
  runs once with whatever the loop variable ended on.

- **Every row is the same as row 1.** The inner loop multiplies the wrong
  pair — `column * column` or `row * row` instead of `row * column`. Nested
  loops make it very easy to reach for the wrong one of two similar names.

- **`ValueError: Invalid format specifier '>CELL_WIDTH' for object of type
  'int'`.** The inner braces went missing, so you wrote
  `f"{row * column:>CELL_WIDTH}"`. The header and rule print fine, because
  they were built before the broken line ran:

  ```text
     x |   1   2   3   4   5   6   7   8   9  10  11  12
  -----+------------------------------------------------
  Traceback (most recent call last):
    File "exercise-04-multiplication-table.py", line 45, in <module>
      main()
      ~~~~^^
    File "exercise-04-multiplication-table.py", line 41, in main
      print(build_row(row, TABLE_SIZE))
            ~~~~~~~~~^^^^^^^^^^^^^^^^^
    File "exercise-04-multiplication-table.py", line 19, in build_row
      line += f"{row * column:>CELL_WIDTH}"
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
  ValueError: Invalid format specifier '>CELL_WIDTH' for object of type 'int'
  ```

  The message quotes back the spec it could not read, which is the fastest
  possible clue. Python took `>CELL_WIDTH` as a literal alignment
  instruction and found no number in it. A variable used as a width has to
  be its own slot.

- **`TypeError: can only concatenate str (not "int") to str`.** You wrote
  `line += row * column` and tried to glue a number onto a string:

  ```text
    File "exercise-04-multiplication-table.py", line 19, in build_row
      line += row * column
  TypeError: can only concatenate str (not "int") to str
  ```

  Read the message carefully — it is phrased from the string's point of
  view, which is why "str" comes first. The f-string is what converts the
  number for you. Without one you would need `str(row * column)`, and you
  would have lost the alignment as well.

- **No error, and the grid skews from row 10 onward.** You wrote
  `line = f"{row} |"` for the left header cell:

  ```text
     x |   1   2   3   4   5   6   7   8   9  10  11  12
  -----+------------------------------------------------
  9 |   9  18  27  36  45  54  63  72  81  90  99 108
  10 |  10  20  30  40  50  60  70  80  90 100 110 120
  11 |  11  22  33  44  55  66  77  88  99 110 121 132
  ```

  Every row is shifted left, and rows 10 through 12 are shifted differently
  from rows 1 through 9 because their headers are two characters instead of
  one. The body cells are still correct — it is the frame that moved.
  Format the header cell with the same width spec as everything else and
  the column re-anchors.

- **The `+` sits one character off from the `|`.** You used `CELL_WIDTH`
  dashes instead of `CELL_WIDTH + 1`:

  ```text
     x |   1   2   3   4   5   6   7   8   9  10  11  12
  ----+------------------------------------------------
     1 |   1   2   3   4   5   6   7   8   9  10  11  12
  ```

  Put a finger on the `|` in the header and look straight down. This is a
  bug best found by looking rather than by reading code.

- **`build_rule()` prints an empty line.** You built the rule into a local
  variable but the starter's `return ""` is still the last line, so that is
  what comes back. Return the string you built.

## Under the hood

<details>
<summary>Under the hood — the format spec mini-language, and the slot inside a slot</summary>

Everything after the `:` inside an f-string slot is a tiny separate
language. It is not Python. It is a short description of how to turn one
value into text, and it always comes in the same order:

```text
[[fill]align][sign][#][0][width][,][.precision][type]
```

You will only ever use a few pieces of that, but knowing the order is what
lets you read someone else's:

```text
>>> f"{144:>8}"      # width 8, pushed right
'     144'
>>> f"{144:<8}|"     # pushed left
'144     |'
>>> f"{144:^8}|"     # centred
'  144   |'
>>> f"{144:*^8}"     # centred, padded with * instead of space
'**144***'
>>> f"{1234.5678:>10.2f}"   # width 10, two decimal places, fixed-point
'   1234.57'
>>> f"{1234567:>12,}"       # width 12, thousands separators
'   1,234,567'
```

Numbers are right-aligned by default and strings are left-aligned by
default, which is a sensible choice that will still bite you. That is why
the `x` in the corner cell of this table needs its `>` written out — it is
a string, so without the arrow it would sit on the left while every number
below it sat on the right.

**The slot inside a slot.** Any part of that spec can itself be a slot
filled in while the program runs:

```text
>>> width = 6
>>> f"{144:>{width}}"
'   144'
>>> places = 3
>>> f"{3.14159:.{places}f}"
'3.142'
```

Python builds the spec string first — `{width}` becomes `6`, so the spec
becomes `>6` — and only then applies it. That is why `f"{144:>width}"`
without the braces fails: Python takes `>width` literally, looks for a
number after the `>`, and finds the letters `width`. The error message says
so in as many words: `Invalid format specifier '>CELL_WIDTH'`.

**What the width does and does not promise.** The width is a *minimum*, not
a maximum. If the value is wider, it is printed in full and the column
gets pushed out:

```text
>>> f"{1234:>4}"
'1234'
>>> len(f"{1234:>4}")
4
>>> len(f"{12345:>4}")
5
```

That behaviour is deliberate and it is much better than the alternative.
Silently truncating a number would produce a table that is beautifully
aligned and shows the wrong values. Overflowing produces a table that looks
slightly wrong, which is exactly the signal you want. If you need
truncation you have to ask for it — `f"{text:>4.4}"` caps a string at four
characters as well as padding it to four.

**The same machinery, three spellings.** `f"{144:>4}"`,
`"{:>4}".format(144)` and `format(144, ">4")` are the same operation. The
f-string is newest and shortest; `format()` is useful when the spec is
being worked out somewhere else and handed in as a plain string.

</details>

<details>
<summary>Under the hood — why building a string in a loop is fine here and not always</summary>

`line += f"{row * column:>{CELL_WIDTH}}"` looks like it should be slow.
Strings in Python cannot be changed once made, so `line += x` does not
extend `line` — it builds a brand new string containing both, and points
`line` at that instead. Twelve of those per row means twelve new strings.

Doing that to a string of length *n*, *n* times, is the classic quadratic
trap: each step copies everything you have so far. Build a million-character
string one character at a time that way and you copy roughly half a
trillion characters.

Two reasons it is fine here.

**The numbers are tiny.** A row is at most 60 characters and there are 12
of them. The total copying is measured in kilobytes. Reaching for a faster
technique at this size is not optimisation, it is noise in your code.

**CPython cheats, carefully.** When a string has exactly one name pointing
at it, CPython's `+=` can sometimes resize it in place instead of copying,
which turns the quadratic case back into a linear one. It is an
implementation detail, not a language guarantee — it depends on nothing
else holding a reference to that string — so it is a nice surprise rather
than something to design around.

**What to do when the numbers are not tiny.** Collect the pieces in a list
and join them at the end:

```python
cells = [f"{row * column:>{CELL_WIDTH}}" for column in range(1, size + 1)]
line = f"{row:>{CELL_WIDTH}} |" + "".join(cells)
```

`str.join` looks at every piece first, adds up the total length, allocates
one string of exactly that size, and copies each piece in once. One
allocation, one pass. That is the version to write when you are assembling
a large document, and it is the version you will meet again in Week 5 when
list comprehensions arrive.

For a twelve-row times table, the `+=` version says what it means more
plainly, and that is worth more than the microseconds.

</details>

## Acceptance checklist

- [ ] `python exercise-04-multiplication-table.py` runs with no traceback.
- [ ] The output matches the 12 by 12 block character for character.
- [ ] `build_row(3, 5)` returns `'   3 |   3   6   9  12  15'`.
- [ ] `build_header(5)` and `build_rule(5)` match the strings in step 6.
- [ ] Setting `TABLE_SIZE = 5` produces the small table with no other edit.
- [ ] The `+` in the rule lines up under the `|` in every row.
- [ ] No row ends in a space.
- [ ] Committed to Git with a message like `Add Week 3 exercise 4: multiplication table`.

## Stretch

- Collapse `build_header()` and `build_row()` into one function that takes
  the corner label and the values to print. Two functions that differ by
  one expression are usually one function waiting to be written.
- Work `CELL_WIDTH` out from `TABLE_SIZE` instead of hard-coding it:
  `len(str(size * size)) + 1`. Set `TABLE_SIZE` to 20 and confirm the table
  is still square — the largest cell is 400, so the width should still come
  out as 4 — and at `TABLE_SIZE = 32` it should become 5.
- Print only the lower triangle, so each row stops at the diagonal and row
  3 has three cells. The inner loop's stop value now depends on the outer
  loop's variable, which is the first genuinely two-dimensional thing you
  will have written.
- Time it. Wrap `main()` in `time.perf_counter()` calls and try
  `TABLE_SIZE = 500` — 250,000 cells, and the performance warning from
  [Lecture 2 §11](../lecture-notes/02-loops.md) made concrete.

When your columns line up, move on to
[Exercise 5 — Find the Prime](./exercise-05-find-prime.md).
