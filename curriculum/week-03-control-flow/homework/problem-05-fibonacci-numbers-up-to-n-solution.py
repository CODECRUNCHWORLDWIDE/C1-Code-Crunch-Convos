"""Print every Fibonacci number less than or equal to N.

Week 3 homework, problem 5, Code Crunch Convos.

The sequence starts 0, 1, 1, 2, 3, 5, 8, 13 and each term is the sum of
the two before it. Two variables hold the whole state, and one tuple
assignment moves both forward at once.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-05-fibonacci.py``, write ``input("Enter N: ")`` instead.

Questions go to the error stream and the numbers go to the normal output
stream, so ``python homework-05-fibonacci.py > fib.txt`` saves the
sequence and not the question.
"""

import sys

DIGITS: str = "0123456789"
DEMO_N: str = "50"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


# Read N, refusing anything that is not a positive whole number.
while True:
    raw = ask("Enter N: ", DEMO_N).strip()
    is_whole_number = raw != ""
    for ch in raw:
        if ch not in DIGITS:
            is_whole_number = False
            break
    if is_whole_number and int(raw) >= 1:
        n = int(raw)
        break
    print("Please type a positive whole number, like 50.")

a, b = 0, 1
while a <= n:
    print(a)
    a, b = b, a + b
