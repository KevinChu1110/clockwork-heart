import sqlite3

conn = sqlite3.connect("/root/.hermes/profiles/side/state.db")
c = conn.cursor()
for col in c.execute("PRAGMA table_info(messages);"):
    print(col)
c.execute("SELECT tool_calls FROM messages WHERE id=23508;")
row = c.fetchone()
print("tool_calls:", row[0])
