"""Reverse the digits of a non-negative integer.

Week 3 homework, problem 3, Code Crunch Convos.

Arithmetic only: the digits are peeled off with ``% 10`` and ``// 10``
and rebuilt with an accumulator. There is no ``str()`` anywhere in the
answer, which is the whole point of the exercise.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-03-reverse-number.py``, write
``input("Enter a non-negative integer: ")`` instead.

Questions go to the error stream and the result goes to the normal output
stream, so ``python homework-03-reverse-number.py > result.txt`` saves the
answer and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_NUMBER: str = "1200"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read a number, refusing anything that is not a whole number.
while True:
    raw = ask("Enter a non-negative integer: ", DEMO_NUMBER).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number:
        number = int(raw)
        break
    print("Please type a non-negative whole number, like 12345.")

remaining = number
reversed_number = 0

while remaining > 0:
    digit = remaining % 10           # last digit
    reversed_number = reversed_number * 10 + digit
    remaining = remaining // 10      # drop that digit

print(f"Reversed: {reversed_number}")
