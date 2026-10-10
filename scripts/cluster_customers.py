from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

BASE = Path.cwd()
INPUT = BASE / "data" / "processed" / "segmentation" / "rfm"
OUTPUT = BASE / "data" / "processed" / "segmentation" / "kmeans"

print("Reading RFM data...")

parts = list(INPUT.glob("part-*.csv"))
if not parts:
    raise FileNotFoundError(f"No Spark CSV part files found in {INPUT}")

rfm = pd.concat(
    [pd.read_csv(file) for file in parts],
    ignore_index=True
)

rfm = rfm.dropna(
    subset=["customer_unique_id", "recency_days", "frequency", "monetary"]
).copy()

print("Customers loaded:", len(rfm))

# Transform skewed variables before clustering.
rfm["log_frequency"] = __import__("numpy").log1p(rfm["frequency"])
rfm["log_monetary"] = __import__("numpy").log1p(rfm["monetary"])

features = rfm[
    ["recency_days", "log_frequency", "log_monetary"]
]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Compare cluster counts from 2 to 5 using a reproducible sample.
sample_size = min(5000, len(rfm))
sample = scaled_features[:sample_size]

print("\nComparing cluster counts...")
results = []

for k in range(2, 6):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    sample_labels = model.fit_predict(sample)
    score = silhouette_score(sample, sample_labels)

    results.append((k, score))
    print(f"k={k}, silhouette score={score:.4f}")

best_k = max(results, key=lambda item: item[1])[0]
print("\nSelected cluster count:", best_k)

# Fit the final model to all customers.
model = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)
rfm["cluster"] = model.fit_predict(scaled_features)

# Summarize each cluster using the original RFM values.
summary = (
    rfm.groupby("cluster")
    .agg(
        customer_count=("customer_unique_id", "count"),
        avg_recency_days=("recency_days", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        median_monetary=("monetary", "median")
    )
    .reset_index()
)

OUTPUT.mkdir(parents=True, exist_ok=True)

rfm[
    ["customer_unique_id", "recency_days", "frequency", "monetary", "cluster"]
].to_csv(OUTPUT / "customer_segments.csv", index=False)

summary.to_csv(OUTPUT / "cluster_summary.csv", index=False)

print("\nCluster summary:")
print(summary.round(2).to_string(index=False))

print("\nSaved customer segments to:", OUTPUT / "customer_segments.csv")
print("Saved cluster summary to:", OUTPUT / "cluster_summary.csv")
