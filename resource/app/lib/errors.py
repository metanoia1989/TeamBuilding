#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import jsonify
from app.api import api_blueprint
from app.extensions import auth
from app.exceptions import ValidationError

@api_blueprint.app_errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

@api_blueprint.app_errorhandler(404)
def not_found_error(e):
    return not_found()

def success(msg='ok'):
    response = jsonify({'error_code': 0, 'msg': msg})
    response.status_code = 201
    return response

def execute_success():
    response = jsonify({'error_code': 1, 'msg': 'ok'})
    response.status_code = 204
    return response

def server_error(msg='sorry, server has a mistake!'):
    response = jsonify({'error_code': 999, 'msg': msg})
    response.status_code = 500
    return response

def bad_request(msg='invalid paramter'):
    response = jsonify({'error_code': 1000, 'msg': msg})
    response.status_code = 400
    return response

def unauthorized(msg='authorization faild'):
    response = jsonify({'error_code': 1005, 'msg': msg})
    response.status_code = 401
    return response

def forbidden_error(msg='forbidden access'):
    response = jsonify({'error_code': 1003, 'msg': msg})
    response.status_code = 403
    return response

def not_found(msg='the resource are not found 0_0.'):
    response = jsonify({'error_code': 1001, 'msg': msg})
    response.status_code = 404
    return response