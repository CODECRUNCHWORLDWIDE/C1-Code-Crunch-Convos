# Exercise 3 — JSON Config

> **Topic:** loading a JSON file into a dict, changing it, and saving it back
> **Lecture:** [02 — CSV and JSON](../lecture-notes/02-csv-and-json.md)
> **Difficulty:** Easy
> **Target time:** 20 minutes
> **Why this one:** load, change, save is how nearly every settings file, cache and saved-game in your career gets edited by a program. The lecture shows you the three lines. This exercise makes you deal with the two things the lecture skipped: making the output the same every time, and making a second run do nothing at all.

## The Brief

The community site reads its settings from a JSON file. Right now comments are
switched off, three chapters are listed, and uploads are capped at 5 MB. The
org has voted to turn comments on, add the new Nairobi chapter, and raise the
cap to 10 MB.

**JSON** — JavaScript Object Notation — is a way of writing down nested data as
text. It has objects (which arrive in Python as dicts), arrays (lists),
strings, numbers, `true`, `false` and `null`. That is the entire list. It looks
very like Python and it is not Python, and the places where it differs are
where people get hurt.

You could open the file in an editor and change it by hand. You are going to
write a script instead, because next month there will be four more chapters,
and because a script can be re-run, reviewed by somebody else, and committed to
Git where it explains itself.

Two properties matter more than the edits do.

**Deterministic** means the same input always produces the same bytes out. Not
"the same information" — the same *characters*, in the same order. That is what
makes a Git diff show you the one line that changed instead of a reshuffled
file.

**Idempotent** is the longer word for "running it twice is the same as running
it once". Run your script ten times and Nairobi must appear once, not ten
times. A script you can safely re-run is a script you never have to remember
whether you already ran.

## Starter

First, the data. Create `data/site-config.json` with exactly this content:

```json
{
  "site_name": "Code Crunch Worldwide",
  "theme": "light",
  "features": {
    "newsletter": true,
    "comments": false
  },
  "chapters": ["Lagos", "Manila", "Bogota"],
  "max_upload_mb": 5
}
```

Now the code. Save this as `exercise-03-json-config.py`:

```python
"""exercise-03-json-config.py — load a JSON config, edit it, write it back.

Enables the comments feature, adds the Nairobi chapter, and raises the upload
cap. Re-running the script leaves the file unchanged.
"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "data" / "site-config.json"
NEW_MAX_UPLOAD_MB = 10


def load_config(path: Path) -> dict:
    """Read the JSON file at *path* and return it as a dict."""
    # TODO: open the file for reading and return json.load(...)
    return {}


def set_feature(config: dict, name: str, enabled: bool) -> bool:
    """Set config["features"][name] to *enabled*.

    Returns:
        True if the value changed, False if it was already correct.

    Raises:
        KeyError: if *name* is not an existing feature.
    """
    # TODO: raise KeyError when name is missing from config["features"]
    # TODO: return False when the value already equals enabled
    # TODO: otherwise set it and return True
    return False


def add_chapter(config: dict, name: str) -> bool:
    """Append *name* to config["chapters"] unless it is already listed.

    Returns:
        True if the chapter was added, False if it was already there.
    """
    # TODO: guard against duplicates, then append
    return False


def save_config(config: dict, path: Path) -> None:
    """Write *config* back to *path* as sorted, indented JSON."""
    # TODO: open for writing, json.dump with indent=2 and sort_keys=True
    # TODO: write a final "\n" so the file ends with a newline


def main() -> None:
    """Apply this month's config changes and report each one."""
    config = load_config(CONFIG_PATH)
    print(f"Loaded {len(config)} top-level keys from {CONFIG_PATH.name}")

    if set_feature(config, "comments", True):
        print("Enabled feature: comments")
    else:
        print("Feature already enabled: comments")

    for chapter in ("Nairobi", "Lagos"):
        if add_chapter(config, chapter):
            print(f"Added chapter: {chapter}")
        else:
            print(f"Chapter already listed: {chapter}")

    old_cap = config["max_upload_mb"]
    if old_cap < NEW_MAX_UPLOAD_MB:
        config["max_upload_mb"] = NEW_MAX_UPLOAD_MB
        print(f"Raised max_upload_mb from {old_cap} to {NEW_MAX_UPLOAD_MB}")
    else:
        print(f"max_upload_mb already at {old_cap}")

    save_config(config, CONFIG_PATH)
    print(f"Wrote {CONFIG_PATH.name}")


if __name__ == "__main__":
    main()
```

