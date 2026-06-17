# Challenge 02 — Customer segmentation with k-means

## The problem

You work for a small e-commerce shop. Marketing wants to understand whether customers naturally fall into distinct *segments* — groups that behave similarly — so that they can tailor campaigns. You have no labels. This is an unsupervised problem.

You will use **k-means** to find clusters in customer data and **inertia (the elbow method)** to choose how many clusters to use.

## Generate the data

We will use scikit-learn's `make_blobs` to produce synthetic customer data so you can run this offline. Three features per customer:

- `annual_spend` — total spend in the last year (dollars).
- `purchase_freq` — number of purchases in the last year.
- `avg_basket` — average order value (dollars).

```python
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs


def make_customer_data(random_state: int = 42) -> pd.DataFrame:
    centers = [
        (200, 3, 60),     # bargain hunters: low spend, few orders, small basket
        (1500, 20, 75),   # regulars: medium spend, many orders, normal basket
        (4000, 8, 500),   # whales: high spend, few orders, huge basket
        (700, 12, 60),    # casuals: moderate spend, several orders
    ]
    X, _ = make_blobs(
        n_samples=400,
        centers=centers,
        cluster_std=[60, 200, 600, 100],
        random_state=random_state,
    )
    df = pd.DataFrame(X, columns=["annual_spend", "purchase_freq", "avg_basket"])
    # Avoid negative values for plausibility.
    df = df.clip(lower=0)
    return df
```

## Requirements

1. **Generate the data** with the function above. Inspect it (`df.describe()`, scatter plots).
2. **Scale the features.** k-means uses Euclidean distance, so features must be on comparable scales. Use `StandardScaler`.
3. **Pick K with the elbow method.** Train `KMeans(n_clusters=k)` for k from 1 to 10. For each, record `model.inertia_`. Plot inertia vs k. Find the "elbow" — the point of diminishing returns. You should see it somewhere around k=4 (because we built four blobs).
4. **Fit the final model** at your chosen K and assign each customer a cluster label.
5. **Profile each cluster.** Group by cluster label, compute mean of each feature, and write a one-sentence description per cluster (e.g., "Cluster 2: low spend, small basket, infrequent — bargain hunters").
6. **Visualise.** Make a 2D scatter (e.g., `annual_spend` vs `avg_basket`), colour by cluster.

## Skeleton

```python
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def elbow_plot(X_scaled: np.ndarray) -> None:
    inertias = []
    ks = range(1, 11)
    for k in ks:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X_scaled)
        inertias.append(model.inertia_)

    plt.figure()
    plt.plot(list(ks), inertias, marker="o")
    plt.xlabel("k (number of clusters)")
    plt.ylabel("inertia (within-cluster sum of squares)")
    plt.title("Elbow method")
    plt.grid(True)
    plt.show()


def main() -> None:
    df = make_customer_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df.values)

    elbow_plot(X_scaled)  # Look at the chart, then choose K.

    chosen_k = 4  # adjust based on what your elbow plot shows
    kmeans = KMeans(n_clusters=chosen_k, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    # Profile each cluster.
    profile = df.groupby("cluster").mean(numeric_only=True)
    print("Cluster profiles (means):")
    print(profile)

    # Quick visualisation in two of the three feature dimensions.
    plt.figure()
    for c in sorted(df["cluster"].unique()):
        sub = df[df["cluster"] == c]
        plt.scatter(sub["annual_spend"], sub["avg_basket"], label=f"cluster {c}", alpha=0.6)
    plt.xlabel("annual_spend")
    plt.ylabel("avg_basket")
    plt.legend()
    plt.title(f"k-means with k={chosen_k}")
    plt.show()


if __name__ == "__main__":
    main()
```

## What to look out for

- **k-means assumes spherical, similar-sized clusters in the scaled feature space.** Real customer data rarely satisfies this perfectly. If the clusters look bad, the assumption may be the problem, not your code.
- **k-means is non-deterministic.** Different initialisations can produce different clusters. Setting `random_state` and `n_init=10` (run the algorithm 10 times and keep the best) helps.
- **Cluster labels are arbitrary.** Cluster 2 in one run might be cluster 0 in the next. Don't rely on the label number — rely on the profile means.

## Stretch goals

- Try `DBSCAN` (a density-based clustering algorithm) on the same data. It does not require you to choose K up front. How do its clusters compare?
- Compute the silhouette score (`from sklearn.metrics import silhouette_score`) for each K. Plot it alongside inertia. Compare the recommendations of the two metrics.
- Write a short markdown blurb you could send to marketing summarising the segments and one campaign idea per segment.

## Reflection

After you finish, answer:

1. Did the elbow you saw match the four-segment design of the data? If not, why might that be?
2. If marketing told you "we want five segments", how would you respond? (Hint: K is not always best chosen by the elbow.)
3. What kinds of business questions would clustering NOT be the right tool for?
