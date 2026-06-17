# Challenge 02 — Mad Libs Generator

Mad Libs is a classic word game: one player fills in blanks of a story
template with a noun, verb, adjective, and so on — usually before
seeing the surrounding text. The result is often absurd. Your job is to
write a Python script that plays the role of the prompter.

## Goal

Practice reading multiple strings from the user, doing light string
cleanup, and composing a multi-line story with an f-string.

## Specification

### Inputs

Prompt the user, in order, for the following parts of speech. The exact
prompt text is up to you, but it must clearly tell the user what kind
of word to enter:

1. An adjective.
2. A plural noun.
3. A place.
4. A verb ending in ``-ing``.
5. A famous person's name.
6. A number.
7. A type of food.

After each prompt, strip leading and trailing whitespace from the input
using ``.strip()``.

### Output

Compose and print this story, substituting the user's answers into the
bracketed slots. The story must be printed as a single multi-line block
(use a triple-quoted f-string).

```text
=== Your Mad Libs Story ===

One sunny morning, a very {adjective} group of {plural_noun} decided
to visit {place}. They spent the day {verb_ing} and pretending to be
{famous_person}. After about {number} hours, everyone was hungry, so
they shared a giant plate of {food} and went home with a great story
to tell.

=== The End ===
```

### Constraints

- Use exactly one ``print()`` call for the story block (a triple-quoted
  f-string).
- Echo each cleaned input back to the user before showing the story,
  in the form ``"Got 'spectacular'"`` — this confirms the strip worked
  and helps debug spaces.
- The script must be runnable from any directory and not crash on
  empty input (an empty string is allowed; it'll just look funny).

## Suggested Skeleton

```python
"""Mad Libs generator using input() and f-strings."""


def main() -> None:
    adjective = input("Give me an adjective: ").strip()
    plural_noun = input("Give me a plural noun: ").strip()
    place = input("Name a place: ").strip()
    verb_ing = input("A verb ending in -ing: ").strip()
    famous_person = input("A famous person's name: ").strip()
    number = input("A number: ").strip()
    food = input("A type of food: ").strip()

    # TODO: echo each input back as confirmation.

    story = f"""..."""  # TODO: build the multi-line story with f-string

    print(story)


if __name__ == "__main__":
    main()
```

## Stretch Goals

- **Title-case the famous person's name** with ``.title()`` before
  substituting it.
- **Two stories**: write a second template (maybe a sci-fi setting) and
  ask the user at the start which one to play. Print the chosen story
  at the end.
- **Save the result**: write the final story to a file called
  ``my_madlib.txt`` and print ``"Saved to my_madlib.txt"`` (file I/O
  is officially Week 6 territory, but ``open()`` and ``.write()`` are
  worth a peek now).
- **Word-count guard**: ensure the adjective contains no spaces — if
  it does, reprompt once. Builds a tiny validation muscle.

## Grading Rubric (Self-Check)

| Criterion | Points |
|-----------|-------:|
| Prompts for all seven inputs with clear messages | 2 |
| Strips whitespace from each input | 1 |
| Echoes the cleaned inputs back to the user | 1 |
| Story prints as a single multi-line f-string | 3 |
| Substitutions land in the correct slots | 2 |
| Code is tidy with a docstring and ``main()`` pattern | 1 |
| **Total** | **10** |
