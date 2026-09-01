"""exercise-03-password-checker-solution.py — retry loop with a full problem report.

Prompts until the typed password satisfies every rule, listing all the
rules it breaks on each attempt.

Two ways to run it:

    python exercise-03-password-checker-solution.py         walks the sample session
    python exercise-03-password-checker-solution.py --ask   asks you to type

The sample session is the default so that a run with nobody at the
keyboard prints the same six lines every time instead of waiting for
typing that is never coming.

The prompt and the password go to stderr; only the verdict goes to
stdout. That is why `python … > report.txt` saves the verdict and never
saves a password.
"""

import sys

MIN_LENGTH = 12
BLOCKLIST = ("password1234", "qwertyuiop12", "letmein12345")

ASK_FLAG = "--ask"
PROMPT = "> "
DEMO_ATTEMPTS = ("crunch", "123456789012", "letmein12345", "crunchtime12")
DEMO_NOTE = f"Walking the sample session. Pass {ASK_FLAG} to type your own."
DEMO_EXHAUSTED = "Sample session ran out with nothing acceptable in it."


def find_problems(candidate: str) -> list[str]:
    """Return a list of human-readable reasons `candidate` is unacceptable.

    An empty list means the candidate passed every rule.
    """
    problems: list[str] = []
    if len(candidate) < MIN_LENGTH:
        problems.append(
            f"Too short: {len(candidate)} characters, minimum is {MIN_LENGTH}."
        )
    if not any(ch.isdigit() for ch in candidate):
        problems.append("No digits: add at least one 0-9.")
    if not any(ch.isalpha() for ch in candidate):
        problems.append("No letters: add at least one A-Z or a-z.")
    if candidate.lower() in BLOCKLIST:
        problems.append(
            "That password is on the community blocklist. Pick something else."
        )
    return problems


def read_candidate(attempt: int, interactive: bool) -> str:
    """Return the password for this attempt, typed or scripted.

    `attempt` is 1 on the first pass, 2 on the second, and so on. The
    prompt and the scripted answer both go to stderr, so no password
    ever reaches stdout.
    """
    print(PROMPT, end="", file=sys.stderr, flush=True)
    if interactive:
        return input()
    scripted = DEMO_ATTEMPTS[attempt - 1]
    print(scripted, file=sys.stderr)
    return scripted


def main() -> None:
    """Prompt until the password is acceptable, then report the attempt count."""
    interactive = ASK_FLAG in sys.argv[1:]
    if not interactive:
        print(DEMO_NOTE, file=sys.stderr)

    print("Choose a password. It is never printed back to you.")
    attempts = 0

    while True:
        if not interactive and attempts == len(DEMO_ATTEMPTS):
            print(DEMO_EXHAUSTED)
            break

        attempts += 1
        candidate = read_candidate(attempts, interactive)
        problems = find_problems(candidate)

        if problems:
            for problem in problems:
                print(f"  - {problem}")
            continue

        print(f"Password accepted after {attempts} attempts.")
        break


if __name__ == "__main__":
    main()
