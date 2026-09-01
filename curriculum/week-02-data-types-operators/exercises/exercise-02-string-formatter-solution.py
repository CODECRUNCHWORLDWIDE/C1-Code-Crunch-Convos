"""exercise-02-string-formatter-solution.py — print an aligned fixed-width report.

Week 2, Exercise 2. Practises f-strings, field widths, alignment, fill
characters, thousands separators, and the percentage format type.
"""

REPORT_WIDTH: int = 29
TITLE: str = "Weekly Lab Minutes"

NAME_WIDTH: int = 14
MINUTES_WIDTH: int = 7
SHARE_WIDTH: int = 8


def title_bar(title: str) -> str:
    """Return the title centred in REPORT_WIDTH and padded with '='.

    One space sits on each side of the title before padding, so the text
    never touches the '=' characters.
    """
    spaced: str = f" {title} "
    return f"{spaced:=^{REPORT_WIDTH}}"


def format_row(name: str, minutes: int, share: float) -> str:
    """Return one report row, exactly REPORT_WIDTH characters long.

    Name left-aligned in NAME_WIDTH; minutes right-aligned in
    MINUTES_WIDTH with a thousands separator; share (a fraction such as
    0.4706) right-aligned in SHARE_WIDTH as a percentage with one
    decimal place.
    """
    return (f"{name:<{NAME_WIDTH}}"
            f"{minutes:>{MINUTES_WIDTH},}"
            f"{share:>{SHARE_WIDTH}.1%}")


def main() -> None:
    """Print the whole report."""
    ada_minutes: int = 1_240
    grace_minutes: int = 980
    alan_minutes: int = 415
    total_minutes: int = ada_minutes + grace_minutes + alan_minutes

    print(title_bar(TITLE))
    print(f"{'Member':<{NAME_WIDTH}}"
          f"{'Minutes':>{MINUTES_WIDTH}}"
          f"{'Share':>{SHARE_WIDTH}}")
    print("-" * REPORT_WIDTH)
    print(format_row("Ada Lovelace", ada_minutes, ada_minutes / total_minutes))
    print(format_row("Grace Hopper", grace_minutes, grace_minutes / total_minutes))
    print(format_row("Alan Turing", alan_minutes, alan_minutes / total_minutes))
    print("-" * REPORT_WIDTH)
    print(format_row("TOTAL", total_minutes, 1.0))


if __name__ == "__main__":
    main()
