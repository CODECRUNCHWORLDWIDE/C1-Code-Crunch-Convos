# Lecture 03 — Exceptions and Logging

> **Read time:** ~30 min. **Type-along time:** ~60 min.

So far your programs have been **happy-path** programs: if everything goes right, they do the right thing. But real software runs in a world full of broken things — missing files, bad network connections, malformed input, full disks. Code that ignores those possibilities is brittle. Code that handles them deliberately is **robust**.

This lecture covers Python's two tools for that: the **exception system** (for handling problems when they occur) and the **`logging` module** (for telling you what your program is doing, especially when something goes wrong).

---

## 1. Why exceptions exist

Imagine writing a function `read_config(path)` that returns a dictionary. What does it return if the file doesn't exist?

In some older languages the answer is "a special sentinel value, like `null` or `-1`, and the caller has to check." That has two problems:

1. Callers **forget to check** all the time.
2. Sentinels make function signatures lie — `read_config` claims to return a dict, but sometimes it returns `None`.

Python's answer is **exceptions**. When something goes wrong, the function **raises** an exception. Control jumps out of the function and propagates up the call stack until something **catches** it. If nothing catches it, the program crashes with a traceback. This means:

- Errors are **loud by default** — you cannot accidentally ignore them.
- You can handle them **at the right level** — sometimes the caller knows what to do, sometimes the caller's caller does.
- Function signatures stay clean — `read_config` always returns a dict, or it does not return at all.

---

## 2. `try` / `except` — the basics

```python
from pathlib import Path

try:
    text = Path("config.json").read_text(encoding="utf-8")
except FileNotFoundError:
    text = "{}"   # fall back to empty config
```

The flow:

1. Python tries to execute the `try` block.
2. If an exception of the listed type (or a subclass) is raised, control jumps to the matching `except` block.
3. If no exception is raised, the `except` block is skipped.
4. After either path, execution continues after the `try`/`except`.

You can catch multiple types:

```python
try:
    n = int(s)
except (ValueError, TypeError):
    n = 0
```

You can bind the exception object to a name to inspect it:

```python
try:
    n = int(s)
except ValueError as e:
    print(f"Could not parse {s!r}: {e}")
    n = 0
```

---

## 3. `else` and `finally`

`try` has two more optional clauses.

### `else` — runs only if no exception

```python
try:
    f = open("data.txt", "r", encoding="utf-8")
except FileNotFoundError:
    print("no data yet")
else:
    with f:
        print(f.read())
```

The `else` block runs **only if the `try` block completed without raising**. It is useful for code that should run on success but should not be protected by the same `except` (because if *it* raises, you want the exception to propagate normally).

### `finally` — always runs

```python
f = open("data.txt", "r", encoding="utf-8")
try:
    process(f.read())
finally:
    f.close()
```

The `finally` block runs **no matter what** — on success, on exception, even if you `return` from inside the `try`. This is exactly the pattern that `with` automates for you. You rarely write `finally` by hand once you know `with`, but it is the right tool for cleanup that has no context-manager wrapper.

---

## 4. Narrow vs broad `except` — always prefer narrow

A bare `except:` (or `except Exception:`) catches **everything**, including bugs in your own code, `KeyboardInterrupt` (the user pressing Ctrl-C), and runtime issues that should crash the program loudly.

```python
# BAD — hides every possible problem, including typos
try:
    result = compute(x)
except:
    result = 0
```

If `compute` has a `NameError` because you typo'd a variable, this code silently returns `0` and you spend three hours debugging a downstream symptom.

**Rule:** catch the **narrowest** exception that matches what you actually expect.

```python
# GOOD — only swallows the specific failure you anticipated
try:
    result = compute(x)
except ZeroDivisionError:
    result = 0
```

The only legitimate reasons to catch `Exception` broadly are:

1. **Logging-and-reraising** at the top of a long-running service: catch, log, re-raise so the failure is recorded but not swallowed.
2. **Plugin systems** where you cannot know what third-party code might raise.

If you find yourself writing `except Exception:` as a beginner, stop and ask "what specific failure am I expecting here?" Then catch that.