Four names worth knowing before you start.

**`json.load` and `json.loads`.** `load` reads from an open file. `loads` reads
from a string you already have. The `s` means string, and the same `s` runs
through `dump` and `dumps`.

**`indent=2`.** Without it, `json.dump` writes the whole thing on one line.
With it you get two-space indentation and one value per line, which is what
makes the file readable and what makes a diff show you a single changed line.

**`sort_keys=True`.** Write the keys of every object in alphabetical order
rather than in the order the dict happens to hold them.

**Mutator.** A function that changes something it was given. The three
functions in the middle of the starter are mutators, and each one returns a
`bool` saying whether it actually changed anything.

## Requirements

1. `load_config` returns a plain `dict` with five keys, so `len(config)` is `5`.
2. `set_feature(config, "comnents", True)` — note the typo — raises `KeyError`.
   It must not create a new feature. A typo that quietly adds a setting nothing
   reads is a bug you will hunt for an hour.
3. `add_chapter` appends to the existing list and keeps the order. After the
   run, `chapters` is `["Lagos", "Manila", "Bogota", "Nairobi"]` — Nairobi at
   the end, not sorted into place.
4. `save_config` writes with `indent=2` and `sort_keys=True`, and the file ends
   with a single newline character.
5. On a first run your script prints six lines, and they are the six under
   `--- first run ---` in Expected output below.
6. On a second run it prints the six "already" lines, and the file on disk is
   byte-for-byte identical to what the first run left. Not "the same settings" —
   the same bytes.

## Constraints

- **Read the file completely and close it before you open it for writing.**
  `"w"` mode empties the file to zero bytes the instant it opens. If you nest
  the writing block inside the reading block — or just open the writer too
  early — you wipe the only copy of the config you meant to edit. Read, close,
  change, write. Four verbs, in that order, forever.
- **Use `json.load(f)` with a file object, not `json.load(path)`.** `load`
  wants something with a `.read()` method, and a `Path` is a name, not an open
  file. If what you have is a string, the function is `json.loads`.
- **Never parse JSON with `eval()`.** JSON's `true`, `false` and `null` are not
  Python words, so `eval` fails on the easy files — and on a hostile one it
  runs whatever code the file contains. `json.loads` is a parser. It reads;
  it does not execute.
- **Pass `sort_keys=True` and `indent=2`.** Python dicts remember the order you
  put things in, so without sorting, the key order in your file is a record of
  the order your edits happened to run. Move two unrelated lines in `main` and
  the whole file reshuffles. Sorting throws that history away and leaves only
  the content, which is what turns a diff into a readable list of real changes.
- **Keep `chapters` a list, not a set.** A set would make removing duplicates
  free, and then `json.dump` would raise `TypeError: Object of type set is not
  JSON serializable`, because JSON has no set. Use an
  `if name not in config["chapters"]` check and keep the list.
- **Return booleans from the mutators and print in `main`.** A function that
  both changes something and announces it can never be reused by a caller who
  wants different wording, or wants to count the changes, or wants silence. The
  mutator reports what it did; the caller decides what to say about it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-03-json-config.py
--- first run ---
Loaded 5 top-level keys from site-config.json
Enabled feature: comments
Added chapter: Nairobi
Chapter already listed: Lagos
Raised max_upload_mb from 5 to 10
Wrote site-config.json

