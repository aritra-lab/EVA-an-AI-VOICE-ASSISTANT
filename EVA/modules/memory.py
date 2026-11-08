from core.database import db
db.execute("""
CREATE TABLE IF NOT EXISTS memory (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
def remember(key, value):
    key = key.lower().strip()
    db.execute(
    "INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)",
    (key, value))
def recall(key):
    key = key.lower().strip()
    result = db.fetchone(
    "SELECT value FROM memory WHERE key=?",
    (key,)
)
    if result:
        return result[0]
    return None
def get_all_memories():
    memories = db.fetchall("SELECT * FROM memory")
    return memories
def forget(key):
    key = key.lower().strip()
    db.execute(
    "DELETE FROM memory WHERE key=?",
    (key,)
)