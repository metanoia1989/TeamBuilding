#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from werkzeug.security import generate_password_hash
from app.api import api, meta_fields
from app.extensions import auth
from app.models.user import User as UserModel
from app.models.role import Role as RoleModel
from app.lib.errors import success, execute_success
from app.lib.decorators import paginate

# 请求字段过滤
user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('email', type=inputs.regex('^\w+([+-.]\w+)*@\w+\.\w+$'), trim=True, required=True, help='邮箱不合标准')
user_post_parser.add_argument('username', type=str, required=True, trim=True, help='必须填写用户名')
user_post_parser.add_argument('password_hash', type=str, required=True, trim=True, help='必须填写密码')
user_post_parser.add_argument('confirmed', type=bool, default=1)
user_post_parser.add_argument('name', type=str)
user_post_parser.add_argument('location', type=str)
user_post_parser.add_argument('about_me', type=str)
user_post_parser.add_argument('member_since', type=int)
user_post_parser.add_argument('role_id', type=int)
# args = user_parser.parse_args() # 解析参数

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument('email', type=inputs.regex('^\w+([+-.]\w+)*@\w+\.\w+$'), trim=True, required=True, help='邮箱不合标准')
user_put_parser.add_argument('username', type=str, required=True, trim=True, help='必须填写用户名')
user_put_parser.add_argument('password_hash', type=str, trim=True)
user_put_parser.add_argument('confirmed', type=bool, default=1)
user_put_parser.add_argument('name', type=str)
user_put_parser.add_argument('location', type=str)
user_put_parser.add_argument('about_me', type=str)
user_put_parser.add_argument('member_since', type=int)
user_put_parser.add_argument('role_id', type=int)

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

class UserApi(Resource):
    method_decorators = {
        'delete': [auth.login_required],
        'post': [auth.login_required],
        'put': [auth.login_required],
    }

    @marshal_with(user_fields)
    def get(self, id=None):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        return user
    
    def delete(self, id=None):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        user.delete()
        return execute_success()
    
    def post(self):
        args = user_post_parser.parse_args()
        if 'password_hash' in args:
            args.password_hash = generate_password_hash(args.password_hash)
        # user owns the task
        args['author_id'] = g.current_user.id
        user = UserModel.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)

        args = user_put_parser.parse_args()
        if 'password_hash' in args:
            args.password_hash = generate_password_hash(args.password_hash)
        user.update(**args)
        return execute_success()

class UserCollectionApi(Resource):

    @marshal_with(user_collection_fields)
    @paginate(10)
    def get(self, user_id=None):
        users = UserModel.query
        return users

    
api.add_resource(UserApi, '/user' ,'/user/<int:id>', endpoint='user')
api.add_resource(UserCollectionApi, '/users', endpoint='users', methods=['GET'])