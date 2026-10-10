from pathlib import Path
from pyspark.sql import SparkSession

output = Path.cwd() / "data" / "processed" / "segmentation" / "rfm"

spark = (
    SparkSession.builder
    .appName("VerifyRFMOutput")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    rfm = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(output))
    )

    print("Output folder exists:", output.exists())
    print("Columns:", rfm.columns)
    print("Customer records:", rfm.count())

    print("\nSample records:")
    rfm.show(5, truncate=False)

    expected_columns = {
        "customer_unique_id",
        "recency_days",
        "frequency",
        "monetary"
    }

    if set(rfm.columns) == expected_columns and rfm.count() == 93358:
        print("\nPASS: RFM output verified.")
    else:
        print("\nCHECK: Output columns or record count differ from expected.")

finally:
    spark.stop()
