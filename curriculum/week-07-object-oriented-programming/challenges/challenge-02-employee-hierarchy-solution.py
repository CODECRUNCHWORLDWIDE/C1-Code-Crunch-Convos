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
