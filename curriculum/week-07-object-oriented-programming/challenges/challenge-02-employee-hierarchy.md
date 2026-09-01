# Challenge 02 — Employee Hierarchy and Payroll

> **Topic:** inheritance that is honest, `super()` used properly, and one function that pays everybody
> **Lecture:** [02 — Inheritance and Composition](../lecture-notes/02-inheritance-and-composition.md)
> **Difficulty:** Medium
> **Target time:** 90–120 minutes
> **Why this one:** the point is not the payroll arithmetic. It is choosing a family of classes where every "is-a" is really true, and using `super()` so that a rule written once stays written once. Exercise 3 showed you polymorphism with three formulas. This shows you the same idea when the subclasses also have to *extend* the parent's answer rather than replace it.

## The Brief

Model a small company.

Everybody on the payroll is an **`Employee`**: they have a name, a base
salary, and a method `monthly_salary()` that says what they get paid this
month. For a plain employee that is just the base salary.

Some people are **engineers**. An engineer *is an* employee who also has a
level from 1 to 5, and each level adds ten per cent on top of the base.

Some people are **managers**. A manager *is an* employee who also has a list
of direct reports, and gets five per cent of what their team is paid.

Then one module-level function, `total_payroll(employees)`, adds up
everybody's monthly salary. It must work without ever asking what kind of
employee it is holding — no `isinstance` anywhere. That constraint is the
whole challenge in one line.

Two ideas here are new, and both are about `super()`.

**Extending rather than replacing.** In Exercise 3 each subclass's `area()`
threw away whatever the parent would have said. Here `Engineer.monthly_salary`
wants the parent's answer and then multiplies it. So the body starts with
`base = super().monthly_salary()`. That looks like a pointless detour today —
it just returns `self.base_salary`. It stops looking pointless the day
`Employee.monthly_salary` grows a cost-of-living adjustment, because with
`super()` that lands in one file and every subclass inherits it. Written as
`self.base_salary * (1 + ...)`, the subclass has quietly forked the
definition of "base pay", and nobody finds out until a payslip is wrong.

**An honest "is-a".** Inheritance is a claim: *every* manager can be used
anywhere an employee can. The test is whether the subclass ever has to
*remove* something. Nothing here does — a manager is still paid, still
appears on the payroll, still answers `monthly_salary()`. Managing is
something extra a manager does, not something an employee stops being. The
first stretch goal introduces a `Contractor`, where that claim starts to
creak, and being able to feel the difference is the point.

There is also a business rule that has nothing to do with pay and everything
to do with **when** you check things: a manager must earn at least 1.2 times
their highest-paid direct report. It has to hold when the manager is created
*and* when a report is added later, and adding a report that would break it
must leave the manager exactly as it was.

## Starter

Create `payroll.py` and fill in the `TODO` markers.

