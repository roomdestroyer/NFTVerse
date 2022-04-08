from flask import Blueprint, render_template
from .utils.common_util import is_logged_in

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')


# Dashboard.html界面显示用户账号与导航栏
@dashboard_bp.route('/dashboard/')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')
