#!/usr/bin/env python3
# -*- conding:utf8 -*-

from app.models.resource import Resource as Resource_Model
from flask_restful import Resource, fields, marshal_with, reqparse
from app.api import api
from app.extensions import auth
from flask import abort
from app.models.resource import Resource as Resource_Model
from app.models.user import User 


# 格式化输出
user_fields = {
    'id': fields.Integer,
    'role_id':fields.Integer, 
    'email': fields.String,
    'username': fields.String,
    'confirmed': fields.Boolean,
    'name': fields.String,
    'about_me': fields.String,
    'avatar_hash': fields.String,
}