```python
"""payroll.py — employee hierarchy and payroll.

    python payroll.py

Reflection questions
--------------------
TODO: answer the three questions from the Steps section here, in 2-3
sentences each, before you call this finished.
"""

from __future__ import annotations

from collections.abc import Iterable

MANAGER_SALARY_RATIO = 1.2   # a manager must earn >= 1.2x their top report
MANAGER_TEAM_BONUS = 0.05    # 5% of the team's monthly pay
ENGINEER_BONUS_PER_LEVEL = 0.1


class Employee:
    """Someone on the payroll. The base case: pay is just the base salary."""

    def __init__(self, name: str, base_salary: float) -> None:
        """Store a validated name and base salary."""
        # TODO: refuse an empty name and a negative base_salary,
        # then store self.name and self.base_salary as a float

    def monthly_salary(self) -> float:
        """One month's pay. The base case is the base salary."""
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        """Developer form, naming the actual subclass."""
        # TODO: use type(self).__name__ so subclasses inherit this usefully
        raise NotImplementedError


class Engineer(Employee):
    """An individual contributor. Level 1-5 adds 10% per level."""

    MIN_LEVEL = 1
    MAX_LEVEL = 5

    def __init__(self, name: str, base_salary: float, level: int) -> None:
        """Let Employee validate the shared fields, then check the level."""
        # TODO: super().__init__(...) FIRST, then check the level range

    def monthly_salary(self) -> float:
        """The base figure plus 10% per level."""
        # TODO: start from super().monthly_salary(), do not re-read base_salary
        raise NotImplementedError


class Manager(Employee):
    """An employee who also has direct reports."""

    def __init__(
        self,
        name: str,
        base_salary: float,
        reports: list[Employee] | None = None,
    ) -> None:
        """Let Employee validate the shared fields, then check the 1.2x rule."""
        # TODO: super().__init__(...), then build self.reports as a COPY
        # of the list you were handed, then check the ratio

    def _check_salary_ratio(self, reports: list[Employee]) -> None:
        """A manager must earn at least 1.2x their highest-paid direct report."""
        # TODO: no reports means nothing to check.
        # Otherwise compare self.base_salary against
        # MANAGER_SALARY_RATIO * the highest report base_salary.

    def add_report(self, employee: Employee) -> None:
        """Add a direct report, re-checking the ratio before committing."""
        # TODO: check the list you are ABOUT to have, then append

    def monthly_salary(self) -> float:
        """The base figure plus 5% of the team's monthly pay."""
        # TODO: super() for the base, then sum the team's monthly_salary()
        raise NotImplementedError


def total_payroll(employees: Iterable[Employee]) -> float:
    """Sum of everybody's monthly pay. No isinstance, no branching, on purpose."""
    # TODO: one line
    raise NotImplementedError


def main() -> None:
    """Pay a small company, then show every validation rule refusing."""
    alice = Engineer(name="Alice", base_salary=5000, level=3)
    bob = Engineer(name="Bob", base_salary=4500, level=2)
    carol = Manager(name="Carol", base_salary=7000, reports=[alice, bob])

    print(alice.monthly_salary())    # 5000 * 1.3 = 6500.0
    print(bob.monthly_salary())      # 4500 * 1.2 = 5400.0
    print(carol.monthly_salary())    # 7000 + 0.05*(6500+5400) = 7595.0
    print(total_payroll([alice, bob, carol]))

    dave = Employee(name="Dave", base_salary=3000)
    print("with a plain employee:", total_payroll([alice, bob, carol, dave]))

    erin = Manager(name="Erin", base_salary=9000, reports=[carol])
    print("erin:", round(erin.monthly_salary(), 2))
    print("mro:", [c.__name__ for c in Manager.__mro__])

    for label, thunk in [
        ("negative salary", lambda: Employee("Zed", -1)),
        ("bad level", lambda: Engineer("Zed", 5000, level=9)),
        ("underpaid manager", lambda: Manager("Zed", 5000, reports=[alice])),
    ]:
        try:
            thunk()
        except ValueError as exc:
            print(f"ValueError ({label}): {exc}")

    frank = Engineer(name="Frank", base_salary=6500, level=1)
    try:
        carol.add_report(frank)
    except ValueError as exc:
        print("ValueError (add_report):", exc)
    print("carol still has:", [r.name for r in carol.reports])


if __name__ == "__main__":
    main()
```

One thing in that starter is worth naming before you start.
**`reports: list[Employee] | None = None`** is not shyness about types. A
literal `[]` in a signature is evaluated **once**, when the function is
defined, so every manager created without a `reports` argument would share
one list — the Biscuit-and-Juniper bug from Exercise 1, in a signature. `None`
plus "build the list inside" is the standard fix.

## Requirements

### `Employee`

1. Fields `name: str` and `base_salary: float`.
2. A negative `base_salary` raises `ValueError`. So does an empty or
   whitespace-only name.
3. `monthly_salary(self) -> float` returns `self.base_salary`.
4. `__repr__` uses `type(self).__name__`, so a subclass with no extra fields
   needs no repr of its own.

### `Engineer(Employee)`

1. Adds `level: int`, valid from 1 through 5. Anything else raises
   `ValueError`.
2. `__init__` calls `super().__init__(name, base_salary)` as its first
   statement.
3. `monthly_salary` overrides the parent and returns
   `super().monthly_salary() * (1 + 0.1 * level)`.

### `Manager(Employee)`

1. Adds `reports: list[Employee]`, defaulting to empty, and stored as a
   **copy** of whatever list it was handed.
