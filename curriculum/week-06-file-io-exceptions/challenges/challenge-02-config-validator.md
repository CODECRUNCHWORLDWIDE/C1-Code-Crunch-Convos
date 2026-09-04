# Challenge 2 — Config Validator

> **Topic:** designing an exception family for a small library, and translating somebody else's exception into your own
> **Lecture:** [03 — Exceptions and Logging](../lecture-notes/03-exceptions-and-logging.md)
> **Difficulty:** the validating is a `for` loop over a dict; deciding what your errors *are* is the work
> **Target time:** 2–3 hours
> **Why this one:** this is the first thing you write that is a **library** rather than a script. Somebody else calls it, and what they get back when things go wrong is your design, not an accident. Exercise 5 taught you to raise your own exceptions. This one teaches you to build the small set of them that a caller can actually act on.

## The Brief

Every program that reads a settings file has the same bad day. The file is
missing a key. Or a key has a string where a number belongs. Or somebody
hand-edited it at midnight and left a trailing comma, so it is not even JSON
any more. The program starts anyway, gets four screens further in, and dies
somewhere that has nothing to do with the actual cause.

A **validator** moves that failure to the front. Read the file, check it
against a description of what a good file looks like, and either hand back the
settings or say — precisely, in one sentence — what is wrong with them.

That description is called a **schema**. Yours is going to be a plain Python
dict mapping each required key to the type its value must have:

```python
SCHEMA = {
    "log_level": str,
    "debug": bool,
    "port": int,
    "tags": list,
    "database": dict,
}
```

A valid config has all five of those keys, with values of those types. Extra
keys it does not mention are fine — real schemas are stricter, and being
relaxed here keeps the challenge about exceptions rather than about schema
design.

Here is the part that makes it a challenge. **Two completely different things
can be wrong**, and a caller will want to do different things about each:

- The file is not valid JSON at all. Nothing can be read out of it. The right
  response is usually "restore a backup".
- The file is valid JSON but the wrong shape. It parsed fine; it just does not
  say what this version of the program needs. The right response is usually
  "run a migration" or "tell the user which key to fix".

So you get two exception types, both inheriting from one base. A caller who
cares about the difference catches the specific one. A caller who just wants to
refuse to start catches the base. That choice is the API you are designing, and
it costs three lines.

One more thing, and it is the part graders look for. When you catch
`json.JSONDecodeError` and raise your own error instead, use `raise ... from e`.
The message you write carries the line and column, which is what a *user*
needs. The chained original carries the full parser traceback, which is what a
*maintainer* needs. `from e` keeps both.

## Starter

Save this as `challenge-02-config-validator.py` and fill in the `TODO`s:

