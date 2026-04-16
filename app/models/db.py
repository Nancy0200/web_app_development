import sqlite3
import os


def get_db_connection():
    """
    建立並回傳一個 SQLite 資料庫連線物件。
    使用 row_factory = sqlite3.Row，讓查詢結果可以用欄位名稱取值（類似 dict）。

    Returns:
        sqlite3.Connection: 資料庫連線物件
    """
    # 取得 instance 資料夾的路徑（相對於此檔案往上兩層）
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, 'instance', 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
