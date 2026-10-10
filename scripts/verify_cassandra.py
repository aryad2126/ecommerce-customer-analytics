from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"])
session = cluster.connect("ecommerce_analytics")

try:
    print("Checking Cassandra order history...")

    result = session.execute("""
        SELECT COUNT(*)
        FROM customer_order_history
    """)
    count = result.one()[0]

    print(f"Rows found in Cassandra: {count}")

    if count == 99441:
        print("PASS: All 99,441 order records are present.")
    else:
        print(f"CHECK: Expected 99,441 rows; found {count}.")

    print("\nSample order history:")
    rows = session.execute("""
        SELECT customer_unique_id, order_purchase_timestamp,
               order_id, order_status, item_total, payment_total
        FROM customer_order_history
        LIMIT 5
    """)

    for row in rows:
        print(row)

finally:
    session.shutdown()
    cluster.shutdown()
