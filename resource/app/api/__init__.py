#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint
 
api = Blueprint('api', __name__)

from . import authentication, errors