from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BASE = Path.cwd()
RAW = BASE / "data" / "raw" / "olist"
CLEANED = BASE / "data" / "processed" / "cleaned"
OUTPUT = BASE / "data" / "processed" / "segmentation" / "rfm"

spark = (
    SparkSession.builder
    .appName("OlistRFMAnalysis")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

try:
    orders = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(CLEANED / "orders"))
        .withColumn(
            "order_purchase_timestamp",
            F.to_timestamp("order_purchase_timestamp")
        )
    )

    customers = (
        spark.read.option("header", True)
        .csv(str(RAW / "olist_customers_dataset.csv"))
        .select("customer_id", "customer_unique_id")
    )

    items = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(CLEANED / "order_item_summary"))
        .select("order_id", "item_total")
    )

    # RFM is based only on completed/delivered orders.
    delivered = (
        orders.filter(F.col("order_status") == "delivered")
        .join(customers, "customer_id", "inner")
        .join(items, "order_id", "left")
    )

    reference_date = (
        delivered.select(
            F.date_add(
                F.to_date(F.max("order_purchase_timestamp")), 1
            ).alias("reference_date")
        ).first()["reference_date"]
    )

    print("RFM reference date:", reference_date)
    print("Delivered orders:", delivered.select("order_id").distinct().count())

    rfm = (
        delivered.groupBy("customer_unique_id")
        .agg(
            F.datediff(
                F.lit(reference_date),
                F.to_date(F.max("order_purchase_timestamp"))
            ).alias("recency_days"),
            F.countDistinct("order_id").alias("frequency"),
            F.sum(F.coalesce(F.col("item_total"), F.lit(0.0)))
            .alias("monetary"),
        )
    )

    # Validate values before saving.
    print("\nRFM customer count:", rfm.count())
    print("Rows with invalid RFM values:",
          rfm.filter(
              F.col("recency_days").isNull()
              | (F.col("recency_days") < 0)
              | (F.col("frequency") < 1)
              | F.col("monetary").isNull()
              | (F.col("monetary") < 0)
          ).count())

    print("\nRFM summary statistics:")
    rfm.select("recency_days", "frequency", "monetary").summary(
        "count", "mean", "stddev", "min", "25%", "50%", "75%", "max"
    ).show(truncate=False)

    print("\nCustomers with the highest frequency:")
    rfm.orderBy(
        F.desc("frequency"), F.desc("monetary")
    ).show(10, truncate=False)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    (
        rfm.write
        .mode("overwrite")
        .option("header", True)
        .csv(str(OUTPUT))
    )

    print("\nRFM data saved to:", OUTPUT)

finally:
    spark.stop()
