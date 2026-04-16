import os
import sqlite3
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # 設定 Secret Key（供 Session 使用）
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫
    init_db(app)

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.bazi import bazi_bp
    from app.routes.divination import divination_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(bazi_bp)
    app.register_blueprint(divination_bp)

    return app


def init_db(app):
    """根據 database/schema.sql 初始化 SQLite 資料庫"""
    db_path = os.path.join(app.instance_path, 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')

    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
