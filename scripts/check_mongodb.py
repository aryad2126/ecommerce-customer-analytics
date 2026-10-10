from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

try:
    result = client.admin.command("ping")
    print("MongoDB connection: SUCCESS")
    print("Ping result:", result)

    print("\nExisting databases:")
    print(client.list_database_names())

finally:
    client.close()
