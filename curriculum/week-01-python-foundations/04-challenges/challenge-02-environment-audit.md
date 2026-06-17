# Challenge 2 — Environment Audit

**Estimated time:** 30–60 minutes

## The Brief

Every Python project survives or dies by *reproducibility*: can someone
else (or future-you) recreate the exact same environment you used? In
this challenge you'll write a small auditing script called `audit.py`
that prints a friendly summary of the Python environment it is running
in. Output should look approximately like this:

```text
==========================================================
 Python Environment Audit
==========================================================
Python version : 3.12.3
Implementation : CPython
Platform       : macOS-14.4.1-arm64-arm-64bit
Executable     : /Users/you/projects/hello-you/.venv/bin/python
Working dir    : /Users/you/projects/hello-you
Inside venv    : yes

Installed packages (5):
  - pip            24.0
  - requests       2.31.0
  - certifi        2024.7.4
  - charset-normalizer  3.3.2
  - urllib3        2.2.2
==========================================================
```

## Functional Requirements

The script must print, in any sensible order:

1. The Python version (for example `3.12.3`).
2. The Python implementation name (almost always `CPython`).
3. A platform string (operating system + architecture).
4. The full path to the running Python interpreter.
5. The current working directory.
6. Whether the script is running inside a virtual environment
   (`yes` / `no`).
7. A list of installed packages with their versions.

## Technical Requirements

- The file must start with a module-level docstring.
- Use type hints on every function you define.
- Use the standard-library `sys` and `platform` modules. Read the docs
  at <https://docs.python.org/3/library/sys.html> and
  <https://docs.python.org/3/library/platform.html>.
- For the installed-package list, choose **one** of these approaches:
  - **Simple:** call `pip list` as a child process with the
    `subprocess` module
    (<https://docs.python.org/3/library/subprocess.html>).
  - **Slightly fancier:** use `importlib.metadata.distributions()`
    (<https://docs.python.org/3/library/importlib.metadata.html>).
- Wrap the printing in a `main()` function and guard it with
  `if __name__ == "__main__":`.

## Hints

- `sys.version_info` gives you a tuple like `(3, 12, 3, 'final', 0)`.
- `sys.executable` returns the path to the running interpreter.
- `platform.platform()` returns a human-readable platform string.
- `sys.prefix != sys.base_prefix` is `True` when you are inside a venv.
- To run a child process and capture its output:

  ```python
  import subprocess

  result = subprocess.run(
      ["python", "-m", "pip", "list"],
      capture_output=True,
      text=True,
      check=True,
  )
  print(result.stdout)
  ```

## Suggested Skeleton

```python
"""audit.py — print a summary of the current Python environment."""

import sys
import platform


def is_in_virtualenv() -> bool:
    """Return True when running inside a venv."""
    return sys.prefix != sys.base_prefix


def main() -> None:
    print("=" * 58)
    print(" Python Environment Audit")
    print("=" * 58)
    print(f"Python version : {platform.python_version()}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Executable     : {sys.executable}")
    # TODO: print working directory, venv status, and installed packages.


if __name__ == "__main__":
    main()
```

## Stretch Goals

- Print the audit as **JSON** when the user passes `--json` on the
  command line. Use the `json` module and `sys.argv`.
- Sort the package list alphabetically, case-insensitive.
- Color the "yes"/"no" venv indicator green/red using `colorama`.
- Write the output to a file instead of stdout when `--output report.txt`
  is passed.

## Acceptance Checklist

- [ ] Script runs and prints the required fields.
- [ ] Script correctly reports `yes` when run inside a venv and `no`
      when run from a fresh terminal without activation.
- [ ] Type hints are present on every function.
- [ ] Module docstring describes the script's purpose in one or two
      sentences.
- [ ] You have committed the file to Git with a clear message such as
      `Add Challenge 2: environment audit script`.
