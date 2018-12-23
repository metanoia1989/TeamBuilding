#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import jsonify
from app.api import api_blueprint
from app.extensions import auth
from app.exceptions import ValidationError, ApiException
# from .authentication import auth

def forbidden_error(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

@api_blueprint.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

class Success(ApiException):
    code = 201
    error_code = 0
    msg = 'Create ok'

class ExecuteSuccess(ApiException):
    code = 204
    error_code = 1
    msg = 'Execute ok'

class ServerError(ApiException):
    code = 500
    error_code = 999
    msg = 'Sorry, server has a mistake!'

class ParameterException(ApiException):
    code = 400
    error_code = 1000
    msg = 'Invalid parameter'

class NotFound(ApiException):
    code = 404
    error_code = 1001
    msg = 'The resource are not found 0_0...'

class AuthFailed(ApiException):
    code = 401
    error_code = 1005
    msg = 'Authorization failed'

class Forbidden(ApiException):
    code = 403
    error_code = 1004
    msg = 'Forbidden access'