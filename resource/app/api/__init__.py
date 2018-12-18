#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
 
api = Blueprint('api', __name__)

auth = HTTPTokenAuth(scheme='Bearer')

from . import authentication, errors