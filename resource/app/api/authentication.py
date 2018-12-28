#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import g, jsonify, request
from app.models.user import User
from app.api import api_blueprint
from app.lib.errors import forbidden_error, unauthorized, success
from app.extensions import auth
from werkzeug.security import generate_password_hash, check_password_hash

@auth.verify_token
def verify_token(token):
    g.current_user = User.verify_auth_token(token)
    return g.current_user is not None

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api_blueprint.route('/tokens/', methods=['POST'])
def get_token():
    json = request.get_json()
    email = json.get('email')
    password = json.get('password')
    if email == '' or password == '':
        return False
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    token = g.current_user.generate_auth_token(expiration=3600 * 24 )
    return jsonify({ "token": token, "expiration": 3600 * 24 })

@api_blueprint.route('/')
@auth.login_required
def index():
    return jsonify({ 'username': g.current_user.username })


@api_blueprint.route('/test')
@auth.login_required
def test():
    return request.endpoint