```python
"""challenge-02-config-validator.py — a tiny JSON config validator.

Loads a JSON config file and checks it against a hand-written schema. Either
returns the parsed dict or raises a ConfigError saying exactly what is wrong.

    python challenge-02-config-validator.py
"""

import json
from pathlib import Path


class ConfigError(Exception):
    """Base class for all config validation errors."""


class ConfigParseError(ConfigError):
    """Raised when the file is not valid JSON."""


class ConfigSchemaError(ConfigError):
    """Raised when the JSON is valid but does not match the schema."""


SCHEMA: dict[str, type | tuple[type, ...]] = {
    "log_level": str,
    "debug": bool,
    "port": int,
    "tags": list,
    "database": dict,
}


def _type_name(expected: type | tuple[type, ...]) -> str:
    """Return a human-readable name for a single type or a tuple of them."""
    # TODO: "int" for int; "str or NoneType" for (str, type(None))
    return "?"


def _matches(value: object, expected: type | tuple[type, ...]) -> bool:
    """Return isinstance(value, expected), with the bool/int trap closed."""
    # TODO: reject a bool unless bool is what the schema actually asked for
    # TODO: otherwise return isinstance(value, expected)
    return False


def load_json(path: Path) -> object:
    """Read *path* and parse it as JSON.

    Raises:
        ConfigParseError: the file cannot be read, or is not valid JSON.
    """
    # TODO: read the text; on OSError raise ConfigParseError from e
    # TODO: json.loads it; on json.JSONDecodeError raise ConfigParseError
    #       from e, with e.lineno, e.colno and e.msg in the message
    return {}


def check_schema(config: dict, schema: dict[str, type | tuple[type, ...]]) -> None:
    """Raise ConfigSchemaError on the first key that is missing or mistyped."""
    # TODO: for each key in the schema:
    # TODO:   missing   -> raise ConfigSchemaError("missing required key: 'x'")
    # TODO:   wrong type -> raise ConfigSchemaError("key 'x' expected int, got str")


def validate_config(path: Path, schema: dict) -> dict:
    """Load and validate a JSON config file. Return the parsed dict."""
    config = load_json(path)
    # TODO: raise ConfigSchemaError when the top-level value is not a dict
    check_schema(config, schema)
    return config


if __name__ == "__main__":
    # TODO: write at least three configs to disk — a good one, one with a
    #       wrong type, one that is not JSON — and validate each in a
    #       try/except that prints the outcome.
    pass
```

Four names worth knowing before you start.

**`isinstance(value, expected)`.** Asks "is this value of this type", and it
accepts a *tuple* of types meaning "any of these". That is not a coincidence —
it is why a schema of plain type objects needs no parsing step at all.

**`type(value).__name__`.** The type's name as a string, so you can put `str`
or `NoneType` into an error message.

**`e.lineno`, `e.colno`, `e.msg`.** Attributes on a `json.JSONDecodeError`. The
numbers are where the problem is; `msg` is the parser's own sentence. Read
these off the object; never match on the printed text.

**The leading underscore** in `_matches` and `_type_name`. A convention meaning
"this is internal to the module". Nothing enforces it. It tells a reader which
names are the API and which are the plumbing.

## Requirements

1. Three exception classes: `ConfigError` inheriting from `Exception`, and
   `ConfigParseError` and `ConfigSchemaError` both inheriting from
   `ConfigError`. Each has a docstring.
2. `validate_config(path, schema)` returns the parsed dict when the config is
   valid.
3. A key in the schema but missing from the config raises `ConfigSchemaError`
   with a message like `missing required key: 'debug'`.
4. A value of the wrong type raises `ConfigSchemaError` with a message like
   `key 'port' expected int, got str`.
5. A file that is not valid JSON raises `ConfigParseError`, and the message
   carries the line and column from the parser.
6. That `ConfigParseError` is raised **`from`** the underlying
   `json.JSONDecodeError`, so the traceback preserves the cause.
7. Extra keys in the config that the schema does not mention are fine. Do not
   raise on them.
8. A file whose top-level value is not an object — `[1, 2, 3]` is valid JSON —
   raises `ConfigSchemaError` naming that, not a misleading "missing key".
9. The `__main__` block demonstrates at least three outcomes: a valid config, a
   schema mismatch, and a parse error, each caught and printed.
10. Every function has type hints and a docstring. Standard library only.

## Constraints

- **Read `e.lineno`, `e.colno` and `e.msg` off the exception. Never hard-code
  the parser's sentence.** The wording changed in CPython 3.13: a trailing
  comma that used to report `Expecting property name enclosed in double quotes`
  now reports `Illegal trailing comma before end of object`. Code that reads
  the attributes is correct on both. Code that pattern-matches the string is a
  validator that lies about every other kind of syntax error.
- **Catch `json.JSONDecodeError`, not `ValueError`.** `JSONDecodeError` is a
  subclass of `ValueError`, so `except ValueError:` does catch it — and also
  catches any `ValueError` your own code raises inside the same `try`, turning
  a genuine bug into a "the file is invalid JSON" message about a file that
  parsed perfectly. And `e.lineno` does not exist on a plain `ValueError`, so
  the moment that happens you get an `AttributeError` *inside your error
  handler*.
