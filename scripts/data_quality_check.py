import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw/olist")

print("OLIST DATA QUALITY SUMMARY")
print("=" * 65)

for file in sorted(DATA_DIR.glob("*.csv")):
    df = pd.read_csv(file)

    print(f"\nFILE: {file.name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Exact duplicate rows: {df.duplicated().sum():,}")

    # Check duplicates in common identifier columns.
    for column in ["order_id", "customer_id", "customer_unique_id",
                   "product_id", "seller_id", "review_id"]:
        if column in df.columns:
            print(
                f"Duplicate values in {column}: "
                f"{df[column].duplicated().sum():,}"
            )

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("Missing values: None")
    else:
        print("Missing values:")
        print(missing.to_string())

print("\nInspection completed.")