--- second run ---
Loaded 5 top-level keys from site-config.json
Feature already enabled: comments
Chapter already listed: Nairobi
Chapter already listed: Lagos
max_upload_mb already at 10
Wrote site-config.json

byte-identical after the second run: True

--- site-config.json ---
{
  "chapters": [
    "Lagos",
    "Manila",
    "Bogota",
    "Nairobi"
  ],
  "features": {
    "comments": true,
    "newsletter": true
  },
  "max_upload_mb": 10,
  "site_name": "Code Crunch Worldwide",
  "theme": "light"
}
```

Your own `exercise-03-json-config.py` prints six lines per run. The shipped
file runs the same changes twice, hashes the file in between, and prints
whether the two hashes matched — because "a second run changes nothing" is the
property this exercise is really about, and a claim you can print is better
than a claim you have to trust.

Two things to notice in the saved file. The top-level keys are alphabetical
now. And `chapters` is not, because `sort_keys` sorts the keys of every object
and never touches the contents of an array. That is correct: the order of an
array is data, and reordering it would change the meaning.

## Steps

1. Create `data/site-config.json` with the block above.
2. Copy it somewhere safe before you write any code:
   `cp data/site-config.json data/site-config.json.bak`. A mistake in
   `save_config` then costs you nothing.
3. Implement `load_config`, then check it from a REPL — open `python`, load the
   file, and print `config.keys()`.
4. Implement `set_feature` and `add_chapter`. Test the duplicate path and the
   typo path before you ever write the file.
5. Implement `save_config` last. Run the script and read the file.
6. Run the script again and diff the file against itself:
   `git diff data/site-config.json` shows nothing after the second run.
7. Now break it on purpose, so the error is one you recognise rather than one
   you fear. Add a comma after the **last** entry, so the file ends:

   ```text
     "max_upload_mb": 5,
   }
   ```

   That is a **trailing comma** — legal in Python, illegal in JSON. Run the
   script and read the message:

   ```text
   json.decoder.JSONDecodeError: Illegal trailing comma before end of object: line 9 column 21 (char 194)
   ```

   Three numbers, all useful. `line 9` and `column 21` are where to put your
   cursor. `char 194` counts from the start of the whole file.

   A version note, because this exact string changed recently. CPython 3.13
   rewrote the JSON parser's messages to name the real problem. On 3.12 and
   earlier the same file reports `Expecting property name enclosed in double
   quotes` and points at the token *after* the comma, because the older parser
   described what it was hoping to find next rather than what was wrong. Both
   sentences describe the same broken file. If you are on 3.12 you will see the
   older wording and nothing is wrong with your code.

   Then try a *doubled* comma instead — `"theme": "light",,` — and you get the
   older message even on 3.13, because that genuinely is a missing property
   name:

   ```text
   json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 3 column 20 (char 61)
   ```

   The lesson to carry into Challenge 02: read `e.msg`, `e.lineno` and `e.colno`
   off the exception object rather than matching on the sentence. The numbers
   are stable. The wording is not.

8. Put the file back the way it was and run once more to confirm it is healthy.

## The Solution

```python
"""exercise-03-json-config-solution.py — load a JSON config, edit it, write it back.

Enables the comments feature, adds the Nairobi chapter, and raises the upload
cap. Re-running the script leaves the file byte-for-byte unchanged.

The file you write yourself keeps its sample config in a ``data/`` folder next
to the script. This shipped answer builds that same ``data/`` folder inside a
throwaway temporary directory first, writing the exact config the page gives
you, so the download runs on any machine with nothing set up beforehand. It
then applies the changes twice and hashes the file in between, because
"running it twice changes nothing" is the property this exercise is really
about. Everything from ``load_config`` to ``apply_changes`` is the exercise.

Run it with::

    python exercise-03-json-config-solution.py
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

NEW_MAX_UPLOAD_MB = 10

#: The config exactly as the exercise page gives it.
SAMPLE_CONFIG = """{
  "site_name": "Code Crunch Worldwide",
  "theme": "light",
  "features": {
    "newsletter": true,
    "comments": false
  },
  "chapters": ["Lagos", "Manila", "Bogota"],
  "max_upload_mb": 5
}
"""


def load_config(path: Path) -> dict:
    """Read the JSON file at *path* and return it as a dict."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def set_feature(config: dict, name: str, enabled: bool) -> bool:
    """Set config["features"][name] to *enabled*.

    Returns:
        True if the value changed, False if it was already correct.

    Raises:
        KeyError: if *name* is not an existing feature.
    """
    features = config["features"]
    if name not in features:
        raise KeyError(name)
    if features[name] == enabled:
        return False
    features[name] = enabled
    return True


