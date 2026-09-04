# Homework Problem 3 — A Tiny Script with Comments and a Docstring

> **Topic:** module docstrings, `#` comments, constants, type hints, and the `if __name__ == "__main__":` guard
> **Lecture:** [Lecture 1 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 45 minutes
> **Why this one:** it is the smallest possible program that still has every habit you will use for fifteen weeks. Three facts about you, printed. The facts are not the point; the shape of the file is.

## The Brief

Inside the project you built in Problem 2, write a script called
`about_me.py` that prints three facts about you: your name, your favourite
food, and one thing you want to be able to do with Python by the end of
this course.

That is the easy half. The other half is that the file has to be *shaped*
like a real Python file:

- It starts with a **docstring** — a triple-quoted string on the first
  line that says what the file is for. Not a comment. A string.
- It has at least two **comments**, the `#` kind, explaining a decision a
  reader would otherwise have to guess at.
- The printing happens inside a **function** with a type hint on it.

A docstring and a comment look similar and are completely different
animals. A comment is a note in the margin — Python throws it away before
your program ever runs. A docstring is a real piece of your program that
sticks around and can be read back while the program is running. That is
what `help()` reads. That is what your editor shows you in a tooltip.
Under the hood has the full story.

## Starter

Create `about_me.py` in your `week-01-homework` folder with this, then
replace the three strings with facts about you:

```python
"""TODO: one line saying what this file does.

TODO: a sentence or two of detail. This whole block is the docstring.
"""

# TODO: a comment explaining why the facts live up here
NAME: str = "TODO"
FAVORITE_FOOD: str = "TODO"
COURSE_GOAL: str = "TODO"


def main() -> None:
    """TODO: one line saying what this function does."""
    # TODO: a second comment
    print(f"My name is {NAME}.")


if __name__ == "__main__":
    main()
```

That starter runs as pasted. It prints one line. Your job is to get it to
three, and to fill in every `TODO`.


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/homework/problem-03-a-tiny-script-with-comments-and-a-docstring.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `python about_me.py` prints exactly three lines, one fact per line.
2. The first thing in the file, ignoring blank lines, is a triple-quoted
   docstring.
3. At least two `#` comments appear somewhere in the file.
4. All the printing happens inside one function that carries a type hint —
   `def main() -> None:` is enough.
5. The `if __name__ == "__main__":` guard is present and calls `main()`.

## Constraints

- **Use `"""` for docstrings, not `'''`.** Both are legal. Python's style
  guide for docstrings picks the double-quoted form and asks you to be
  consistent, which keeps the other style free for the rare docstring that
  has to contain a `"""` inside it. Pick one and stop thinking about it.
- **The three facts are constants at the top of the file, in
  `SCREAMING_SNAKE_CASE`.** Python has no way to make a value truly
  unchangeable, so the capital letters are a message to humans: this is a
  setting, do not reassign it.
- **Three separate `print()` calls, not one with `\n` in it.** One
  statement per line of output. It is longer and it is easier to be
  visibly wrong about, which is the trade you want.
- **Write the type hint even though nothing checks it.** Python stores
  annotations and otherwise ignores them at runtime. They are for readers
  and for tools. Writing them now, while the functions are trivial, is how
  it becomes automatic later, when it starts catching real bugs.

## Expected output

```text
$ python about_me.py
My name is Ada Lovelace.
My favorite food is cold sesame noodles.
My goal for this course is to automate the boring parts of my job with Python.
```

Your three facts will be your own. Three lines is the part that is being
checked.

## Steps

1. Activate your Week 1 environment and `cd` into `week-01-homework`.
2. Create `about_me.py` and paste the starter.
3. Replace the three `TODO` strings with your own facts.
4. Add the two missing `print()` calls.
5. Write the module docstring and both comments properly. Say *why*, not
   *what* — `# print the name` is worthless; `# keep the data at the top
   so the printing code never changes` earns its space.
6. Run it: `python about_me.py`. Count the lines.
7. Check the docstring is really a docstring:
   `python -c "import about_me; print(about_me.__doc__ is not None)"`
   should print `True`.
8. Commit: `git add about_me.py` then
   `git commit -m "Add about_me.py with three facts"`.

## The Solution

```python
"""Print three facts about the author: name, food, and a course goal.

Week 1 homework, problem 3, Code Crunch Convos. Three lines out, no input
in. Save your own copy as ``about_me.py`` in your homework repository.
"""

# Edit these three strings and nothing else. Keeping the data at the top
# means the printing code below never has to change.
NAME: str = "Ada Lovelace"
FAVORITE_FOOD: str = "cold sesame noodles"
COURSE_GOAL: str = "automate the boring parts of my job with Python"


def main() -> None:
    """Print exactly three lines, one fact per line."""
    # One print() per fact, so the output is three lines even if a fact
    # is empty -- print() with no arguments still ends the line.
    print(f"My name is {NAME}.")
    print(f"My favorite food is {FAVORITE_FOOD}.")
    print(f"My goal for this course is to {COURSE_GOAL}.")


if __name__ == "__main__":
    main()
```

**Why it works.**

**The docstring is the first *statement*, not the first line.** That
distinction matters. Python takes a string sitting alone at the top of a
file and attaches it to the file itself, under the name `__doc__`. You can
read it back while the program runs:

```bash
python -c "import about_me; print(about_me.__doc__.splitlines()[0])"
```

```text
Print three facts about the author: name, food, and a course goal.
```

Try that with a `#` comment and there is nothing to read — the comment
stopped existing before the program started. If you put a comment *above*
the docstring, the docstring is still the first statement and everything
still works, because comments are invisible to this rule.

**Data at the top, formatting at the bottom.** Three constants and then
three `print()` calls is more lines than one long `print()`. What you buy
is separation: the thing a reader is most likely to want to change (the
facts) sits away from the thing they are least likely to change (the
printing). That instinct is behind every configuration file you will ever
write.

**`-> None` is not decoration.** `main()` ends with no `return`
statement, so it hands back `None`, and the annotation says so out loud.
Python does not enforce it; it stores it and moves on.

**Three `print()` calls, not one.** `print("a\nb\nc")` gives the same
three lines and is shorter. It is also the version where a missing `\n`
silently glues two facts together, and where you cannot put a comment
against one individual fact.

## Run it

Copy the worked answer on this page into `problem-03-a-tiny-script-with-comments-and-a-docstring.py` and run it:
and run it:

```bash
python problem-03-a-tiny-script-with-comments-and-a-docstring.py
```

It is the same program as `about_me.py`; only the filename differs, so the
page and the file can be checked against each other automatically. Save
your own copy as `about_me.py` in your homework repository.

## Common bugs to catch

- **`SyntaxError: unterminated triple-quoted string literal`.** You opened
  with `"""` and closed with `'''`, or forgot to close it at all. The
  quotes have to match, and there have to be two sets.
- **The file prints nothing.** You defined `main()` and never called it,
  or you mistyped the guard. `__main__` has two underscores on each side —
  four in total. `_main_` is a different string and will never match.
- **`about_me.__doc__` is `None`.** You put the docstring inside `main()`
  instead of at the top of the file. Both docstrings are good and a
  healthy file has both; the module-level one is the one being asked for.
- **You called `main()` without the guard, and importing the file printed
  everything.** The file still works when you run it directly, but the
  moment anything imports it, all three facts appear as a side effect.
  Week 1 is where that habit is cheapest to install.
- **A `#` inside a string is not a comment.**

  ```python
  print("Use # for comments")  # this one really is a comment
  ```

  Only the second `#` starts a comment. The first is a character inside a
  string. Python always knows which is which; people who were taught
  "`#` starts a comment" without the qualifier do not.
- **Your comments say what the code already says.** `# print the name`
  above `print(NAME)` is noise. A comment earns its place by explaining a
  decision — why this way and not the obvious other way.

## Under the hood

<details>
<summary>Under the hood — why a docstring is not a comment</summary>

They are handled at two completely different stages, and the difference is
worth seeing rather than memorising.

**A comment dies in the tokenizer.** Before Python compiles anything, it
chops your source into tokens. When it meets a `#` outside a string, it
throws away the rest of the line. By the time the compiler runs, the
comment has already stopped existing. There is no runtime cost and no
runtime trace — you cannot ask a running program what its comments said,
because the answer is nowhere.

**A docstring is compiled into your program.** A string literal that
appears as the *first statement* of a module, a class, or a function is
given a special job: Python stores it as that object's `__doc__`
attribute. It is a real object, taking real memory, readable at runtime:

```bash
python -c "import about_me; print(type(about_me.__doc__), len(about_me.__doc__))"
```

```text
<class 'str'> 213
```

Everything that shows you documentation is reading that attribute.
`help(about_me)` reads it. Your editor's tooltip reads it. Documentation
generators read it. That is the whole reason the convention exists.

You can watch the difference in the compiled bytecode:

```bash
python -c "import dis; dis.dis(compile(open('about_me.py').read(), 'about_me.py', 'exec'))"
```

The comments are simply absent. The docstring appears as a constant being
stored.

Three follow-on facts:

- **Only the first statement counts.** A string sitting on line 40 in the
  middle of a function is a perfectly legal expression that gets evaluated
  and thrown away. It is not a docstring, and nothing will tell you so.
  Some people use that for multi-line "comments"; it works, and it costs
  you a string object each time the line runs.
- **`python -OO` strips docstrings.** Running with two `-O` flags discards
  them to save memory, and `__doc__` becomes `None`. Any code that depends
  on reading its own docstrings breaks under that flag. Rare, but it is
  the reason docstrings are documentation and never program logic.
- **The style rules are PEP 257.** One-line summary, imperative mood
  ("Print three facts", not "Prints three facts"), a blank line before any
  longer explanation, closing `"""` on its own line for multi-line
  docstrings.

</details>

<details>
<summary>Under the hood — what the __main__ guard is really comparing</summary>

Every module Python loads gets a variable called `__name__`. The value
depends entirely on *how* it was loaded:

- Run directly, as `python about_me.py`, the module's `__name__` is the
  string `"__main__"`.
- Imported by something else, as `import about_me`, its `__name__` is
  `"about_me"` — the module's own name.

So `if __name__ == "__main__":` reads as "only do this if I am the file
that was run, not a file that was imported". Prove it in one line:

```bash
python -c "import about_me; print(about_me.__name__)"
```

```text
about_me
```

This is the line that separates a *script* (something you run) from a
*module* (something you import). Without it, every import has side
effects, and by Week 4, when you start importing your own code, that turns
into a genuinely confusing class of bug — output appearing from a file you
only meant to borrow one function from.

The annotations work the same way: stored, not enforced. `main()` carries
its hint in a dictionary you can read:

```bash
python -c "import about_me; print(about_me.main.__annotations__)"
```

```text
{'return': None}
```

Python will happily run a function whose annotation is a lie. Type
checkers exist precisely because the interpreter does not check.

</details>

## Acceptance checklist

- [ ] `python about_me.py` prints exactly three lines.
- [ ] The first non-blank line of the file opens a triple-quoted
      docstring.
- [ ] `python -c "import about_me; print(about_me.__doc__ is not None)"`
      prints `True`.
- [ ] At least two `#` comments are present, and each explains a decision
      rather than restating the code.
- [ ] All printing happens inside `main()`, which is annotated `-> None`.
- [ ] The `if __name__ == "__main__":` guard calls `main()`.
- [ ] Committed with a message like `Add about_me.py with three facts`.

## Stretch

- Count your own comments with a program instead of your eyes:

  ```bash
  python -c "print(sum(1 for line in open('about_me.py', encoding='utf-8') if line.lstrip().startswith('#')))"
  ```

  It only sees whole-line comments — a trailing comment after code would
  need a real parser to find — and that limitation is itself worth
  noticing.
- Run `help(about_me)` inside the REPL after importing it, and see your
  own docstring formatted the way the standard library's is.
- Read PEP 8 all the way through at <https://peps.python.org/pep-0008/>,
  then run `import this` in the REPL for PEP 20, Python's design
  philosophy in twenty lines. Both are short. Both explain rules you have
  been following without knowing why.
- Rewrite the three facts as a list of strings and print them in a loop.
  Same output, and it is the shape a test would need in Week 11.

Next: [Homework Problem 4 — Install and Freeze a Package](./problem-04-install-and-freeze-a-package.md).
