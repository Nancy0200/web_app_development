import json
import sqlite3
from app.models.db import get_db_connection


class DivinationHistory:
    """
    負責管理 divination_history 資料表的所有 CRUD 操作。
    每筆紀錄代表使用者一次線上占卜（抽籤）的問題與結果。
    """

    @staticmethod
    def create(session_id, question, draw_result):
        """
        新增一筆占卜紀錄到資料庫。

        Args:
            session_id (str): Flask session 的唯一識別碼，用以匹配使用者。
            question (str): 使用者心中默想的問題或疑惑。
            draw_result (dict): 抽籤結果的字典（含籤號、籤詩、解說等），會被序列化為 JSON。

        Returns:
            int | None: 成功時回傳新紀錄的 id，失敗時回傳 None。
        """
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO divination_history
                   (session_id, question, draw_result)
                   VALUES (?, ?, ?)""",
                (session_id, question, json.dumps(draw_result, ensure_ascii=False))
            )
            conn.commit()
            last_id = cur.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"[DivinationHistory.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        依 id 查詢單筆占卜紀錄。

        Args:
            record_id (int): 要查詢的紀錄 id。

        Returns:
            dict | None: 找到時回傳該紀錄的字典（含反序列化的 draw_result），否則回傳 None。
        """
        try:
            conn = get_db_connection()
            row = conn.execute(
                "SELECT * FROM divination_history WHERE id = ?", (record_id,)
            ).fetchone()

            if row is None:
                return None

            record = dict(row)
            # 將 JSON 字串反序列化回 dict
            record['draw_result'] = json.loads(record['draw_result'])
            return record
        except (sqlite3.Error, json.JSONDecodeError) as e:
            print(f"[DivinationHistory.get_by_id] 錯誤: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_by_session(session_id):
        """
        查詢某個 Session 所有的占卜歷史紀錄，依建立時間降序排列（最新在前）。

        Args:
            session_id (str): Flask session 的唯一識別碼。

        Returns:
            list[dict]: 紀錄列表，每筆為 dict；若無資料則回傳空列表。
        """
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM divination_history WHERE session_id = ? ORDER BY created_at DESC",
                (session_id,)
            ).fetchall()

            records = []
            for row in rows:
                record = dict(row)
                try:
                    record['draw_result'] = json.loads(record['draw_result'])
                except json.JSONDecodeError:
                    record['draw_result'] = {}
                records.append(record)
            return records
        except sqlite3.Error as e:
            print(f"[DivinationHistory.get_all_by_session] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def delete(record_id):
        """
        依 id 刪除一筆占卜紀錄。

        Args:
            record_id (int): 要刪除的紀錄 id。

        Returns:
            bool: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM divination_history WHERE id = ?", (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DivinationHistory.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()
