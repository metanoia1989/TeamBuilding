#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint
from flask_restful import Api, fields
 
# 初始化蓝图以及restful api扩展
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

# Marshaled fields for meta section
meta_fields = {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer,
}

# 导入路由视图
from . import authentication
from . import resources
from . import user
from . import project
from . import test
