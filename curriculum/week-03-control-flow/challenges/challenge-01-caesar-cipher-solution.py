"""Caesar cipher: shift every letter, leave everything else alone.

Challenge 1, Week 3, Code Crunch Convos. Encodes or decodes one line of
text with a Caesar shift. Uppercase stays uppercase, lowercase stays
lowercase, and digits, spaces and punctuation pass straight through.

Week 3 rules: the cipher itself uses no functions -- ``def`` is Week 4 --
and no ``try`` / ``except``, which is Week 6. The one helper below,
``ask()``, is scaffolding rather than part of the answer. It is what lets
this file run and print a whole session when nobody is at the keyboard.

The questions go to the error stream and the results go to the normal
output stream, so ``python caesar.py > out.txt`` saves the results and
none of the questions.

Run it with::

    python caesar.py
"""

import sys

LOWER_A: int = ord("a")  # 97
UPPER_A: int = ord("A")  # 65
DIGITS: str = "0123456789"

# The session this file plays when its input stream is already finished.
DEMO_ANSWERS: list[str] = [
    "encode",
    "3",
    "Hello, World!",
    "y",
    "decode",
    "3",
    "Khoor, Zruog!",
    "n",
]


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or a demo answer when nobody types.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on once the demo script above has
            run out. Every call site passes something that ends the
            program, so the file can never loop forever unattended.

    Returns:
        The line that was typed, or the next demo answer. A demo answer
        is echoed after the prompt on the normal output stream, so the
        printed session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        answer = DEMO_ANSWERS.pop(0) if DEMO_ANSWERS else demo
        print(f"{prompt}{answer}")
        return answer


while True:
    # --- mode ---
    while True:
        mode = ask("Mode (encode/decode): ", "encode").strip().lower()
        if mode in ("encode", "decode"):
            break
        print("Please type 'encode' or 'decode'.")

    # --- shift (a whole number, possibly negative) ---
    while True:
        raw_shift = ask("Shift: ", "0").strip()
        body = raw_shift[1:] if raw_shift[:1] in ("-", "+") else raw_shift
        is_whole_number = body != ""
        for ch in body:
            if ch not in DIGITS:
                is_whole_number = False
                break
        if is_whole_number:
            shift = int(raw_shift)
            break
        print("The shift must be a whole number, like 3, 0 or -3.")

    # Decoding is just encoding by the opposite shift.
    if mode == "decode":
        shift = -shift
    shift %= 26  # 3 and 29 now agree; -3 becomes 23

    # --- transform ---
    message = ask("Message: ", "")
    pieces = []
    for ch in message:
        if "a" <= ch <= "z":
            position = ord(ch) - LOWER_A
            pieces.append(chr((position + shift) % 26 + LOWER_A))
        elif "A" <= ch <= "Z":
            position = ord(ch) - UPPER_A
            pieces.append(chr((position + shift) % 26 + UPPER_A))
        else:
            pieces.append(ch)

    result = "".join(pieces)
    print(f"Result:  {result}")

    again = ask("Encode another? (y/n) ", "n").strip().lower()
    if again not in ("y", "yes"):
        print("Bye!")
        break
    print()
