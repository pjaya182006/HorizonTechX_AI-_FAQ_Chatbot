import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    user_message TEXT,
                    bot_response TEXT,
                    confidence REAL,
                    timestamp TEXT
                )
            ''')
            conn.commit()

    def log_message(self, username, user_msg, bot_resp, confidence):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO chat_logs (username, user_message, bot_response, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, user_msg, bot_resp, confidence, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()

    def get_chat_history(self, username):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM chat_logs WHERE username = ? ORDER BY id ASC', (username,))
            return cursor.fetchall()

    def get_global_logs(self, limit=50):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM chat_logs ORDER BY id DESC LIMIT ?', (limit,))
            return cursor.fetchall()

    def get_analytics_summary(self):
        with self.get_connection() as conn:
            total_queries = conn.execute('SELECT COUNT(*) FROM chat_logs').fetchone()[0]
            avg_confidence = conn.execute('SELECT AVG(confidence) FROM chat_logs').fetchone()[0] or 0.0
            return {
                'total_queries': total_queries,
                'avg_confidence': round(avg_confidence, 2)
            }