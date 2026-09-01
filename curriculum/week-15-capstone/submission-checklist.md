# Submission Checklist

The last thing you do before you submit. Walk this list top to bottom
and tick each box *only* after you have actually verified it. If you
cannot truthfully tick a box, fix the underlying issue rather than
leaving it blank.

## 1. Code is on GitHub

- [ ] `git status` reports a clean working tree.
- [ ] `git push` reports "Everything up-to-date".
- [ ] Opening the repo on GitHub in a private browser window shows the
      latest commit on `main`.

## 2. Repo is public

- [ ] Repo settings show **Public** visibility.
- [ ] You can open the repo URL in a logged-out browser tab.
- [ ] No private files (datasets, secrets, personal info) are checked
      in. (Run `git ls-files | grep -Ei "key|token|password|\.env$"` —
      it should return nothing.)

## 3. README is excellent

- [ ] Title and one-sentence pitch.
- [ ] CI status badge near the top.
- [ ] At least one screenshot or GIF of the project working.
- [ ] Features section (3–5 bullets).
- [ ] Install instructions, in a fenced code block, copy-pasteable.
- [ ] Usage section with one realistic example and its output.
- [ ] Live demo link (if applicable).
- [ ] Walkthrough video link.
- [ ] Project structure (a `tree`-style snippet).
- [ ] Development setup: how to run tests and lints.
- [ ] Contributing section (or link to `CONTRIBUTING.md`).
- [ ] License section pointing to the `LICENSE` file.
- [ ] Acknowledgements (datasets, libraries, mentors).
- [ ] You re-cloned the repo into a fresh `/tmp` directory and followed
      the install steps *exactly* — and it worked.

## 4. License is added

- [ ] A `LICENSE` file exists at the repo root.
- [ ] GitHub recognises the license — it shows the license name in the
      repo's right sidebar.
- [ ] The README's License section names the same license.

## 5. Tests pass on CI

- [ ] `pytest` runs locally with no failures.
- [ ] `pytest --cov` reports **≥ 70%** coverage.
- [ ] `ruff check .` exits clean.
- [ ] `black --check .` exits clean.
- [ ] The CI badge on `main` is **green**.
- [ ] At least one integration test exists (not only unit tests).
- [ ] No tests are `@pytest.mark.skip` without a comment explaining
      why.

## 6. Demo works

- [ ] (Web/API) The deployed URL is reachable in a private browser
      window and the headline feature works.
- [ ] (Web/API) Demo credentials (if needed) are documented in the
      README and they actually work.
- [ ] (Data) The headline notebook re-runs top-to-bottom from a fresh
      kernel without manual intervention.
- [ ] (CLI/Automation) The headline command works on a fresh clone
      following the README's install steps.
- [ ] (ML) Both the training and inference commands work; a trained
      model artefact is committed (small) or auto-trains on first run.

## 7. Video is recorded

- [ ] The walkthrough is 3–5 minutes long.
- [ ] It is unlisted on YouTube or Loom — not "Private", not
      "Public-but-no-one-will-find-it".
- [ ] You watched the whole thing back without cringing.
- [ ] Audio is audible. Text in the recording is legible at 720p.
- [ ] The video URL is in the README under a clear heading.

## 8. Repo is pinned on profile

- [ ] You opened `https://github.com/<your-username>` in a private
      browser window.
- [ ] The capstone repo appears in the **Pinned** section, in **position 1**.
- [ ] Old, embarrassing repos are no longer pinned.
- [ ] The repo has a one-line description and 3+ topic tags on its
      settings page.

## 9. Retrospective written

- [ ] `docs/RETRO.md` exists.
- [ ] It contains at least the four sections: *what went well*, *what
      was hard*, *what I'd do differently*, *what I learned*.
- [ ] It is **honest**. (No "everything went amazingly" — that helps
      nobody.)
- [ ] It is committed and pushed.

## 10. Issue and PR hygiene

- [ ] Every "user story" issue from Milestone 02 is closed.
- [ ] Any deferred features are open as `nice-to-have` issues.
- [ ] At least one merged pull request exists with a meaningful
      description.
- [ ] No PRs are open in a "Draft" state at submission time (except
      genuine future work).

## 11. Final submission

Submit per your cohort's process. At minimum, include:

- [ ] The GitHub repo URL.
- [ ] The walkthrough video URL.
- [ ] The deployed demo URL (if applicable).
- [ ] A 2-sentence pitch — the same one from the top of your README.
- [ ] (Optional) A request for specific feedback — "I'd love a code
      review of `src/<package>/streaks.py` in particular" gets you far
      more useful reviewer attention than a generic ask.

## 12. After you submit

- [ ] Post about the project in the community channel.
- [ ] Add the project to your LinkedIn under "Projects" with the
      resume-style summary from
      [lecture-notes/03-presentation-and-portfolio.md](lecture-notes/03-presentation-and-portfolio.md).
- [ ] Pat yourself on the back. You shipped.
