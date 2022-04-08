from flask import Blueprint, session, redirect, url_for, request, flash, render_template, jsonify, make_response
from flask_cors import cross_origin, CORS
from models import User, db_session, Admin, Email_code
from .utils.common_util import email_send, is_logged_in, build_response
from config import basedir
import json

login_bp = Blueprint('login', __name__)
CORS(login_bp)


# 用户注册
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获得前端json数据
        json_dict = json.loads(request.get_data(as_text=True))
        register_id = json_dict.get('user_id')
        register_email = json_dict.get('email_address')
        code = "200"

        # 根据register_id查找user_information表中记录
        user_record = db_session.query(User).filter_by(user_id=register_id).all()
        if user_record:
            data = {"msg": "注册账号已存在"}
            response = build_response(data, code)
            return response

        # 账号不存在, 验证邮箱是否可用
        email_record = db_session.query(User).filter_by(email_address=register_email).all()
        if email_record:
            data = {"msg": "注册邮箱已存在"}
            response = build_response(data, code)
            return response
        else:
            # 发送验证码
            data = {"msg": "邮箱验证码已发送"}
            if email_send(register_email) == "error":
                data = {"msg": "邮箱错误"}
            response = build_response(data, code)
            return response


@login_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        return render_template('verify.html')
    if request.method == 'POST':
        # 获得用户输入的验证码
        # 错：json_dict = request.json
        json_dict = json.loads(request.get_data(as_text=True))
        code = "200"
        user_id = json_dict.get('user_id')
        password = json_dict.get('password')
        email_address = json_dict.get('email_address')
        input_code = json_dict.get('email_code')

        record = db_session.query(Email_code).filter_by(email_address=email_address).all()
        if not record:
            data = {"msg": "邮箱错误"}
            response = build_response(data, code)
            return response
        email_code = record[0].email_code

        if input_code != email_code:
            data = {"msg": "验证码输入错误"}
            response = build_response(data, code)
            return response
        else:
            # 用户输入验证码正确
            # if not db_session.query(User).filter_by(user_id=user_id).all() and not db_session.query(User).filter_by(email_address=email_address):
            db_session.add(User(user_id=user_id, password=password, email_address=email_address,
                                balance=0, profit=0, team_performance=0, leader_id=0, rank=0))
            db_session.commit()
            session['logged_in'] = True
            session['user_id'] = user_id
            data = {"msg": "验证成功"}

            response = build_response(data, code)
            return response


# 用户登录
@cross_origin()
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    print(11111)
    # 获得前端json数据
    if request.method == 'GET':
        return render_template('login.html')
    json_dict = json.loads(request.get_data(as_text=True))
    candidate_user_id = json_dict.get('user_id')
    candidate_password = json_dict.get('password')
    user_record = db_session.query(User).filter_by(user_id=candidate_user_id).all()
    admin_record = db_session.query(Admin).filter_by(user_id=candidate_user_id).all()
    code = "200"
    if not user_record and not admin_record:
        data = {"msg": "账号不存在"}
        response = build_response(data, code)
        return response

    # 对比用户填写的密码和用户表中记录的密码是否一致
    if user_record:
        # 用户密码验证
        if candidate_password == user_record[0].password:
            # 写入session
            session['logged_in'] = True
            session['user_id'] = candidate_user_id
            email_address = user_record[0].email_address
            balance = user_record[0].balance
            profit = user_record[0].profit
            team_performance = user_record[0].team_performance
            leader_id = user_record[0].leader_id
            rank = user_record[0].rank
            """
            data = {"msg": "用户登录成功", "user_id": candidate_user_id, "password": candidate_password,
                    "email_address": email_address, "balance": balance, "profit": profit,
                    "team_performance": team_performance, "leader_id": leader_id, "rank": rank}
            """
            data = {"msg": "用户登录成功"}
            response = build_response(data, code)
            return response
        else:
            data = {"msg": "密码错误"}
            response = build_response(data, code)
            return response
    # 对比用户填写的密码和管理员表中记录的密码是否一致
    if admin_record:
        if candidate_password == admin_record[0].password:
            data = {"msg": "管理员登录成功"}
            response = build_response(data, code)
            return response
        else:
            data = {"msg": "密码错误"}
            response = build_response(data, code)
            return response


# 退出登录
@login_bp.route('/logout')
def logout():
    session.clear()
    data = {"msg": "成功退出"}
    code = "200"
    response = build_response(data, code)
    return response
