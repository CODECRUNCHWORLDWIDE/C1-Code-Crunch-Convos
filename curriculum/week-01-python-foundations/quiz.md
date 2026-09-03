# Week 1 Quiz

Ten multiple-choice questions to verify you've absorbed the week's
material. Commit to an answer, then open the fold under the question to
check yourself. A passing score is 8 / 10.

No tools allowed — try to answer from memory first. If you have to look
something up, mark the question and revisit it.

---

## 1. Which command verifies that Python is installed and on your PATH?

- A. `python --print-version`
- B. `python --version`
- C. `python -v --check`
- D. `python check`

<details>
<summary>Answer</summary>

**B** — `python --version`. The double-dash form is the canonical flag.

</details>

## 2. What does REPL stand for?

- A. Run, Eval, Print, Loop
- B. Read, Execute, Push, Loop
- C. Read, Eval, Print, Loop
- D. Run, Evaluate, Process, Log

<details>
<summary>Answer</summary>

**C** — Read, Eval, Print, Loop. The REPL reads input, evaluates it,
prints the result, and loops.

</details>

## 3. Which of the following is the **safest** way to invoke `pip`?

- A. `pip install requests`
- B. `python -m pip install requests`
- C. `sudo pip install requests`
- D. `pip3 install --global requests`

<details>
<summary>Answer</summary>

**B** — `python -m pip install requests`. The `python -m pip` form
guarantees you're using the pip belonging to the active Python.

</details>

## 4. What does `python -m venv .venv` do?

- A. Activates an existing virtual environment named `.venv`.
- B. Lists every virtual environment on the machine.
- C. Creates a new virtual environment in a folder called `.venv`.
- D. Deletes the virtual environment in `.venv`.

<details>
<summary>Answer</summary>

**C** — It creates a new virtual environment in a folder called
`.venv`. Activation is a separate step.

</details>

## 5. Which command shows the contents of the current directory on macOS/Linux?

- A. `dir`
- B. `cd`
- C. `pwd`
- D. `ls`

<details>
<summary>Answer</summary>

**D** — `ls`. (`dir` is the Windows `cmd.exe` command; `pwd` prints the
current path; `cd` changes directory.)

</details>

## 6. After making changes to a file, which Git command stages those changes
   for the next commit?

- A. `git stage`
- B. `git add`
- C. `git commit`
- D. `git push`

<details>
<summary>Answer</summary>

**B** — `git add`. Staging is the step before `git commit`.

</details>

## 7. What is the difference between **Git** and **GitHub**?

- A. They are two names for the same tool.
- B. Git is a graphical app; GitHub is the command-line version.
- C. Git is a version-control system; GitHub is a hosting service for Git
     repositories.
- D. GitHub replaces Git; you no longer need Git to use GitHub.

<details>
<summary>Answer</summary>

**C** — Git is the version-control system; GitHub is one of many
hosting services that store Git repositories on the web.

</details>

## 8. Which of the following lines belongs in a Python project's
   `.gitignore`?

- A. `README.md`
- B. `.venv/`
- C. `main.py`
- D. `requirements.txt`

<details>
<summary>Answer</summary>

**B** — `.venv/`. Virtual environments are recreated locally from
`requirements.txt` and should not be tracked in version control.

</details>

## 9. In a `.py` file, which of these starts a single-line comment?

- A. `//`
- B. `--`
- C. `#`
- D. `;`

<details>
<summary>Answer</summary>

**C** — `#` begins a single-line comment in Python. (`//` is C/C++/JS,
`--` is SQL/Lua, `;` is Lisp/assembly.)

</details>

## 10. Inside an activated venv, you run `python -c "import sys;
   print(sys.executable)"`. The printed path should be:

- A. The system Python at `/usr/bin/python3` (macOS/Linux) or
     `C:\Python312\python.exe` (Windows).
- B. A path **inside** the venv's folder (for example,
     `~/projects/myapp/.venv/bin/python`).
- C. Empty.
- D. An error message — `sys.executable` requires extra installation.

<details>
<summary>Answer</summary>

**B** — A path inside the venv's folder. If you see the system Python
instead, activation didn't take effect.

</details>

---

