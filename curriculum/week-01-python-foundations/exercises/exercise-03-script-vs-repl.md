# Exercise 3 — Script vs REPL

> **Topic:** Comparing `python script.py` to `python -i script.py`
> **Lecture:** [01 — Installing Python and Running Your First Program](../lecture-notes/01-installing-python-and-running-your-first-program.md)
> **Difficulty:** Beginner
> **Target time:** 15 minutes
> **Why this one:** exercises 1 and 2 taught you the two ways to run Python. This one shows they are the same machine with a different door, and it hands you `python -i`, the cheapest debugging tool you will ever learn. Skip it and you will spend Week 4 adding `print()` calls to find out what a variable held, when you could have just asked it.

## The Brief

You are keeping the signup list for the workshop night from Exercise 2.
You want a script that sums it up: how many people, their initials on one
line, and the longest name so you know how wide to cut the name tags.

That is the visible half. The real subject is what happens the moment the
script finishes.

Run it the ordinary way and everything vanishes as the last line prints.
The interpreter starts, does the work, exits, and takes the list with it.
Run the *same file* with `python -i` and the interpreter does exactly the
same work — then, instead of leaving, it hands you a `>>>` prompt with the
list, the functions, and every other name from the file still sitting
there ready to poke at.

Identical code both times. The only thing that changed is whether Python
walked out of the room or stayed. Knowing you get to choose is the
difference between guessing at a bug and looking straight at one.

## Starter

Make `exercise-03-script-vs-repl.py` with this content and fill in the
marked spots:

```python
"""exercise-03-script-vs-repl.py — one file, two ways to run it."""

SIGNUPS: list[str] = ["Ada", "Grace", "Katherine", "Dorothy", "Mary"]


def initials(names: list[str]) -> str:
    """Return each name's first letter, joined by single spaces."""
    # TODO: "Ada", "Grace" -> "A G". Empty list -> "".
    raise NotImplementedError


def longest(names: list[str]) -> str:
    """Return the longest name. Ties go to the earliest one in the list."""
    # TODO: measure length, do not sort alphabetically. Empty list -> "".
    raise NotImplementedError


len(SIGNUPS)  # TODO: this prints nothing. Say why in a comment on this line.


if __name__ == "__main__":
    print(f"Signups: {len(SIGNUPS)}")
    print(f"Initials: {initials(SIGNUPS)}")
    print(f"Longest name: {longest(SIGNUPS)}")
    print(f"Running as: {__name__!r}")
```


**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/exercises/exercise-03-script-vs-repl.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `initials(SIGNUPS)` returns exactly `"A G K D M"` — one space between
   letters, and no space hanging off the end.
2. `longest(SIGNUPS)` returns `"Katherine"`, and
   `longest(["Ana", "Bob", "Cyd"])` returns `"Ana"`. All three of those
   are three letters long, and the rule is that the earliest one wins.
3. Both functions return `""` for an empty list instead of raising.
4. Run the file both ways and check that the four printed lines are
   identical, character for character, between the two runs.
5. Keep the bare `len(SIGNUPS)` line, with your explanation beside it.
6. At the bottom of the file, answer three questions in comments: what
   survives a plain run, what survives a `-i` run, and whether a name you
   add at the `>>>` prompt shows up the next time you run the script.

## Constraints

- **Use `max(names, key=len)`, not `sorted(...)`.** You want one item, and
  sorting arranges all of them just to get it. Worse than slow, it is
  wrong: `sorted(SIGNUPS)[-1]` and `max(SIGNUPS)` both hand back `'Mary'`,
  the alphabetically last name, not the longest. That answer raises no
  error at all, which makes it the most dangerous kind of wrong.
- **Build the initials with `" ".join(...)`, not by adding strings in a
  loop.** The hand-rolled loop version nearly always leaves a space
  dangling off the end, and a trailing space is invisible right up until
  something compares your string to the expected one.
- **Do not edit the file while a `python -i` session is open on it.** The
  session read the file once when it started and never looks at the disk
  again. Change the file, retype the call, get the old behaviour, and lose
  twenty minutes to a bug you already fixed. Exit, then re-run.
- **Run both versions in a terminal you can see.** Your editor's run
  button usually drops the `-i` and shuts the window on exit, hiding the
  exact behaviour this exercise is about.

## Expected output

An ordinary run does the work and exits. Real output, captured on CPython
3.13.2:

