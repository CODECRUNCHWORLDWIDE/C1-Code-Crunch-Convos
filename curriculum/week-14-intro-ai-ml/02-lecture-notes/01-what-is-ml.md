# Lecture 1 — What is machine learning?

## Read time

About 30 minutes. Re-read after Lecture 2 — it will land differently.

## A working definition

Here is the most useful one-line definition you will get this week:

> Machine learning is the practice of writing programs whose behaviour is determined by examples rather than by hand-written rules.

That is it. Everything else — neural networks, transformers, k-means, gradient boosting, the entire AI industry — is an elaboration of that single idea.

Compare two ways of writing a spam filter:

**Traditional programming.** A human reads a few thousand spam messages and writes rules:
- "If the message contains 'FREE!!!' flag it."
- "If the sender is not in the address book and the message has more than three exclamation marks, flag it."
- "If the message says 'Nigerian prince' flag it."
- "Unless it is from grandma."
- "Wait, grandma sent us a prince story last week. Let's add an exception."

This works for a while. Then spammers change tactics. Now you write new rules. Then they change again. Your rule list grows to thousands of lines. Maintenance is a nightmare. You are losing.

**Machine learning.** You collect a few thousand messages that humans have already labelled "spam" or "ham". You hand them to a program. The program looks at the words in each message and learns, on its own, which patterns predict the label. When new spam comes along, you re-label some of it and re-train. The "rules" are now numbers inside the model, automatically adjusted to whatever the data says.

Same problem. Different solution. The ML solution scales because the human cost is bounded: humans label, humans do not write rules. The rules are emergent.

## What ML is NOT

We have to start here because the term is used so loosely that it has become almost meaningless.

- **ML is not intelligence.** A trained model does not "understand" anything. A spam classifier does not know what spam is. It knows which numerical patterns in word counts tend to coincide with the label `1`. It will happily mark a heartfelt letter as spam if the letter happens to share those patterns.
- **ML is not magic.** Every prediction can, in principle, be traced back to a calculation on numbers. Some models (decision trees, linear regression) are easy to trace. Some (giant neural networks) are hard. But there is no oracle in the box.
- **ML is not always better than rules.** If the rules are clear, write the rules. ML is for problems where the rules are unclear, numerous, or constantly changing — pattern problems, not logic problems.
- **ML is not "AI" in the sci-fi sense.** When marketers say "AI", they usually mean "a statistical model trained on data". That is fine, but do not confuse it with HAL 9000.
- **ML does not replace the need to think.** It replaces the need to enumerate rules. You still have to choose the problem, choose the features, judge the metrics, and decide whether to ship.

A good mental model: machine learning is `if`/`else` learned from examples instead of typed from a keyboard.

## Pattern recognition, with math

What ML actually does is fit a mathematical function `f` such that `f(input) ≈ output` for the examples you have shown it. That function has parameters (sometimes a few, sometimes billions), and "training" is the process of nudging those parameters until the predictions on training data look right.

The smallest example: fit a straight line through points. You probably did this in high school. You have `(x, y)` pairs, and you want a line `y = m*x + b` that minimises the squared distance from the points. That is **linear regression**. It is also full-on machine learning. The parameters are `m` and `b`. The training process picks them.

A slightly bigger example: fit a curve to thousands of pixels in an image so that the curve outputs `0.96` when there's a cat and `0.01` when there isn't. That is a convolutional neural network. The parameters are millions of numbers. The training process is the same idea — adjust parameters to minimise an error function. Just more of it.

The principle is the same at both scales. The math gets fancier, the libraries help more, but the loop is:

1. Make a guess.
2. Measure how wrong the guess was.
3. Nudge the parameters in a direction that reduces the wrongness.
4. Repeat.

## The data is the program

Karpathy famously called this "Software 2.0". The conceptual shift is huge: in classical programming, the source code is the program. In ML, the source code is short — `model = LogisticRegression(); model.fit(X, y)` — but the program's behaviour is mostly determined by `X` and `y`. The dataset is the program.

Implication 1: **garbage in, garbage out**. If your data is biased, mislabelled, or unrepresentative, your model will faithfully reproduce those problems. This is not a model bug. It is a data property. We will hammer on this all week.

Implication 2: **debugging shifts**. You do not step through code with a debugger to find why the model said "spam". You inspect the data, the features, the metrics, and you ask: *which examples is it getting wrong, and what do they have in common?* Debugging ML is debugging datasets and pipelines, not stack traces.

Implication 3: **versioning matters in new ways**. You now have to version not just the code but the data and the trained model. Three artefacts, not one.

## The two big families

Most of ML splits along one axis:

### Supervised learning

You have inputs (`X`) and known outputs (`y`). You want to predict `y` from `X` for new examples. Spam classification (text → label), house price prediction (features → price), medical diagnosis (test results → condition) — all supervised.

Supervised learning splits again:

- **Classification** — `y` is a category. Spam/ham. Setosa/versicolor/virginica. Survived/died. Output is a label.
- **Regression** — `y` is a number. House price. Temperature tomorrow. Click-through rate. Output is a scalar.

If you can ask "which one is this?", it's classification. If you can ask "how much?", it's regression.

### Unsupervised learning

You have inputs (`X`) but no labels. You want the algorithm to discover structure on its own. Customer segmentation (group similar customers without knowing the groups in advance), anomaly detection, topic modelling — all unsupervised.

The classic unsupervised method we will see this week is **k-means clustering**: tell the algorithm how many groups you want, and it groups your data into that many clusters by similarity.

