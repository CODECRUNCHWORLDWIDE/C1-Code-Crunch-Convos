# ML Track Example — Movie Recommender

Train a recommender on the classic **MovieLens** dataset, then deploy
it as a small **CLI inference service**: given a user ID or a list of
liked movies, return the top-N recommended movies. The project ships
with reproducible training, evaluation metrics, and a saved model
artefact so a reviewer can re-run inference without retraining.

## MVP sentence

> *A user can run `movie-recommender for-user 42 --top 5` and get five
> ranked movie recommendations based on a model trained on the
> MovieLens 100K dataset.*

If that sentence is true after a clean clone and `pip install -e .`,
the MVP is done.

## Two algorithm options — pick one

For a week-sized project, you should pick *one* of these two
approaches. Do not try both.

- **Content-based** — embed each movie as a vector of its genre tags
  (and/or title TF-IDF) and recommend the movies most similar to ones
  the user has rated highly. Simple, no matrix factorisation, and
  works for "cold-start" new users if you accept a list of liked movies
  rather than a user ID.
- **Collaborative filtering** — factorise the user-item rating matrix
  (`scikit-learn`'s `TruncatedSVD`, or `implicit` for an ALS variant).
  Better recommendations for known users; useless for users not in the
  training set.

Pick *content-based* if you want a simpler week. Pick *collaborative
filtering* if you want to flex Week 14 a bit more.

## User stories

1. **Train.** As a developer, I can run `movie-recommender train` to
   train and save a model artefact to `models/recommender.pkl`.
2. **Recommend.** As a user, I can run `movie-recommender for-user 42
   --top 5` and get five ranked recommendations.
3. **Cold-start.** As a new user, I can run
   `movie-recommender similar-to "Toy Story (1995)" --top 5` and get
   five movies similar to one I already like.
4. **Evaluate.** As a developer, I can run
   `movie-recommender evaluate` and see a printed RMSE (collaborative)
   or precision@k (content-based) over a held-out split.

## Anti-goals

- A web UI.
- Real-time learning / online updates.
- Multiple algorithms in one repo (pick one).
- A 10 GB MovieLens variant — use **MovieLens 100K** or **MovieLens 1M**
  at most.
- Hyperparameter tuning beyond two or three values per knob.

## Suggested tech stack

- Python 3.11+
- `pandas`, `numpy`
- `scikit-learn` for vectorising and basic factorisation
- (Optional) `implicit` for ALS — only if you go collaborative
- `click` for the CLI
- `joblib` for saving and loading models
- `pytest` + `pytest-cov`
- `ruff` + `black`
- GitHub Actions

## Folder layout

```text
movie-recommender/
├── src/movie_recommender/
│   ├── __init__.py
│   ├── cli.py             # click entry point
│   ├── data.py            # load_ratings(), load_movies()
│   ├── content.py         # content-based model
│   ├── collab.py          # collaborative filtering model (if chosen)
│   ├── evaluate.py        # train/test split + metrics
│   └── persistence.py     # save_model, load_model
├── tests/
│   ├── fixtures/
│   │   ├── ratings_tiny.csv
│   │   └── movies_tiny.csv
│   ├── test_data.py
│   ├── test_content.py
│   └── test_cli.py
├── models/                 # checked-in trained artefact (small!)
│   └── recommender.pkl
├── data/
│   └── .gitkeep            # raw MovieLens is downloaded, not committed
├── docs/
│   ├── PROPOSAL.md
│   └── RETRO.md
├── .github/workflows/ci.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

## Dataset

Use the **MovieLens 100K** dataset:
<https://grouplens.org/datasets/movielens/100k/>. Don't commit it — your
`data.py` should download and cache it on first run.

License note: MovieLens data is research-use, freely redistributable
*with attribution*. Mention GroupLens in your README's
"Acknowledgements" section.

## A representative `content.py`

```python
"""A simple content-based movie recommender."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ContentModel:
    """A fitted content-based recommender.

    Attributes:
        movies: DataFrame indexed by ``movie_id`` with column ``title``.
        features: TF-IDF feature matrix, one row per movie.
        vectorizer: The fitted ``TfidfVectorizer``, kept so we can
            embed new free-text queries.
    """

    movies: pd.DataFrame
    features: np.ndarray
    vectorizer: TfidfVectorizer

    def similar_to(self, title: str, top_n: int = 5) -> pd.DataFrame:
        """Return the ``top_n`` movies most similar to ``title``."""
        match = self.movies[self.movies["title"].str.casefold() == title.casefold()]
        if match.empty:
            raise KeyError(f"No movie titled {title!r} in the catalogue.")
        idx = match.index[0]
        sims = cosine_similarity(self.features[idx], self.features).ravel()
        sims[idx] = -1.0  # exclude itself
        top_idx = np.argpartition(-sims, top_n)[:top_n]
        top_idx = top_idx[np.argsort(-sims[top_idx])]
        return self.movies.iloc[top_idx].assign(score=sims[top_idx])


def fit(movies: pd.DataFrame) -> ContentModel:
    """Fit a content-based model from a ``movies`` DataFrame.

    ``movies`` must have columns ``movie_id``, ``title``, and ``genres``
    (pipe-separated, in the MovieLens convention).
    """
    text = movies["genres"].str.replace("|", " ", regex=False)
    vectorizer = TfidfVectorizer(min_df=1)
    features = vectorizer.fit_transform(text).toarray()
    return ContentModel(
        movies=movies.set_index("movie_id"),
        features=features,
        vectorizer=vectorizer,
    )
```

That fits in one file, is testable, has a docstring on every public
piece, and uses type hints throughout — exactly what the rubric
rewards.

## Day-by-day plan

**Day 1.** Proposal. Decide content vs collaborative.

**Day 2.** Skeleton, CI, click CLI with three stub commands that print
"not yet implemented".

**Day 3 AM.** `data.py` — download MovieLens 100K, cache to `data/`,
load into pandas. Test against `ratings_tiny.csv` fixture.

**Day 3 PM.** Fit the model (content or collaborative). Save with
joblib. Print the top-5 for one example user/movie at the end of
`train`.

**Day 4 AM.** `cli.py` — wire `train`, `for-user`, `similar-to`, and
`evaluate` to the model. Tests with `click.testing.CliRunner`.

**Day 4 PM.** `evaluate.py` — a train/test split, plus precision@k
(content) or RMSE (collaborative). Print a small results table.

**Day 5.** Push coverage past 70%. Write a thorough README — explain
the algorithm in plain English, show the CLI commands and their
outputs, cite GroupLens. Add a screenshot of the evaluation output.

**Day 6.** Record the walkthrough video. Show training, then inference,
then a code tour focusing on `content.py` and one test.

**Day 7.** Retro, pin, submit.

## Where this project demonstrates each week

- **Week 6** — file I/O, CSV loading, caching the downloaded zip.
- **Week 8** — `requests` for downloading the dataset.
- **Week 11** — pytest, fixtures, CI on a model-trained artefact.
- **Week 12** — `click` CLI as a real automation interface.
- **Week 13** — pandas data wrangling.
- **Week 14** — the ML model itself, plus the evaluation step.

## "Done" check

- [ ] `pip install -e ".[dev]" && movie-recommender train` succeeds on
      a fresh clone.
- [ ] `movie-recommender for-user 42 --top 5` prints five titles.
- [ ] `movie-recommender similar-to "Toy Story (1995)" --top 5` prints
      five similar titles.
- [ ] `movie-recommender evaluate` prints a real metric.
- [ ] Coverage ≥ 70%, lint clean, CI green.

## Stretch goals

- **A tiny Flask wrapper.** One route, `/recommend?user=42&top=5`,
  returns JSON. Deploy on Fly.io.
- **A second algorithm and an A/B comparison.** Skip unless Day 5 is
  done by lunchtime.

## A note on dataset licensing

MovieLens datasets are provided by GroupLens at the University of
Minnesota for *non-commercial* research use. Cite them in your README:

> Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets:
> History and Context. *ACM TiiS*, 5(4), 1–19.
> <https://doi.org/10.1145/2827872>