2. The manager's `base_salary` must be at least 1.2 times the highest
   `base_salary` among the direct reports. Otherwise `ValueError`, naming the
   offending report and the figure that would be needed.
3. `add_report(self, employee) -> None` re-checks that rule against the list
   it is *about to* have, and appends only if the check passes.
4. `monthly_salary` returns `super().monthly_salary() + 0.05 * <the sum of
   the reports' monthly salaries>`.

### `total_payroll(employees)`

A module-level function, not a method. It takes any iterable of `Employee`
and returns the sum of their `monthly_salary()` values, with **zero**
`isinstance` checks and no branching on type.

## Constraints

- **Single inheritance only.** One parent per class, no mixing in extra
  parents.
- **Every subclass `__init__` starts with `super().__init__(...)`.** That
  keeps the non-negative-salary check in exactly one file, so fixing or
  extending it fixes it for every role. It also means the parent's fields
  exist before the subclass's checks run.
- **Every overridden `monthly_salary` calls `super().monthly_salary()` for
  the base figure.** `return self.base_salary * (1 + 0.1 * self.level)`
  produces the right number today and passes every test. It is still wrong,
  and no error message will ever tell you: the subclass has copied the
  definition of "base pay".
- **The 1.2x rule compares `base_salary`, not `monthly_salary()`.** The
  alternative is circular — a manager's monthly salary depends on their
  reports' monthly salaries, so validating against it would make the
  constructor's answer depend on itself.
- **`add_report` checks before it appends.** Build the list you are about to
  have, validate *that*, and only then commit. The alternative — append,
  check, pop back on failure — works but leaves a window where the object is
  illegal, and it is exactly the kind of undo that gets forgotten when
  somebody adds a third caller.
- **Copy the `reports` list you are handed.** `self.reports = list(reports)`
  means the caller's list and the manager's list are different objects, so a
  later `some_list.append(...)` on the caller's side cannot silently add a
  report and skip the ratio check. This is a second, independent fix from the
  `None` default.
- **Every error is a `ValueError` with a message that names the value.**
  `ValueError("bad")` tells a reader nothing they did not already know.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-employee-hierarchy-solution.py
