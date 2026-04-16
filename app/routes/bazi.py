from flask import Blueprint, render_template, request, redirect, url_for, session, abort

bazi_bp = Blueprint('bazi', __name__, url_prefix='/bazi')

@bazi_bp.route('/')
def bazi_form():
    """
    顯示給使用者輸入出生年、月、日、時與性別的 HTML 表單。
    """
    pass

@bazi_bp.route('/calculate', methods=['POST'])
def bazi_calculate():
    """
    處理使用者送出的生辰資料：
    1. 驗證資料有效性
    2. 確保 session 中有合法的 session_id
    3. 執行八字排盤邏輯運算
    4. 呼叫 BaziHistory model 將結果儲存進 DB
    5. 重導向到 /bazi/result/<id>
    """
    pass

@bazi_bp.route('/result/<int:record_id>')
def bazi_result(record_id):
    """
    使用 record_id 向資料庫查詢歷史紀錄：
    - 查無資料丟 404
    - 查到資料則渲染 bazi/result.html 顯示詳細排盤結果
    """
    pass
