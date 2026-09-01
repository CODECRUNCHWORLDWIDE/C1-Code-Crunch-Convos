"""Flip a matrix's rows and columns with one nested list comprehension.

Week 5 homework, problem 1, Code Crunch Convos.

Add ``transpose`` to your own ``week-05-solutions.py``. This file is the
published answer, and the longer name keeps it from landing on top of your work.

Read the comprehension from the outside in. The outer clause walks the column
numbers; the inner one walks the rows and picks out the number sitting in that
column. Each finished inner list is one column of the input, which is what a
transpose is.
"""


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return the transpose of a rectangular matrix, as a list comprehension.

    Args:
        matrix: A list of rows. Every row must be the same length.

    Returns:
        A new list of columns. An ``r`` by ``c`` matrix gives back ``c`` lists
        of ``r`` numbers each. An empty matrix gives back an empty list.

    Example:
        >>> transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    if not matrix:
        return []
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def _check() -> None:
    """Run the three asserts the brief requires, plus two it implies."""
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1]]) == [[1]]
    assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
    assert transpose([]) == []
    assert transpose(transpose([[1, 2, 3], [4, 5, 6]])) == [[1, 2, 3], [4, 5, 6]]


def _demo() -> None:
    """Print the brief's three examples, then the empty matrix."""
    print(transpose([[1, 2, 3], [4, 5, 6]]))
    print(transpose([[1]]))
    print(transpose([[1, 2], [3, 4], [5, 6]]))
    print(transpose([]))
    print("All 5 asserts passed.")


if __name__ == "__main__":
    _check()
    _demo()
