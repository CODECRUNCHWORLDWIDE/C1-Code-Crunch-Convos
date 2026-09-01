"""Count the vowels in a sentence.

Week 3 homework, problem 2, Code Crunch Convos.

Vowels are a, e, i, o and u, and the count is case-insensitive, so A and
a are the same letter.

The answer itself uses no functions and no ``try``/``except`` - those are
Week 4 and Week 6. The one ``def`` in this file is ``ask``, and it is not
part of the answer: it is the question-asking shim that lets the download
run when nobody is at the keyboard. In your own copy, saved as
``homework-02-count-vowels.py``, write ``input("Enter a sentence: ")``
instead.

Questions go to the error stream and the count goes to the normal output
stream, so ``python homework-02-count-vowels.py > count.txt`` saves the
answer and not the question.
"""

import sys

VOWELS: str = "aeiou"
DEMO_SENTENCE: str = "Hello, World!"


def ask(prompt: str, demo: str) -> str:
    """Read one answer. Falls back to ``demo`` when nobody is typing."""
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


text = ask("Enter a sentence: ", DEMO_SENTENCE)

# The counting pattern: start at zero outside the loop, add one inside.
count = 0
for ch in text.lower():
    if ch in VOWELS:
        count += 1

print(f"That sentence has {count} vowel(s).")
