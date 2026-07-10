import uuid
import json
from datetime import datetime
import psycopg2


class RequestContext:

    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
  
    
    def __del__(self):
        self.conn.close()
        

    def new_request(self, session_id: str):
        return str(uuid.uuid4())

    # =========================
    # log event
    # =========================
    def add(self, request_id, session_id, role, content, metadata=None):

        metadata = metadata or {}

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO request
                (request_id, session_id, role, content, metadata, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                request_id,
                session_id,
                role,
                content,
                json.dumps(metadata),
                datetime.now()
            ))

        self.conn.commit()

    # =========================
    # get full context for agent
    # =========================
    def get(self, request_id, limit=50):

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT role, content, metadata, created_at
                FROM request
                WHERE request_id = %s
                ORDER BY id ASC
                LIMIT %s
            """, (request_id, limit))

            rows = cur.fetchall()

        return [
            {
                "role": r[0],
                "content": r[1],
                "metadata": r[2],
                "time": r[3].isoformat()
            }
            for r in rows
        ]