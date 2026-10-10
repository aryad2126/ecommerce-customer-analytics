from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BASE = Path.cwd()
RAW = BASE / "data" / "raw" / "olist"
CLEANED = BASE / "data" / "processed" / "cleaned"
OUTPUT = BASE / "data" / "processed" / "marts" / "customer_purchase"

spark = (
    SparkSession.builder
    .appName("OlistCustomerPurchaseAnalytics")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")


try:
    print("\nLoading orders...")
    orders = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(CLEANED / "orders"))
        .withColumn(
            "order_purchase_timestamp",
            F.to_timestamp("order_purchase_timestamp")
        )
    )

    print("Loading customers...")
    customers = (
        spark.read.option("header", True)
        .csv(str(RAW / "olist_customers_dataset.csv"))
        .select("customer_id", "customer_unique_id", "customer_city",
                "customer_state")
    )

    print("Loading order-level item and payment summaries...")
    items = spark.read.option("header", True).option(
        "inferSchema", True
    ).csv(str(CLEANED / "order_item_summary"))

    payments = spark.read.option("header", True).option(
        "inferSchema", True
    ).csv(str(CLEANED / "order_payment_summary"))

    # Join each order to its customer identity and the pre-aggregated
    # financial summaries. Each summary has at most one row per order.
    order_level = (
        orders
        .join(customers, "customer_id", "left")
        .join(items, "order_id", "left")
        .join(payments, "order_id", "left")
        .withColumn(
            "item_total",
            F.col("item_total").cast("double")
        )
        .withColumn(
            "payment_total",
            F.col("payment_total").cast("double")
        )
    )

    print("\nOrder-level joined rows:", order_level.count())
    print("Unique orders:", order_level.select("order_id").distinct().count())
    print("Rows missing customer identity:",
          order_level.filter(F.col("customer_unique_id").isNull()).count())

    # Recency will be calculated later using a clearly defined reference date.
    # This step builds frequency and spending metrics first.
    customer_metrics = (
        order_level
        .filter(F.col("customer_unique_id").isNotNull())
        .groupBy("customer_unique_id")
        .agg(
            F.countDistinct("order_id").alias("all_order_count"),
            F.countDistinct(
                F.when(
                    F.col("order_status") == "delivered",
                    F.col("order_id")
                )
            ).alias("delivered_order_count"),
            F.sum(
                F.when(
                    F.col("order_status") == "delivered",
                    F.coalesce(F.col("item_total"), F.lit(0.0))
                ).otherwise(F.lit(0.0))
            ).alias("delivered_item_spend"),
            F.sum(
                F.when(
                    F.col("order_status") == "delivered",
                    F.coalesce(F.col("payment_total"), F.lit(0.0))
                ).otherwise(F.lit(0.0))
            ).alias("delivered_payment_total"),
            F.max("order_purchase_timestamp").alias("last_order_timestamp"),
            F.first("customer_state", ignorenulls=True).alias("customer_state"),
            F.first("customer_city", ignorenulls=True).alias("customer_city"),
        )
        .withColumn(
            "is_repeat_customer",
            F.col("delivered_order_count") >= 2
        )
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)

    (
        customer_metrics.write
        .mode("overwrite")
        .option("header", True)
        .csv(str(OUTPUT))
    )

    print("\nCustomer metrics saved to:", OUTPUT)
    print("Unique customers:", customer_metrics.count())

    print("\nRepeat-customer summary:")
    customer_metrics.agg(
        F.count("*").alias("unique_customers"),
        F.sum(
            F.when(F.col("is_repeat_customer"), 1).otherwise(0)
        ).alias("repeat_customers"),
        F.avg("delivered_order_count").alias("avg_delivered_orders"),
        F.sum("delivered_item_spend").alias("delivered_item_spend_total"),
        F.sum("delivered_payment_total").alias("delivered_payment_total"),
    ).show(truncate=False)

    print("\nTop 10 customers by delivered item spend:")
    (
        customer_metrics
        .orderBy(F.desc("delivered_item_spend"))
        .select(
            "customer_unique_id",
            "delivered_order_count",
            "delivered_item_spend",
            "delivered_payment_total",
            "customer_state"
        )
        .show(10, truncate=False)
    )

finally:
    spark.stop()
