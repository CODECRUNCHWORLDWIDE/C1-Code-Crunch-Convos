"""The nine tests, in the order they were written.

Each test failed for the right reason before the corresponding production code
existed. Read them top to bottom and you are reading the TDD session.
"""

from __future__ import annotations

import pytest

from fizzbuzz import fizzbuzz


def test_returns_a_list() -> None:
    assert isinstance(fizzbuzz(1), list)


def test_length_matches_n() -> None:
    assert len(fizzbuzz(5)) == 5


def test_plain_numbers() -> None:
    assert fizzbuzz(2) == ["1", "2"]


def test_three_is_fizz() -> None:
    assert fizzbuzz(3)[2] == "Fizz"


def test_five_is_buzz() -> None:
    assert fizzbuzz(5)[4] == "Buzz"


def test_fifteen_is_fizzbuzz() -> None:
    assert fizzbuzz(15)[14] == "FizzBuzz"


def test_full_output_to_fifteen() -> None:
    assert fizzbuzz(15) == [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
    ]


def test_zero_returns_empty_list() -> None:
    assert fizzbuzz(0) == []


def test_negative_raises_value_error() -> None:
    with pytest.raises(ValueError, match="must be non-negative"):
        fizzbuzz(-1)
