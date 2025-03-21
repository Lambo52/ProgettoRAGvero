import sqlite3
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os

class DBManager:
    def __init__(self):
        self.db_file = 'date_storage.db'
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def initialize_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stored_date (
                id INTEGER PRIMARY KEY,
                date TEXT
            )
        ''')
        self.conn.commit()

    def setdate(self, date):  # NON TOCCARE NIENTE QUI
        if isinstance(date, str):
            date = parsedate_to_datetime(date)
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        # Assicurati che la tabella esista
        self.initialize_db()
        # id è 1 tanto è solo quello
        self.cursor.execute('''
            INSERT OR REPLACE INTO stored_date (id, date) VALUES (1, ?)
        ''', (date.isoformat(),))
        self.conn.commit()

    def get_stored_date(self):  # NON TOCCARE NIENTE QUI
        if not os.path.exists(self.db_file):
            return None
        try:
            self.cursor.execute('SELECT date FROM stored_date WHERE id = 1')
            row = self.cursor.fetchone()
            if row:
                return datetime.fromisoformat(row[0])
            else:
                return None
        except Exception as e:
            print(f"Errore lettura data salvata: {e}")
            return None

    def initialize_mail_ids_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mail_ids (
                id TEXT PRIMARY KEY
            )
        ''')
        self.conn.commit()

    def load_stored_ids(self):
        if not os.path.exists(self.db_file):
            return []
        try:
            self.cursor.execute('SELECT id FROM mail_ids')
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Errore lettura degli id: {e}")
            return []

    def save_ids(self, ids):
        # Assicurati che la tabella esista
        self.initialize_mail_ids_table()
        # Pulizia della tabella
        self.cursor.execute('DELETE FROM mail_ids')
        for mail_id in ids:
            self.cursor.execute('INSERT INTO mail_ids (id) VALUES (?)', (mail_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
