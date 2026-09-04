# Exercise 2 — String Formatter

> **Topic:** f-strings, field width, alignment, and format specifications
> **Lecture:** [02 — Operators and Strings](../lecture-notes/02-operators-and-strings.md)
> **Difficulty:** Easy
> **Target time:** 25 minutes
> **Why this one:** every program you write from here on prints something a person has to read, and columns that do not line up are the difference between a report and a mess. The rules for lining things up are small — a fill character, an alignment, a width, a precision, a type — but nobody learns them by reading. You learn them by getting a column off by one and fixing it. This is also the direct rehearsal for Wednesday's tip calculator and Friday's mini-project, both of which print aligned output.

## The Brief

The community lab tracks how many minutes each member spends on the
practice machines. On Sunday somebody prints a summary and pins it to the
wall. You are writing the printer.

The report is a block of text exactly 29 characters across: a title bar,
a row of column headings, three member rows, and a total row. Numbers are
pushed to the right so the digits stack neatly under each other. Names are
pushed to the left so the block has a clean left edge.

The interesting part is the share column. Your data does not hold
percentages. It holds fractions. Ada's 1,240 minutes out of the group's
2,635 comes to `0.4705882...`, and the report has to say `47.1%`.

Python has a tool for exactly that: a format type written `%`, which
multiplies by 100 and adds the sign for you. The trap is that there are
two natural-looking wrong answers, and neither of them crashes. Multiply
by 100 yourself *and* use `%`, and you get `4705.9%`. Skip `%` and write
`.1f`, and you get `0.5`. Both run. Both are wrong. That is the trap this
whole exercise is built around.

## Starter

Create `exercise-02-string-formatter.py` and fill the two `TODO`s:

```python
"""exercise-02-string-formatter.py — print an aligned fixed-width report.

Week 2, Exercise 2. Practises f-strings, field widths, alignment, fill
characters, thousands separators, and the percentage format type.
"""

REPORT_WIDTH: int = 29
TITLE: str = "Weekly Lab Minutes"

NAME_WIDTH: int = 14
MINUTES_WIDTH: int = 7
SHARE_WIDTH: int = 8


def title_bar(title: str) -> str:
    """Return the title centred in REPORT_WIDTH and padded with '='.

    One space sits on each side of the title before padding, so the text
    never touches the '=' characters.
    """
    # TODO: centre the spaced title with the ^ alignment and '=' as fill.
    ...


def format_row(name: str, minutes: int, share: float) -> str:
    """Return one report row, exactly REPORT_WIDTH characters long.

    Name left-aligned in NAME_WIDTH; minutes right-aligned in
    MINUTES_WIDTH with a thousands separator; share (a fraction such as
    0.4706) right-aligned in SHARE_WIDTH as a percentage with one
    decimal place.
    """
    # TODO: return a single f-string with three fields and no manual spaces.
    ...


def main() -> None:
    """Print the whole report."""
    ada_minutes: int = 1_240
    grace_minutes: int = 980
    alan_minutes: int = 415
    total_minutes: int = ada_minutes + grace_minutes + alan_minutes

    print(title_bar(TITLE))
    print(f"{'Member':<{NAME_WIDTH}}"
          f"{'Minutes':>{MINUTES_WIDTH}}"
          f"{'Share':>{SHARE_WIDTH}}")
    print("-" * REPORT_WIDTH)
    print(format_row("Ada Lovelace", ada_minutes, ada_minutes / total_minutes))
    print(format_row("Grace Hopper", grace_minutes, grace_minutes / total_minutes))
    print(format_row("Alan Turing", alan_minutes, alan_minutes / total_minutes))
    print("-" * REPORT_WIDTH)
    print(format_row("TOTAL", total_minutes, 1.0))


if __name__ == "__main__":
    main()
```

Two pieces of vocabulary, both visible in the starter.

Inside an f-string, a colon splits the placeholder in two. On the left of
the colon is *what to show*. On the right is the **format spec**: the
instructions for how to show it. `{'Member':<14}` means "the word Member,
pushed left, in a space 14 characters wide".