- **Always `raise ... from e`.** Without it Python still chains, but the
  traceback is labelled "During handling of the above exception, another
  exception occurred" — which reads as "your error handler crashed". `from e`
  says "this is a deliberate translation". Same data, opposite message to the
  person reading it at two in the morning.
- **Use `isinstance`, not `type(value) == expected`.** `==` rejects any
  subclass, and — the real trap — a tuple like `(str, type(None))` can never
  equal a single type, so optional keys become impossible to express.
- **Close the bool/int trap.** `bool` is a subclass of `int` in Python, so
  `isinstance(True, int)` is `True` and a config saying `"port": true` sails
  through a naive `int` check. Reject a `bool` unless `bool` is what the schema
  asked for.
- **Loop over the schema, not over the config.** The schema is the list of
  things that must be true. Loop over the config instead and "extra keys are
  fine" needs explicit code, while "a missing key" stops being noticed at all.
- **Check the top level is a dict before you validate it.** `json.loads("[1,
  2, 3]")` returns a list. Then `key not in config` runs a membership test
  against a list of numbers, finds nothing, and reports `missing required key:
  'log_level'` — technically true and wildly misleading.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2. It writes four
demonstration configs into a temporary folder and validates each one:

```text
$ python challenge-02-config-validator.py
good.json: OK - 6 keys, port=5432
wrong-type.json: ConfigSchemaError: key 'port' expected int, got str
missing-key.json: ConfigSchemaError: missing required key: 'debug'
bad-json.json: ConfigParseError: invalid JSON at line 1, column 16: Illegal trailing comma before end of object
```

Read those four lines as four different jobs done correctly.

`good.json` reports **6 keys** on a five-key schema, because it carries a
`"comment"` key the schema never mentions. Extra keys are allowed, and the
count proves it was kept rather than stripped.

`wrong-type.json` names the key, the expected type and the actual type. All
three matter. A message reading `bad value for 'port'` tells the user nothing
they did not already suspect.

`missing-key.json` names which key. There are five in the schema; guessing is
not a reasonable thing to ask of somebody.

`bad-json.json` gives a line and a column. On CPython 3.12 and earlier that
last line reads `line 1, column 17: Expecting property name enclosed in double
quotes` instead — the older parser described what it was hoping to find next,
rather than what was actually wrong. Your code is correct on both, because it
reads the numbers and the message off the exception object.

And here is the chaining, which is invisible in the four lines above because
every error was caught. Let one escape and the traceback shows both halves:

```text
Traceback (most recent call last):
  File "challenge-02-config-validator.py", line 84, in load_json
    return json.loads(raw)
           ~~~~~~~~~~^^^^^
  File "...\Lib\json\__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "...\Lib\json\decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "...\Lib\json\decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Illegal trailing comma before end of object: line 1 column 16 (char 15)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
  File "challenge-02-config-validator.py", line 86, in load_json
    raise ConfigParseError(
        f"invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
    ) from e
ConfigParseError: invalid JSON at line 1, column 16: Illegal trailing comma before end of object
```

Your line numbers will differ. The sentence in the middle is the one to look
for: **"The above exception was the direct cause of the following exception"**.
That is `from e` earning its keep.

## Steps

1. Save the starter. Run it. Nothing happens, which is the baseline.
2. Write the four config files by hand first, in a folder called `configs/`, so
   you can look at them:

   ```json
   { "debug": true, }
   ```

   That is `bad-json.json`, and it is a trailing comma — legal in Python,
   illegal in JSON.
3. Implement `load_json`, with only the `json.JSONDecodeError` branch at first.
   Point it at `bad-json.json` and read your own message.
4. Add the `OSError` branch. Test it by pointing at a filename that does not
   exist.
