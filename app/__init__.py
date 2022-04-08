from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from config import config
from flask_mail import Mail
import os

# 导入蓝图板块
from .admin import admin_bp
from .artwork import artwork_bp
from .dashboard import dashboard_bp
from .user import user_bp
from .login import login_bp


# 声明一个方法, 创建app
def create_app():
    # 注册app
    app = Flask(__name__, static_folder='./static', template_folder='./template', static_url_path='')

    # 配置app
    env = os.getenv('FLASK_ENV')
    app.config.from_object(config.get(env))

    # app绑定数据库
    mail = Mail(app)
    mail.init_app(app)
    db = SQLAlchemy()
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(admin_bp)
    app.register_blueprint(artwork_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(login_bp)
    # CORS(app)

    return app
