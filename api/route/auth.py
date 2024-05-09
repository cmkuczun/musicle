from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
sys.path.append("..")
from service.auth import *

auth_api = Blueprint('auth', __name__)

@auth_api.route('/login/', methods=['POST'])
def auth_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = login_service(username, password)
    return jsonify(user_id), HTTPStatus.OK

@auth_api.route('/register/', methods=['POST'])
def auth_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = register_service(username, password)
    return jsonify(user_id), HTTPStatus.OK
