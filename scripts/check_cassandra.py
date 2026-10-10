from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"], port=9042)
session = None

try:
    session = cluster.connect()

    print("Cassandra connection: SUCCESS")
    print("Cassandra version:", cluster.metadata.cluster_name)

    print("\nExisting keyspaces:")
    rows = session.execute("""
        SELECT keyspace_name
        FROM system_schema.keyspaces
    """)

    for row in rows:
        print("-", row.keyspace_name)

finally:
    if session is not None:
        session.shutdown()
    cluster.shutdown()
