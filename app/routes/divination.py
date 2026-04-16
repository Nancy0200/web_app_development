from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from app.models.divination_history import DivinationHistory
from app.models.divination_data import draw_lot
from app.routes.main import ensure_session_id

divination_bp = Blueprint('divination', __name__, url_prefix='/divination')


@divination_bp.route('/')
def divination_draw_page():
    """
    顯示占卜抽籤儀式頁面。
    讓使用者輸入心中默念的問題後點擊「抽籤」。
    """
    return render_template('divination/draw.html')


@divination_bp.route('/draw', methods=['POST'])
def divination_draw_action():
    """
    接收並處理抽籤請求：
    1. 確保 session_id 存在
    2. 取得並驗證使用者輸入的問題
    3. 執行隨機抽籤演算法
    4. 將問題與籤詩結果存入資料庫
    5. 重導向至結果頁
    """
    session_id = ensure_session_id()

    question = request.form.get('question', '').strip()

    if not question:
        flash('請先在心中默想您的問題，並在欄位中填寫。', 'warning')
        return redirect(url_for('divination.divination_draw_page'))

    if len(question) > 200:
        flash('問題描述請勿超過 200 字。', 'warning')
        return redirect(url_for('divination.divination_draw_page'))

    # 執行抽籤
    lot_result = draw_lot()

    # 存入資料庫
    record_id = DivinationHistory.create(
        session_id=session_id,
        question=question,
        draw_result=lot_result,
    )

    if record_id is None:
        flash('儲存紀錄時發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('divination.divination_draw_page'))

    return redirect(url_for('divination.divination_result', record_id=record_id))


@divination_bp.route('/result/<int:record_id>')
def divination_result(record_id):
    """
    顯示單筆占卜結果頁：
    - 從資料庫查詢指定 id 的籤詩紀錄
    - 找不到則回傳 404
    - 找到則渲染籤詩解析頁面
    """
    record = DivinationHistory.get_by_id(record_id)

    if record is None:
        abort(404)

    return render_template('divination/result.html', record=record)
