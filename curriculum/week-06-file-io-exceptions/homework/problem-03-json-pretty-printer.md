# Homework Problem 3 — JSON Pretty-Printer

> **Topic:** reformatting a JSON file, and failing on a broken one in exactly one line
> **Lecture:** [Lecture 02 — CSV and JSON](../lecture-notes/02-csv-and-json.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** an exception is not just a crash. It is an object carrying facts, and `json.JSONDecodeError` carries the line, the column and the parser's own explanation. This problem is where you stop printing "something went wrong" and start printing what actually did.

## The Brief

Somebody hands you a JSON file that is all on one line, with the keys in
whatever order they came out of a program. You want it readable: two
spaces of indentation, keys in alphabetical order.

```bash
python json_pretty.py messy.json clean.json
```

Nothing prints. The file is written. Silence is what a well-behaved tool
sounds like when it succeeds.

Now the interesting half. The input might not be valid JSON at all. When
that happens your tool prints **exactly one** line and stops:

```text
ERROR  bad.json:1:17  Illegal trailing comma before end of object
```

Four facts in one line: the file, the line number, the column number,
and what the parser objected to. Then the process exits with code `1`,
because that is the part a script checks.

Not a traceback. A traceback is twelve lines of Python internals aimed
at the person who wrote the tool. This message is aimed at the person
who has a broken file.

And `clean.json` — or whatever output file was named — must be
**untouched**. It might be a good file from this morning's run.

## Starter

Save this as `json_pretty.py` in your `homework/` folder and fill in the
`TODO`s. It runs as pasted — it copies valid JSON through unformatted and
crashes with a traceback on anything else:

```python
"""Rewrite a JSON file with two-space indentation and sorted keys."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

log = logging.getLogger("json_pretty")


def pretty(src: Path, dst: Path) -> int:
    """Rewrite `src` into `dst`, pretty-printed. Return a process exit code.

    Args:
        src: The JSON file to read.
        dst: The file to write the pretty-printed version to.

    Returns:
        0 on success, 1 if the input could not be read or parsed.
    """
    # TODO: wrap this in try/except and handle FileNotFoundError,
    #       UnicodeDecodeError and json.JSONDecodeError, returning 1
    data = json.loads(src.read_text(encoding="utf-8"))

    # TODO: pass indent=2 and sort_keys=True
    text = json.dumps(data)
    dst.write_text(text + "\n", encoding="utf-8")
    return 0


def main(argv: list[str]) -> int:
    """Pretty-print the files named in `argv`."""
    logging.basicConfig(format="%(levelname)s  %(message)s")
    if len(argv) != 2:
        print("usage: json_pretty.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    return pretty(Path(argv[0]), Path(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Make one good input and one broken one to try it on:

```bash
python -c "
from pathlib import Path
Path('messy.json').write_text('{\"name\":\"Alice\",\"age\":30}\n', encoding='utf-8')
Path('bad.json').write_text('{\"name\": \"Alice\",}\n', encoding='utf-8')
"
python json_pretty.py messy.json clean.json
python json_pretty.py bad.json out.json
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C1-Code-Crunch-Convos/curriculum/week-06-file-io-exceptions/homework/problem-03-json-pretty-printer.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. The input path is `sys.argv[1]` and the output path is `sys.argv[2]`.
2. On success the output is written with `indent=2` and
   `sort_keys=True`, and nothing is printed.
3. Invalid JSON prints exactly one line containing the path, the line
   number, the column number and the parser's message.
4. That failure exits with code `1`.
5. The output file is not created or modified when the input fails to
   parse.
6. The line and message come from the exception's own attributes, never
   from a string you typed.
7. Every function has type hints and a docstring.

## Constraints

- **Parse before you open the output.** `json.loads` runs on the text
  you read; only after it succeeds does anything get written. Open the
  output first and `"w"` has already emptied it before the parser has
  seen a single character.
- **Catch `json.JSONDecodeError`, not `ValueError`.**
  `JSONDecodeError` *is* a `ValueError`, so the broad catch does match —
  and it also matches every other `ValueError` from inside the same
  `try`, and then `e.lineno` does not exist and your error handler
  raises `AttributeError` while handling an error.
- **Read `e.lineno`, `e.colno` and `e.msg` off the exception.** Type the
  message yourself and your tool reports "Expecting property name
  enclosed in double quotes" for an unterminated string, a bad escape,
  and a stray bracket. Reading the attributes gives a correct message
  for every syntax error there is.
- **Return the exit code, do not let the exception escape.** A traceback
  happens to exit non-zero, but with eleven lines of noise and by
  accident rather than on purpose.
- **`sort_keys=True` is not only about looks.** It makes the output
  deterministic, so the same input always produces the same bytes. That
  is what turns this script into something you can run in a commit hook.

## Expected output

The shipped answer runs its own demo when you give it no arguments, so
it works from a clean checkout. It writes one good and one broken JSON
file into a scratch folder, pretty-prints the good one and shows the
result, then tries the broken one:

```bash
$ python problem-03-json-pretty-printer.py
```

```text
messy.json -> clean.json: exit 0
{
  "active": true,
  "age": 30,
  "manager": null,
  "name": "Alice",
  "tags": [
    "b",
    "a"
  ]
}
bad.json -> out.json: exit 1
out.json exists: False
```

Two things in there are worth stopping on.

**The keys are alphabetical but the array is not.** `"b"` still comes
before `"a"` inside `tags`. `sort_keys` sorts the keys of objects and
never the elements of arrays — which is correct, because a JSON array is
ordered and reordering it would change the data.

**`out.json exists: False`.** The broken input cost nothing. No file was
created, so nothing could have been destroyed.

The diagnostic line itself went to stderr:

```console
ERROR  bad.json:1:17  Illegal trailing comma before end of object
```

Count them if you like — `python json_pretty.py bad.json out.json 2>&1 | wc -l` prints `1`.

## Steps

1. Activate your Week 6 environment and `cd` into your `homework/`
   folder.
2. Save the Starter as `json_pretty.py`. Make the two sample inputs shown
   under **Starter** and run it on `messy.json`. It writes `clean.json`,
   still on one line.
3. Add `indent=2, sort_keys=True` to the `json.dumps` call. Run it again
   and look at `clean.json`. That is half the problem done.
4. Run it on `bad.json`. You get a traceback ending in
   `json.decoder.JSONDecodeError`. Read the last line carefully — the
   line and column are already in there.
5. In the REPL, catch the exception and look at what it carries:

   ```bash
   python -c "
   import json
   try:
       json.loads('{\"name\": \"Alice\",}')
   except json.JSONDecodeError as e:
       print(e.lineno, e.colno, e.msg)
   "
   ```

6. Wrap the parse in `try` and add the three `except` clauses. The
   `JSONDecodeError` one formats those attributes:
   `log.error("%s:%d:%d  %s", src, e.lineno, e.colno, e.msg)` and
   returns 1.
7. Run it on `bad.json` again. One line, no traceback. Check the exit
   code and check the output file was never made:

   ```bash
   python json_pretty.py bad.json out.json
   echo "exit=$?"
   ls out.json
   ```

8. Check that the tool is idempotent — running it on its own output
   changes nothing:

   ```bash
   python json_pretty.py clean.json clean2.json
   python json_pretty.py clean2.json clean3.json
   diff clean2.json clean3.json && echo "stable"
   ```

9. Compare against **The Solution**, work down the acceptance checklist,
   and commit: `git add homework/json_pretty.py` then
   `git commit -m "Week 6 homework: JSON pretty-printer"`.

## The Solution

```python
"""Homework 3 — JSON pretty-printer.

Reads a JSON document and rewrites it with indent=2 and sorted keys. On a
parse error it emits exactly one diagnostic line and exits 1, leaving the
output file untouched.

    python json_pretty.py messy.json clean.json

Run it with no arguments and it builds its own good and bad input files in a
scratch folder first, so the download works from a clean checkout with nothing
set up.

Save your own copy as ``json_pretty.py`` in your ``homework/`` folder.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
from pathlib import Path

# "%(levelname)s  %(message)s" -- deliberately NOT the %(levelname)-8s format
# used elsewhere this week, because the spec's example line is
#     ERROR  bad.json:1:17  Expecting property name enclosed in double quotes
# with exactly two spaces after the level.
log = logging.getLogger("json_pretty")


def pretty(src: Path, dst: Path) -> int:
    """Rewrite *src* into *dst*, pretty-printed. Return a process exit code.

    Parsing happens in full before *dst* is opened, so a bad input never
    truncates a good output file.

    Args:
        src: The JSON file to read.
        dst: The file to write the pretty-printed version to.

    Returns:
        0 on success, 1 if the input could not be read or parsed.
    """
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        log.error("%s: no such file", src)
        return 1
    except UnicodeDecodeError as e:
        log.error("%s: not valid UTF-8 (%s)", src, e.reason)
        return 1
    except json.JSONDecodeError as e:
        log.error("%s:%d:%d  %s", src, e.lineno, e.colno, e.msg)
        return 1

    text = json.dumps(data, indent=2, sort_keys=True)
    dst.write_text(text + "\n", encoding="utf-8")
    return 0


def _demo() -> int:
    """Pretty-print one good file and one broken one in a scratch folder.

    The scratch folder is a temporary directory this function makes and
    deletes, so the demo needs nothing placed by hand and leaves nothing
    behind. It changes into that folder first so the diagnostic line names
    ``bad.json`` rather than a long temporary path.

    Returns:
        Always 0. Both demonstrated outcomes are the intended ones.
    """
    home = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="json_pretty_") as scratch:
        try:
            os.chdir(scratch)
            Path("messy.json").write_text(
                '{"name":"Alice","tags":["b","a"],"active":true,'
                '"age":30,"manager":null}\n',
                encoding="utf-8",
            )
            Path("bad.json").write_text('{"name": "Alice",}\n', encoding="utf-8")

            code = pretty(Path("messy.json"), Path("clean.json"))
            print(f"messy.json -> clean.json: exit {code}")
            print(Path("clean.json").read_text(encoding="utf-8"), end="")

            code = pretty(Path("bad.json"), Path("out.json"))
            print(f"bad.json -> out.json: exit {code}")
            print(f"out.json exists: {Path('out.json').exists()}")
        finally:
            os.chdir(home)
    return 0


def main(argv: list[str]) -> int:
    """Pretty-print the files named in *argv*, or run the demo when empty.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The process exit code.
    """
    logging.basicConfig(format="%(levelname)s  %(message)s")
    if not argv:
        return _demo()
    if len(argv) != 2:
        print("usage: json_pretty.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    return pretty(Path(argv[0]), Path(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**Why it works.**

**The order `read_text` → `loads` → `dumps` → `write_text` is the
answer.** Everything that can fail happens before anything is written.
The brief's own example runs `python json_pretty.py bad.json out.json`,
and it is entirely plausible that `out.json` is a good file from an
earlier run. Parsing first means a bad input costs nothing at all.

**Three `except` clauses, because there are three different things that
go wrong.** `FileNotFoundError` and `UnicodeDecodeError` are about
getting the text at all. `json.JSONDecodeError` is about what the text
says. Writing them separately is what lets each one produce a message
that actually helps. Two of the three are children of things you might
be tempted to catch broadly — `OSError` and `ValueError` — and doing
that would collapse all three messages into one useless one.

**`e.lineno`, `e.colno` and `e.msg` are why the exception exists.**
`json.JSONDecodeError` carries the position and the parser's own
explanation as attributes, precisely so that you can format them the way
your tool wants. Reading them gives a correct message for every syntax
error, not just the one you happened to test.

**The `logging` format is chosen to match the required line.**
`format="%(levelname)s  %(message)s"` produces `ERROR`, two spaces, then
the message. That is not the `%(levelname)-8s %(name)s  %(message)s`
format the rest of this week uses — the brief's example has two spaces
after `ERROR` and no logger name, so the format follows the brief.

**Returning the code keeps the exception handled.**
`raise SystemExit(main(...))` turns the returned integer into the
process's exit code. `sys.exit(1)` inside the `except` works just as
well. What does not work is re-raising, because then the user gets the
traceback the brief forbade.

**The demo builds its own data.** `_demo` makes a temporary folder,
changes into it, writes both inputs, runs both cases, and changes back
out before the folder is deleted. Changing directory first is also why
the diagnostic says `bad.json` and not a long temporary path.

## Run it

Copy the worked answer on this page into `problem-03-json-pretty-printer.py` and run it:
and run it:

```bash
python problem-03-json-pretty-printer.py
```

With no arguments it creates its own good and broken JSON files in a
temporary folder and runs both cases, so it works anywhere with nothing
set up. Give it two paths and it does the real job:

```bash
python problem-03-json-pretty-printer.py messy.json clean.json
```

Save your own copy as `json_pretty.py` in your homework folder, and
commit that one. The longer download name is there so it cannot
overwrite your work.

## Common bugs to catch

- **Opening the output file before parsing.** This destroys data, in
  silence, and it is the mistake this problem exists to prevent:

  ```python
  with dst.open("w", encoding="utf-8") as out:          # opened too early
      data = json.loads(src.read_text(encoding="utf-8"))
      json.dump(data, out, indent=2, sort_keys=True)
  ```

  ```text
  precious.json before: 19 bytes
    ...
  json.decoder.JSONDecodeError: Illegal trailing comma before end of object: line 1 column 17 (char 16)
  precious.json after:  0 bytes
  ```

  `"w"` truncated the output on the way *in*, before a byte of JSON was
  parsed. The file is gone and the traceback does not mention it. Do
  that once on purpose, on a file you do not care about, and you will
  never write it again.
- **`except ValueError:` instead of `except json.JSONDecodeError:`.**
  It catches, because `JSONDecodeError` is a `ValueError`. It also
  catches every other `ValueError` in the same `try`, and then:

  ```text
  AttributeError: 'ValueError' object has no attribute 'lineno'
  ```

  An `AttributeError` raised inside your own error handler is a
  miserable thing to debug.
- **Printing the error and forgetting the exit code.**

  ```python
  except json.JSONDecodeError as e:
      print(f"ERROR  {src}:{e.lineno}:{e.colno}  {e.msg}")
  ```

  Looks right, exits `0`. Every script and every CI step that checks the
  exit status now believes the file was formatted.
- **Calling `json.dumps` on the raw text instead of the parsed object.**

  ```text
  >>> json.dumps('{"a":1}')
  '"{\\"a\\":1}"'
  ```

  That is a JSON *string* containing your document, escaped. If your
  output is one long quoted line full of backslashes, you skipped the
  `loads`.
- **Hard-coding the parser's message so the example matches.** Then a
  file with an unterminated string reports a trailing comma. The whole
  value of the tool is that the message is true.

## Under the hood

<details>
<summary>Under the hood — why a bare except: hides bugs, and what to catch instead</summary>

`except:` with nothing after it catches **everything**. Not just the
failure you were thinking of. Everything.

```python
try:
    data = json.loads(src.read_text(encoding="utf-8"))
except:                      # never write this
    print("could not read the file")
    return 1
```

Three separate problems live in those two lines.

**It catches your own bugs and calls them the user's.** Misspell
`src` as `scr` inside that `try` and you get a `NameError`. The handler
reports "could not read the file", so you go and check the file. The
file is fine. You check its permissions. You check its encoding. The bug
was on the line above, and your error handler is the reason you cannot
see it.

**It catches things that are not errors at all.** `KeyboardInterrupt`
and `SystemExit` do not inherit from `Exception` — they inherit from
`BaseException`, one level up — precisely so that ordinary handling does
not swallow them:

```text
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── OSError
      ├── ValueError
      └── ... everything you normally catch
```

A bare `except:` sits above that split. Press Ctrl-C during a long loop
wrapped in one and the interrupt is caught, discarded, and the loop
continues. You have written a program you cannot stop.

**It throws away the information.** `except:` has no `as e`, so there is
nothing left to inspect, log, or re-raise.

The ladder, from worst to best:

| What you write | What it catches | Use it |
|---|---|---|
| `except:` | absolutely everything, Ctrl-C included | never |
| `except BaseException:` | the same, but at least on purpose | almost never |
| `except Exception:` | every ordinary error, including your bugs | top-level handlers only |
| `except (OSError, UnicodeDecodeError):` | the failures you named | this |
| `except json.JSONDecodeError as e:` | one failure, with its data | best when it fits |

The rule that makes the choice for you: **catch the narrowest type that
you can actually do something about.** If your handler's answer to a
`NameError` would be wrong, then a clause that can catch `NameError` is
too wide.

There is one honest use for `except Exception:` — the outermost handler
of a long-running program, whose job is to log the failure with its
traceback and carry on serving the next request:

```python
except Exception:
    log.exception("request failed")   # logs the full traceback
```

`log.exception` is the part that makes it defensible. It keeps the
information instead of destroying it. A handler that catches broadly and
prints a friendly sentence has thrown away the only evidence anybody
had.

</details>

<details>
<summary>Under the hood — what an exception object carries besides its message</summary>

`raise` does not throw a string. It throws an **object**, and the useful
ones carry structured facts.

```text
>>> import json
>>> try:
...     json.loads('{"name": "Alice",}')
... except json.JSONDecodeError as e:
...     print(type(e).__mro__)
...     print(e.msg, e.lineno, e.colno, e.pos)
...
(<class 'json.decoder.JSONDecodeError'>, <class 'ValueError'>, <class 'Exception'>, <class 'BaseException'>, <class 'object'>)
Illegal trailing comma before end of object 1 17 16
```

`.pos` is the character offset from the start of the document;
`.lineno` and `.colno` are that same position expressed the way an
editor shows it. `.doc` holds the whole input, which is how you would
print the offending line with a caret under it if you wanted to.

Other exceptions carry their own:

| Exception | Useful attributes |
|---|---|
| `OSError` and its children | `.errno`, `.strerror`, `.filename` |
| `UnicodeDecodeError` | `.encoding`, `.object`, `.start`, `.end`, `.reason` |
| `subprocess.CalledProcessError` | `.returncode`, `.output` |
| any exception | `.args`, `__traceback__`, `__cause__`, `__context__` |

That last row is why `except FileNotFoundError as e: print(e.filename)`
prints the path without any string-chopping.

**A version note you should read.** The brief's example line says:

```text
ERROR  bad.json:1:17  Expecting property name enclosed in double quotes
```

On CPython 3.13 the same input reports:

```text
ERROR  bad.json:1:17  Illegal trailing comma before end of object
```

The line and column are identical. Only the wording changed: 3.13
rewrote the `json` module's messages to name the actual problem instead
of describing what the parser wanted to see next. Your code is right on
both versions **because it reads `e.msg` instead of printing a sentence
you typed**. That is the whole argument for reading attributes off the
exception, demonstrated by the language changing underneath the example.

</details>

## Acceptance checklist

- [ ] `python json_pretty.py messy.json clean.json` prints nothing and
      exits 0.
- [ ] `clean.json` is indented two spaces with its object keys in
      alphabetical order.
- [ ] Arrays inside it keep their original order.
- [ ] `python json_pretty.py bad.json out.json` prints exactly one line.
- [ ] That line contains the path, the line number, the column number
      and the parser's message.
- [ ] That run exits with code 1.
- [ ] `out.json` does not exist afterwards.
- [ ] The message comes from `e.msg`, not from a string in your source.
- [ ] `except json.JSONDecodeError`, not `except ValueError` and not a
      bare `except:`.
- [ ] Every function has type hints and a docstring.
- [ ] Committed with a message like
      `Week 6 homework: JSON pretty-printer`.

## Stretch

- **Print the offending line with a caret under it.** `e.doc` holds the
  whole input and `e.colno` says where to point. Three lines of code and
  the error message becomes something you can act on without opening an
  editor.
- **Format in place.** Allow one argument, meaning "rewrite this file".
  Read it all, parse it, and only then write back over it. Then use
  problem 6's atomic write so that a crash cannot leave the file
  half-formatted.
- **Add `--check`.** Do not write anything; exit 0 if the file is
  already formatted and 1 if it is not. That is exactly what a commit
  hook needs, and you can build it by comparing the formatted text with
  the original.
- **Keep the original key order.** Drop `sort_keys` and see what
  changes. `json.loads` gives you a plain dict, and since Python 3.7
  dicts remember insertion order, so the original order survives for
  free. Decide which of the two behaviours you would want as the
  default and write down why.
- **Handle a JSON file that is a list at the top level, or a bare
  number.** All three are valid JSON documents. Check that your tool
  does something sensible with `[1, 2, 3]` and with `42`.

Next: [Homework Problem 4 — Retry-On-Error Decorator](./problem-04-retry-on-error-decorator-preview-of-decorators.md).
