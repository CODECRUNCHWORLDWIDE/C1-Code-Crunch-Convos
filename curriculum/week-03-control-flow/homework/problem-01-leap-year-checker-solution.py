"""Leap year checker.

Week 3 homework, problem 1, Code Crunch Convos.

A year is a leap year when it divides by 4, except centuries, which are
leap years only when they divide by 400.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-01-leap-year.py``, write ``input("Enter a year: ")`` instead.

Questions go to the error stream and the verdict goes to the normal
output stream, so ``python homework-01-leap-year.py > verdict.txt`` saves
the answer and not the questions.
"""

import sys

DIGITS: str = "0123456789"
DEMO_YEAR: str = "1900"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read a year, refusing anything that is not a whole number.
while True:
    raw = ask("Enter a year: ", DEMO_YEAR).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        year = int(raw)
        break
    print("Please type a year as a whole number, like 2024.")

# The Gregorian rule, most specific test first.
if year % 400 == 0:
    is_leap = True
elif year % 100 == 0:
    is_leap = False
elif year % 4 == 0:
    is_leap = True
else:
    is_leap = False

if is_leap:
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")
