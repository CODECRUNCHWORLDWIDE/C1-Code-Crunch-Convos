"""Print three facts about the author: name, food, and a course goal.

Week 1 homework, problem 3, Code Crunch Convos. Three lines out, no input
in. Save your own copy as ``about_me.py`` in your homework repository.
"""

# Edit these three strings and nothing else. Keeping the data at the top
# means the printing code below never has to change.
NAME: str = "Ada Lovelace"
FAVORITE_FOOD: str = "cold sesame noodles"
COURSE_GOAL: str = "automate the boring parts of my job with Python"


def main() -> None:
    """Print exactly three lines, one fact per line."""
    # One print() per fact, so the output is three lines even if a fact
    # is empty -- print() with no arguments still ends the line.
    print(f"My name is {NAME}.")
    print(f"My favorite food is {FAVORITE_FOOD}.")
    print(f"My goal for this course is to {COURSE_GOAL}.")


if __name__ == "__main__":
    main()