And look at the header line in `main()`: the width is itself in braces,
`{'Member':<{NAME_WIDTH}}`. A placeholder inside a format spec lets you
feed the width in as a variable instead of typing `14` in four places.
Use the same trick in `format_row()`.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-02-data-types-operators/exercises/exercise-02-string-formatter.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `title_bar()` returns a string of exactly `REPORT_WIDTH` characters,
   with the title centred, one space on each side of it, and `=` filling
   the rest.
2. `format_row()` returns a string of exactly `REPORT_WIDTH` characters.
3. The name field is pushed left in `NAME_WIDTH`.
4. The minutes field is pushed right in `MINUTES_WIDTH` and uses a comma
   as a thousands separator, so `1240` prints as `1,240` and `980` prints
   as `980` with no comma.
5. The share field is pushed right in `SHARE_WIDTH` and uses the
   percentage format type with one decimal place, so `0.4705882` prints
   as `47.1%`.
6. `format_row()` builds one f-string. No `+` joining, no `str()` calls,
   and no spaces typed between the fields.
7. Do not change `main()` or the module constants.

## Constraints

- **No spaces typed by hand between the columns.** You could pad with
  `" " * (14 - len(name))` and it would work today. It breaks the first
  time a name is longer than 14, because the repeat count goes negative,
  a negative repeat gives you the empty string, and the column collapses
  with nothing said about it. A width in a format spec never goes
  negative and never cuts anything off. Let it do the counting.
- **Use the `%` format type, not your own multiplication.**
  `{share:.1%}` multiplies by 100, rounds to one decimal, and puts the
  sign on, all in one step. `{share * 100:.1f}%` produces the same seven
  characters today, but the `%` is now sitting *outside* the width you
  reserved, so the column is one character wider than `SHARE_WIDTH`
  claims and everything after it drifts. Anything that belongs to the
  number belongs inside the braces.
- **Use `:,` for the thousands separator, not string surgery.** Cutting
  digits into groups of three by hand is a classic beginner detour, and
  it breaks on four-digit and seven-digit numbers in different ways. One
  comma in the format spec handles every size of number.
- **Keep the constants at the top of the file in `UPPER_SNAKE_CASE`.**
  The three column widths have to add up to `REPORT_WIDTH`, and the
  separator line uses `REPORT_WIDTH` too. If those numbers are scattered
  through the file as digits, changing the report width means hunting all
  of them down, and you will miss one. Step 6 below is the test for this.

## Expected output

This is the real output of the finished file, captured on CPython 3.13.2:

```text
$ python exercise-02-string-formatter.py
==== Weekly Lab Minutes =====
Member        Minutes   Share
-----------------------------
Ada Lovelace    1,240   47.1%
Grace Hopper      980   37.2%
Alan Turing       415   15.7%
-----------------------------
TOTAL           2,635  100.0%
```

Two details worth checking against your own run.

The title bar has four `=` on the left and five on the right. There are
nine spare columns and centring cannot split nine evenly, so the extra
one goes on the right. That is defined behaviour, not a bug.

And the three member percentages happen to add to exactly `100.0`. That is
luck, not law. Rounded shares often come to `99.9` or `100.1`, and a real
report would say so in a footnote.

## Steps

1. Turn on your Week 2 virtual environment.
2. Create `exercise-02-string-formatter.py` and paste the starter in.
3. Write `title_bar()` first, since it is one placeholder. Run the file.
   You will see the bar, the headings, the separator, and then four lines
   reading `None`, because `format_row()` still has `...` for a body and
   `print()` is perfectly happy to print `None`:

   ```text
   ==== Weekly Lab Minutes =====
   Member        Minutes   Share
   -----------------------------
   None
   None
   None
   -----------------------------
   None
   ```

   No traceback. That is worth seeing on purpose: a function that has not
   been written yet does not always announce itself.
4. Write `format_row()`. Run again and compare every line to the Expected
   output. If a column is off, count characters rather than squinting.
5. Check the widths instead of trusting your eyes. Add two temporary
   lines at the end of `main()`:

   ```python
   print(len(format_row("Ada Lovelace", 1_240, 0.4705882)))  # must be 29
   print(len(title_bar(TITLE)))                              # must be 29
   ```

   ```text
   29
   29
   ```

   Delete both lines again.
