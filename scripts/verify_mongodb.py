from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

try:
    db = client["ecommerce_analytics"]
    customers = db["customers"]

    total = customers.count_documents({})
    unique_ids = len(customers.distinct("customer_unique_id"))

    # Count only customers whose cluster value is not null.
    with_rfm = customers.count_documents({
        "cluster": {"$ne": None}
    })

    without_rfm = customers.count_documents({
        "cluster": None
    })

    print("Total documents:", total)
    print("Unique customer IDs:", unique_ids)
    print("Customers with RFM data:", with_rfm)
    print("Customers without RFM data:", without_rfm)

    print("\nCustomer counts by cluster:")
    for result in customers.aggregate([
        {"$match": {"cluster": {"$ne": None}}},
        {"$group": {
            "_id": "$cluster",
            "customer_count": {"$sum": 1},
            "average_frequency": {"$avg": "$frequency"},
            "average_monetary": {"$avg": "$monetary"}
        }},
        {"$sort": {"_id": 1}}
    ]):
        print(result)

    if (
        total == 96096
        and unique_ids == 96096
        and with_rfm == 93358
        and without_rfm == 2738
    ):
        print("\nPASS: MongoDB data verified.")
    else:
        print("\nCHECK: Counts differ from expected values.")

finally:
    client.close()