5. Implement `_type_name` and `check_schema` with plain `isinstance`. Run all
   four configs. Three of the four lines should already be right.
6. Now break it on purpose. Add `"port": true` to `good.json` and watch it pass
   validation:

   ```text
   >>> isinstance(True, int)
   True
   ```

   That is the bool/int trap, and it is the reason `_matches` exists. Implement
   `_matches`, re-run, and watch it fail correctly.
7. Add the top-level check. Test it with a file containing `[1, 2, 3]`.
8. Write the `__main__` block. Use `try` / `except ConfigParseError` /
   `except ConfigSchemaError` / `else`, and notice that the `else` branch is
   where the success message belongs — the `try` block should hold only the
   call that can fail.
9. Delete one `from e` and run the failing case again. Read the middle sentence
   of the traceback. Put it back.

## The Solution

```python
"""challenge-02-config-validator-solution.py — a tiny JSON config validator.

Three exception classes in a one-parent tree (ConfigError is the type callers
catch when they do not care *why* the config was bad), and one public function
that does load-then-validate in two clearly separated phases. A file that is not
JSON at all and a file that is JSON but the wrong shape are different kinds of
wrong, so they get different exception types — and both are a ConfigError.

Trade-off: validation stops at the first problem. That keeps the code and the
message simple. Collecting every problem in one pass is the fourth stretch goal
on the page, and it is what you would actually ship.

The four demonstration configs are written into a throwaway temporary directory
at run time, so the download runs on any machine with nothing set up beforehand
and leaves nothing behind.

Run it with::

    python challenge-02-config-validator-solution.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


class ConfigError(Exception):
    """Base class for all config validation errors."""


class ConfigParseError(ConfigError):
    """Raised when the file is not valid JSON."""


class ConfigSchemaError(ConfigError):
    """Raised when the JSON is valid but does not match the schema."""


SCHEMA: dict[str, type | tuple[type, ...]] = {
    "log_level": str,
    "debug": bool,
    "port": int,
    "tags": list,
    "database": dict,
}


def _type_name(expected: type | tuple[type, ...]) -> str:
    """Return a human-readable name for a single type or a tuple of them."""
    if isinstance(expected, tuple):
        return " or ".join(t.__name__ for t in expected)
    return expected.__name__


def _matches(value: object, expected: type | tuple[type, ...]) -> bool:
    """Return isinstance(value, expected), with the bool/int trap closed.

    ``bool`` is a subclass of ``int`` in Python, so ``isinstance(True, int)`` is
    True. A config that says ``"port": true`` would otherwise sail through an
    ``int`` check. Unless bool was explicitly asked for, reject bools.
    """
    wants_bool = expected is bool or (isinstance(expected, tuple) and bool in expected)
    if isinstance(value, bool) and not wants_bool:
        return False
    return isinstance(value, expected)


def load_json(path: Path) -> object:
    """Read *path* and parse it as JSON.

    Raises:
        ConfigParseError: the file cannot be read, or is not valid JSON. The
            message carries the parser's own line, column and explanation.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConfigParseError(f"cannot read {path.name}: {e.strerror}") from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ConfigParseError(
            f"invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e


def check_schema(config: dict, schema: dict[str, type | tuple[type, ...]]) -> None:
    """Raise ConfigSchemaError on the first key that is missing or mistyped."""
    for key, expected in schema.items():
        if key not in config:
            raise ConfigSchemaError(f"missing required key: {key!r}")
        value = config[key]
        if not _matches(value, expected):
            raise ConfigSchemaError(
                f"key {key!r} expected {_type_name(expected)}, "
                f"got {type(value).__name__}"
            )


def validate_config(path: Path, schema: dict) -> dict:
    """Load and validate a JSON config file. Return the parsed dict.

    Raises:
        ConfigParseError: if the file cannot be parsed as JSON.
            The error message includes the offending line and column.
        ConfigSchemaError: if the JSON does not match *schema*.
            The error message names the offending key and the expected type.
    """
    config = load_json(path)
    if not isinstance(config, dict):
        raise ConfigSchemaError(
            f"top-level value must be an object, got {type(config).__name__}"
        )
    check_schema(config, schema)
    return config


#: One config per outcome the validator has to produce.
CASES: dict[str, str] = {
    "good.json": """{
  "log_level": "INFO",
  "debug": true,
  "port": 5432,
  "tags": ["prod", "eu-west"],
  "database": {"host": "db-primary"},
  "comment": "extra keys are allowed"
}
""",
    "wrong-type.json": """{
  "log_level": "INFO",
  "debug": true,
  "port": "5432",
  "tags": [],
  "database": {}
}
""",
    "missing-key.json": """{
  "log_level": "INFO",
  "port": 5432,
  "tags": [],
  "database": {}
}
""",
    "bad-json.json": '{ "debug": true, }\n',
}


def main() -> None:
    """Write the four demonstration configs and validate each one."""
    with tempfile.TemporaryDirectory() as workspace:
        scratch = Path(workspace) / "configs"
        scratch.mkdir(parents=True, exist_ok=True)

        for name, text in CASES.items():
            path = scratch / name
            path.write_text(text, encoding="utf-8")
            try:
                config = validate_config(path, SCHEMA)
            except ConfigParseError as e:
                print(f"{name}: ConfigParseError: {e}")
            except ConfigSchemaError as e:
                print(f"{name}: ConfigSchemaError: {e}")
            else:
                print(f"{name}: OK - {len(config)} keys, port={config['port']}")


if __name__ == "__main__":
    main()
```

