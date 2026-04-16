from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from app.models.bazi_history import BaziHistory
from app.models.bazi_logic import calculate_bazi
from app.routes.main import ensure_session_id

bazi_bp = Blueprint('bazi', __name__, url_prefix='/bazi')

CURRENT_YEAR = 2026


@bazi_bp.route('/')
def bazi_form():
    """
    顯示八字資料輸入表單頁面。
    讓使用者輸入出生年、月、日、時與性別。
    """
    return render_template('bazi/form.html', current_year=CURRENT_YEAR)


@bazi_bp.route('/calculate', methods=['POST'])
def bazi_calculate():
    """
    接收並處理使用者送出的生辰資料：
    1. 驗證必填欄位是否填寫
    2. 轉換資料型別並進行基本範圍驗證
    3. 呼叫八字排盤邏輯進行計算
    4. 存入資料庫並重導向至結果頁
    """
    session_id = ensure_session_id()

    # 取得表單資料
    birth_year_str = request.form.get('birth_year', '').strip()
    birth_month_str = request.form.get('birth_month', '').strip()
    birth_day_str = request.form.get('birth_day', '').strip()
    birth_time_str = request.form.get('birth_time', '').strip()
    gender = request.form.get('gender', '').strip()

    # 必填欄位驗證
    if not all([birth_year_str, birth_month_str, birth_day_str, gender]):
        flash('請填寫所有必填欄位（出生年月日與性別）。', 'danger')
        return redirect(url_for('bazi.bazi_form'))

    # 數值轉換與範圍驗證
    try:
        birth_year = int(birth_year_str)
        birth_month = int(birth_month_str)
        birth_day = int(birth_day_str)
        birth_time = int(birth_time_str) if birth_time_str else None

        if not (1900 <= birth_year <= CURRENT_YEAR):
            raise ValueError('年份超出範圍')
        if not (1 <= birth_month <= 12):
            raise ValueError('月份超出範圍')
        if not (1 <= birth_day <= 31):
            raise ValueError('日期超出範圍')
        if birth_time is not None and not (0 <= birth_time <= 23):
            raise ValueError('時辰超出範圍')
        if gender not in ('M', 'F'):
            raise ValueError('性別格式不正確')

    except ValueError as e:
        flash(f'輸入資料有誤：{e}，請重新確認。', 'danger')
        return redirect(url_for('bazi.bazi_form'))

    # 執行八字排盤計算
    bazi_result = calculate_bazi(birth_year, birth_month, birth_day, birth_time, gender)

    # 存入資料庫
    record_id = BaziHistory.create(
        session_id=session_id,
        birth_year=birth_year,
        birth_month=birth_month,
        birth_day=birth_day,
        birth_time=birth_time,
        gender=gender,
        bazi_result=bazi_result,
    )

    if record_id is None:
        flash('儲存紀錄時發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('bazi.bazi_form'))

    return redirect(url_for('bazi.bazi_result', record_id=record_id))


@bazi_bp.route('/result/<int:record_id>')
def bazi_result(record_id):
    """
    顯示單筆八字排盤結果頁：
    - 從資料庫查詢指定 id 的紀錄
    - 找不到則回傳 404
    - 找到則渲染結果頁並傳入資料
    """
    record = BaziHistory.get_by_id(record_id)

    if record is None:
        abort(404)

    return render_template('bazi/result.html', record=record)
