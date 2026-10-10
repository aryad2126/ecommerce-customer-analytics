from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BASE = Path.cwd()
RAW = BASE / "data" / "raw" / "olist"
CLEANED = BASE / "data" / "processed" / "cleaned"

spark = (
    SparkSession.builder
    .appName("OlistItemsAndPayments")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")


def save_csv(df, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (
        df.write
        .mode("overwrite")
        .option("header", True)
        .csv(str(folder))
    )


try:
    print("\nReading order items...")
    items = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW / "olist_order_items_dataset.csv"))
    )

    print("Original item rows:", items.count())

    # Validate numeric fields and preserve individual item records.
    items = (
        items
        .withColumn("price", F.col("price").cast("double"))
        .withColumn("freight_value", F.col("freight_value").cast("double"))
    )

    print("\nItem records with missing order IDs:",
          items.filter(F.col("order_id").isNull()).count())
    print("Item records with invalid prices:",
          items.filter(
              F.col("price").isNull() | (F.col("price") < 0)
          ).count())
    print("Item records with invalid freight values:",
          items.filter(
              F.col("freight_value").isNull()
              | (F.col("freight_value") < 0)
          ).count())

    # Aggregate item values to one row per order.
    item_summary = (
        items.groupBy("order_id")
        .agg(
            F.count("*").alias("item_count"),
            F.sum("price").alias("item_total"),
            F.sum("freight_value").alias("freight_total"),
            F.countDistinct("product_id").alias("distinct_products"),
            F.countDistinct("seller_id").alias("distinct_sellers"),
        )
    )

    print("\nOrder item summary:")
    item_summary.select(
        F.count("*").alias("orders_with_items"),
        F.sum("item_total").alias("sum_item_values"),
        F.sum("freight_total").alias("sum_freight_values"),
    ).show(truncate=False)

    print("\nReading payments...")
    payments = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW / "olist_order_payments_dataset.csv"))
    )

    print("Original payment rows:", payments.count())

    payments = (
        payments
        .withColumn("payment_value", F.col("payment_value").cast("double"))
        .withColumn(
            "payment_installments",
            F.col("payment_installments").cast("integer")
        )
    )

    print("\nPayment records with missing order IDs:",
          payments.filter(F.col("order_id").isNull()).count())
    print("Payment records with invalid payment values:",
          payments.filter(
              F.col("payment_value").isNull()
              | (F.col("payment_value") < 0)
          ).count())

    # Aggregate payment records separately to avoid item-payment multiplication.
    payment_summary = (
        payments.groupBy("order_id")
        .agg(
            F.sum("payment_value").alias("payment_total"),
            F.count("*").alias("payment_record_count"),
            F.countDistinct("payment_type").alias("payment_type_count"),
            F.max("payment_installments").alias("max_installments"),
        )
    )

    print("\nPayment summary:")
    payment_summary.select(
        F.count("*").alias("orders_with_payments"),
        F.sum("payment_total").alias("sum_payment_values"),
    ).show(truncate=False)

    # Save cleaned detail records and order-level aggregates.
    save_csv(items, CLEANED / "order_items")
    save_csv(payments, CLEANED / "order_payments")
    save_csv(item_summary, CLEANED / "order_item_summary")
    save_csv(payment_summary, CLEANED / "order_payment_summary")

    # Join only after each source is aggregated to one row per order.
    combined = (
        item_summary.alias("i")
        .join(payment_summary.alias("p"), on="order_id", how="full_outer")
    )

    print("\nCombined order-level summary:")
    combined.select(
        F.count("*").alias("orders_in_either_summary"),
        F.sum(
            F.when(F.col("item_total").isNotNull(), 1).otherwise(0)
        ).alias("orders_with_items"),
        F.sum(
            F.when(F.col("payment_total").isNotNull(), 1).otherwise(0)
        ).alias("orders_with_payments"),
    ).show(truncate=False)

    save_csv(combined, CLEANED / "order_purchase_summary")

    print("\nAll four outputs saved successfully.")

finally:
    spark.stop()