6. Change `REPORT_WIDTH` to `35` and `NAME_WIDTH` to `20`, then rerun:

   ```text
   ======= Weekly Lab Minutes ========
   Member              Minutes   Share
   -----------------------------------
   Ada Lovelace          1,240   47.1%
   Grace Hopper            980   37.2%
   Alan Turing             415   15.7%
   -----------------------------------
   TOTAL                 2,635  100.0%
   ```

   Everything still lines up and the separators still match the rows.
   That is the proof that no width is hard-coded. If a line refuses to
   move, you have a number typed in somewhere. Put both constants back to
   `29` and `14`.
7. Run `mypy exercise-02-string-formatter.py` if you have it installed.

## The Solution

```python
"""exercise-02-string-formatter-solution.py — print an aligned fixed-width report.

Week 2, Exercise 2. Practises f-strings, field widths, alignment, fill
characters, thousands separators, and the percentage format type.
"""

REPORT_WIDTH: int = 29
TITLE: str = "Weekly Lab Minutes"

NAME_WIDTH: int = 14
MINUTES_WIDTH: int = 7
SHARE_WIDTH: int = 8


def title_bar(title: str) -> str:
    """Return the title centred in REPORT_WIDTH and padded with '='.

    One space sits on each side of the title before padding, so the text
    never touches the '=' characters.
    """
    spaced: str = f" {title} "
    return f"{spaced:=^{REPORT_WIDTH}}"


def format_row(name: str, minutes: int, share: float) -> str:
    """Return one report row, exactly REPORT_WIDTH characters long.

    Name left-aligned in NAME_WIDTH; minutes right-aligned in
    MINUTES_WIDTH with a thousands separator; share (a fraction such as
    0.4706) right-aligned in SHARE_WIDTH as a percentage with one
    decimal place.
    """
    return (f"{name:<{NAME_WIDTH}}"
            f"{minutes:>{MINUTES_WIDTH},}"
            f"{share:>{SHARE_WIDTH}.1%}")


def main() -> None:
    """Print the whole report."""
    ada_minutes: int = 1_240
    grace_minutes: int = 980
    alan_minutes: int = 415
    total_minutes: int = ada_minutes + grace_minutes + alan_minutes

    print(title_bar(TITLE))
    print(f"{'Member':<{NAME_WIDTH}}"
          f"{'Minutes':>{MINUTES_WIDTH}}"
          f"{'Share':>{SHARE_WIDTH}}")
    print("-" * REPORT_WIDTH)
    print(format_row("Ada Lovelace", ada_minutes, ada_minutes / total_minutes))
    print(format_row("Grace Hopper", grace_minutes, grace_minutes / total_minutes))
    print(format_row("Alan Turing", alan_minutes, alan_minutes / total_minutes))
    print("-" * REPORT_WIDTH)
    print(format_row("TOTAL", total_minutes, 1.0))


if __name__ == "__main__":
    main()
```

**The title is built first, then padded, and the order is the whole
point.** The docstring asks for one space on each side of the title
*before* the padding goes on. So `spaced` gets made first, as
`" Weekly Lab Minutes "` — twenty characters — and only then is that
twenty-character string centred in twenty-nine. You cannot do both in one
placeholder. `:=^29` pads whatever value you hand it, so handing it the
bare title gives you `=====Weekly Lab Minutes======`, with the `=`
characters jammed against the words. Build, then pad. It comes up every
time the contents of a field are themselves worked out.

**`=^29` is three separate decisions in five characters.** `=` is the
fill character. `^` is the alignment. `29` is the width. The fill always
sits immediately before the alignment character, which is why a stray
comma in that slot turns into fill instead of a thousands separator — see
Common bugs to catch.

**`{minutes:>7,}` puts the comma after the width because the grammar says
so.** The order inside a format spec is fixed: fill, align, sign, width,
grouping, precision, type. Right-align, width seven, then group with
commas. `1240` becomes `1,240` and `980` stays `980`, because the
separator only shows up where there is a group boundary to mark. The full
grammar is in Under the hood, and every format-spec error you will ever
hit is a piece written out of that order.

