import uuid
from flask import Blueprint, render_template, session
from app.models.bazi_history import BaziHistory
from app.models.divination_history import DivinationHistory

main_bp = Blueprint('main', __name__)


def ensure_session_id():
    """確保 session 中有唯一的 session_id，若無則產生一個。"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']


@main_bp.route('/')
def index():
    """
    首頁：顯示服務選擇區塊（八字排盤、線上占卜）。
    確保 session_id 已建立。
    """
    ensure_session_id()
    return render_template('index.html')


@main_bp.route('/history')
def history():
    """
    歷史紀錄頁：利用 session 內的 session_id，
    從資料庫查找此 session 的所有算命與占卜紀錄並條列。
    """
    session_id = ensure_session_id()

    bazi_records = BaziHistory.get_all_by_session(session_id)
    divination_records = DivinationHistory.get_all_by_session(session_id)

    return render_template(
        'history.html',
        bazi_records=bazi_records,
        divination_records=divination_records,
    )
