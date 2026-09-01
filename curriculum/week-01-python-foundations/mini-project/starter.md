# Mini-Project Starter — "Hello, You"

> **Project:** [Mini-Project — "Hello, You"](./README.md)
> **Week:** 1
> **What this is:** the scaffold for the Week 1 mini-project. Copy the block
> below into a file called `hello_you.py` inside your own `hello-you/` folder,
> then fill in the four `TODO`s. The scaffold already runs before you touch it,
> so you always have a working program to grow rather than a broken one to
> repair.

Everything the mini-project spec asks for is here in outline: two functions
with type hints, a module docstring, and the `if __name__ == "__main__":`
guard. What is missing is the part only you can write — reading the answers
and assembling the sentence.

## How to use this page

1. Make the project folder and move into it:

   ```bash
   mkdir hello-you
   cd hello-you
   ```

2. Create the virtual environment and activate it, exactly as in Lecture 2:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell the activate line is
   `.venv\Scripts\Activate.ps1` instead. Your prompt should now start with
   `(.venv)`.

3. Create an empty file named `hello_you.py` and paste in the whole code
   block from the section below. Do not rename anything yet.

4. Run it once before you edit a single character:

   ```bash
   python hello_you.py
   ```

   You should see one line: `Hello, friend.` That line is the placeholder,
   and seeing it proves your file, your interpreter, and your terminal all
   agree with each other. Debugging one problem at a time starts with
   confirming there is only one.

5. Work the four `TODO`s top to bottom. Run the script after each one. Four
   short runs beat one long guess.

6. Delete each `# TODO:` comment as you satisfy it. A `TODO` left in finished
   code is a note to a reader that something is unfinished, and it will be
   wrong by tomorrow.

## The starter

```python
"""hello_you.py — greet one person, by name, from the terminal.

Week 1 mini-project for Code Crunch Convos. Asks for a name and an
optional favorite programming language, then prints a single friendly
line. Run it with: python hello_you.py
"""

DEFAULT_NAME: str = "friend"
DEFAULT_LANGUAGE: str = "Python"


def prompt_user() -> tuple[str, str]:
    """Ask for a name and a favorite language and return both, cleaned.

    Returns:
        A pair of strings, name first. Each falls back to its DEFAULT_
        constant when the user types nothing but whitespace.
    """
    # TODO 1: read the name with input("Your name: "), then strip() it and
    #         fall back to DEFAULT_NAME when the result is empty.
    # TODO 2: read the language the same way, falling back to
    #         DEFAULT_LANGUAGE. The prompt text is up to you; the sample
    #         session below uses "Favorite language (Enter for Python): ".
    # TODO 3: return the two cleaned strings as one tuple, name first.
    return DEFAULT_NAME, DEFAULT_LANGUAGE


def build_greeting(name: str, language: str) -> str:
    """Return the greeting line for name and language.

    build_greeting("Ada", "Python") returns
    'Hello, Ada! Welcome to Code Crunch Convos. May your Python be readable.'

    Args:
        name: the person's name, already stripped.
        language: their favorite language, already stripped.

    Returns:
        One line of text. This function never prints; main() does that.
    """
    # TODO 4: build the sentence in the docstring above with an f-string
    #         and return it. Both values go in; nothing gets printed here.
    return f"Hello, {name}."


def main() -> None:
    """Collect the two answers, build the greeting, and print it."""
    name, language = prompt_user()
    print(build_greeting(name, language))


if __name__ == "__main__":
    main()
```

## What each TODO is asking for

- **TODO 1 — read and clean the name.** `input()` hands back exactly what was
  typed, including any stray spaces before or after. `str.strip()` removes
  them. Then use the `or` trick from the spec's hints: an empty string is
  falsy, so `raw.strip() or DEFAULT_NAME` gives you the typed name when there
  is one and `"friend"` when the user just pressed Enter. Two operations, one
  line, no `if` — which matters, because conditionals are Week 3.
- **TODO 2 — read and clean the language.** Identical shape, different
  constant. Writing the same pattern twice on purpose is how it stops being a
  pattern you look up and starts being one you know.
