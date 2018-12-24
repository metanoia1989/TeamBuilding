#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort, g
from flask_restful import Resource, fields, marshal_with, reqparse
from app.api import api, meta_fields
from app.api.user import user_fields
from app.api.category import category_fields
from app.extensions import auth
from app.models.resource import Resource as Resource_Model
from app.models.user import User
from app.lib.decorators import paginate
from app.lib.errors import success, execute_success

# 请求字段过滤
resource_parser = reqparse.RequestParser()
resource_parser.add_argument('title', type=str, required=True)
resource_parser.add_argument('body_md', type=str, required=True)
resource_parser.add_argument('pin', type=bool, default=False)
resource_parser.add_argument('hot', type=bool, default=False)
resource_parser.add_argument('category_id', type=int, required=True, help='必须添加标签')
resource_parser.add_argument('author_id', type=int)
# args = resource_parser.parse_args() # 解析参数

# 格式化输出
resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body_md': fields.String(default=''),
    'body_html': fields.String(default=''),
    'timestamp': fields.DateTime,
    'pin': fields.Boolean(default=False),
    'hot': fields.Boolean(default=False),
    'clicks': fields.Integer(default=0),
    'author': fields.Nested(user_fields),
    'category': fields.Nested(category_fields),
}

resource_collection_fields = {
    'items': fields.List(fields.Nested(resource_fields)),
    'meta': fields.Nested(meta_fields),
}

class Resource(Resource):
    decorators = [auth.login_required]
    @marshal_with(resource_fields)
    def get(self, id=None):
        resource = Resource_Model.query.filter_by(id=id).first()
        if not resource:
            abort(404)
        return resource
    
    def delete(self, id=None):
        resource = Resource_Model.query.filter_by(id=id).first()
        if not resource:
            abort(404)
        resource.delete()
        return execute_success()
    
    def post(self):
        args = resource_parser.parse_args()
        # user owns the task
        args['author_id'] = g.current_user.id
        resource = Resource_Model.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        resource = Resource_Model.query.filter_by(id=id).first()
        if not resource:
            abort(404)
        resource.update(**resource_parser.parse_args())
        return execute_success()

class ResourceCollection(Resource):
    decorators = [auth.login_required]

    @marshal_with(resource_collection_fields)
    @paginate(10)
    def get(self, user_id=None):
        resources = Resource_Model.query
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                abort(404)
            resources = Resource_Model.query.filter_by(author_id=user.id) 
        return resources

    
api.add_resource(Resource, '/resource' ,'/resource/<int:id>', endpoint='resource')
api.add_resource(ResourceCollection, '/resources' ,'/resources/<int:user_id>', endpoint='resources')
