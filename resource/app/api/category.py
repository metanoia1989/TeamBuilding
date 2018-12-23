#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.models.resource import Resource as Resource_Model
from flask_restful import Resource, fields, marshal_with, reqparse
from app.api import api
from app.extensions import auth
from flask import abort
from app.models.resource import Resource as Resource_Model
from app.models.category import Category


# 格式化输出
category_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

