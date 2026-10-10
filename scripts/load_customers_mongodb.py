from pathlib import Path
import math
import pandas as pd
from pymongo import MongoClient, UpdateOne

BASE = Path.cwd()
PROCESSED = BASE / "data" / "processed"
PURCHASE_FOLDER = PROCESSED / "marts" / "customer_purchase"
SEGMENT_FILE = (
    PROCESSED / "segmentation" / "kmeans" / "customer_segments.csv"
)

DATABASE_NAME = "ecommerce_analytics"
COLLECTION_NAME = "customers"
BATCH_SIZE = 1000


def load_spark_csv_folder(folder):
    files = list(folder.glob("part-*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV part files found in {folder}")

    return pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )


def clean_value(value):
    if value is None or pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float) and not math.isfinite(value):
        return None

    return value


print("Loading customer purchase analytics...")
purchase = load_spark_csv_folder(PURCHASE_FOLDER)

print("Loading customer segments...")
segments = pd.read_csv(SEGMENT_FILE)

# Each input should contain one record per customer.
if purchase["customer_unique_id"].duplicated().any():
    raise ValueError("Duplicate customer IDs in purchase analytics.")

if segments["customer_unique_id"].duplicated().any():
    raise ValueError("Duplicate customer IDs in segmentation data.")

# Attach segmentation where available; retain customers without an RFM row.
combined = purchase.merge(
    segments,
    on="customer_unique_id",
    how="left",
    validate="one_to_one",
    suffixes=("_purchase", "_rfm")
)

# Use the RFM frequency and monetary values as the segmentation metrics.
combined["segment_label"] = combined["cluster"].map({
    0: "Mostly one-time purchasers",
    1: "Repeat purchasers"
})

print("Customer documents to import:", len(combined))
print("Customers with RFM metrics:", combined["cluster"].notna().sum())
print("Customers without RFM metrics:", combined["cluster"].isna().sum())

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command("ping")
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    collection.create_index(
        "customer_unique_id",
        unique=True
    )
    collection.create_index("cluster")
    collection.create_index("customer_state")

    operations = []

    for row in combined.to_dict(orient="records"):
        document = {
            key: clean_value(value)
            for key, value in row.items()
        }

        customer_id = document["customer_unique_id"]

        operations.append(
            UpdateOne(
                {"customer_unique_id": customer_id},
                {"$set": document},
                upsert=True
            )
        )

        if len(operations) >= BATCH_SIZE:
            collection.bulk_write(operations, ordered=False)
            operations = []

    if operations:
        collection.bulk_write(operations, ordered=False)

    print("\nMongoDB import completed.")
    print("Database:", DATABASE_NAME)
    print("Collection:", COLLECTION_NAME)
    print("Documents in collection:", collection.count_documents({}))
    print("Unique customer IDs:", collection.distinct(
        "customer_unique_id"
    ).__len__())

    print("\nSample customer document:")
    sample = collection.find_one(
        {},
        {"_id": 0}
    )
    print(sample)

finally:
    client.close()
