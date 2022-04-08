from flask import Blueprint, session, redirect, json, request, url_for, flash, render_template
from config import ADMIN_ADDRESS
from models import Artwork, db_session, User, Investment

from .utils.common_util import is_logged_in, build_response

artwork_bp = Blueprint('artwork', __name__, url_prefix='/')


# 艺术品主页
@artwork_bp.route('/artwork/', methods=['POST', 'GET'])
# @is_logged_in
def artwork():
    # 渲染静态页面
    if request.method == 'GET':
        records = db_session.query(Artwork).all()
        ret = {}
        data = {}
        i = 0
        for record in records:
            data["id"] = record.id
            data["name"] = record.name
            data["artist"] = record.artist
            data["details"] = record.details
            data["price"] = record.price
            data["image"] = record.image
            ret[i] = data
            i = i + 1
        response = build_response(ret, "200")
        return response


# 用户点击进入某个艺术品后，显示该艺术品的详细信息与投资选项
@artwork_bp.route('/artwork/details/', methods=['POST', 'GET'])
# @is_logged_in
def details():
    if request.method == 'GET':
        return render_template('details.html')
    if request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        artwork_id = json_dict.get('id')
        record = db_session.query(Artwork).get(artwork_id)
        data = {"id": record.id, "name": record.name, "artist": record.artist, "details": record.details,
                "price": record.price, "image": record.image}
        response = build_response(data, "200")
        return response


# 用户在艺术品详情页点击投资按钮后，跳转到该页面，显示平台U地址，用户自己确认是否执行投资
@artwork_bp.route('/artwork/details/invest/', methods=['POST', 'GET'])
# @is_logged_in
def invest():
    if request.method == 'GET':
        return render_template('invest.html')
    elif request.method == 'POST':
        json_dict = json.loads(request.get_data(as_text=True))
        user_id = json_dict.get('user_id')
        artwork_id = json_dict.get('artwork_id')
        # 获取艺术品的价格
        artwork_record = db_session.query(Artwork).get(artwork_id)

        # 获取用户余额
        user_record = db_session.query(User).get(user_id)
        user_balance = user_record.balance

        # 用户账户余额不足，则不能投资
        if not user_balance:
            data = {"msg": "balance_insufficient"}
            return json.dumps(data), 105, {"ContentType": "application/json"}

        # 艺术品price上升，用户资产减少
        artwork_record.price = artwork_record.price + user_balance
        user_record.balance = 0

        relevant_investment = db_session.query(Investment).filter_by(user_id=user_id, artwork_id=artwork_id).all()
        # 如果投资关系存在，则将投资额度加进去
        if relevant_investment:
            relevant_investment.asset = relevant_investment.asset + user_balance
        else:
            # 如果投资关系不存在，则增加一条投资记录
            db_session.add(Investment(user_id=user_id, artwork_id=artwork_id, asset=user_balance))

        db_session.commit()

        data = {"msg": "success"}
        response = build_response(data, "200")
        return response
