from core.database import db

db.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT
)
""")

def add_note(note):
    db.execute(
        "INSERT INTO notes (note) VALUES (?)",(note,))

def get_notes():
    return db.fetchall("SELECT * FROM notes")

def clear_notes():
    db.execute("DELETE FROM notes")

def notes_count():
    result=db.fetchone("SELECT COUNT(*) FROM notes")
    return result[0]

def delete_note(note_id):
    db.execute(
        "DELETE FROM notes WHERE id=?",
        (note_id,)
    )

def find_note_by_keyword(keyword):
    return db.fetchall(
        "SELECT id, note FROM notes WHERE note LIKE ?",
        ('%' + keyword + '%',)
    )