- **TODO 3 — return both.** One `return` statement with a comma in it. The
  comma is what builds the tuple; the parentheses are optional. `main()`
  already unpacks the pair into two names, so the order matters: name first,
  language second.
- **TODO 4 — assemble the sentence.** One f-string with two placeholders in
  it. Read the exact wording out of the docstring and match it character for
  character, including the exclamation point after the name and the period at
  the end. Return it rather than printing it, so that later — in Week 11 —
  the same function can be checked by a test instead of by your eyes.

## Expected output when you are done

Three sessions. The first types both answers, the second leaves the language
blank, and the third leaves both blank.

```text
$ python hello_you.py
Your name: Ada
Favorite language (Enter for Python): Rust
Hello, Ada! Welcome to Code Crunch Convos. May your Rust be readable.

$ python hello_you.py
Your name:   Grace Hopper
Favorite language (Enter for Python):
Hello, Grace Hopper! Welcome to Code Crunch Convos. May your Python be readable.

$ python hello_you.py
Your name:
Favorite language (Enter for Python):
Hello, friend! Welcome to Code Crunch Convos. May your Python be readable.
```

Look closely at the second session. The name was typed with two leading
spaces and came back clean, which is `strip()` earning its place. The third
session is the one that proves your fallbacks work.

## Common bugs to catch

- **`TypeError: cannot unpack non-iterable NoneType object`.** `prompt_user()`
  has no `return` — you deleted the placeholder line while filling in TODO 3
  and never replaced it. A function that falls off the end gives back `None`,
  and `None` cannot be spread across `name, language`.
- **The greeting prints twice.** You called `print()` inside
  `build_greeting()` *and* left the `print()` in `main()`. Building and
  displaying are two jobs; keep them in two places.
- **`Hello, ! Welcome to...` with an empty name.** Your fallback is on the
  wrong side of the `or`, or you wrote `raw or raw.strip()`. The expression
  reads left to right and returns the first truthy operand, so the stripped
  value has to come first: `raw.strip() or DEFAULT_NAME`.
- **`Hello,    Ada   ! Welcome to...`.** You put `raw_name` into the f-string
  instead of the stripped `name`. Strings are immutable, so `raw.strip()`
  returns a new string and leaves the original untouched — you have to assign
  the result to something and then use that.
- **`SyntaxError: f-string: expecting '}'`.** A brace is unbalanced, or you
  nested the same kind of quote inside the f-string. Use `f"...{name}..."`
  with double quotes outside and no quotes inside.
- **`NameError: name 'DEFAULT_LANGUAGE' is not defined`.** The constant is
  defined below the function that uses it, or it is spelled differently in the
  two places. Constants go at the top of the file, under the docstring, in
  `SCREAMING_SNAKE_CASE`.
- **`python: command not found` or the wrong Python runs.** Your virtual
  environment is not active. Re-run the activate command from step 2 and check
  that your prompt shows `(.venv)`.

## When you are done

Tick these off against the mini-project's own checklist before you call it
finished.

- [ ] `python hello_you.py` runs with no traceback and exits on its own.
- [ ] It prompts for a name and for an optional language.
- [ ] The greeting contains both the name and the language, worded exactly as
      the spec shows.
- [ ] Whitespace-only input for either question falls back to the default.
- [ ] Both functions carry type hints and a docstring, and no `TODO` comments
      are left in the file.
- [ ] The entry point sits inside `if __name__ == "__main__":`.
- [ ] The project lives in its own `hello-you/` folder with a `.venv/` that
      Git is not tracking.
- [ ] `.gitignore` lists at least `.venv/`, `__pycache__/`, and `.DS_Store`.
- [ ] A user-facing `README.md` explains what the program does and how to run
      it.
- [ ] The repository is on GitHub, public, with at least three commits that
      say what changed.
- [ ] Committed and pushed:

      ```bash
      git add hello_you.py
      git commit -m "Implement prompt_user and build_greeting"
      git push
      ```

Then paste the repository URL into your Week 1 notes. You will want it in
Week 2, and future you will want it long after that.
