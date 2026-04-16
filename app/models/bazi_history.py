import json
import sqlite3
from app.models.db import get_db_connection


class BaziHistory:
    """
    負責管理 bazi_history 資料表的所有 CRUD 操作。
    每筆紀錄代表使用者一次八字排盤與命格解析的完整結果。
    """

    @staticmethod
    def create(session_id, birth_year, birth_month, birth_day, birth_time, gender, bazi_result):
        """
        新增一筆八字算命紀錄到資料庫。

        Args:
            session_id (str): Flask session 的唯一識別碼，用以匹配使用者。
            birth_year (int): 出生年份。
            birth_month (int): 出生月份（1-12）。
            birth_day (int): 出生日期（1-31）。
            birth_time (int | None): 出生時辰（0-23），可為 None。
            gender (str): 性別，'M' 代表男，'F' 代表女。
            bazi_result (dict): 八字計算結果的字典，會被序列化為 JSON 字串存入 DB。

        Returns:
            int | None: 成功時回傳新紀錄的 id，失敗時回傳 None。
        """
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO bazi_history
                   (session_id, birth_year, birth_month, birth_day, birth_time, gender, bazi_result)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, birth_year, birth_month, birth_day, birth_time, gender, json.dumps(bazi_result, ensure_ascii=False))
            )
            conn.commit()
            last_id = cur.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"[BaziHistory.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        依 id 查詢單筆八字算命紀錄。

        Args:
            record_id (int): 要查詢的紀錄 id。

        Returns:
            dict | None: 找到時回傳該紀錄的字典（含反序列化的 bazi_result），否則回傳 None。
        """
        try:
            conn = get_db_connection()
            row = conn.execute(
                "SELECT * FROM bazi_history WHERE id = ?", (record_id,)
            ).fetchone()

            if row is None:
                return None

            record = dict(row)
            # 將 JSON 字串反序列化回 dict
            record['bazi_result'] = json.loads(record['bazi_result'])
            return record
        except (sqlite3.Error, json.JSONDecodeError) as e:
            print(f"[BaziHistory.get_by_id] 錯誤: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_by_session(session_id):
        """
        查詢某個 Session 所有的八字算命歷史紀錄，依建立時間降序排列（最新在前）。

        Args:
            session_id (str): Flask session 的唯一識別碼。

        Returns:
            list[dict]: 紀錄列表，每筆為 dict；若無資料則回傳空列表。
        """
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM bazi_history WHERE session_id = ? ORDER BY created_at DESC",
                (session_id,)
            ).fetchall()

            records = []
            for row in rows:
                record = dict(row)
                try:
                    record['bazi_result'] = json.loads(record['bazi_result'])
                except json.JSONDecodeError:
                    record['bazi_result'] = {}
                records.append(record)
            return records
        except sqlite3.Error as e:
            print(f"[BaziHistory.get_all_by_session] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def delete(record_id):
        """
        依 id 刪除一筆八字算命紀錄。

        Args:
            record_id (int): 要刪除的紀錄 id。

        Returns:
            bool: 成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM bazi_history WHERE id = ?", (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[BaziHistory.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()
