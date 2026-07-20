# Challenge 1 — Personalized ASCII Banner

**Estimated time:** 30–60 minutes

## The Brief

Write a Python script called `banner.py` that asks the user for their
name, then prints a banner with the name **centered** inside a box of
ASCII characters. The banner should look something like this when the
user types `Ada`:

```text
*****************
*               *
*      Ada      *
*               *
*****************
```

## Functional Requirements

Your script must:

1. Prompt for a name using the built-in `input()` function.
2. Strip leading and trailing whitespace from the user's input.
3. Print a rectangular banner where:
   - The top and bottom borders are rows of `*` characters.
   - The left and right borders are also `*` characters.
   - There is one empty padded row above and below the name.
   - The name is centered horizontally inside the banner.
4. The banner width should adapt to the length of the name (at minimum
   the name length plus six characters of padding).

## Technical Requirements

- The file must include a module-level docstring at the top describing
  the script.
- Use **type hints** on every function signature.
- Use an `if __name__ == "__main__":` guard so the script can also be
  imported without auto-running.
- Use the `str.center()` method to handle the centering — do **not**
  manually count spaces.

## Hints

- `input("Your name: ")` returns whatever the user typed, as a string.
- `"Ada".center(15, " ")` returns `'      Ada      '` (length 15).
- `"*" * 17` returns 17 stars in a row.
- An f-string lets you embed values in a string: `f"*{padded}*"`.

## Suggested Skeleton

```python
"""banner.py — print a centered ASCII banner."""


def build_banner(name: str, padding: int = 6) -> str:
    """Return the multi-line banner for ``name`` as one big string."""
    # TODO: compute inner_width, build the four kinds of row, join them.
    ...


def main() -> None:
    raw: str = input("Your name: ")
    name: str = raw.strip()
    if not name:
        print("(no name provided)")
        return
    print(build_banner(name))


if __name__ == "__main__":
    main()
```

## Stretch Goals

If you finish quickly, try one or more of these:

- Accept the name from the command line instead: `python banner.py Ada`
  using `sys.argv`.
- Allow the user to choose the border character (`*`, `#`, `=`, …).
- Read multiple names from a text file, one per line, and print a banner
  for each.
- Use the `colorama` package (install it with `python -m pip install
  colorama`) to print the banner in color, and add the package to your
  `requirements.txt`.

## Acceptance Checklist

- [ ] Script runs without errors when given a typical name.
- [ ] Script handles a name with surrounding spaces (`"  Ada  "`).
- [ ] Banner adapts to short and long names.
- [ ] Code passes a quick read for PEP 8 style (4-space indentation,
      `snake_case` function names).
- [ ] You have committed the file to Git with a clear message such as
      `Add Challenge 1: personalized ASCII banner`.