### Other families (not this week)

- **Semi-supervised** — most data unlabelled, a little labelled. Useful when labels are expensive.
- **Reinforcement learning** — learning by trial and error against a reward signal. Game-playing agents, robotics.
- **Self-supervised** — the model generates its own labels from the data (the foundation of modern LLMs).

This week is supervised + a peek at unsupervised. That is enough to be dangerous.

## The ML workflow

Almost every supervised ML project follows the same nine-step shape. Memorise this.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  1. Frame the problem    ──>  Is this a classification? Regression?    │
│                               What does "success" mean numerically?    │
│                                                                        │
│  2. Get the data         ──>  CSV, database, API, files, scrapes.      │
│                                                                        │
│  3. Explore the data     ──>  pandas, plots. Look for nulls,           │
│                               outliers, weirdness. (Week 13 muscle.)   │
│                                                                        │
│  4. Clean & engineer     ──>  Drop or impute nulls. Build new          │
│     features                  features. Encode categoricals.           │
│                                                                        │
│  5. Split                ──>  train_test_split. Keep test set untouched │
│                               until the very end.                      │
│                                                                        │
│  6. Train baseline       ──>  Simplest model that could work.          │
│                               LogisticRegression is a great default.   │
│                                                                        │
│  7. Evaluate             ──>  Right metric for the problem. Accuracy   │
│                               is not always the right metric.          │
│                                                                        │
│  8. Iterate              ──>  Try more models. Tune hyperparameters.   │
│                               Add features. Re-evaluate.               │
│                                                                        │
│  9. Ship & monitor       ──>  Save the model. Wire it into prod.       │
│                               Watch for drift over time.               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

Beginners usually skip steps 1, 3, and 9. Senior ML practitioners spend most of their time on 1, 3, 4, and 9.

A practical warning: **never look at your test set during steps 4–8**. The moment your eyes touch it, it stops being a test set and becomes another training set. We will see why this matters in Lecture 3.

## When ML is the right tool

Use ML when:

- The problem is fundamentally **pattern-shaped** rather than rule-shaped. Lots of fuzzy edge cases, lots of "you know it when you see it".
- You have, or can get, **enough labelled examples**. "Enough" depends on the problem — a few hundred for simple classifiers, millions for large language models. As a rule of thumb: if you cannot collect ten times as many examples as you have features, reconsider.
- The cost of being **occasionally wrong** is acceptable. Spam filter occasionally lets one through? Fine. Medical diagnosis occasionally misses cancer? Very much not fine — and even when ML is the right tool there, it lives behind a clinician.
- The underlying distribution is **reasonably stable**. If next month's spam looks nothing like last month's, you need to plan for retraining.

## When ML is the wrong tool

Do not use ML when:

- The rules are **clear and stable**. Tax brackets. Currency conversion. Don't train a model. Write the formula.
- You have **almost no data**. Three examples and a hope is not training data.
- A mistake is **catastrophic and unauditable**. If you cannot explain why your model denied someone a loan, do not deploy a model to deny loans. (More on this in Lecture 3.)
- The problem is actually **a search problem**. "Find the document matching this query" — that is information retrieval. ML can help rank results, but the core problem is not learned.
- **Speed and determinism** matter more than accuracy. A regex finishes in microseconds and never surprises you.
- You are using it to **automate away accountability**. "The algorithm decided" is not an answer when a human asks why their kid lost benefits.

A useful self-test: write down what a non-ML solution would look like. If you can sketch one and it's good enough, ship that and move on.

## A small concrete example to chew on

Suppose you run a bookstore and you want to predict which books a customer will buy next month. Walk through the workflow in your head:

1. **Frame.** Per customer, predict the set of books they'll purchase. Classification per (customer, book) pair? Or recommend a top-N list? Different framings, different models.
2. **Get the data.** Historical purchases per customer. Maybe browsing data. Maybe demographics.
3. **Explore.** What's the distribution of purchases per customer? Power law (some customers buy a lot, most buy nothing)? Are there cold-start customers with no history?
4. **Engineer.** Per (customer, book) pair, features could be: customer's average price tolerance, books in the same genre they've bought, time since last purchase.
5. **Split.** Train on purchases before October, test on purchases in November.
6. **Baseline.** Predict the most-popular books, ignoring the customer entirely. This is your floor. Beat it.
7. **Evaluate.** Top-10 precision? Revenue per recommendation? Choose what matters to the business.
8. **Iterate.** Add collaborative-filtering features. Try a tree model.
9. **Ship.** Run the model nightly, write recommendations to the user profile table.

This whole thing — the workflow, the framing, the metric choice, the baselines — is the actual job. The library call is the easy part.

## What you should take away

- ML is `if`/`else` learned from examples.
- The data is the program. Bad data ⇒ bad model. Always.
- Supervised vs unsupervised; classification vs regression. Know the four boxes cold.
- The workflow has nine steps. Skip steps at your peril.
- Most problems do not need ML. Recognising those is a skill.

In Lecture 2 we will write actual code: load data, split it, train a model, evaluate it. The pieces will start clicking together.

## Self-check

Before moving on, you should be able to answer (out loud, no peeking):

1. What is the difference between classification and regression? Give one example of each.
2. What is the difference between supervised and unsupervised learning?
3. Why is "the data is the program" a useful frame?
4. Name three situations where ML is the wrong tool.
5. What is the first step of the ML workflow, and why is it the one beginners skip?

If any of those are fuzzy, re-read the relevant section.

On to Lecture 2.
