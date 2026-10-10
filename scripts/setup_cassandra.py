from cassandra.cluster import Cluster

KEYSPACE = "ecommerce_analytics"

cluster = Cluster(["127.0.0.1"], port=9042)
session = None

try:
    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
        WITH replication = {{
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }}
    """)

    session.set_keyspace(KEYSPACE)

    session.execute("""
        CREATE TABLE IF NOT EXISTS customer_order_history (
            customer_unique_id text,
            order_purchase_timestamp timestamp,
            order_id text,
            order_status text,
            customer_state text,
            item_total double,
            payment_total double,
            order_approved_at timestamp,
            order_delivered_carrier_date timestamp,
            order_delivered_customer_date timestamp,
            order_estimated_delivery_date timestamp,
            PRIMARY KEY (
                (customer_unique_id),
                order_purchase_timestamp,
                order_id
            )
        ) WITH CLUSTERING ORDER BY (
            order_purchase_timestamp DESC,
            order_id ASC
        )
    """)

    print("Cassandra keyspace ready:", KEYSPACE)
    print("Table ready: customer_order_history")

    print("\nTable columns:")
    rows = session.execute("""
        SELECT column_name, kind, position
        FROM system_schema.columns
        WHERE keyspace_name = %s
          AND table_name = %s
    """, (KEYSPACE, "customer_order_history"))

    for row in rows:
        print(
            f"{row.column_name}: "
            f"kind={row.kind}, position={row.position}"
        )

    print("\nPASS: Cassandra schema created or already exists.")

finally:
    if session is not None:
        session.shutdown()
    cluster.shutdown()
