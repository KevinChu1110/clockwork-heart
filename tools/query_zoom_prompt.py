import sqlite3

conn = sqlite3.connect("/root/.hermes/profiles/side/state.db")
c = conn.cursor()
c.execute("SELECT id, content, tool_calls FROM messages WHERE id=23506;")
row = c.fetchone()
if row:
    print("content:", row[1])
    print("tool_calls:", row[2])
