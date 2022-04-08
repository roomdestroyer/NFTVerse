from flask import session, redirect, url_for, flash, make_response, jsonify
from functools import wraps
from models import db_session, Email_code
from flask_mail import Message, Mail
import random


# 判断用户是否已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login.login'))

    return wrap


# 发送6位随机验证码
def email_send(email_address):
    code = str("")
    for i in range(6):
        code += str(random.randint(0, 9))
    # 给用户提交的邮箱发送邮件
    mail = Mail()
    message = Message(subject='登录验证码', recipients=[email_address], body='您的验证码是：%s' % code)
    try:
        mail.send(message)
    except Exception:
        code = "error"
    record = db_session.query(Email_code).filter_by(email_address=email_address).all()

    if not record:
        db_session.add(Email_code(email_address=email_address, email_code=code))
        db_session.commit()
    else:
        record[0].email_code = code
        db_session.commit()

    return code


def build_response(data, status):
    response = make_response(jsonify(data))
    response.status = status
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

