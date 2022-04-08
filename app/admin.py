from flask import Blueprint, redirect, url_for, request, flash, json
from config import CONVERSION_RATE
from models import db, db_session, DealRecords, User

from .utils.common_util import is_logged_in, build_response

admin_bp = Blueprint('admin', __name__, url_prefix='/')


# 管理员登录后，跳转到确认页面
@admin_bp.route('/admin/', methods=['GET', 'POST'])
@is_logged_in
def admin():
    # 查找数据库中所有未经确认的交易
    records = db_session.query(DealRecords).filter_by(confirmed=0).all()
    if request.method == 'GET':
        ret = {}
        data = {}
        i = 0
        for record in records:
            data["id"] = record.id
            data["user_id"] = record.user_id
            data["user_address"] = record.user_address
            data["deposit"] = record.deposit
            data["withdraw"] = record.withdraw
            data["confirmed"] = record.confirmed
            ret[i] = data
            i = i + 1
        response = build_response(ret, "200")
        return response
    elif request.method == 'POST':
        # 获得前端json数据
        json_dict = request.json
        deal_id = json_dict.get('id')
        deal_type = json_dict.get('type')
        admin_input = json_dict.get('input')

        record = db_session.query(DealRecords).get(deal_id)
        user_id = record.user_id

        # 确认交易
        if deal_type == 1:
            # 确认充值交易
            if record.deposit:
                deal_amount = record.deposit
                deposit_confirmed(user_id, deal_id, admin_input, deal_amount)
            else:
                # 确认提现交易
                deal_amount = record.withdraw
                withdraw_confirmed(user_id, deal_id, admin_input, deal_amount)
        else:
            # 拒绝交易
            admin_rejected(deal_id)

        ret = {"id": deal_id, "msg": "success"}
        response = build_response(ret, "200")
        return response


def withdraw_confirmed(user_id, deal_id, admin_input, deal_amount):

    # 如果管理员不输入充值金额，则按照用户输入的金额来换算币
    if not admin_input:
        actual_amount = admin_input
    else:
        actual_amount = deal_amount

    # 查询用户现有的币
    record = db_session.query(User).get(user_id)
    user_balance = record.balance

    # 用户的币减少
    withdraw_SACOB = actual_amount * CONVERSION_RATE
    user = db_session.query(User).get(user_id)
    user.balance = user_balance - withdraw_SACOB

    # deal表中confirmed状态改为1
    deal = db_session.query(DealRecords).get(deal_id)
    deal.confirmed = 1
    db_session.commit()


def deposit_confirmed(user_id, deal_id, admin_input, deal_amount):

    # 如果管理员不输入充值金额，则按照用户输入的金额来换算币
    if not admin_input:
        actual_amount = admin_input
    else:
        actual_amount = deal_amount

    # 查询用户现有的币
    record = db_session.query(User).get(user_id)
    user_balance = record.balance

    # 用户的币增加
    withdraw_SACOB = actual_amount * CONVERSION_RATE
    user = db_session.query(User).get(user_id)
    user.balance = user_balance + withdraw_SACOB

    # deal表中confirmed状态改为1
    deal = db_session.query(DealRecords).get(deal_id)
    deal.confirmed = 1
    db_session.commit()


def admin_rejected(deal_id):

    # deal表中confirmed状态改为2
    deal = db_session.query(DealRecords).get(deal_id)
    deal.confirmed = 2
    db_session.commit()