6500.0
5400.0
7595.0
19495.0
with a plain employee: 22495.0
erin: 9379.75
mro: ['Manager', 'Employee', 'object']
ValueError (negative salary): Zed: base_salary must be non-negative, got -1
ValueError (bad level): Zed: level must be between 1 and 5, got 9
ValueError (underpaid manager): Zed: base_salary 5000.00 is below the required 1.2x of Alice's 5000.00 (needs at least 6000.00)
ValueError (add_report): Carol: base_salary 7000.00 is below the required 1.2x of Frank's 6500.00 (needs at least 7800.00)
carol still has: ['Alice', 'Bob']
```

Check the first four by hand. Alice is `5000 * 1.3 = 6500.0`. Bob is
`4500 * 1.2 = 5400.0`. Carol is `7000 + 0.05 * (6500 + 5400) = 7595.0`. The
total is `6500 + 5400 + 7595 = 19495.0`.

`erin: 9379.75` is the interesting one, because Erin manages Carol, who
manages two engineers. Erin's team bonus is 5% of Carol's *monthly* salary —
`9000 + 0.05 * 7595 = 9379.75`. Nothing in `Manager.monthly_salary`
special-cases a report who is also a manager. The nesting falls out of
calling the same method on whatever is in the list.

The last line is the one that proves `add_report` checks before it commits.
Frank was refused, and Carol still has exactly the two reports she started
with.

## Steps

1. Write `Employee` and get `Employee("Dave", 3000).monthly_salary()`
   returning `3000.0`. Note the `.0` — `float(base_salary)` normalises at the
   boundary, so an `int` argument and a `float` argument behave the same
   everywhere downstream.
2. Write `Engineer`. Check Alice is `6500.0` before you go on.
3. Write `total_payroll` next, before `Manager`, and run it over two
   engineers and a plain employee. One line, `sum(...)`, no `if`.
4. Write `Manager.__init__` and `monthly_salary`. Check Carol is `7595.0`.
5. Write `_check_salary_ratio` and call it from `__init__`. Confirm the
   underpaid manager is refused.
6. Write `add_report` so it validates the prospective list first. Confirm
   Frank is refused **and** that `carol.reports` is unchanged afterwards.
7. Build Erin, the manager of a manager, and check `9379.75` by hand. That
   number is the recursion working.
8. Answer the three reflection questions in a comment block at the top of
   your file:
   1. Why is `Manager(Employee)` an honest "is-a" here? Could you have used
      composition instead, and what would you have lost or gained?
   2. The `reports` field is a *list of `Employee`*, but it accepts
      engineers and sub-managers too. Which property makes that work
      transparently?
   3. Where did `super()` save you from duplication? If you added
      `SeniorEngineer(Engineer)`, how would `super()` help again?
9. Grep your own file for the two structural rules: `isinstance` must not
   appear in `total_payroll`, and every subclass `__init__` and every
   overridden `monthly_salary` must contain a `super()` call.

## The Solution

```python
"""challenge-02-employee-hierarchy-solution.py — employee hierarchy and payroll.

The `-solution` in the name keeps this file from colliding with the
`payroll.py` you write yourself. Run it with::

    python challenge-02-employee-hierarchy-solution.py

Reflection questions
--------------------
1. Is `Manager(Employee)` an honest "is-a"?
   Yes. A manager is paid, appears on the payroll, and answers to the same
   `monthly_salary()` contract as anyone else; managing is something extra a
   manager does, not something an employee stops being. Nothing is removed or
   disabled in the subclass, which is the test from lecture 02. Composition
   would also work — `Employee` holding a `ManagementDuties` object — and it
   would let one person pick up and drop the manager role at runtime without
   changing their identity. What it costs is the free polymorphism: with
   composition, `total_payroll` has to ask each employee whether they have
   duties, so the bonus logic leaks out of the class and back into the caller.

2. Why does `reports: list[Employee]` accept engineers and sub-managers?
   The Liskov substitution principle, expressed in Python as subtype
   polymorphism: an `Engineer` *is* an `Employee`, so anywhere the code says
   "an Employee" an Engineer is legal. `Manager.monthly_salary` calls
   `report.monthly_salary()` and Python resolves that through each object's own
   MRO at call time, so an engineer report contributes its level bonus and a
   sub-manager report contributes its own team bonus, with no branching here.

3. Where did `super()` save duplication?
   In two places. `super().__init__(name, base_salary)` keeps the non-negative
   salary check in exactly one file, so fixing or extending it fixes it for
   every role. And `super().monthly_salary()` means each subclass writes only
   the delta it is responsible for — the level bonus, the team bonus — instead
   of restating "start from base_salary". Adding `SeniorEngineer(Engineer)`
   would be the same move one layer down: `super().__init__(...)` runs
   `Engineer`'s level validation, and `super().monthly_salary()` returns the
   already-level-adjusted figure, so the new class only writes the seniority
   premium it adds.
"""

from __future__ import annotations

from collections.abc import Iterable

MANAGER_SALARY_RATIO = 1.2   # a manager must earn >= 1.2x their top report
MANAGER_TEAM_BONUS = 0.05    # 5% of the team's monthly pay
ENGINEER_BONUS_PER_LEVEL = 0.1


class Employee:
    """Someone on the payroll. The base case: pay is just the base salary."""

    def __init__(self, name: str, base_salary: float) -> None:
        """Store a validated name and base salary."""
        if not name.strip():
            raise ValueError("an employee needs a non-empty name")
        if base_salary < 0:
            raise ValueError(
                f"{name}: base_salary must be non-negative, got {base_salary!r}"
            )
        self.name = name
        self.base_salary = float(base_salary)

    def monthly_salary(self) -> float:
        """One month's pay. The base case is the base salary."""
        return self.base_salary

    def __repr__(self) -> str:
        """Developer form, naming the actual subclass."""
        return f"{type(self).__name__}(name={self.name!r}, base_salary={self.base_salary!r})"


