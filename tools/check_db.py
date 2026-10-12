import sqlite3

conn = sqlite3.connect('/root/.hermes/kanban/boards/side-bravesoul/kanban.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT id, status, current_run_id, assignee FROM tasks WHERE id='t_4884c141'")
row = cur.fetchone()
print(dict(row) if row else "None")

cur.execute("SELECT id, task_id, profile, status, outcome FROM task_runs WHERE task_id='t_4884c141' ORDER BY id DESC")
for r in cur.fetchall():
    print("run:", dict(r))
conn.close()
