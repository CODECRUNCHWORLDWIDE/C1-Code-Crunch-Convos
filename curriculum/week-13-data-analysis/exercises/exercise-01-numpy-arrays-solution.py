"""exercise-01-numpy-arrays.py — vector math on ten days of solar output.

Reports totals, averages, the best day, and above-average days using
NumPy array operations only. No Python loops.
"""

import numpy as np

SOLAR_LOG: dict[str, list[int]] = {
    "day":       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "kwh":       [18, 23, 19, 24, 21, 17, 23, 20, 26, 17],
    "cloud_pct": [40, 10, 35, 5, 20, 55, 10, 30, 0, 60],
}

RATE_PER_KWH = 0.18


def main() -> None:
    """Print the nine report lines described in the exercise brief."""
    days = np.array(SOLAR_LOG["day"])
    kwh = np.array(SOLAR_LOG["kwh"])
    cloud = np.array(SOLAR_LOG["cloud_pct"])

    print(f"Readings: {kwh}")
    print(f"dtype={kwh.dtype}  shape={kwh.shape}  ndim={kwh.ndim}")

    total = kwh.sum()
    mean = kwh.mean()
    print(f"Total: {total} kWh")
    print(f"Mean: {mean:.2f} kWh")

    best = np.argmax(kwh)
    print(f"Best day: day {days[best]} ({kwh[best]} kWh, {cloud[best]}% cloud)")

    revenue = (kwh * RATE_PER_KWH).sum()
    print(f"Revenue at ${RATE_PER_KWH}/kWh: ${revenue:.2f}")

    deviation = kwh - mean
    print(f"Deviation from mean: {np.round(deviation, 1).tolist()}")

    above = kwh > mean
    print(f"Above-average days: {above.sum()} of {kwh.size}")
    print(f"Above-average mean: {kwh[above].mean():.2f} kWh")


if __name__ == "__main__":
    main()