```text
$ python exercise-03-script-vs-repl.py
Signups: 5
Initials: A G K D M
Longest name: Katherine
Running as: '__main__'
```

Add `-i` and you get those same four lines, then a prompt instead of an
exit — and no version banner, because Python only prints the banner when
you start it with nothing to run. Here is the whole session, including the
proof that the name you add does not survive:

```text
$ python -i exercise-03-script-vs-repl.py
Signups: 5
Initials: A G K D M
Longest name: Katherine
Running as: '__main__'
>>> SIGNUPS
['Ada', 'Grace', 'Katherine', 'Dorothy', 'Mary']
>>> SIGNUPS.append("Annie")
>>> initials(SIGNUPS)
'A G K D M A'
>>> longest(SIGNUPS)
'Katherine'
>>> max(SIGNUPS)
'Mary'
>>> len(SIGNUPS)
6
>>> exit()
$ python exercise-03-script-vs-repl.py
Signups: 5
Initials: A G K D M
Longest name: Katherine
Running as: '__main__'
```

Three things to notice. `longest` still says `Katherine`, because `Annie`
is shorter. `max` says `Mary`, because without `key=len` it compares
alphabetically. And the count is six inside the session and five again
after it — `Annie` only ever existed in that session's memory. That is
requirement 6's third question answered by experiment instead of by
argument.

## Steps

1. Switch on your Week 1 virtual environment, make the file, paste the
   starter, and fill in the two functions.
2. Run it normally. You land back at your shell prompt.
3. Run it with `-i`. You land at `>>>` instead.
4. At that prompt type `SIGNUPS`, then `initials(SIGNUPS)`, then
   `Katherine` on its own. The first two answer. The third is a
   `NameError`, because a name *inside* the list is not a name in your
   namespace — the list holds the text `"Katherine"`, it does not create a
   variable called `Katherine`.
5. Append `"Annie"`, check both functions again, then `exit()`. Re-run the
   script normally and watch the count go back to five.
6. Answer the three comment questions at the bottom, then commit.

## The Solution

```python
"""exercise-03-script-vs-repl-solution.py — one file, two ways to run it."""

SIGNUPS: list[str] = ["Ada", "Grace", "Katherine", "Dorothy", "Mary"]


def initials(names: list[str]) -> str:
    """Return each name's first letter, joined by single spaces."""
    return " ".join(name[0] for name in names)


def longest(names: list[str]) -> str:
    """Return the longest name. Ties go to the earliest one in the list."""
    if not names:
        return ""
    return max(names, key=len)


len(SIGNUPS)  # Value computed, then discarded; only the REPL echoes results.


if __name__ == "__main__":
    print(f"Signups: {len(SIGNUPS)}")
    print(f"Initials: {initials(SIGNUPS)}")
    print(f"Longest name: {longest(SIGNUPS)}")
    print(f"Running as: {__name__!r}")


# What survives a plain run?  Nothing. The interpreter exits when the last
# line finishes and every name in this file is freed with it.
# What survives a `python -i` run?  The whole module namespace: SIGNUPS,
# initials, longest, __name__ — Python drops you at >>> instead of exiting.
# Does a name appended at the >>> prompt show up in the next run?  No. The
# append changed the list object in memory, not the source file on disk,
# so a fresh run builds the same five-name list again.
```

**`" ".join(...)` puts the separator *between* the pieces, never after the
last one.** Think of the separator as glue and the list as the things
being glued. Five names need four dabs of glue, not five, and `join` knows
that. So `"A G K D M"` comes out with no space on the end and requirement
1 is satisfied without you trimming anything. Build it by hand and the
trailing space is nearly guaranteed:

```text
>>> out = ""
>>> for n in SIGNUPS:
...     out += n[0] + " "
...
>>> repr(out)
"'A G K D M '"
```

`repr()` is how you make invisible characters visible — it shows you the
quotes, so you can see the space sitting between the `M` and the closing
quote. Reach for it any time a string looks right but fails a check.

`join` is a method on the *string*, which reads backwards until you see
why: the glue is the thing that knows how to stick, and the list is what
gets stuck.

**`name[0] for name in names` is a generator expression, and it is a Week
5 tool.** Read it in an order that is not left to right:
`for name in names` is the loop, and `name[0]` is what you hand over on
each pass. The whole thing is an object that feeds those letters to `join`
one at a time. It is the same work as the `for` loop above, written as one
expression instead of three statements. If it reads as noise today, write
the loop version — `result = []`, `result.append(name[0])` inside the
loop, `" ".join(result)` at the end — and move on. That is a completely
acceptable Week 1 answer and does the same job.
[Week 5, Lecture 3](../../week-05-data-structures/lecture-notes/03-comprehensions-and-big-o.md)
teaches this properly.

