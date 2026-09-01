"""BMI calculator with no ``if`` statement in the answer.

Week 2 homework, problem 2, Code Crunch Convos.
BMI = weight_kg / (height_m ** 2)

The four categories are printed as plain True/False flags, because ``if`` is
a Week 3 topic. Questions go to the error stream so the flags on the normal
output stream stay clean enough to redirect into a file. When nobody is at
the keyboard the script uses the example figures. Save your own copy as
``homework-02-bmi.py``.
"""

import sys

LABEL_WIDTH: int = 12
UNDERWEIGHT_MAX: float = 18.5
NORMAL_MAX: float = 25.0
OVERWEIGHT_MAX: float = 30.0

SAMPLE_WEIGHT_KG: str = "70"
SAMPLE_HEIGHT_M: str = "1.74"


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str, fallback: str) -> str:
    """Return the typed line, or ``fallback`` when nobody is at the keyboard."""
    if not someone_is_typing():
        return fallback
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        return fallback


def print_report(weight_kg: float, height_m: float) -> None:
    """Print the BMI and one True/False flag per category."""
    bmi: float = weight_kg / (height_m ** 2)

    underweight: bool = bmi < UNDERWEIGHT_MAX
    normal: bool = UNDERWEIGHT_MAX <= bmi < NORMAL_MAX
    overweight: bool = NORMAL_MAX <= bmi < OVERWEIGHT_MAX
    obese: bool = bmi >= OVERWEIGHT_MAX

    print(f"BMI: {bmi:.1f}")
    print(f"{'Underweight':<{LABEL_WIDTH}}: {underweight}")
    print(f"{'Normal':<{LABEL_WIDTH}}: {normal}")
    print(f"{'Overweight':<{LABEL_WIDTH}}: {overweight}")
    print(f"{'Obese':<{LABEL_WIDTH}}: {obese}")


def main() -> None:
    """Read weight and height, print the BMI and four category flags."""
    weight_kg: float = float(ask("Weight in kilograms: ", SAMPLE_WEIGHT_KG))
    height_m: float = float(ask("Height in meters: ", SAMPLE_HEIGHT_M))
    print_report(weight_kg, height_m)


if __name__ == "__main__":
    main()