def add_chapter(config: dict, name: str) -> bool:
    """Append *name* to config["chapters"] unless it is already listed.

    Returns:
        True if the chapter was added, False if it was already there.
    """
    chapters = config["chapters"]
    if name in chapters:
        return False
    chapters.append(name)
    return True


def save_config(config: dict, path: Path) -> None:
    """Write *config* back to *path* as sorted, indented JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)
        f.write("\n")


def apply_changes(path: Path) -> None:
    """Apply this month's config changes to the file at *path*, reporting each."""
    config = load_config(path)
    print(f"Loaded {len(config)} top-level keys from {path.name}")

    if set_feature(config, "comments", True):
        print("Enabled feature: comments")
    else:
        print("Feature already enabled: comments")

    for chapter in ("Nairobi", "Lagos"):
        if add_chapter(config, chapter):
            print(f"Added chapter: {chapter}")
        else:
            print(f"Chapter already listed: {chapter}")

    old_cap = config["max_upload_mb"]
    if old_cap < NEW_MAX_UPLOAD_MB:
        config["max_upload_mb"] = NEW_MAX_UPLOAD_MB
        print(f"Raised max_upload_mb from {old_cap} to {NEW_MAX_UPLOAD_MB}")
    else:
        print(f"max_upload_mb already at {old_cap}")

    save_config(config, path)
    print(f"Wrote {path.name}")


def digest(path: Path) -> str:
    """Return the SHA-256 of the raw bytes of *path*, as hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_sample(folder: Path) -> Path:
    """Write the sample site config into *folder* and return its path."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "site-config.json"
    path.write_text(SAMPLE_CONFIG, encoding="utf-8")
    return path


