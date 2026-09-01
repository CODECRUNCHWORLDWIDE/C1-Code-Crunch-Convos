"""Sum the digits of a non-negative integer.

Week 3 homework, problem 4, Code Crunch Convos.

The same conveyor belt as problem 3 - ``% 10`` to read the last digit,
``// 10`` to drop it - with a plainer accumulator: add the digit instead
of shifting the total left first.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-04-sum-digits.py``, write
``input("Enter a non-negative integer: ")`` instead.

Questions go to the error stream and the total goes to the normal output
stream, so ``python homework-04-sum-digits.py > total.txt`` saves the
answer and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_NUMBER: str = "12345"


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
digit_sum = 0

while remaining > 0:
    digit_sum += remaining % 10
    remaining = remaining // 10

print(f"Sum of digits: {digit_sum}")
