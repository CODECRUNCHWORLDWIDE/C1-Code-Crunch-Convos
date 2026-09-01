"""exercise-05-import-and-use-solution.py — one afternoon at the community garden.

Four functions, and the body of every one is a single call into a module that
already ships with Python. No pip install, no hand-rolled formulas.

One line differs from the starter: `random.seed(2026)` at the top of the
__main__ block, so this published file prints the same trial plots every
time. Your own file has no seed and prints a different line each run, which
is what `random.sample` is for. Seeding lives in __main__ and never inside a
function -- the page explains why.
"""

import math
import random
import statistics
from math import isclose

RAINFALL_MM = [12.4, 8.1, 15.0, 9.6, 11.2, 8.1, 20.3]
PLOTS = ["Plot A", "Plot B", "Plot C", "Plot D", "Plot E", "Plot F"]


def circle_bed_area(diameter_m: float) -> float:
    """Return the area of a round planting bed, in square meters.

    Args:
        diameter_m: The bed's diameter in meters.

    Returns:
        The area, rounded to two decimals.
    """
    radius_m = diameter_m / 2
    return round(math.pi * radius_m**2, 2)


def bags_of_compost(area_m2: float, coverage_m2: float = 4.0) -> int:
    """Return how many whole bags of compost it takes to cover `area_m2`."""
    return math.ceil(area_m2 / coverage_m2)


def rainfall_summary(readings: list[float]) -> dict[str, float]:
    """Return mean, median, mode and sample stdev of `readings`, each to 2 dp.

    Args:
        readings: Daily rainfall in millimetres. At least two values.

    Returns:
        A dict with keys "mean", "median", "mode", "stdev".
    """
    return {
        "mean": round(statistics.mean(readings), 2),
        "median": round(statistics.median(readings), 2),
        "mode": round(statistics.mode(readings), 2),
        "stdev": round(statistics.stdev(readings), 2),
    }


def pick_trial_plots(plots: list[str], k: int) -> list[str]:
    """Return `k` distinct plots chosen at random for this week's trial."""
    return random.sample(plots, k)


if __name__ == "__main__":
    random.seed(2026)

    assert isclose(circle_bed_area(3.0), 7.07), circle_bed_area(3.0)
    assert isclose(circle_bed_area(1.0), 0.79), circle_bed_area(1.0)
    assert isclose(circle_bed_area(0.0), 0.0), circle_bed_area(0.0)

    assert bags_of_compost(7.07) == 2, bags_of_compost(7.07)
    assert bags_of_compost(8.0) == 2, bags_of_compost(8.0)
    assert bags_of_compost(8.01) == 3, bags_of_compost(8.01)
    assert bags_of_compost(0.0) == 0, bags_of_compost(0.0)
    assert bags_of_compost(10.0, coverage_m2=5.0) == 2

    summary = rainfall_summary(RAINFALL_MM)
    assert isclose(summary["mean"], 12.1), summary
    assert isclose(summary["median"], 11.2), summary
    assert isclose(summary["mode"], 8.1), summary
    assert isclose(summary["stdev"], 4.37), summary

    trial = pick_trial_plots(PLOTS, 3)
    assert len(trial) == 3, trial
    assert len(set(trial)) == 3, "a plot cannot be in the trial twice"
    assert set(trial) <= set(PLOTS), trial

    bed = circle_bed_area(3.0)
    print(f"Round bed, 3.0 m across: {bed} m2")
    print(f"Compost bags needed: {bags_of_compost(bed)}")
    print(
        f"Rainfall: mean {summary['mean']} mm, median {summary['median']} mm, "
        f"mode {summary['mode']} mm, stdev {summary['stdev']} mm"
    )
    print(f"Trial plots this week: {trial}")
    print("All checks passed.")
