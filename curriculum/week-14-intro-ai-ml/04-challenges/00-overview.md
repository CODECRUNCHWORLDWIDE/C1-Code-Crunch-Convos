# Week 14 — Challenges

Exercises were guided. Challenges are not. Each one specifies the goal and the dataset; the design choices are yours.

## The list

| # | File | Type | Difficulty |
|---|--------------------------------------|----------------|------------|
| 1 | `challenge-01-titanic-survival.md` | Classification | Medium |
| 2 | `challenge-02-kmeans-clustering.md` | Clustering | Medium |

## How to approach a challenge

1. **Skim the prompt** to identify the dataset, target, and metric.
2. **Spend 10 minutes exploring the data** in a Jupyter notebook or a scratch script. Print `df.info()`, `df.describe()`, value counts. Do not skip this. Beginners always skip this.
3. **Write a baseline.** Simplest possible model. Just get a number on the board.
4. **Iterate.** Try one change at a time. Did it help? Why?
5. **Write up what you found** in `solutions/challenge-XX-yourname.md` — a paragraph is enough. Include your final metrics and one thing that surprised you.

## Grading rubric (self-assessment)

Give yourself one point for each:

- [ ] Loaded and inspected the data before modelling.
- [ ] Split data correctly with `random_state` set.
- [ ] Trained at least one baseline.
- [ ] Reported the right metric for the problem (not just accuracy).
- [ ] Tried at least one improvement and measured it.
- [ ] Documented your final result in plain language.

6/6 is a strong solution.

## Datasets

- **Titanic**: `import seaborn as sns; df = sns.load_dataset("titanic")`
- **Customer data for clustering**: synthetic data you generate inside the script — instructions are in the challenge file.

No external downloads needed. Have fun.
