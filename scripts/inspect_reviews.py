import pandas as pd
from pathlib import Path

file = Path("data/raw/olist/olist_order_reviews_dataset.csv")
df = pd.read_csv(file)

print("REVIEW DATASET INVESTIGATION")
print("=" * 55)

print("\nTotal rows:", len(df))
print("Unique review IDs:", df["review_id"].nunique())
print("Unique order IDs:", df["order_id"].nunique())

print("\nRows with repeated review IDs:")
repeated_review_ids = df[df.duplicated("review_id", keep=False)]
print("Count:", len(repeated_review_ids))
print(repeated_review_ids.sort_values("review_id").head(12).to_string(index=False))

print("\nRows with repeated order IDs:")
repeated_order_ids = df[df.duplicated("order_id", keep=False)]
print("Count:", len(repeated_order_ids))
print(repeated_order_ids.sort_values("order_id").head(12).to_string(index=False))

print("\nReview score distribution:")
print(df["review_score"].value_counts(dropna=False).sort_index())

print("\nInvestigation completed.")
