"""Exercise 01 — NumPy arrays, vector math, broadcasting.

Goal
----
Practise the three core NumPy moves you will use every day this week:

1. Creating arrays from Python lists and from NumPy generators.
2. Doing element-wise (vectorized) math without writing a Python loop.
3. Combining arrays of different but compatible shapes with broadcasting.

How to run
----------
    python exercise-01-numpy-arrays.py

You should see the script print a series of labelled outputs. Compare them
against the `# Expected:` comments. Fill in the `# YOUR CODE HERE` blocks
until every comparison passes.
"""

from __future__ import annotations

import numpy as np


def part_1_create_arrays() -> None:
    """Create arrays from lists and from NumPy helpers."""

    print("\n--- Part 1: Creating arrays ---")

    # 1a. Turn the Python list below into a NumPy array.
    py_list: list[int] = [2, 4, 6, 8, 10]
    arr: np.ndarray = np.array(py_list)
    print("1a. arr      =", arr)
    print("    dtype    =", arr.dtype)
    print("    shape    =", arr.shape)
    # Expected: arr = [ 2  4  6  8 10], dtype int64, shape (5,)

    # 1b. Build an array of the integers from 0 to 19 inclusive.
    #     Use np.arange.
    # YOUR CODE HERE
    zero_to_nineteen: np.ndarray = np.arange(20)
    print("1b. 0..19    =", zero_to_nineteen)
    # Expected: 0..19 = [ 0  1  2 ... 18 19]

    # 1c. Build an array of 5 evenly spaced numbers from 0.0 to 1.0.
    #     Use np.linspace.
    # YOUR CODE HERE
    five_points: np.ndarray = np.linspace(0.0, 1.0, 5)
    print("1c. linspace =", five_points)
    # Expected: [0. 0.25 0.5 0.75 1.]

    # 1d. Build a 3x4 array of zeros and a 3x4 array of ones.
    # YOUR CODE HERE
    zeros: np.ndarray = np.zeros((3, 4))
    ones: np.ndarray = np.ones((3, 4))
    print("1d. zeros.shape =", zeros.shape, "ones.shape =", ones.shape)
    # Expected: zeros.shape = (3, 4) ones.shape = (3, 4)


def part_2_vector_math() -> None:
    """Use vectorized arithmetic instead of a Python loop."""

    print("\n--- Part 2: Vector math ---")

    prices: np.ndarray = np.array([9.99, 19.95, 4.50, 29.99, 14.50])

    # 2a. Compute a "with tax" array using an 8% sales tax — no Python loop.
    # YOUR CODE HERE
    with_tax: np.ndarray = prices * 1.08
    print("2a. with_tax =", np.round(with_tax, 2))
    # Expected: [10.79 21.55  4.86 32.39 15.66]

    # 2b. Compute the total, mean, max, and min of `prices` in one line each.
    # YOUR CODE HERE
    total: float = prices.sum()
    avg: float = prices.mean()
    largest: float = prices.max()
    smallest: float = prices.min()
    print(f"2b. total={total:.2f}  avg={avg:.2f}  max={largest:.2f}  min={smallest:.2f}")
    # Expected: total=78.93  avg=15.79  max=29.99  min=4.50


def part_3_broadcasting() -> None:
    """Combine arrays of different shapes with broadcasting."""

    print("\n--- Part 3: Broadcasting ---")

    # A 4x3 matrix of test scores: 4 students, 3 exams.
    scores: np.ndarray = np.array(
        [
            [82, 91, 76],   # Ada
            [65, 70, 72],   # Bo
            [88, 85, 90],   # Cara
            [50, 55, 60],   # Dee
        ]
    )

    # 3a. Compute each *exam's* mean (one number per column).
    #     Hint: axis=0 means "collapse rows".
    # YOUR CODE HERE
    exam_means: np.ndarray = scores.mean(axis=0)
    print("3a. exam_means =", exam_means)
    # Expected: [71.25 75.25 74.5 ]

    # 3b. Subtract each exam's mean from every student's score for that exam.
    #     This is broadcasting in action: shape (4, 3) - shape (3,) → (4, 3).
    # YOUR CODE HERE
    centered: np.ndarray = scores - exam_means
    print("3b. centered:\n", centered)
    # Expected: a 4x3 array of values centered on 0 per column.

    # 3c. Compute each *student's* mean (one number per row).
    # YOUR CODE HERE
    student_means: np.ndarray = scores.mean(axis=1)
    print("3c. student_means =", student_means)
    # Expected: [83.0 69.0 87.66... 55.0]

    # 3d. Identify students whose mean is above 75 using a boolean mask.
    # YOUR CODE HERE
    passing: np.ndarray = student_means > 75
    print("3d. passing mask =", passing)
    # Expected: [ True False  True False]


def main() -> None:
    """Run all three parts."""
    part_1_create_arrays()
    part_2_vector_math()
    part_3_broadcasting()
    print("\nAll parts ran. Compare the output above to the # Expected: lines.")


if __name__ == "__main__":
    main()
