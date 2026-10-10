from pathlib import Path
import pandas as pd

folder = (
    Path.cwd()
    / "data"
    / "processed"
    / "segmentation"
    / "kmeans"
)

segments = pd.read_csv(folder / "customer_segments.csv")
summary = pd.read_csv(folder / "cluster_summary.csv")

print("Customer segment rows:", len(segments))
print("Unique customer IDs:", segments["customer_unique_id"].nunique())
print("Missing values:")
print(segments.isnull().sum().to_string())

print("\nCluster counts:")
print(segments["cluster"].value_counts().sort_index().to_string())

print("\nCluster summary file:")
print(summary.to_string(index=False))

valid = (
    len(segments) == 93358
    and segments["customer_unique_id"].nunique() == 93358
    and segments["cluster"].notna().all()
    and segments["cluster"].isin(summary["cluster"]).all()
)

print("\nPASS: Segmentation output verified." if valid
      else "\nCHECK: Segmentation output needs investigation.")