**`max(names, key=len)` measures; `max(names)` compares.** This is the
constraint worth understanding, because getting it wrong raises no error:

```text
>>> max(SIGNUPS)
'Mary'
>>> sorted(SIGNUPS)[-1]
'Mary'
>>> max(SIGNUPS, key=len)
'Katherine'
```

Without `key`, `max` compares the names themselves, and text compares
alphabetically, so `Mary` wins on its `M`. With `key=len`, `max` runs
`len` on each name, compares *those numbers*, and hands back the original
name that produced the biggest one. A wrong answer that raises an
exception costs you five minutes. A wrong answer that returns a
believable name costs you however long it takes to notice.

**Ties go to the earliest, for free.** `max` keeps whatever it is holding
and only swaps when it finds something *strictly* bigger, so the first of
several equal-length names is never bumped. `longest(["Ana", "Bob",
"Cyd"])` returns `'Ana'` and you never wrote a rule for it. Worth checking
rather than assuming, which is why requirement 2 names that case.

**The empty guard is on `longest` and not on `initials`.** `max([])` has
nothing to hand back and says so. `" ".join([])` has a perfectly good
answer — the empty string. So `longest` needs `if not names: return ""`
and `initials` does not. A guard you do not need is not free; it is a line
the next reader has to check.

**The bare `len(SIGNUPS)` line is the whole exercise in one line.** Python
works out `5` and then throws it away, because in a script nothing shows
a value unless you call `print()`. Type that identical line at a `>>>`
prompt and `5` appears. **Same code, same value, different treatment of
the result.** Every "why does my script print nothing" question a beginner
asks is this one.

**`{__name__!r}` prints `'__main__'` with the quotes on.** `!r` inside an
f-string asks for `repr()` instead of the plain text. For a string those
differ by exactly the quotation marks, and here the quotes are the
information: they tell you `__main__` is a *piece of text*, not a keyword.
`__name__` is an ordinary variable that Python fills in for you, and the
guard is an ordinary comparison. Nothing magic, just a convention with a
lot of underscores.

**No banner under `-i`.** Bare `python` prints the version banner because
it has nothing else to do. `python -i script.py` has a file to run, so it
runs it first and drops you at the prompt with no banner. If you see a
banner, you started a bare REPL and your script never ran.

## Run it

Copy the worked answer on this page into `exercise-03-script-vs-repl.py` and run it:

```bash
python exercise-03-script-vs-repl.py
```

Then run the same file the other way, `python -i exercise-03-script-vs-repl.py`,
and compare. Same four lines, then a `>>>` prompt with everything loaded.

## Common bugs to catch

- **`NameError: name 'SIGNUPS' is not defined` at the prompt.** You typed
  bare `python` and expected your file's names to be there. A fresh REPL
  knows nothing about any file. Look for the banner: banner means bare
  REPL, no banner means your script ran. Use
  `python -i exercise-03-script-vs-repl.py`.

- **`AttributeError: 'list' object has no attribute 'join'`.** You wrote
  `SIGNUPS.join(" ")`:

  ```text
  >>> SIGNUPS.join(" ")
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
      SIGNUPS.join(" ")
      ^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'join'
  ```

  The two are the wrong way round. It is `separator.join(items)` —
  `" ".join(SIGNUPS)`. Everyone writes it backwards at least once.

- **`TypeError: str.join() takes exactly one argument (2 given)`.** You
  wrote `" ".join("A", "G")`:

  ```text
  >>> " ".join("A", "G")
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
      " ".join("A", "G")
      ~~~~~~~~^^^^^^^^^^
  TypeError: str.join() takes exactly one argument (2 given)
  ```

  `join` takes one list, not loose arguments. Wrap them:
  `" ".join(["A", "G"])`.

- **`ValueError: max() iterable argument is empty`.** `max([])` was handed
  nothing:

  ```text
  >>> max([])
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
      max([])
      ~~~^^^^
  ValueError: max() iterable argument is empty
  ```

  On older interpreters the same situation reads
  `ValueError: max() arg is an empty sequence`. CPython reworded it; both
  mean one thing, which is that `max` refuses to guess. If your terminal
  shows one wording and this page shows the other, nothing is wrong —
  check `python -V`. Guard the empty list before you call it, as `longest`
  does.

