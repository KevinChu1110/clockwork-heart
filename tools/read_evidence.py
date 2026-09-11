import sqlite3

conn = sqlite3.connect("/root/.hermes/profiles/side/verification_evidence.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())
for row in cursor.execute("SELECT * FROM sqlite_master WHERE type='table'"):
    print(row)
