#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask_httpauth import HTTPTokenAuth
from flask import g, jsonify
from ..models import AnonymousUser, User
from . import api
from .errors import forbidden_error, unauthorized

auth = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    if token == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(email=token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return True

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden_error('Unconfirmed account')

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600
    })