from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BASE = Path.cwd()
CLEANED = BASE / "data" / "processed" / "cleaned"

spark = (
    SparkSession.builder
    .appName("CheckOrderCoverage")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    orders = (
        spark.read.option("header", True)
        .csv(str(CLEANED / "orders"))
    )

    items = (
        spark.read.option("header", True)
        .csv(str(CLEANED / "order_item_summary"))
        .select("order_id")
        .withColumn("has_items", F.lit(True))
    )

    payments = (
        spark.read.option("header", True)
        .csv(str(CLEANED / "order_payment_summary"))
        .select("order_id")
        .withColumn("has_payment", F.lit(True))
    )

    coverage = (
        orders.select("order_id", "order_status")
        .join(items, "order_id", "left")
        .join(payments, "order_id", "left")
        .withColumn("has_items", F.coalesce("has_items", F.lit(False)))
        .withColumn(
            "has_payment",
            F.coalesce("has_payment", F.lit(False))
        )
    )

    print("\nOrder coverage by status:")
    (
        coverage.groupBy("order_status", "has_items", "has_payment")
        .count()
        .orderBy("order_status", "has_items", "has_payment")
        .show(100, truncate=False)
    )

    print("\nOrders missing item records:")
    coverage.filter(~F.col("has_items")).groupBy("order_status").count().show()

    print("\nOrders missing payment records:")
    coverage.filter(~F.col("has_payment")).groupBy("order_status").count().show()

finally:
    spark.stop()
