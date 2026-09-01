# Lecture Note 3 — Recursion

> Estimated reading time: 35 minutes. Have a Python REPL open while you read.

You already know that a function can call another function — Lecture Note 1 built `hypotenuse` out of `square`. Nothing in the language says the function being called has to be a *different* function. A function is allowed to call itself, and when it does, we call that **recursion**.

That one sentence is the whole mechanism. Recursion feels hard not because the mechanism is complicated but because you have to trust a function that has not finished yet. This note is about building that trust, and about the call stack underneath that makes the trust safe.

---

## 1. What recursion actually is

A recursive function solves a problem by solving a **smaller version of the same problem**, then doing one small piece of work with that answer.

Take factorial. `5!` means `5 * 4 * 3 * 2 * 1`. Look at it sideways and a smaller factorial is hiding inside: `5! = 5 * (4 * 3 * 2 * 1) = 5 * 4!`. In general, `n!` is `n` times `(n - 1)!`. Written in Python:

```python
def factorial(n: int) -> int:
    """Return n factorial for a non-negative integer n."""
    if n == 0:
        return 1
    return n * factorial(n - 1)


print(factorial(5))   # 120
```

Read the last line out loud: "n factorial is n times n-minus-one factorial." The code says exactly what the mathematics says. That is the payoff — when a problem is *defined* recursively, the recursive code is a direct translation with nothing invented in between.

Two questions come up immediately, and they are the right questions. How does it ever stop? And how can `factorial` call `factorial` when `factorial` has not finished computing yet? Section 2 answers the first, section 4 the second.

---

## 2. The two required parts

Every correct recursive function has exactly two kinds of branch.

**The base case.** An input small enough to answer outright, with no further calls. Here it is `n == 0`, returning `1`.

**The recursive case.** Everything else: shrink the problem, call yourself, combine.

```python
def factorial(n: int) -> int:
    """Return n factorial for a non-negative integer n."""
    if n == 0:          # base case: answer directly
        return 1
    return n * factorial(n - 1)   # recursive case: shrink, call, combine
```

Three properties must hold together. If any one fails, the function is broken.

1. There is at least one base case.
2. Every recursive call moves the argument **towards** a base case.
3. The base case is actually reachable from every legal input.

Point 3 is the subtle one:

```python
def factorial(n: int) -> int:
    """Return n factorial. BROKEN for n = 0."""
    if n == 1:
        return 1
    return n * factorial(n - 1)
```

For `factorial(5)` this is fine. For `factorial(0)` it is a disaster: `0` is not `1`, so it calls `factorial(-1)`, then `factorial(-2)`, marching away from the base case forever. A base case exists and the argument does shrink — but the base case is unreachable from `0`. All three properties matter.

Form this habit now: **write the base case line before you write the recursive line, every single time.** Not because you cannot reorder them later, but because writing the recursive call first is how people forget the base case entirely.

---

## 3. What a missing base case looks like

Python does not hang forever when recursion runs away. It gives up and raises.

```python
def countdown(n: int) -> None:
    """Print n down to 1. BROKEN: no base case."""
    print(n)
    countdown(n - 1)


countdown(3)
```

Output, abbreviated:

```text
3
2
1
0
-1
-2
...
-994
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

Notice it printed straight past zero. Nothing in the code said "stop at 1" — that was only in your head and in the docstring. The fix is a base case:

```python
def countdown(n: int) -> None:
    """Print n down to 1, then stop."""
    if n < 1:
        return
    print(n)
    countdown(n - 1)
```

`RecursionError` is your friend: it is Python telling you, quickly and loudly, that a recursive function is not converging. An infinite `while` loop tells you nothing — it just sits there. Recursion at least fails fast.

---

## 4. The call stack, drawn out

This is the section that makes recursion click. Read it slowly.

Every time any Python function is called, the interpreter creates a **stack frame**: a small block of memory holding that call's parameters, its local variables, and where to return when it finishes. Frames live in a stack — last in, first out. The frame for the call you are inside sits on top; the frame for whoever called you sits beneath it.

Recursion is not special here. `factorial(4)` calling `factorial(3)` gets a new frame for the same reason `main` calling `print` does. The only difference is that the frames happen to belong to the same function, each with its own private `n`.

That is the answer to "how can a function call itself before it has finished?" It cannot, and it does not. `factorial(4)` **pauses** halfway through the expression `4 * factorial(3)` and waits. Its frame stays on the stack holding `n = 4` until the answer it is waiting for arrives.

Here is `factorial(4)` in full.

```text
Calls going in -- each one pauses and pushes a new frame:

  push  factorial(4)   n=4   needs 4 * factorial(3), pauses
  push  factorial(3)   n=3   needs 3 * factorial(2), pauses
  push  factorial(2)   n=2   needs 2 * factorial(1), pauses
  push  factorial(1)   n=1   needs 1 * factorial(0), pauses
  push  factorial(0)   n=0   base case, no further call