**The exception tree is the API.** `ConfigParseError` and `ConfigSchemaError`
both inherit from `ConfigError`, which gives a caller a choice it did not have
before:

```python
except ConfigParseError:   # "the file is corrupt"  — offer to restore a backup
except ConfigSchemaError:  # "the file is stale"    — offer to run a migration
except ConfigError:        # "the config is bad"    — just refuse to start
```

That is the same shape the standard library and every good third-party package
use: `requests` has `HTTPError` and `ConnectionError` under
`RequestException`, so you can catch either the specific case or the family.
The base class costs three lines, and it is the difference between a library
callers can handle precisely and one where they have to match on your error
messages.

**`raise ... from e` is doing real work here, not decoration.** The
`ConfigParseError` message carries the line, the column and the parser's own
explanation — everything a user needs to fix the file. The chained original
carries the whole `json` traceback — everything a maintainer needs. Both
audiences, one raise.

**Why `_matches` exists at all.** `bool` is a subclass of `int` in Python, a
decision from long ago that lets `True + True == 2`:

```text
>>> isinstance(True, int)
True
```

So a config with `"port": true` passes a plain `isinstance(value, int)` check,
and your program later tries to bind to port `True`. `_matches` rejects a bool
unless the schema actually asked for one. This is not over-engineering — it is
the one place where "exact types" in the brief and `isinstance` in the code
genuinely disagree, and a config validator that cannot tell `true` from a port
number is not validating.

**Why the schema is a plain dict of types.** Because a `type` is a first-class
value in Python and `isinstance` takes one directly. No parsing step, no
mini-language, no `eval`. And `isinstance` already accepting a *tuple* of types
is what makes the "optional keys" stretch goal expressible as
`(str, type(None))` with no new machinery at all. The design is doing less work
than it looks like, on purpose.

**Why `check_schema` loops over the schema and not the config.** The brief says
extra keys are fine. Looping over the schema means unknown keys are never even
looked at, so "allow extras" needs zero code. Loop over the config instead and
you have to write `if key not in schema: continue` — and you quietly stop
noticing missing keys, which is half the point of a validator.