---

## 5. The built-in exception hierarchy

All built-in exceptions inherit from `BaseException`. Most user code only deals with the `Exception` branch. A simplified tree of the ones you will meet this year:

```
BaseException
 ├── SystemExit               # sys.exit() — do not catch
 ├── KeyboardInterrupt        # Ctrl-C — do not catch
 └── Exception
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    └── OverflowError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── OSError              # file system & OS errors
      │    ├── FileNotFoundError
      │    ├── PermissionError
      │    ├── IsADirectoryError
      │    └── NotADirectoryError
      ├── TypeError            # wrong type
      ├── ValueError           # right type, wrong value
      │    └── UnicodeError    # encoding issues
      ├── AttributeError       # missing method or attribute
      ├── NameError            # undefined variable
      └── RuntimeError         # generic
```

Two practical consequences:

1. `except OSError:` catches `FileNotFoundError`, `PermissionError`, and friends — useful when you do not care which file-system error happened, just that something filesystem-y went wrong.
2. **Never catch `BaseException`** unless you are writing a framework. Catching it swallows `KeyboardInterrupt`, which means users cannot Ctrl-C your program.

Full hierarchy: [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).

---

## 6. `raise` — signaling errors yourself

The flip side of `except` is `raise`. You use it when **your** code detects a problem.

```python
def withdraw(balance: float, amount: float) -> float:
    if amount > balance:
        raise ValueError(f"cannot withdraw {amount}; balance is {balance}")
    return balance - amount
```

Pick the most specific built-in exception that fits, or define a custom one (next section). The string you pass becomes the exception message.

### Re-raising

Inside an `except` block, a bare `raise` re-raises the current exception, preserving the traceback.

```python
try:
    do_thing()
except FileNotFoundError:
    log("file missing, aborting")
    raise            # propagates the original exception unchanged
```

This is useful for "log and re-raise" patterns where you want to record something but not actually handle the error.

### Exception chaining — `raise ... from ...`

Sometimes you want to convert one exception into another while keeping the original cause:

```python
def load_config(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"invalid config file {path}") from e
```

The `from e` part tells Python "this new exception was caused by `e`." The traceback will show both. Without `from`, Python will still chain them implicitly (and print "During handling of the above exception, another exception occurred"), but using `from` is more explicit and conveys intent.

You can also write `from None` to suppress the original traceback entirely — useful when the inner exception is an implementation detail you do not want to leak to the caller.

---

## 7. Custom exception classes

When the built-in exceptions do not describe your domain well, define your own. A custom exception is just a class inheriting from `Exception`:

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""

def withdraw(balance: float, amount: float) -> float:
    if amount > balance:
        raise InsufficientFundsError(
            f"cannot withdraw {amount}; balance is {balance}"
        )
    return balance - amount
```

You can add attributes to make the exception useful to callers:

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance: float, amount: float) -> None:
        super().__init__(f"cannot withdraw {amount}; balance is {balance}")
        self.balance = balance
        self.amount = amount

try:
    withdraw(50, 100)
except InsufficientFundsError as e:
    print(f"Short by {e.amount - e.balance}")
```

Good practice for any non-trivial project:

1. Define a **base** exception for your project, e.g. `class BankError(Exception): pass`.
2. Make specific exceptions inherit from it: `class InsufficientFundsError(BankError): pass`.
3. Callers can `except BankError:` to catch anything your library raises without also catching unrelated `ValueError`s from elsewhere.

You will see this exact pattern in the standard library — for example, `requests.HTTPError` and `requests.ConnectionError` both inherit from `requests.RequestException`.

---

## 8. EAFP vs LBYL

There are two philosophies for handling "might this work?" situations:

- **LBYL — Look Before You Leap.** Check preconditions before acting.
- **EAFP — Easier to Ask Forgiveness than Permission.** Try the operation; catch the failure if it occurs.

Python idiomatically prefers EAFP for most cases. Compare:

```python
# LBYL — looks reasonable, but has a race condition
if path.exists():
    text = path.read_text(encoding="utf-8")
else:
    text = ""
```