def main() -> None:
    """Apply the changes twice and prove the second run changed nothing."""
    with tempfile.TemporaryDirectory() as workspace:
        config_path = build_sample(Path(workspace) / "data")

        print("--- first run ---")
        apply_changes(config_path)
        after_first = digest(config_path)

        print()
        print("--- second run ---")
        apply_changes(config_path)
        after_second = digest(config_path)

        print()
        print(f"byte-identical after the second run: {after_first == after_second}")

        print()
        print(f"--- {config_path.name} ---")
        print(config_path.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
```

**`load_config` closes the file before anything is changed.** The `with` block
inside `load_config` ends when the function returns, so by the time
`set_feature` runs there is no open handle on the config at all. That ordering
is the entire safety story here. `save_config` opens the same path in `"w"`,
which empties it — and emptying a file you have already read completely into a
dict is harmless, while emptying one you are still reading destroys it.

**The three mutators return `bool` and print nothing.** Look at what that buys
`main`: it says "Enabled feature: comments" the first time and "Feature already
enabled: comments" the second, from the same call, because the function
reported *what it did* rather than *what it was asked to do*. Separating the
decision from the announcement is why the first-run output and the second-run
output come out of identical code.

**Idempotence lives in two `if` statements and nowhere else.** `add_chapter`
checks `if name in chapters` before appending. `set_feature` checks
`if features[name] == enabled` before assigning. Neither check does anything on
the first run — both are false and the code proceeds. They exist so the
*second* run is a no-op. Notice that `chapters` is read fresh out of `config`
inside the function, so the membership test asks about the current list rather
than about some copy taken earlier.

**`raise KeyError(name)` for a typo, deliberately, instead of creating the
key.** `config["features"]["comnents"] = True` is perfectly legal Python —
dicts create keys when you assign to them — and it would give you a config with
a setting nothing reads and a feature nobody enabled. The membership check
turns a silent hours-long bug into an immediate `KeyError: 'comnents'` that
names the typo out loud.

**`sort_keys=True` makes the output a function of the data.** With it, the same
five keys always come out in the same five places, no matter what order your
edits ran in. `sort_keys` applies to every object at every depth, which is why
`features` came out with `comments` before `newsletter` even though the file
had them the other way round.

**The trailing `f.write("\n")` is a separate call because `json.dump` will not
do it.** `dump` writes the value and stops. Almost every text tool ever
written expects a file to end with a newline: Git says `\ No newline at end of
file` when it does not, and appending to such a file glues your new content
onto the end of the last line. One extra `write`, inside the same `with`, and
the file is well-formed.

**About the harness.** `SAMPLE_CONFIG`, `build_sample`, `digest` and the double
run in `main` exist so this download runs on a machine where you have created
nothing, and so the idempotence claim is demonstrated instead of asserted.
`apply_changes` is your `main` with the path passed in as an argument rather
than read from a module constant — which is the one change that makes it
callable twice.

## Run it

Copy the worked answer on this page into `exercise-03-json-config.py` and run it:

```bash
python exercise-03-json-config.py
```

It needs no `data/` folder: it writes its own copy of the config into a
temporary directory, applies the changes twice, prints the hash comparison and
the finished file, and cleans up after itself. The `-solution` in the name
keeps it from colliding with your own `exercise-03-json-config.py`.

## Common bugs to catch

- **`TypeError: Object of type set is not JSON serializable`.**

  ```text
  Traceback (most recent call last):
    File "<string>", line 3, in <module>
      json.dump({'chapters': {'Lagos','Manila'}}, sys.stdout, indent=2)
    File "...\Lib\json\encoder.py", line 180, in default
      raise TypeError(f'Object of type {o.__class__.__name__} '
                      f'is not JSON serializable')
  TypeError: Object of type set is not JSON serializable
  ```

  You reached for a `set` to prevent duplicate chapters. JSON has objects,
  arrays, strings, numbers, booleans and null, and nothing else. The nasty part
  is *when* it raises: `dump` writes as it encodes, so by the time it gives up
  it has already put the opening brace and the key into your file. Convert with
  `sorted(the_set)` before dumping, or keep the list.

- **`AttributeError: 'WindowsPath' object has no attribute 'read'`**
  (`'PosixPath'` on macOS and Linux).

  ```text
  Traceback (most recent call last):
    File "<string>", line 4, in <module>
      json.load(Path('data/site-config.json'))
    File "...\Lib\json\__init__.py", line 293, in load
      return loads(fp.read(),
                   ^^^^^^^
  AttributeError: 'WindowsPath' object has no attribute 'read'
  ```

  You handed the `Path` straight to `json.load`. The traceback points at
  `fp.read()` inside the standard library, which is the clearest possible
  statement of what `load` wants. The parameter is even named `fp`, for file
  pointer.

- **`TypeError: dump() missing 1 required positional argument: 'fp'`.** You
  called `json.dump(config)` when you meant `json.dumps(config)`. Reading the
  argument name out of the message is faster than opening the docs.

- **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.**
  That message is the signature of an empty file, and it is worth memorising.
  Your config was not empty a moment ago — you opened it for writing before you
  read it, and `"w"` emptied it. There is no recovery except the backup step 2
  told you to make.

- **Nairobi is in the list twice after two runs.** `add_chapter` appends
  without checking. The membership test has to happen before the append, and it
  has to run against the current list.

- **The second run produces a diff even though nothing changed.** Three
  different causes, one symptom. You omitted `sort_keys=True`, so the key order
  follows whatever your edits did. Or you skipped the trailing newline, so Git
  reports `\ No newline at end of file`. Or you used `indent=4` one run and
  `indent=2` the next. Pin all three and the diff is empty by construction.

- **`KeyError: 'features'` coming out of `set_feature`.** You loaded a
  different file than you think, or an earlier buggy run overwrote the config
  with a partial dict. Print `config` right after loading.

## Under the hood

<details>
<summary>Under the hood — what "with" actually promises when a write blows up halfway</summary>

`with` is not a special case bolted onto files. It is a general protocol, and
knowing the shape tells you exactly what it does and does not guarantee.

Any object with a `__enter__` and an `__exit__` method is a **context
manager**. `with thing as name:` calls `thing.__enter__()`, binds the result to
`name`, runs the block, and then calls `thing.__exit__(...)` — always. Normal
exit, `return`, `break`, or an exception on the way through: `__exit__` runs.

Here it is in the open, with a deliberate failure in the middle:

```text
>>> class Loud:
...     def __enter__(self):
...         print("enter")
...         return self
...     def __exit__(self, exc_type, exc, tb):
...         print("exit, exception was:", exc_type.__name__ if exc_type else None)
...
>>> with Loud():
...     raise ValueError("boom")
...
enter
exit, exception was: ValueError
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    raise ValueError("boom")
ValueError: boom
```

`__exit__` ran, printed, and then the exception carried on to your terminal. It
sees the exception; it does not swallow it unless it returns something truthy,
and a file's `__exit__` never does.

**What that buys you for a file, precisely: it is closed, and closing flushes
the buffer.** Writing to a text file does not put bytes on the disk. It puts
characters into a buffer in memory, and the buffer is emptied to disk when it
fills up or when the file is closed. Skip the `with`, crash before `close`, and
whatever is still in the buffer is gone.

```text
>>> from pathlib import Path
>>> p = Path("half.txt")
>>> f = p.open("w", encoding="utf-8")
>>> f.write("hello")
5
>>> p.read_bytes()
b''
>>> f.close()
>>> p.read_bytes()
b'hello'
```

Five characters written, and zero bytes on disk until `close` ran.

**And here is what `with` does not promise, which matters for this exercise.**
It does not undo. If `json.dump` raises halfway through — because you slipped a
`set` into your config — then `"w"` has already emptied the file and `dump` has
already written a partial value into it, and `__exit__` closes the file
faithfully with that half-written mess inside it. The file is closed, the
buffer is flushed, and the content is broken.

You can watch it happen:

```text
>>> import json
>>> from pathlib import Path
>>> p = Path("broken.json")
>>> try:
...     with p.open("w", encoding="utf-8") as f:
...         json.dump({"chapters": {"Lagos"}}, f, indent=2, sort_keys=True)
... except TypeError as e:
...     print("raised:", e)
...
raised: Object of type set is not JSON serializable
>>> p.read_text(encoding="utf-8")
'{\n  "chapters": '
```

Your config is now fifteen characters long.

The fix has a name — the **atomic write** — and it is this exercise's first
stretch goal. Write to a temporary file beside the real one, and only when the
write has finished successfully, rename it over the top:

```python
tmp_path = path.with_suffix(".json.tmp")
with tmp_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, sort_keys=True)
    f.write("\n")
tmp_path.replace(path)
```

If the dump raises, the rename never runs and the real config is untouched. If
it succeeds, `Path.replace` swaps the files in one filesystem operation, so
there is no instant at which a reader can see a half-written config. That is
what "atomic" means: from outside, it either happened or it did not.

`with` gives you *cleanup*. It does not give you *rollback*. Rollback is
something you design.

</details>

<details>
<summary>Under the hood — the five places JSON and Python disagree</summary>

JSON looks so much like Python that the differences are easy to miss, and every
one of them shows up eventually as a confusing error.

**1. `true`, `false`, `null` are lowercase, and are not Python words.** Python
writes `True`, `False`, `None`. The `json` module translates in both
directions, which is why you can write `if config["features"]["comments"]:` and
have it work. It is also why `eval` on a JSON file fails immediately:
`NameError: name 'true' is not defined`.

**2. Object keys must be strings, and `dump` converts yours silently.** JSON
has no other key type. Python is happy with `{1: "a"}`, so `json.dumps` quietly
turns the key into `"1"` — and it does not come back as a number:

```text
>>> import json
>>> json.dumps({1: "a", 2.5: "b", None: "c"})
'{"1": "a", "2.5": "b", "null": "c"}'
>>> json.loads(json.dumps({1: "a"}))
{'1': 'a'}
```

An `int` key went out and a `str` key came back. That is not a roundtrip.

**3. No trailing commas, ever.** `[1, 2, 3,]` is valid Python and invalid JSON.
This is the single most common hand-editing mistake, and it is why step 7 makes
you do it on purpose.

**4. No comments.** There is no `//` and no `#`. Every "commented JSON" you
have seen is a different format wearing JSON's name — JSON5, JSONC, or somebody
allowing a `"_comment"` key that nothing reads. If you need to explain a
setting, add a real key for it, which is what the challenge's `good.json` does.

**5. Numbers are one type in the format and two in Python.** JSON has "number".
Python decodes anything with a `.` or an `e` in it as `float` and anything else
as `int`. So `5` returns as `5` and `5.0` returns as `5.0`, and they are not
the same object even though they compare equal. Meanwhile Python's special
floats have no JSON spelling at all, and the module writes them anyway:

```text
>>> json.dumps([float("nan"), float("inf")])
'[NaN, Infinity]'
```

That output is *not valid JSON*. Python reads it back happily and a strict
parser in another language will reject it. Pass `allow_nan=False` to get a
`ValueError` at write time instead of a surprise in somebody else's system.

One more that is not a disagreement but bites just as hard: **JSON has no
tuple.** `json.dumps((1, 2))` gives you `[1, 2]`, and loading it gives you a
list. Tuples go in and lists come out, permanently.

</details>

## Acceptance checklist

- [ ] The script runs with no traceback.
- [ ] `chapters` ends with `"Nairobi"` and contains no duplicates.
- [ ] `features.comments` is `true` and `max_upload_mb` is `10`.
- [ ] The saved file has sorted keys, two-space indentation, and a trailing newline.
- [ ] A second run prints the "already" lines and leaves the file byte-identical.
- [ ] `set_feature(config, "comnents", True)` raises `KeyError`.
- [ ] `git diff data/site-config.json` is empty after the second run.
- [ ] Committed to Git with a message like `Add Week 6 exercise 3: JSON config editor`.

## Stretch

- Make the write atomic, using the pattern from the first **Under the hood**
  block: dump to `site-config.json.tmp`, then `tmp_path.replace(CONFIG_PATH)`.
  A crash partway through can no longer leave a broken config behind, because
  the rename is a single filesystem operation.

- Add `remove_chapter(config, name) -> bool` that returns `False` instead of
  raising when the chapter is not listed. Then write a comment explaining why
  removal is forgiving while `set_feature` is strict. (The short version:
  "remove something that is not there" already has the outcome you wanted.
  "Enable a feature that does not exist" does not.)

- Record when the edit happened. Add a `"last_edited"` key set to
  `datetime.datetime.now().isoformat()`, run it twice, and watch the
  byte-identical second run break. Then decide which of the two properties you
  care about more, and write down why. There is a real answer here and it
  depends on who reads the file.

When your second run is a no-op, move on to
[Exercise 4 — Safe Divide](./exercise-04-safe-divide.md).
