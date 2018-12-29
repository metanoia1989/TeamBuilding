#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from app.api import api, meta_fields
from app.extensions import auth
from app.models.category import Category as CategoryModel 
from app.lib.errors import success, execute_success
from app.lib.decorators import paginate, api_permission_control

# 请求字段过滤
category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str)
# args = category_parser.parse_args() # 解析参数

# 格式化输出
category_fields = {
    'id': fields.Integer,
    'name':fields.String, 
}

category_collection_fields = {
    'items': fields.List(fields.Nested(category_fields)),
    'meta': fields.Nested(meta_fields),
}

class CategoryApi(Resource):
    method_decorators = {
        'delete': [auth.login_required, api_permission_control()],
        'post': [auth.login_required, api_permission_control()],
        'put': [auth.login_required, api_permission_control()],
    }

    @marshal_with(category_fields)
    def get(self, id=None):
        category = CategoryModel.query.filter_by(id=id).first()
        if not category:
            abort(404)
        return category
    
    def delete(self, id=None):
        category = CategoryModel.query.filter_by(id=id).first()
        if not category:
            abort(404)
        category.delete()
        return execute_success()
    
    def post(self):
        args = category_parser.parse_args()
        # category owns the task
        category = CategoryModel.create(**args)
        return success()

    def put(self, id=0, **kwargs):
        category = CategoryModel.query.filter_by(id=id).first()
        if not category:
            abort(404)
        category.update(**category_parser.parse_args())
        return execute_success()

class CategoryCollectionApi(Resource):

    @marshal_with(category_collection_fields)
    @paginate(10)
    def get(self, category_id=None):
        categorys = CategoryModel.query
        return categorys
    
api.add_resource(CategoryApi, '/category' ,'/category/<int:id>', endpoint='category')
api.add_resource(CategoryCollectionApi, '/categorys' , endpoint='categorys')