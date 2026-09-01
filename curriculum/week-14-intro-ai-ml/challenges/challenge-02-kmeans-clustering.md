# Challenge 2 — Customer Segmentation With k-means

> **Topic:** Unsupervised clustering, the elbow method, and reading cluster profiles
> **Lecture:** [03 — Pipelines, Evaluation, and Ethics](../lecture-notes/03-pipelines-evaluation-and-ethics.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** every model so far had a right answer to learn — a price, a species, survival. This one has none. You have customers and no labels, and the job is to let the data tell you what groups exist. It is your first taste of *unsupervised* learning, and it changes how you evaluate: with no ground truth, "how accurate?" is not even a question you can ask.

## The Brief

You work for a small online shop. Marketing wants to know whether the customers
fall into natural **segments** — groups that behave alike — so they can send each
group a different campaign instead of blasting everyone the same email. Nobody
has labelled the customers. There is no "correct" segment written down anywhere.
That is what makes this unsupervised.

You will use **k-means**, which is the simplest clustering idea there is. Picture
dropping four pins on a map, assigning every customer to their nearest pin, then
sliding each pin to the middle of its crowd, and repeating until the pins stop
moving. Those final pins are the cluster centres, and each customer belongs to
the nearest one. The only hard decision is *how many pins* — how many segments
exist — and for that you use the **elbow method**: try many values of k, measure
how tight the clusters are at each, and look for the point where adding another
cluster stops helping much.

Each customer here has three numbers, the classic marketing "RFM" set:
**annual_spend** (money), **purchase_freq** (how often they order), and
**recency_days** (days since their last order — smaller is fresher). The data is
generated with `make_blobs` so it runs offline; every seed is pinned.

## Starter

Copy this into `challenge-02-kmeans-clustering.py`. The data generator is given;
you fill in the elbow loop and the profiling.

```python
"""challenge-02-kmeans-clustering.py — segment customers, choose k by the elbow."""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")  # silence a Windows KMeans warning

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.datasets import make_blobs  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

RANDOM_STATE = 42
FEATURES = ["annual_spend", "purchase_freq", "recency_days"]


def make_customer_data(seed: int = RANDOM_STATE) -> pd.DataFrame:
    """Four hidden segments of customers, three RFM features each."""
    points, _ = make_blobs(
        n_samples=400, centers=4, cluster_std=0.55, n_features=3,
        center_box=(-6.0, 6.0), random_state=seed,
    )

    def to_units(column, low, high):
        return low + (column - column.min()) * (high - low) / (column.max() - column.min())

    return pd.DataFrame({
        "annual_spend": to_units(points[:, 0], 150.0, 5200.0).round(0),
        "purchase_freq": to_units(points[:, 1], 2.0, 40.0).round(0),
        "recency_days": to_units(points[:, 2], 3.0, 350.0).round(0),
    })


def main() -> None:
    df = make_customer_data()
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df.values)

    # TODO: for k in 1..7, fit KMeans(n_clusters=k, random_state=42, n_init=10)
    # and print k and model.inertia_. Look for the bend.

    # TODO: fit the final KMeans at your chosen k, attach labels to df, and print
    # each cluster's size and the mean of each feature (its profile).


if __name__ == "__main__":
    main()
```

## Requirements

1. **Scale first.** k-means measures straight-line distance, so a feature that
   runs to thousands would drown one that runs to tens. Put every feature on the
   same footing with `StandardScaler` before clustering.
2. **Find k with the elbow.** Fit `KMeans` for k from 1 to 7, record each
   model's `inertia_` (the total spread inside its clusters), and print them.
   The elbow is where the drops suddenly go small.
3. **Fit the final model** at your chosen k with `random_state=42` and
   `n_init=10`, and label every customer.
4. **Report cluster sizes**, so you can see whether the split is balanced or one
   cluster swallowed everyone.
5. **Profile each cluster** — the mean of each feature per cluster — and be ready
   to describe each segment in one sentence.

## Constraints

- **`random_state=42` and `n_init=10` on every `KMeans`.** k-means starts from
  random pin positions and can land in a different arrangement each run.
  `n_init=10` runs it ten times and keeps the tightest result; the seed makes
  those ten identical on every machine. Skip either and your inertias — and your
  elbow — wobble from run to run.
- **Scale, then cluster, in that order.** With features on their raw scales,
  `annual_spend` alone would decide every cluster and the other two would be
  noise. Standardising is not optional here; it is the difference between
  clustering on behaviour and clustering on dollars.
- **Do not read meaning into the cluster *numbers*.** Cluster 0 in your run might
  be cluster 2 in mine. The label is arbitrary; the *profile* — the means — is
  what identifies a segment. Describe segments by their numbers, never by their
  id.

## Expected output

The whole run is deterministic because every seed is pinned. The inertia falls
off a cliff through k=4 and then flattens — that cliff-then-flat shape is the
elbow, and it points at four segments, which is exactly how many were built in.

```text
$ python challenge-02-kmeans-clustering-solution.py
customers: 400   features: ['annual_spend', 'purchase_freq', 'recency_days']
--- elbow: inertia at each k (look for the bend) ---
  k=1  inertia=   1200.0
  k=2  inertia=    502.2  (drop    697.8)
  k=3  inertia=    115.2  (drop    387.0)
  k=4  inertia=     27.3  (drop     87.8)
  k=5  inertia=     24.8  (drop      2.6)
  k=6  inertia=     22.3  (drop      2.5)
  k=7  inertia=     20.2  (drop      2.1)
--- chosen k = 4 ---
cluster sizes:
  cluster 0: 100
  cluster 1: 100
  cluster 2: 100
  cluster 3: 100
cluster profiles (mean of each feature, original units):
  cluster 0: annual_spend= 3980.7  purchase_freq= 10.8  recency_days=  39.0
  cluster 1: annual_spend=  870.3  purchase_freq= 34.1  recency_days= 190.9
  cluster 2: annual_spend= 4637.4  purchase_freq=  6.5  recency_days= 313.8
  cluster 3: annual_spend= 2699.3  purchase_freq= 36.9  recency_days= 230.2
```

Read the drops, not the inertias. Going from one cluster to two saves 698; two to
three saves 387; three to four still saves 88. Then four to five saves **2.6** —
the bottom has dropped out. That collapse is the elbow: past four, you are
splitting groups that were already tight, buying almost nothing. Then read the
profiles as segments: cluster 0 spends big and bought recently (a loyal
high-value customer); cluster 2 spent the most of all but has not been seen in
314 days (a high-value customer who has lapsed — the one marketing should chase
first).

## Steps

1. Paste the starter and run it. `make_customer_data` and the scaler work; the
   two `TODO`s are yours.
2. Write the elbow loop. Print k and `inertia_` for k in 1..7. Eyeball where the
   drops stop being big.
3. Pick your k from the elbow and fit the final model. Attach the labels with
   `df["cluster"] = kmeans.fit_predict(x_scaled)`.
4. Print cluster sizes. If one cluster has almost everyone, your k is probably
   too small or you forgot to scale.
5. Print each cluster's feature means and write a one-line name for each segment.
6. Change `chosen_k` to 6 and look at the profiles again — you will see the four
   real groups plus two that are just shavings off the others.

## The Solution

```python
"""challenge-02-kmeans-clustering.py — segment customers with k-means, choose k by the elbow.

An unsupervised problem: no labels, just customer behaviour, and the question
"do these people fall into natural groups?". The three features are the classic
RFM set marketing teams actually use — Recency (days since last order), Frequency
(orders per year) and Monetary (annual spend) — which are genuinely independent,
so nothing here is a stand-in for anything else.

The data is generated with make_blobs so it runs offline, and every seed is
pinned so the run is identical on every machine. The real version of this task
ends in a scatter plot; a plot has no place in a headless, text-compared run, so
this prints the two things the plot would show: the inertia at each k (the elbow,
as a table) and the mean profile of each final cluster.

Run it with::

    python challenge-02-kmeans-clustering-solution.py
"""

from __future__ import annotations

import os

# k-means on Windows + MKL can print a memory-leak warning; one thread silences
# it without changing any result. Set before scikit-learn imports its backend.
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.datasets import make_blobs  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

RANDOM_STATE = 42
FEATURES = ["annual_spend", "purchase_freq", "recency_days"]


def make_customer_data(seed: int = RANDOM_STATE) -> pd.DataFrame:
    """Four hidden segments of customers, three RFM features each.

    The blobs are generated well-separated in an abstract space, then each column
    is stretched into a plausible business range — dollars, orders per year, days
    since last order. Real customer features sit on wildly different scales like
    this, which is exactly why k-means needs the StandardScaler step below.
    """
    points, _ = make_blobs(
        n_samples=400,
        centers=4,
        cluster_std=0.55,
        n_features=3,
        center_box=(-6.0, 6.0),
        random_state=seed,
    )

    def to_units(column: np.ndarray, low: float, high: float) -> np.ndarray:
        """Stretch one column onto [low, high] — affine, so the clusters survive."""
        return low + (column - column.min()) * (high - low) / (column.max() - column.min())

    return pd.DataFrame(
        {
            "annual_spend": to_units(points[:, 0], 150.0, 5200.0).round(0),
            "purchase_freq": to_units(points[:, 1], 2.0, 40.0).round(0),
            "recency_days": to_units(points[:, 2], 3.0, 350.0).round(0),
        }
    )


def inertia_by_k(x_scaled: np.ndarray, k_values: range) -> dict[int, float]:
    """Fit k-means for each k and record its inertia (within-cluster spread)."""
    inertias: dict[int, float] = {}
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        model.fit(x_scaled)
        inertias[k] = float(model.inertia_)
    return inertias


def main() -> None:
    """Scale, find the elbow, cluster at the chosen k, and profile the segments."""
    df = make_customer_data()
    print(f"customers: {len(df)}   features: {list(df.columns)}")

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df.values)

    print("--- elbow: inertia at each k (look for the bend) ---")
    inertias = inertia_by_k(x_scaled, range(1, 8))
    previous = None
    for k, inertia in inertias.items():
        drop = "" if previous is None else f"  (drop {previous - inertia:8.1f})"
        print(f"  k={k}  inertia={inertia:9.1f}{drop}")
        previous = inertia

    chosen_k = 4  # the drops collapse after k=4, and we built four blobs
    print(f"--- chosen k = {chosen_k} ---")
    kmeans = KMeans(n_clusters=chosen_k, random_state=RANDOM_STATE, n_init=10)
    df["cluster"] = kmeans.fit_predict(x_scaled)

    print("cluster sizes:")
    for cluster, size in df["cluster"].value_counts().sort_index().items():
        print(f"  cluster {cluster}: {size}")

    print("cluster profiles (mean of each feature, original units):")
    profile = df.groupby("cluster")[FEATURES].mean()
    for cluster, row in profile.iterrows():
        print(
            f"  cluster {cluster}: "
            f"annual_spend={row['annual_spend']:7.1f}  "
            f"purchase_freq={row['purchase_freq']:5.1f}  "
            f"recency_days={row['recency_days']:6.1f}"
        )


if __name__ == "__main__":
    main()
```

**Scaling is the load-bearing line, and it is easy to skip.** `annual_spend`
runs to thousands, `purchase_freq` to tens. k-means adds up squared differences
across the features, so before scaling a $500 gap and a 5-order gap are not
remotely comparable — the money term is a million times bigger and it decides
every cluster on its own. `StandardScaler` re-expresses each feature in standard
deviations, so "unusually high spend" and "unusually frequent" count the same.
The synthetic data deliberately stretches the three columns onto very different
ranges precisely so this step has something to do.

**Inertia only ever falls, which is why you read the *drops*.** Inertia is the
total squared distance from each point to its cluster's centre. Add a cluster and
that number can only go down — with `k` equal to the number of points it hits
zero, every point its own cluster. So a low inertia is not "good"; the signal is
the *shape* of the fall. Here it plunges 698, 387, 88 and then flatlines at 2.6.
The knee in that curve is the elbow, and it is the honest answer to "how many
segments", precisely because it stops rewarding you for splitting hairs.

**`n_init=10` is not decoration.** k-means is sensitive to where its centres
start; a bad start lands in a bad arrangement (a *local* minimum). Running it ten
times from ten starts and keeping the tightest is how scikit-learn dodges that,
and `random_state` makes the ten starts reproducible. Drop `n_init` and two runs
can disagree about the clusters entirely.

**The profile is the deliverable, not the labels.** k-means hands back cluster
*numbers*, and those numbers are meaningless — nothing says cluster 0 is
"better" than cluster 2. The means are what turn a number into a segment you can
name and act on: cluster 2 here is "spent the most, gone quiet for ten months",
which is a specific person to write a specific email to. That translation from
number to profile to action is the entire point of the exercise.

## Download and run

Download
[challenge-02-kmeans-clustering-solution.py](./challenge-02-kmeans-clustering-solution.py)
and run it:

```bash
python challenge-02-kmeans-clustering-solution.py
```

It needs only `scikit-learn`, `pandas`, and `numpy`. The 400 customers are
generated from a fixed seed inside the file, so there is nothing to download and
the elbow and the profiles are identical on every machine. The `-solution`
suffix keeps it clear of your own `challenge-02-kmeans-clustering.py`.

## Common bugs to catch

- **One cluster holds almost everyone.** You clustered the raw frame without
  scaling, so `annual_spend` dominated the distance and the other two features
  vanished. Fit `StandardScaler` first and cluster the scaled array.
- **The inertias — and the elbow — change every run.** A seed is missing on a
  `KMeans`, or you dropped `n_init`. Pin `random_state=42` and set `n_init=10` on
  every fit, the ones in the loop included.
- **`ValueError: n_samples=... should be >= n_clusters=...`** You put a k larger
  than the number of customers into the loop. Keep the range sensible (1..7 or
  so) and well below `len(df)`.
- **You read the cluster numbers as a ranking.** Cluster 0 is not "first" or
  "best"; the numbers are assigned arbitrarily and can differ between runs even
  with a fixed seed if you change anything upstream. Always describe a segment by
  its profile.
- **`UserWarning` about a memory leak on Windows.** Harmless, and the
  `OMP_NUM_THREADS=1` line at the top of the file silences it. It never changes a
  result — it is a threading note, not a modelling one.

## Under the hood

<details>
<summary>Under the hood — why the elbow is a judgement call, not a formula</summary>

The elbow method has a dirty secret: there is no equation that returns "the
elbow". You are eyeballing a curve for a bend, and on real data the bend is often
a gentle graceful curve with no obvious corner at all. This synthetic set has a
sharp elbow because it was built from four clean, well-separated blobs; genuine
customer data rarely obliges.

That is why practitioners bring a second opinion. The **silhouette score**
measures, for each point, how much closer it is to its own cluster than to the
nearest other cluster, and averages that over everyone — a number from -1 to 1
where higher is better. Unlike inertia it does not always improve with more
clusters, so it can actually *peak* at the right k rather than just flatten. Run
it alongside the elbow and the two usually agree; when they disagree, you have
learned that your clusters are not as clean as you hoped, which is itself worth
knowing.

And there is a deeper limit. k-means assumes clusters are roughly round and
similar in size, because it assigns points by straight-line distance to a centre.
Give it two long crescents interleaved, or one tiny dense group beside one huge
sparse one, and it will carve them wrongly no matter what k you pick — not
because your code is broken, but because the tool's assumption does not fit the
data. That is when you reach for a density-based method like `DBSCAN`, which
grows clusters from crowded regions and does not need k chosen in advance. The
elbow tells you how many round blobs there are; it cannot tell you that round
blobs were the wrong model.

</details>

## Acceptance checklist

- [ ] Features are standardised before clustering.
- [ ] Inertia is printed for k from 1 to 7, and you can point at the elbow.
- [ ] The final model uses `random_state=42` and `n_init=10`.
- [ ] Cluster sizes print, and the split is balanced (roughly 100 each here).
- [ ] Each cluster's feature means print, and you named each segment in a
      sentence.
- [ ] Two runs produce identical inertias and profiles.
- [ ] Committed with a message like `Add Week 14 challenge 2: k-means segmentation`.

## Stretch

- **Silhouette alongside inertia.** Compute `silhouette_score(x_scaled, labels)`
  for each k from 2 to 7 and print it next to the inertia. Where does it peak?
  Does it agree with the elbow?
- **DBSCAN.** Cluster the same scaled data with `DBSCAN(eps=0.5)`. It picks the
  number of clusters itself and marks outliers as `-1`. How does its answer
  compare, and what does it do that k-means cannot?
- **A campaign per segment.** Write one sentence of marketing per cluster — who
  they are and one thing you would send them. The lapsed high-spender (cluster 2)
  and the loyal recent one (cluster 0) should get very different emails.
- **"We want five segments."** Suppose marketing insists on five. Refit at k=5,
  look at the new profiles, and write a short answer: the elbow says four, but k
  is a business decision as much as a statistical one — what would you tell them?

That is the week's challenge set. The graded practice is in
[the homework](../homework/README.md), and the week caps off with
[the mini-project](../mini-project/README.md).
