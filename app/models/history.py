import sqlite3
import json
from datetime import datetime

DATABASE_URL = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

class BaziHistory:
    @staticmethod
    def create(session_id, birth_year, birth_month, birth_day, birth_time, gender, bazi_result):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO bazi_history (session_id, birth_year, birth_month, birth_day, birth_time, gender, bazi_result) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session_id, birth_year, birth_month, birth_day, birth_time, gender, json.dumps(bazi_result))
        )
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute("SELECT * FROM bazi_history WHERE id = ?", (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def get_all_by_session(session_id):
        conn = get_db_connection()
        records = conn.execute("SELECT * FROM bazi_history WHERE session_id = ? ORDER BY created_at DESC", (session_id,)).fetchall()
        conn.close()
        return [dict(r) for r in records]

class DivinationHistory:
    @staticmethod
    def create(session_id, question, draw_result):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO divination_history (session_id, question, draw_result) VALUES (?, ?, ?)",
            (session_id, question, json.dumps(draw_result))
        )
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute("SELECT * FROM divination_history WHERE id = ?", (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def get_all_by_session(session_id):
        conn = get_db_connection()
        records = conn.execute("SELECT * FROM divination_history WHERE session_id = ? ORDER BY created_at DESC", (session_id,)).fetchall()
        conn.close()
        return [dict(r) for r in records]
