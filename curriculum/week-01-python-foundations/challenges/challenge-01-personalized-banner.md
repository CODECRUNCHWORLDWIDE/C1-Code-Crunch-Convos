# Challenge 1 — Personalized ASCII Banner

> **Topic:** strings, one small function, and reading arguments from the command line
> **Lecture:** [01 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** starter, with one piece of arithmetic that has to be exactly right
> **Target time:** 30–60 minutes
> **Why this one:** it is the first time you write a function that *builds* text instead of printing it, and that one habit is reused in the Week 1 mini-project and in almost everything after it.

## The Brief

You are going to draw a name inside a box made of stars.

Think of a picture frame. The picture is the name. The frame is a rectangle
of `*` characters. Between the picture and the frame there is a mat — a
margin of empty space, the same amount on the left and on the right, so the
name sits dead centre.

For the name `Ada`, the finished frame looks like this:

```text
*****************
*               *
*      Ada      *
*               *
*****************
```

Count the stars on the top row: seventeen. The name is three letters, there
are six spaces on each side of it, and there is one star at each end.
`3 + 6 + 6 + 1 + 1 = 17`. Change the name and every one of those numbers has
to move together, or the box comes out crooked.

That is the whole challenge: one function that takes a name and gives back
the five lines of the box, and a tiny bit of glue that reads the name and
prints the result.

## Starter

Save this as `banner.py` and run it before you change anything. It runs as
pasted — it just draws an empty frame, because `build_banner` does not do
its job yet.

```python
"""banner.py -- print a name centered inside a box of ASCII characters."""

import sys

DEMO_NAME: str = "Ada"


def build_banner(name: str, padding: int = 6, border: str = "*") -> str:
    """Return the multi-line banner for a name as one string.

    Args:
        name: the text to centre, already trimmed.
        padding: spaces between the name and each border column.
        border: the single character the box is drawn with.

    Returns:
        Five lines joined by newlines: edge, blank, name, blank, edge.
    """
    # TODO 1: work out inner_width from len(name) and padding.
    # TODO 2: build the edge row, the blank row and the name row.
    # TODO 3: join the five rows with "\n" and return them.
    return ""


def read_name(argv: list[str]) -> str:
    """Return the name to draw, trimmed of the spaces around it."""
    # TODO 4: join the words with spaces, strip them, fall back to DEMO_NAME.
    return DEMO_NAME


def main() -> None:
    """Read one name from the command line and print its banner."""
    print(build_banner(read_name(sys.argv[1:])))


if __name__ == "__main__":
    main()
```


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/challenges/challenge-01-personalized-banner.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `build_banner(name)` **returns** the finished banner as one string. It
   does not print anything.
2. The banner is five rows, top to bottom: a solid row of `*`, a blank
   padded row, the row with the name in it, another blank padded row, a
   solid row of `*`.
3. The name sits in the middle of its row, with **six spaces on each side**.
   So the inside of the box is `len(name) + 12` characters wide and the whole
   box is `len(name) + 14`.
4. Use `str.center()` to do the centring. Do not count spaces by hand.
5. `read_name(argv)` takes the words typed after the script name, joins them
   with single spaces, and removes any whitespace around the result.
6. When no name is given, the script prints the banner for `DEMO_NAME`
   instead of failing.
7. Every function has a type hint on every parameter and on its return, and
   a docstring saying what it gives back.
8. The file ends with an `if __name__ == "__main__":` guard.

## Constraints

- **`build_banner` returns, never prints.** A function that returns a string
  can be printed, saved to a file, coloured, or dropped into a bigger
  message. A function that prints can only ever print. The Week 1
  mini-project imports this exact function for its banner stretch goal, and
  that is only possible because it returns.
- **`str.center()`, not hand-counted spaces.** The centring and the frame
  width have to agree for every possible name. If you compute them in two
  separate places, they will disagree eventually and your box will have a
  wobbly edge. One number, derived once.
- **The name comes from the command line, not from `input()`.** That keeps
  the script runnable the same way for everyone — you, a classmate, an
  automated check — with no keyboard needed. `input()` arrives in the
  mini-project, where prompting is the point. There is a full `input()`
  version of this script under *Stretch*.
- **Six spaces per side, not three.** The number is fixed so that everyone's
  output matches the picture above, character for character. *Under the
  hood* explains where six comes from.
- **Standard library only.** Nothing to install, so the file runs on a fresh
  Python the moment it is downloaded.

## Expected output

Run with no arguments, the script draws the demo name. This is the real
stdout on CPython 3.13.2:

```text
$ python challenge-01-personalized-banner.py
*****************
*               *
*      Ada      *
*               *
*****************
```

Give it a name and the box grows to fit:

```text
$ python challenge-01-personalized-banner.py Grace Hopper
**************************
*                        *
*      Grace Hopper      *
*                        *
**************************
```

Twenty-six stars: twelve letters, one space, six spaces each side, two
border columns. And extra whitespace is trimmed away before anything is
measured:

```text
$ python challenge-01-personalized-banner.py "  Bo  "
****************
*              *
*      Bo      *
*              *
****************
```

Sixteen wide, not twenty — the four typed spaces never reached the maths.

## Steps

1. Save the starter as `banner.py` and run `python banner.py`. It prints an
   empty line. Nothing is broken; the function is just empty.
2. Fill in **TODO 1**. `inner_width` is the width of the *inside* of the box:
   `len(name) + 2 * padding`. Print it and check that `Ada` gives 15.
3. Fill in **TODO 2**, one row at a time.
   - The edge row is `border * (inner_width + 2)` — the inside plus the two
     border columns.
   - The blank row is a border character, `inner_width` spaces, a border
     character.
   - The name row is the same shape with `name.center(inner_width)` in the
     middle instead of the spaces.
4. Fill in **TODO 3**. `"\n".join([...])` glues the five rows together with a
   newline between each pair. Run it. You should see the box.
5. Fill in **TODO 4**. `" ".join(argv)` turns `["Grace", "Hopper"]` into
   `"Grace Hopper"`. Then `.strip()`. Then `or DEMO_NAME` for the empty case.
6. Test all three cases from *Expected output*: no argument, two words, and a
   quoted name with spaces around it.
7. Commit it:

   ```bash
   git add banner.py
   git commit -m "Add Challenge 1: personalized ASCII banner"
   ```

## The Solution

```python
"""banner.py -- print a name centered inside a box of ASCII characters.

Challenge 1, Week 1, Code Crunch Convos. Takes a name from the command
line, trims the whitespace around it, and prints a rectangular banner
whose width grows with the name.

Run it with::

    python banner.py Ada
"""

import sys

DEMO_NAME: str = "Ada"


def build_banner(name: str, padding: int = 6, border: str = "*") -> str:
    """Return the multi-line banner for a name as one string.

    ``padding`` is the number of spaces on each side of the name, so the
    inside of the box is ``len(name) + 2 * padding`` characters wide.

    Args:
        name: the text to centre, already trimmed.
        padding: spaces between the name and each border column.
        border: the single character the box is drawn with.

    Returns:
        Five lines joined by newlines: edge, blank, name, blank, edge.
    """
    inner_width: int = len(name) + 2 * padding
    edge: str = border * (inner_width + 2)
    blank: str = f"{border}{' ' * inner_width}{border}"
    middle: str = f"{border}{name.center(inner_width)}{border}"
    return "\n".join([edge, blank, middle, blank, edge])


def read_name(argv: list[str]) -> str:
    """Return the name to draw, trimmed of the spaces around it.

    Args:
        argv: the words typed after the script name, usually
            ``sys.argv[1:]``.

    Returns:
        Those words joined by single spaces and stripped. When nothing
        was given, ``DEMO_NAME``, so the file always prints a banner.
    """
    return " ".join(argv).strip() or DEMO_NAME


def main() -> None:
    """Read one name from the command line and print its banner."""
    print(build_banner(read_name(sys.argv[1:])))


if __name__ == "__main__":
    main()
```

**One number drives everything.** `inner_width` is worked out once, and the
other three quantities are built from it. The edge rows are `inner_width + 2`
long — the inside, plus one border column on each side. The blank row and the
name row are both exactly `inner_width` characters wrapped in a border
character. Because every row is measured from the same number, the box cannot
come out ragged. Type the widths in separately — one expression for the top
rule, another for the middle — and you have two sources of truth. Sooner or
later they disagree for some name length, and your box has a wobbly edge.

**`str.center()` does the arithmetic you were told not to do.**
`name.center(inner_width)` hands back a *new* string of length `inner_width`
with `name` sitting in the middle and spaces filling the rest. Strings in
Python never change, so every string method returns a new string rather than
editing the old one — `name` is untouched afterwards. Here the split is always
perfectly even, because the leftover space is `inner_width - len(name)`, which
is `2 * padding`, which is 12 for any name at all. Twelve halves cleanly into
six and six.

**`" ".join(argv)` handles names with spaces in them.** The shell hands your
script a *list* of words. `Grace Hopper` arrives as `["Grace", "Hopper"]`, so
joining with a single space rebuilds the name. Quoting it — `"Grace Hopper"` —
arrives as one item and joins to itself. Both spellings work.

**`or DEMO_NAME` is the empty case.** An empty string is *falsy* in Python:
in a yes-or-no position it counts as no. `or` gives back the first operand
that counts as yes, so `"" or "Ada"` is `"Ada"` and `"Bo" or "Ada"` is `"Bo"`.
The `.strip()` has to come first, because a string of three spaces is *truthy*
— it is not empty, it just looks it.

**`if __name__ == "__main__":` makes the file both a program and a library.**
When Python runs a file directly it sets that file's `__name__` to the text
`"__main__"`. When the same file is *imported* by another file, `__name__` is
the module name instead — `"banner"`. So the guard means: only read the
command line when I am the program, not when I am somebody else's toolbox.
Without it, `from banner import build_banner` in the mini-project would print
a banner as a side effect of the import.

## Download and run

Download [challenge-01-personalized-banner-solution.py](./challenge-01-personalized-banner-solution.py) and run it:

```bash
python challenge-01-personalized-banner-solution.py
```

Pass a name to draw somebody else:

```bash
python challenge-01-personalized-banner-solution.py Grace Hopper
```

In your own project, save the same code as `banner.py`. A module name with
hyphens in it cannot be imported — a hyphen means subtraction — and the
mini-project's stretch goal imports this file.

## Common bugs to catch

**The name row is one character too wide.** Symptom: the top rule and the
name row do not line up.

```text
*****************
*               *
*      Ada       *
*****************
```

Cause: you counted the padding by hand on the name row and computed it on the
edge row, so the two disagree. Fix: build every row from `inner_width`.

**The box is two characters too wide inside.** You called
`name.center(inner_width + 2)` and then wrapped it in border characters. The
`+ 2` belongs to the *edge* row only. The name row and the blank row are the
inside; only the edge rows include the border columns.

**A name typed with spaces makes an oversized box.** `python banner.py "  Ada  "`
without the `.strip()` gives `len(name) == 7`, so the box is four characters
wider than it should be and the name looks off-centre inside it, because the
invisible spaces are counted as part of the name. Strip first, then measure.

**`SyntaxError: f-string: expecting '}'`.** One closing brace is missing.
On CPython 3.13.2:

```text
  File "banner.py", line 34
    middle: str = f"{border}{name.center(inner_width){border}"
                                                             ^
SyntaxError: f-string: expecting '}'
```

The caret sits at the end of the line, not at the mistake — Python read to the
end of the string still waiting for the `}` that never came. Look for the
opening `{` that has no partner.

**`TypeError: unsupported operand type(s) for +: 'int' and 'str'`.** You wrote
the padding as text instead of a number:

```text
Traceback (most recent call last):
  File "banner.py", line 58, in <module>
    main()
    ~~~~^^
  File "banner.py", line 54, in main
    print(build_banner(read_name(sys.argv[1:])))
          ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "banner.py", line 31, in build_banner
    inner_width: int = len(name) + 2 * "6"
                       ~~~~~~~~~~^~~~~~~~~
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

`2 * "6"` is the string `"66"`, and you cannot add a string to the integer
that `len()` returned. Drop the quotes. The `~~~^~~~` markers under the line
point at the exact part of the expression that failed; they arrived in Python
3.11 and are one reason this course targets 3.11 and up.

**`NameError: name 'build_banner' is not defined`.** You called the function
above the `def` that creates it, or you are running the wrong file. Python
reads a file top to bottom; a name exists only after the line that made it.

## Under the hood

<details>
<summary>Under the hood — where the number six came from, and what center does with an odd leftover</summary>

**Why six spaces and not three.** The requirement could have been read as
"six characters of padding in total, three per side". That reading is
defensible in English and it produces a box eleven characters wide for `Ada`,
which does not match the picture. Six *per side* produces seventeen, which
does. When a written spec and its worked example disagree, the example is
what a grader compares against, and the example is what everybody else on the
course will have produced. Six per side it is.

The algebra, written out once:

```text
inner_width = len(name) + 2 * padding      the space inside the frame
total_width = inner_width + 2              plus one border column each side
            = len(name) + 2 * padding + 2
            = len(name) + 14               when padding is 6
```

So `Ada` gives `3 + 14 = 17`, `Bo` gives `2 + 14 = 16`, and `Grace Hopper`
gives `12 + 14 = 26`. Every width in *Expected output* is that formula.

**`str.center` and the odd leftover.** In this challenge the leftover space
is always `2 * padding`, an even number, so it splits evenly and the question
never comes up. It comes up the moment you use `center` anywhere else, so it
is worth knowing.

`s.center(width)` has `width - len(s)` spaces to distribute. Call that the
*margin*. When the margin is even, both sides get half. When the margin is
odd, one side gets the extra space — and which side is not what most people
guess. CPython's rule is: the extra space goes on the **left** only when the
margin and the width are *both* odd. Otherwise it goes on the right.

Measured on CPython 3.13.2:

| Call | Result | Margin | Width | Extra space |
|---|---|---|---|---|
| `"ab".center(5)` | `'  ab '` | 3, odd | 5, odd | left |
| `"abc".center(6)` | `' abc  '` | 3, odd | 6, even | right |
| `"abcd".center(9)` | `'   abcd  '` | 5, odd | 9, odd | left |
| `"abc".center(8)` | `'  abc   '` | 5, odd | 8, even | right |
| `"x".center(5)` | `'  x  '` | 4, even | 5, odd | none, even split |

Reproduce it yourself:

```bash
python -c "print(repr('ab'.center(5)), repr('abc'.center(6)))"
```

```text
'  ab ' ' abc  '
```

The practical lesson: if you are lining up several `center`ed strings in a
column and some of them are off by one, you have hit this rule. The fix is
to make the margin even — which is exactly what a fixed `padding` on both
sides does here.

**Why `"\n".join(rows)` instead of five `print` calls.** Joining builds one
string, which the caller can do anything with. Five prints commit to the
terminal on the spot. It is also cheaper: `join` walks the list once, adds up
the total length, allocates one string of that size, and copies each piece in.
Repeatedly doing `text = text + row + "\n"` allocates a brand new string on
every pass and copies everything that came before, so the work grows with the
square of the number of rows. With five rows nobody could measure the
difference. With fifty thousand rows it is the difference between instant and
a coffee break, and `join` is no harder to type.

**`sys.argv[0]` is not an argument.** `sys.argv` is the list of words the
shell handed your program, and the first one is always the script's own path.
That is why the code passes `sys.argv[1:]` — everything *after* the script
name. Passing the whole list would draw a banner containing the filename.

**Why `read_name` takes `argv` as a parameter** instead of reaching for
`sys.argv` itself. A function that reads a global can only ever be tested by
changing that global. A function that takes its input as an argument can be
called with anything: `read_name(["Ada"])`, `read_name([])`,
`read_name(["  ", ""])`. You can check all three from one `python -c` line
without touching the command line at all. This is the same instinct as
"return, do not print", applied to inputs instead of outputs.

</details>

## Acceptance checklist

- [ ] `python banner.py` prints the seventeen-wide `Ada` box, exactly as in
      *Expected output*.
- [ ] `python banner.py Grace Hopper` prints a twenty-six-wide box.
- [ ] `python banner.py "  Ada  "` prints the seventeen-wide box, not a
      twenty-one-wide one.
- [ ] Every top and bottom rule is exactly as long as the rows between them.
- [ ] `build_banner` contains no `print` call.
- [ ] `str.center()` appears in the file, and no hand-counted run of spaces
      does.
- [ ] Every function has type hints on its parameters and its return, and a
      docstring.
- [ ] The file ends with the `if __name__ == "__main__":` guard.
- [ ] Four-space indentation, `snake_case` names, lines under 80 characters.
- [ ] Committed with a clear message such as
      `Add Challenge 1: personalized ASCII banner`.

## Stretch

**Prompt for the name instead.** Swap `read_name` for a version that asks:

```python
def ask_name() -> str:
    """Return a name typed at the keyboard, trimmed."""
    return input("Your name: ").strip() or DEMO_NAME
```

Then `main` becomes `print(build_banner(ask_name()))`. Run it and type `Ada`:

```text
Your name: Ada
*****************
*               *
*      Ada      *
*               *
*****************
```

Keep this as a second file, `banner_ask.py`. A script that waits for a
keyboard cannot be checked automatically, which is why the graded file reads
its name from the command line.

**Choose the border character.** `build_banner` already takes `border`. Wire
it to a `--char` flag. Slice the value rather than indexing it —
`value[:1]` gives `""` for an empty string, where `value[0]` raises
`IndexError: string index out of range` — then `or "*"` supplies the default.
Two crashes removed by one slice.

**Banner a whole file of names.** Read one name per line and print a banner
for each:

```python
def read_names(path: str) -> list[str]:
    """Return the non-blank, whitespace-stripped lines of a file."""
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]
```

`encoding="utf-8"` is not optional politeness. Leave it out and Python uses
whatever your operating system prefers, so a file containing `José` reads
differently on Windows than on macOS.

**Colour it.** Install `colorama` with `python -m pip install colorama`, then
wrap the banner in `Fore.CYAN` and `Style.RESET_ALL`. Put the import inside a
`try` / `except ImportError` so the file still runs for somebody who has not
installed it, and call `just_fix_windows_console()` once at the top — it turns
on colour handling in the Windows console and does nothing at all on macOS and
Linux. Freeze the dependency afterwards with
`python -m pip freeze > requirements.txt`.

**Reuse it.** The Week 1 mini-project has a stretch goal that prints your
greeting inside this banner. Copy `banner.py` next to `hello_you.py` and
`from banner import build_banner`. If your `build_banner` printed instead of
returning, this is the moment you would have to rewrite it.
