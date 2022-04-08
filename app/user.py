from flask import Blueprint, redirect, json, url_for, request, flash, render_template, session
from config import ADMIN_ADDRESS
from models import User, db_session, DealRecords
from .utils.common_util import is_logged_in, build_response

user_bp = Blueprint('user', __name__, url_prefix='/')


# 用户个人主页
@user_bp.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        user_id = json_dict.get('user_id')
        record = db_session.query(User).filter_by(user_id=user_id).all()
        team_count = 0
        if record:
            data = {"user_id": record[0].user_id, "password": record[0].password,
                    "email_address": record[0].email_address, "balance": record[0].balance, "profit": record[0].profit, "team_count": team_count,
                    "team_performance": record[0].team_performance, "leader_id": record[0].leader_id, "rank": record[0].rank}
            response = build_response(data, "200")
            return response
        else:
            response = build_response({"msg": "用户不存在"}, "200")
            return response
    else:
        return render_template('user.html')


# 暂不支持个人信息的修改，后期若需要再扩充
"""
# 用户修改个人信息页面
@app.route('/edit/', methods=['GET', 'POST'])
@is_logged_in
def edit():
    user_id = session.get('user_id')
    db = MysqlUtil()
    if request.method == 'GET':
        sql = "SELECT * FROM user_information  WHERE id = '%s'" % user_id
        record = db.fetchone(sql)
        # 如果用户记录不存在，提示错误信息
        if not record:
            flash('用户不存在！')
            return redirect(url_for('login'))
        else:
            return render_template('edit.html', msg=record)
    elif request.method == 'POST':
        pass
"""


# 我的团队
@user_bp.route('/team', methods=['GET', 'POST'])
@is_logged_in
def team():
    if request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        user_id = json_dict.get('user_id')
        user_record = db_session.query(User).get(user_id)
        if not user_record:
            response = build_response({"msg": "account_error"}, "100")
            return response

        leader_id = user_record.leader_id

        teammate_records = db_session.query(User).filter_by(leader_id=leader_id).all()
        teammates_count = 0
        for i in teammate_records:
            teamates_count = teammates_count + 1

        # 查询团队业绩
        team_performance = 0
        for teammate in teammate_records:
            team_performance = teammate.profit + team_performance

        data = {"teammates_count": teammates_count, "team_performance": team_performance}
        response = build_response(data, "200")
        return response
    else:
        return render_template('team.html')


# 用户申请充值
@user_bp.route('/deposit', methods=['GET', 'POST'])
@is_logged_in
def deposit():
    if request.method == 'GET':
        return render_template('deposit.html')
    elif request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        user_id = json_dict.get('user_id')
        usdt_address = json_dict.get('usdt_address')
        deposit_amount = json_dict.get('deposit_amount')

        db_session.add(DealRecords(user_id=user_id, user_address=usdt_address, deposit=deposit_amount, withdraw=0, confirmed=0))
        db_session.commit()

        response = build_response({"msg": "success"}, "200")
        return response


# 用户申请提现
@user_bp.route('/withdraw', methods=['GET', 'POST'])
@is_logged_in
def withdraw():
    if request.method == 'GET':
        return render_template('withdraw.html')
    elif request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        user_id = json_dict.get('user_id')
        usdt_address = json_dict.get('usdt_address')
        withdraw_amount = json_dict.get('withdraw_amount')

        db_session.add(DealRecords(user_id=user_id, user_address=usdt_address, deposit=0, withdraw=withdraw_amount, confirmed=0))
        db_session.commit()

        response = build_response({"msg": "success"}, "200")
        return response