The stack at its deepest, newest frame on top:

  +--------------------------------------+
  | factorial(0)   n=0   about to return |  <- top
  +--------------------------------------+
  | factorial(1)   n=1   paused          |
  +--------------------------------------+
  | factorial(2)   n=2   paused          |
  +--------------------------------------+
  | factorial(3)   n=3   paused          |
  +--------------------------------------+
  | factorial(4)   n=4   paused          |  <- bottom, your original call
  +--------------------------------------+

Answers coming back out -- each frame finishes its pending multiply, then pops:

  pop   factorial(0)  ->  1
  pop   factorial(1)  ->  1 * 1  =  1
  pop   factorial(2)  ->  2 * 1  =  2
  pop   factorial(3)  ->  3 * 2  =  6
  pop   factorial(4)  ->  4 * 6  = 24

Result: 24
```

Five things worth pulling out of that drawing:

1. **Nothing is computed on the way down.** The whole descent is bookkeeping: pause, push, pause, push. The first real arithmetic happens on the way back up.
2. **Each frame has its own `n`.** Five different `n` values are alive at once and none interfere. That is the LEGB local scope from Lecture Note 2 — one fresh local namespace per call.
3. **The base case turns the descent around.** It is the only frame that returns without waiting for anybody.
4. **Returns come back in the exact reverse of the call order.** Last in, first out.
5. **Depth costs memory.** Five frames is nothing. Five hundred thousand frames is not nothing, which is section 5.

If you would rather watch this than read it, paste `factorial` into [Python Tutor](https://pythontutor.com/) and step through it.

---

## 5. The recursion limit is real, not theoretical

Python caps how deep the stack can get. You can ask:

```python
import sys

print(sys.getrecursionlimit())   # 1000 on a default CPython install
```

Roughly a thousand frames, and some are already spent by whatever called your code, so the depth actually available to you is a little less. Cross the line and you get the error from section 3: `RecursionError: maximum recursion depth exceeded`.

You can raise the ceiling with `sys.setrecursionlimit(3000)`. Do it reluctantly, and understand the trade. That limit is a guard rail, not an annoyance: each Python frame also consumes space on the operating system's real C stack, which has a fixed size Python does not control. Set the limit high enough and a runaway recursion stops raising a catchable `RecursionError` and instead crashes the whole interpreter with a segmentation fault, taking your unsaved work with it. A clean exception is a much better failure than a hard crash.

### Why Python cannot just optimise this away

You may hear that "tail recursion is free". In some languages it is. A **tail call** is a recursive call whose result is returned directly, with no pending work left in the caller:

```python
def factorial_tail(n: int, accumulator: int = 1) -> int:
    """Return n factorial, carrying the running product in `accumulator`."""
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)   # nothing left to do after this
```

There is genuinely nothing for the calling frame to do once that call returns, so a compiler could reuse the frame instead of pushing a new one, turning the recursion into a loop. Scheme guarantees this. Scala does it for self-calls. **CPython does not do it at all**, and that is deliberate rather than an oversight — discarding frames would destroy the stack traces that make Python debuggable. So `factorial_tail(2000)` raises `RecursionError` exactly like the ordinary version. Rewriting into tail form buys you nothing in Python; do not spend an afternoon on it.

The practical consequence: **recursion depth in Python is a budget of about a thousand.** Recursing over a balanced tree of a million nodes is fine, because such a tree is only about twenty levels deep. Recursing over a list of a million items, one item per call, is not. Depth is what costs you, not total work.

---

## 6. Iterative versus recursive: be honest about it

The two factorials side by side.

```python
def factorial_iterative(n: int) -> int:
    """Return n factorial for non-negative n, computed with a loop."""
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total


