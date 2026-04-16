from flask import Blueprint, render_template, request, redirect, url_for, session, abort

divination_bp = Blueprint('divination', __name__, url_prefix='/divination')

@divination_bp.route('/')
def divination_draw_page():
    """
    顯示讓使用者輸入問題（默想）並點選「抽籤」的儀式感頁面。
    """
    pass

@divination_bp.route('/draw', methods=['POST'])
def divination_draw_action():
    """
    處理抽籤請求：
    1. 確保 session 存在
    2. 接收並記錄使用者的問題字串
    3. 呼叫隨機抽籤演算法，取得一支籤詩
    4. 存入 DivinationHistory DB 中
    5. 重導向到結果頁
    """
    pass

@divination_bp.route('/result/<int:record_id>')
def divination_result(record_id):
    """
    使用 record_id 向 DivinationHistory 查詢：
    - 找到就解析 JSON 並渲染 divination/result.html
    - 找不到就 404
    """
    pass
