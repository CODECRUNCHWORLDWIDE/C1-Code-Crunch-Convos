# Getting Help

You will get stuck. That is the most useful part of learning to code — it forces you to develop debugging skills. But you should never stay stuck for hours alone. Here's how to get unblocked.

## 1. Try this first (the 20-minute rule)

Spend up to 20 minutes trying to solve it yourself. In that time:

- **Read the error message slowly.** Read it word by word. Python errors are usually informative.
- **Look at the line number** the error points to. Read 3 lines before and after.
- **Print, print, print.** Add `print(variable)` to see what your code is actually doing.
- **Re-read the prompt.** Did you misread the question?
- **Compare to the example.** Where does your code differ from the lecture example?

If you can't solve it after 20 minutes, ask for help. Staying stuck longer rarely helps.

## 2. Ask a good question

A great question gets a great answer. A bad question gets ignored. Use this template:

```text
**What I'm trying to do:**
Write a function that returns the average of a list of numbers.

**What I tried:**
def average(nums):
    return sum(nums) / len(nums)

**What I expected:**
average([1, 2, 3]) → 2.0

**What actually happened:**
ZeroDivisionError: division by zero

**Where I'm confused:**
I think empty lists break my function but I'm not sure how to handle it.
```

This pattern is sometimes called the "[Rubber Duck](https://rubberduckdebugging.com/)" pattern — half the time, just writing the question makes you spot your own bug.

## 3. Where to ask

| Channel                                                                                            | Best for                                |
| -------------------------------------------------------------------------------------------------- | --------------------------------------- |
| [GitHub Discussions](https://github.com/CODE-CRUNCH-CLUB/C1-Code-Crunch-Convos/discussions)        | Curriculum questions, project showcase  |
| [GitHub Issues](https://github.com/CODE-CRUNCH-CLUB/C1-Code-Crunch-Convos/issues)                  | Bugs, typos, broken links               |
| [Python Discord](https://discord.gg/python)                                                        | Real-time Python help (active 24/7)     |
| [Stack Overflow](https://stackoverflow.com/questions/tagged/python)                                | Specific technical questions            |
| [r/learnpython](https://www.reddit.com/r/learnpython/)                                             | Beginner-friendly Python community      |

## 4. Searching effectively

Before posting, **search**. Most beginner questions have been asked thousands of times.

- Copy the **exact error message** (the last line of the traceback) into Google.
- Include `python` or `python3` in your search.
- Look for [Stack Overflow](https://stackoverflow.com/) answers with high vote counts.
- Don't trust an answer just because it's the top result — check the date (Python 2 answers are everywhere).

## 5. Reading the docs

The [official Python docs](https://docs.python.org/3/) are the single best source of truth. Bookmark them.

- The **Library Reference** is the answer to "what does this function do?".
- The **Tutorial** is the answer to "how does this language feature work?".
- Module docs (e.g. [`datetime`](https://docs.python.org/3/library/datetime.html)) have runnable examples.

If a tutorial blog post contradicts the official docs, the docs are right.

## 6. Using AI assistants responsibly

Tools like ChatGPT, Claude, and Copilot can be helpful — but lean on them carefully:

- ✅ Use them to **explain** an error or concept.
- ✅ Use them to **review** code you've already written.
- ❌ Don't copy-paste their code without understanding it. You'll fail Week 3 when the same pattern reappears.
- ❌ Don't use them to do exercises for you. You'll be cheating yourself out of the learning.

A rule of thumb: if you can't explain every line of code you submit, you didn't learn from writing it.

## 7. When to give up (and come back tomorrow)

Sometimes your brain just needs sleep. After ~2 hours of being stuck, a break beats persistence. Many bugs solve themselves after a walk or a night of rest.

---

**Remember:** Asking for help is a skill. The best engineers in the world ask questions constantly. The difference between them and beginners is that they ask *better* questions.
