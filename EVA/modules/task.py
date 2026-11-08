from core.database import db
from datetime import date

db.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    due_date TEXT,
    priority TEXT DEFAULT 'normal',
    completed INTEGER DEFAULT 0
)
""")

def add_task(task, due_date, priority):
    db.execute(
        "INSERT INTO tasks (task, due_date, priority) VALUES (?, ?, ?)",
        (task, due_date, priority)
    )

def get_tasks():
    return db.fetchall(
        "SELECT id, task, due_date, priority, completed FROM tasks"
    )

def find_task_by_keyword(keyword):
    return db.fetchall(
        "SELECT id, task FROM tasks WHERE task LIKE ?",
        ('%' + keyword + '%',)
    )

def complete_task(task_id):
    db.execute(
        "UPDATE tasks SET completed=1 WHERE id=?",
        (task_id,)
    )

def delete_task(keyword):
    db.execute(
        "DELETE FROM tasks WHERE task LIKE ?",
        ('%' + keyword + '%',)
    )

def delete_task_by_id(task_id):
    db.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )
 
def get_due_tasks():
    today = str(date.today())

    return db.fetchall(
        "SELECT * FROM tasks WHERE due_date=? AND completed=0",
        (today,)
    )

def get_overdue_tasks():
    today = str(date.today())

    return db.fetchall(
        "SELECT * FROM tasks WHERE due_date < ? AND completed=0",
        (today,)
    )

def get_pending_tasks():
    return db.fetchall(
        "SELECT id, task, due_date FROM tasks WHERE completed=0"
    )

def task_count():
    result = db.fetchone(
        "SELECT COUNT(*) FROM tasks"
    )
    return result[0]

def pending_task_count():
    result = db.fetchone(
        "SELECT COUNT(*) FROM tasks WHERE completed=0"
    )
    return result[0]
