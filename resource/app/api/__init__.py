#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
 
api = Blueprint('api', __name__)

auth = HTTPTokenAuth(scheme='Bearer')
tokens = {
    'secret-token-1': 'John',
    'secret-token-2': 'Susan',
}
# api_auth   = HTTPBasicAuth()


from . import authentication, errors