Between the `exists()` check and the `read_text()` call, another process could delete the file. The check is not a guarantee.

```python
# EAFP — atomic, no race
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    text = ""
```

EAFP is also often faster — `dict["key"]` is faster than `if "key" in dict: dict["key"]` because it avoids the double lookup.

When does LBYL make sense?

- Cheap, side-effect-free checks (`if not arg: raise ValueError`).
- Validating user input before doing expensive work.
- Cases where the failure mode is genuinely rare and the check is genuinely cheap.

For file and dict operations, default to EAFP.

---

## 9. The `logging` module — why `print` isn't enough

Quick: at 2 a.m., your production server is misbehaving. Which would you rather have?

(A) The `print` statements you scattered through your code three months ago, all mixed with normal program output, with no timestamps, no severity, no source file or line number.

(B) A structured log with timestamps, severity levels, the function name, and an option to silence noisy modules.

That is what `logging` gives you over `print`. The cost is **one import and one line of setup**.

### Minimum viable setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

log = logging.getLogger(__name__)

log.debug("entered function with x=%d", x)
log.info("loaded %d records from %s", len(records), path)
log.warning("config file missing; using defaults")
log.error("could not write report: %s", err)
log.critical("database unreachable; shutting down")
```

A run produces output like:

```
2026-05-13 14:30:01,234 | INFO     | my_module | loaded 42 records from data.csv
2026-05-13 14:30:01,235 | WARNING  | my_module | config file missing; using defaults
```

### Log levels

| Level | When to use |
|---|---|
| `DEBUG` | Verbose diagnostic info. Only shown when debugging. |
| `INFO` | Routine "things are happening" messages. |
| `WARNING` | Something unusual happened, but the program continues. |
| `ERROR` | Something went wrong, an operation failed. |
| `CRITICAL` | The program cannot continue. |

The `level=` argument to `basicConfig` sets the **threshold** — messages below that level are suppressed. In development you might use `DEBUG`; in production, `INFO` or `WARNING`.

### `getLogger(__name__)`

The convention is to get a logger named after your module. This lets you tune verbosity per module — e.g. silence noisy library logging without silencing your own code.

### Logging exceptions

The killer feature: `log.exception(msg)` records the message **plus the current traceback**. Use it inside an `except` block:

```python
try:
    process(record)
except ValueError:
    log.exception("could not process record %r; skipping", record)
```

You get the full traceback in the log without crashing the program. This is enormously useful for batch jobs that should keep going even if individual items fail.

### When to use `print` instead

`print` is fine for:

- One-off scripts you will run once and throw away.
- User-facing CLI output (the program's *result*, not its diagnostics).
- The REPL.

Use `logging` for:

- Anything that will run more than once.
- Anything that will run unattended.
- Anything where you might need to debug a past failure.

Rough rule: if it answers "what does the user see?", use `print`. If it answers "what is the program doing?", use `logging`.

---

## 10. Putting it all together

A small file-processing function with proper error handling and logging:

```python
import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)


class ConfigError(Exception):
    """Raised when the config file cannot be loaded or is invalid."""


def load_config(path: Path) -> dict:
    """Load a JSON config file. Returns an empty dict if the file is missing."""
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        log.warning("config file %s not found; using defaults", path)
        return {}
    except PermissionError as e:
        raise ConfigError(f"cannot read {path}: permission denied") from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"invalid JSON in {path} at line {e.lineno}, column {e.colno}"
        ) from e
```

This function demonstrates everything from this lecture:

- **Narrow excepts** for `FileNotFoundError`, `PermissionError`, `JSONDecodeError`.
- **Logging** for the recoverable case (missing file).
- **`raise ... from e`** to convert library exceptions into a domain-specific one.
- A **custom exception** (`ConfigError`) so callers have one type to catch.

---

## What's next

You have now seen all of Week 6's pieces — files, paths, CSV, JSON, exceptions, and logging. The mini-project (a log file analyzer) brings them all together.

Head to `exercises/README.md` to start the practice problems, or jump straight to `mini-project/README.md` if you are confident.
