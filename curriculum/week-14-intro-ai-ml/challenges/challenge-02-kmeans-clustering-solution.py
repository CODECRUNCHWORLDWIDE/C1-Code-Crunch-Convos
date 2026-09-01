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
