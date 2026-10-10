from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BASE_DIR = Path.cwd()
INPUT_FILE = BASE_DIR / "data" / "raw" / "olist" / "olist_orders_dataset.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "cleaned" / "orders"

spark = (
    SparkSession.builder
    .appName("OlistOrdersPreprocessing")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

try:
    print("\nReading orders dataset with PySpark...")
    orders = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    print("\nOriginal row count:", orders.count())
    print("Original schema:")
    orders.printSchema()

    timestamp_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in timestamp_columns:
        orders = orders.withColumn(
            column,
            F.to_timestamp(F.col(column))
        )

    print("\nOrder status counts:")
    (
        orders.groupBy("order_status")
        .count()
        .orderBy(F.desc("count"))
        .show(truncate=False)
    )

    print("\nMissing values by column:")
    missing_expressions = [
        F.sum(
            F.when(F.col(column).isNull(), 1).otherwise(0)
        ).alias(column)
        for column in orders.columns
    ]

    orders.select(*missing_expressions).show(truncate=False)

    print("\nSample of processed orders:")
    orders.select(
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ).show(5, truncate=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    (
        orders.write
        .mode("overwrite")
        .option("header", True)
        .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
        .csv(str(OUTPUT_DIR))
    )

    print("\nProcessed orders saved to:", OUTPUT_DIR)
    print("Output is a folder containing Spark CSV part files.")

finally:
    spark.stop()