- **`IndexError: string index out of range`.** A blank entry got into the
  list and `name[0]` had nothing to reach for. The exercise tells you to
  trigger this one deliberately:

  ```text
  >>> initials(["Ada", ""])
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
      initials(["Ada", ""])
      ~~~~~~~~^^^^^^^^^^^^^
    File "exercise-03-script-vs-repl.py", line 8, in initials
      return " ".join(name[0] for name in names)
             ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "exercise-03-script-vs-repl.py", line 8, in <genexpr>
      return " ".join(name[0] for name in names)
                      ~~~~^^^
  IndexError: string index out of range
  ```

  `""` has no character at position 0. Note the frame labelled
  `<genexpr>`, which is how you can tell the failure happened inside the
  generator expression and not in the `join`. If you want the function to
  survive blank entries, filter them:
  `" ".join(name[0] for name in names if name)`. The solution above
  deliberately does not, so this error stays reproducible.

- **`SyntaxError: invalid syntax` on
  `import exercise-03-script-vs-repl`.** Python reads those hyphens as
  subtraction:

  ```text
  >>> import exercise-03-script-vs-repl
    File "<stdin>", line 1
      import exercise-03-script-vs-repl
                     ^
  SyntaxError: invalid syntax
  ```

  A module name has to be a valid Python name, and `-` is the minus sign.
  That is precisely why `-i` is how you load a hyphenated file: `-i` takes
  a *path*, not a module name. If you want it importable, call it
  `signups.py`.

- **The terminal seems to hang after `-i`, or your edits seem ignored.**
  It is not hung, it is waiting at `>>>`. Leave with `exit()`, Ctrl+D, or
  Ctrl+Z then Enter on Windows. And the session read the file once at
  startup, so edits need a fresh run. There is no reload.

## Under the hood

<details>
<summary>Under the hood — why python -i leaves the script's names bound</summary>

Here is the thing that makes `-i` feel like magic, and the reason it is
not.

When Python runs `python script.py`, it does not put your script in some
special script-shaped container. It creates an ordinary module called
`__main__`, gives that module a dictionary to keep its names in, and
executes your file's code with that dictionary as its global namespace.
`SIGNUPS`, `initials` and `longest` are keys in that dictionary.

When Python runs `python`, with no file, it makes the *same* `__main__`
module with the *same* kind of dictionary, and then reads lines from you
and executes each one against it.

`-i` simply does both, in that order. Run the file into `__main__`'s
dictionary; then, instead of exiting, start reading lines and execute them
against that same dictionary. Nothing is transferred, imported, or
restored, because there was only ever one namespace and it never went
away.

That is also why `-i` gives you a prompt *even when the script crashed*.
The traceback prints, the interpreter declines to exit, and the dictionary
still holds every name that got bound before the crash — which is exactly
the state you want to inspect. Try it: put a `raise NotImplementedError`
back into `initials` and run it under `-i`.

```text
$ python -i exercise-03-script-vs-repl.py
Signups: 5
Traceback (most recent call last):
  File "exercise-03-script-vs-repl.py", line 23, in <module>
    print(f"Initials: {initials(SIGNUPS)}")
                       ~~~~~~~~^^^^^^^^^
  File "exercise-03-script-vs-repl.py", line 8, in initials
    raise NotImplementedError
NotImplementedError
>>> SIGNUPS
['Ada', 'Grace', 'Katherine', 'Dorothy', 'Mary']
```

The program crashed **and you still have a prompt**, standing exactly
where it broke. Under a plain `python` you would get the traceback and
your shell back, and to look at `SIGNUPS` you would have to add a
`print()` and run the whole thing again.

`-i` is not a special flag with special powers. It is one boolean the
interpreter checks before it shuts down, and you can see it as data:
`sys.flags.inspect` is `1` under `-i` and `0` without it.

</details>

<details>
<summary>Under the hood — __main__ is a role, not a filename</summary>

`__main__` is the name Python gives to *whatever it was told to run*. Not
to a file — to the entry point, whatever shape it came in.

```bash
python -c "print(__name__)"
```

```text
__main__
```

That is not a file at all, and it still calls itself `__main__`. Same
answer from `python script.py`, from `python -m package`, and from the
bare interactive prompt. Meanwhile a module you *import* gets its own
name: inside `signups.py`, `__name__` is `'signups'`.

