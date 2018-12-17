#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import g, jsonify
from ..models import User
from . import api, auth, tokens
from .errors import forbidden_error, unauthorized
from werkzeug.security import generate_password_hash, check_password_hash



users = [
    { 'username': 'Tom', 'password': generate_password_hash('111111') },
    { 'username': 'Michael', 'password': generate_password_hash('123456') },
]

# @auth.get_password
# def get_password(username):
#     for user in users:
#         if user['username'] == username:
#             return user['password']
#     return None

# @auth.verify_password
# def verify_password(username, password):
#     for user in users:
#         if user['username'] == username:
#             if check_password_hash(user['password'], generate_password_hash(password)):
#                 return True
#     return False

@auth.verify_token
def verify_token(token):
    g.user = None
    if token in tokens:
        g.user = tokens[token]
        return True
    return False

@api.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % g.user