class Engineer(Employee):
    """An individual contributor. Level 1-5 adds 10% per level."""

    MIN_LEVEL = 1
    MAX_LEVEL = 5

    def __init__(self, name: str, base_salary: float, level: int) -> None:
        """Let Employee validate the shared fields, then check the level."""
        super().__init__(name, base_salary)          # reuse the base validation
        if not self.MIN_LEVEL <= level <= self.MAX_LEVEL:
            raise ValueError(
                f"{name}: level must be between {self.MIN_LEVEL} and "
                f"{self.MAX_LEVEL}, got {level!r}"
            )
        self.level = level

    def monthly_salary(self) -> float:
        """The base figure plus 10% per level."""
        base = super().monthly_salary()              # Employee decides the base
        return base * (1 + ENGINEER_BONUS_PER_LEVEL * self.level)

    def __repr__(self) -> str:
        """Developer form, including the level."""
        return (
            f"Engineer(name={self.name!r}, base_salary={self.base_salary!r}, "
            f"level={self.level!r})"
        )


class Manager(Employee):
    """An employee who also has direct reports."""

    def __init__(
        self,
        name: str,
        base_salary: float,
        reports: list[Employee] | None = None,
    ) -> None:
        """Let Employee validate the shared fields, then check the 1.2x rule."""
        super().__init__(name, base_salary)
        # `None` default, then build the list here: a shared `[]` default would
        # be the same class-attribute footgun from lecture 01.
        self.reports: list[Employee] = list(reports) if reports else []
        self._check_salary_ratio(self.reports)

    # --- the 1.2x rule, in one place --------------------------------------

    def _check_salary_ratio(self, reports: list[Employee]) -> None:
        """A manager must earn at least 1.2x their highest-paid direct report."""
        if not reports:
            return
        top = max(report.base_salary for report in reports)
        required = MANAGER_SALARY_RATIO * top
        if self.base_salary < required:
            offender = max(reports, key=lambda r: r.base_salary)
            raise ValueError(
                f"{self.name}: base_salary {self.base_salary:.2f} is below the "
                f"required {MANAGER_SALARY_RATIO}x of {offender.name}'s "
                f"{top:.2f} (needs at least {required:.2f})"
            )

    def add_report(self, employee: Employee) -> None:
        """Add a direct report, re-checking the ratio before committing."""
        self._check_salary_ratio([*self.reports, employee])   # may raise
        self.reports.append(employee)

    # --- pay ---------------------------------------------------------------

    def monthly_salary(self) -> float:
        """The base figure plus 5% of the team's monthly pay."""
        base = super().monthly_salary()
        team = sum(report.monthly_salary() for report in self.reports)
        return base + MANAGER_TEAM_BONUS * team

    def __repr__(self) -> str:
        """Developer form, naming the reports rather than repring them."""
        return (
            f"Manager(name={self.name!r}, base_salary={self.base_salary!r}, "
            f"reports={[r.name for r in self.reports]!r})"
        )


def total_payroll(employees: Iterable[Employee]) -> float:
    """Sum of everybody's monthly pay. No isinstance, no branching, on purpose."""
    return sum(employee.monthly_salary() for employee in employees)


def main() -> None:
    """Pay a small company, then show every validation rule refusing."""
    alice = Engineer(name="Alice", base_salary=5000, level=3)
    bob = Engineer(name="Bob", base_salary=4500, level=2)
    carol = Manager(name="Carol", base_salary=7000, reports=[alice, bob])

    print(alice.monthly_salary())    # 5000 * 1.3 = 6500.0
    print(bob.monthly_salary())      # 4500 * 1.2 = 5400.0
    print(carol.monthly_salary())    # 7000 + 0.05*(6500+5400) = 7595.0
    print(total_payroll([alice, bob, carol]))

    # A plain Employee still works through the same call.
    dave = Employee(name="Dave", base_salary=3000)
    print("with a plain employee:", total_payroll([alice, bob, carol, dave]))

    # Nesting: a manager of managers is just another report.
    erin = Manager(name="Erin", base_salary=9000, reports=[carol])
    print("erin:", round(erin.monthly_salary(), 2))
    print("mro:", [c.__name__ for c in Manager.__mro__])

    # --- validation ----------------------------------------------------
    for label, thunk in [
        ("negative salary", lambda: Employee("Zed", -1)),
        ("bad level", lambda: Engineer("Zed", 5000, level=9)),
        ("underpaid manager", lambda: Manager("Zed", 5000, reports=[alice])),
    ]:
        try:
            thunk()
        except ValueError as exc:
            print(f"ValueError ({label}): {exc}")

    frank = Engineer(name="Frank", base_salary=6500, level=1)
    try:
        carol.add_report(frank)
    except ValueError as exc:
        print("ValueError (add_report):", exc)
    print("carol still has:", [r.name for r in carol.reports])


