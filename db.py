import sqlite3
import os
from pathlib import Path

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_dick_stats (
                user_id TEXT PRIMARY KEY,
                user_name TEXT,
                length REAL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def get_user_length(self, user_id: str):
        cursor = self.conn.cursor()
        cursor.execute('SELECT length FROM user_dick_stats WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0.0

    def update_user_length(self, user_id: str, user_name: str, length: float):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO user_dick_stats (user_id, user_name, length) 
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            length = excluded.length,
            user_name = excluded.user_name
        ''', (user_id, user_name, length))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
