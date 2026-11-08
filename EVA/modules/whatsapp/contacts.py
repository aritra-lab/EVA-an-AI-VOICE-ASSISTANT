
import re
from core.database import db


def initialize_contacts():
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("EVA: WHATSAPP CONTACTS READY.")
    except Exception as e:
        print(f"CONTACT DATABASE ERROR: {e}")



def add_contact(name, phone):
    try:
        name = name.strip()
        phone = phone.strip()

        if not name:
            print("EVA: CONTACT NAME IS REQUIRED.")
            return False

        # Remove common phone-number formatting characters
        phone = phone.replace(" ", "")
        phone = phone.replace("-", "")
        phone = phone.replace("(", "")
        phone = phone.replace(")", "")

        # Validate phone number
        if not re.fullmatch(r"\+?[0-9]{8,15}", phone):
            print("EVA: INVALID PHONE NUMBER.")
            return False

        db.execute(
            "INSERT INTO whatsapp_contacts (name, phone) VALUES (?, ?)",
            (name, phone)
        )

        print(f"EVA: {name} ADDED SUCCESSFULLY.")
        return True

    except Exception as e:
        print(f"ADD CONTACT ERROR: {e}")
        return False


def search_contacts(query):
    try:
        query = query.strip()

        return db.fetchall(
            """
            SELECT id, name, phone
            FROM whatsapp_contacts
            WHERE name LIKE ? OR phone LIKE ?
            ORDER BY name
            """,
            (f"%{query}%", f"%{query}%")
        )

    except Exception as e:
        print(f"SEARCH CONTACT ERROR: {e}")
        return []


def get_all_contacts():
    try:
        return db.fetchall(
            "SELECT id, name, phone FROM whatsapp_contacts ORDER BY name"
        )
    except Exception as e:
        print(f"GET CONTACTS ERROR: {e}")
        return []


def delete_contact(contact_id):
    try:
        db.execute(
            "DELETE FROM whatsapp_contacts WHERE id = ?",
            (contact_id,)
        )
        print("EVA: CONTACT DELETED.")
        return True

    except Exception as e:
        print(f"DELETE CONTACT ERROR: {e}")
        return False