**`{share:.1%}` is handed the raw fraction and does the multiplying
itself.** `ada_minutes / total_minutes` is `0.47058...`. The `%`
presentation type multiplies by 100, rounds to the precision you asked
for, and puts the sign on the end — all inside the width you reserved.
Multiply by 100 yourself and the value arrives as `47.058...`, and `%`
scales it again to `4705.9%`. Skip `%` and write `.1f` and you get `0.5`,
which is the fraction rounded to one decimal and is a perfectly
reasonable-looking wrong answer.

**Nested placeholders are what make the constants real.**
`f"{name:<{NAME_WIDTH}}"` drops `14` into the spec while the program is
running, producing `<14`. Because no width is ever typed as a digit
inside `format_row()`, changing the constants at the top re-lays the whole
report. That is exactly what step 6 tests.

**A width is a minimum, never a maximum.** `Ada Lovelace` is twelve
characters and gets padded to fourteen. A nineteen-character name would
take all nineteen and push the numbers right, and that is correct
behaviour — chopping somebody's name off silently is worse than a ragged
column. If you genuinely want a hard cap, add a precision:
`{name:<14.14}`, which on a string means "at most this many characters".

```text
>>> format("Ada Lovelace Extra", "<14.14")
'Ada Lovelace E'
```

## Run it

Copy the worked answer on this page into `exercise-02-string-formatter.py` and run it:

```bash
python exercise-02-string-formatter.py
```

## Common bugs to catch

- **The share column prints `0.5`.** You wrote `.1f` where `.1%` was
  needed. The `f` type prints the number it was given; the `%` type
  scales first.

  ```text
       0.5
  ```

- **The share column prints `4705.9%`.** You did both — multiplied by 100
  yourself *and* used `%`:

  ```text
   4705.9%
  ```

  Pick one, and pick the format spec, because it keeps the sign inside
  the field.

- **The minutes column prints `,,,1240`.** You wrote `{minutes:,>7}`:

  ```text
  ,,,1240
  ```

  No error at all. Python read that as "fill with commas, push right,
  width 7", which is a legal and completely useless instruction. The fill
  slot is whatever sits immediately before `<`, `>` or `^`. The thousands
  separator goes after the width: `{minutes:>7,}`.

- **A comma anywhere else in the spec.** Two different messages, and
  which one you get depends on where the comma landed. Comma before the
  width:

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(format(1240, '>,7'))
            ~~~~~~^^^^^^^^^^^^^
  ValueError: Cannot specify ',' with '7'.
  ```

  Read that message carefully, because it is confusing the first time.
  The character Python names is not the comma's neighbour — it is the
  *presentation type* Python thinks you asked for. By the time it reached
  the comma it had already swallowed `7` as a type letter, so `7` is what
  it complains about.

  Apply a comma to a string and the same message names `'s'`, the type
  Python uses for text, because text has no digit groups to separate:

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(f"{'Ada':>7,}")
              ^^^^^^^^^^^
  ValueError: Cannot specify ',' with 's'.
  ```

  Put the comma between the precision and the type and the parser rejects
  the whole spec instead:

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print(f'{12.5:.2,f}')
              ^^^^^^^^^^^
  ValueError: Invalid format specifier '.2,f' for object of type 'float'
  ```

- **Building the row with `+`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      print("Ada" + 1240)
            ~~~~~~^~~~~~
  TypeError: can only concatenate str (not "int") to str
  ```

  Wrapping the number in `str()` silences that and costs you the format
  spec at the same time, which is why requirement 6 forbids both.

- **Padding by hand with `" " * (14 - len(name))`.** It works until a name
  is longer than the field. Then the repeat count goes negative, a
  negative repeat gives the empty string, and the column collapses with
  no warning:

  ```text
  'Ada Lovelace Extra'
  ```

  Not one space of padding, no error, and the next column starts wherever
  the name happened to stop.

- **Four rows print `None` and nothing raises.** You left `...` in
  `format_row()`. `print()` will print `None` quite happily:

  ```text
  ==== Weekly Lab Minutes =====
  Member        Minutes   Share
  -----------------------------
  None
  None
  None
  -----------------------------
  None
  ```

  There is a louder version of this mistake, but it belongs to Exercise 3,
  where a `None` gets *formatted with a spec* rather than merely printed,
  and raises `TypeError: unsupported format string passed to
  NoneType.__format__`. Here you get four quiet `None`s. `mypy` catches
  it without running anything:

  ```text
  exercise-02-string-formatter.py:25: error: Missing return statement  [empty-body]
  Found 1 error in 1 file (checked 1 source file)
  ```