**Why the top-level check comes before `check_schema`.** A file containing
`[1, 2, 3]` is perfectly valid JSON, and `json.loads` hands back a list.
Without the guard, `key not in config` runs a membership test against a list of
numbers, finds nothing, and reports `missing required key: 'log_level'` — true,
and useless. One `isinstance(config, dict)` check buys the honest message.

**Why `load_json` is annotated `-> object` and not `-> dict`.** Because it
genuinely can return a list, a string or a number — that is what JSON allows at
the top level. Saying `-> dict` would be a promise the function cannot keep,
and it would hide exactly the case requirement 8 exists to catch.
`validate_config` is the function that narrows it, right after the
`isinstance` check.

**`load_json` catches `OSError` too.** A missing file and an unreadable file
are both "cannot get the config", which is what `ConfigParseError` means to a
caller. Translating it here means a caller never has to know the function
touches the filesystem at all.

**About the harness.** `CASES` and the temporary folder in `main` exist so this
download runs on a machine where you have created nothing and leaves nothing
behind. The four cases are the four outcomes the validator has to produce, one
each.

## Run it

Copy the worked answer on this page into `challenge-02-config-validator.py` and run it:

```bash
python challenge-02-config-validator.py
```

It writes its four demonstration configs into a temporary directory, validates
each one, prints the outcome, and cleans up after itself. The `-solution` in
the name keeps it from colliding with your own
`challenge-02-config-validator.py`.

## Common bugs to catch

- **The traceback says "During handling of the above exception".**

  ```text
  json.decoder.JSONDecodeError: Illegal trailing comma before end of object: line 1 column 16 (char 15)

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    ...
  ConfigParseError: invalid JSON in configs\bad-json.json
  ```

  You forgot `from e`. Python chains implicitly either way, so all the data is
  still there — with the wrong label on it. "During handling of the above
  exception" means *something went wrong while you were handling an error*,
  which is a bug report. "The above exception was the direct cause" means
  *this is a deliberate translation*. The rubric puts two points on this.

- **`AttributeError: 'ValueError' object has no attribute 'lineno'` — raised
  inside your own error handler.** You caught `ValueError` instead of
  `json.JSONDecodeError`, so a `ValueError` from somewhere else in the same
  `try` block reached a handler that assumed it was a JSON error. Catch the
  narrowest type.

- **`"port": true` passes validation.** The bool/int trap. `isinstance(True,
  int)` is `True`, and a naive check has no way to object. Add the `_matches`
  guard.

- **A schema asking for `(str, type(None))` never matches anything.** You used
  `type(value) == expected`. A tuple can never equal a single type. `isinstance`
  is the tool; the bool guard is the one place you wrap it.

- **`missing required key: 'log_level'` for a file containing `[1, 2, 3]`.**
  Technically true, wildly misleading. You validated before checking the
  top-level type.

- **Extra keys are rejected.** You looped over the config instead of over the
  schema. Loop over the thing that lists the rules.

- **`ConfigSchemaError` never fires because `ConfigParseError` catches
  everything.** You ordered your `except` clauses with the base class first:

  ```python
  except ConfigError as e:        # matches both subclasses
      ...
  except ConfigSchemaError as e:  # never reached
      ...
  ```

  Same rule as Challenge 01. Narrowest first, always.

- **`TypeError: isinstance() arg 2 must be a type, a tuple of types, or a
  union`.** A schema value is not a type — you wrote `"port": "int"` with quote
  marks around it, so the schema holds a string. The whole point of the design
  is that the type object itself goes in the dict.

## Under the hood

<details>
<summary>Under the hood — designing an exception family somebody else has to use</summary>

The three classes in this challenge take three lines and they are the most
consequential design decision on the page. Here is the reasoning behind each
part, because you will make this decision again.

**How many types?** One rule: **there should be one exception type per
different thing a caller might reasonably do about it.** Not one per line of
code that can fail. If two failures would be handled identically by everyone,
they are one type with different messages.