if __name__ == "__main__":
    main()
```

**`total_payroll` is the whole point, and it is one line.**
`sum(employee.monthly_salary() for employee in employees)` never asks what
kind of employee it has. Python resolves `.monthly_salary` at call time by
walking that specific object's MRO, so an `Engineer` runs
`Engineer.monthly_salary`, a `Manager` runs `Manager.monthly_salary`, and a
plain `Employee` runs the base version — from the same expression. Adding a
`Contractor` next week requires zero edits here. That is why the requirements
forbid `isinstance`: an `isinstance` chain re-centralises knowledge of every
subclass in the one function that was supposed to not need it, and it grows a
branch every time somebody adds a role.

**Each `monthly_salary` override writes only its delta.** `Engineer` computes
`super().monthly_salary() * (1 + 0.1 * level)`. Mechanically, `super()`
returns a proxy that starts the attribute lookup at the *next* class in
`type(self).__mro__` after the current one. It is not "my parent class" in
general — it is "the next link in this instance's chain", which is why it
composes correctly through several levels of subclass.

**The 1.2x rule lives in one private method, called from two places.**
`__init__` checks the list it was handed; `add_report` checks the list it is
*about to* have. Building `[*self.reports, employee]` and validating that
before changing anything is what makes the failure clean: if the check
raises, `self.reports` is untouched, and the demo's last line proves it.

**`reports: list[Employee] | None = None` and then `list(reports)` are two
separate fixes.** The `None` default avoids the shared-mutable-default trap.
The `list(reports)` copy is independent of it: it means the caller's list and
the manager's list are different objects.

**`float(base_salary)` normalises at the boundary.** `Employee("X", 5000)`
stores `5000.0`, so repr and arithmetic behave the same whether the caller
passed an `int` or a `float`.

**The example numbers land exactly, and that is partly luck.**
`5000 * (1 + 0.1 * 3)` is `6500.0`, not `6500.000000000001`, because
`0.1 * 3` gives `0.30000000000000004` and adding `1` rounds that back to
exactly `1.3` at the machine's precision. Do not build a habit on it. Real
payroll uses `decimal.Decimal` or whole cents, for the reasons Exercise 5
spends a page on.

## Download and run

Download
[challenge-02-employee-hierarchy-solution.py](./challenge-02-employee-hierarchy-solution.py)
and run it:

```bash
python challenge-02-employee-hierarchy-solution.py
```

It imports only `collections.abc` and needs no setup. The reflection answers
are the module docstring at the top, which is where the brief asks for them.
Save your own version as `payroll.py`.

## Common bugs to catch

- **`AttributeError: 'Engineer' object has no attribute 'base_salary'`.** The
  subclass `__init__` never called `super().__init__(...)`:

  ```python
  class Engineer(Employee):
      def __init__(self, name, base_salary, level):
          self.level = level          # and nothing else
  ```

  The traceback points at `monthly_salary`, not at `__init__`, because that
  is where the missing attribute is first read — so the error surfaces a long
  way from its cause. Every rule about `super().__init__` exists to prevent
  this.

- **Re-implementing the base calculation instead of calling `super()`.**
  `return self.base_salary * (1 + 0.1 * self.level)` produces the right
  number today and passes every test. There is no error message for this one
  — it is caught only in review, or by a wrong payslip six months later.

- **Reaching for `isinstance` in `total_payroll`.**

  ```python
  def total_payroll(employees):
      total = 0.0
      for e in employees:
          if isinstance(e, Manager):
              total += e.base_salary + 0.05 * sum(r.monthly_salary() for r in e.reports)
          elif isinstance(e, Engineer):
              total += e.base_salary * (1 + 0.1 * e.level)
          else:
              total += e.base_salary
      return total
  ```

  This runs and gives the right answer. It is the design the challenge is
  teaching you to avoid: the pay rules now live in two places, an ordering
  bug is waiting (put a subclass check *after* its parent's and the parent
  branch swallows it), and every new role means editing a function that has
  nothing to do with roles.

- **Mutating first and validating second in `add_report`.**

  ```python
  def add_report(self, employee):
      self.reports.append(employee)
      self._check_salary_ratio(self.reports)   # too late
  ```

  The `ValueError` is raised, the caller catches it and carries on — and the
  manager is now holding an illegal report. The demo's last line is the test
  for this: `carol still has: ['Alice', 'Bob']`, not three names.

- **A mutable default in the signature.**
  `def __init__(self, name, base_salary, reports=[])` gives every
  default-constructed manager the *same* list object. Two managers, one call
  to `add_report`, both teams grow. This is Exercise 1's `tricks = []` in a
  different costume.

- **`erin` comes out as `9350.0` instead of `9379.75`.** You summed the
  reports' `base_salary` instead of their `monthly_salary()`. The recursion
  is the point: `9000 + 0.05 * 7595` is `9379.75`; `9000 + 0.05 * 7000` is
  `9350.0`.

- **`AttributeError: 'str' object has no attribute 'strip'` from
  `Employee.__init__`.** You called it positionally with the arguments in the
  wrong order, or passed a number where the name goes. Read the traceback's
  bottom frame: it is telling you which value arrived where.

## Under the hood

<details>
<summary>Under the hood — what super() is really doing, and how to tell when an "is-a" has gone bad</summary>

`super()` with no arguments looks like a keyword. It is a class, and it is
doing two things you can see.

First, it needs to know *which class the current method was written in*. Not
the object's class — the class whose body the code physically sits in. Python
supplies that through a hidden `__class__` cell that the compiler adds to any
method body that mentions `super`. That is why the no-argument form only
works inside a class body, and why the explicit form exists:

```python
super().monthly_salary()            # inside Engineer
super(Engineer, self).monthly_salary()   # exactly the same thing
```

Second, it starts the attribute search at the class **after** that one in
`type(self).__mro__`. Watch it with three levels:

```text
>>> class SeniorEngineer(Engineer):
...     def monthly_salary(self):
...         return super().monthly_salary() * 1.15
...
>>> [c.__name__ for c in SeniorEngineer.__mro__]
['SeniorEngineer', 'Engineer', 'Employee', 'object']
>>> s = SeniorEngineer("Sam", 5000, level=3)
>>> s.monthly_salary()
7474.999999999999
```

Three classes contributed and none of them knew how deep the chain went.
`SeniorEngineer` asked for the next link and got `Engineer`'s
level-adjusted `6500.0`; `Engineer` asked for the next link and got
`Employee`'s `5000.0`. Each class wrote only its own delta:
`5000 × 1.3 × 1.15`.

And look at the answer. `7474.999999999999`, not `7475.0` — one more
multiplication was enough to expose what Alice's `6500.0` was hiding. The
`.0` in the demo's output was luck, not a rule, which is exactly why the
solution says not to build a habit on it.

Because the search is over `type(self).__mro__`, and `self` is the *actual*
object, `super()` inside `Engineer` does not always mean `Employee`. In a
class with two parents it can land somewhere that `Engineer` has never heard
of. That is a feature — it is what gives every class in a diamond exactly one
turn — and it is why the rule is "next in the MRO", not "my parent".

Now the harder question the challenge is really about: **how do you know an
"is-a" is honest?**

The test has a name — the **Liskov substitution principle** — and it says:
anywhere the code expects an `Employee`, handing it a subclass must not
change whether the code is correct. `total_payroll` is a live demonstration.
It was written against `Employee` and it works, unchanged, on engineers and
managers. Nothing was substituted badly.

The warning signs that a subclass is *not* substitutable:

1. **It has to disable something.** A subclass whose override raises
   `NotImplementedError`, or returns `None` where the parent promised a
   number, has taken a capability away. Callers holding the parent type are
   now wrong through no fault of their own.
2. **It has to neutralise a parent field.** The first stretch goal is
   exactly this. `Contractor` is paid `hourly_rate * hours_per_month`, and
   `base_salary` means nothing to it — so it passes `0.0` up to satisfy a
   check that has stopped meaning anything. Nothing breaks, and that is the
   problem: the field is structurally present and semantically dead, and
   every future reader has to learn the exception.
3. **Its override stops calling `super()`.** This is the mechanical tell for
   sign 2. `Contractor.monthly_salary` cannot call `super()`, because the
   parent's answer is not part of its calculation at all. When an override
   stops needing its parent, it has stopped *extending* it, and the "is-a" is
   on borrowed time.

Two clean ways out when you spot it:

- **Push the field down.** Leave `Employee` with `name` and the
  `monthly_salary()` promise; move `base_salary` into a
  `SalariedEmployee(Employee)` that `Engineer` and `Manager` extend.
  `Contractor` then inherits nothing it does not use. This is the "smallest
  honest base class" move, and it is a strictly better hierarchy.
- **Stop inheriting.** If roles keep sprouting fields the base does not want,
  the base class was a bad abstraction. Give `Employee` a `pay` object — a
  `FlatSalary`, a `LevelledSalary`, an `HourlySalary` — and let the role be a
  field rather than a type. That is the third stretch goal.

Which is better *here*? The hierarchy, and it is worth saying why plainly:
the "is-a" is real, nothing is disabled, and there are three roles rather
than thirty. Composition starts winning at the point where roles multiply,
combine, or change during one person's life — promoting Bob becomes
`bob.pay = TeamBonus(...)`, one assignment on the same object, instead of
constructing a new `Manager` and hunting down every list that held the old
`Engineer`.

That is the actual content of "prefer composition over inheritance". Not
"inheritance is bad", but "inheritance is a commitment made at construction
time, so make it only where the relationship really is permanent."

One thing composition costs you, though, and it is the sharpest difference:
**where the invariant lives**. The 1.2x rule is a fact about a manager and
their reports. In the hierarchy it lives in `Manager.__init__` and
`add_report`, enforced at the boundary, and a `Manager` cannot exist in an
illegal state. With strategies there is no `Manager` to enforce it — a pay
rule is not an org-chart rule — so you would need a separate `OrgChart`
object owning that invariant. A fifth class the hierarchy did not need.

</details>

## Acceptance checklist

- [ ] `python payroll.py` runs a demo with no traceback.
- [ ] Single inheritance only; no multiple inheritance, no mixins.
- [ ] Every subclass `__init__` calls `super().__init__(...)` first.
- [ ] Every overridden `monthly_salary` calls `super().monthly_salary()`.
- [ ] `total_payroll` contains zero `isinstance` checks and no `if`.
- [ ] Alice is `6500.0`, Bob is `5400.0`, Carol is `7595.0`, and the total is
      `19495.0`.
- [ ] A manager of a manager gives `9379.75`, not `9350.0`.
- [ ] Every validation error is a `ValueError` whose message names the value.
- [ ] A refused `add_report` leaves `reports` unchanged.
- [ ] Every signature is type-hinted.
- [ ] The three reflection answers are a comment block at the top of your
      file.
- [ ] Committed to Git with a message like
      `Add Week 7 challenge 2: employee hierarchy`.

## Stretch

- Add a `Contractor(Employee)` whose `monthly_salary` is
  `hourly_rate * hours_per_month`, with no relationship to `base_salary` at
  all. Then answer, in a comment: what happened to the parent's validation
  rule? (Nothing breaks, and that is the problem — read the Under the hood
  block.) Pick one of the two clean handlings and say why.
- Refactor the hierarchy to use `@dataclass`. You will need
  `kw_only=True`, and when you find out why, write it down. Note two more
  things: a subclass overriding `__post_init__` must call
  `super().__post_init__()` itself or the parent's validation silently never
  runs, and the generated `__repr__` for a manager reprs every report in
  full, which turns one `print` into a wall of text.
- Replace the hierarchy with **composition**: each employee has a
  `SalaryStrategy`. Get the same total out of both designs, then compare them
  in a paragraph — including where the 1.2x rule ends up living, which is the
  question the Under the hood block leaves you with.

That is Week 7's challenges. Next is the
[homework](../homework/README.md), six problems that each take one idea from
this week and push on it.
