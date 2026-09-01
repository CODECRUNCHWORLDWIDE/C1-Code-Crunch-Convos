"""Mad Libs generator using input() and f-strings.

Challenge 2, Week 2, Code Crunch Convos. Prompts for seven words,
strips the whitespace off each one, echoes them back, and prints the
finished story as a single multi-line f-string.

The questions go to the error stream and the story goes to the normal
output stream, so ``python madlibs.py > story.txt`` saves the story and
nothing else. When the input stream is already finished -- which is what
happens when a checker runs the file -- each question answers itself
from the demo words below instead of waiting for typing that is never
coming. The first demo word carries two leading spaces on purpose, so
the automatic run proves the stripping works with nobody typing.

Run it with::

    python madlibs.py
"""

import sys

DEMO_ADJECTIVE: str = "  spectacular"
DEMO_PLURAL_NOUN: str = "ferrets"
DEMO_PLACE: str = "Brooklyn"
DEMO_VERB_ING: str = "juggling"
DEMO_FAMOUS_PERSON: str = "Grace Hopper"
DEMO_NUMBER: str = "7"
DEMO_FOOD: str = "tacos"


def ask(prompt: str, demo: str) -> str:
    """Return the answer to ``prompt``, or ``demo`` when nobody answers.

    Args:
        prompt: the question to show, including its trailing space.
        demo: the answer to fall back on when the input stream has
            already ended.

    Returns:
        The line that was typed, or ``demo``. A demo answer is echoed
        after the prompt on the normal output stream, so the printed
        session reads the same whether a person answered or not.
    """
    print(prompt, end="", file=sys.stderr, flush=True)
    try:
        return input()
    except EOFError:
        print(f"{prompt}{demo}")
        return demo


def main() -> None:
    """Collect the seven words and print the story."""
    adjective = ask("Give me an adjective: ", DEMO_ADJECTIVE).strip()
    plural_noun = ask("Give me a plural noun: ", DEMO_PLURAL_NOUN).strip()
    place = ask("Name a place: ", DEMO_PLACE).strip()
    verb_ing = ask("A verb ending in -ing: ", DEMO_VERB_ING).strip()
    famous_person = ask(
        "A famous person's name: ", DEMO_FAMOUS_PERSON
    ).strip()
    number = ask("A number: ", DEMO_NUMBER).strip()
    food = ask("A type of food: ", DEMO_FOOD).strip()

    print(f"Got {adjective!r}")
    print(f"Got {plural_noun!r}")
    print(f"Got {place!r}")
    print(f"Got {verb_ing!r}")
    print(f"Got {famous_person!r}")
    print(f"Got {number!r}")
    print(f"Got {food!r}")

    story = f"""=== Your Mad Libs Story ===

One sunny morning, a very {adjective} group of {plural_noun} decided
to visit {place}. They spent the day {verb_ing} and pretending to be
{famous_person}. After about {number} hours, everyone was hungry, so
they shared a giant plate of {food} and went home with a great story
to tell.

=== The End ==="""

    print(story)


if __name__ == "__main__":
    main()
