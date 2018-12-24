#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from app.api import api, meta_fields
from app.extensions import auth
from app.models.user import User 
from app.models.role import Role
from app.lib.errors import success, execute_success
from app.lib.decorators import paginate

# 请求字段过滤
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=inputs.regex('^\w([+-.]\w+)*@\w+\.\w+$'), trim=True, required=True, help='邮箱不合标准')
user_parser.add_argument('username', type=str, required=True, trim=True, help='必须填写用户名')
user_parser.add_argument('password_hash', type=str, required=True, trim=True, help='必须填写密码')
user_parser.add_argument('confirmed', type=bool, default=1)
user_parser.add_argument('name', type=str)
user_parser.add_argument('location', type=str)
user_parser.add_argument('about_me', type=str)
user_parser.add_argument('member_since', type=int)
# user_parser.add_argument('role_id', type=int, choices=Role.get_role_ids())
# args = user_parser.parse_args() # 解析参数

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

user_collection_fields = {
    'items': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}

class User(Resource):
    decorators = [auth.login_required]

    @marshal_with(user_fields)
    def get(self, id=None):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)
        return user
    
    def delete(self, id=None):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)
        user.delete()
        return execute_success()
    
    def post(self):
        args = user_parser.parse_args()
        # user owns the task
        args['author_id'] = g.current_user.id
        user = User.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)
        user.update(**user_parser.parse_args())
        return execute_success()

class UserCollection(Resource):
    decorators = [auth.login_required]

    @marshal_with(user_collection_fields)
    @paginate(10)
    def get(self, user_id=None):
        users = User.query
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                abort(404)
            users = User.query.filter_by(author_id=user.id) 
        return users

    
api.add_resource(User, '/user' ,'/user/<int:id>', endpoint='user')
api.add_resource(UserCollection, '/users' ,'/users/<int:user_id>', endpoint='users')