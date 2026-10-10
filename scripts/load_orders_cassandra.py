from pathlib import Path
from datetime import datetime
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType, ConsistencyLevel

BASE = Path.cwd()
RAW = BASE / "data" / "raw" / "olist"
CLEANED = BASE / "data" / "processed" / "cleaned"

KEYSPACE = "ecommerce_analytics"
TABLE = "customer_order_history"
BATCH_SIZE = 50


def read_spark_csv(folder):
    files = list(folder.glob("part-*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV part files found in {folder}")

    return pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )


def parse_timestamp(value):
    if value is None or pd.isna(value) or str(value).strip() == "":
        return None

    timestamp = pd.to_datetime(value, errors="coerce", utc=True)

    if pd.isna(timestamp):
        return None

    # Cassandra driver's timestamp values should be timezone-aware or UTC.
    return timestamp.to_pydatetime()


def clean_text(value):
    if value is None or pd.isna(value):
        return None
    return str(value)


print("Reading processed orders...")
orders = read_spark_csv(CLEANED / "orders")

print("Reading customer identities...")
customers = pd.read_csv(
    RAW / "olist_customers_dataset.csv",
    usecols=["customer_id", "customer_unique_id"]
)

print("Reading item totals...")
items = read_spark_csv(CLEANED / "order_item_summary")[
    ["order_id", "item_total"]
]

print("Reading payment totals...")
payments = read_spark_csv(CLEANED / "order_payment_summary")[
    ["order_id", "payment_total"]
]

# Keep the joins one-to-one at the order level.
if customers["customer_id"].duplicated().any():
    raise ValueError("Duplicate customer_id values found.")

if items["order_id"].duplicated().any():
    raise ValueError("Duplicate order_id values in item summary.")

if payments["order_id"].duplicated().any():
    raise ValueError("Duplicate order_id values in payment summary.")

orders = orders.merge(
    customers, on="customer_id", how="left", validate="many_to_one"
)
orders = orders.merge(
    items, on="order_id", how="left", validate="one_to_one"
)
orders = orders.merge(
    payments, on="order_id", how="left", validate="one_to_one"
)

print("\nJoined order rows:", len(orders))
print("Unique order IDs:", orders["order_id"].nunique())

# Cassandra partition key and first clustering key cannot be null.
valid_key = (
    orders["customer_unique_id"].notna()
    & orders["order_purchase_timestamp"].notna()
)
skipped = int((~valid_key).sum())
valid_orders = orders.loc[valid_key].copy()

print("Rows skipped for missing customer ID or purchase timestamp:", skipped)
print("Rows eligible for Cassandra:", len(valid_orders))

cluster = Cluster(["127.0.0.1"], port=9042)
session = None

try:
    session = cluster.connect(KEYSPACE)

    insert = session.prepare("""
        INSERT INTO customer_order_history (
            customer_unique_id,
            order_purchase_timestamp,
            order_id,
            order_status,
            customer_state,
            item_total,
            payment_total,
            order_approved_at,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    insert.consistency_level = ConsistencyLevel.ONE

    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    attempted = 0
    batches_sent = 0

    for row in valid_orders.to_dict(orient="records"):
        purchase_timestamp = parse_timestamp(
            row["order_purchase_timestamp"]
        )

        if purchase_timestamp is None:
            skipped += 1
            continue

        values = (
            str(row["customer_unique_id"]),
            purchase_timestamp,
            str(row["order_id"]),
            clean_text(row.get("order_status")),
            clean_text(row.get("customer_state")),
            None if pd.isna(row.get("item_total")) else float(row["item_total"]),
            None if pd.isna(row.get("payment_total")) else float(row["payment_total"]),
            parse_timestamp(row.get("order_approved_at")),
            parse_timestamp(row.get("order_delivered_carrier_date")),
            parse_timestamp(row.get("order_delivered_customer_date")),
            parse_timestamp(row.get("order_estimated_delivery_date"))
        )

        batch.add(insert, values)
        attempted += 1

        if len(batch) >= BATCH_SIZE:
            session.execute(batch)
            batches_sent += 1
            batch = BatchStatement(batch_type=BatchType.UNLOGGED)

    if len(batch):
        session.execute(batch)
        batches_sent += 1

    print("\nCassandra import completed.")
    print("Rows attempted:", attempted)
    print("Rows skipped:", skipped)
    print("Batches sent:", batches_sent)
    print("Keyspace:", KEYSPACE)
    print("Table:", TABLE)

finally:
    if session is not None:
        session.shutdown()
    cluster.shutdown()