- **The title bar is 28 or 30 characters.** You padded the title with
  spaces *after* centring instead of before, or you forgot one of the two
  spaces. Build the spaced title first, then centre the whole thing.

- **Names longer than 14 characters push the numbers right.** Correct
  behaviour, not a bug. A width is a minimum. If you want hard
  truncation, you need the `.14` precision described above.

## Under the hood

<details>
<summary>Under the hood — the whole format-spec grammar, in order</summary>

Everything after the colon in a placeholder is the format spec, and it
has a fixed grammar. This is it, on CPython 3.13:

```text
[[fill]align][sign][z][#][0][width][grouping][.precision][type]
```

Every part is optional. What is *not* optional is the order. Write two
parts out of sequence and you get one of the errors in Common bugs to
catch. Taking them one at a time:

**`fill`** — any single character, and it only counts as fill if an
alignment character comes straight after it. `=^29` fills with `=`.
`,>7` fills with commas, which is legal and almost never what anybody
meant.

**`align`** — `<` pushes left, `>` pushes right, `^` centres, and `=`
puts the padding between the sign and the digits, which is a
number-only trick for cheque-style output:

```text
>>> format(1240, '=+9,')
'+   1,240'
```

Text defaults to `<` and numbers default to `>`. Those two defaults are
why a table full of `{name}` and `{count}` mostly lines up before you ask
it to.

**`sign`** — `+` always shows one, `-` shows one only for negatives (the
default), and a space puts a blank where a `+` would go, so positive and
negative numbers occupy the same width.

**`z`** — new in Python 3.11. It turns negative zero into positive zero,
so a rounded `-0.0` does not appear in your report as `-0.00`.

**`#`** — the alternate form. On `b`, `o` and `x` it adds the `0b`, `0o`
or `0x` prefix.

**`0`** — pad with zeros. `{7:03}` gives `007`. It is shorthand for
`0=`, the fill-and-align pair.

**`width`** — the minimum number of characters. Never a maximum. Never
negative.

**`grouping`** — `,` for commas or `_` for underscores:

```text
>>> format(1240, '>7,')
'  1,240'
>>> format(1240, '>7_')
'  1_240'
```

**`.precision`** — the dot and a number. On `f` and `%` it is digits
after the decimal point. On `g` it is significant digits. On a *string*
it is a maximum length, and that is the one place a format spec will cut
something off:

```text
>>> format("Ada Lovelace Extra", "<14.14")
'Ada Lovelace E'
```

**`type`** — the last character, saying what kind of thing to print.
`d` whole number, `f` fixed decimal, `e` scientific, `g` general, `%`
percentage, `b` `o` `x` binary, octal, hex, `s` text. Leave it off and
Python picks the sensible default for the value's type.

Now, the question this exercise makes you answer: **where is the comma
legal?** Exactly one place — after the width and before the precision.
That is `{minutes:>7,}` and `{total:>9,.2f}`. Nowhere else. The three
failures all come from moving it:

- `,>7` — the comma is read as the fill character, so you get `,,,1240`
  and no error at all.
- `>,7` — `ValueError: Cannot specify ',' with '7'.`
- `.2,f` — `ValueError: Invalid format specifier '.2,f' for object of
  type 'float'`

The middle message is the one that reads like nonsense. Here is why it
says `'7'`. The parser reads left to right: it takes `>` as the
alignment, then looks for a sign, a `z`, a `#`, a `0`, a width. It finds a
comma where the width should be, so the width is empty and the comma is
the grouping option. Then it reads on and finds `7`, and the only thing
left in the grammar is `type`. So Python believes you asked for
presentation type `7`, and reports the clash between grouping and that
type. Same story for `'s'` when you apply a comma to a string: `s` really
is the string type, and text has no thousands to separate.

</details>

<details>
<summary>Under the hood — what an f-string actually compiles to</summary>

