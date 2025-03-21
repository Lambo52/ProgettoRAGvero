import sqlite3
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os

DATABASE_FILE = 'date_storage.db'

def initialize_db():
    #creazione db e tabella 1, tabella 2 fatta dopo perché si
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stored_date (
            id INTEGER PRIMARY KEY,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def setdate(date):  # NON TOCCARE NIENTE QUI
    if isinstance(date, str):
        date = parsedate_to_datetime(date)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    
    initialize_db()  #assolutamente da tenere
    
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    # id è 1 tanto è solo quello
    c.execute('''
        INSERT OR REPLACE INTO stored_date (id, date) VALUES (1, ?)
    ''', (date.isoformat(),))
    conn.commit()
    conn.close()

def get_stored_date():  # NON TOCCARE NIENTE QUI
    if not os.path.exists(DATABASE_FILE):
        return None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT date FROM stored_date WHERE id = 1')
        row = c.fetchone()
        conn.close()
        if row:
            return datetime.fromisoformat(row[0])
        else:
            return None
    except Exception as e:
        print(f"Errore lettura data salvata: {e}")
        return None

def initialize_mail_ids_table():
    
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mail_ids (
            id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def load_stored_ids():
    
    if not os.path.exists(DATABASE_FILE):
        return []
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT id FROM mail_ids')
        rows = c.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Errore lettura degli id: {e}")
        return []

def save_ids(ids):
    
    initialize_mail_ids_table()  # Assicurati che la tabella esista
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    #via tutto e metto tutto da 0
    c.execute('DELETE FROM mail_ids')
    
    for mail_id in ids:
        c.execute('INSERT INTO mail_ids (id) VALUES (?)', (mail_id,))
    conn.commit()
    conn.close()
