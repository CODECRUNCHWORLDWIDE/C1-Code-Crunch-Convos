# Week 14 — Resources

A curated, intentionally short list. Read the official docs first; books second; videos third. Skip nothing in the "core" section.

## Core (read these this week)

- **scikit-learn — official site.** <https://scikit-learn.org/stable/>
  Start here for everything API-related. The front page links to "Getting Started", which is genuinely good.
- **scikit-learn — User Guide.** <https://scikit-learn.org/stable/user_guide.html>
  Treat this like a textbook. Sections you should at least skim this week:
  - 1.1 Linear Models
  - 1.10 Decision Trees
  - 1.13 Feature selection
  - 3. Model selection and evaluation (especially 3.1, 3.3, 3.4)
  - 6. Dataset transformations (Pipelines and ColumnTransformer)
- **scikit-learn — API reference.** <https://scikit-learn.org/stable/api/index.html>
  When you need to look up exact arguments, default values, or return shapes — this is where you go. Get used to reading it.

## Books

- **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurelien Geron** (3rd edition).
  The gold standard for practical ML in Python. Chapters 1–3 alone cover most of what we do this week, with worked examples. If you only buy one ML book this year, buy this one.
- **"Introduction to Machine Learning with Python" by Andreas Mueller and Sarah Guido.**
  Mueller is a core scikit-learn maintainer. The book is shorter than Geron's and laser-focused on scikit-learn idioms. Excellent companion read.
- **"Weapons of Math Destruction" by Cathy O'Neil.**
  Non-technical, essential. Case studies of algorithmic systems causing real harm at scale (sentencing, hiring, insurance, education). Read this before you ever ship a model that touches another human being's life. It is short. There is no excuse.

## Video (use sparingly — coding beats watching)

- **3Blue1Brown — "Neural Networks" playlist on YouTube.**
  <https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi>
  The clearest visual intuition for what a neural network actually does. We do not train neural nets this week — but understanding the math here will make the rest of your career easier. Four episodes, about an hour total.

## Mentioned only

- **fast.ai.** <https://www.fast.ai/>
  A free, opinionated, top-down deep-learning course. Not a fit for this week (we want bottom-up first), but bookmark it for after you finish the bootcamp.

## Datasets you will see this week

- **Iris** — built into scikit-learn (`load_iris`). The "hello world" of classification.
- **Titanic** — available via seaborn (`sns.load_dataset("titanic")`) and on Kaggle.
- **SMS Spam Collection** — UCI Machine Learning Repository.
  <https://archive.ics.uci.edu/dataset/228/sms+spam+collection>
  We use a small synthetic CSV in the mini-project so you can run things offline, but the real UCI dataset is a useful next step.
- **California Housing** — built into scikit-learn (`fetch_california_housing`). Replacement for the deprecated Boston housing dataset.

## Cheat sheet (one-pager)

Bookmark this and revisit it whenever you are lost:

- `model = Estimator(...)` — create the model with hyperparameters.
- `model.fit(X_train, y_train)` — learn from training data.
- `model.predict(X_test)` — produce predictions.
- `model.score(X_test, y_test)` — convenience: accuracy or R squared.
- `transformer.fit_transform(X)` — fit + transform in one shot (for preprocessing).
- `train_test_split(X, y, test_size=0.2, random_state=42)` — split data.
- `from sklearn.pipeline import Pipeline` — chain steps.
- `from sklearn.compose import ColumnTransformer` — different preprocessing per column.
- `from sklearn.metrics import classification_report, confusion_matrix` — evaluate.
- `import joblib; joblib.dump(model, "m.joblib")` — save. `joblib.load(...)` — load.

Once these become muscle memory, you will be productive across most ML libraries.

## What to skip

You will see a lot of content online about transformers, LLMs, agents, RAG, and "AI engineering". Almost none of it will make sense without the foundations you are building this week. Resist the temptation to chase shiny tools. After Week 14 you can pick them up in days; without Week 14 you will fake it for years.