def factorial_recursive(n: int) -> int:
    """Return n factorial for non-negative n, by calling itself."""
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)
```

They agree on every non-negative input. They are not equally good.

| | Iterative | Recursive |
|---|---|---|
| Extra memory | One `int` | One stack frame per call |
| Largest usable `n` | Whatever fits in RAM | Under 1000 |
| Speed at `n = 20` | Baseline | Roughly twice as slow |
| Reads like the definition | No | Yes |

Timed with `timeit` at `n = 20`, twenty thousand repetitions each, the recursive version took about 2.3 times as long on the machine these notes were written on. Your number will differ; the direction will not. Function calls in Python are not free, and the recursive version builds and tears down a frame `n` times where the loop does it once.

So for factorial, **the loop wins**. It is faster, it has no depth limit, and it is not harder to read. That is not an argument against recursion, though — it is an argument against recursion *on flat, counting problems*. Anything shaped like "do this `n` times" is a loop wearing a costume. Recursion earns its keep when the **data itself** is nested or branching, which is section 7.

---

## 7. Where recursion genuinely reads better

Suppose the org keeps its project files in nested folders and you want the total size. Model it as a dict whose values are either a file size in KB or another folder:

```python
type Folder = dict[str, int | Folder]

PROJECT: Folder = {
    "README.md": 2,
    "src": {
        "main.py": 6,
        "helpers": {"strings.py": 3, "dates.py": 4},
    },
    "tests": {"test_main.py": 5},
}
```

(`type Folder = ...` is the type-alias statement added in Python 3.12. It is allowed to refer to itself, which is exactly what a recursive data structure needs. See [PEP 695](https://peps.python.org/pep-0695/).)

Now the total:

```python
def total_kb(folder: Folder) -> int:
    """Return the combined size in KB of every file at any depth under `folder`.

    Args:
        folder: A mapping of name to either a file size or a nested folder.
    """
    total = 0
    for entry in folder.values():
        if isinstance(entry, dict):
            total += total_kb(entry)   # a folder: same problem, smaller input
        else:
            total += entry             # a file: base case
    return total


print(total_kb(PROJECT))   # 20
```

Six lines of body, handling nesting of any depth. The base case here is not a numeric condition but a **shape** condition: "this entry is not a folder" is what makes a branch stop. The recursion terminates because every call descends one level and the structure is finite. Now the loop — without recursion you must keep the pending folders somewhere yourself:

```python
def total_kb_iterative(folder: Folder) -> int:
    """Return the combined size in KB under `folder`, using an explicit stack."""
    total = 0
    stack: list[Folder] = [folder]
    while stack:
        current = stack.pop()
        for entry in current.values():
            if isinstance(entry, dict):
                stack.append(entry)
            else:
                total += entry
    return total
```

This works and returns the same `20`. But look at what you had to invent: `stack`, the decision that it is a list, the decision to `pop` from the end, and its whole lifetime. You rebuilt by hand the thing Python was already doing for you in section 4.

**That is the trade in one sentence.** Recursion borrows the interpreter's call stack to remember where you were. When the data is tree-shaped, that is a real simplification. When the data is a straight line, you are paying for a stack you did not need.

---

## 8. A warning about naive Fibonacci

Every recursion tutorial reaches for Fibonacci. Most do not tell you it is a bad example, so here is the honest version.

```python
def fib(n: int) -> int:
    """Return the nth Fibonacci number, counting from fib(0) = 0."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Correct, and quietly catastrophic, because the recursive case makes **two** calls instead of one. The full call tree for `fib(5)`:

```text
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   │   ├── fib(1)
│   │   │   └── fib(0)
│   │   └── fib(1)
│   └── fib(2)
│       ├── fib(1)
│       └── fib(0)
└── fib(3)
    ├── fib(2)
    │   ├── fib(1)
    │   └── fib(0)
    └── fib(1)
```

Count the nodes: **15 calls** to compute the fifth Fibonacci number. Notice how much of the tree is duplicated work — `fib(3)` is computed twice, `fib(2)` three times, `fib(1)` five times. Nothing is remembered between branches, and it gets worse fast:

| `n` | Calls to `fib` |
|---|---|
| 5 | 15 |
| 10 | 177 |
| 20 | 21,891 |
| 30 | 2,692,537 |
| 35 | 29,860,703 |

That is roughly a 1.6x increase in work for every increase of 1 in `n`, which is exponential growth. `fib(30)` took about a fifth of a second in a quick timing run. `fib(50)` would take days.

The fix is to remember answers you already computed, and Python ships a decorator for exactly that:

```python
from functools import cache


@cache
def fib(n: int) -> int:
    """Return the nth Fibonacci number, counting from fib(0) = 0."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(35))   # 9227465
