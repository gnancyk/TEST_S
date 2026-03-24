from flask import Blueprint, request, jsonify
from ..services.user_service import create_user, get_all_users

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users)

@bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    user = create_user(data)
    return jsonify(user), 201
