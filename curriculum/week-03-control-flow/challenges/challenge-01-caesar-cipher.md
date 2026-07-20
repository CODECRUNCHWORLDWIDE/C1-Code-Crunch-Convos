# Challenge 01 — Caesar Cipher

Build a tiny command-line tool that encodes and decodes text using a
**Caesar cipher** — one of the oldest known ciphers, attributed to
Julius Caesar himself. It is not real cryptography (it is trivially
breakable), but it is a perfect exercise for loops, string indexing, and
the modulo operator.

## The idea

Each letter in the alphabet is shifted by a fixed amount. With a shift
of 3:

- `A` → `D`
- `B` → `E`
- `Z` → `C`   (it wraps around)
- non-letters (digits, spaces, punctuation) are left untouched

To decode, shift in the opposite direction (or by `26 - shift`).

## Requirements

Save your solution as `challenge-01-caesar-cipher.py` in this folder.

1. The program prompts the user for:
   - a **mode**: `encode` or `decode`
   - a **shift** (an integer, any value — positive, zero, or negative)
   - a **message** (a single line of text)
2. It then prints the transformed message.
3. **Uppercase stays uppercase**, **lowercase stays lowercase**, and any
   character that is not a letter is copied through unchanged.
4. The shift must wrap modulo 26: a shift of `3` and a shift of `29`
   must produce the same output.
5. After printing, the program asks "encode another? (y/n)" and loops
   if the answer is `y`, otherwise exits with a friendly goodbye.

## Sample session

```text
Mode (encode/decode): encode
Shift: 3
Message: Hello, World!
Result:  Khoor, Zruog!
Encode another? (y/n) y

Mode (encode/decode): decode
Shift: 3
Message: Khoor, Zruog!
Result:  Hello, World!
Encode another? (y/n) n
Bye!
```

## Hints

- `ord('A')` is `65`, `ord('a')` is `97`. `chr(...)` is the inverse.
- For an uppercase letter `c`, its 0-based position is `ord(c) - 65`.
  Apply the shift, take `% 26`, add `65` back, convert with `chr`.
- Handle `decode` by treating it as encode with a negative shift.
- `str.isupper()`, `str.islower()`, and `str.isalpha()` are your
  friends.
- Build the output with a list and `"".join(...)` at the end (see
  Lecture 3) — this is exactly the situation where building a string
  with `+=` would be slow.

## Acceptance criteria

- Encoding `"abc"` with shift `1` returns `"bcd"`.
- Encoding `"xyz"` with shift `3` returns `"abc"` (wrap-around).
- Encoding `"Hello, World!"` with shift `13` and then decoding the
  result with shift `13` returns the original string.
- A shift of `0` returns the input unchanged.
- A shift of `-3` decodes what `+3` encoded.

## Stretch goals

- Add a "brute force" mode that prints all 26 possible decodings of a
  message — useful when you don't know the shift.
- Read the message from a file (`open(...)`, Week 6 preview) and write
  the result to another file.
- Replace the prompt with `argparse` (Week 4 preview).
