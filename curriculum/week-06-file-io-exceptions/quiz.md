# Week 6 — Quiz

Ten multiple-choice questions covering file I/O, paths, CSV, JSON, exceptions, and logging. **Answer first, then scroll to the answer key at the bottom.** Target: 8/10 or higher.

---

### Question 1

Which `open()` mode opens a file for writing, **truncating it to empty if it already exists**?

- A. `"r"`
- B. `"a"`
- C. `"w"`
- D. `"x"`

---

### Question 2

What is the main reason to use the `with` statement when opening files?

- A. It is slightly faster than calling `open()` directly.
- B. It guarantees the file is closed even if an exception is raised inside the block.
- C. It is required by the Python interpreter — `open()` will not work otherwise.
- D. It automatically converts text to UTF-8.

---

### Question 3

Given the following code, what does `text` contain after it runs?

```python
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.readlines()
```

- A. A single string with the entire file contents.
- B. A list of strings, one per line, with `\n` at the end of each.
- C. An iterator over the lines of the file.
- D. The number of lines in the file.

---

### Question 4

You are using the `csv` module to read a file. Why should you pass `newline=""` to `open()`?

- A. To strip trailing whitespace from each row.
- B. To allow the file to contain empty rows.
- C. So that `csv` can handle line endings itself; otherwise Python's default newline translation can split rows incorrectly.
- D. It is purely cosmetic and has no real effect.

---

### Question 5

Which of the following is **not** a valid JSON value?

- A. `null`
- B. `42`
- C. `'hello'` (single-quoted string)
- D. `[1, 2, 3]`

---

### Question 6

What does `raise SomeError("boom") from original_exc` do?

- A. Replaces `original_exc` with `SomeError` silently.
- B. Raises `SomeError`, and the traceback explicitly shows that it was caused by `original_exc`.
- C. Suppresses `original_exc` so it does not appear in the traceback.
- D. Re-raises `original_exc` with the message "boom".

---

### Question 7

Which approach is more Pythonic for handling a key that might be missing from a dict?

- A. LBYL: `if key in d: value = d[key]` else default.
- B. EAFP: `try: value = d[key]` `except KeyError: value = default`.
- C. Both are equally Pythonic; pick whichever you like.
- D. Use `d.get(key, default)` — neither EAFP nor LBYL.

(Pick the answer that matches the lecture's stated preference.)

---

### Question 8

Why is `except Exception:` usually a bad practice in production code?

- A. It is slower than catching specific exceptions.
- B. It hides bugs by catching unexpected errors that should crash the program loudly.
- C. It is not allowed in Python 3.10+.
- D. It only catches one exception at a time.

---

### Question 9

Which `logging` method records the current traceback along with a message?

- A. `log.debug(msg)`
- B. `log.error(msg)`
- C. `log.exception(msg)`
- D. `log.critical(msg)`

---

### Question 10

You have a `Path` object `p = Path("/Users/jane/notes/draft.md")`. Which expression gives you `"draft"` (no extension)?

- A. `p.name`
- B. `p.stem`
- C. `p.suffix`
- D. `p.parent`

---

## Answer key

<details>
<summary>Click to reveal answers</summary>

1. **C** — `"w"` opens for writing and truncates. `"a"` opens for appending without truncating. `"x"` raises if the file already exists.
2. **B** — `with` calls the file object's `__exit__` method, which closes the file even on exceptions.
3. **B** — `.readlines()` returns a list of strings, one per line, with `\n` at the end of each (except possibly the last line if the file did not end with a newline).
4. **C** — Python's default newline translation can corrupt CSV rows that contain embedded newlines inside quoted fields. The `csv` module documents this requirement explicitly.
5. **C** — JSON strings must use double quotes. Single-quoted strings are valid Python but invalid JSON.
6. **B** — `raise ... from ...` is explicit exception chaining. The traceback shows "The above exception was the direct cause of the following exception."
7. **B** — The lecture states Python idiomatically prefers EAFP. (Note that `d.get(key, default)` is also fine in this specific case and arguably better for dict lookups; the question is asking about EAFP vs LBYL in general.)
8. **B** — Catching `Exception` swallows `NameError`, `AttributeError`, etc., turning a clear crash into a mysterious wrong result.
9. **C** — `log.exception` is essentially `log.error` plus the current traceback. Only call it inside an `except` block.
10. **B** — `p.stem` strips the extension. `p.name` keeps it (`'draft.md'`); `p.suffix` returns `'.md'`; `p.parent` returns the containing directory.

</details>

---

If you scored 7 or below: re-read the relevant lecture and retake. Specifically:

- Questions 1–4 → lecture 01.
- Questions 5 → lecture 02.
- Questions 6–9 → lecture 03.
- Question 10 → lecture 01 section 6.
