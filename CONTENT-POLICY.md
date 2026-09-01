# C1 Content Policy — Original Problems, Honest Sources

This course is published under **GPL-3.0**. Anyone may fork it, teach from it,
print it, translate it, and sell a bootcamp built on it. That promise only holds
if every problem in it is ours and every dataset in it is cleared. This document
is the rule that keeps it true.

It is binding on every contributor and every future edit. It is the curriculum
sibling of the contribution rule in [CONTRIBUTING.md](CONTRIBUTING.md), stated in
full.

---

## The rule

**Every problem posed in this course is written for this course.**

Not restated from somewhere else. Not reskinned from somewhere else. Written.

That covers the problem statement, the constraints, the examples, the expected
output, the starter code, the test data, and the explanatory prose around them.

---

## Why the stricter rule

A weaker rule — "put other people's exercises in your own words" — is legally
defensible. [17 U.S.C. § 102(b)](https://www.law.cornell.edu/uscode/text/17/102)
does not protect "any idea, procedure, process, system, method of operation," so
the *task* of writing a temperature converter is free for anyone to teach. We
could have gone that way. We did not, for three reasons.

1. **Restating invites paste-then-paraphrase.** In practice the author opens the
   other page, then edits. That produces a derivative work, and it is
   detectable. The only reliable defense is to never open the page.
2. **Examples and test data have no idea/expression defense.** A curated set of
   cases can be protectable as a compilation, and that is where the industry's
   actual enforcement has been aimed. A clean restatement paired with someone
   else's examples is still exposed.
3. **Downstream freedom is the point.** A translated fork, a printed workbook, a
   paid bootcamp — GPL-3.0 promises all of those. We cannot promise them on top
   of borrowed problems.

There is a teaching dividend too. A learner who recognises an exercise by title
can retrieve a remembered answer without solving anything. Original problems
defeat that. This course measures whether you can write the code, not whether
you have seen the puzzle.

---

## What is allowed

**Classic tasks, written our way.** FizzBuzz, Celsius to Fahrenheit, a prime
check, a word-frequency count — these are folk exercises with no single author,
and they are fine to *assign*. What must be ours is the statement, the domain,
the bounds, the examples, and the edge cases. Write the spec yourself; do not
copy anyone's phrasing of it.

**Reference by name and link.** Titles are not copyrightable —
[37 CFR § 202.1(a)](https://www.law.cornell.edu/cfr/text/37/202.1) excludes
"names, titles, and slogans." A hyperlink reproduces nothing. So this form is
fine, and is the standard one:

> **Practice elsewhere.** The same pattern appears as
> [LeetCode 1 · Two Sum](https://leetcode.com/problems/two-sum/) if you want a
> judge to run against.

Title, number, plain out-link. Nothing else crosses over.

**Standard library behaviour and documented APIs.** Quoting a real exception
string, a `--help` output, or a documented signature is fact, not expression.
Quote them exactly — a paraphrased traceback is worse than useless to a beginner
searching for it.

**Well-known public datasets, named and linked.** Iris, Titanic, and the
`sklearn.datasets` built-ins are standard teaching data and are fine. Name the
source and check the terms before adding any new one. Prefer data the learner
can generate or that ships with a library — an exercise that needs a download is
an exercise that breaks offline.

**Teaching a published method.** Test-driven development, the accumulator
pattern, the guard clause — these are procedures, excluded by § 102(b). We teach
them in our own words. We do not copy anyone's write-up of them.

---

## What is forbidden

- Any problem statement taken or adapted from another course, platform, book, or
  tutorial.
- Any example input/output taken from another source, including its explanation.
- Any constraint block taken from elsewhere. **Choose our own bounds, and justify
  them pedagogically.**
- Any starter file or solution derived from another author's code, including
  their variable names when those are distinctive.
- Any section that announces borrowed provenance — `Constraints (LeetCode)`,
  `adapted from`, or similar. If that phrase is needed, what follows it is
  already a violation.
- Any logo, stylesheet, or repo name implying affiliation with a platform.
- Scraping any platform for problems. That is contract, not copyright, and the
  fair-use arguments above do not reach it.
- **CodePath material in any form.** Their terms require prior written consent to
  republish. Their pedagogy may be described in our words; their prose and
  problem sets may not be reproduced at all.

---

## Tells that mean something was copied

Any of these in a diff is a rejection, no discussion:

| Tell | Why it is a tell |
|---|---|
| `.length`, `console.log`, `System.out` in a spec | This course is Python. It came from somewhere |
| `nums`, `arr`, `s`, `k` with no domain meaning | Platform-generic naming. Ours are named for the story |
| A bound like `1 <= n <= 10^4` with no stated reason | We justify every bound. An unjustified one was inherited |
| An example that demonstrates rather than teaches | Ours are chosen to punish a specific wrong approach |
| A dataset appearing with no source line | Either invented and unverified, or lifted |
| Expected output nobody ran | Every output block in this course came from a real run |

---

## How to write an original exercise

**Do not open the other site.** Start from the skill, not from a page.

1. **Name the skill** you need to drill — "reading a CSV and filtering rows
   without losing a quoted comma."
2. **Invent a domain** where that skill is the natural move. Sign-up sheets,
   sensor logs, a roastery catalogue, mentor hours. Real nouns, small numbers.
3. **Write the contract yourself.** Inputs, output, and — deliberately — what
   happens on the empty case, the malformed case, and the tie. Vary these from
   the obvious defaults.
4. **Choose constraints that teach.** Every bound should have a reason you can
   say out loud: this size makes the naive version too slow; this one forces
   validation; this one keeps the recursion safe.
5. **Write examples that teach.** Include the degenerate case and at least one
   that punishes the common wrong approach.
6. **Run it.** Solve your own exercise and paste the real output. An expected
   output block that was typed rather than run is a defect.

**A costume is not enough.** Renaming an array to "transaction amounts" is
reskinning, and reskinning still tracks someone else's contract. Change the
contract too — return a count instead of the list, or define the tie-break, or
refuse the invalid input instead of clamping it.

---

## Required footer

Every course README that references an outside practice platform carries this,
verbatim:

> **Not affiliated with, endorsed by, or sponsored by LeetCode, HackerRank,
> NeetCode, Kaggle, or CodePath.** Problem names and numbers are referenced for
> practice only; all problems, examples, constraints, starter code, and test
> data in this course are original work, published under GPL-3.0. Each named
> platform is a trademark of its respective owner.

---

## If you ever need to reproduce an outside problem verbatim

Only these are clean:

| Source | License | Note |
|---|---|---|
| [Exercism `problem-specifications`](https://github.com/exercism/problem-specifications) | MIT | Cleanest option |
| [Kattis](https://www.kattis.com/problem-package-format/spec/legacy.html) | Per-problem `license` field | Use only `public domain`, `cc0`, `cc by`, `cc by-sa` |
| [Codeforces](https://codeforces.com/blog/entry/967) | Explicit republish grant | Attribution and a direct link, next to the statement |

**Two traps.** Codeforces forbids republishing their problems on anything
"supporting automatic testing," so any graded auto-runner may carry original
problems only. And Project Euler and CSES are **CC BY-NC-SA**: ShareAlike is
viral and would drag this whole curriculum under a non-commercial license, which
is incompatible with GPL-3.0 and with letting other people build on it. Do not
use them.

---

*Questions about a specific case: open an issue before writing, not after.*
