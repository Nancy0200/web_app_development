from flask import Blueprint, render_template, session, request, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示服務選擇區塊 (八字排盤、線上占卜)。
    """
    pass

@main_bp.route('/history')
def history():
    """
    歷史紀錄頁：利用 session 內的 session_id，從資料庫查找此人的所有算命與占卜紀錄並條列。
    """
    pass
