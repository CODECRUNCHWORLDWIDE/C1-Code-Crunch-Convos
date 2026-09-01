# Week 12 — Quiz

Ten multiple-choice questions. Pick one answer for each. Answers and short explanations are at the bottom — try the quiz first without peeking.

---

### 1. Which `argparse` action makes a flag *not* take a value but record `True` when present?

- A. `action="store"`
- B. `action="store_const"`
- C. `action="store_true"`
- D. `action="append"`

---

### 2. You want `python tool.py --version` to print `tool 2.0.0` and exit. Which line wires it up?

- A. `parser.add_argument("--version", default="2.0.0")`
- B. `parser.add_argument("--version", action="version", version="%(prog)s 2.0.0")`
- C. `parser.add_argument("--version", action="store_true")`
- D. `parser.print_version("tool 2.0.0")`

---

### 3. What is the **conventional** exit code for "command-line arguments were used incorrectly"?

- A. `0`
- B. `1`
- C. `2`
- D. `127`

---

### 4. Which `subprocess.run` invocation captures stdout as a string and raises on non-zero exit?

- A. `subprocess.run("ls", shell=True)`
- B. `subprocess.run(["ls"], stdout=True, text=True, check=True)`
- C. `subprocess.run(["ls"], capture_output=True, text=True, check=True)`
- D. `subprocess.call(["ls"], stdout=subprocess.PIPE)`

---

### 5. Why should you avoid `shell=True` when the command string includes user-provided input?

- A. It is slower than `shell=False`.
- B. It does not return stdout.
- C. It enables shell injection attacks.
- D. It only works on Linux.

---

### 6. Which `shutil` function makes a `.zip` archive of a directory?

- A. `shutil.zip()`
- B. `shutil.make_archive(base_name, "zip", root_dir)`
- C. `shutil.compress()`
- D. `shutil.archive(base_name, root_dir, format="zip")`

---

### 7. You want every file two or more levels deep under `~/photos` that ends in `.jpg`. Which expression returns them?

- A. `Path("~/photos").glob("*.jpg")`
- B. `Path.home().joinpath("photos").rglob("*.jpg")`
- C. `Path("~/photos").rglob("*.jpg")`
- D. `Path.home().glob("photos/*.jpg")`

---

### 8. According to the lecture's ethics rules, what is the *first* thing you should do before scraping a site?

- A. Set a fake User-Agent that looks like a browser.
- B. Read the site's `robots.txt` and respect it.
- C. Spin up 50 parallel workers to be efficient.
- D. Check if the page has a `<title>` tag.

---

### 9. You want a job to run at 02:00 every day on Linux. Which cron expression is correct?

- A. `0 2 * * *`
- B. `2 0 * * *`
- C. `* * 2 0 *`
- D. `@every 2h`

---

### 10. Which statement about `python-dotenv` and `.env` files is **correct**?

- A. `.env` files should always be committed to git for reproducibility.
- B. `load_dotenv()` automatically encrypts your secrets.
- C. `.env` files belong in `.gitignore`; ship a `.env.example` instead.
- D. `.env` only works on Windows.

---

## Answers

1. **C** — `store_true` is the standard way to make a boolean flag.
2. **B** — `action="version"` with a `version=` string is the built-in pattern. `%(prog)s` is interpolated to the program name.
3. **C** — Convention is `2` for misuse of CLI args. `argparse` already uses this.
4. **C** — `capture_output=True` + `text=True` + `check=True` is the canonical incantation.
5. **C** — User input is concatenated into a shell command, allowing arbitrary commands to run.
6. **B** — `shutil.make_archive(base, "zip", root_dir)` returns the path of the created archive.
7. **B** — `rglob` walks recursively. `~` is not expanded inside `Path()` — use `Path.home()` or `Path("~/photos").expanduser()`.
8. **B** — `robots.txt` first. Identifying yourself is a *positive* behavior, but the *first* check is whether you're even allowed there. Faking a User-Agent (A) is *bad* etiquette.
9. **A** — Format is `minute hour day-of-month month day-of-week`. `0 2 * * *` is "minute 0 of hour 2, every day".
10. **C** — `.env` files contain secrets; never commit them. The convention is to commit `.env.example` with empty values.
