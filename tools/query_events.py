import sqlite3

conn = sqlite3.connect("/root/.hermes/profiles/side/verification_evidence.db")
cursor = conn.cursor()
for row in cursor.execute("SELECT command, output_summary FROM verification_events ORDER BY id DESC LIMIT 10"):
    print("CMD:", row[0])
    print("SUMMARY:", row[1])
    print("-" * 50)
