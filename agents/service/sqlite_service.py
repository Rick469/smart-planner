import sqlite3
import time

class PlannerDB:

    def __init__(self, db_path="../planner.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_table()

    def __del__(self):
        self.conn.close()

    def _init_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            timestamp REAL
        )
        """)
        self.conn.commit()

    def set_cache(self, key, value):
        self.conn.execute(
            "REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
            (key, value, time.time())
        )
        self.conn.commit()

    def get_cache(self, key, ttl=3600):

        cursor = self.conn.execute(
            "SELECT value, timestamp FROM cache WHERE key=?",
            (key,)
        )

        row = cursor.fetchone()
        if not row:
            return None

        value, ts = row

        if time.time() - ts > ttl:
            return None

        return value