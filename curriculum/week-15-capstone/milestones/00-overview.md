# Capstone Milestones

The capstone is broken into **five milestones over seven days**. Read
this index, then follow each milestone in order. Do not skip ahead — a
shaky Milestone 1 means a shaky Milestone 5.

Each milestone file contains:

- **Goal** — what "done" looks like for this milestone.
- **Tasks** — a numbered checklist.
- **Outputs** — the artefacts you produce.
- **Pitfalls** — common ways students stall here.

## Index

| #   | Day(s)   | Milestone                                                    | Outcome                                |
|-----|----------|--------------------------------------------------------------|----------------------------------------|
| 01  | Day 1    | [Idea & Scope](01-idea-and-scope.md)                         | A 1-page proposal merged to `main`.    |
| 02  | Day 2    | [Design & Skeleton](02-design-and-skeleton.md)               | Public repo with green CI on a stub.   |
| 03  | Day 3–4  | [Build Core](03-build-core.md)                               | MVP working on a feature branch.       |
| 04  | Day 5    | [Test & Polish](04-test-and-polish.md)                       | 70% coverage, lint-clean, screenshots. |
| 05  | Day 6–7  | [Ship & Present](05-ship-and-present.md)                     | Deploy, video, retro, submit.          |

## How to use the milestones

Each evening, open the next milestone file. At the top of every file is
a **Goal**. Read that first. If you can already check off every task in
the milestone, move on. If you cannot, do the tasks in order.

Each milestone ends with **Outputs** — the concrete things that should
exist in your repo by the end of that day. Reviewers (including
future-you) use those Outputs to judge whether the milestone is done.

### Daily ritual

At the end of every build day, do four things in this order:

1. `git status` — make sure nothing is uncommitted.
2. `git push` — make sure everything is on GitHub.
3. Look at the CI badge. Is it green? If not, fix before tomorrow.
4. Update the **Milestones** section of `docs/PROPOSAL.md` with a tick
   or a slip note.

That last step is the one most students skip; it is the one that keeps
you honest about whether you are on track.

## If you fall behind

It happens — life is not graded on a 7-day calendar. The capstone is
graded on what you ship, not on the exact day you shipped it. The rules
of thumb:

- If you slip by half a day, *cut a feature*, not your test coverage or
  your README.
- If you slip by more than one day, message a mentor *before* extending
  yourself. They have seen every shape of stuck and can usually unstick
  you in fifteen minutes.
- Never skip the "Test & Polish" milestone to "save time". An untested,
  unpolished project will lose more points than a smaller, polished one.
