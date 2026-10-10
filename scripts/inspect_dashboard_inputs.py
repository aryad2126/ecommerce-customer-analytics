from pathlib import Path
import pandas as pd

BASE = Path.cwd()
DATA = BASE / "data" / "processed"

folders = [
    DATA / "cleaned" / "orders",
    DATA / "cleaned" / "order_purchase_summary",
    DATA / "marts" / "customer_purchase",
    DATA / "segmentation" / "rfm",
]

for folder in folders:
    files = sorted(folder.glob("part-*.csv"))
    print(f"\n{'=' * 65}")
    print(f"DATASET: {folder.name}")
    print(f"Part files: {len(files)}")

    if not files:
        print("No part files found.")
        continue

    frames = [pd.read_csv(file, nrows=5) for file in files]
    print("Columns:", list(frames[0].columns))

# Small outputs that are already ordinary CSV files
for filename in [
    DATA / "segmentation" / "kmeans" / "cluster_summary.csv",
    DATA / "segmentation" / "kmeans" / "customer_segments.csv",
]:
    print(f"\n{'=' * 65}")
    print(f"FILE: {filename.name}")
    if filename.exists():
        df = pd.read_csv(filename, nrows=5)
        print("Columns:", list(df.columns))
        print(df.to_string(index=False))
    else:
        print("File not found.")

print("\nInspection complete.")
