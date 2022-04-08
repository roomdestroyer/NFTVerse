from flask_migrate import Migrate, MigrateCommand
from flask import redirect, url_for, request, render_template
from flask_script import Manager
from models import db, db_session, User
from app import create_app
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from config import config
from flask_mail import Mail
import os

# 导入蓝图板块
from app.admin import admin_bp
from app.artwork import artwork_bp
from app.dashboard import dashboard_bp
from app.user import user_bp
from app.login import login_bp


app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
# @cross_origin()
def index():
    return render_template('index.html')


if __name__ == '__main__':
    """
    db_session.add_all([
        DealRecords(user_id=1, deposit=10, withdraw=0, confirmed=0),
        DealRecords(user_id=2, deposit=11, withdraw=0, confirmed=0)
    ])
    r = db_session.query(DealRecords).filter_by(confirmed=0).all()
    for instance in r:
        print(instance.id, "  ", instance.user_id, "  ", instance.deposit)

    record_id = 1
    deals = db_session.query(DealRecords).filter_by(user_id=1)
    for item in deals:
        item.confirmed = 1
    db_session.commit()
    """
    """
    db_session.add_all(([
        User(user_id=1, password=1, email_address='1761806916@qq.com'),
        User(user_id=2, password=2)
    ]))
    db_session.commit()
    """
    # manager.run()
    # app.template_folder = 'D:\\00000\\sdunft\\app\\dist'
    print(app.template_folder)
    app.run()
