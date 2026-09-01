"""exercise-04-scope-mystery-solution.py — five scope bugs, all five fixed.

Bug 1 (sign_up counter): UnboundLocalError. Assigning to VOLUNTEERS_SIGNED_UP
    anywhere in the body made it local for the whole function, so the read on
    the right-hand side had nothing to read. Rule: assignment decides scope,
    and it decides it for the entire function. Fixed with `global`.
Bug 2 (sign_up roster): no exception, wrong answer. `roster: list[str] = []`
    is evaluated once, at def time, so every call that omitted a roster shared
    one list. Rule: default values are bound at definition, not at call.
    Fixed with the None sentinel.
Bug 3 (module-level `sum = 0`): TypeError, 'int' object is not callable. A
    module-level name hid the built-in for the whole file. Rule: LEGB looks in
    Global before Builtins. Fixed by deleting the line.
Bug 4 (add's running total): UnboundLocalError. `running += bags` is an
    assignment, so `running` was local to `add` and the enclosing function's
    variable was invisible for writing. Rule: `nonlocal` reaches the enclosing
    function scope; `global` would reach past it to the module.
Bug 5 (crew_capacity): no exception, wrong answer. The function read module
    state instead of its own parameter. Rule: a name in the signature is a
    promise; a function that ignores it is not pure and not honest.
"""

VOLUNTEERS_SIGNED_UP = 0
BAGS_PER_VOLUNTEER = 3
METERS_PER_VOLUNTEER = 40


def sign_up(name: str, roster: list[str] | None = None) -> list[str]:
    """Add `name` to `roster` and return the roster."""
    global VOLUNTEERS_SIGNED_UP
    if roster is None:
        roster = []
    roster.append(name)
    VOLUNTEERS_SIGNED_UP = VOLUNTEERS_SIGNED_UP + 1
    return roster


def bags_for_crew(crew_size: int) -> int:
    """Return how many trash bags a crew of `crew_size` needs."""
    per_person = [BAGS_PER_VOLUNTEER] * crew_size
    return sum(per_person)


def street_totals(counts: dict[str, int]) -> dict[str, int]:
    """Return a running total of bags collected, street by street."""
    running = 0

    def add(bags: int) -> int:
        """Add `bags` to the running total and return the new total."""
        nonlocal running
        running += bags
        return running

    return {street: add(bags) for street, bags in counts.items()}


def crew_capacity(crew_size: int) -> int:
    """Return how many meters of curb a crew of `crew_size` can clear."""
    return METERS_PER_VOLUNTEER * crew_size


if __name__ == "__main__":
    first = sign_up("Rosa")
    second = sign_up("Ken")
    assert first == ["Rosa"], first
    assert second == ["Ken"], second
    assert VOLUNTEERS_SIGNED_UP == 2, VOLUNTEERS_SIGNED_UP

    assert bags_for_crew(4) == 12, bags_for_crew(4)
    assert bags_for_crew(0) == 0, bags_for_crew(0)

    totals = street_totals({"Cedar Street": 5, "Mill Road": 3, "Front Street": 2})
    assert totals == {"Cedar Street": 5, "Mill Road": 8, "Front Street": 10}, totals

    assert crew_capacity(3) == 120, crew_capacity(3)
    assert crew_capacity(0) == 0, crew_capacity(0)

    print(f"{VOLUNTEERS_SIGNED_UP} volunteers signed up.")
    print(f"Bags for a crew of 4: {bags_for_crew(4)}")
    print(f"Street totals: {totals}")
    print(f"A crew of 3 clears {crew_capacity(3)} m of curb.")
    print("All checks passed.")