That is the entire mechanism behind the guard, and it is why the guard
works identically in all those cases. Try it directly. Copy the file to
`signups.py` — no hyphens, so it is importable — and load it as a module
instead of running it:

```text
$ python -i -c "import signups"
>>> SIGNUPS
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    SIGNUPS
NameError: name 'SIGNUPS' is not defined
>>> signups.SIGNUPS
['Ada', 'Grace', 'Katherine', 'Dorothy', 'Mary']
>>> signups.longest(signups.SIGNUPS)
'Katherine'
>>> __name__
'__main__'
```

Two things changed and both matter.

The names now live *under* `signups.` instead of at the top level.
Importing creates a namespace and hangs it off a variable; running a file
does not. So bare `SIGNUPS` is a `NameError`.

And **the four print lines did not appear**. Inside `signups.py`,
`__name__` is `'signups'`, so `__name__ == "__main__"` is false and the
printing never runs. Meanwhile `__name__` at the prompt is `'__main__'`,
because the prompt is the thing Python was told to run. That is the guard
doing its job, demonstrated rather than described.

There is also `PYTHONINSPECT=1`, an environment variable that switches on
the same flag as `-i` without you typing it. Useful when something else is
building the command line for you. A menace if you forget to unset it,
because every script you run for the rest of that terminal session will
trap you at a prompt.

</details>

<details>
<summary>Under the hood — expression statements, and where the value actually goes</summary>

The bare `len(SIGNUPS)` line is called an **expression statement**: an
expression sitting on a line by itself, with nobody catching the result.

Python compiles it to bytecode — the small numbered steps the interpreter
actually walks through — and that bytecode computes the value and then
throws it away. The `dis` module lets you read those steps. A script is
compiled in what Python calls `"exec"` mode:

```text
>>> import dis
>>> dis.dis(compile("len(x)", "<s>", "exec"))
  0           RESUME                   0

  1           LOAD_NAME                0 (len)
              PUSH_NULL
              LOAD_NAME                1 (x)
              CALL                     1
              POP_TOP
              RETURN_CONST             0 (None)
```

`POP_TOP` is the throwing-away. The value was worked out, put down, and
dropped.

Now compile the identical source the way the prompt does, in `"single"`
mode:

```text
>>> dis.dis(compile("len(x)", "<s>", "single"))
  0           RESUME                   0

  1           LOAD_NAME                0 (len)
              PUSH_NULL
              LOAD_NAME                1 (x)
              CALL                     1
              CALL_INTRINSIC_1         1 (INTRINSIC_PRINT)
              POP_TOP
              RETURN_CONST             0 (None)
```

One extra instruction, and that is the entire difference.
`INTRINSIC_PRINT` hands the value to `sys.displayhook`, which is the
function that prints it and binds it to `_`. Then `POP_TOP` throws it away
just like before.

That is the honest, complete answer to "why does my script print nothing".
It is not that scripts are quieter. It is that the prompt compiles your
line with one extra instruction on the end, and `print()` is how you ask
for that instruction yourself.

`sys.displayhook` skips `None`, which is why `print("hi")` shows `hi` and
not `hi` followed by `None`.

</details>

## Acceptance checklist

- [ ] The script runs both ways with no traceback.
- [ ] The four printed lines are identical under `python` and `python -i`.
- [ ] `initials(SIGNUPS)` is `"A G K D M"` with no trailing space — check it with `repr()`.
- [ ] `longest(["Ana", "Bob", "Cyd"])` returns `"Ana"`.
- [ ] Both functions return `""` for an empty list.
- [ ] The three questions at the bottom are answered in comments.
- [ ] The file is committed to Git with a message like `Add Week 1 exercise 3: script vs REPL`.

## Stretch

- Run `python -c "print(__name__)"` and compare it to the script's fourth
  line. Both say `__main__`, which is your first hint that `__main__`
  means "whatever Python was told to run", not "a file".
- Set `PYTHONINSPECT=1` and run the script without `-i`. You get the same
  interactive prompt. Then unset it, or every script you run for the rest
  of the day will trap you at `>>>`.
- Copy the file to `signups.py` — no hyphens — and try
  `python -i -c "import signups"`. The names now live under `signups.`
  instead of at the top level, and the four print lines do not appear at
  all. That is the difference between running a file and importing one.

That is Week 1's exercises done. Take the training wheels off in
[the Week 1 challenges](../challenges/README.md).
