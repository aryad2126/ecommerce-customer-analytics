from pathlib import Path
from pyspark.sql import SparkSession

OUTPUT_DIR = Path("data/processed/cleaned/orders")

spark = (
    SparkSession.builder
    .appName("VerifyProcessedOrders")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    files = list(OUTPUT_DIR.glob("part-*.csv"))
    print("Spark CSV part files found:", len(files))

    if not files:
        raise FileNotFoundError(
            f"No Spark CSV part files found in {OUTPUT_DIR}"
        )

    saved_orders = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(OUTPUT_DIR))
    )

    row_count = saved_orders.count()
    print("Rows read from saved output:", row_count)
    print("Columns:", saved_orders.columns)

    if row_count == 99441:
        print("PASS: All 99,441 orders are present.")
    else:
        print("CHECK REQUIRED: Row count differs from expected.")

    print("\nSample from saved output:")
    saved_orders.select(
        "order_id",
        "order_status",
        "order_purchase_timestamp"
    ).show(5, truncate=False)

finally:
    spark.stop()