Test it here. "The file is corrupt" leads to *restore a backup*. "The file is
the wrong shape" leads to *migrate, or tell the user which key to fix*. Two
different actions, two types. Now imagine splitting `ConfigSchemaError` into
`MissingKeyError` and `WrongTypeError` — what would a caller do differently?
Nothing: both mean "tell the user, refuse to start". One type, two messages.
That is why the design stops where it does.

**Why a base class rather than three unrelated types.** So a caller can be
imprecise on purpose. `except ConfigError:` says "I do not care why, I am not
starting", and — the part that matters over time — it keeps working when you
add a fourth failure mode next year. Every caller that used the base class
needs no edit. Without a base class, adding a type is a breaking change to
everybody.

**Whether to inherit from a built-in.** Tempting: make `ConfigSchemaError`
inherit from `ValueError` and existing handlers catch it for free. Mostly,
resist. It leaks an implementation detail into your contract, and it means a
caller's broad `except ValueError:` around something unrelated swallows your
error.

The exception that proves the rule is `json.JSONDecodeError`, which *does*
inherit from `ValueError` — because it was added to a module whose users had
been writing `except ValueError:` around `json.loads` for years, and breaking
all of them was not worth the purity. Inheriting from a built-in is a
backwards-compatibility decision. With no existing callers, `Exception` is the
honest parent.

**What to put on the exception besides a message.** Exercise 5 put
`.line_number` and `.raw` on its errors. The general rule: **the message is for
a human, the attributes are for a program.** If a caller might want to say
"which key was it" without parsing your sentence, that key belongs in an
attribute. A production version of this validator would carry `.key` and
`.path`, and the fourth stretch goal below carries `.problems` for exactly this
reason.

**How much to put in the message.** Enough that the reader can act without
opening anything else. `key 'port' expected int, got str` names the thing, the
expectation and the reality. Compare `invalid config`, which tells the reader
only that you noticed.

**And the failure mode this whole design exists to prevent.** A library that
raises bare `Exception("something went wrong")` forces every caller to catch
`Exception` — which means they also catch the `KeyError` from a bug in your
code, and report it as a bad config file. The types you raise are how you tell
callers which failures are theirs to handle and which are yours to fix.

</details>

<details>
<summary>Under the hood — how JSONDecodeError knows where the problem is</summary>

`invalid JSON at line 1, column 16` is not a guess. The parser tracks a single
number and computes the rest, and knowing that explains both the useful and the
odd parts of the message.

**One number underneath everything.** `JSONDecodeError` carries `pos`, the
zero-based index of the offending character in the whole document. `lineno` and
`colno` are derived from it by counting newlines up to that point — which is
why `char 194` appears in the printed message alongside the line and column.
Same fact, three renderings:

```text
>>> import json
>>> try:
...     json.loads('{ "debug": true, }')
... except json.JSONDecodeError as e:
...     print(e.msg, "|", e.lineno, e.colno, e.pos)
...
Illegal trailing comma before end of object | 1 16 15
```

`pos` is 15 and `colno` is 16, because `pos` counts from zero and humans count
columns from one.

**Why the message changed in 3.13.** The old parser reported what it *wanted
next*: seeing a comma, it expected a property name, did not find one, and said
`Expecting property name enclosed in double quotes` while pointing at the token
*after* the comma. Correct, and unhelpful — the user has to work backwards from
"expected a name" to "delete that comma". CPython 3.13 added dedicated messages
for the common mistakes, so the same file now says `Illegal trailing comma
before end of object` and points at the comma itself.

Both describe the same broken file. This is exactly why the constraint says to
read `e.msg` rather than match on it: the numbers are a stable contract, the
sentence is a human-facing string that improves over time.

**Why the column is sometimes not where you would put your cursor.** The parser
reports the first position at which the document became *impossible*, which is
not always where the mistake was made. Miss a closing brace at the end of a
nested object and the parser happily keeps reading, then fails several lines
later when it meets something that cannot follow. The number is honest about
what the parser knew and when; it is not a claim about intent. This is true of
every parser you will ever use, including Python's own.

