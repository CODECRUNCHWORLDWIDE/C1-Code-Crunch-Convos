# Challenge 02 — Employee Hierarchy and Payroll

> **Estimated time:** 90–120 minutes. **Difficulty:** medium.

Model a small company. The point is not the payroll math — it is choosing a
hierarchy that is **honest** (every "is-a" is real) and using `super()`
correctly.

---

## Background

A company has employees. Some are individual contributors (engineers); some
are managers (who also happen to have a small list of direct reports). Total
payroll is the sum of everyone's monthly salary.

---

## Requirements

Build a single file `payroll.py` with three classes and a function.

### `Employee` (base class)

- Fields: `name: str`, `base_salary: float`.
- Validation: `base_salary` must be non-negative; raise `ValueError`
  otherwise.
- Method `monthly_salary(self) -> float`. For a plain `Employee` this is
  simply `self.base_salary`.
- A useful `__repr__`.

### `Engineer(Employee)`

- Adds a `level: int` field (1 through 5).
- Validation: `level` must be in the range `1..5`.
- Override `monthly_salary` to add a level-based bonus, e.g.
  `base_salary * (1 + 0.1 * level)` (10% per level). Use `super()` so the
  base salary is still computed by `Employee`.
- Use `super().__init__(...)` in `__init__`.

### `Manager(Employee)`

- Adds a field `reports: list[Employee]` (default empty).
- Validation: a manager's salary must be at least 1.2x the maximum salary of
  any direct report — raise `ValueError` in `__init__` if not. (Compare
  against `base_salary`, not `monthly_salary`, to keep the rule simple.)
- A method `add_report(self, employee: Employee) -> None` that appends to
  the list. It should re-check the 1.2x rule and raise `ValueError` if
  adding this report would violate it.
- Override `monthly_salary` to return `base_salary + 0.05 * <sum of direct
  reports' monthly salaries>` (a small management bonus that grows with team
  size). Again, call `super()` for the base figure.

### `total_payroll(employees)`

A **module-level function** (not a method) that takes any iterable of
`Employee` and returns the sum of their `monthly_salary()` values. It must
work polymorphically — you should not need `isinstance` checks inside it.

> The point of `total_payroll` is **polymorphism**. The same line of code
> handles `Employee`, `Engineer`, and `Manager` because they all expose
> `monthly_salary()`.

---

## Example session

```python
from payroll import Employee, Engineer, Manager, total_payroll

alice = Engineer(name="Alice", base_salary=5000, level=3)
bob   = Engineer(name="Bob",   base_salary=4500, level=2)
carol = Manager (name="Carol", base_salary=7000, reports=[alice, bob])

print(alice.monthly_salary())   # 5000 * 1.3 = 6500.0
print(bob.monthly_salary())     # 4500 * 1.2 = 5400.0
print(carol.monthly_salary())   # 7000 + 0.05*(6500+5400) = 7595.0

print(total_payroll([alice, bob, carol]))   # 19495.0
```

---

## Acceptance criteria

- [ ] Single inheritance only; no multiple inheritance, no `mixin`.
- [ ] Every subclass `__init__` calls `super().__init__(...)`.
- [ ] Every overridden `monthly_salary` calls `super().monthly_salary()` to
      get the base figure.
- [ ] All validation errors raise `ValueError` with a clear message.
- [ ] `total_payroll` contains **zero** `isinstance` checks.
- [ ] All code is type-hinted.
- [ ] `python payroll.py` runs a demo at the bottom and prints the example
      numbers (or your own equivalent).

---

## Reflection questions

After your code works, write **2–3 sentences** answering each:

1. Why is `Manager(Employee)` an honest "is-a" relationship here? Could you
   have used composition instead — and what would you have lost or gained?
2. The `reports` field is a *list of `Employee`* — but it actually accepts
   any subclass too (engineers, sub-managers). Which OOP property makes
   that work transparently?
3. Where did `super()` save you from duplication? Imagine adding a new
   subclass `SeniorEngineer(Engineer)` — how would `super()` help again?

Add your answers as a short comment block at the top of `payroll.py`.

---

## Stretch goals

- Add a `Contractor(Employee)` whose `monthly_salary` is `hourly_rate *
  hours_per_month` (no relationship to `base_salary` at all). What happens
  to the parent's validation rule? How do you handle it cleanly?
- Refactor the hierarchy to use `@dataclass`. Where does it help, where
  does it get awkward?
- Replace the inheritance hierarchy with **composition** (each `Employee`
  has a `SalaryStrategy`). Compare the two designs in a paragraph at the
  bottom of the file.
