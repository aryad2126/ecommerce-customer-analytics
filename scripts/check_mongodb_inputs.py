from pathlib import Path
import pandas as pd

base = Path.cwd() / "data" / "processed"

purchase_folder = base / "marts" / "customer_purchase"
segment_file = (
    base / "segmentation" / "kmeans" / "customer_segments.csv"
)

print("Customer purchase folder exists:", purchase_folder.exists())
print("Segmentation file exists:", segment_file.exists())

if not purchase_folder.exists():
    raise FileNotFoundError(purchase_folder)

if not segment_file.exists():
    raise FileNotFoundError(segment_file)

purchase_parts = list(purchase_folder.glob("part-*.csv"))

if not purchase_parts:
    raise FileNotFoundError(
        f"No Spark CSV part files found in {purchase_folder}"
    )

purchase = pd.concat(
    [pd.read_csv(file) for file in purchase_parts],
    ignore_index=True
)

segments = pd.read_csv(segment_file)

print("\nCustomer purchase rows:", len(purchase))
print("Segment rows:", len(segments))

print("\nCustomer purchase columns:")
print(purchase.columns.tolist())

print("\nSegment columns:")
print(segments.columns.tolist())

print("\nCustomer purchase sample:")
print(purchase.head(3).to_string(index=False))

print("\nSegment sample:")
print(segments.head(3).to_string(index=False))

print("\nUnique purchase customer IDs:",
      purchase["customer_unique_id"].nunique())
print("Unique segment customer IDs:",
      segments["customer_unique_id"].nunique())
print("Purchase rows without customer ID:",
      purchase["customer_unique_id"].isna().sum())
print("Segment rows without customer ID:",
      segments["customer_unique_id"].isna().sum())