**And the one that catches everybody:**

```text
>>> json.loads("")
Traceback (most recent call last):
  ...
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

`Expecting value: line 1 column 1 (char 0)` is the signature of an **empty
file**. Memorise it. When you see it, the question is not "what is wrong with
my JSON" but "why is that file empty" — and the usual answer is that something
opened it in `"w"` mode before reading it, which is the disaster Exercise 3's
constraints exist to prevent.

</details>

## Acceptance checklist

- [ ] Three exception classes, correctly related, each with a docstring.
- [ ] `validate_config` returns the parsed dict on a valid config.
- [ ] A missing key produces `missing required key: 'debug'`.
- [ ] A wrong type produces `key 'port' expected int, got str`.
- [ ] A bad JSON file produces a `ConfigParseError` carrying line and column.
- [ ] That `ConfigParseError` is raised `from` the `json.JSONDecodeError`, and
      the traceback says "the direct cause of".
- [ ] Extra keys in the config are accepted.
- [ ] A top-level array produces an honest message, not a "missing key" one.
- [ ] `"port": true` is rejected.
- [ ] No message text is hard-coded from the parser; `e.msg`, `e.lineno` and
      `e.colno` are read off the exception.
- [ ] The `__main__` block demonstrates at least three outcomes.
- [ ] Committed to Git with a message like `Add Week 6 challenge 2: config validator`.

## Stretch

Each of these changes the schema format a little. Do them one at a time.

1. **Nested schemas.** Let a schema value itself be a dict, so you can write
   `"database": {"host": str, "port": int}` and have it validated recursively.
   Thread the key path through as a `prefix` string so a nested problem reports
   `'database.host'` rather than a bare `'host'` that could be any of three
   keys. Recurse only *after* `isinstance(value, dict)` confirms there is
   something to recurse into, or you get an `AttributeError` from inside your
   own validator instead of a validation message.

2. **Optional keys.** Let a key be marked as "may be absent". The brief's
   suggestion — `(str, type(None))` — works with no new machinery, and means
   "may be `null`", which is subtly different from "may be missing". A small
   frozen dataclass marker, `Optional(str)`, can express both. Whichever you
   pick, note that optional means *may be absent*, not *may be wrong*: a
   present-but-mistyped optional key is still an error.

3. **Range constraints.** Validate that `port` is between 1 and 65535. Check
   the range *after* the int check, in an `elif`, so the comparison never sees a
   string — and so that `70000` reports the bound it broke rather than a type
   that was fine.

4. **Collect every problem at once.** Have the validation return a *list* of
   problems instead of raising on the first, and let `validate_config` decide
   that an empty list means success. This is the shape you actually want in
   real tooling: somebody fixing a config wants all eight problems in one pass,
   not eight edit-and-run cycles. Give `ConfigSchemaError` a `.problems`
   attribute holding the structured list, and format a readable default message
   for the one-problem and many-problem cases separately.

   Done well, the output reads like this:

   ```text
   ConfigSchemaError: 8 problems:
     - key 'log_level' expected str, got int
     - missing required key: 'debug'
     - key 'port' must be between 1 and 65535, got 70000
     - key 'tags' expected list, got dict
     - key 'database.host' expected str, got NoneType
     - key 'database.port' expected int, got str
     - key 'database.replica' expected str, got int
     - key 'description' expected str, got int
   ```

   `NoneType` is what `type(None).__name__` gives you. If you would rather say
   `null` to match JSON's own vocabulary, that is a one-line mapping and a
   defensible choice — write down which audience you decided for.

That is Week 6's challenges. Next comes the [homework](../homework/README.md), and
then the [mini-project](../mini-project/README.md), where the log parser you
build uses every piece of this week at once.
