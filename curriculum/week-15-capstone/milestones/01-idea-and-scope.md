# Milestone 01 — Idea & Scope (Day 1)

## Goal

By end of Day 1, you have a **1-page proposal** in `docs/PROPOSAL.md`
that names the problem, the user, the MVP in a single sentence,
explicit anti-goals, your tech stack, and a milestone-by-milestone plan
with dates. The proposal is committed to your (still local-only, that's
fine) repo.

You write *no application code* today. The day's product is the plan.

## Tasks

1. **Block out two uninterrupted hours.** Planning while distracted
   produces vague plans, which produce vague projects.

2. **Brainstorm three project ideas.** For each, write one sentence: the
   problem, and who has it. Cross out any idea you do not personally
   care about — you will not finish it.

3. **Pick a track.** One of:
   - Web App (Flask + DB + auth)
   - Data (notebook + package + writeup)
   - ML (train + deploy a model)
   - Automation (a tool that solves a real workflow problem)
   - API (REST API + docs + deploy)

   Read the matching `examples/<track>.md` file in this week's folder
   for a worked example.

4. **Write the MVP sentence.** A single sentence of the form
   *"<User> can <verb> <object> and see <result>."* If you cannot write
   that sentence, the idea is not concrete enough yet.

5. **Write 3 to 5 user stories.** Each in the form
   *"As a <user>, I want to <action>, so that <benefit>."* These become
   the GitHub issues you open in Milestone 02.

6. **Write explicit anti-goals.** At least four things you are
   deliberately *not* doing this week. Anti-goals are how you defend the
   MVP from scope creep.

7. **Pick your tech stack and freeze it.** Write the version-pinned
   Python and library list. Refuse to change it during the week without
   a good reason.

8. **Lay out milestones with dates.** Copy the table from this week's
   README and add real calendar dates for each milestone.

9. **Create the repo locally.** `mkdir <project>`, `cd <project>`,
   `git init`, `mkdir docs`, save the proposal as `docs/PROPOSAL.md`,
   commit. You will push it to GitHub tomorrow.

## Outputs

By end of Day 1 you have:

- A local git repo with one commit.
- `docs/PROPOSAL.md` containing:
  - Project title
  - Problem statement (2–3 sentences)
  - User (who is this for?)
  - **The MVP sentence**
  - 3–5 user stories
  - 4+ anti-goals
  - Tech stack (with versions)
  - Milestones with calendar dates
- A clear, decided **track** from the list of five.

## Proposal template

Copy this into `docs/PROPOSAL.md` and fill it in. Keep it on one page.

```markdown
# <Project Name> — Capstone Proposal

**Author:** <your name>
**Track:** <Web App | Data | ML | Automation | API>
**Date:** <today>

## Problem

<2–3 sentences. What problem does this solve, and why does anyone
care? Write it like you are explaining it to a friend at lunch.>

## Users

<Who is this for? "Me" is a valid answer. "Everyone" is not.>

## MVP

> *<One sentence in the form: "<User> can <verb> <object> and see
> <result>.">*

## User stories

1. As a ..., I want to ..., so that ....
2. As a ..., I want to ..., so that ....
3. As a ..., I want to ..., so that ....

## Anti-goals (NOT building this week)

- ...
- ...
- ...
- ...

## Tech stack

- Python 3.x
- <framework or library 1>
- <framework or library 2>
- Testing: pytest, pytest-cov
- Lint/format: ruff (and/or black)
- CI: GitHub Actions
- Hosting: <Fly.io | Render | Railway | GitHub Pages | N/A>

## Milestones

| Day(s)   | Milestone               | Status |
|----------|-------------------------|--------|
| Day 1    | Idea & Scope            | <date> |
| Day 2    | Design & Skeleton       | <date> |
| Day 3    | Build Core (AM, PM)     | <date> |
| Day 4    | Build Core (AM, PM)     | <date> |
| Day 5    | Test & Polish           | <date> |
| Day 6    | Ship & Present          | <date> |
| Day 7    | Ship & Present          | <date> |

## Risks

<Two or three things you are worried about, and what you'll do if they
happen. E.g. "If the public transit API is rate-limiting me, I will
cache responses locally and fall back to the cached version.">
```

## Worked example

For a thin walked-through example, see the *Habit Tracker* worked plan
inside [../lecture-notes/01-planning-your-capstone.md](../lecture-notes/01-planning-your-capstone.md)
at the end. It uses exactly this template.

## Pitfalls

- **"I'll decide the MVP later."** Then you will spend the week
  deciding instead of building. Decide today.
- **Two MVPs.** "A blog *and* a chatbot" is two projects. Pick one. The
  other goes in your post-bootcamp list.
- **Avoiding anti-goals.** Listing what you *will not* build feels
  pessimistic. It is actually the most useful section of the proposal.
- **Choosing tech you have never used.** This week is not for
  learning a new framework. Use what Weeks 1–14 taught you.
- **Planning for more time than you have.** Be ruthless: how many
  *real* hours will you spend tomorrow? Plan for those, not the
  optimistic version.

## Done check

You are done with Milestone 01 when:

- [ ] `docs/PROPOSAL.md` exists and fits on one screen.
- [ ] You can recite the MVP sentence without looking at the file.
- [ ] You have at least four anti-goals.
- [ ] The tech stack is committed-to.
- [ ] The milestone table has real dates.
- [ ] The proposal is committed to git.

Tomorrow: scaffold the repo. See
[02-design-and-skeleton.md](02-design-and-skeleton.md).
