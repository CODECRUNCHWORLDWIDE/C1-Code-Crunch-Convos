# Week 6 — Resources

A curated list of references for this week. The official Python docs should be your first stop for any question that comes up.

---

## Official Python documentation

These are the canonical references. Bookmark them.

- **[Reading and Writing Files (tutorial)](https://docs.python.org/3/tutorial/inputoutput.html)** — the official tutorial chapter. Covers `open()`, `with`, formatted output, and the basics of `json`. Start here.
- **[`pathlib` — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)** — the modern way to handle paths. Replaces most uses of `os.path`.
- **[`csv` — CSV file reading and writing](https://docs.python.org/3/library/csv.html)** — `reader`, `writer`, `DictReader`, `DictWriter`, dialects, and quoting rules.
- **[`json` — JSON encoder and decoder](https://docs.python.org/3/library/json.html)** — `load`, `loads`, `dump`, `dumps`, plus the conversion table between Python and JSON types.
- **[Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)** — the full hierarchy. Skim it once; refer back when you are catching errors.
- **[Errors and Exceptions (tutorial)](https://docs.python.org/3/tutorial/errors.html)** — the tutorial chapter for `try`/`except`/`raise`/custom exceptions.
- **[`logging` — Logging facility for Python](https://docs.python.org/3/library/logging.html)** — the API reference. Dense but authoritative.
- **[Logging HOWTO](https://docs.python.org/3/howto/logging.html)** — a much friendlier introduction than the API reference. Read this first.
- **[Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)** — patterns and recipes for real-world logging setups.

---

## Real Python articles

Real Python's tutorials are well-edited and beginner-friendly.

- **[Reading and Writing Files in Python](https://realpython.com/read-write-files-python/)** — a clear walkthrough of file modes, `with`, and common patterns.
- **[Python's `pathlib` Module: Taming the File System](https://realpython.com/python-pathlib/)** — pathlib from zero to confident.
- **[Reading and Writing CSV Files in Python](https://realpython.com/python-csv/)** — covers the `csv` module and a quick preview of `pandas`.
- **[Working With JSON Data in Python](https://realpython.com/python-json/)** — encoding, decoding, and the common gotchas.
- **[Python Exceptions: An Introduction](https://realpython.com/python-exceptions/)** — `try`/`except` from first principles.
- **[Python's `raise`: Effectively Raising Exceptions in Your Code](https://realpython.com/python-raise-exception/)** — when and how to raise, including chaining.
- **[Logging in Python](https://realpython.com/python-logging/)** — the article that finally makes the logging module click.

---

## PEPs and deeper reading

- **[PEP 343 — The "with" Statement](https://peps.python.org/pep-0343/)** — the spec that introduced `with`. Worth skimming once you are comfortable with the syntax.
- **[PEP 3151 — Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)** — why `FileNotFoundError`, `PermissionError`, etc. exist as distinct types instead of generic `IOError`.
- **[PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/#programming-recommendations)** — the section on exceptions is short and worth re-reading.

---

## Tools and references

- **[`pathlib` cheat sheet](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module)** — official mapping from `os`/`os.path` to `pathlib`. Lifesaver when porting old code.
- **[JSONLint](https://jsonlint.com/)** — paste in JSON to validate it. Useful when debugging your JSON files.
- **[CSV viewer for VS Code](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv)** — Rainbow CSV. Colorizes columns so misaligned rows jump out.

---

## Videos (optional)

- **["Python File Handling" — Corey Schafer](https://www.youtube.com/watch?v=Uh2ebFW8OYM)** — solid 30-minute overview.
- **["Python Logging" — mCoding](https://www.youtube.com/watch?v=9L77QExPmI0)** — opinionated but excellent take on logging.

---

## How to use this list

Don't read everything before starting the exercises. Read the **Python tutorial chapters** first, then dip into the Real Python articles for the topics that confuse you. Treat the API reference docs as a place to **look things up**, not as required reading.