An f-string is not a special kind of string that gets examined at run
time. It is ordinary Python, assembled by the compiler before your
program starts. `format(value, spec)` is the plain-function version of
the same thing, and both end up calling one method:

```text
>>> f"{1240:>7,}"
'  1,240'
>>> format(1240, '>7,')
'  1,240'
>>> (1240).__format__('>7,')
'  1,240'
```

`__format__` is a method that every type carries. That is why the same
spec means different things to different values: `int.__format__` knows
about thousands separators, `str.__format__` does not, and
`float.__format__` knows about `%`. The spec is not a language of its
own. It is a string handed to the value and interpreted by the value.

That also explains `TypeError: unsupported format string passed to
NoneType.__format__`. `None` has a `__format__` too, but it accepts only
the empty spec. Print a `None` and you get `None`. Format one with `.2f`
and it refuses.

Now the nested placeholder, which is where this gets interesting. Ask
Python to disassemble `f"{name:<{w}}"`:

```text
  LOAD_NAME                0 (name)
  LOAD_CONST               0 ('<')
  LOAD_NAME                1 (w)
  FORMAT_SIMPLE
  BUILD_STRING             2
  FORMAT_WITH_SPEC
  RETURN_VALUE
```

Read the middle three instructions. Python turns `w` into text, glues it
onto `'<'` to make the string `'<14'`, and only then hands that finished
spec to `name`. The spec is built at run time, out of whatever `w`
happens to be. That is the entire mechanism behind
`{name:<{NAME_WIDTH}}`, and it is why changing one constant at the top of
the file re-lays every row.

Since Python 3.12 the nesting can go deeper than one level, because the
compiler now parses f-strings with the ordinary Python parser rather than
with a separate hand-written one. It is legal and it is unreadable. One
level is enough for every table you will ever print.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] Output matches the Expected output block exactly, including the four-then-five `=` split in the title bar.
- [ ] `len()` of any row is exactly 29, and so is `len(title_bar(TITLE))`.
- [ ] `format_row()` is a single f-string with no `+`, no `str()`, and no typed spaces.
- [ ] Changing `REPORT_WIDTH` and `NAME_WIDTH` keeps the report aligned.
- [ ] `mypy` reports no issues, if you have it installed.
- [ ] The file is committed to Git with a message like `Add Week 2 exercise 2: string formatter`.

## Stretch

- Force a sign on the share column with `{share:>+{SHARE_WIDTH}.1%}`, and
  add a fourth column showing minutes as hours, `minutes / 60`, with two
  decimals. Widen `REPORT_WIDTH` to `38` and give the new column its own
  `HOURS_WIDTH: int = 9`:

  ```text
  ========= Weekly Lab Minutes =========
  Member        Minutes   Share    Hours
  --------------------------------------
  Ada Lovelace    1,240  +47.1%    20.67
  Grace Hopper      980  +37.2%    16.33
  Alan Turing       415  +15.7%     6.92
  --------------------------------------
  TOTAL           2,635 +100.0%    43.92
  ```

  Look at the total row. `+100.0%` is seven characters against `47.1%`'s
  six, so it now touches the column before it. The sign is inside the
  field, exactly as it should be — but the field was sized for numbers
  with no sign. Widen `SHARE_WIDTH` to nine and the block breathes again.
  A forced sign is genuinely useful for changes, where you want `-2.4%`
  and `+2.4%` to take the same room, and it is noise for a share of a
  whole that can never be negative.

  The hours column is worked out inside the placeholder, because a
  placeholder accepts any expression. Fine for arithmetic this small. It
  stops being fine the moment the expression needs a name to explain
  itself.

- Right-align the names instead — change `<` to `>` in the name field —
  and read the result. The left edge turns ragged and your eye loses the
  line it was following. Left for text, right for numbers is not a taste
  thing. It is about which edge carries the information: the first letter
  of a name, the last digit of a number.

- Print the same three rows with `_` as the grouping character instead of
  `,`, and with `{minutes:>7d}` spelled out. Confirm that the default
  type for an `int` was `d` all along.

When your columns line up, move on to
[Exercise 3 — Temperature Converter](./exercise-03-temperature-converter.md).
