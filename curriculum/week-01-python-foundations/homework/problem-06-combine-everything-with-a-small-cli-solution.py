"""Ask for a name and three tasks, then print a numbered plan.

Week 1 homework, problem 6, Code Crunch Convos. Everything typed is
stripped of surrounding whitespace before it is used or printed. Save
your own copy as ``day_planner.py`` in your homework repository.

Prompts go to the error stream and the plan goes to the normal output
stream, so ``python day_planner.py > plan.txt`` saves the plan and
nothing else. When nobody is at the keyboard, the script prints a
built-in example rather than waiting for typing that is never coming.
"""

import sys

TASK_COUNT: int = 3
SAMPLE_NAME: str = "  Ada  "
SAMPLE_TASKS: list[str] = [
    "  ship the mini-project ",
    "read PEP 8",
    "walk the dog  ",
]


def someone_is_typing() -> bool:
    """Return True when standard input is a real interactive terminal."""
    return sys.stdin is not None and sys.stdin.isatty()


def ask(prompt: str) -> str:
    """Show ``prompt``, then return the typed answer without padding."""
    print(prompt, end="", file=sys.stderr, flush=True)
    return input().strip()


def prompt_name() -> str:
    """Return the typed name with surrounding whitespace removed."""
    return ask("What is your name? ")


def prompt_tasks(count: int = TASK_COUNT) -> list[str]:
    """Return ``count`` stripped task strings, asking once per task."""
    tasks: list[str] = []
    for number in range(1, count + 1):
        tasks.append(ask(f"Task {number}: "))
    return tasks


def print_plan(name: str, tasks: list[str]) -> None:
    """Print the header line, then one numbered line per task."""
    print(f"Today, {name}:")
    for index, task in enumerate(tasks, start=1):
        print(f"  {index}. {task}")


def main() -> None:
    """Collect a name and three tasks, then print the numbered plan."""
    name: str = SAMPLE_NAME.strip()
    tasks: list[str] = [task.strip() for task in SAMPLE_TASKS]
    if someone_is_typing():
        try:
            name = prompt_name()
            tasks = prompt_tasks()
        except EOFError:
            print("\nNo input; showing the example plan.", file=sys.stderr)
    print_plan(name, tasks)


if __name__ == "__main__":
    main()
