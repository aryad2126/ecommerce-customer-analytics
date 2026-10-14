"""
hdfs_storage_pipeline.py
HDFS Data Loading and Export Utility for Big Data Analytics Mini Project.
Demonstrates HDFS integration using the Hadoop CLI (`hdfs dfs`).
Decoupled from normal dashboard startup so the dashboard runs seamlessly whether HDFS is active or offline.
"""

import subprocess
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MARTS_DIR = BASE_DIR / "data" / "processed" / "marts"
HDFS_TARGET_DIR = "/ecommerce_analytics/marts"

def is_hdfs_reachable(host="localhost", port=9000, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def run_hdfs_pipeline():
    print("=" * 60)
    print("HDFS DISTRIBUTED STORAGE PIPELINE")
    print("=" * 60)

    print(f"Checking HDFS NameNode at localhost:9000...")
    if not is_hdfs_reachable():
        print("[STATUS] HDFS NameNode is currently offline / not running on port 9000.")
        print("To start Hadoop HDFS in Windows / WSL:")
        print("  1. Run: %HADOOP_HOME%\\sbin\\start-dfs.cmd (or in WSL: start-dfs.sh)")
        print("  2. Verify NameNode at http://localhost:9870")
        print("  3. Re-run this script: python scripts/hdfs_storage_pipeline.py")
        print("\nThe Streamlit dashboard handles this status gracefully and reports 'Hadoop offline'.")
        return False

    print("[SUCCESS] HDFS NameNode is ACTIVE and reachable!")
    print(f"Creating HDFS target directory: {HDFS_TARGET_DIR}...")
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", HDFS_TARGET_DIR], check=True)

    print(f"Uploading processed marts to HDFS from {MARTS_DIR}...")
    for csv_file in MARTS_DIR.glob("*.csv"):
        print(f"  Uploading {csv_file.name} to {HDFS_TARGET_DIR}/...")
        subprocess.run(["hdfs", "dfs", "-put", "-f", str(csv_file), f"{HDFS_TARGET_DIR}/{csv_file.name}"], check=True)

    print("\nVerifying files in HDFS:")
    subprocess.run(["hdfs", "dfs", "-ls", HDFS_TARGET_DIR], check=True)
    print("\n[SUCCESS] HDFS export pipeline completed successfully.")
    return True

if __name__ == "__main__":
    run_hdfs_pipeline()
