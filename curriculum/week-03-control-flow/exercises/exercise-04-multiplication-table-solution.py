"""exercise-04-multiplication-table-solution.py — nested loops and aligned columns.

Prints an aligned N-by-N multiplication table with header row, header
column, and a separator rule.
"""

TABLE_SIZE = 12
CELL_WIDTH = 4


def build_row(row: int, size: int) -> str:
    """Return one body row of the table, header cell included.

    Example for row 3 of a 5-wide table:
    "   3 |   3   6   9  12  15"
    """
    line = f"{row:>{CELL_WIDTH}} |"
    for column in range(1, size + 1):
        line += f"{row * column:>{CELL_WIDTH}}"
    return line


def build_header(size: int) -> str:
    """Return the header row: an 'x' corner cell then 1 through size."""
    line = f"{'x':>{CELL_WIDTH}} |"
    for column in range(1, size + 1):
        line += f"{column:>{CELL_WIDTH}}"
    return line


def build_rule(size: int) -> str:
    """Return the separator rule that sits under the header."""
    return "-" * (CELL_WIDTH + 1) + "+" + "-" * (CELL_WIDTH * size)


def main() -> None:
    """Print the header, the rule, and every body row."""
    print(build_header(TABLE_SIZE))
    print(build_rule(TABLE_SIZE))
    for row in range(1, TABLE_SIZE + 1):
        print(build_row(row, TABLE_SIZE))


if __name__ == "__main__":
    main()
