# Milestone 05 — Ship & Present (Days 6–7)

## Goal

By end of Day 7, your project is **deployed** (if it has a web UI), a
**walkthrough video** of 3–5 minutes is recorded and linked from the
README, the repo is **pinned** on your GitHub profile, a
**retrospective** is in `docs/RETRO.md`, and the [submission checklist](../submission-checklist.md)
is fully ticked.

This is the most rewarding milestone. You are turning a finished
project into a *visible* finished project.

## Day 6 — Deploy and record

### AM: Deploy (Web App, API, ML inference)

Skip this section if you are on the data or automation track and have
no hosted UI. Your notebook or CLI on GitHub already *is* the demo.

1. **Pick one host** from [../resources.md](../resources.md) and stop
   shopping. Fly.io, Render, Railway, PythonAnywhere, and Hugging Face
   Spaces are all fine.

2. **Prepare for production.** Make sure your app:
   - Reads its port from `$PORT` (or your host's equivalent).
   - Binds to `0.0.0.0`, not `127.0.0.1`.
   - Loads secrets from environment variables, not hard-coded.
   - Does *not* check secrets into git. (Search your repo for "key" and
     "token" before pushing.)
   - Has a `Procfile`, `fly.toml`, or equivalent.
   - Includes any seed data script the demo needs.

3. **Deploy.** Follow your host's docs literally; do not improvise.

4. **Visit the deployed URL** from a private browser window. Sign up.
   Click around. Fix anything visibly broken.

5. **Add the URL to your README** under a *Live demo* heading. Include
   demo credentials if applicable:

   ```markdown
   ## Live demo

   <https://your-app.fly.dev>

   Sign up with any email, or try the seeded account:

   - **Email:** `demo@example.com`
   - **Password:** `demo`
   ```

6. **Commit and push** the README update.

### PM: Record the walkthrough video

Use the structure from [../lecture-notes/02-building-and-shipping.md](../lecture-notes/02-building-and-shipping.md):

| Time         | Content                                       |
|--------------|-----------------------------------------------|
| 0:00–0:20    | Who you are + project + problem.              |
| 0:20–0:50    | Live demo solving the problem end-to-end.     |
| 0:50–2:30    | Code tour: tree, README, a module, a test, CI.|
| 2:30–3:30    | A real decision or trade-off you made.        |
| 3:30–4:00    | What you'd do with another week.              |

Steps:

1. **Write talking points** (not a full script). Bullet list, half a
   page. Run through them once out loud before recording.

2. **Set up your screen.** Close Slack, hide bookmarks, increase font
   size. Maybe disable notifications.

3. **Record in 2–3 takes.** Pick the best one. Do not edit per
   sentence; viewers tolerate a "uh" more than a visible cut.

4. **Upload as Unlisted** to YouTube or Loom. Copy the URL.

5. **Add the URL to your README** under a *Walkthrough video*
   heading.

6. **Commit and push.**

## Day 7 — Retro, pin, submit

### AM: Retrospective

Write `docs/RETRO.md`. This is a short (≈ 500 words) reflection. It is
*not* a marketing piece — be honest. Three sections work well:

```markdown
# Capstone Retrospective

## What went well

- Three or four bullets. What did you do that you are proud of? Did the
  Day 1 proposal hold up? Did you finish on time? Did you learn
  something about your own working style?

## What was hard

- Three or four bullets. Where did you get stuck? What took twice as
  long as you thought? What did you have to cut?

## What I would do differently next time

- Three or four bullets. Concrete decisions, not "be better at coding".
  E.g. "Start the CI on Day 1, not Day 2."

## What I learned

- Two or three bullets. Specific skills or habits that stuck.
```

Commit and push as `docs(retro): add capstone retrospective`.

### Midday: pin the repo

Follow [../lecture-notes/03-presentation-and-portfolio.md](../lecture-notes/03-presentation-and-portfolio.md)
section *Pinning your repo*. Pin the capstone in **position 1**. Untick
old practice repos. Verify the GitHub profile loads with the capstone
on top.

While you are here:

- Add a one-line description to the repo.
- Add 3–5 topics: `flask`, `python`, `capstone`, `bootcamp`, plus one
  topic for your track.
- If you have not yet, write a tiny **profile README** in the
  `<your-username>/<your-username>` repo with a one-line bio and links
  to the capstone and your email/LinkedIn.

### PM: Final pass and submit

1. **Walk the [submission checklist](../submission-checklist.md)
   top to bottom.** Tick each item *only* after you have actually
   verified it.

2. **Do a final "stranger test"** of the README in a clean clone:

   ```bash
   cd /tmp
   git clone https://github.com/<you>/<repo>.git capstone-test
   cd capstone-test
   # follow README install steps exactly
   ```

3. **Submit.** Wherever you submit (a form, a PR to the bootcamp's
   `projects/capstone/` folder, a message to your mentor), include:

   - The GitHub repo URL.
   - The walkthrough video URL.
   - The deployed demo URL (if applicable).
   - A 2-sentence pitch — the same one from the top of your README.

4. **Tell people.** Post on the community channel; tell a friend; share
   on LinkedIn or Mastodon. The bootcamp ends today. The project lives
   on as long as you keep talking about it.

## Outputs

By end of Day 7:

- [ ] (If web) The app is deployed and reachable at a public URL.
- [ ] A 3–5 minute walkthrough video is unlisted on YouTube/Loom and
      linked from the README.
- [ ] `docs/RETRO.md` exists.
- [ ] The repo is pinned in position 1 on your GitHub profile.
- [ ] The repo description and topics are set.
- [ ] Submission is in (per your cohort's process).
- [ ] All boxes in [submission-checklist.md](../submission-checklist.md)
      are ticked.

## Pitfalls

- **Trying to record perfectly.** Three takes is enough. Recruiters do
  not grade a video on pronunciation — they grade it on whether you
  understand what you built. Stop polishing.
- **Deploying at midnight on Day 7.** Hosting providers can fail; DNS
  can be slow; your free dyno can take 90 seconds to wake up. Deploy on
  Day 6 morning so there is room to fix things.
- **Writing the retro like marketing.** "Everything went amazingly!"
  retros help nobody — least of all future-you. Be honest.
- **Forgetting to pin.** This is the single highest-leverage minute of
  the week.

## Done check

- [ ] Demo URL works (if applicable).
- [ ] Video URL works.
- [ ] Retro is committed.
- [ ] Repo is pinned.
- [ ] Submission is in.

You did it. Welcome to the other side.