```

With `@cache`, `fib(35)` runs 36 distinct calls instead of 29,860,703, and 33 repeat lookups come straight from the cache. Exponential collapses to linear on one import and one decorator line. That is as far as we go here — caching and dynamic programming get their own treatment later in the bootcamp. Carry out something narrower instead: **when a recursive function calls itself more than once per invocation, stop and count the work before you trust it.** One call per invocation is linear. Two is exponential unless you do something about it.

---

## 9. How to debug a recursive function

A plain `print(n)` in a recursive body gives you a flat wall of numbers with no indication of which call produced which line. Two techniques fix that.

### Carry the depth as a parameter

Add a `depth` parameter defaulting to `0`, increment it on each recursive call, and use it to indent:

```python
def factorial(n: int, depth: int = 0) -> int:
    """Return n factorial, printing an indented trace of each call.

    Args:
        n: A non-negative integer.
        depth: How many frames deep this call is. Callers leave it at 0.
    """
    pad = "  " * depth
    print(f"{pad}-> factorial({n})")
    result = 1 if n == 0 else n * factorial(n - 1, depth + 1)
    print(f"{pad}<- factorial({n}) = {result}")
    return result


factorial(4)
```

Output:

```text
-> factorial(4)
  -> factorial(3)
    -> factorial(2)
      -> factorial(1)
        -> factorial(0)
        <- factorial(0) = 1
      <- factorial(1) = 1
    <- factorial(2) = 2
  <- factorial(3) = 6
<- factorial(4) = 24
```

That is section 4's diagram, printed by the program itself. Indentation is stack depth, right-pointing arrows are frames being pushed, left-pointing arrows are frames popping with their answers. This one trick solves most recursion bugs on sight:

- Lines march right forever and never come back: the argument is not shrinking, or the base case is unreachable.
- The rightmost line is not the case you expected: your base case condition is wrong.
- The descent looks right but the values coming out are wrong: the bug is in how you combine the sub-answer, not in the recursion.

Note the default `depth: int = 0`. Callers never pass it, so the debugging parameter costs them nothing. Delete both prints and the parameter when you are done.

### Print on the way in *and* on the way out

Even without indentation, printing at entry and at exit beats printing once. Half of all recursion bugs live in the unwinding, and a single print in the middle of the body never shows you the unwinding at all. If you still cannot see it, do not try to hold five frames in your head: test the base case in isolation, then the smallest input that needs exactly one recursive call. If both are right and the general case is wrong, the combine step is your suspect.

---

## 10. Quick drills

Predict the output before you run each snippet.

**Drill A**

```python
def h(n: int) -> int:
    """Return n factorial. Something here is wrong."""
    if n == 0:
        return 1
    return n * h(n)


print(h(3))
```

**Drill B**

```python
def count_leaves(items: list) -> int:
    """Count the non-list items at any depth inside `items`."""
    total = 0
    for item in items:
        total += count_leaves(item) if isinstance(item, list) else 1
    return total


print(count_leaves([1, [2, 3], [[4], 5]]))
```

Answers:

- **A:** `RecursionError: maximum recursion depth exceeded`. A base case exists, but `h(n)` passes `n` unchanged, so the problem never gets smaller. Property 2 from section 2 is violated.
- **B:** `5`. The leaves are `1`, `2`, `3`, `4`, `5`. Lists recurse, non-lists count as one. Same shape as `total_kb`.

If A surprised you, reread section 2. If B surprised you, reread section 7.

---

## 11. Checklist before you move on

- [ ] You can state the two required parts of a recursive function without looking.
- [ ] You can explain the difference between a missing base case and an unreachable one.
- [ ] You can draw the stack for `factorial(4)` on paper, pushes and pops, and land on 24.
- [ ] You can say roughly what Python's default recursion limit is, why raising it is risky, and why no tail-call optimisation makes depth a hard constraint.
- [ ] You can argue for the iterative factorial over the recursive one, on the merits.
- [ ] You can name a shape of data where recursion is clearly the better choice, and say why.
- [ ] You can explain why naive `fib` is exponential when `factorial` is linear.
- [ ] You can add a `depth` parameter to a recursive function and read the indented trace.

Exercise 3 is the practice for this note. You will write both factorials, prove they agree for every `n` from 0 to 15, and use them to count seating arrangements for a community cleanup day. Keep this note open beside it, especially section 2 and the trace in section 4.

Next up: [Lecture Note 4 — Modules and imports](./04-modules-and-imports.md).
