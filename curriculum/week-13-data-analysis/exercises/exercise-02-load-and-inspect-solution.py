# --- Cell 1 — imports ---
"""exercise-02-load-and-inspect.py — first look at a twelve-branch table."""

import pandas as pd


# --- Cell 2 — the data ---
BRANCHES: dict[str, list] = {
    "branch": [
        "Alder", "Birch", "Cedar", "Dogwood", "Elm", "Fir",
        "Ginkgo", "Hawthorn", "Ironwood", "Juniper", "Katsura", "Linden",
    ],
    "region": [
        "North", "South", "North", "East", "South", "North",
        "West", "South", "North", "East", "South", "North",
    ],
    "visits":       [4820, 3110, 5640, 2980, 6150, 3720,
                     4410, 5230, 2760, 6890, 3980, 5010],
    "holds_filled": [612, 488, 903, 377, 1044, 521,
                     688, 815, 342, 1176, 559, 742],
    "open_hours":   [48, 40, 56, 32, 56, 40, 48, 56, 32, 60, 40, 48],
}

df = pd.DataFrame(BRANCHES)


# --- Cell 3 — the first five rows ---
print("--- head ---")
print(df.head())


# --- Cell 4 — size and column types ---
print("--- shape ---")
print(df.shape)
print("--- dtypes ---")
print(df.dtypes)


# --- Cell 5 — the full structural summary ---
print("--- info ---")
df.info()


# --- Cell 6 — summary statistics ---
print("--- describe ---")
print(df.describe().round(2))


# --- Cell 7 — how many branches per region ---
print("--- value_counts ---")
print(df["region"].value_counts())


# --- Cell 8 — the last three rows ---
print("--- tail(3) ---")
print(df.tail(3))


# --- Cell 9 — one derived column ---
print("--- derived ---")
df["visits_per_hour"] = (df["visits"] / df["open_hours"]).round(1)
print(df[["branch", "region", "visits_per_hour"]].head())
